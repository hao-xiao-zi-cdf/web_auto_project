import yaml
import traceback
from config import setting
from utils.recordlog import logs

class OperationConfig:
    """封装读取 *.yaml 配置文件的工具类"""

    def __init__(self, filepath=None):
        # 未传入路径时使用默认配置路径
        self.__filepath = filepath or setting.FILE_PATH['CONFIG']
        try:
            with open(self.__filepath, 'r', encoding='utf-8') as f:
                self.conf = yaml.safe_load(f)
        except Exception as e:
            # 记录异常信息及完整堆栈
            logs.error(f"读取配置文件失败: {e}\n{traceback.format_exc()}")
            self.conf = {}

        self.type = self.get_report_type('type')

    def get_item_value(self, section_name):
        """
        根据 yaml 文件的顶级 key 获取该段下所有键值对
        :param section_name: 顶级段名
        :return: 以字典形式返回
        """
        return dict(self.conf.get(section_name, {}))

    def get_section_for_data(self, section, option):
        """
        根据 section 和 option 获取对应的配置值
        :param section: 顶级段名
        :param option: 段下的键名
        :return: 配置值，读取失败时返回空字符串
        """
        try:
            return self.conf[section][option]
        except (KeyError, TypeError) as e:
            logs.error(traceback.format_exc())
            return ''

    def write_config_data(self, section, option_key, option_value):
        """
        向 yaml 配置文件中写入数据（仅当 section 不存在时写入）
        :param section: 顶级段名
        :param option_key: 键名
        :param option_value: 键值
        """
        if section not in self.conf:
            self.conf[section] = {option_key: option_value}
            with open(self.__filepath, 'w', encoding='utf-8') as f:
                yaml.dump(self.conf, f, allow_unicode=True, default_flow_style=False)
        else:
            logs.info(f'"{section}" 值已存在，写入失败')

    def get_section_mysql(self, option):
        """获取 MYSQL 段下的配置项"""
        return self.get_section_for_data("MYSQL", option)

    def get_report_type(self, option):
        """获取 REPORT_TYPE 段下的配置项"""
        return self.get_section_for_data('REPORT_TYPE', option)

    def get_section_jenkins(self, option):
        """获取 JENKINS 段下的配置项"""
        return self.get_section_for_data("JENKINS", option)
