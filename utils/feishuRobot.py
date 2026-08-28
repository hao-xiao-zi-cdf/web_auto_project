import time
import hmac
import hashlib
import base64
import requests
from config.operationConfig import OperationConfig
from utils.recordlog import logs

# 读取飞书机器人配置
_config = OperationConfig()
WEBHOOK_URL = _config.get_section_for_data('FEI_SHU', 'WEBHOOK_URL')
SECRET = _config.get_section_for_data('FEI_SHU', 'SECRET')


def generate_sign():
    """
    计算飞书机器人签名
    将 timestamp + "\n" + 密钥 作为 HmacSHA256 的 key，对空字节串计算签名，再 Base64 编码
    :return: (当前时间戳(秒), 签名)
    """
    timestamp = str(round(time.time()))
    # 拼接 timestamp 和密钥作为 HMAC key，对空串计算签名
    string_to_sign = f'{timestamp}\n{SECRET}'
    hmac_code = hmac.new(
        string_to_sign.encode('utf-8'),
        b'',
        digestmod=hashlib.sha256
    ).digest()
    sign = base64.b64encode(hmac_code).decode('utf-8')
    return timestamp, sign


def send_feishu_msg(content_str, at_all=True):
    """
    向飞书机器人推送消息
    :param content_str: 发送的内容
    :param at_all: 是否@全员，默认为True
    :return: 接口响应JSON
    """
    timestamp, sign = generate_sign()
    # @全员时在文本末尾追加 <at> 标签
    if at_all:
        content_str = f'{content_str}\n<at user_id="all">所有人</at>'

    data = {
        "timestamp": timestamp,
        "sign": sign,
        "msg_type": "text",
        "content": {"text": content_str}
    }
    headers = {'Content-Type': 'application/json;charset=utf-8'}
    try:
        res = requests.post(WEBHOOK_URL, json=data, headers=headers)
        res_json = res.json()
        # 飞书接口新旧版本返回字段不同：新版为 code，旧版为 StatusCode，为 0 时才表示推送成功
        if res_json.get('code', res_json.get('StatusCode')) == 0:
            logs.info(f"飞书通知推送成功，响应：{res_json}")
        else:
            logs.error(f"飞书通知推送失败，响应：{res_json}")
        return res_json
    except Exception as e:
        logs.error(f"飞书通知推送异常：{e}")
        return {}