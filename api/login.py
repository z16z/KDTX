# 接口封装
"""
    接口封装时，重点是依据接口文档封装接口信息，需要使用的测试数据是从测试用例传递的
    接口方法被调用时，需要返回对应的响应结果
"""

# # 1.导包
# import requests
#
# from script.test_01image import response
#
#
# # 2.创建一个类--1）初始化、2）验证码、3）登录
# class LoginAPI:
#     def __init__(self):
#         # 指定url基本信息
#         self.url_verify = 'http://kdtx-test.itheima.net/api/captchaImage'
#         self.url_login = 'http://kdtx-test.itheima.net/api/login'
#
#     def get_verify_code(self):
#         # response = requests.get(url=self.url_verify)
#         return requests.get(url=self.url_verify)
#
#     def login(self,test_data):
#         return requests.post(url=self.url_login,json=test_data)

# 导包
import requests
from commom.yaml_utils import extract_value



# 定义类
class LoginAPI:
    def __init__(self,test_data):
        # test_data是全局变量管理器，包含了需要依赖使用的变量
        self.test_data = test_data # 传入TestData实例，用于获取变量

    def _replace_variables(self,data):
        """递归替换数据中的变量引用，如{{uuid}}-->实际生成的uuid的值"""
        if isinstance(data,str):  # isinstance是用来判断是否是该数据类型，即判断data是否是字符串类型
            # 查找{{变量名}}格式的字符串并且替换
            import re
            pattern = r'\{\{(.*?)\}\}' # 正则表达式，匹配{{xxx}}格式
            matches = re.findall(pattern,data) # 提取所有{{}}中的变量名
            for var in matches:
                # 从全局变量中拿出实际值
                var_value = self.test_data.get_variable(var)
                if var_value is not None:
                    # 替换{{变量名}}为实际值
                    data = data.replace(f'{{{{{var}}}}}',str(var_value))
            return data
        elif isinstance(data,dict):
            # 递归处理字典（如请求的json参数是字典）
            return {k:self._replace_variables(v) for k,v in data.items()}
        elif isinstance(data,list):
            return [self._replace_variables(item) for item in data]
        else:
            return data

    def send_reqeust(self,case):
        """
        发送请求并处理响应
        :param case: 单条用例数据（ymal中的一个接口配置）
        :return: 响应对象
        """
        # 添加一个前置操作，检查并执行前置请求
        if 'pre_request' in case:
            self.send_reqeust(case['pre_request'])  # 递归调用自身来执行前置请求

        # 1.替换请求中的变量
        request_data = case['request']
        request_data = self._replace_variables(request_data)

        # 2.请求解析参数（从替换后的request_data中提取）
        method = request_data['method'].upper() # 请求方法转大写避免大小写问题
        url = request_data['url']
        params = request_data.get('params',{}) # GET请求的参数，如name=xxx，默认空字典
        json_data = request_data.get('json',{}) # POST请求的JSON参数
        headers = request_data.get('headers',{}) # 请求头

        # 3.发送HTTP请求
        try:
            if method == 'GET':
                response = requests.get(url=url,params=params,headers=headers)
            elif method == 'POST':
                response = requests.post(url,json=json_data,headers=headers)
            else:
                raise ValueError(f'不支持的请求方法:{method}')
        except Exception as e:
            raise Exception(f'请求发送失败：{str(e)}')

        # 5.验证响应是否符合预期（如状态码、返回msg）
        self._validate_response(response, case.get('response', {}))

        # 4.从响应中提取变量，存入全局变量
        if 'extract' in case:
            extract_rules = case['extract']
            if response.status_code == 200:
                try:
                    response_json = response.json() # 把响应体转成json字典
                    # 调用yaml_utils.py中的extract_value，根据jsonpath提取变量
                    extracted = extract_value(response_json,extract_rules)
                    # 把提取的变量存入test_data,供后续用例使用
                    for key,value in extracted.items():
                        self.test_data.set_variable(key,value)
                except requests.exceptions.JSONDecodeError:
                    print(f"警告：响应体不是有效的JSON，无法提取变量。响应内容：{response.text}")

        # 6.返回响应对象（方便测试用例后续自定义处理）
        return response


        # 响应验证
    def _validate_response(self,response,expected):
        """验证响应是否符合预期"""
        # 1.验证响应状态码
        if 'status_code' in expected:
            assert response.status_code == expected['status_code'],\
                f'状态吗不符合：预期{expected['status_code']},实际{response.status_code}'

        # 2.验证响应体json（部分字段匹配）
        if 'json' in expected:
            response_json = response.json()
            expected_json = expected['json']
            # 遍历预期中每一个字段，验证实际响应是否包含且值一致
            for key,expect_value in expected_json.items():
                actual_value = response_json.get(key)
                assert actual_value == expect_value,\
                f'响应字段[{key}]不一致:预期{expect_value}，实际{actual_value}'




