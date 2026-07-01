"""
豆瓣读书搜索结果页页面类
封装搜索结果页的元素定位和业务操作方法
"""
from selenium.webdriver.common.by import By

from base.base_page import BasePage


class SearchResultPage(BasePage):
    """
    豆瓣读书搜索结果页类
    继承自 BasePage，封装搜索结果页相关的元素定位和业务操作
    """

    # ==================== 元素定位器 ====================

    # 搜索结果列表（多个结果项）- 多套备选定位器，增加成功率
    result_items_selectors = [
        (By.CSS_SELECTOR, "li.subject-item"),
        (By.CSS_SELECTOR, "div.item-root"),
        (By.CSS_SELECTOR, ".result-list .item"),
        (By.XPATH, "//li[contains(@class, 'subject')]"),
        (By.CSS_SELECTOR, "div#root li"),
    ]

    # 第一个搜索结果的标题链接 - 多套备选
    first_book_title_selectors = [
        (By.CSS_SELECTOR, "li.subject-item h2 a"),
        (By.CSS_SELECTOR, "div.item-root h3 a"),
        (By.CSS_SELECTOR, ".result-list .item h2 a"),
        (By.XPATH, "//a[contains(@class, 'title')]"),
    ]

    # 无搜索结果提示文本 - 多套备选
    no_result_selectors = [
        (By.CSS_SELECTOR, "div.no-result"),
        (By.CSS_SELECTOR, ".empty-state"),
        (By.XPATH, "//div[contains(text(), '没有找到')]"),
        (By.XPATH, "//div[contains(text(), '暂无')]"),
    ]

    # ==================== 业务操作方法 ====================

    def get_result_items(self):
        """
        获取搜索结果列表项（尝试多套定位器，快速检查，不等待超时）

        Returns:
            list: 搜索结果元素列表
        """
        self.logger.info("获取搜索结果列表项")
        for selector in self.result_items_selectors:
            try:
                # 快速检查：用 find_elements 不触发超时等待
                elements = self.driver.find_elements(*selector)
                if elements and len(elements) > 0:
                    # 检查第一个元素是否可见
                    try:
                        if elements[0].is_displayed():
                            self.logger.info(f"使用定位器 {selector} 找到 {len(elements)} 个结果")
                            return elements
                    except Exception:
                        pass
            except Exception:
                continue
        self.logger.warning("所有定位器都未找到结果项，返回空列表")
        return []

    def get_result_titles(self):
        """
        获取所有搜索结果的图书标题列表

        Returns:
            list: 图书标题字符串列表
        """
        self.logger.info("获取所有搜索结果的图书标题列表")
        items = self.get_result_items()
        titles = []
        for item in items:
            try:
                # 尝试多种方式获取标题
                title_element = None
                for tag in ["h2 a", "h3 a", ".title a", "a.title"]:
                    try:
                        title_element = item.find_element(By.CSS_SELECTOR, tag)
                        break
                    except Exception:
                        continue
                if title_element is None:
                    # 尝试找任何 a 标签
                    try:
                        title_element = item.find_element(By.TAG_NAME, "a")
                    except Exception:
                        continue
                if title_element is not None:
                    title = title_element.text.strip()
                    if title:
                        titles.append(title)
            except Exception:
                continue
        self.logger.info(f"共获取到 {len(titles)} 个搜索结果标题")
        return titles

    def click_first_book(self):
        """
        点击第一个搜索结果，进入详情页

        Returns:
            bool: 是否点击成功
        """
        self.logger.info("点击第一个搜索结果")
        items = self.get_result_items()
        if items and len(items) > 0:
            try:
                # 点击第一个结果的链接
                first_item = items[0]
                for tag in ["h2 a", "h3 a", ".title a", "a.title", "a"]:
                    try:
                        link = first_item.find_element(By.CSS_SELECTOR, tag)
                        self.click_element(link)
                        self.logger.info("点击第一个搜索结果成功")
                        return True
                    except Exception:
                        continue
                # 都不行就点击元素本身
                self.click_element(first_item)
                return True
            except Exception as e:
                self.logger.error(f"点击第一个搜索结果失败：{e}")
                return False
        self.logger.warning("没有找到搜索结果，无法点击")
        return False

    def is_result_empty(self):
        """
        判断是否无搜索结果

        Returns:
            bool: 无搜索结果返回 True，有结果返回 False
        """
        self.logger.info("判断搜索结果是否为空")
        # 先检查是否有无结果提示
        for selector in self.no_result_selectors:
            try:
                element = self.find_element(selector)
                if element and element.is_displayed():
                    self.logger.info("找到无结果提示，搜索结果为空")
                    return True
            except Exception:
                continue
        # 再检查结果数量
        items = self.get_result_items()
        result = len(items) == 0
        self.logger.info(f"搜索结果数量：{len(items)}，是否为空：{result}")
        return result

    def get_title(self):
        """
        获取页面标题（用于验证搜索结果页）

        Returns:
            str: 页面标题
        """
        return self.driver.title
