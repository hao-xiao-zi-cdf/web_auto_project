from playwright.sync_api import Page


class LoginPage:

    def __init__(self, page: Page):
        self.page = page
        self.locator_username = page.get_by_label("用 户 名:")
        self.locator_password = page.get_by_label("密     码:")
        self.locator_login_btn = page.locator('text=立即登录')
        self.locator_register_link = page.locator('text=没有账号？点这注册')
        # 用户名输入框提示语
        self.locator_username_tip1 = page.locator('[data-fv-validator="notEmpty"][data-fv-for="username"]')
        self.locator_username_tip2 = page.locator('[data-fv-validator="stringLength"][data-fv-for="username"]')
        self.locator_username_tip3 = page.locator('[data-fv-validator="regexp"][data-fv-for="username"]')
        # 密码输入框提示语
        self.locator_password_tip1 = page.locator('[data-fv-validator="notEmpty"][data-fv-for="password"]')
        self.locator_password_tip2 = page.locator('[data-fv-validator="stringLength"][data-fv-for="password"]')
        self.locator_password_tip3 = page.locator('[data-fv-validator="regexp"][data-fv-for="password"]')
        # 账号或密码不正确！
        self.locator_login_error = page.locator('text=账号或密码不正确！')

    def navigate(self):
        self.page.goto("/login.html")

    def fill_username(self, username):
        self.locator_username.fill(username)

    def fill_password(self, password):
        self.locator_password.fill(password)

    def click_login_button(self):
        self.locator_login_btn.click()

    def click_register_link(self):
        self.locator_register_link.click()

    def login(self, username, password) -> None:
        """完整登录操作"""
        self.locator_username.fill(username)
        self.locator_password.fill(password)
        self.locator_login_btn.click()
