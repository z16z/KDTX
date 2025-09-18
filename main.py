

import pytest


# 登录接口+课程接口
import subprocess
import shutil
import os

# 定义报告路径
allure_results_dir = './report/allure-results'
allure_report_dir = './report/allure-html'

# 清理旧的报告目录
if os.path.exists(allure_report_dir):
    shutil.rmtree(allure_report_dir)

# 运行 pytest
pytest.main(['-s'])

# 运行 allure 命令生成 html 报告（相当于在终端中执行命令：allure generate ./report/allure-results --clean -o ./report/allure-html）
subprocess.run(['allure', 'generate', allure_results_dir, '--clean', '-o', allure_report_dir])

# # 登录接口
# # 定义报告路径
# allure_results_dir = './report/allure-results_login'
# allure_report_dir = './report/allure-html_login'
#
# # 清理旧的报告目录
# if os.path.exists(allure_report_dir):
#     shutil.rmtree(allure_report_dir)
#
# # 运行 pytest
# pytest.main(['-s', './script/test_05login_param.py','--alluredir=./report/allure-results_login'])
# # pytest ./script/test_06course.py --alluredir=./report/allure-results_course
# # subprocess.run(['pytest','./script/test_06course.py','--alluredir=./report/allure-results_course'])



# 运行 allure 命令生成 html 报告（相当于在终端中执行命令：allure generate ./report/allure-results --clean -o ./report/allure-html）
# subprocess.run(['allure', 'generate', './report/allure-results_login', '--clean', '-o', './report/allure-html_login'])






# 课程接口
# # 定义报告路径
# allure_results_dir = './report/allure-results_course'
# allure_report_dir = './report/allure-html_course'
#
# # 清理旧的报告目录
# if os.path.exists(allure_report_dir):
#     shutil.rmtree(allure_report_dir)
#
# # 运行 pytest
# pytest.main(['-s', './script/test_06course.py','--alluredir=./report/allure-results_course'])
# # pytest ./script/test_06course.py --alluredir=./report/allure-results_course
# # subprocess.run(['pytest','./script/test_06course.py','--alluredir=./report/allure-results_course'])
#
#
#
# # 运行 allure 命令生成 html 报告（相当于在终端中执行命令：allure generate ./report/allure-results --clean -o ./report/allure-html）
# subprocess.run(['allure', 'generate', './report/allure-results_course', '--clean', '-o', './report/allure-html_course'])
