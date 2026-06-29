"""
图书详情页测试用例
测试图书详情页的信息展示和页面元素是否正常
"""
import allure
import pytest

from common.data_reader import read_json
from common.logger import get_logger
from page.book_detail_page import BookDetailPage
from page.home_page import HomePage
from page.search_result_page import SearchResultPage

# 获取 logger 实例
logger = get_logger()

# 读取测试数据
book_detail_data = read_json("book_detail_data.json")
test_cases = book_detail_data.get("test_cases", [])


@allure.feature("图书详情")
class TestBookDetail:
    """
    图书详情页测试类
    包含图书详情页信息展示和页面元素验证的测试用例
    """

    @pytest.mark.parametrize("case_data", test_cases,
                             ids=[case["case_name"] for case in test_cases])
    @allure.story("详情页信息")
    @allure.title("{case_data[case_name]} - 测试图书详情页信息展示")
    def test_book_detail_info(self, driver, case_data):
        """
        测试图书详情页信息展示

        Args:
            driver: WebDriver 实例
            case_data: 测试用例数据字典
        """
        # 提取测试数据
        search_keyword = case_data["search_keyword"]
        expect_title_contains = case_data["expect_title_contains"]
        expect_author_contains = case_data["expect_author_contains"]
        case_name = case_data["case_name"]

        logger.info(f"开始执行测试用例：{case_name}")

        # 实例化页面对象
        home_page = HomePage(driver)
        search_result_page = SearchResultPage(driver)
        book_detail_page = BookDetailPage(driver)

        with allure.step("步骤1：打开豆瓣读书首页"):
            logger.info("步骤1：打开豆瓣读书首页")
            home_page.open()

        with allure.step(f"步骤2：搜索图书，关键词：{search_keyword}"):
            logger.info(f"步骤2：搜索图书，关键词：{search_keyword}")
            home_page.search_book(search_keyword)

        with allure.step("步骤3：点击第一个搜索结果进入详情页"):
            logger.info("步骤3：点击第一个搜索结果进入详情页")
            search_result_page.click_first_book()

        with allure.step("步骤4：验证详情页信息"):
            logger.info("步骤4：验证详情页信息")

            # 验证详情页是否正确加载
            logger.info("验证详情页是否正确加载")
            assert book_detail_page.is_book_detail_displayed(), (
                "图书详情页未正确加载显示"
            )

            # 验证图书标题包含预期关键词
            logger.info(f"验证图书标题包含：{expect_title_contains}")
            actual_title = book_detail_page.get_book_title()
            assert expect_title_contains in actual_title, (
                f"图书标题不包含预期关键词，预期包含：{expect_title_contains}，实际标题：{actual_title}"
            )

            # 验证作者信息包含预期作者
            logger.info(f"验证作者信息包含：{expect_author_contains}")
            actual_author = book_detail_page.get_book_author()
            assert expect_author_contains in actual_author, (
                f"作者信息不包含预期作者，预期包含：{expect_author_contains}，实际作者：{actual_author}"
            )

            # 验证评分存在且不为空
            logger.info("验证评分存在且不为空")
            actual_rating = book_detail_page.get_book_rating()
            assert actual_rating and actual_rating.strip(), (
                f"评分为空或不存在，实际评分：{actual_rating}"
            )

        logger.info(f"测试用例执行完成：{case_name}")

    @pytest.mark.parametrize("case_data", test_cases,
                             ids=[case["case_name"] for case in test_cases])
    @allure.story("页面元素")
    @allure.title("{case_data[case_name]} - 测试详情页各元素是否正常展示")
    def test_book_detail_page_elements(self, driver, case_data):
        """
        测试详情页各元素是否正常展示

        Args:
            driver: WebDriver 实例
            case_data: 测试用例数据字典
        """
        # 提取测试数据
        search_keyword = case_data["search_keyword"]
        case_name = case_data["case_name"]

        logger.info(f"开始执行测试用例：{case_name}")

        # 实例化页面对象
        home_page = HomePage(driver)
        search_result_page = SearchResultPage(driver)
        book_detail_page = BookDetailPage(driver)

        with allure.step("步骤1：打开豆瓣读书首页"):
            logger.info("步骤1：打开豆瓣读书首页")
            home_page.open()

        with allure.step(f"步骤2：搜索图书，关键词：{search_keyword}"):
            logger.info(f"步骤2：搜索图书，关键词：{search_keyword}")
            home_page.search_book(search_keyword)

        with allure.step("步骤3：点击第一个搜索结果进入详情页"):
            logger.info("步骤3：点击第一个搜索结果进入详情页")
            search_result_page.click_first_book()

        with allure.step("步骤4：检查各元素是否可见"):
            logger.info("步骤4：检查各元素是否可见")

            # 验证图书标题可见
            logger.info("验证图书标题可见")
            assert book_detail_page.is_element_visible(book_detail_page.book_title), (
                "图书标题不可见"
            )

            # 验证作者信息可见
            logger.info("验证作者信息可见")
            assert book_detail_page.is_element_visible(book_detail_page.book_author), (
                "作者信息不可见"
            )

            # 验证评分可见
            logger.info("验证评分可见")
            assert book_detail_page.is_element_visible(book_detail_page.book_rating), (
                "评分不可见"
            )

            # 验证内容简介可见（如果有的话）
            logger.info("验证内容简介可见")
            try:
                summary_visible = book_detail_page.is_element_visible(
                    book_detail_page.book_summary
                )
                if summary_visible:
                    logger.info("内容简介可见")
                else:
                    logger.info("内容简介不可见（可能该图书暂无简介）")
            except Exception as e:
                logger.info(f"内容简介检查异常：{e}，跳过该断言")

        logger.info(f"测试用例执行完成：{case_name}")
