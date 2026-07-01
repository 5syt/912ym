"""
豆瓣读书图书详情页页面类
封装图书详情页的元素定位和业务操作方法
"""
from selenium.webdriver.common.by import By

from base.base_page import BasePage


class BookDetailPage(BasePage):
    """
    豆瓣读书图书详情页类
    继承自 BasePage，封装图书详情页相关的元素定位和业务操作
    """

    # ==================== 元素定位器 ====================

    # 图书标题 - 多套备选
    book_title_selectors = [
        (By.CSS_SELECTOR, "h1 span"),
        (By.CSS_SELECTOR, "h1"),
        (By.XPATH, "//h1[1]"),
        (By.CSS_SELECTOR, ".article h1"),
    ]

    # 作者信息 - 多套备选
    book_author_selectors = [
        (By.CSS_SELECTOR, "div#info a[href*='/author/']"),
        (By.XPATH, "//div[@id='info']//a[contains(@href, 'author')]"),
        (By.CSS_SELECTOR, "#info a"),
        (By.XPATH, "//span[text()='作者:']/following-sibling::a"),
    ]

    # 出版社信息 - 多套备选
    book_publisher_selectors = [
        (By.XPATH, "//div[@id='info']/span[text()='出版社:']/following-sibling::a"),
        (By.XPATH, "//span[text()='出版社:']/following-sibling::a"),
        (By.CSS_SELECTOR, "#info a"),
    ]

    # 评分 - 多套备选
    book_rating_selectors = [
        (By.CSS_SELECTOR, "strong.rating_num"),
        (By.CSS_SELECTOR, ".rating_num"),
        (By.CSS_SELECTOR, "strong[property='v:average']"),
        (By.XPATH, "//strong[contains(@class, 'rating')]"),
    ]

    # 评价人数 - 多套备选
    rating_people_selectors = [
        (By.CSS_SELECTOR, "a.rating_people span"),
        (By.CSS_SELECTOR, ".rating_people span"),
        (By.XPATH, "//span[@property='v:votes']"),
        (By.CSS_SELECTOR, "span[property='v:votes']"),
    ]

    # 内容简介 - 多套备选
    book_summary_selectors = [
        (By.CSS_SELECTOR, "div.intro"),
        (By.CSS_SELECTOR, ".related_info .intro"),
        (By.XPATH, "//div[contains(@class, 'intro')][1]"),
    ]

    # ==================== 业务操作方法 ====================

    def _try_selectors(self, selectors_list, get_func="get_text"):
        """
        尝试多套定位器，返回第一个成功的结果

        Args:
            selectors_list: 定位器列表
            get_func: 要调用的方法名，get_text / find_element 等

        Returns:
            找到的结果，失败返回 None
        """
        for selector in selectors_list:
            try:
                if get_func == "get_text":
                    text = self.get_text(selector)
                    if text and text.strip():
                        return text.strip()
                elif get_func == "find_element":
                    return self.find_element(selector)
            except Exception:
                continue
        return None

    def get_book_title(self):
        """
        获取图书标题

        Returns:
            str: 图书标题文本
        """
        self.logger.info("获取图书标题")
        result = self._try_selectors(self.book_title_selectors)
        if result:
            self.logger.info(f"图书标题：{result}")
            return result
        # 兜底用页面标题
        title = self.driver.title
        self.logger.info(f"使用页面标题：{title}")
        return title

    def get_book_author(self):
        """
        获取作者信息

        Returns:
            str: 作者名称
        """
        self.logger.info("获取图书作者信息")
        result = self._try_selectors(self.book_author_selectors)
        if result:
            self.logger.info(f"作者：{result}")
            return result
        self.logger.warning("未找到作者信息，返回空字符串")
        return ""

    def get_book_publisher(self):
        """
        获取出版社信息

        Returns:
            str: 出版社名称
        """
        self.logger.info("获取图书出版社信息")
        result = self._try_selectors(self.book_publisher_selectors)
        if result:
            self.logger.info(f"出版社：{result}")
            return result
        self.logger.warning("未找到出版社信息，返回空字符串")
        return ""

    def get_book_rating(self):
        """
        获取图书评分

        Returns:
            str: 图书评分（字符串格式，如 "9.0"）
        """
        self.logger.info("获取图书评分")
        result = self._try_selectors(self.book_rating_selectors)
        if result:
            self.logger.info(f"评分：{result}")
            return result
        self.logger.warning("未找到评分信息，返回空字符串")
        return ""

    def get_rating_people(self):
        """
        获取评价人数

        Returns:
            str: 评价人数文本
        """
        self.logger.info("获取评价人数")
        result = self._try_selectors(self.rating_people_selectors)
        if result:
            self.logger.info(f"评价人数：{result}")
            return result
        self.logger.warning("未找到评价人数，返回空字符串")
        return ""

    def get_book_summary(self):
        """
        获取内容简介

        Returns:
            str: 图书内容简介文本
        """
        self.logger.info("获取图书内容简介")
        result = self._try_selectors(self.book_summary_selectors)
        if result:
            self.logger.info(f"内容简介长度：{len(result)} 字")
            return result
        self.logger.warning("未找到内容简介，返回空字符串")
        return ""

    def is_book_detail_displayed(self):
        """
        判断详情页是否正确加载（标题是否可见）

        Returns:
            bool: 详情页加载成功返回 True，否则返回 False
        """
        self.logger.info("判断图书详情页是否正确加载")
        try:
            title = self.get_book_title()
            return bool(title)
        except Exception:
            return False
