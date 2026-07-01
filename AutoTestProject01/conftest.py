"""
pytest 配置文件
包含 fixtures 和钩子函数的定义
"""
import os
import sys
from pathlib import Path

# 自动将项目根目录添加到 Python 路径（兼容 PyCharm 和命令行运行）
_current_file = Path(__file__).resolve()
_project_root = _current_file.parent
if str(_project_root) not in sys.path:
    sys.path.insert(0, str(_project_root))

from datetime import datetime

import allure
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from common import config
from common.data_reader import read_json
from common.logger import get_logger
from common.screenshot import save_screenshot

# 获取 logger 实例
logger = get_logger()


@pytest.fixture(scope="function")
def driver():
    """
    浏览器驱动 fixture，每个测试用例创建一个新的浏览器实例

    Returns:
        webdriver.Chrome: Chrome 浏览器驱动实例
    """
    # 配置 ChromeOptions
    chrome_options = Options()

    # 通过环境变量控制无头模式，默认关闭
    headless = os.getenv("HEADLESS", "false").lower() == "true"
    if headless:
        chrome_options.add_argument("--headless=new")
        logger.info("启用无头模式")

    # 启动最大化
    chrome_options.add_argument("--start-maximized")
    # 禁用 GPU 加速
    chrome_options.add_argument("--disable-gpu")
    # 禁用沙箱模式（Linux 环境下需要）
    chrome_options.add_argument("--no-sandbox")
    # 禁用 /dev/shm 共享内存（避免资源限制）
    chrome_options.add_argument("--disable-dev-shm-usage")

    logger.info("启动 Chrome 浏览器...")
    # 创建 WebDriver 实例
    driver = webdriver.Chrome(options=chrome_options)
    # 最大化窗口
    driver.maximize_window()
    logger.info("Chrome 浏览器启动成功")

    # yield 之前是 setup，yield 之后是 teardown
    yield driver

    # teardown: 关闭浏览器
    logger.info("关闭 Chrome 浏览器...")
    driver.quit()
    logger.info("Chrome 浏览器已关闭")


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    pytest 测试结果钩子，用于测试失败时自动截图

    Args:
        item: 测试用例对象
        call: 测试调用对象
    """
    # 执行测试并获取结果
    outcome = yield
    report = outcome.get_result()

    # 仅在测试用例执行阶段（call）且失败时截图
    if report.when == "call" and report.failed:
        # 从测试用例的 fixture 中获取 driver
        driver = item.funcargs.get("driver", None)

        if driver is not None:
            # 生成截图文件名：用例名_时间戳
            case_name = item.name
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            screenshot_name = "{}_{}".format(case_name, timestamp)

            logger.info("测试用例 '{}' 失败，正在截图...".format(case_name))

            try:
                # 保存截图
                screenshot_path = save_screenshot(driver, screenshot_name)
                logger.info("截图已保存：{}".format(screenshot_path))

                # 将截图附加到 Allure 报告中
                with open(screenshot_path, "rb") as f:
                    allure.attach(
                        f.read(),
                        name="失败截图",
                        attachment_type=allure.attachment_type.PNG,
                    )
                logger.info("截图已附加到 Allure 报告")
            except Exception as e:
                logger.error("截图失败：{}".format(str(e)))
        else:
            logger.warning("测试用例 '{}' 失败，但未找到 driver，无法截图".format(item.name))


@pytest.fixture(scope="session")
def search_test_data():
    """
    搜索测试数据 fixture，session 级别

    Returns:
        list: 搜索测试用例数据列表
    """
    logger.info("读取搜索测试数据...")
    data = read_json("search_data.json")
    test_cases = data.get("test_cases", [])
    logger.info("已加载 {} 条搜索测试用例".format(len(test_cases)))
    return test_cases


@pytest.fixture(scope="session")
def category_test_data():
    """
    分类测试数据 fixture，session 级别

    Returns:
        list: 分类测试用例数据列表
    """
    logger.info("读取分类测试数据...")
    data = read_json("category_data.json")
    test_cases = data.get("test_cases", [])
    logger.info("已加载 {} 条分类测试用例".format(len(test_cases)))
    return test_cases


@pytest.fixture(scope="session")
def book_detail_test_data():
    """
    图书详情测试数据 fixture，session 级别

    Returns:
        list: 图书详情测试用例数据列表
    """
    logger.info("读取图书详情测试数据...")
    data = read_json("book_detail_data.json")
    test_cases = data.get("test_cases", [])
    logger.info("已加载 {} 条图书详情测试用例".format(len(test_cases)))
    return test_cases


def pytest_sessionfinish(session, exitstatus):
    """
    pytest 会话结束钩子，用于生成 Allure 环境配置文件

    Args:
        session: pytest 会话对象
        exitstatus: 退出状态码
    """
    logger.info("生成 Allure 环境配置文件...")

    # allure-results 目录路径
    allure_results_dir = os.path.join(config.PROJECT_ROOT, "report", "allure-results")

    # 确保目录存在
    if not os.path.exists(allure_results_dir):
        os.makedirs(allure_results_dir)

    # environment.properties 文件路径
    env_file_path = os.path.join(allure_results_dir, "environment.properties")

    # 环境信息内容
    env_content = """Browser=Chrome
Environment=Production
System=豆瓣读书
BASE_URL={}
""".format(config.BASE_URL)

    try:
        # 写入环境配置文件
        with open(env_file_path, "w", encoding="utf-8") as f:
            f.write(env_content)
        logger.info("Allure 环境配置文件已生成：{}".format(env_file_path))
    except Exception as e:
        logger.error("生成 Allure 环境配置文件失败：{}".format(str(e)))
