import os
import allure
import pytest
from pytest import Item
from typing import Any, Dict
from slugify import slugify
from config.setting import DD_MSG, FS_MSG
from config.setting import JENKINS_ENHANCE
from utils.dingRobot import send_dd_msg
from utils.feishuRobot import send_feishu_msg
from utils.recordlog import logs

# 本地插件注册
pytest_plugins = ['plugins.pytest_playwright', 'plugins.pytest_base_url_plugin']

def pytest_runtest_call(item: Item):
    # 动态添加测试类的allure.feature()
    if item.parent._obj.__doc__:
        allure.dynamic.feature(item.parent._obj.__doc__)
    # 动态添加测试用例的title标题allure.title()
    if item.function.__doc__:
        allure.dynamic.title(item.function.__doc__)


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    把失败用例的截图/录屏附加到 allure 用例主体。
    fixture teardown 里的 attach 只会挂到 after-fixture（container json），
    报告正文看不到，因此统一在这里附加：
    - call 阶段：用例失败时页面尚未关闭，直接截图并附加到用例主体；
    - teardown 阶段：录屏文件已由 fixture 保存并暂存路径，此处统一附加到用例主体。
    """
    report = (yield).get_result()
    if report.when == "call" and report.failed:
        screenshot_option = item.config.getoption("--screenshot")
        if screenshot_option in ("on", "only-on-failure"):
            page = item.funcargs.get("page") or item.funcargs.get("unlogin_page")
            if page is not None:
                try:
                    screenshot_path = os.path.join(
                        item.config.getoption("--output"),
                        slugify(item.nodeid),
                        "test-failed-1.png",
                    )
                    page.screenshot(timeout=5000, path=screenshot_path)
                    logs.info(f"用例失败，保存截图到用例主体：{screenshot_path}")
                    allure.attach.file(
                        screenshot_path,
                        name=f"{item.name}-failed-1",
                        attachment_type=allure.attachment_type.PNG,
                    )
                except Exception as e:
                    logs.warning(f"失败用例保存截图失败：{e}")
    elif report.when == "teardown":
        for video_path in getattr(item, "_video_artifacts", []):
            try:
                allure.attach.file(
                    video_path,
                    name=os.path.basename(video_path),
                    attachment_type=allure.attachment_type.WEBM,
                )
                logs.info(f"附加用例录屏到报告主体：{video_path}")
            except Exception as e:
                logs.warning(f"附加用例录屏失败：{video_path}，原因：{e}")


@pytest.fixture(scope="session")
def browser_type_launch_args(pytestconfig: Any) -> Dict:
    """覆盖官方插件的配置，添加窗口最大化参数"""
    launch_options = {}
    headed_option = pytestconfig.getoption("--headed")
    if headed_option:
        launch_options["headless"] = False
    else:
        launch_options["headless"] = True  # 默认显示浏览器窗口
    # 添加窗口最大化
    launch_options["args"] = ["--start-maximized"]
    return launch_options

# 钩子函数，测试结束后执行
def pytest_terminal_summary(terminalreporter, exitstatus, config):
    """测试结束后收集结果摘要，并按配置推送通知"""
    total = terminalreporter._numcollected
    passed = len(terminalreporter.stats.get('passed', []))
    failed = len(terminalreporter.stats.get('failed', []))
    error = len(terminalreporter.stats.get('error', []))
    skipped = len(terminalreporter.stats.get('skipped', []))
    # pytest 9.x 中 _session_start 是 Instant 对象，通过 elapsed().seconds 获取耗时（秒）
    duration = terminalreporter._session_start.elapsed().seconds

    summary = (
        f"自动化测试结果，通知如下，请着重关注测试失败的接口，具体执行结果如下：\n"
        f"测试用例总数：{total}\n"
        f"测试通过数：{passed}\n"
        f"测试失败数：{failed}\n"
        f"错误数量：{error}\n"
        f"跳过执行数量：{skipped}\n"
        f"执行总时长：{duration}"
    )
    logs.info(f"测试执行完成，结果摘要：\n{summary}")

    # Jenkins 构建信息增强：追加构建编号与报告链接，方便收到通知后直接点击查看
    # 本地运行或 Jenkins 不可达时查询会失败，捕获后降级为普通通知，不影响测试流程
    if JENKINS_ENHANCE:
        try:
            from utils.jenkins_handler import JenkinsHandler
            build_info = JenkinsHandler().get_build_enhance_info()
            summary += (
                f"\n构建编号：第{build_info['build_number']}次"
                f"\n构建地址：{build_info['build_url']}"
                f"\nAllure 报告：{build_info['allure_url']}"
            )
        except Exception as e:
            logs.error(f'查询 Jenkins 构建信息失败，降级发送普通通知：{e}')

    if DD_MSG:
        send_dd_msg(summary)
    if FS_MSG:
        send_feishu_msg(summary)