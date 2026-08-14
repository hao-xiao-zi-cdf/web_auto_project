from playwright.sync_api import Page

class AddProjectPage:
    """新增项目页面"""

    def __init__(self,page : Page):
        self.page = page
        # 页面元素
        self.locator_project_name = page.get_by_label("项目名称:")
        self.locator_publish_app = page.get_by_label("所属应用:")
        self.locator_project_desc = page.get_by_label('项目描述:')
        self.locator_save_button = page.get_by_text('点击提交')
        self.locator_boot_box = page.locator('.bootbox-body')

    # 单个操作
    def navigate(self):
        self.page.goto("/add_project.html")

    def fill_project_name(self, name):
        self.locator_project_name.fill(name)

    def fill_publish_app(self, text):
        self.locator_publish_app.fill(text)

    def fill_project_desc(self, text):
        self.locator_project_desc.fill(text)

    def click_save_button(self):
        self.locator_save_button.click()

    # 完整操作
    def input_project(self, name: str, app: str, desc: str) -> None:
        """
        新增项目
        :param name: 项目名称
        :param app: 发布app
        :param desc: 描述
        :return: None
        """
        self.locator_project_name.fill(name)
        self.locator_publish_app.fill(app)
        self.locator_project_desc.fill(desc)