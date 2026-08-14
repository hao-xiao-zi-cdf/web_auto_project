from base.base_page import BasePage


class AddProjectPage(BasePage):
    """新增项目页面"""
    # 页面元素
    project_name = 'label[for="project_name"]'
    publish_app = 'label[for="publish_app"]'
    project_desc = 'label[for="project_desc"]'
    save_button = '#save_project'
    boot_box = '.bootbox-body'

    # 单个操作
    def fill_project_name(self, name):
        self.base_input(self.project_name, name)

    def fill_publish_app(self, text):
        self.base_input(self.publish_app, text)

    def fill_project_desc(self, text):
        self.base_input(self.project_desc, text)

    def click_save_button(self):
        self.base_click(self.save_button)

    # 完整操作
    def input_project(self, name: str, app: str, desc: str) -> None:
        """
        新增项目
        :param name: 项目名称
        :param app: 发布app
        :param desc: 描述
        :return: None
        """
        self.fill_project_name(name)
        self.fill_publish_app(app)
        self.fill_project_desc(desc)
    