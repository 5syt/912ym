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

    # 图书标题（h1 标签下的 span）
    book_title = (By.CSS_SELECTOR, "h1 span")

    # 作者信息
    book_author = (By.CSS_SELECTOR, "div#info a[href*='/author/']")

    # 出版社信息
    book_publisher = (By.XPATH, "//div[@id='info']/span[text()='出版社:']/following-sibling::a")

    # 评分（rating_num 类）
    book_rating = (By.CSS_SELECTOR, "strong.rating_num")

    # 评价人数
    rating_people = (By.CSS_SELECTOR, "a.rating_people span")

    # 内容简介
    book_summary = (By.CSS_SELECTOR, "div.intro")

    # ==================== 业务操作方法 ====================

    def get_book_title(self):
        """
        获取图书标题

        Returns:
            str: 图书标题文本
        """
        self.logger.info("获取图书标题")
        return self.get_text(self.book_title)

    def get_book_author(self):
        """
        获取作者信息

        Returns:
            str: 作者名称
        """
        self.logger.info("获取图书作者信息")
        return self.get_text(self.book_author)

    def get_book_publisher(self):
        """
        获取出版社信息

        Returns:
            str: 出版社名称
        """
        self.logger.info("获取图书出版社信息")
        return self.get_text(self.book_publisher)

    def get_book_rating(self):
        """
        获取图书评分

        Returns:
            str: 图书评分（字符串格式，如 "9.0"）
        """
        self.logger.info("获取图书评分")
        return self.get_text(self.book_rating)

    def get_rating_people(self):
        """
        获取评价人数

        Returns:
            str: 评价人数文本
        """
        self.logger.info("获取评价人数")
        return self.get_text(self.rating_people)

    def get_book_summary(self):
        """
        获取内容简介

        Returns:
            str: 图书内容简介文本
        """
        self.logger.info("获取图书内容简介")
        return self.get_text(self.book_summary)

    def is_book_detail_displayed(self):
        """
        判断详情页是否正确加载（标题是否可见）

        Returns:
            bool: 详情页加载成功返回 True，否则返回 False
        """
        self.logger.info("判断图书详情页是否正确加载")
        return self.is_element_visible(self.book_title)
