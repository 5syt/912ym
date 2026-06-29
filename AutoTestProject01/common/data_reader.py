"""
数据读取模块
封装 JSON 文件读取方法
"""
import json
import os

from common.config import DATA_DIR


def read_json(file_name):
    """
    读取 JSON 文件并返回解析后的 Python 字典/列表

    Args:
        file_name (str): JSON 文件名，如 search_data.json

    Returns:
        dict or list: 解析后的 JSON 数据

    Raises:
        FileNotFoundError: 文件不存在时抛出
        json.JSONDecodeError: JSON 解析失败时抛出
    """
    # 拼接完整文件路径
    file_path = os.path.join(DATA_DIR, file_name)

    # 检查文件是否存在
    if not os.path.exists(file_path):
        raise FileNotFoundError("数据文件不存在：{}".format(file_path))

    # 读取并解析 JSON 文件
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    return data
