import datetime
from playwright.sync_api import Page


class BasePage(object):
    """
    页面公共类
    """

    def __init__(self, page: Page):
        """
        初始化
        :param page: playwright 的 page 对象
        """
        self.page = page

    # 页面打开
    def open_url(self, url) -> None:
        """
        输入网址
        :param url: URL资源路径
        :return: 无
        """
        self.page.goto(url)

    # 基础操作：接收元素定位属性值
    def base_click(self, loc, **kwargs) -> None:
        """
        点击元素
        :param loc: 元素定位方式及属性值
        :return: 无
        """
        self.page.locator(loc).click(**kwargs)

    def base_input(self, loc, text, **kwargs):
        """
        输入元素
        :param loc: 元素定位信息
        :param text: 输入的文本信息
        :return: 无
        """
        self.page.locator(loc).clear(**kwargs)
        self.page.locator(loc).fill(text, **kwargs)

    def get_text(self, loc, **kwargs):
        """
        获取元素文本信息
        :param loc: 元素定位信息
        :return: 元素文本信息
        """
        self.page.locator(loc).wait_for(**kwargs)
        return self.page.locator(loc).text_content().strip()

    def base_hover(self, loc, **kwargs):
        """
        鼠标悬停
        :param loc: 元素定位信息
        :return: 无
        """
        self.page.locator(loc).hover(**kwargs)

    def base_double_click(self, loc, **kwargs):
        """
        鼠标双击
        :param loc: 元素定位信息
        :return: 无
        """
        self.page.locator(loc).dblclick(**kwargs)

    def base_right_click(self, loc, **kwargs):
        """
        鼠标右击
        :param loc: 元素定位信息
        :return: 无
        """
        self.page.locator(loc).click(button="right", **kwargs)

    # 多窗口
    def get_new_window(self, trigger_action):
        """
       获取新打开的窗口
       :param trigger_action: 触发打开新窗口的操作，如 lambda: self.page.click("#btn")
       :return: 新窗口的 page 对象
       """
        # 触发打开新窗口的操作
        with self.page.expect_popup() as popup_info:
            trigger_action()
        # 获取新窗口的 page 对象
        new_page = popup_info.value
        # 等待新窗口加载完成
        new_page.wait_for_load_state("load")
        # 返回新窗口的 page 对象
        return new_page

    # 切换frame
    def get_frame(self, frame_loc):
        """
        获取 frame 元素
        :param frame_loc: frame元素定位信息
        :return: frame 元素对象
        """
        return self.page.frame_locator(frame_loc)

    # 截图
    def get_screen_shot(self, img_name):
        """
        获取页面截图
        :param img_name: 截图名称
        :return: 无
        """
        # 获取当前时间，按照时间格式保存
        now = datetime.now().strftime("%Y%m%d_%H%M%S")
        # 截图保存路径
        import os
        path = os.path.join("", 'img', f"{img_name}_{now}.png")
        # 截图全屏
        self.page.screenshot(path=path)

    # 下拉框 select_option
    def base_select_option(self, loc, label=None, value=None, index=None, **kwargs):
        """
        根据提供的条件在下拉框中选中指定的选项
        :param loc: 元素定位信息
        :param label: 选项的可见文本标签
        :param value: 选项的 value 属性值
        :param index: 选项的索引（从 0 开始）
        :param kwargs: 传递给 Playwright select_option 的额外参数（如 timeout, force 等）
        :return: 无
        """
        # 获取目标下拉框元素定位器
        ele = self.page.locator(loc)

        # 优先匹配标签文本，其次匹配 value 属性，最后匹配索引位置
        if label:
            ele.select_option(label=label, **kwargs)
        elif value:
            ele.select_option(value=value, **kwargs)
        elif index is not None:
            ele.select_option(index=index, **kwargs)
