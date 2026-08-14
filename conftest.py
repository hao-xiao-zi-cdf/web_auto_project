from playwright.sync_api import sync_playwright
from pytest import Item
import allure
import pytest
from typing import Dict

# 本地插件注册
pytest_plugins = ['plugins.pytest_playwright', 'plugins.pytest_base_url_plugin']


def pytest_runtest_call(item: Item):
    # 动态添加测试类的allure.feature()
    if item.parent._obj.__doc__:
        allure.dynamic.feature(item.parent._obj.__doc__)
    # 动态添加测试用例的title标题allure.title()
    if item.function.__doc__:
        allure.dynamic.title(item.function.__doc__)

@pytest.fixture(scope="function")
def page():
    """
    启动浏览器，并返回page对象
    """
    with sync_playwright() as p:
        # 启动chrome浏览器,显示界面，需要开启最大化
        browser = p.chromium.launch(headless=False, args=["--start-maximized"])
        # 创建浏览器上下文（独立浏览器环境，不污染其他账号/数据），不显示窗口大小
        context = browser.new_context(no_viewport=True)
        # 创建浏览器窗口
        page = context.new_page()
        yield page  # 返回page对象
        # 关闭浏览器
        browser.close()