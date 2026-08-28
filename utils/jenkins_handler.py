import re
import jenkins
from config.operationConfig import OperationConfig
from utils.recordlog import logs

class JenkinsHandler:
    """Jenkins 操作类，封装构建查询、状态获取、测试报告统计等功能"""

    def __init__(self):
        conf = OperationConfig()
        # 强制转 str：YAML 会把纯数字密码/用户名解析为整数，而 python-jenkins 要求字符串（内部调 encode）
        self.__server = jenkins.Jenkins(
            url=str(conf.get_section_jenkins('url')),
            username=str(conf.get_section_jenkins('username')),
            password=str(conf.get_section_jenkins('password')),
            timeout=int(conf.get_section_jenkins('timeout'))
        )
        self.job_name = conf.get_section_jenkins('job_name')

    def get_job_number(self):
        """读取当前 job 的最新构建号"""
        return self.__server.get_job_info(self.job_name)['lastBuild']['number']

    def get_build_job_status(self):
        """读取最新构建的状态"""
        build_num = self.get_job_number()
        return self.__server.get_build_info(self.job_name, build_num)['result']

    def get_console_log(self):
        """获取最新构建的控制台日志"""
        return self.__server.get_build_console_output(self.job_name, self.get_job_number())

    def get_job_description(self):
        """返回 job 描述信息和 URL（单次请求获取）"""
        job_info = self.__server.get_job_info(self.job_name)
        return job_info['description'], job_info['url']

    def get_build_report(self):
        """获取最新构建的测试报告"""
        return self.__server.get_build_test_report(self.job_name, self.get_job_number())

    def get_build_enhance_info(self):
        """
        获取构建编号、构建地址与 Allure 报告链接等链接类信息
        构建进行中即可查询，用于增强钉钉/飞书通知内容；
        最终构建结果在构建结束前未知，故此处仅提供链接
        :return: 包含 build_number、build_url、allure_url 的字典
        """
        build_num = self.get_job_number()
        # python-jenkins 1.x 无 get_job_url 方法，改用 get_job_info 的 url 字段（新旧版本均兼容）
        job_url = self.__server.get_job_info(self.job_name)['url']
        build_url = f'{job_url}{build_num}/'
        logs.info(f"查询 Jenkins 构建信息成功：第{build_num}次，构建地址：{build_url}")
        return {
            'build_number': build_num,
            'build_url': build_url,
            # Allure Jenkins 插件生成报告页的固定相对路径
            'allure_url': f'{build_url}allure/'
        }

    def report_success_or_fail(self):
        """
        统计测试报告的成功数、失败数、跳过数、成功率及执行时长，
        并从控制台日志中提取 allure 报告链接
        :return: 包含统计信息和报告链接的字典
        """
        report_info = self.get_build_report()
        # python-jenkins 获取测试报告失败时返回 None，先判空收窄类型，避免下标访问 None 报 TypeError
        if report_info is None:
            raise ValueError(f'获取 job [{self.job_name}] 最新构建的测试报告失败，无法统计测试结果')
        pass_count = report_info['passCount']
        fail_count = report_info['failCount']
        skip_count = report_info['skipCount']
        total_count = pass_count + fail_count + skip_count
        duration = report_info['duration']

        # 将秒数转换为"X时X分X秒"格式（duration 可能为小数字符串，先转 float 再取整）
        hour, remainder = divmod(int(float(duration)), 3600)
        minute, seconds = divmod(remainder, 60)
        execute_duration = f'{hour}时{minute}分{seconds}秒'

        # 从控制台日志中提取 allure 报告链接（未匹配到时返回空字符串，避免 None.group() 报错）
        console_log = self.get_console_log()
        match = re.search(
            rf'http://[\d.]+:\d+/job/{self.job_name}/(.*?)allure', console_log
        )
        report_line = match.group(0) if match else ''

        return {
            'total': total_count,
            'pass_count': pass_count,
            'fail_count': fail_count,
            'skip_count': skip_count,
            'execute_duration': execute_duration,
            'report_line': report_line
        }
