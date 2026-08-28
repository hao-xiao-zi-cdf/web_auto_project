import os
import logging
import datetime
from logging.handlers import RotatingFileHandler
from config import setting

# 日志目录与文件路径
log_path = setting.FILE_PATH["LOG"]
os.makedirs(log_path, exist_ok=True)
logfile_name = os.path.join(log_path, f"test.{datetime.datetime.now():%Y%m%d}.log")

class RecordLog:
    """日志模块：负责清理过期日志并创建 logger 实例"""

    # 日志保留天数，超过自动清理
    LOG_RETENTION_DAYS = 30
    # 单个日志文件最大字节数（5MB）
    MAX_BYTES = 5 * 1024 * 1024
    # 日志文件滚动备份数量
    BACKUP_COUNT = 7

    def __init__(self):
        self._clean_overdue_logs()
        self.logger = self._create_logger()

    def _clean_overdue_logs(self):
        """清理超过保留天数的日志文件"""
        cutoff = (datetime.datetime.now() - datetime.timedelta(days=self.LOG_RETENTION_DAYS)).timestamp()
        for filename in os.listdir(log_path):
            # 遍历日志目录下的所有文件，拆分文件名和拓展名，过滤掉无扩展名的文件
            if os.path.splitext(filename)[1]:
                filepath = os.path.join(log_path, filename)
                # 获取文件创建时间，若早于截止时间则删除
                if os.path.getctime(filepath) < cutoff:
                    os.remove(filepath)

    def _create_logger(self):
        """创建并配置 logger（文件 + 控制台双输出）"""
        logger = logging.getLogger(__name__)
        # 防止重复打印日志
        if not logger.handlers:
            logger.setLevel(setting.LOG_LEVEL)
            fmt = logging.Formatter(
                '%(levelname)s - %(asctime)s - %(filename)s:%(lineno)d -[%(module)s:%(funcName)s] - %(message)s'
            )

            # 文件输出：按大小滚动备份
            fh = RotatingFileHandler(
                filename=logfile_name, mode='a',
                maxBytes=self.MAX_BYTES, backupCount=self.BACKUP_COUNT, encoding='utf-8'
            )
            fh.setLevel(setting.LOG_LEVEL)
            fh.setFormatter(fmt)
            # 将相应的handler添加在logger对象中
            logger.addHandler(fh)
            # 控制台输出
            sh = logging.StreamHandler()
            sh.setLevel(setting.STREAM_LOG_LEVEL)
            sh.setFormatter(fmt)
            logger.addHandler(sh)
        return logger

logs = RecordLog().logger
