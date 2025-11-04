import os
from commom.yaml_utils import read_yaml,GlobalData
from api.base_api import BaseAPI
import pytest
# 1.读取yaml测试数据
# 获取当前脚本（test_05login_param.py）所在的绝对目录
current_script_dir = os.path.dirname(os.path.abspath(__file__))
# 向上返回一级目录（回到 KDTX/）
parent_dir = os.path.dirname(current_script_dir)
# 拼接 data/login.yaml 的路径
yaml_path = os.path.join(parent_dir, "data", "login.yaml")

cases = read_yaml(yaml_path)

# 利用fixture来保证整个测试期间只进行一次登录操作
@pytest.fixture(scope='session')
def login_fixture():
    """这是一个专门用于获取token的前置fixture，只执行一次"""
    test_data = GlobalData()
    login_api = BaseAPI(test_data)

    current_script_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_script_dir)
    login_yaml_path = os.path.join(parent_dir,"data","login.yaml")
    cases = read_yaml(login_yaml_path)
    for case in cases:
        if case['name'] == 'login_success':
            login_api.send_reqeust(case)
            return test_data.get_variable('token')

    raise Exception("未找到login_success用例")