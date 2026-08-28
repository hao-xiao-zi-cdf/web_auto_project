import json
import os
from utils.recordlog import logs


def read_json(file_name):
    """
    读取JSON文件并转换为格式为 [(), (), ...] 的列表
    :param file_name: json文件名
    :return: 列表
    """
    data = []
    file_path = os.path.dirname(__file__) + "/data/" + file_name
    try:
        with open(file_path, mode='r', encoding='utf-8') as f:
            # 读取JSON文件并解析为Python对象
            tmp = json.load(f)
            for i in tmp:
                # i 就是一个字典
                a = tuple(i.values())  # a=("13800002011","Aa12346","登录成功")
                data.append(a)  # [("13800002011","Aa12346","登录成功"),()]
    except (FileNotFoundError, json.JSONDecodeError) as e:
        logs.error(f"读取数据文件 {file_path} 失败：{e}")
    # 返回列表
    return data