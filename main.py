import subprocess
import shutil
import os

import pytest

# 定义报告路径
allure_results_dir = './report/allure-results'
allure_report_dir = './report/allure-html'

# 清理旧的报告目录
if os.path.exists(allure_report_dir):
    shutil.rmtree(allure_report_dir)

# 运行 pytest
pytest.main(['-s', './script/test_05login_param.py'])

# 运行 allure 命令生成 html 报告（相当于在终端中执行命令：allure generate ./report/allure-results --clean -o ./report/allure-html）
subprocess.run(['allure', 'generate', allure_results_dir, '--clean', '-o', allure_report_dir])
