import uuid

from pages.add_module_page import AddModulePage
from playwright.sync_api import expect, Page
import pytest
from mocks import mock_api

class TestAddModule:
    """新增模块页面"""

    @pytest.fixture(autouse=True)
    def start_for_each(self, pre_login, page: Page):
        print("for each--start: 打开添加模块页")
        self.add_module = AddModulePage(page)
        # 拦截项目选项数据，模拟返回选项
        self.add_module.page.route(**mock_api.mock_project_select_200)
        self.add_module.navigate()
        yield
        print("for each--end: 后置操作")

    def test_01_add_module_success_normal(self):
        """新增模块成功-模块名称[1-30位非特殊字符] + 所属项目已存在 + 项目描述[0-100位字符]"""
        self.add_module.add_module(uuid.uuid4().hex[:10], "test", "项目描述")
        # mock 200 成功数据
        self.add_module.page.route(**mock_api.mock_add_module_200)
        # 断言跳转到项目列表页
        with self.add_module.page.expect_navigation(url="**/list_module.html"):
            # 保存成功后，重定向到列表页
            self.add_module.click_save_module()

    def test_02_add_module_fail_name_empty(self):
        """新增模块失败-模块名称为空"""
        self.add_module.add_module("", "test", "项目描述")
        self.add_module.click_save_module()
        # 断言
        expect(self.add_module.locator_save_button).to_be_disabled()

    def test_03_add_module_fail_module_repeat(self):
        """新增模块失败-模块名重复"""
        self.add_module.add_module("t", "test", "项目描述")
        # mock 400数据
        self.add_module.page.route(**mock_api.mock_add_module_400)
        self.add_module.click_save_module()
        # 断言
        expect(self.add_module.locator_boot_box).to_contain_text('已存在')

    # def test_04_add_module_fail_name_len_31(self):
    #     """新增模块失败-模块名称31位字符"""
    #     self.add_module.add_module(uuid.uuid4().hex[:31], "test", "项目描述")
    #     # 断言
    #     expect(self.add_module.locator_save_button).to_be_disabled()
    #
    # def test_05_add_module_fail_name_spe_char(self):
    #     """新增模块失败-模块名称包含1-30位特殊字符"""
    #     self.add_module.add_module(uuid.uuid4().hex[:1] + "!@#$%^&", "test", "项目描述")
    #     # 断言
    #     expect(self.add_module.locator_save_button).to_be_disabled()
    #
    # def test_06_add_module_fail_project_none(self):
    #     """新增模块失败-所属项目为空"""
    #     self.add_module.add_module(uuid.uuid4().hex[:10], "", "项目描述")
    #     # 断言
    #     expect(self.add_module.locator_save_button).to_be_disabled()
    #
    # def test_07_add_module_fail_desc_len_101(self):
    #     """新增模块失败-项目描述101位数字符"""
    #     self.add_module.add_module(uuid.uuid4().hex[:10], "test", "." * 200)
    #     # 断言
    #     expect(self.add_module.locator_save_button).to_be_disabled()

    @pytest.mark.parametrize("module_name,module_value, module_desc", [
            [uuid.uuid4().hex[:31], "test", "项目描述"],
            [uuid.uuid4().hex[:1] + "！@#￥%^&*()", "test", "项目描述"],
            [uuid.uuid4().hex[:10], "", "项目描述"],
            [uuid.uuid4().hex[:10], "test", "." * 200]
        ])
    def test_08_add_module_fail_desc_len_101(self, module_name,module_value, module_desc):
        """参数化"""
        self.add_module.add_module(module_name, module_value, module_desc)
        # 断言
        expect(self.add_module.locator_save_button).to_be_disabled()