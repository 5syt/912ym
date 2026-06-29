"""
日志模块
封装 Python logging 模块，提供统一的日志输出功能
"""
import logging
import os
from datetime import datetime

from common.config import LOG_DIR


# 单例模式的 logger 实例
_logger_instance = None


def get_logger():
    """
    获取 logger 实例，使用单例模式

    Returns:
        logging.Logger: 配置好的 logger 实例
    """
    global _logger_instance

    # 如果已经存在实例，直接返回
    if _logger_instance is not None:
        return _logger_instance

    # 创建 logger 实例
    logger = logging.getLogger("autotest")
    logger.setLevel(logging.DEBUG)
    logger.propagate = False

    # 定义日志格式
    formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s"
    )

    # 控制台输出处理器
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # 文件输出处理器
    # 确保日志目录存在
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)

    # 日志文件名按日期命名
    log_file_name = "autotest_{}.log".format(datetime.now().strftime("%Y%m%d"))
    log_file_path = os.path.join(LOG_DIR, log_file_name)

    file_handler = logging.FileHandler(log_file_path, encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # 保存单例
    _logger_instance = logger

    return logger
