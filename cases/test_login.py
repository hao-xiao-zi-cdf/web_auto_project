from playwright.sync_api import expect
from pages.login_page import LoginPage


class TestLogin:
    """登录页面"""

    def test_01_login_success(self, page):
        """登录成功-已注册的1位非特殊字符账号 + 6位正确密码"""

        # 创建登录页面对象
        login = LoginPage(page)
        # 输出网址
        login.open_url("/login.html")
        # 进行登录操作
        login.login("p","123456")
        # 断言
        expect(login.page).to_have_title("首页")
        expect(login.page).to_have_url("index.html")

    def test_02_login_success(self, page):
        """登录成功-已注册的10位非特殊字符账号 + 10位正确密码"""
        # 创建登录页面对象
        login = LoginPage(page)
        # 打开网页
        login.open_url("/login.html")
        # 登录操作
        login.login("123456789p","1234567890")
        # 断言
        expect(login.page).to_have_title("首页")
        expect(login.page).to_have_url("index.html")

    def test_03_login_success(self, page):
        """登录成功-已注册的30位非特殊字符账号 + 16位正确密码"""
        # 创建登录页面对象
        login = LoginPage(page)
        # 打开网页
        login.open_url("/login.html")
        # 登录操作
        login.login("123456789p123456789p123456789p", "1234567890123456")
        # 断言
        expect(login.page).to_have_title("首页")
        expect(login.page).to_have_url("/index.html")

    def test_04_login_fail_username_empty(self, page):
        """登录失败-用户名为空"""
        # 创建登录页面对象
        login = LoginPage(page)
        # 打开网页
        login.open_url("http://47.116.12.183/login.html")
        # 登录操作
        login.login("", "123456")
        # 断言
        expect(login.page.locator(LoginPage.username_tip1)).to_be_visible()
        expect(login.page.locator(LoginPage.username_tip1)).to_contain_text("不能为空")
        # 按钮不可点击
        expect(login.page.locator(LoginPage.login_btn)).not_to_be_enabled()

    def test_05_login_fail_username_len_30(self, page):
        """登陆失败-用户名大于30字符"""
        # 创建登录页面对象
        login = LoginPage(page)
        # 打开网页
        login.open_url("/login.html")
        # 登录操作
        login.fill_username("123456789p123456789p123456789ps")
        # 断言
        expect(login.page.locator(LoginPage.username_tip2)).to_be_visible()
        expect(login.page.locator(LoginPage.username_tip2)).to_contain_text("用户名称1-30位字符")
        expect(login.page.locator(LoginPage.login_btn)).not_to_be_enabled()

    def test_06_login_fail_username_spe_char(self, page):
        """登录失败-用户名有特殊字符"""
        # 创建登录页面对象
        login = LoginPage(page)
        # 打开网页
        login.open_url("/login.html")
        # 登录操作
        login.fill_username("-------")
        login.fill_password("123456")
        # 断言
        expect(login.page.locator(LoginPage.username_tip3)).to_be_visible()
        expect(login.page.locator(LoginPage.username_tip3)).to_contain_text("用户名称不能有特殊字符,请用中英文数字_")
        expect(login.page.locator(LoginPage.login_btn)).not_to_be_enabled()

    def test_07_login_fail_password_len_5(self, page):
        """登录失败-密码为5位字符"""
        # 创建登录页面对象
        login = LoginPage(page)
        # 打开网页
        login.open_url("/login.html")
        # 登录操作
        login.fill_username("p")
        login.fill_password("12345")
        # 断言
        expect(login.page.locator(LoginPage.password_tip2)).to_be_visible()
        expect(login.page.locator(LoginPage.password_tip2)).to_contain_text("密码6-16位字符")
        expect(login.page.locator(LoginPage.login_btn)).not_to_be_enabled()

    def test_08_login_fail_password_len_17(self, page):
        """登录失败-密码为17位数字符"""
        # 创建登录页面对象
        login = LoginPage(page)
        # 打开网页
        login.open_url("/login.html")
        # 登录操作
        login.fill_username("p")
        login.fill_password("12312312312312312")
        # 断言
        expect(login.page.locator(LoginPage.password_tip3)).to_be_visible()
        expect(login.page.locator(LoginPage.password_tip3)).to_contain_text("密码6-16位字符")
        expect(login.page.locator(LoginPage.login_btn)).not_to_be_enabled()

    def test_09_login_fail_password_empty(self, page):
        """登录失败-密码为空"""
        # 创建登录页面对象
        login = LoginPage(page)
        # 打开网页
        login.open_url("/login.html")
        # 登录操作
        login.login("p", "")
        # 断言
        expect(login.page.locator(LoginPage.password_tip1)).to_be_visible()
        expect(login.page.locator(LoginPage.password_tip1)).to_contain_text("不能为空")
        # 按钮不可点击
        expect(login.page.locator(LoginPage.login_btn)).not_to_be_enabled()

    def test_10_login_fail_password_spe_char(self, page):
        """登录失败-密码为6-16位的特殊字符"""
        # 创建登录页面对象
        login = LoginPage(page)
        # 打开网页
        login.open_url("/login.html")
        # 登录操作
        login.fill_username("p")
        login.fill_password("------")
        # 断言
        expect(login.page.locator(LoginPage.password_tip3)).to_be_visible()
        expect(login.page.locator(LoginPage.password_tip3)).to_contain_text("用户名称不能有特殊字符,请用中英文数字_")
        expect(login.page.locator(LoginPage.login_btn)).not_to_be_enabled()

    def test_11_login_fail_password_error(self, page):
        """登录失败-6-16位的字符的不正确密码"""
        # 创建登录页面对象
        login = LoginPage(page)
        # 打开网页
        login.open_url("/login.html")
        # 登录操作
        login.login("p", "123321")
        # 断言
        expect(login.page.locator(LoginPage.login_error)).to_be_visible()
        expect(login.page.locator(LoginPage.login_error)).to_contain_text("账号或密码不正确！")
        expect(login.page.locator(LoginPage.login_btn)).not_to_be_enabled()

    def test_12_login_link(self, page):
        """检测跳转链接"""
        # 创建登录页面对象
        login = LoginPage(page)
        # 打开网页
        login.open_url("/login.html")
        # 断言
        expect(login.register_link).to_have_attribute('href', 'register.html')
        # 点击
        login.click_register_link()
        expect(login.page).to_have_url('/register.html')
        expect(login.page).to_have_title('注册')