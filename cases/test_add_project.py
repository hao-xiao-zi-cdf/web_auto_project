from pages.add_project_page import AddProjectPage
from playwright.sync_api import expect, Page
import pytest
import uuid
from data import mock_api
from utils.recordlog import logs

class TestAddProject:
    """新增项目页面"""

    @pytest.fixture(autouse=True)
    def start_for_each(self, pre_login, page: Page):
        logs.info("用例前置：打开添加项目页")
        self.add_project = AddProjectPage(page)
        self.add_project.navigate()
        yield
        logs.info("用例后置：执行后置操作")

    def test_01_add_project_success_normal(self, page: Page):
        """新增项目成功-项目名称[1-30位非特殊字符] + 所属应用[0-30位非特殊字符] + 项目描述[0-200位字符]"""
        self.add_project.input_project(uuid.uuid4().hex[:10], uuid.uuid4().hex[:15], uuid.uuid4().hex[:30])
        logs.info("已填写合法项目信息，点击保存并断言跳转项目列表页")
        # 断言跳转到项目列表页
        with page.expect_navigation(url="**/list_project.html"):
            # 保存成功后，重定向到列表页
            self.add_project.click_save_button()

    def test_02_add_add_project_fail_name_exist_400(self, page: Page):
        """新增项目失败-项目名称已存在"""
        self.add_project.input_project("t", "test", "test")
        # mock 接口返回400
        page.route(**mock_api.mock_project_400)
        logs.info("已 mock 新增项目接口返回400，校验重复提示")
        self.add_project.click_save_button()
        # 校验结果 弹出框文本包含
        expect(self.add_project.locator_boot_box).to_be_visible()
        expect(self.add_project.locator_boot_box).to_contain_text('已存在')

    def test_08_add_project_fail_res_code_500(self,page: Page):
        """服务器返回500状态码"""
        self.add_project.input_project("test", "test", "test")
        # mock 接口返回500
        page.route(**mock_api.mock_project_500)
        logs.info("已 mock 新增项目接口返回500，校验异常提示")
        self.add_project.click_save_button()
        # 校验结果 弹出框文本包含
        expect(self.add_project.locator_boot_box).to_contain_text('操作异常')

    def test_03_add_project_fail_name_empty(self):
        """新增项目失败-项目名称为空"""
        self.add_project.input_project("", "test", "test")
        self.add_project.click_save_button()
        logs.info("已提交空项目名，断言保存按钮不可点击")
        # 断言
        expect(self.add_project.locator_save_button).to_be_disabled()

    # def test_04_add_project_fail_name_len_31(self):
    #     """新增项目失败-项目名称31位字符"""
    #     self.add_project.input_project(uuid.uuid4().hex[:31], "test", "test")
    #     # 断言
    #     expect(self.add_project.locator_save_button).to_be_disabled()
    #
    # def test_05_add_project_fail_name_spe_char(self):
    #     """新增项目失败-项目名称包含10位特殊字符"""
    #     self.add_project.input_project(uuid.uuid4().hex[:1] + "！@#￥%^&*()", "test", "test")
    #     # 断言
    #     expect(self.add_project.locator_save_button).to_be_disabled()
    #
    # def test_06_add_project_fail_app_len_31(self):
    #     """新增项目失败-所属应用31位字符"""
    #     self.add_project.input_project("test", uuid.uuid4().hex[:31], "test")
    #     # 断言
    #     expect(self.add_project.locator_save_button).to_be_disabled()
    #
    # def test_07_add_project_fail_app_spe_char(self):
    #     """新增项目失败-所属应用包含10位特殊字符"""
    #     self.add_project.input_project("test", uuid.uuid4().hex[:1] + "！@#￥%^&*()", "test")
    #     # 断言
    #     expect(self.add_project.locator_save_button).to_be_disabled()
    #
    # def test_08_add_project_fail_desc_len_201(self):
    #     """新增项目失败-项目描述201位字符"""
    #     self.add_project.input_project(uuid.uuid4().hex[:10],uuid.uuid4().hex[:1],"." * 200)
    #     # 断言
    #     expect(self.add_project.locator_save_button).to_be_disabled()

    # 参数化
    @pytest.mark.parametrize("name, app, desc", [
        [uuid.uuid4().hex[:31], "test", "test"],
        [uuid.uuid4().hex[:1] + "！@#￥%^&*()", "test", "test"],
        ["test", uuid.uuid4().hex[:31], "test"],
        ["test", uuid.uuid4().hex[:1] + "！@#￥%^&*()", "test"],
        ["test", "test", "." * 300]
    ])
    def test_09_add_project_fail_5(self, name, app, desc):
        """参数化-"""
        self.add_project.input_project(name, app, desc)
        logs.info(f"参数化输入：name={name}，app={app}，desc={desc}")
        # 断言
        expect(self.add_project.locator_save_button).to_be_disabled()