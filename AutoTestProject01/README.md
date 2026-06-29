# AutoTestProject01 豆瓣读书自动化测试项目

## 项目简介

本项目是基于 **Selenium + Pytest** 的 Web 自动化测试框架，采用 **Page Object Model (POM)** 设计模式，针对豆瓣读书网站进行功能自动化测试。项目集成了 Allure 测试报告系统，支持失败自动截图、日志记录、数据驱动等功能。

## 技术栈

| 技术/工具 | 版本要求 | 说明 |
|-----------|----------|------|
| Python | >= 3.8 | 编程语言 |
| Selenium | >= 4.0.0 | Web 自动化测试框架 |
| Pytest | >= 7.0.0 | 测试框架 |
| Allure Pytest | >= 2.13.0 | 测试报告插件 |
| pytest-html | >= 3.0.0 | HTML 测试报告 |
| Chrome 浏览器 | 最新版 | 测试浏览器 |
| ChromeDriver | 与浏览器匹配 | 浏览器驱动 |

## 项目结构

```
AutoTestProject01/
├── base/                          # 页面基类目录
│   ├── __init__.py               # 模块说明
│   └── base_page.py              # BasePage 基类，封装 Selenium 常用操作
├── common/                        # 公共工具模块
│   ├── __init__.py               # 模块说明
│   ├── config.py                 # 全局配置常量
│   ├── logger.py                 # 日志模块（单例模式）
│   ├── screenshot.py             # 截图工具
│   └── data_reader.py            # JSON 数据读取工具
├── page/                          # Page Object 页面类目录
│   ├── __init__.py               # 模块说明
│   ├── home_page.py              # 豆瓣读书首页
│   ├── search_result_page.py     # 搜索结果页
│   ├── book_detail_page.py       # 图书详情页
│   └── category_page.py          # 分类浏览页
├── testcase/                      # 测试用例目录
│   ├── __init__.py               # 模块说明
│   ├── test_book_search.py       # 图书搜索功能测试
│   ├── test_book_detail.py       # 图书详情页测试
│   └── test_category_browse.py   # 分类浏览功能测试
├── data/                          # 测试数据目录
│   ├── __init__.py               # 模块说明
│   ├── search_data.json          # 搜索测试数据
│   ├── category_data.json        # 分类测试数据
│   └── book_detail_data.json     # 图书详情测试数据
├── report/                        # 测试报告目录
│   ├── __init__.py               # 模块说明
│   ├── allure-results/           # Allure 测试结果数据
│   ├── allure-report/            # Allure HTML 报告（生成后）
│   └── screenshots/              # 失败截图目录
│       └── __init__.py
├── logs/                          # 日志目录
│   ├── __init__.py               # 模块说明
│   └── autotest_YYYYMMDD.log     # 按日期生成的日志文件
├── conftest.py                   # pytest 配置文件（fixtures、钩子函数）
├── pytest.ini                    # pytest 配置文件
├── requirements.txt              # Python 依赖包列表
├── run_test.sh                   # Linux/Mac 一键运行脚本
├── run_test.bat                  # Windows 一键运行脚本
└── README.md                     # 项目说明文档
```

## 环境要求

### 系统要求
- Windows / macOS / Linux
- Python 3.8 及以上版本
- Chrome 浏览器（最新版）

### 前置依赖
1. **Python 环境**：确保已安装 Python 3.8+
2. **Chrome 浏览器**：下载并安装最新版 Chrome
3. **ChromeDriver**：
   - Selenium 4.6+ 内置 Selenium Manager，可自动管理驱动
   - 如使用旧版本，需手动下载与 Chrome 版本匹配的 ChromeDriver 并配置到 PATH 中
4. **Allure 命令行工具**（可选，用于生成 Allure HTML 报告）
   - 安装方式：参考 [Allure 官方文档](https://allurereport.org/docs/install/)

## 安装和运行步骤

### 1. 克隆项目

```bash
git clone <项目地址>
cd AutoTestProject01
```

### 2. 安装项目依赖

```bash
pip install -r requirements.txt
```

### 3. 运行测试

#### 方式一：使用一键运行脚本（推荐）

**Linux / macOS：**
```bash
chmod +x run_test.sh
./run_test.sh
```

**Windows：**
```cmd
run_test.bat
```

#### 方式二：手动执行 pytest

```bash
# 运行所有测试用例
pytest

# 运行指定测试文件
pytest testcase/test_book_search.py

# 运行指定测试类
pytest testcase/test_book_search.py::TestBookSearch

# 运行指定测试方法
pytest testcase/test_book_search.py::TestBookSearch::test_search_book

# 无头模式运行（不显示浏览器）
HEADLESS=true pytest

# 显示详细输出
pytest -v

# 仅收集测试用例（不执行）
pytest --collect-only
```

## 测试报告生成方法

### 1. Allure 报告（推荐）

#### 生成 Allure 结果数据

项目已在 `pytest.ini` 中配置了 Allure 结果输出目录，运行 pytest 会自动生成结果数据：

```bash
pytest
# 结果数据将保存到 report/allure-results/
```

#### 生成并查看 Allure HTML 报告

```bash
# 方式一：直接启动服务查看（推荐）
allure serve report/allure-results

# 方式二：生成静态 HTML 报告
allure generate report/allure-results -o report/allure-report --clean

# 打开报告
# macOS:
open report/allure-report/index.html
# Windows:
start report/allure-report/index.html
# Linux:
xdg-open report/allure-report/index.html
```

### 2. pytest-html 报告

```bash
pytest --html=report/report.html --self-contained-html
```

报告将生成在 `report/report.html`，使用浏览器打开即可查看。

## 核心功能说明

### 1. Page Object 设计模式
- 每个页面对应一个 Page 类，封装元素定位和业务操作
- 测试用例与页面实现解耦，提高代码可维护性

### 2. 失败自动截图
- 测试用例失败时自动截图
- 截图自动附加到 Allure 报告中
- 截图文件保存在 `report/screenshots/` 目录

### 3. 日志记录
- 单例模式的 logger 实例
- 同时输出到控制台和文件
- 日志文件按日期命名，保存在 `logs/` 目录

### 4. 数据驱动测试
- 使用 JSON 文件管理测试数据
- 支持 `@pytest.mark.parametrize` 参数化
- 测试数据与测试代码分离

### 5. Allure 报告集成
- 支持 @allure.feature、@allure.story 等特性标注
- 支持动态用例标题
- 支持分步骤展示测试过程

## 测试用例概览

| 测试模块 | 测试用例数 | 说明 |
|---------|-----------|------|
| 图书搜索 | 4 | 正常搜索、无结果搜索、空关键词等场景 |
| 图书详情 | 6 | 详情页信息展示、页面元素验证 |
| 分类浏览 | 6 | 分类导航跳转、图书列表展示 |
| **合计** | **16** | - |

## 配置说明

主要配置项定义在 `common/config.py` 中：

| 配置项 | 默认值 | 说明 |
|-------|--------|------|
| BASE_URL | https://book.douban.com | 测试网站基础 URL |
| TIMEOUT | 10 | 元素显式等待超时时间（秒） |
| BROWSER | chrome | 浏览器类型 |
| SCREENSHOT_DIR | report/screenshots | 截图保存目录 |
| LOG_DIR | logs | 日志保存目录 |
| DATA_DIR | data | 测试数据目录 |

## 常见问题

### 1. ChromeDriver 相关问题
如果遇到 ChromeDriver 版本不匹配问题，请确保：
- Selenium 版本 >= 4.6（自动管理驱动）
- 或手动下载对应版本的 ChromeDriver 并配置到 PATH

### 2. 无头模式运行
在 CI/CD 或无图形界面环境下运行：
```bash
HEADLESS=true pytest
```

### 3. 元素定位失败
- 检查网络连接是否正常
- 确认网站结构是否发生变化
- 适当调整 `TIMEOUT` 超时时间
