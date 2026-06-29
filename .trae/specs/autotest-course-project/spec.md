# 基于Selenium+Python的豆瓣读书自动化测试实战 - Product Requirement Document

## Overview
- **Summary**: 本项目是《自动化测试》课程设计，使用 Python 语言结合 Selenium WebDriver 和 pytest 框架，对豆瓣读书（book.douban.com）的核心功能模块进行自动化测试。项目采用 Page Object 设计模式，实现数据驱动测试，包含显式等待、断言、失败自动截图、日志记录和 Allure 测试报告等完整功能。
- **Purpose**: 全面展示对自动化测试核心知识与技能的掌握，包括 Selenium WebDriver、pytest 框架、PO 设计模式、数据驱动思想、日志记录等，完成从被测对象分析到测试报告生成的全流程实践。
- **Target Users**: 课程教师（作为评分依据）、学习自动化测试的学生（作为参考案例）。

## Goals
- 完成豆瓣读书至少 3 个核心业务场景的自动化测试脚本
- 严格遵循 Page Object 设计模式，实现页面元素定位与业务操作分离
- 实现数据驱动测试，测试数据与脚本完全分离（JSON 格式）
- 正确使用显式等待（WebDriverWait），每条用例有明确断言
- 实现用例失败自动截图功能
- 使用 logging 模块在关键步骤记录日志
- 生成 Allure HTML 格式测试报告，包含用例统计、执行耗时、失败截图等
- 项目结构规范，代码遵循 PEP8 标准，有清晰中文注释

## Non-Goals (Out of Scope)
- 不进行性能测试、压力测试、安全测试
- 不实现完整的 CI/CD 流水线集成
- 不测试豆瓣全站功能，仅覆盖核心模块的典型场景
- 不编写课程设计报告文档（本项目仅提供代码实现和测试脚本）
- 不涉及移动端自动化测试
- 不测试需要登录验证码的场景（避免反爬限制）

## Background & Context
- 本项目是广州华商学院《自动化测试》课程（课程代码 SKC3203）的期末课程设计
- 技术栈要求：Python + Selenium + pytest
- 设计模式要求：Page Object Design Pattern
- 项目文件夹命名：AutoTestProject+学号后两位
- 评分标准共 8 项，总分 100 分，包括：选题规范度（5分）、功能完整性（30分）、PO模式设计与实现（20分）、数据驱动与参数化（20分）、等待机制与断言（10分）、日志与失败截图（5分）、测试报告质量（5分）、设计报告格式规范（5分）
- 选择豆瓣读书作为被测对象原因：网站结构稳定，反爬相对温和，有丰富的功能模块（搜索、分类浏览、图书详情等），适合自动化测试练习

## Functional Requirements
- **FR-1**: 项目规范目录结构，包含 base、page、testcase、data、report、logs、common 等模块
- **FR-2**: BasePage 基类封装，包含元素定位、点击、输入、获取文本、显式等待等通用方法
- **FR-3**: Page Object 页面类实现，至少覆盖首页、搜索结果页、图书详情页、分类页 4 个页面
- **FR-4**: 图书搜索功能自动化测试（数据驱动，至少 3 组测试数据）
- **FR-5**: 图书分类浏览功能自动化测试
- **FR-6**: 图书详情页信息展示功能自动化测试
- **FR-7**: JSON 格式测试数据管理，与脚本完全分离
- **FR-8**: 用例失败自动截图保存功能
- **FR-9**: logging 日志记录（INFO、ERROR 级别）
- **FR-10**: Allure 测试报告生成，包含完整统计信息和失败截图附件

## Non-Functional Requirements
- **NFR-1**: 代码遵循 Python PEP8 规范，命名清晰，有中文注释
- **NFR-2**: 全部使用显式等待（WebDriverWait），禁止硬编码 time.sleep()
- **NFR-3**: 每条测试用例必须有明确的 assert 断言
- **NFR-4**: 测试脚本应稳定运行，无语法错误和运行时崩溃
- **NFR-5**: 项目结构清晰，各模块职责明确，代码复用性高
- **NFR-6**: 日志信息完整，关键步骤（打开浏览器、定位元素、点击、断言等）均有记录

## Constraints
- **Technical**: 
  - 必须使用 Python 语言
  - 必须使用 Selenium WebDriver 库
  - 必须使用 pytest 测试框架
  - 必须采用 Page Object 设计模式
  - 测试数据必须存放在独立文件中（JSON）
  - 必须使用 Allure 生成测试报告
- **Business**: 
  - 至少覆盖 3 个核心业务场景
  - 数据驱动至少 3 组数据
  - 需考虑反爬限制，脚本不宜频繁请求
- **Dependencies**: 
  - Python 3.x
  - Selenium 库
  - pytest 框架
  - allure-pytest 插件
  - 浏览器驱动（ChromeDriver）
  - PyYAML（如用 YAML）/ openpyxl（如用 Excel）

## Assumptions
- 豆瓣读书网站（book.douban.com）在测试期间可正常访问
- 测试环境已安装 Chrome 浏览器和对应版本的 ChromeDriver
- 被测网站没有严重的反爬机制导致脚本无法运行
- 测试用例仅覆盖公开可访问的页面，不涉及需要登录的功能
- 网络连接稳定，页面加载时间在合理范围内

## Acceptance Criteria

### AC-1: 项目结构规范
- **Given**: 项目创建完成
- **When**: 查看项目目录结构
- **Then**: 目录包含 base、page、testcase、data、report、logs、common 等文件夹，各模块职责清晰
- **Verification**: `human-judgment`
- **Notes**: 对照课程要求的目录结构进行检查

### AC-2: BasePage 基类设计合理
- **Given**: BasePage 基类已实现
- **When**: 查看基类代码
- **Then**: 封装了元素查找、点击、输入、获取文本、显式等待等通用方法，代码复用性高
- **Verification**: `human-judgment`

### AC-3: PO模式严格分离
- **Given**: 页面类和测试用例类已实现
- **When**: 检查页面类与测试用例的关系
- **Then**: 页面元素定位与业务操作封装在 Page 类中，测试用例仅调用 Page 类方法，两者完全分离
- **Verification**: `human-judgment`

### AC-4: 图书搜索功能测试通过
- **Given**: 测试数据已准备，搜索页面 PO 类已实现
- **When**: 运行图书搜索测试用例（至少 3 组数据）
- **Then**: 所有测试用例执行完成，断言验证搜索结果与预期一致
- **Verification**: `programmatic`

### AC-5: 分类浏览功能测试通过
- **Given**: 分类页 PO 类已实现
- **When**: 运行分类浏览测试用例
- **Then**: 测试用例执行通过，断言验证分类跳转正确、图书列表展示正常
- **Verification**: `programmatic`

### AC-6: 图书详情页测试通过
- **Given**: 图书详情页 PO 类已实现
- **When**: 运行图书详情页测试用例
- **Then**: 测试用例执行通过，断言验证图书标题、作者、出版社等信息正确展示
- **Verification**: `programmatic`

### AC-7: 数据驱动实现正确
- **Given**: JSON 测试数据文件已创建
- **When**: 检查测试用例参数化实现
- **Then**: 测试数据完全存放在 JSON 文件中，使用 pytest.mark.parametrize 进行参数化，至少 3 组数据
- **Verification**: `human-judgment`

### AC-8: 显式等待机制正确
- **Given**: 所有测试脚本已编写
- **When**: 检查等待相关代码
- **Then**: 全部使用 WebDriverWait 显式等待，无硬编码 time.sleep()
- **Verification**: `human-judgment`

### AC-9: 断言覆盖完整
- **Given**: 所有测试用例已编写
- **When**: 检查每条测试用例
- **Then**: 每条测试用例都有明确的 assert 断言，验证预期结果
- **Verification**: `human-judgment`

### AC-10: 失败自动截图功能正常
- **Given**: 测试框架配置了失败截图钩子
- **When**: 某条测试用例执行失败
- **Then**: 自动截取当前页面截图，保存到指定目录，截图文件名包含用例名和时间戳
- **Verification**: `programmatic`

### AC-11: 日志记录完整
- **Given**: logging 模块已配置
- **When**: 运行测试用例后查看日志文件
- **Then**: 关键步骤（打开浏览器、定位元素、点击按钮、断言等）有 INFO 级别日志，出错时有 ERROR 级别日志
- **Verification**: `human-judgment`

### AC-12: Allure测试报告完整
- **Given**: 测试执行完成
- **When**: 生成并查看 Allure 测试报告
- **Then**: 报告包含用例总数、通过数、失败数、执行耗时、每条用例详细状态，失败用例包含截图附件
- **Verification**: `programmatic`

### AC-13: 代码规范
- **Given**: 项目代码已完成
- **When**: 审查代码风格
- **Then**: 变量、函数、类命名遵循 PEP8 规范，关键代码有清晰中文注释
- **Verification**: `human-judgment`

## Open Questions
- [ ] 学号后两位具体是多少（用于项目文件夹命名）？当前默认使用 01 作为占位符
- [ ] 是否需要增加更多测试场景（如排行榜、标签筛选等）？
- [ ] 测试环境是否已安装 Allure 命令行工具？
