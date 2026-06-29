"""
页面基类模块
封装 Selenium 常用操作，提供统一的元素定位和页面操作方法
"""
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from common.logger import get_logger
from common.config import TIMEOUT
from common.screenshot import save_screenshot


class BasePage:
    """
    页面基类
    所有页面类的父类，封装了常用的 Selenium 操作方法
    """

    def __init__(self, driver):
        """
        初始化方法

        Args:
            driver: WebDriver 实例
        """
        self.driver = driver
        self.logger = get_logger()
        self.wait = WebDriverWait(self.driver, TIMEOUT)

    # ==================== 元素定位相关方法 ====================

    def find_element(self, locator):
        """
        查找单个元素，等待元素可见

        Args:
            locator (tuple): 元素定位器，格式为 (By.ID, "id_value")

        Returns:
            WebElement: 找到的元素对象

        Raises:
            TimeoutException: 超时未找到元素
        """
        try:
            self.logger.info(f"查找元素：{locator}")
            element = self.wait.until(EC.visibility_of_element_located(locator))
            return element
        except Exception as e:
            self.logger.error(f"查找元素失败：{locator}，错误信息：{e}")
            raise

    def find_elements(self, locator):
        """
        查找多个元素，等待至少一个元素存在

        Args:
            locator (tuple): 元素定位器，格式为 (By.ID, "id_value")

        Returns:
            list: 找到的元素列表

        Raises:
            TimeoutException: 超时未找到元素
        """
        try:
            self.logger.info(f"查找多个元素：{locator}")
            elements = self.wait.until(EC.presence_of_all_elements_located(locator))
            return elements
        except Exception as e:
            self.logger.error(f"查找多个元素失败：{locator}，错误信息：{e}")
            raise

    def wait_element_clickable(self, locator):
        """
        等待元素可点击

        Args:
            locator (tuple): 元素定位器，格式为 (By.ID, "id_value")

        Returns:
            WebElement: 可点击的元素对象

        Raises:
            TimeoutException: 超时元素不可点击
        """
        try:
            self.logger.info(f"等待元素可点击：{locator}")
            element = self.wait.until(EC.element_to_be_clickable(locator))
            return element
        except Exception as e:
            self.logger.error(f"等待元素可点击失败：{locator}，错误信息：{e}")
            raise

    def wait_element_visible(self, locator):
        """
        等待元素可见

        Args:
            locator (tuple): 元素定位器，格式为 (By.ID, "id_value")

        Returns:
            WebElement: 可见的元素对象

        Raises:
            TimeoutException: 超时元素不可见
        """
        try:
            self.logger.info(f"等待元素可见：{locator}")
            element = self.wait.until(EC.visibility_of_element_located(locator))
            return element
        except Exception as e:
            self.logger.error(f"等待元素可见失败：{locator}，错误信息：{e}")
            raise

    def wait_element_present(self, locator):
        """
        等待元素存在于 DOM 中

        Args:
            locator (tuple): 元素定位器，格式为 (By.ID, "id_value")

        Returns:
            WebElement: 存在的元素对象

        Raises:
            TimeoutException: 超时元素不存在
        """
        try:
            self.logger.info(f"等待元素存在：{locator}")
            element = self.wait.until(EC.presence_of_element_located(locator))
            return element
        except Exception as e:
            self.logger.error(f"等待元素存在失败：{locator}，错误信息：{e}")
            raise

    # ==================== 元素操作方法 ====================

    def click(self, locator):
        """
        点击元素，先等待可点击再点击

        Args:
            locator (tuple): 元素定位器，格式为 (By.ID, "id_value")

        Raises:
            TimeoutException: 超时元素不可点击
        """
        try:
            self.logger.info(f"点击元素：{locator}")
            element = self.wait_element_clickable(locator)
            element.click()
        except Exception as e:
            self.logger.error(f"点击元素失败：{locator}，错误信息：{e}")
            raise

    def input_text(self, locator, text):
        """
        输入文本，先等待可见再清除再输入

        Args:
            locator (tuple): 元素定位器，格式为 (By.ID, "id_value")
            text (str): 要输入的文本内容

        Raises:
            TimeoutException: 超时元素不可见
        """
        try:
            self.logger.info(f"在元素 {locator} 中输入文本：{text}")
            element = self.wait_element_visible(locator)
            element.clear()
            element.send_keys(text)
        except Exception as e:
            self.logger.error(f"输入文本失败：{locator}，错误信息：{e}")
            raise

    def clear(self, locator):
        """
        清除输入框内容

        Args:
            locator (tuple): 元素定位器，格式为 (By.ID, "id_value")

        Raises:
            TimeoutException: 超时元素不可见
        """
        try:
            self.logger.info(f"清除元素内容：{locator}")
            element = self.wait_element_visible(locator)
            element.clear()
        except Exception as e:
            self.logger.error(f"清除元素内容失败：{locator}，错误信息：{e}")
            raise

    def get_text(self, locator):
        """
        获取元素文本

        Args:
            locator (tuple): 元素定位器，格式为 (By.ID, "id_value")

        Returns:
            str: 元素的文本内容

        Raises:
            TimeoutException: 超时元素不可见
        """
        try:
            self.logger.info(f"获取元素文本：{locator}")
            element = self.wait_element_visible(locator)
            text = element.text
            self.logger.info(f"元素文本内容：{text}")
            return text
        except Exception as e:
            self.logger.error(f"获取元素文本失败：{locator}，错误信息：{e}")
            raise

    def get_attribute(self, locator, name):
        """
        获取元素属性值

        Args:
            locator (tuple): 元素定位器，格式为 (By.ID, "id_value")
            name (str): 属性名称

        Returns:
            str: 属性值

        Raises:
            TimeoutException: 超时元素不存在
        """
        try:
            self.logger.info(f"获取元素 {locator} 的属性：{name}")
            element = self.wait_element_present(locator)
            value = element.get_attribute(name)
            self.logger.info(f"属性 {name} 的值：{value}")
            return value
        except Exception as e:
            self.logger.error(f"获取元素属性失败：{locator}，错误信息：{e}")
            raise

    def is_element_visible(self, locator):
        """
        判断元素是否可见

        Args:
            locator (tuple): 元素定位器，格式为 (By.ID, "id_value")

        Returns:
            bool: 元素可见返回 True，否则返回 False
        """
        try:
            self.logger.info(f"判断元素是否可见：{locator}")
            self.wait.until(EC.visibility_of_element_located(locator))
            self.logger.info(f"元素可见：{locator}")
            return True
        except Exception as e:
            self.logger.info(f"元素不可见：{locator}，错误信息：{e}")
            return False

    # ==================== 页面操作方法 ====================

    def open_url(self, url):
        """
        打开指定 URL

        Args:
            url (str): 要打开的网址
        """
        try:
            self.logger.info(f"打开 URL：{url}")
            self.driver.get(url)
        except Exception as e:
            self.logger.error(f"打开 URL 失败：{url}，错误信息：{e}")
            raise

    def get_title(self):
        """
        获取页面标题

        Returns:
            str: 页面标题
        """
        try:
            title = self.driver.title
            self.logger.info(f"获取页面标题：{title}")
            return title
        except Exception as e:
            self.logger.error(f"获取页面标题失败，错误信息：{e}")
            raise

    def get_current_url(self):
        """
        获取当前页面 URL

        Returns:
            str: 当前页面 URL
        """
        try:
            url = self.driver.current_url
            self.logger.info(f"获取当前页面 URL：{url}")
            return url
        except Exception as e:
            self.logger.error(f"获取当前页面 URL 失败，错误信息：{e}")
            raise

    def maximize_window(self):
        """
        最大化窗口
        """
        try:
            self.logger.info("最大化浏览器窗口")
            self.driver.maximize_window()
        except Exception as e:
            self.logger.error(f"最大化窗口失败，错误信息：{e}")
            raise

    def refresh(self):
        """
        刷新页面
        """
        try:
            self.logger.info("刷新页面")
            self.driver.refresh()
        except Exception as e:
            self.logger.error(f"刷新页面失败，错误信息：{e}")
            raise

    def back(self):
        """
        浏览器后退
        """
        try:
            self.logger.info("浏览器后退")
            self.driver.back()
        except Exception as e:
            self.logger.error(f"浏览器后退失败，错误信息：{e}")
            raise

    def forward(self):
        """
        浏览器前进
        """
        try:
            self.logger.info("浏览器前进")
            self.driver.forward()
        except Exception as e:
            self.logger.error(f"浏览器前进失败，错误信息：{e}")
            raise

    # ==================== 截图方法 ====================

    def save_screenshot(self, screenshot_name):
        """
        保存截图

        Args:
            screenshot_name (str): 截图名称前缀

        Returns:
            str: 截图文件的完整路径
        """
        try:
            self.logger.info(f"保存截图：{screenshot_name}")
            file_path = save_screenshot(self.driver, screenshot_name)
            self.logger.info(f"截图已保存到：{file_path}")
            return file_path
        except Exception as e:
            self.logger.error(f"保存截图失败：{screenshot_name}，错误信息：{e}")
            raise
