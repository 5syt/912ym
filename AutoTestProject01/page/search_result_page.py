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

    # 搜索结果列表（多个结果项）
    result_items = (By.CSS_SELECTOR, "li.subject-item")

    # 搜索结果数量统计文本
    result_count_text = (By.CSS_SELECTOR, "div.sc-740dd40e-3 h2 span")

    # 搜索关键词展示区域
    search_keyword = (By.CSS_SELECTOR, "div.sc-740dd40e-3 h2")

    # 第一个搜索结果的标题链接
    first_book_title = (By.CSS_SELECTOR, "li.subject-item:first-child h2 a")

    # 无搜索结果提示文本
    no_result_tip = (By.CSS_SELECTOR, "div.sc-740dd40e-1")

    # ==================== 业务操作方法 ====================

    def get_result_count_text(self):
        """
        获取搜索结果数量统计文本

        Returns:
            str: 搜索结果数量统计文本
        """
        self.logger.info("获取搜索结果数量统计文本")
        return self.get_text(self.result_count_text)

    def get_result_titles(self):
        """
        获取所有搜索结果的图书标题列表

        Returns:
            list: 图书标题字符串列表
        """
        self.logger.info("获取所有搜索结果的图书标题列表")
        elements = self.find_elements(self.result_items)
        titles = []
        for element in elements:
            # 从每个结果项中提取标题链接文本
            title_element = element.find_element(By.CSS_SELECTOR, "h2 a")
            title = title_element.text.strip()
            if title:
                titles.append(title)
        self.logger.info(f"共获取到 {len(titles)} 个搜索结果标题")
        return titles

    def click_first_book(self):
        """
        点击第一个搜索结果，进入详情页

        Returns:
            SearchResultPage: 当前页面对象（页面跳转由测试用例处理）
        """
        self.logger.info("点击第一个搜索结果")
        self.click(self.first_book_title)
        return self

    def is_result_empty(self):
        """
        判断是否无搜索结果

        Returns:
            bool: 无搜索结果返回 True，有结果返回 False
        """
        self.logger.info("判断搜索结果是否为空")
        # 尝试查找无结果提示元素
        try:
            self.find_element(self.no_result_tip)
            self.logger.info("搜索结果为空")
            return True
        except Exception:
            # 如果找不到无结果提示，再检查是否有结果项
            try:
                elements = self.find_elements(self.result_items)
                result = len(elements) == 0
                self.logger.info(f"搜索结果是否为空：{result}")
                return result
            except Exception:
                self.logger.info("搜索结果为空（未找到结果列表）")
                return True
