# 基于Selenium+Python的豆瓣读书自动化测试实战 - The Implementation Plan (Decomposed and Prioritized Task List)

## [x] Task 1: 项目目录结构搭建与基础配置
- **Priority**: high
- **Depends On**: None
- **Description**: 
  - 创建项目根目录 AutoTestProject01
  - 搭建规范的目录结构：base、page、testcase、data、report、logs、common
  - 创建 requirements.txt 列出所有依赖
  - 创建 pytest 配置文件 pytest.ini
  - 创建 __init__.py 文件使各目录成为 Python 包
- **Acceptance Criteria Addressed**: [AC-1]
- **Test Requirements**:
  - `programmatic` TR-1.1: 项目目录结构完整，包含 base/page/testcase/data/report/logs/common 7 个目录
  - `programmatic` TR-1.2: requirements.txt 包含 selenium、pytest、allure-pytest 等必要依赖
  - `human-judgement` TR-1.3: 目录命名规范，各目录职责清晰
- **Notes**: 项目命名使用 AutoTestProject01，学号后两位默认为 01

## [x] Task 2: 公共工具模块实现（日志、配置、数据读取）
- **Priority**: high
- **Depends On**: Task 1
- **Description**: 
  - 实现 logger.py：封装 logging 模块，支持文件输出和控制台输出，包含 INFO/ERROR 级别
  - 实现 config.py：管理全局配置（URL、超时时间、浏览器类型等）
  - 实现 data_reader.py：封装 JSON 数据文件读取方法
  - 实现 screenshot.py：封装截图保存工具方法
- **Acceptance Criteria Addressed**: [AC-11]
- **Test Requirements**:
  - `programmatic` TR-2.1: logger 模块可正常生成日志文件，包含 INFO 和 ERROR 级别日志
  - `programmatic` TR-2.2: data_reader 可正确读取 JSON 文件并返回字典/列表格式数据
  - `human-judgement` TR-2.3: 公共工具代码结构清晰，有中文注释
- **Notes**: 日志文件按日期命名，保存在 logs 目录

## [x] Task 3: BasePage 基类封装
- **Priority**: high
- **Depends On**: Task 2
- **Description**: 
  - 创建 base_page.py 基类
  - 封装元素查找方法（find_element、find_elements）
  - 封装点击、输入、获取文本、清除等常用操作
  - 封装显式等待方法（等待元素可见、等待元素可点击、等待页面加载）
  - 封装截图方法
  - 集成 logger 日志记录
- **Acceptance Criteria Addressed**: [AC-2, AC-8]
- **Test Requirements**:
  - `programmatic` TR-3.1: BasePage 基类包含 find_element、click、input_text、get_text 等核心方法
  - `programmatic` TR-3.2: 所有元素定位均使用 WebDriverWait 显式等待
  - `human-judgement` TR-3.3: 基类设计合理，代码复用性高，有完整中文注释
- **Notes**: 默认显式等待超时时间设为 10 秒

## [x] Task 4: Page Object 页面类实现
- **Priority**: high
- **Depends On**: Task 3
- **Description**: 
  - 实现 HomePage（首页）：封装搜索框元素、搜索按钮、导航菜单等
  - 实现 SearchResultPage（搜索结果页）：封装结果列表、结果数量、筛选选项等
  - 实现 BookDetailPage（图书详情页）：封装图书标题、作者、出版社、价格、评分等
  - 实现 CategoryPage（分类页）：封装分类导航、图书列表等
  - 每个页面类继承 BasePage，封装页面特有元素和业务操作方法
- **Acceptance Criteria Addressed**: [AC-3]
- **Test Requirements**:
  - `programmatic` TR-4.1: 4 个页面类均正确继承 BasePage
  - `programmatic` TR-4.2: 每个页面类封装了对应的元素定位和业务操作方法
  - `human-judgement` TR-4.3: 页面类与测试用例完全分离，页面类不包含断言逻辑
- **Notes**: 元素定位优先使用 CSS Selector 或 XPath，保证稳定性

## [x] Task 5: JSON 测试数据文件创建
- **Priority**: high
- **Depends On**: Task 1
- **Description**: 
  - 创建 search_data.json：图书搜索测试数据（至少 3 组，含正常关键词、特殊字符、无结果关键词等）
  - 创建 category_data.json：分类浏览测试数据
  - 创建 book_detail_data.json：图书详情页测试数据（指定几本具体图书）
- **Acceptance Criteria Addressed**: [AC-7]
- **Test Requirements**:
  - `programmatic` TR-5.1: JSON 文件格式正确，可被正常解析
  - `programmatic` TR-5.2: 搜索测试数据至少包含 3 组不同的测试用例数据
  - `human-judgement` TR-5.3: 测试数据覆盖正常、异常等多种场景
- **Notes**: 测试数据与预期结果一一对应

## [x] Task 6: conftest.py 与 Fixture 配置
- **Priority**: high
- **Depends On**: Task 2, Task 3
- **Description**: 
  - 创建 conftest.py 文件
  - 实现浏览器驱动 fixture（setup/teardown）
  - 实现失败自动截图钩子（pytest_runtest_makereport）
  - 集成 Allure 环境配置
  - 配置测试数据加载 fixture
- **Acceptance Criteria Addressed**: [AC-10]
- **Test Requirements**:
  - `programmatic` TR-6.1: 浏览器驱动 fixture 可正常启动和关闭浏览器
  - `programmatic` TR-6.2: 用例失败时自动截图并保存到指定目录
  - `human-judgement` TR-6.3: fixture 设计合理，作用域设置得当
- **Notes**: 默认使用 Chrome 浏览器，无头模式可配置

## [x] Task 7: 图书搜索功能测试用例
- **Priority**: high
- **Depends On**: Task 4, Task 5, Task 6
- **Description**: 
  - 创建 test_book_search.py 测试文件
  - 实现搜索功能测试用例（数据驱动，读取 JSON 数据）
  - 使用 pytest.mark.parametrize 进行参数化
  - 每条用例有明确断言（验证搜索结果页标题、结果数量等）
  - 添加 Allure 装饰器（@allure.feature、@allure.story、@allure.title）
- **Acceptance Criteria Addressed**: [AC-4, AC-7, AC-9]
- **Test Requirements**:
  - `programmatic` TR-7.1: 至少 3 组数据驱动的搜索测试用例可正常执行
  - `programmatic` TR-7.2: 每条测试用例都有明确的 assert 断言
  - `human-judgement` TR-7.3: 测试用例命名规范，场景覆盖合理
- **Notes**: 测试用例之间保持独立，互不影响

## [x] Task 8: 分类浏览功能测试用例
- **Priority**: high
- **Depends On**: Task 4, Task 6
- **Description**: 
  - 创建 test_category_browse.py 测试文件
  - 实现分类导航跳转测试用例
  - 实现分类页图书列表展示测试用例
  - 添加 Allure 装饰器
  - 每条用例有明确断言
- **Acceptance Criteria Addressed**: [AC-5, AC-9]
- **Test Requirements**:
  - `programmatic` TR-8.1: 分类浏览测试用例可正常执行并通过
  - `programmatic` TR-8.2: 每条测试用例都有明确的 assert 断言
  - `human-judgement` TR-8.3: 测试场景设计合理，覆盖核心分类功能
- **Notes**: 选择 2-3 个典型分类进行测试

## [x] Task 9: 图书详情页功能测试用例
- **Priority**: high
- **Depends On**: Task 4, Task 5, Task 6
- **Description**: 
  - 创建 test_book_detail.py 测试文件
  - 实现图书详情页信息展示测试用例
  - 验证图书标题、作者、出版社、评分等核心信息
  - 添加 Allure 装饰器
  - 每条用例有明确断言
- **Acceptance Criteria Addressed**: [AC-6, AC-9]
- **Test Requirements**:
  - `programmatic` TR-9.1: 图书详情页测试用例可正常执行并通过
  - `programmatic` TR-9.2: 每条测试用例都有明确的 assert 断言
  - `human-judgement` TR-9.3: 验证的信息字段全面，覆盖详情页核心内容
- **Notes**: 选择 2-3 本具体图书进行测试

## [x] Task 10: Allure 报告集成与优化
- **Priority**: medium
- **Depends On**: Task 7, Task 8, Task 9
- **Description**: 
  - 完善 Allure 报告配置
  - 在关键步骤添加 allure.step 装饰
  - 失败用例自动附加截图到 Allure 报告
  - 添加环境信息到 Allure 报告
  - 编写运行脚本 run_test.sh 或 run_test.bat
- **Acceptance Criteria Addressed**: [AC-12]
- **Test Requirements**:
  - `programmatic` TR-10.1: 可生成完整的 Allure HTML 报告
  - `programmatic` TR-10.2: 报告包含用例总数、通过数、失败数、执行耗时等统计
  - `programmatic` TR-10.3: 失败用例在报告中包含截图附件
  - `human-judgement` TR-10.4: 报告结构清晰，信息完整美观
- **Notes**: 报告生成命令：allure generate allure-results -o allure-report

## [x] Task 11: 代码规范与整体优化
- **Priority**: medium
- **Depends On**: Task 10
- **Description**: 
  - 检查并优化代码命名，确保符合 PEP8 规范
  - 完善中文注释，关键代码段有清晰说明
  - 优化导入语句，移除未使用的导入
  - 编写 README.md 说明项目使用方法
  - 整体测试，确保所有用例稳定运行
- **Acceptance Criteria Addressed**: [AC-13]
- **Test Requirements**:
  - `programmatic` TR-11.1: 所有测试用例可稳定运行通过
  - `human-judgement` TR-11.2: 代码命名规范，符合 PEP8
  - `human-judgement` TR-11.3: 关键代码有清晰中文注释
  - `human-judgement` TR-11.4: README 文档清晰，包含环境搭建和运行说明
- **Notes**: 可使用 flake8 或 pylint 检查代码规范
