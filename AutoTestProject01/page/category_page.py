"""
豆瓣读书分类页页面类
封装分类页的元素定位和业务操作方法
"""
from selenium.webdriver.common.by import By

from base.base_page import BasePage


class CategoryPage(BasePage):
    """
    豆瓣读书分类页类
    继承自 BasePage，封装分类页相关的元素定位和业务操作
    """

    # ==================== 元素定位器 ====================

    # 分类标题
    category_title = (By.CSS_SELECTOR, "div#content h1")

    # 图书列表项
    book_list_items = (By.CSS_SELECTOR, "li.subject-item")

    # 分页区域
    pagination = (By.CSS_SELECTOR, "div.paginator")

    # 下一页按钮
    next_page_button = (By.CSS_SELECTOR, "a.next")

    # ==================== 业务操作方法 ====================

    def get_category_title(self):
        """
        获取分类标题

        Returns:
            str: 分类标题文本
        """
        self.logger.info("获取分类标题")
        return self.get_text(self.category_title)

    def get_book_list_count(self):
        """
        获取当前页图书列表数量

        Returns:
            int: 当前页的图书数量
        """
        self.logger.info("获取当前页图书列表数量")
        try:
            elements = self.find_elements(self.book_list_items)
            count = len(elements)
            self.logger.info(f"当前页图书数量：{count}")
            return count
        except Exception as e:
            self.logger.info(f"获取图书列表数量失败，返回0：{e}")
            return 0

    def click_book_by_index(self, index):
        """
        点击列表中第 index 本图书

        Args:
            index (int): 图书索引，从 1 开始

        Returns:
            CategoryPage: 当前页面对象（页面跳转由测试用例处理）

        Raises:
            IndexError: 索引超出范围时抛出
        """
        self.logger.info(f"点击列表中第 {index} 本图书")
        # 获取所有图书列表项
        elements = self.find_elements(self.book_list_items)
        if index < 1 or index > len(elements):
            self.logger.error(f"索引 {index} 超出范围，当前页共有 {len(elements)} 本图书")
            raise IndexError(
                f"索引 {index} 超出范围，当前页共有 {len(elements)} 本图书"
            )
        # 获取指定索引的图书项，点击其标题链接
        book_element = elements[index - 1]
        title_link = book_element.find_element(By.CSS_SELECTOR, "h2 a")
        self.logger.info(f"点击图书：{title_link.text}")
        title_link.click()
        return self

    def is_category_page_displayed(self):
        """
        判断分类页是否正确加载

        Returns:
            bool: 分类页加载成功返回 True，否则返回 False
        """
        self.logger.info("判断分类页是否正确加载")
        return self.is_element_visible(self.category_title)

    def has_pagination(self):
        """
        判断是否有分页区域

        Returns:
            bool: 有分页返回 True，否则返回 False
        """
        self.logger.info("判断是否有分页区域")
        return self.is_element_visible(self.pagination)
