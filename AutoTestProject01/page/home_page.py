"""
豆瓣读书首页页面类
封装首页的元素定位和业务操作方法
"""
from selenium.webdriver.common.by import By

from base.base_page import BasePage


class HomePage(BasePage):
    """
    豆瓣读书首页类
    继承自 BasePage，封装首页相关的元素定位和业务操作
    """

    # 页面 URL
    url = "https://book.douban.com"

    # ==================== 元素定位器 ====================

    # 搜索输入框
    search_input = (By.ID, "inp-query")

    # 搜索按钮
    search_button = (By.CSS_SELECTOR, "input[type='submit']")

    # 导航栏分类链接（文学、流行、文化等）
    # 使用 XPath 定位包含指定文本的导航链接
    category_link = (By.XPATH, "//div[@class='nav-items']/a[contains(text(), '{}')]")

    # ==================== 业务操作方法 ====================

    def open(self):
        """
        打开豆瓣读书首页

        Returns:
            HomePage: 当前页面对象，支持链式调用
        """
        self.logger.info("打开豆瓣读书首页")
        self.open_url(self.url)
        return self

    def search_book(self, keyword):
        """
        在搜索框输入关键词并点击搜索按钮

        Args:
            keyword (str): 要搜索的图书关键词

        Returns:
            HomePage: 当前页面对象（页面跳转由测试用例处理）
        """
        self.logger.info(f"搜索图书，关键词：{keyword}")
        # 输入搜索关键词
        self.input_text(self.search_input, keyword)
        # 点击搜索按钮
        self.click(self.search_button)
        return self

    def click_category(self, category_name):
        """
        点击指定分类导航链接

        Args:
            category_name (str): 分类名称，如"文学"、"流行"、"文化"等

        Returns:
            HomePage: 当前页面对象（页面跳转由测试用例处理）
        """
        self.logger.info(f"点击导航分类：{category_name}")
        # 动态构建分类链接定位器
        locator = (self.category_link[0], self.category_link[1].format(category_name))
        # 点击分类链接
        self.click(locator)
        return self
