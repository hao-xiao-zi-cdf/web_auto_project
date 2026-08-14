from base.base_page import BasePage


class RegisterPage(BasePage):
    """注册页面"""
    # 类属性：页面元素
    username = "#username"
    password = "#password"
    register_btn = 'text=立即注册'
    login_link = 'text=已有账号？点这登录'
    # 用户名输入框提示语
    username_tip1 = '[data-fv-validator="notEmpty"][data-fv-for="username"]'
    username_tip2 = '[data-fv-validator="stringLength"][data-fv-for="username"]'
    username_tip3 = '[data-fv-validator="regexp"][data-fv-for="username"]'
    # 密码输入框提示语
    password_tip1 = '[data-fv-validator="notEmpty"][data-fv-for="password"]'
    password_tip2 = '[data-fv-validator="stringLength"][data-fv-for="password"]'
    password_tip3 = '[data-fv-validator="regexp"][data-fv-for="password"]'
    # 账号或密码不正确
    register_error = 'text=用户名已存在或不合法！'

    # 单个操作
    def fill_username(self, username):
        self.base_input(self.username, username)

    def fill_password(self, password):
        self.base_input(self.password, password)

    def click_register_button(self):
        self.base_click(self.register_btn)

    def click_login_link(self):
        self.base_click(self.login_link)

    # 完整操作
    def register(self, username, password) -> None:
        """完整注册操作"""
        self.fill_username(username)
        self.fill_password(password)
        self.click_register_button()
    