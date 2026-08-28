import os
import shutil
import pytest
from config import setting
from utils.recordlog import logs

if __name__ == '__main__':

    # JUnit XML 报告路径：Jenkins 邮件模板靠它提取用例统计信息，单独存放在 report 目录，
    # 与 allure 原始数据目录 reports 分开；每次运行前重建该目录，避免旧文件残留
    result_xml_dir = setting.FILE_PATH['RESULTXML']
    shutil.rmtree(result_xml_dir, ignore_errors=True)
    os.makedirs(result_xml_dir)
    result_xml = os.path.join(result_xml_dir, 'results.xml')

    # 运行测试用例（--clean-alluredir 会在执行前自动清空 reports 目录，无需手动清理）
    logs.info("开始执行测试用例...")
    pytest.main(['--alluredir', './reports', '--clean-alluredir', f'--junitxml={result_xml}'])

    # 生成测试报告
    logs.info("测试用例执行完成，开始生成 Allure 报告...")
    os.system('allure generate ./reports -o ./allure_report --clean')

    # 打开报告
    logs.info("Allure 报告生成完成，正在打开报告...")
    os.system('allure open ./allure_report')