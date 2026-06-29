"""
截图工具模块
封装截图保存方法
"""
import os
from datetime import datetime

from common.config import SCREENSHOT_DIR


def save_screenshot(driver, screenshot_name):
    """
    保存浏览器截图到指定目录

    Args:
        driver: WebDriver 实例
        screenshot_name (str): 截图名称前缀

    Returns:
        str: 截图文件的完整路径
    """
    # 确保截图目录存在，不存在则创建
    if not os.path.exists(SCREENSHOT_DIR):
        os.makedirs(SCREENSHOT_DIR)

    # 生成截图文件名：名称_年月日_时分秒.png
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_name = "{}_{}.png".format(screenshot_name, timestamp)
    file_path = os.path.join(SCREENSHOT_DIR, file_name)

    # 保存截图
    driver.save_screenshot(file_path)

    return file_path
