import pytest
from pages.login_page import LoginPage

"""
全局默认账号使用py/123456。在cases目录的conftest.py文件下
涉及多个账号切换操作的时候
我们可以创建新的上下文，用其它账号登录
管理员账号admin/123456
"""


@pytest.fixture(scope="module")
def admin_context(browser, base_url, pytestconfig, browser_context_args):
    """
    创建admin上下文, 加载admin.json数据
    :return:
    """
    context = browser.new_context(**browser_context_args)
    page = context.new_page()
    LoginPage(page).navigate()
    LoginPage(page).login("admin", "123456")
    # 等待登录成功页面重定向
    page.wait_for_url(url='**/index.html')
    yield context
    context.close()