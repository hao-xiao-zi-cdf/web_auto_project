import uuid
from time import sleep

import pytest
from pages.project_list_page import ProjectListPage, Page
from playwright.sync_api import expect
from data import mock_api
from utils.recordlog import logs


class TestProjectList:
    """项目列表"""

    @pytest.fixture(autouse=True)
    def start_for_each(self, pre_login, page: Page):
        logs.info("用例前置：打开项目列表页")
        self.project = ProjectListPage(page)
        self.project.navigate()
        yield
        logs.info("用例后置：执行后置操作")

    def test_01_project_list_add_project_success(self):
        """新增项目成功"""
        self.project.click_add_project()
        self.project.add_project(uuid.uuid4().hex[:10], "dcsdcsc3", "123456")
        # 模拟mock返回200
        self.project.page.route(**mock_api.mock_project_200)
        logs.info("已填写项目信息并 mock 返回200，断言模态框关闭并回到项目列表")
        self.project.locator_modal_save.click()
        # 断言模态框不显示，并且回到项目列表页
        expect(self.project.locator_add_modal).not_to_be_visible()
        expect(self.project.locator_panel_heading_project_list).to_have_text("项目列表")

    def test_02_project_list_add_project_fail_name_empty(self):
        """新增项目失败-项目名为空"""
        self.project.click_add_project()
        self.project.add_project("", "dcsdcsc3", "123456")
        logs.info("已提交空项目名，断言模态框不隐藏")
        self.project.locator_modal_save.click()
        # 断言模态框不隐藏
        expect(self.project.locator_add_modal).not_to_be_hidden()

    def test_03_project_list_add_project_fail_name_repeat_400(self):
        """新增项目失败-项目名重复已存在"""
        self.project.click_add_project()
        self.project.add_project("yo yo","dcsdcsc3","123456")
        # mock模拟返回400
        self.project.page.route(**mock_api.mock_project_400)
        logs.info("已 mock 新增项目接口返回400，校验重复提示弹窗")
        self.project.locator_modal_save.click()
        # 弹窗判断
        expect(self.project.locator_boot_box).to_contain_text("已存在")

    def test_04_project_list_add_project_fail_server_500(self):
        """新增项目失败-服务器返回500"""
        self.project.click_add_project()
        self.project.add_project("test","dcsdcsc3","123456")
        # 模拟mock返回500
        self.project.page.route(**mock_api.mock_project_500)
        logs.info("已 mock 新增项目接口返回500，校验异常提示弹窗")
        self.project.locator_modal_save.click()
        # 弹窗判断
        expect(self.project.locator_boot_box).to_contain_text("操作异常")

    def test_05_project_list_add_project_click_cancel_button(self):
        """点击取消按钮返回上一页"""
        self.project.click_add_project()
        self.project.add_project("iii", "dcsdcsc3", "123456")
        logs.info("已填写项目信息，点击取消按钮校验模态框关闭")
        self.project.locator_modal_dismiss.click()
        # 断言模态框不显示
        expect(self.project.locator_add_modal).not_to_be_visible()

    def test_06_project_list_search_project_ajax(self):
        """项目列表搜索功能，点搜索按钮查询请求"""
        self.project.search_project("test")
        logs.info("点击搜索按钮，拦截并断言搜索请求")
        # 点搜索按钮
        with self.project.page.expect_request('**/api/project**') as req:
            self.project.click_search_button()
        # 断言搜索请求参数
        assert "project_name=test" in req.value.url
        assert req.value.method == "GET"

    def test_07_project_list_search_project_0(self):
        """项目列表页搜索功能， 模拟搜索0个结果"""
        self.project.search_project("test")
        # 期望输入框有内容
        expect(self.project.locator_search_project).to_have_value('test')
        # 模拟mock返回0个结果
        self.project.page.route(**mock_api.mock_project_search_0)
        logs.info("已 mock 搜索返回0条结果，断言无匹配记录提示")
        self.project.click_search_button()
        # 断言搜索结果为0
        expect(self.project.locator_table_tr).to_contain_text('没有找到匹配的记录')

    def test_08_project_list_search_project_1(self):
        """项目列表页搜索功能， 模拟搜索一个结果"""
        self.project.search_project("test")
        # 期望输入框有内容
        expect(self.project.locator_search_project).to_have_value('test')
        # 模拟mock返回1个结果
        self.project.page.route(**mock_api.mock_project_search_1)
        logs.info("已 mock 搜索返回1条结果，断言搜索结果行数")
        self.project.click_search_button()
        # 期望结果 值搜索一个值
        expect(self.project.locator_table_tr).to_have_count(1)

    def test_09_project_list_refresh_project_ajax(self):
        """项目列表刷新功能，点刷新按钮查询请求"""
        logs.info("点击刷新按钮，拦截并断言刷新请求")
        with self.project.page.expect_request('**/api/project**') as req:
            self.project.click_refresh()

        # 断言发起的请求对象
        assert req.value.method == "GET"
        assert "page=1" in req.value.url

    def test_10_project_list_table_link(self):
        """表格行内 链接"""
        # 造数据，mock 行内数据
        self.project.page.route(**mock_api.mock_project_search_1)
        logs.info("已 mock 行内数据，断言行内链接属性")
        # 重新刷新页面
        self.project.page.reload()
        # 断言链接有某属性
        expect(self.project.locator_link_debugtalk).to_have_attribute("href", "debugtalk.html?project_id=1")

    def test_11_project_list_table_delete(self):
        """表格行内删除 {"message": "无权限操作，请联系管理员"}"""
        # 造数据，mock 行内数据
        self.project.page.route(**mock_api.mock_project_search_1)
        # 重新刷新页面
        self.project.page.reload()
        # 点击删除
        self.project.locator_table_delete.click()
        expect(self.project.locator_boot_box).to_contain_text('确定要删除选中的数据？')
        # mock 拦截请求，返回{"message": "无权限操作，请联系管理员"}
        self.project.page.route(**mock_api.mock_project_delete_403)
        logs.info("已 mock 删除接口返回403，确认删除并校验无权限弹窗")
        # 点确定删除
        self.project.locator_boot_box_accept.click()
        # 获取最后一个boot_box
        expect(self.project.locator_boot_box.last).to_contain_text('操作异常："无权限操作，请联系管理员"')

    def test_12_project_list_table_edit(self):
        """表格行内编辑"""
        # 造数据，mock 行内数据
        self.project.page.route(**mock_api.mock_project_search_1)
        logs.info("已 mock 行内数据，点击编辑并断言编辑模态框")
        # 重新刷新页面
        self.project.page.reload()
        # 点击编辑
        self.project.locator_table_edit.first.click()
        # 断言
        expect(self.project.locator_edit_modal).to_be_visible()
