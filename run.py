import os
import pytest
from utils.recordlog import logs

if __name__ == '__main__':

    # 运行测试用例(自动清理 allure-results)
    logs.info("开始执行测试用例...")
    pytest.main(['--alluredir', './reports', '--clean-alluredir'])

    # 生成测试报告
    logs.info("测试用例执行完成，开始生成 Allure 报告...")
    os.system('allure generate ./reports -o ./allure_report --clean')

    # 打开报告
    logs.info("Allure 报告生成完成，正在打开报告...")
    os.system('allure open ./allure_report')