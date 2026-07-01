"""
配置模块
定义全局配置常量，所有路径基于项目根目录动态计算
"""
import os


# 项目根目录：common 目录的上一级
COMMON_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(COMMON_DIR)

# 基础 URL
BASE_URL = "https://book.douban.com"

# 显式等待超时时间（秒）- 优化：从10秒缩短到5秒，加快测试速度
TIMEOUT = 5

# 浏览器类型
BROWSER = "chrome"

# 截图保存目录
SCREENSHOT_DIR = os.path.join(PROJECT_ROOT, "report", "screenshots")

# 日志目录
LOG_DIR = os.path.join(PROJECT_ROOT, "logs")

# 测试数据目录
DATA_DIR = os.path.join(PROJECT_ROOT, "data")
