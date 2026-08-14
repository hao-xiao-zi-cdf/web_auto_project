from pytest import Item
from playwright.sync_api import BrowserType
from typing import Any, Dict
import allure
import pytest

# 本地插件注册
pytest_plugins = ['plugins.pytest_playwright', 'plugins.pytest_base_url_plugin']


def pytest_runtest_call(item: Item):
    # 动态添加测试类的allure.feature()
    if item.parent._obj.__doc__:
        allure.dynamic.feature(item.parent._obj.__doc__)
    # 动态添加测试用例的title标题allure.title()
    if item.function.__doc__:
        allure.dynamic.title(item.function.__doc__)


@pytest.fixture(scope="session")
def browser_type_launch_args(pytestconfig: Any) -> Dict:
    """覆盖官方插件的配置，添加窗口最大化参数"""
    launch_options = {}
    headed_option = pytestconfig.getoption("--headed")
    if headed_option:
        launch_options["headless"] = False
    else:
        launch_options["headless"] = False  # 默认显示浏览器窗口
    # 添加窗口最大化
    launch_options["args"] = ["--start-maximized"]
    return launch_options