import os
import pytest
from utils.recordlog import logs

if __name__ == '__main__':

    # JUnit XML 报告路径：Jenkins 构建时邮件模板靠它提取用例统计信息（总数/成功/失败/跳过）
    # 复用已有的 reports 目录，不新建文件夹；该文件在测试会话结束时写入，
    # 不会被启动阶段的 --clean-alluredir 清掉，allure 也只认 *-result.json，不会误解析它

    # 运行测试用例(自动清理 allure-results)
    logs.info("开始执行测试用例...")
    pytest.main(['--alluredir', './reports', '--clean-alluredir', '--junitxml=reports/results.xml'])

    # 生成测试报告
    logs.info("测试用例执行完成，开始生成 Allure 报告...")
    os.system('allure generate ./reports -o ./allure_report --clean')

    # 打开报告
    logs.info("Allure 报告生成完成，正在打开报告...")
    os.system('allure open ./allure_report')