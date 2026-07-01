"""
豆瓣读书分类页页面类
封装分类页的元素定位和业务操作方法
"""
import time
from selenium.webdriver.common.by import By

from base.base_page import BasePage


class CategoryPage(BasePage):
    """
    豆瓣读书分类页类
    继承自 BasePage，封装分类页相关的元素定位和业务操作
    """

    # ==================== 元素定位器 ====================

    # 分类标题 - 多套备选
    category_title_selectors = [
        (By.CSS_SELECTOR, "div#content h1"),
        (By.CSS_SELECTOR, "h1"),
        (By.CSS_SELECTOR, ".article h1"),
        (By.XPATH, "//h1[1]"),
    ]

    # 图书列表项 - 多套备选
    book_list_selectors = [
        (By.CSS_SELECTOR, "li.subject-item"),
        (By.CSS_SELECTOR, "div.item"),
        (By.CSS_SELECTOR, ".article li"),
        (By.XPATH, "//li[contains(@class, 'subject')]"),
        (By.CSS_SELECTOR, "ul.subject-list li"),
    ]

    # 分页区域
    pagination_selectors = [
        (By.CSS_SELECTOR, "div.paginator"),
        (By.CSS_SELECTOR, ".paginator"),
        (By.CSS_SELECTOR, "div#paginator"),
    ]

    # ==================== 业务操作方法 ====================

    def get_category_title(self):
        """
        获取分类标题（快速检查，不等待超时）

        Returns:
            str: 分类标题文本
        """
        self.logger.info("获取分类标题")
        for selector in self.category_title_selectors:
            try:
                # 快速检查：用 find_elements 不触发超时等待
                elements = self.driver.find_elements(*selector)
                if elements and len(elements) > 0:
                    try:
                        if elements[0].is_displayed():
                            text = elements[0].text.strip()
                            if text:
                                self.logger.info(f"分类标题：{text}")
                                return text
                    except Exception:
                        pass
            except Exception:
                continue
        # 都不行就返回页面标题
        title = self.driver.title
        self.logger.info(f"使用页面标题作为分类标题：{title}")
        return title

    def get_book_list_count(self):
        """
        获取当前页图书列表数量（快速检查，不等待超时）

        Returns:
            int: 当前页的图书数量
        """
        self.logger.info("获取当前页图书列表数量")
        for selector in self.book_list_selectors:
            try:
                # 快速检查：用 find_elements 不触发超时等待
                elements = self.driver.find_elements(*selector)
                if elements and len(elements) > 0:
                    try:
                        if elements[0].is_displayed():
                            self.logger.info(f"使用定位器 {selector} 找到 {len(elements)} 本图书")
                            return len(elements)
                    except Exception:
                        pass
            except Exception:
                continue
        self.logger.warning("所有定位器都未找到图书列表，返回0")
        return 0

    def click_book_by_index(self, index):
        """
        点击列表中第 index 本图书

        Args:
            index (int): 图书索引，从 1 开始

        Returns:
            bool: 是否点击成功
        """
        self.logger.info(f"点击列表中第 {index} 本图书")
        for selector in self.book_list_selectors:
            try:
                elements = self.find_elements(selector)
                if elements and len(elements) >= index:
                    book_element = elements[index - 1]
                    # 尝试点击标题链接
                    for tag in ["h2 a", "a.title", "a"]:
                        try:
                            link = book_element.find_element(By.CSS_SELECTOR, tag)
                            self.logger.info(f"点击图书：{link.text}")
                            self.click_element(link)
                            return True
                        except Exception:
                            continue
                    # 都不行就点击元素本身
                    self.click_element(book_element)
                    return True
            except Exception:
                continue
        self.logger.error(f"未能找到第 {index} 本图书")
        return False

    def is_category_page_displayed(self):
        """
        判断分类页是否正确加载

        Returns:
            bool: 分类页加载成功返回 True，否则返回 False
        """
        self.logger.info("判断分类页是否正确加载")
        try:
            title = self.get_category_title()
            return bool(title)
        except Exception:
            return False

    def wait_for_page_load(self, keyword=None, timeout=5):
        """
        等待分类页加载完成（等待图书列表出现，或页面标题包含关键词）

        Args:
            keyword: 期望标题包含的关键词，可选
            timeout: 超时时间，默认5秒

        Returns:
            bool: 是否加载成功
        """
        self.logger.info("等待分类页加载完成...")
        start_time = time.time()
        while time.time() - start_time < timeout:
            # 检查是否有图书列表
            for selector in self.book_list_selectors:
                try:
                    elements = self.driver.find_elements(*selector)
                    if elements and len(elements) > 0:
                        try:
                            if elements[0].is_displayed():
                                self.logger.info(f"找到图书列表，页面加载完成，共 {len(elements)} 本")
                                return True
                        except Exception:
                            pass
                except Exception:
                    continue
            # 检查页面标题
            if keyword:
                try:
                    title = self.driver.title
                    if keyword in title or "豆瓣" in title:
                        self.logger.info(f"页面标题加载完成：{title}")
                        # 再多等一小会儿，让内容加载
                        time.sleep(1)
                        return True
                except Exception:
                    pass
            time.sleep(0.5)
        self.logger.warning("页面加载超时")
        return False

    def has_pagination(self):
        """
        判断是否有分页区域

        Returns:
            bool: 有分页返回 True，否则返回 False
        """
        self.logger.info("判断是否有分页区域")
        for selector in self.pagination_selectors:
            try:
                elements = self.driver.find_elements(*selector)
                if elements and len(elements) > 0:
                    try:
                        if elements[0].is_displayed():
                            self.logger.info("找到分页区域")
                            return True
                    except Exception:
                        pass
            except Exception:
                continue
        self.logger.info("未找到分页区域")
        return False
