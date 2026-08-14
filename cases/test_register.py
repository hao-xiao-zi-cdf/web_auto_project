from pages.register_page import RegisterPage
from playwright.sync_api import expect

class TestRegister:
    """注册功能"""

    def test_01_register_success(self, page):
        """注册成功-未注册的1位非特殊字符账号 + 6位正确密码"""

        # 创建注册页面对象
        register = RegisterPage(page)
        # 输出网址
        register.open_url("/register.html")
        # 进行注册操作
        register.register("m", "123456")
        # 断言
        expect(register.page).to_have_title("首页")
        expect(register.page).to_have_url("index.html")

    def test_02_register_success(self, page):
        """注册成功-未注册的10位非特殊字符账号 + 10位正确密码"""
        # 创建注册页面对象
        register = RegisterPage(page)
        # 打开网页
        register.open_url("/register.html")
        # 注册操作
        register.register("123456789m", "1234567890")
        # 断言
        expect(register.page).to_have_title("首页")
        expect(register.page).to_have_url("index.html")

    def test_03_register_success(self, page):
        """注册成功-未注册的30位非特殊字符账号 + 16位正确密码"""
        # 创建注册页面对象
        register = RegisterPage(page)
        # 打开网页
        register.open_url("/register.html")
        # 注册操作
        register.register("123456789p123456789p123456789m", "1234567890123456")
        # 断言
        expect(register.page).to_have_title("首页")
        expect(register.page).to_have_url("/index.html")

    def test_04_register_fail_username_empty(self, page):
        """注册失败-用户名为空"""
        # 创建注册页面对象
        register = RegisterPage(page)
        # 打开网页
        register.open_url("http://47.116.12.183/register.html")
        # 注册操作
        register.register("", "123456")
        # 断言
        expect(register.page.locator(RegisterPage.username_tip1)).to_be_visible()
        expect(register.page.locator(RegisterPage.username_tip1)).to_contain_text("不能为空")
        # 按钮不可点击
        expect(register.page.locator(RegisterPage.register_btn)).not_to_be_enabled()

    def test_05_register_fail_username_len_30(self, page):
        """登陆失败-用户名大于30字符"""
        # 创建注册页面对象
        register = RegisterPage(page)
        # 打开网页
        register.open_url("/register.html")
        # 注册操作
        register.fill_username("123456789p123456789p123456789ps")
        # 断言
        expect(register.page.locator(RegisterPage.username_tip2)).to_be_visible()
        expect(register.page.locator(RegisterPage.username_tip2)).to_contain_text("用户名称1-30位字符")
        expect(register.page.locator(RegisterPage.register_btn)).not_to_be_enabled()

    def test_06_register_fail_username_spe_char(self, page):
        """注册失败-用户名有特殊字符"""
        # 创建注册页面对象
        register = RegisterPage(page)
        # 打开网页
        register.open_url("/register.html")
        # 注册操作
        register.fill_username("------")
        register.fill_password("123456")
        # 断言
        expect(register.page.locator(RegisterPage.username_tip3)).to_be_visible()
        expect(register.page.locator(RegisterPage.username_tip3)).to_contain_text("用户名称不能有特殊字符,请用中英文数字_")
        expect(register.page.locator(RegisterPage.register_btn)).not_to_be_enabled()

    def test_07_register_fail_password_len_5(self, page):
        """注册失败-密码为5位字符"""
        # 创建注册页面对象
        register = RegisterPage(page)
        # 打开网页
        register.open_url("/register.html")
        # 注册操作
        register.fill_username("i")
        register.fill_password("12345")
        # 断言
        expect(register.page.locator(RegisterPage.password_tip2)).to_be_visible()
        expect(register.page.locator(RegisterPage.password_tip2)).to_contain_text("密码6-16位字符")
        expect(register.page.locator(RegisterPage.register_btn)).not_to_be_enabled()

    def test_08_register_fail_password_len_17(self, page):
        """注册失败-密码为17位数字符"""
        # 创建注册页面对象
        register = RegisterPage(page)
        # 打开网页
        register.open_url("/register.html")
        # 注册操作
        register.fill_username("g")
        register.fill_password("12312312312312312")
        # 断言
        expect(register.page.locator(RegisterPage.password_tip3)).to_be_visible()
        expect(register.page.locator(RegisterPage.password_tip3)).to_contain_text("密码6-16位字符")
        expect(register.page.locator(RegisterPage.register_btn)).not_to_be_enabled()

    def test_09_register_fail_password_empty(self, page):
        """注册失败-密码为空"""
        # 创建注册页面对象
        register = RegisterPage(page)
        # 打开网页
        register.open_url("/register.html")
        # 注册操作
        register.register("w", "")
        # 断言
        expect(register.page.locator(RegisterPage.password_tip1)).to_be_visible()
        expect(register.page.locator(RegisterPage.password_tip1)).to_contain_text("不能为空")
        # 按钮不可点击
        expect(register.page.locator(RegisterPage.register_btn)).not_to_be_enabled()

    def test_10_register_fail_password_spe_char(self, page):
        """注册失败-密码为6-16位的特殊字符"""
        # 创建注册页面对象
        register = RegisterPage(page)
        # 打开网页
        register.open_url("/register.html")
        # 注册操作
        register.fill_username("i")
        register.fill_password("------")
        # 断言
        expect(register.page.locator(RegisterPage.password_tip3)).to_be_visible()
        expect(register.page.locator(RegisterPage.password_tip3)).to_contain_text("用户名称不能有特殊字符,请用中英文数字_")
        expect(register.page.locator(RegisterPage.register_btn)).not_to_be_enabled()

    def test_11_register_fail_password_error(self, page):
        """注册失败-已注册账号"""
        # 创建注册页面对象
        register = RegisterPage(page)
        # 打开网页
        register.open_url("/register.html")
        # 注册操作
        register.register("p", "123321")
        # 断言
        expect(register.page.locator(RegisterPage.register_error)).to_be_visible()
        expect(register.page.locator(RegisterPage.register_error)).to_contain_text("用户名已存在或不合法！")
        expect(register.page.locator(RegisterPage.register_btn)).not_to_be_enabled()

    def test_12_login_link(self, page):
        """检测跳转链接"""
        # 创建注册页面对象
        register = RegisterPage(page)
        # 打开网页
        register.open_url("/register.html")
        # 断言
        expect(register.login_link).to_have_attribute('href', 'register.html')
        # 点击
        register.click_login_link()
        expect(register.page).to_have_url('/login.html')
        expect(register.page).to_have_title('网站登录')