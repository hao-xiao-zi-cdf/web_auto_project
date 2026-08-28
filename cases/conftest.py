import pytest
from pages.login_page import LoginPage
from typing import Any, List, Dict
from playwright.sync_api import BrowserContext, Page
from plugins.pytest_playwright import save_video_artifacts
from utils.recordlog import logs

@pytest.fixture(scope="session")
def pre_login(context, base_url) -> None:
    """有些网站网页关闭cookie就失效了，全局登录一次"""
    logs.info(f"全局预登录，测试环境 base_url：{base_url}")
    page = context.new_page()
    LoginPage(page).page.goto("/login.html")
    LoginPage(page).login("p", "123456")
    # 等待登录成功页面重定向
    page.wait_for_url(url='**/index.html')

@pytest.fixture(scope="module")
def fresh_context(browser, browser_context_args: Dict):
    """
    登录注册页面（不依赖于先登录）单独创建独立的 context 上下文
    避免全局先登录加载cookie，导致有些打开登录页直接跳到首页去了
    :return:
    """
    context = browser.new_context(**browser_context_args)
    yield context
    context.close()

@pytest.fixture
def unlogin_page(fresh_context: BrowserContext, pytestconfig: Any, request: pytest.FixtureRequest):
    """
    登录注册页面（不依赖于先登录）单独创建独立的 page 对象
    失败截图由 conftest.py 的 pytest_runtest_makereport 钩子在 call 阶段采集并附加到用例主体，
    录屏在页面关闭后保存并暂存路径，由同一钩子在 teardown 阶段统一附加到用例主体
    """
    pages: List[Page] = []

    def _on_page(page: Page) -> None:
        pages.append(page)

    fresh_context.on("page", _on_page)
    page = fresh_context.new_page()
    yield page
    # 收尾时移除监听器，避免向 module 级 context 重复注册导致 pages 列表不断累积
    fresh_context.remove_listener("page", _on_page)
    page.close()
    # 保存录屏并暂存路径（公共逻辑见插件的 save_video_artifacts 函数），
    # 由根 conftest.py 的 makereport 钩子在 teardown 阶段统一附加到用例主体；
    # 必须在 page.close() 之后，录屏文件才会落盘
    save_video_artifacts(pages, pytestconfig, request)
