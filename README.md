# 客达天下CRM - 接口自动化测试框架

## 1. 项目简介

本项目是针对“客达天下”CRM管理系统 的后端API进行的全流程接口自动化测试。

项目基于 Python 搭建，实现了对**登录、课程管理、合同管理**等核心模块的自动化测试，旨在提高回归测试效率，保障接口质量。

## 2. 核心技术栈

* **测试框架**: `Pytest`
* **HTTP请求库**: `Requests`
* **测试报告**: `Allure`
* **数据驱动**: `PyYAML` (用于管理测试数据)
* **动态参数**: `JsonPath` (用于提取和传递接口响应值)
* **版本控制**: `Git`

## 3. 框架设计亮点

* **分层设计**：
    * `api/`: 接口封装层，封装了`BaseAPI`类，统一处理请求发送、断言和变量替换。
    * `data/`: 数据对象层，使用 YAML 文件管理测试数据，实现数据与逻辑分离。
    * `script/`: 测试用例层，使用 Pytest 编写测试脚本，通过 `@pytest.mark.parametrize` 实现数据驱动。
    * `commom/`: 公共工具层，封装了 `yaml_utils.py` 和 `file_utils.py` 等。
    * `main.py`: 统一的执行入口。

* **动态依赖处理**：
    * 使用 `pytest.fixture(scope='session')` 实现全局登录，一次登录获取`token`，供后续所有接口使用。
    * 在YAML中设计了 `pre_request` 关键字，处理“获取验证码 -> 登录”这样的接口依赖。
    * 使用 `extract` 关键字和 `{{variable}}` 语法，实现了接口间（如“查询合同 -> 删除合同”）的动态参数传递。

* **文件上传支持**：
    * 通过 `file_utils.py` 封装了文件读取逻辑，支持 `multipart/form-data` 类型的文件上传接口测试（如“上传合同”功能）。

* **报告自动化**：
    * 集成 Allure 报告，`main.py` 脚本会自动清理旧报告、执行测试、并生成新的Web报告。

## 4. 如何运行

**1. 环境准备**

* 确保已安装 `Python 3.x`
* 确保已安装 `Java JDK 8+` (Allure 报告需要)
* 确保已安装 `Allure` 命令行工具 (执行 `allure --version` 检查)
* 克隆本项目:
    ```bash
    git clone [你项目的Git仓库HTTPS链接]
    ```
* 进入项目目录:
    ```bash
    cd KDTX
    ```

**2. 安装依赖**


    ```bash
    pip install -r requirements.txt
    ```

**3. 执行测试**

* 直接运行 `main.py` 即可（推荐）：
    ```bash
    python main.py
    ```
* `main.py` 会自动执行所有 `script/` 下的测试，并在 `report/allure-html` 目录下生成报告。

**4. 查看报告**

* 脚本执行完毕后，会自动在 `report/allure-html` 目录下生成报告，在浏览器中打开 `index.html` 即可查看。
* (或者手动启动 Allure 服务):
    ```bash
    allure serve report/allure-results
    ```

## 5. Allure 报告示例

*（这里一定要放一张你本地生成的Allure报告的 **概览页(Overview)** 截图，展示出通过率、测试用例分布等，这是最有说服力的）*

![Allure Report](allure.png)
