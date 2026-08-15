from playwright.sync_api import expect, Page
import pytest
import uuid
from mocks import mock_api
from pages.list_env_page import EnvListPage


class TestEnvList:
    """环境列表页面"""

    @pytest.fixture(autouse=True)
    def start_for_each(self, pre_login, page: Page):
        print("for each--start: 打开环境列表页")
        self.env = EnvListPage(page)
        self.env.navigate()
        yield
        print("for each--end: 后置操作")

    def test_01_add_env_success_normal(self):
        """新增环境成功-环境名称[1,40位非特殊字符未存在] + 环境地址http://开头<=200字符 + 简要描述<=100字符"""
        #  弹出新增框
        self.env.click_add_env()
        # 断言模态框不隐藏
        expect(self.env.locator_add_modal).not_to_be_hidden()
        # 输入环境配置信息
        self.env.add_env(uuid.uuid4().hex[:10], "http://test_env.com", "this is a test env")
        # mock 返回200 成功
        self.env.page.route(**mock_api.mock_add_env_200)
        self.env.click_modal_save()
        # 验证新增环境成功
        expect(self.env.locator_add_modal).not_to_be_visible()

    def test_02_add_env_fail_name_too_short(self):
        """新增环境成功-环境名称为2位"""
        self.env.click_add_env()
        # 断言模态框不隐藏
        expect(self.env.locator_add_modal).not_to_be_hidden()
        self.env.add_env("ab", "http://test_env.com", "this is a test env")
        self.env.click_modal_save()
        # 验证新增环境成功
        expect(self.env.locator_add_modal).not_to_be_visible()

    def test_03_add_env_fail_name_empty(self):
        """新增环境失败-环境名称为0位"""
        self.env.click_add_env()
        # 断言模态框不隐藏
        expect(self.env.locator_add_modal).not_to_be_hidden()
        self.env.add_env("", "http://test_env.com", "this is a test env")
        self.env.click_modal_save()
        # 验证新增环境失败
        expect(self.env.locator_modal_env_tip1).to_be_visible()
        expect(self.env.locator_modal_env_tip1).to_have_text('不能为空')

    def test_04_add_env_fail_name_too_long(self):
        """新增环境失败-环境名称>40位"""
        self.env.click_add_env()
        # 断言模态框不隐藏
        expect(self.env.locator_add_modal).not_to_be_hidden()
        self.env.add_env("a" * 50, "http://test_env.com", "this is a test env")
        expect(self.env.locator_modal_env_tip2).to_be_visible()
        expect(self.env.locator_modal_env_tip2).to_contain_text('模块名称1-40位字符')

    def test_05_add_env_fail_name_spe_char(self):
        """新增环境失败-环境名称包含[1,40]位特殊字符"""
        self.env.click_add_env()
        # 断言模态框不隐藏
        expect(self.env.locator_add_modal).not_to_be_hidden()
        self.env.add_env("!@#$%^", "http://test_env.com", "this is a test env")
        expect(self.env.locator_modal_env_tip3).to_be_visible()
        expect(self.env.locator_modal_env_tip3).to_contain_text('模块名称不能有特殊字符')

    def test_06_add_env_fail_name_exist(self):
        """新增环境失败-环境名称已存在"""
        self.env.click_add_env()
        # 断言模态框不隐藏
        expect(self.env.locator_add_modal).not_to_be_hidden()
        self.env.add_env("test", "http://test_env.com", "this is a test env")
        # mock模拟返回400
        self.env.page.route(**mock_api.mock_add_env_400)
        self.env.click_modal_save()
        # 验证弹窗信息
        expect(self.env.locator_boot_box).to_be_visible()
        expect(self.env.locator_boot_box).to_have_text('操作异常：{"env_name":"env_name: test 已存在"}')

    # 参数化
    @pytest.mark.parametrize("address", ["httppp", "httpx://test_env.com", "httpsx://test_env.com"])
    def test_07_add_env_fail_address_no_http(self, address):
        """新增环境失败-环境地址非http://或https://开头"""
        self.env.click_add_env()
        expect(self.env.locator_add_modal).not_to_be_hidden()
        self.env.add_env(uuid.uuid4().hex[:10], address, "this is a test env")
        self.env.click_modal_save()
        # 验证弹窗信息
        expect(self.env.locator_boot_box).to_be_visible()
        expect(self.env.locator_boot_box).to_have_text('操作异常：{"base_url":"base_url must start with http:// or https://"}')

    def test_08_add_env_fail_address_empty(self):
        """新增环境失败-环境地址为空"""
        self.env.click_add_env()
        expect(self.env.locator_add_modal).not_to_be_hidden()
        self.env.add_env(uuid.uuid4().hex[:10], "", "this is a test env")
        self.env.click_modal_save()
        # 验证
        expect(self.env.locator_modal_address_tip1).to_be_visible()
        expect(self.env.locator_modal_address_tip1).to_have_text('不能为空')

    def test_09_add_env_fail_address_too_long(self):
        """新增环境失败-环境地址>200字符"""
        self.env.click_add_env()
        expect(self.env.locator_add_modal).not_to_be_hidden()
        self.env.add_env(uuid.uuid4().hex[:10], "http://test_env.com" * 30, "this is a test env")
        # 验证
        expect(self.env.locator_modal_address_tip2).to_be_visible()
        expect(self.env.locator_modal_address_tip2).to_contain_text('模块名称1-200位字符')

    def test_10_add_env_fail_desc_too_long(self):
        """新增环境失败-简要描述>100字符"""
        self.env.click_add_env()
        expect(self.env.locator_add_modal).not_to_be_hidden()
        self.env.add_env(uuid.uuid4().hex[:10], "http://test_env.com", "this is a test env" * 10)
        # 验证
        expect(self.env.locator_modal_simple_desc_tip).to_be_visible()
        expect(self.env.locator_modal_simple_desc_tip).to_contain_text('最大100位字符')

    def test_11_click_cancel_button(self):
        """点击取消按钮返回上一页"""
        self.env.click_add_env()
        expect(self.env.locator_add_modal).not_to_be_hidden()
        self.env.add_env(uuid.uuid4().hex[:10], "http://test_env.com", "this is a test env")
        # 点击取消按钮
        self.env.click_modal_dismiss()
        # 验证
        # 断言模态框不显示
        expect(self.env.locator_add_modal).not_to_be_visible()