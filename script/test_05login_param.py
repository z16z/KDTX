# 数据驱动，使用yaml
import os
import pytest
import allure
import requests

from commom.yaml_utils import read_yaml,GlobalData
from api.base_api import BaseAPI

# yaml_path = '../data/login.yaml'
# cases = read_yaml(yaml_path)
# 1.读取yaml测试数据
# 获取当前脚本（test_05login_param.py）所在的绝对目录
current_script_dir = os.path.dirname(os.path.abspath(__file__))
# 向上返回一级目录（回到 KDTX/）
parent_dir = os.path.dirname(current_script_dir)
# 拼接 data/login.yaml 的路径
yaml_path = os.path.join(parent_dir, "data", "login.yaml")

cases = read_yaml(yaml_path)

class TestLogin:
    @pytest.fixture(scope='class')
    def global_test_data(self):
        """初始化全局变量管理实例"""
        test_data = GlobalData()
        return test_data

    @pytest.fixture(scope='class')
    def login_api(self,global_test_data):
        """初始化登录接口"""
        return BaseAPI(global_test_data)

    @allure.epic('KDTX')
    @allure.feature('login')
    @pytest.mark.parametrize('case',cases,ids=[i['name'] for i in cases])
    def test_login(self,login_api,case):
        """执行登录流程：先获取验证码，再登录"""
        # 1.读取yaml测试数据
        # # 获取当前脚本（test_05login_param.py）所在的绝对目录
        # current_script_dir = os.path.dirname(os.path.abspath(__file__))
        # # 向上返回一级目录（回到 KDTX/）
        # parent_dir = os.path.dirname(current_script_dir)
        # # 拼接 data/login.yaml 的路径
        # yaml_path = os.path.join(parent_dir, "data", "login.yaml")
        #
        # cases = read_yaml(yaml_path)
        # yaml_path = '../data/login.yaml'
        # cases = read_yaml(yaml_path)

        # 2.按顺序执行每个接口（依赖关系通过yaml顺序保证）
        # for case in cases:
        print(f'执行用例：{case['name']}')
        response = login_api.send_reqeust(case)
        print(f'响应状态码：{response.status_code}')
        try:
            print(f'响应体：{response.json()}')
        except requests.exceptions.JSONDecodeError:
            print(f'响应体：{response.text}')

if __name__ == '__main__':

    # pytest.main(['-s', './script/test_05login_param.py'])
    import subprocess
    import shutil
    import os

    # 定义报告路径
    allure_results_dir = './report/allure-results_login'
    allure_report_dir = './report/allure-html_login'

    # 清理旧的报告目录
    if os.path.exists(allure_report_dir):
        shutil.rmtree(allure_report_dir)

    # 运行 pytest
    pytest.main(['-s', './script/test_05login_param.py'])

    # 运行 allure 命令生成 html 报告（相当于在终端中执行命令：allure generate ./report/allure-results --clean -o ./report/allure-html）
    subprocess.run(['allure', 'generate', allure_results_dir, '--clean', '-o', allure_report_dir])

