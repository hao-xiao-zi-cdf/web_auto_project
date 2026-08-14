import pytest
from playwright.sync_api import sync_playwright


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
        # 等待2秒
        page.wait_for_timeout(2000)  # 等价于 time.sleep(2)
        # 关闭浏览器
        browser.close()