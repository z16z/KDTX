# 导包
import yaml
import json
from jsonpath import jsonpath

# 定义类
class TestData:
    """管理测试过程中的全局变量"""
    def __init__(self):
        self.variables = {}  # 存储键值对：{"uuid": "xxx", "token": "xxx"}

    def set_variable(self,key,value):
        """设置变量"""
        self.variables[key]=value

    def get_variable(self,key):
        """获取变量,不存在则返回None"""
        return self.variables.get(key)

def read_yaml(file_path):
    """读取yaml文件，返回列表形式的接口用例数据"""
    with open(file_path,'r',encoding='utf-8') as f:
        data = yaml.safe_load(f)
    return data if data else []

def extract_value(response_json,extract_rules):
    """
    根据提取规则（JSONPath）从响应中提取值
    :param response_json: 接口响应的json字典
    :param extract_rules: 提取字典的规则，如{"uuid":"$.uuid","token":"$.token"}
    :return: 提取的键值对字典
    """
    extracted = {}
    for key,jsonpath_expr in extract_rules.items():
        # jsonpath返回列表，取第一个元素
        value = jsonpath(response_json,jsonpath_expr)
        if value:
            extracted[key] = value[0]
    return extracted