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

    # 搜索输入框 - 多套备选
    search_input_selectors = [
        (By.ID, "inp-query"),
        (By.CSS_SELECTOR, "#inp-query"),
        (By.NAME, "search_text"),
        (By.CSS_SELECTOR, "input[name='search_text']"),
        (By.CSS_SELECTOR, "input.inp-query"),
        (By.CSS_SELECTOR, ".nav-search input[type='text']"),
        (By.CSS_SELECTOR, ".search-input"),
    ]

    # 搜索按钮 - 多套备选
    search_button_selectors = [
        (By.CSS_SELECTOR, "input[type='submit']"),
        (By.CSS_SELECTOR, "button[type='submit']"),
        (By.CSS_SELECTOR, ".search-btn"),
        (By.CSS_SELECTOR, "#nav-search-btn"),
        (By.CSS_SELECTOR, ".nav-search-btn"),
    ]

    # 导航栏分类链接（文学、流行、文化等）
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

    def _find_search_input(self):
        """
        尝试多套定位器找到搜索框

        Returns:
            WebElement: 搜索框元素
        """
        for selector in self.search_input_selectors:
            try:
                elements = self.driver.find_elements(*selector)
                if elements and len(elements) > 0:
                    try:
                        if elements[0].is_displayed():
                            return elements[0]
                    except Exception:
                        pass
            except Exception:
                continue
        # 都不行就用显式等待找第一个
        return self.wait_element_visible(self.search_input_selectors[0])

    def _find_search_button(self):
        """
        尝试多套定位器找到搜索按钮

        Returns:
            WebElement: 搜索按钮元素
        """
        for selector in self.search_button_selectors:
            try:
                elements = self.driver.find_elements(*selector)
                if elements and len(elements) > 0:
                    try:
                        if elements[0].is_displayed():
                            return elements[0]
                    except Exception:
                        pass
            except Exception:
                continue
        # 都不行就用显式等待找第一个
        return self.wait_element_visible(self.search_button_selectors[0])

    def search_book(self, keyword):
        """
        在搜索框输入关键词并点击搜索按钮

        Args:
            keyword (str): 要搜索的图书关键词

        Returns:
            HomePage: 当前页面对象（页面跳转由测试用例处理）
        """
        self.logger.info(f"搜索图书，关键词：{keyword}")
        # 找到搜索框并输入
        search_input = self._find_search_input()
        search_input.clear()
        search_input.send_keys(keyword)
        # 找到搜索按钮并点击（带安全验证处理）
        search_btn = self._find_search_button()
        self.click_element(search_btn)
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
