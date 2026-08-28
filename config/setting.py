import logging
import os
import sys

"""
放置框架运行所需的基础参数——路径、日志级别、超时时间、报告类型、通知开关，不随环境变化
"""

# 基础路径
DIR_BASE = os.path.dirname(os.path.dirname(__file__))
sys.path.append(DIR_BASE)

# log日志输出级别，可选值：DEBUG, INFO, WARNING, ERROR, CRITICAL
LOG_LEVEL = logging.DEBUG  # 文件
STREAM_LOG_LEVEL = logging.DEBUG  # 控制台

# 是否发送钉钉消息
DD_MSG = True

# 是否发送飞书消息
FS_MSG = True

# 是否在钉钉/飞书通知中附加 Jenkins 构建信息（构建编号、构建地址、Allure 报告链接）
JENKINS_ENHANCE = True

# 文件路径
FILE_PATH = {
    'CONFIG': os.path.join(DIR_BASE, 'config/config.yaml'),
    'LOG': os.path.join(DIR_BASE, 'logs'),
    'YAML': os.path.join(DIR_BASE),
    'RESULTXML': os.path.join(DIR_BASE, 'report'),
}