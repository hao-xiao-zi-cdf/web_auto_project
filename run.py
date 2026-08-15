import os
import pytest

if __name__ == '__main__':
    # 清理历史报告
    if os.path.exists('./allure_report'):
        import shutil

        shutil.rmtree('./allure_report')

    # 运行测试用例(自动清理 allure-results)
    pytest.main(['--alluredir', './reports', '--clean-alluredir'])

    # 生成测试报告
    os.system('allure generate ./reports -o ./allure_report --clean')

    # 打开报告
    os.system('allure open ./allure_report')