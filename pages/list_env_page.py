from playwright.sync_api import Page
import allure


class EnvListPage:
    """环境列表页"""

    def __init__(self, page: Page):
        self.page = page
        self.locator_add_env = page.locator('#btn_add')
        self.locator_search_env = page.get_by_placeholder("环境名称")
        self.locator_search_button = page.get_by_text('搜索')
        # 新增环境模态框
        self.locator_add_modal = page.locator('#myModal')
        self.locator_modal_env_name = self.locator_add_modal.get_by_label("环境名称")
        self.locator_modal_env_address = self.locator_add_modal.get_by_label("环境地址")
        self.locator_modal_env_desc = self.locator_add_modal.get_by_label("简要描述")
        self.locator_modal_save = self.locator_add_modal.get_by_text('保存')
        self.locator_modal_dismiss = self.locator_add_modal.get_by_text("取消")
        # tips
        self.locator_modal_env_tip1 = self.locator_add_modal.locator(
            '[data-fv-validator="notEmpty"][data-fv-for="env_name"]'
        )
        self.locator_modal_env_tip2 = self.locator_add_modal.locator(
            '[data-fv-validator="stringLength"][data-fv-for="env_name"]'
        )
        self.locator_modal_env_tip3 = self.locator_add_modal.locator(
            '[data-fv-validator="regexp"][data-fv-for="env_name"]'
        )
        self.locator_modal_address_tip1 = self.locator_add_modal.locator(
            '[data-fv-validator="notEmpty"][data-fv-for="base_url"]'
        )
        self.locator_modal_address_tip2 = self.locator_add_modal.locator(
            '[data-fv-validator="stringLength"][data-fv-for="base_url"]'
        )
        self.locator_modal_address_tip3 = self.locator_add_modal.locator(
            '[data-fv-validator="regexp"][data-fv-for="base_url"]'
        )
        # boot_box 提示语
        self.locator_boot_box = page.locator('.bootbox-body')

    def navigate(self) -> None:
        with allure.step('导航到/list_env.html'):
            self.page.goto("/list_env.html")

    def click_add_env(self) -> None:
        with allure.step('点击添加环境按钮'):
            self.locator_add_env.click()

    def input_env_name(self, env_name: str) -> None:
        with allure.step(f'模态框输入环境名称: {env_name}'):
            self.locator_modal_env_name.fill(env_name)

    def input_env_address(self, env_address: str) -> None:
        with allure.step(f'模态框输入环境地址: {env_address}'):
            self.locator_modal_env_address.fill(env_address)

    def input_env_desc(self, env_desc: str) -> None:
        with allure.step(f'模态框输入简要描述: {env_desc}'):
            self.locator_modal_env_desc.fill(env_desc)

    def click_modal_save(self) -> None:
        with allure.step('点击模态框保存按钮'):
            self.locator_modal_save.click()

    def click_modal_dismiss(self) -> None:
        with allure.step('点击模态框取消按钮'):
            self.locator_modal_dismiss.click()

    # def search_project(self, name) -> None:
    #     self.locator_search_project.fill(name)
    #
    # def click_search_button(self) -> None:
    #     self.locator_search_button.click()
    #
    # def click_refresh(self) -> None:
    #     self.locator_refresh.click()
