import urllib.parse
import requests
import time
import hmac
import hashlib
import base64
from config.operationConfig import OperationConfig

# 读取钉钉机器人配置
_config = OperationConfig()
WEBHOOK_URL = _config.get_section_for_data('DING_DING', 'WEBHOOK_URL')
SECRET = _config.get_section_for_data('DING_DING', 'SECRET')

def generate_sign():
    """
    计算钉钉机器人加签签名
    签名字符串: timestamp + "\n" + 密钥，使用HmacSHA256算法计算签名，再Base64编码后urlEncode
    :return: (当前时间戳, 签名)
    """
    timestamp = str(round(time.time() * 1000))
    # 拼接签名字符串并计算HmacSHA256签名
    str_to_sign = f'{timestamp}\n{SECRET}'
    hmac_code = hmac.new(
        SECRET.encode('utf-8'),
        str_to_sign.encode('utf-8'),
        digestmod=hashlib.sha256
    ).digest()
    # Base64编码后URL编码
    sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))
    return timestamp, sign


def send_dd_msg(content_str, at_all=True):
    """
    向钉钉机器人推送消息
    :param content_str: 发送的内容
    :param at_all: 是否@全员，默认为True
    :return: 接口响应文本
    """
    timestamp, sign = generate_sign()
    # url(钉钉机器人Webhook地址) + timestamp + sign
    url = f'{WEBHOOK_URL}&timestamp={timestamp}&sign={sign}'
    headers = {'Content-Type': 'application/json;charset=utf-8'}
    data = {
        "msgtype": "text",
        "text": {"content": content_str},
        "at": {"isAtAll": at_all}
    }
    res = requests.post(url, json=data, headers=headers)
    return res.text