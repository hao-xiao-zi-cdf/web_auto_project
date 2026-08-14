from pages.login_page import LoginPage
from playwright.sync_api import expect, Page
import pytest


class TestLogin:
    """登录页面"""

    @pytest.fixture(autouse=True)
    def start_for_each(self, unlogin_page: Page):
        """
        登录功能用独立的上下文环境，不加载cookie
        :param unlogin_page: 独立上下文
        :return: None
        """
        print("for each--start: 打开新页面访问登录页")
        self.login = LoginPage(unlogin_page)
        self.login.navigate()
        yield
        print("for each--end: 后置操作")

    def test_01_login_success(self):
        """登录成功-已注册的1位非特殊字符账号 + 6位正确密码"""

        # 进行登录操作
        self.login.login("p","123456")
        # 断言
        expect(self.login.page).to_have_title("首页")
        expect(self.login.page).to_have_url("index.html")

    def test_02_login_success(self):
        """登录成功-已注册的10位非特殊字符账号 + 10位正确密码"""

        # 登录操作
        self.login.login("123456789p","1234567890")
        # 断言
        expect(self.login.page).to_have_title("首页")
        expect(self.login.page).to_have_url("index.html")

    def test_03_login_success(self):
        """登录成功-已注册的30位非特殊字符账号 + 16位正确密码"""

        # 登录操作
        self.login.login("123456789p123456789p123456789p", "1234567890123456")
        # 断言
        expect(self.login.page).to_have_title("首页")
        expect(self.login.page).to_have_url("/index.html")

    def test_04_login_fail_username_empty(self):
        """登录失败-用户名为空"""

        # 登录操作
        self.login.login("", "123456")
        # 断言
        expect(self.login.locator_username_tip1).to_be_visible()
        expect(self.login.locator_username_tip1).to_contain_text("不能为空")
        # 按钮不可点击
        expect(self.login.locator_login_btn).not_to_be_enabled()

    def test_05_login_fail_username_len_30(self):
        """登陆失败-用户名大于30字符"""

        # 登录操作
        self.login.fill_username("123456789p123456789p123456789ps")
        # 断言
        expect(self.login.locator_username_tip2).to_be_visible()
        expect(self.login.locator_username_tip2).to_contain_text("用户名称1-30位字符")
        expect(self.login.locator_login_btn).not_to_be_enabled()

    def test_06_login_fail_username_spe_char(self):
        """登录失败-用户名有特殊字符"""

        # 登录操作
        self.login.fill_username("-------")
        self.login.fill_password("123456")
        # 断言
        expect(self.login.locator_username_tip3).to_be_visible()
        expect(self.login.locator_username_tip3).to_contain_text("用户名称不能有特殊字符,请用中英文数字_")
        expect(self.login.locator_login_btn).not_to_be_enabled()

    def test_07_login_fail_password_len_5(self):
        """登录失败-密码为5位字符"""

        # 登录操作
        self.login.fill_username("p")
        self.login.fill_password("12345")
        # 断言
        expect(self.login.locator_password_tip2).to_be_visible()
        expect(self.login.locator_password_tip2).to_contain_text("密码6-16位字符")
        expect(self.login.locator_login_btn).not_to_be_enabled()

    def test_08_login_fail_password_len_17(self):
        """登录失败-密码为17位数字符"""

        # 登录操作
        self.login.fill_username("p")
        self.login.fill_password("12312312312312312")
        # 断言
        expect(self.login.locator_password_tip2).to_be_visible()
        expect(self.login.locator_password_tip2).to_contain_text("密码6-16位字符")
        expect(self.login.locator_login_btn).not_to_be_enabled()

    def test_09_login_fail_password_empty(self):
        """登录失败-密码为空"""

        # 登录操作
        self.login.login("p", "")
        # 断言
        expect(self.login.locator_password_tip1).to_be_visible()
        expect(self.login.locator_password_tip1).to_contain_text("不能为空")
        # 按钮不可点击
        expect(self.login.locator_login_btn).not_to_be_enabled()

    def test_10_login_fail_password_spe_char(self):
        """登录失败-密码为6-16位的特殊字符"""

        # 登录操作
        self.login.fill_username("p")
        self.login.fill_password("------")
        # 断言
        expect(self.login.locator_password_tip3).to_be_visible()
        expect(self.login.locator_password_tip3).to_contain_text("不能有特殊字符,请用中英文数字下划线")
        expect(self.login.locator_login_btn).not_to_be_enabled()

    def test_11_login_fail_password_error(self):
        """登录失败-6-16位的字符的不正确密码"""

        # 登录操作
        self.login.login("p", "123321")
        # 断言
        expect(self.login.locator_login_error).to_be_visible()
        expect(self.login.locator_login_error).to_contain_text("账号或密码不正确！")
        expect(self.login.locator_login_btn).to_be_enabled()

    def test_12_login_link(self):
        """检测跳转链接"""

        # 断言
        expect(self.login.locator_register_link).to_have_attribute('href', 'register.html')
        # 点击
        self.login.click_register_link()
        expect(self.login.page).to_have_url('/register.html')
        expect(self.login.page).to_have_title('注册')