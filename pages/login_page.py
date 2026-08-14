from base import base_page


class LoginPage(base_page.BasePage):
    """
    登录页面
    """
    # 类属性：页面元素
    username = "#username"
    password = "#password"
    login_btn = 'text=立即登录'
    register_link = 'text=没有账号？点这注册'
    # 用户名输入框提示语
    username_tip1 = '[data-fv-validator="notEmpty"][data-fv-for="username"]'
    username_tip2 = '[data-fv-validator="stringLength"][data-fv-for="username"]'
    username_tip3 = '[data-fv-validator="regexp"][data-fv-for="username"]'
    # 密码输入框提示语
    password_tip1 = '[data-fv-validator="notEmpty"][data-fv-for="password"]'
    password_tip2 = '[data-fv-validator="stringLength"][data-fv-for="password"]'
    password_tip3 = '[data-fv-validator="regexp"][data-fv-for="password"]'
    # 账号或密码不正确！
    login_error = 'text=账号或密码不正确！'


    # 单个操作
    def fill_username(self, username):
        self.base_input(self.username, username)

    def fill_password(self, password):
        self.base_input(self.password, password)

    def click_login_button(self):
        self.base_click(self.login_btn)

    def click_register_link(self):
        self.base_click(self.register_link)

    def login(self, username, password) -> None:
        """完整登录操作"""
        self.fill_username(username)
        self.fill_password(password)
        self.click_login_button()