from pages.register_page import RegisterPage
from playwright.sync_api import expect,Page
import pytest
import uuid

class TestRegister:
    """注册功能"""

    @pytest.fixture(autouse=True)
    def start_for_each(self, unlogin_page: Page):
        """
        同登录功能用独立的上下文环境，不加载cookie
        :param unlogin_page: 独立上下文
        :return: None
        """
        print("for each--start: 打开新页面访问注册页")
        self.register = RegisterPage(unlogin_page)
        self.register.navigate()
        yield
        print("for each--end: 后置操作")

    def test_01_register_success(self):
        """注册成功-未注册的1位非特殊字符账号 + 6位正确密码"""
        
        # 进行注册操作
        self.register.register(uuid.uuid4().hex[:1], "123456")
        # 断言
        expect(self.register.page).to_have_title("首页")
        expect(self.register.page).to_have_url("index.html")

    def test_02_register_success(self):
        """注册成功-未注册的10位非特殊字符账号 + 10位正确密码"""
        
        # 注册操作
        self.register.register(uuid.uuid4().hex[:10], "1234567890")
        # 断言
        expect(self.register.page).to_have_title("首页")
        expect(self.register.page).to_have_url("index.html")

    def test_03_register_success(self):
        """注册成功-未注册的30位非特殊字符账号 + 16位正确密码"""

        # 注册操作
        self.register.register(uuid.uuid4().hex[:30], "1234567890123456")
        # 断言
        expect(self.register.page).to_have_title("首页")
        expect(self.register.page).to_have_url("/index.html")

    def test_04_register_fail_username_empty(self):
        """注册失败-用户名为空"""

        # 注册操作
        self.register.register("", "123456")
        # 断言
        expect(self.register.locator_username_tip1).to_be_visible()
        expect(self.register.locator_username_tip1).to_contain_text("不能为空")
        # 按钮不可点击
        expect(self.register.locator_register_btn).not_to_be_enabled()

    def test_05_register_fail_username_len_30(self):
        """登陆失败-用户名大于30字符"""

        # 注册操作
        self.register.fill_username("123456789p123456789p123456789ps")
        # 断言
        expect(self.register.locator_username_tip2).to_be_visible()
        expect(self.register.locator_username_tip2).to_contain_text("用户名称1-30位字符")
        expect(self.register.locator_register_btn).not_to_be_enabled()

    def test_06_register_fail_username_spe_char(self):
        """注册失败-用户名有特殊字符"""

        # 注册操作
        self.register.fill_username("------")
        self.register.fill_password("123456")
        # 断言
        expect(self.register.locator_username_tip3).to_be_visible()
        expect(self.register.locator_username_tip3).to_contain_text("用户名称不能有特殊字符,请用中英文数字_")
        expect(self.register.locator_register_btn).not_to_be_enabled()

    def test_07_register_fail_password_len_5(self):
        """注册失败-密码为5位字符"""

        # 注册操作
        self.register.fill_username("i")
        self.register.fill_password("12345")
        # 断言
        expect(self.register.locator_password_tip2).to_be_visible()
        expect(self.register.locator_password_tip2).to_contain_text("密码6-16位字符")
        expect(self.register.locator_register_btn).not_to_be_enabled()

    def test_08_register_fail_password_len_17(self):
        """注册失败-密码为17位数字符"""

        # 注册操作
        self.register.fill_username("g")
        self.register.fill_password("12312312312312312")
        # 断言
        expect(self.register.locator_password_tip2).to_be_visible()
        expect(self.register.locator_password_tip2).to_contain_text("密码6-16位字符")
        expect(self.register.locator_register_btn).not_to_be_enabled()

    def test_09_register_fail_password_empty(self):
        """注册失败-密码为空"""

        # 注册操作
        self.register.register("w", "")
        # 断言
        expect(self.register.locator_password_tip1).to_be_visible()
        expect(self.register.locator_password_tip1).to_contain_text("不能为空")
        # 按钮不可点击
        expect(self.register.locator_register_btn).not_to_be_enabled()

    def test_10_register_fail_password_spe_char(self):
        """注册失败-密码为6-16位的特殊字符"""

        # 注册操作
        self.register.fill_username("i")
        self.register.fill_password("------")
        # 断言
        expect(self.register.locator_password_tip3).to_be_visible()
        expect(self.register.locator_password_tip3).to_contain_text("不能有特殊字符,请用中英文数字下划线")
        expect(self.register.locator_register_btn).not_to_be_enabled()

    def test_11_register_fail_password_error(self):
        """注册失败-已注册账号"""

        # 注册操作
        self.register.register("p", "123321")
        # 断言
        expect(self.register.locator_register_error).to_be_visible()
        expect(self.register.locator_register_error).to_contain_text("用户名已存在或不合法！")
        expect(self.register.locator_register_btn).to_be_enabled()

    def test_12_login_link(self):
        """检测跳转链接"""

        # 断言
        expect(self.register.locator_login_link).to_have_attribute("href", "login.html")
        # 点击
        self.register.click_login_link()
        expect(self.register.page).to_have_url('/login.html')
        expect(self.register.page).to_have_title('网站登录')