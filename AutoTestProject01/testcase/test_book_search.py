"""
图书搜索功能测试用例
测试豆瓣读书的搜索功能，包括正常搜索和无结果搜索场景
"""
import allure
import pytest

from common.data_reader import read_json
from common.logger import get_logger
from page.home_page import HomePage
from page.search_result_page import SearchResultPage

# 获取 logger 实例
logger = get_logger()

# 读取测试数据
search_data = read_json("search_data.json")
test_cases = search_data.get("test_cases", [])


@allure.feature("图书搜索")
class TestBookSearch:
    """
    图书搜索功能测试类
    测试豆瓣读书的搜索功能
    """

    @allure.story("搜索功能")
    @pytest.mark.parametrize(
        "case_data",
        test_cases,
        ids=lambda x: x["case_name"] if isinstance(x, dict) else str(x)
    )
    def test_search_book(self, driver, case_data):
        """
        测试图书搜索功能

        Args:
            driver: WebDriver 实例（fixture）
            case_data: 单条测试用例数据
        """
        # 提取测试数据
        case_name = case_data["case_name"]
        keyword = case_data["keyword"]
        expect_has_result = case_data["expect_has_result"]

        # 动态设置 Allure 用例标题
        allure.dynamic.title(case_name)

        logger.info(f"开始执行测试用例：{case_name}")
        logger.info(f"搜索关键词：{keyword}，期望有结果：{expect_has_result}")

        # 实例化页面对象
        home_page = HomePage(driver)
        search_result_page = SearchResultPage(driver)

        # 步骤1：打开豆瓣读书首页
        with allure.step("打开豆瓣读书首页"):
            logger.info("步骤1：打开豆瓣读书首页")
            home_page.open()

        # 步骤2：在搜索框输入关键词
        with allure.step(f"在搜索框输入关键词：{keyword}"):
            logger.info(f"步骤2：在搜索框输入关键词：{keyword}")
            home_page.input_text(home_page.search_input, keyword)

        # 步骤3：点击搜索按钮
        with allure.step("点击搜索按钮"):
            logger.info("步骤3：点击搜索按钮")
            home_page.click(home_page.search_button)

        # 步骤4：验证搜索结果
        with allure.step("验证搜索结果"):
            logger.info("步骤4：验证搜索结果")

            if expect_has_result:
                # 有结果的断言
                logger.info("验证有结果场景")

                # 断言页面标题包含关键词
                page_title = search_result_page.get_title()
                logger.info(f"页面标题：{page_title}")
                assert keyword in page_title, (
                    f"页面标题不包含关键词'{keyword}'，实际标题：{page_title}"
                )

                # 断言搜索结果数量大于0
                result_items = search_result_page.find_elements(
                    search_result_page.result_items
                )
                result_count = len(result_items)
                logger.info(f"搜索结果数量：{result_count}")
                assert result_count > 0, "搜索结果数量应为大于0"

                # 断言第一个结果标题包含关键词
                first_title = search_result_page.get_text(
                    search_result_page.first_book_title
                )
                logger.info(f"第一个搜索结果标题：{first_title}")
                assert keyword in first_title, (
                    f"第一个结果标题不包含关键词'{keyword}'，实际标题：{first_title}"
                )

            else:
                # 无结果的断言
                logger.info("验证无结果场景")

                # 断言无结果提示可见，或结果列表为空
                is_empty = search_result_page.is_result_empty()
                assert is_empty, "搜索结果应为空，但实际有结果"

        logger.info(f"测试用例 '{case_name}' 执行成功")
