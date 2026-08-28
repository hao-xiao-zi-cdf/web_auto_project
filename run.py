import os
import shutil
import pytest
from config import setting
from utils.recordlog import logs

if __name__ == '__main__':

    # JUnit XML 报告路径：Jenkins 构建时邮件模板靠它提取用例统计信息（总数/成功/失败/跳过）
    # 单独存放在项目根目录的 report 文件夹（见 setting.py 的 FILE_PATH['RESULTXML']），
    # 与 allure 原始数据目录 reports 分开，互不影响；每次运行前清空该目录，避免旧文件残留
    result_xml_dir = setting.FILE_PATH['RESULTXML']
    if os.path.exists(result_xml_dir):
        shutil.rmtree(result_xml_dir)
    os.makedirs(result_xml_dir)
    result_xml = os.path.join(result_xml_dir, 'results.xml')

    # 执行前先显式清空 reports 目录，避免上一次构建的残留结果叠加进本次报告（双保险，不依赖 --clean-alluredir）
    if os.path.exists('./reports'):
        shutil.rmtree('./reports')
        logs.info("已清空上次构建残留的 reports 目录")

    # 运行测试用例(自动清理 allure-results)
    logs.info("开始执行测试用例...")
    pytest.main(['--alluredir', './reports', '--clean-alluredir', f'--junitxml={result_xml}'])

    # 生成测试报告
    logs.info("测试用例执行完成，开始生成 Allure 报告...")
    os.system('allure generate ./reports -o ./allure_report --clean')

    # 打开报告
    logs.info("Allure 报告生成完成，正在打开报告...")
    os.system('allure open ./allure_report')