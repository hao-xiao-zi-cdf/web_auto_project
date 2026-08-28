"""
整个项目中可以用的上下文用3个
page  用例中直接传page，默认使用登录后的context上下文创建的page对象
login_context  专门针对登录的用例创建的上下文，与其他环境隔离
admin_context  针对admin用户登录后的上下文环境
"""
from playwright.sync_api import BrowserContext, Page
import pytest
import uuid
from pages.add_project_page import AddProjectPage
from pages.project_list_page import ProjectListPage
from utils.recordlog import logs


class TestMoreAccounts:

    @pytest.fixture(autouse=True)
    def start_for_each(self, pre_login, page: Page, admin_context: BrowserContext):
        logs.info("用例前置：双账号分别打开添加项目页与项目列表页")
        # 用户1
        self.user1_project = AddProjectPage(page)
        self.user1_project.navigate()
        # 用户2
        page2 = admin_context.new_page()
        self.user2_project = ProjectListPage(page2)
        self.user2_project.navigate()
        yield
        logs.info("用例后置：执行后置操作")

    def test_delete_project(self):
        """
        测试流程：
        step--A账号登录，创建项目xxx
        step--B账号登录，删除项目xxx
        :return:
        """
        # 账号 1 添加项目
        test_project_name = str(uuid.uuid4()).replace('-', '')[:25]
        logs.info(f"账号1创建项目：{test_project_name}")
        self.user1_project.input_project(test_project_name,"xx","xxx")
        # 断言跳转到项目列表页
        with self.user1_project.page.expect_navigation(url="**/list_project.html"):
            # 保存成功后，重定向到列表页
            self.user1_project.click_save_button()

        # 账号 2 操作删除
        logs.info(f"账号2搜索并删除项目：{test_project_name}")
        self.user2_project.search_project(test_project_name)
        with self.user2_project.page.expect_request("**/api/project**"):
            self.user2_project.click_search_button()
        self.user2_project.page.wait_for_timeout(3000)
        self.user2_project.locator_table_delete.click()
        # 确定删除
        with self.user2_project.page.expect_response("**/api/project**") as resp:
            self.user2_project.locator_boot_box_accept.click()
        # 断言删除成功
        resp_obj = resp.value
        logs.info(f"删除接口响应状态码：{resp_obj.status}")
        assert resp_obj.status == 200
