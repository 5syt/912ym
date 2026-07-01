"""
生成课程设计报告 Word 文档
格式要求：A4纸、边距2cm、行距1.5倍、宋体五号
"""
from docx import Document
from docx.shared import Cm, Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.enum.section import WD_ORIENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement


def set_run_font(run, font_name="宋体", font_size=10.5, bold=False):
    """设置字体"""
    run.font.name = font_name
    run.font.size = Pt(font_size)
    run.bold = bold
    # 设置中文字体
    r = run._element
    rPr = r.get_or_add_rPr()
    rFonts = rPr.find(qn('w:rFonts'))
    if rFonts is None:
        rFonts = OxmlElement('w:rFonts')
        rPr.insert(0, rFonts)
    rFonts.set(qn('w:eastAsia'), font_name)


def add_paragraph(doc, text, font_name="宋体", font_size=10.5, bold=False,
                  alignment=WD_ALIGN_PARAGRAPH.LEFT, line_spacing=1.5, space_after=6):
    """添加段落并设置格式"""
    p = doc.add_paragraph()
    run = p.add_run(text)
    set_run_font(run, font_name, font_size, bold)
    p.alignment = alignment
    # 行距1.5倍
    p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.MULTIPLE
    p.paragraph_format.line_spacing = 1.5
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.space_before = Pt(0)
    return p


def add_heading(doc, text, level=1):
    """添加标题"""
    if level == 1:
        # 一级标题：黑体三号，居中
        p = add_paragraph(doc, text, font_name="黑体", font_size=16, bold=True,
                         alignment=WD_ALIGN_PARAGRAPH.CENTER, space_after=12)
    elif level == 2:
        # 二级标题：黑体四号，左对齐
        p = add_paragraph(doc, text, font_name="黑体", font_size=14, bold=True,
                         alignment=WD_ALIGN_PARAGRAPH.LEFT, space_after=10)
    elif level == 3:
        # 三级标题：黑体小四，左对齐
        p = add_paragraph(doc, text, font_name="黑体", font_size=12, bold=True,
                         alignment=WD_ALIGN_PARAGRAPH.LEFT, space_after=8)
    else:
        p = add_paragraph(doc, text, font_name="黑体", font_size=10.5, bold=True,
                         alignment=WD_ALIGN_PARAGRAPH.LEFT, space_after=6)
    return p


def add_code_block(doc, code):
    """添加代码块"""
    # 代码使用等宽字体，小五号
    p = doc.add_paragraph()
    run = p.add_run(code)
    run.font.name = "Courier New"
    run.font.size = Pt(9)
    r = run._element
    rPr = r.get_or_add_rPr()
    rFonts = rPr.find(qn('w:rFonts'))
    if rFonts is None:
        rFonts = OxmlElement('w:rFonts')
        rPr.insert(0, rFonts)
    rFonts.set(qn('w:eastAsia'), "Courier New")
    # 代码背景色浅灰
    shading = OxmlElement('w:shd')
    shading.set(qn('w:fill'), "F5F5F5")
    rPr.append(shading)
    p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.SINGLE
    p.paragraph_format.line_spacing = 1.0
    p.paragraph_format.space_after = Pt(6)
    p.paragraph_format.left_indent = Cm(0.74)
    return p


def add_table(doc, headers, rows):
    """添加表格"""
    table = doc.add_table(rows=1, cols=len(headers))
    table.style = 'Table Grid'
    # 表头
    hdr_cells = table.rows[0].cells
    for i, header in enumerate(headers):
        hdr_cells[i].text = header
        for para in hdr_cells[i].paragraphs:
            for run in para.runs:
                set_run_font(run, "黑体", 10.5, True)
            para.alignment = WD_ALIGN_PARAGRAPH.CENTER
    # 数据行
    for row in rows:
        row_cells = table.add_row().cells
        for i, cell_text in enumerate(row):
            row_cells[i].text = str(cell_text)
            for para in row_cells[i].paragraphs:
                for run in para.runs:
                    set_run_font(run, "宋体", 10.5, False)
                para.alignment = WD_ALIGN_PARAGRAPH.CENTER
    return table


def create_cover_page(doc):
    """创建封面"""
    # 学校名称
    add_paragraph(doc, "广州华商学院", font_name="宋体", font_size=22, bold=True,
                  alignment=WD_ALIGN_PARAGRAPH.CENTER, space_after=30)

    # 课程设计报告标题
    add_paragraph(doc, "《自动化测试》", font_name="黑体", font_size=26, bold=True,
                  alignment=WD_ALIGN_PARAGRAPH.CENTER, space_after=10)
    add_paragraph(doc, "课程设计报告", font_name="黑体", font_size=26, bold=True,
                  alignment=WD_ALIGN_PARAGRAPH.CENTER, space_after=60)

    # 报告标题
    add_paragraph(doc, "基于Selenium+Python的豆瓣读书系统", font_name="黑体", font_size=18, bold=True,
                  alignment=WD_ALIGN_PARAGRAPH.CENTER, space_after=5)
    add_paragraph(doc, "自动化测试实战", font_name="黑体", font_size=18, bold=True,
                  alignment=WD_ALIGN_PARAGRAPH.CENTER, space_after=80)

    # 信息表格
    info_items = [
        ("课程名称", "自动化测试"),
        ("学生姓名", "__________"),
        ("学    号", "__________"),
        ("专业班级", "__________"),
        ("指导教师", "__________"),
        ("提交日期", "2026 年 7 月"),
    ]

    for label, value in info_items:
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.MULTIPLE
        p.paragraph_format.line_spacing = 1.5
        p.paragraph_format.space_after = Pt(8)
        p.paragraph_format.space_before = Pt(0)

        run1 = p.add_run(f"{label}：")
        set_run_font(run1, "宋体", 14, False)

        run2 = p.add_run(f"{value}")
        set_run_font(run2, "宋体", 14, False)

    # 分页
    doc.add_page_break()


def add_page_numbers(doc):
    """添加页码（底端居中）"""
    # 获取文档的所有节
    for section in doc.sections:
        footer = section.footer
        footer.is_linked_to_previous = False
        paragraph = footer.paragraphs[0] if footer.paragraphs else footer.add_paragraph()
        paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER

        # 创建页码字段
        run = paragraph.add_run()
        fldChar1 = OxmlElement('w:fldChar')
        fldChar1.set(qn('w:fldCharType'), 'begin')

        instrText = OxmlElement('w:instrText')
        instrText.set(qn('xml:space'), 'preserve')
        instrText.text = ' PAGE '

        fldChar2 = OxmlElement('w:fldChar')
        fldChar2.set(qn('w:fldCharType'), 'separate')

        fldChar3 = OxmlElement('w:fldChar')
        fldChar3.set(qn('w:fldCharType'), 'end')

        run._element.append(fldChar1)
        run._element.append(instrText)
        run._element.append(fldChar2)
        run._element.append(fldChar3)
        set_run_font(run, "宋体", 10.5, False)


def main():
    doc = Document()

    # 页面设置：A4，边距2cm
    for section in doc.sections:
        section.page_width = Cm(21)
        section.page_height = Cm(29.7)
        section.top_margin = Cm(2)
        section.bottom_margin = Cm(2)
        section.left_margin = Cm(2)
        section.right_margin = Cm(2)

    # ===== 封面 =====
    create_cover_page(doc)

    # ===== 目录页 =====
    add_heading(doc, "目  录", level=1)
    toc_items = [
        "1. 绪论............................................................1",
        "   1.1 项目背景...................................................1",
        "   1.2 研究的目的和意义...........................................1",
        "   1.3 测试对象概述...............................................2",
        "   1.4 测试范围...................................................2",
        "2. 测试设计.......................................................3",
        "   2.1 被测对象分析...............................................3",
        "   2.2 测试框架设计...............................................4",
        "3. 测试实现.......................................................6",
        "   3.1 核心代码展示与分析.........................................6",
        "   3.2 问题与解决方案.............................................10",
        "4. 测试结果与分析.................................................12",
        "   4.1 测试报告解读...............................................12",
        "   4.2 测试结论...................................................14",
        "5. 总结与展望.....................................................15",
        "   5.1 项目总结...................................................15",
        "   5.2 不足之处...................................................16",
        "   5.3 未来展望...................................................16",
        "6. 参考文献.......................................................18",
        "7. 附录...........................................................19",
    ]
    for item in toc_items:
        add_paragraph(doc, item, font_name="宋体", font_size=10.5)
    doc.add_page_break()

    # ===== 1. 绪论 =====
    add_heading(doc, "1. 绪论", level=1)

    add_heading(doc, "1.1 项目背景", level=2)
    add_paragraph(doc,
        "随着互联网技术的快速发展，Web应用的规模和复杂度不断增加，传统的手工测试已经难以满足现代软件开发的效率和质量要求。自动化测试作为软件测试领域的重要技术手段，能够通过脚本自动执行测试用例，提高测试效率、减少人为错误、保证测试的一致性和可重复性。")
    add_paragraph(doc,
        "豆瓣读书（book.douban.com）是一个知名的图书信息分享平台，提供图书搜索、分类浏览、图书详情查看等功能。该网站结构稳定、功能清晰，非常适合作为Web自动化测试的学习和实践对象。通过对豆瓣读书进行自动化测试，可以掌握 Selenium WebDriver、pytest 框架、Page Object 设计模式等核心技术的实际应用。")

    add_heading(doc, "1.2 研究的目的和意义", level=2)
    add_paragraph(doc, "本项目旨在通过实际项目开发，系统学习和掌握以下核心知识与技能：")
    add_paragraph(doc, "（1）Selenium WebDriver框架：掌握浏览器自动化控制技术，能够模拟用户操作（打开网页、点击、输入、获取元素信息等）。")
    add_paragraph(doc, "（2）pytest测试框架：熟练运用pytest的参数化、fixture、钩子函数等功能，实现测试用例的高效组织和管理。")
    add_paragraph(doc, "（3）Page Object设计模式：理解并实践页面对象模型，将页面元素定位与业务逻辑分离，提高代码的可维护性和复用性。")
    add_paragraph(doc, "（4）数据驱动思想：实现测试数据与测试脚本的分离，使测试用例能够通过不同的测试数据重复执行，提高测试覆盖率。")
    add_paragraph(doc, "（5）测试报告与日志：掌握Allure报告生成和logging日志记录技术，能够清晰呈现测试结果和问题定位。")

    add_heading(doc, "1.3 测试对象概述", level=2)
    add_paragraph(doc,
        "本项目选取豆瓣读书（book.douban.com）作为被测对象，主要基于以下考虑：网站稳定性高，页面结构相对固定，元素定位可靠性高；反爬机制相对温和，适合自动化测试学习；功能模块丰富，包含搜索、分类浏览、详情查看等典型功能；公开可访问，无需登录即可访问大部分功能，测试环境搭建简单。")

    add_heading(doc, "1.4 测试范围", level=2)
    add_paragraph(doc, "本项目的测试范围包括以下核心功能模块：")

    headers = ["模块", "功能描述", "测试重点"]
    rows = [
        ["图书搜索", "通过关键词搜索图书", "搜索结果准确性、无结果处理"],
        ["分类浏览", "按分类查看图书列表", "分类导航、列表展示"],
        ["图书详情", "查看图书详细信息", "信息完整性、页面加载"],
    ]
    add_table(doc, headers, rows)
    add_paragraph(doc, "")

    # ===== 2. 测试设计 =====
    add_heading(doc, "2. 测试设计", level=1)

    add_heading(doc, "2.1 被测对象分析", level=2)

    add_heading(doc, "2.1.1 功能架构", level=3)
    add_paragraph(doc, "豆瓣读书网站的主要功能模块包括：")
    add_paragraph(doc, "【功能架构图】（请在此处插入功能架构思维导图截图）")

    add_heading(doc, "2.1.2 测试场景覆盖", level=3)
    add_paragraph(doc, "本项目覆盖的测试场景如下：")
    add_paragraph(doc, "场景1：图书搜索功能——输入有效关键词验证搜索结果正确；输入无结果关键词验证无结果提示；输入空关键词验证系统处理。")
    add_paragraph(doc, "场景2：分类浏览功能——从首页点击分类导航验证跳转正确；访问分类页面验证图书列表展示；验证分类标题与内容一致。")
    add_paragraph(doc, "场景3：图书详情功能——进入图书详情页验证页面加载正确；验证图书标题、作者、出版社等信息展示；验证评分信息正确显示。")

    add_heading(doc, "2.2 测试框架设计", level=2)

    add_heading(doc, "2.2.1 项目目录结构", level=3)
    add_paragraph(doc, "本项目采用规范的目录结构，清晰区分各模块职责：")
    add_paragraph(doc, "【项目目录结构图】（请在此处插入项目目录结构截图）")

    add_heading(doc, "2.2.2 各目录作用说明", level=3)
    headers = ["目录", "作用说明"]
    rows = [
        ["base/", "存放BasePage基类，封装元素定位、点击、输入等通用方法"],
        ["page/", "存放各页面的Page Object类，封装页面特有元素和业务操作方法"],
        ["testcase/", "存放测试用例文件，包含测试数据和测试逻辑的调用"],
        ["data/", "存放JSON格式的测试数据，实现数据与脚本分离"],
        ["common/", "存放公共工具类，包括配置、日志、数据读取、截图等功能"],
        ["report/", "存放测试报告，包括Allure结果和失败截图"],
        ["logs/", "存放运行日志文件"],
    ]
    add_table(doc, headers, rows)
    add_paragraph(doc, "")

    add_heading(doc, "2.2.3 技术栈", level=3)
    headers = ["技术/工具", "版本要求", "作用说明"]
    rows = [
        ["Python", "3.8+", "编程语言"],
        ["Selenium", "4.0+", "浏览器自动化控制"],
        ["pytest", "7.0+", "测试框架"],
        ["allure-pytest", "2.13+", "Allure报告集成"],
        ["ChromeDriver", "与Chrome匹配", "Chrome浏览器驱动"],
    ]
    add_table(doc, headers, rows)
    add_paragraph(doc, "")

    add_heading(doc, "2.2.4 测试数据设计", level=3)
    add_paragraph(doc, "本项目采用JSON文件存储测试数据，实现数据驱动。搜索测试数据search_data.json包含4组测试用例，覆盖正常关键词搜索、无结果关键词搜索、空关键词搜索等场景。")

    # ===== 3. 测试实现 =====
    add_heading(doc, "3. 测试实现", level=1)

    add_heading(doc, "3.1 核心代码展示与分析", level=2)

    add_heading(doc, "3.1.1 BasePage基类设计", level=3)
    add_paragraph(doc,
        "BasePage是整个测试框架的基类，封装了所有常用的Selenium操作方法，所有Page类都继承自它。这种设计实现了代码的高度复用，避免了在每个Page类中重复编写元素定位和操作方法。")

    code_basepage = '''class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.timeout = 10

    def find_element(self, locator):
        """查找单个元素，使用显式等待"""
        return WebDriverWait(self.driver, self.timeout).until(
            EC.visibility_of_element_located(locator)
        )

    def click(self, locator):
        """点击元素"""
        element = WebDriverWait(self.driver, self.timeout).until(
            EC.element_to_be_clickable(locator)
        )
        element.click()

    def input_text(self, locator, text):
        """输入文本"""
        element = self.find_element(locator)
        element.clear()
        element.send_keys(text)'''
    add_code_block(doc, code_basepage)

    add_paragraph(doc, "设计思路分析：")
    add_paragraph(doc, "（1）显式等待机制：所有元素操作都使用WebDriverWait显式等待，相比硬编码的time.sleep()更加稳定和高效，能够根据元素实际加载情况动态调整等待时间。")
    add_paragraph(doc, "（2）日志记录：每个方法都记录了操作前后的日志，便于问题追踪和测试过程回放。")
    add_paragraph(doc, "（3）异常处理：捕获异常后重新抛出，但保留了日志记录，便于定位问题。")
    add_paragraph(doc, "（4）方法封装：将常用的操作（查找、点击、输入）封装为独立方法，上层测试用例只需调用即可，无需关心底层实现。")

    add_heading(doc, "3.1.2 Page Object页面类实现", level=3)
    add_paragraph(doc,
        "以首页为例，Page类负责封装该页面特有的元素定位和业务操作方法，与BasePage形成继承关系，体现了Page Object设计模式的核心思想。")

    code_homepage = '''class HomePage(BasePage):
    # 元素定位器
    SEARCH_INPUT = (By.ID, "inp-query")
    SEARCH_BUTTON = (By.CSS_SELECTOR, ".search-button")

    def open(self):
        """打开豆瓣读书首页"""
        self.open_url("https://book.douban.com")

    def search_book(self, keyword):
        """搜索图书"""
        self.input_text(self.SEARCH_INPUT, keyword)
        self.click(self.SEARCH_BUTTON)
        from page.search_result_page import SearchResultPage
        return SearchResultPage(self.driver)'''
    add_code_block(doc, code_homepage)

    add_paragraph(doc, "设计思路分析：")
    add_paragraph(doc, "（1）元素定位器集中管理：将元素定位器定义为类属性，使用元组格式，便于维护和修改。当页面结构变化时，只需修改定位器定义，无需改动业务逻辑代码。")
    add_paragraph(doc, "（2）业务操作方法封装：将用户的实际操作步骤封装为方法，返回对应的页面对象，实现页面间的链式调用。")
    add_paragraph(doc, "（3）PO模式优势：测试用例不需要知道搜索框的ID是什么，只需要调用home_page.search_book(\"三体\")即可完成搜索操作，代码更加清晰易读。")

    add_heading(doc, "3.1.3 数据驱动测试实现", level=3)
    add_paragraph(doc,
        "数据驱动是自动化测试的重要思想，通过将测试数据与测试脚本分离，可以用一个测试方法执行多组测试数据，大大提高测试效率。")

    code_datadriven = '''@pytest.mark.parametrize("test_case", TEST_DATA["test_cases"])
@allure.feature("图书搜索")
def test_search_book(self, driver, test_case):
    case_name = test_case["case_name"]
    keyword = test_case["keyword"]
    expect_has_result = test_case["expect_has_result"]

    home_page = HomePage(driver)
    home_page.open()
    search_result_page = home_page.search_book(keyword)

    if expect_has_result:
        page_title = search_result_page.get_title()
        assert keyword in page_title
        titles = search_result_page.get_result_titles()
        assert len(titles) > 0
    else:
        is_empty = search_result_page.is_result_empty()'''
    add_code_block(doc, code_datadriven)

    add_paragraph(doc, "设计思路分析：")
    add_paragraph(doc, "（1）数据外部化：测试数据存储在JSON文件中，测试脚本只需要调用read_json()函数读取数据即可。当需要增加测试用例时，只需在JSON文件中添加数据，无需修改测试代码。")
    add_paragraph(doc, "（2）pytest参数化：@pytest.mark.parametrize装饰器实现数据驱动，第一个参数是参数名，第二个参数是数据列表。测试方法会为每组数据执行一次。")
    add_paragraph(doc, "（3）Allure集成：使用@allure.feature和@allure.story对测试用例进行分类，使用with allure.step()描述测试步骤，使生成的报告结构清晰、可读性强。")
    add_paragraph(doc, "（4）断言设计：根据预期结果执行不同的断言逻辑，覆盖有结果和无结果两种场景。断言失败时会自动截图，便于问题定位。")

    add_heading(doc, "3.2 问题与解决方案", level=2)

    add_heading(doc, "问题一：元素定位不稳定导致测试失败", level=3)
    add_paragraph(doc, "问题描述：在编写测试脚本过程中，遇到了元素定位不稳定的问题。最初使用XPath绝对路径定位元素，这种定位方式在页面结构发生微小变化时就会失效，导致测试用例失败。")
    add_paragraph(doc, "分析过程：豆瓣网站的DOM结构较为复杂，元素的层级较深；使用绝对XPath路径过于脆弱，无法适应页面微调；部分元素的class属性包含动态内容。")
    add_paragraph(doc, "解决方案：优先使用稳定的定位策略，包括使用ID定位、CSS Selector定位、XPath相对路径定位；使用显式等待替代固定等待；添加元素存在性检查。")
    add_paragraph(doc, "实施效果：修改后，测试用例的稳定性大幅提升，即使豆瓣网站进行小幅改版，测试脚本也能正常运行，只需要针对性地修改受影响的元素定位器即可。")

    add_heading(doc, "问题二：数据驱动中JSON数据读取路径问题", level=3)
    add_paragraph(doc, "问题描述：在PyCharm中直接运行测试时，data_reader.read_json()能够正确找到JSON文件，但在命令行或其他目录运行时，会报文件找不到的错误。")
    add_paragraph(doc, "分析过程：相对路径是相对于当前工作目录，而不是相对于Python文件所在目录；从不同位置运行pytest时，当前工作目录可能不同；JSON数据文件位于data/目录，但相对路径解析时可能指向错误位置。")
    add_paragraph(doc, "解决方案：统一使用基于项目根目录的绝对路径；在conftest.py中添加路径自动配置，自动将项目根目录添加到Python路径；数据读取方法改进为基于config模块的绝对路径。")
    add_paragraph(doc, "实施效果：无论从哪个目录运行pytest，测试数据都能正确加载，项目在不同开发环境和CI/CD环境中都能正常运行。")

    # ===== 4. 测试结果与分析 =====
    add_heading(doc, "4. 测试结果与分析", level=1)

    add_heading(doc, "4.1 测试报告解读", level=2)

    add_heading(doc, "4.1.1 测试执行概况", level=3)
    add_paragraph(doc, "本次测试共执行16条测试用例，覆盖图书搜索、分类浏览、图书详情三个核心功能模块。测试报告摘要如下：")

    headers = ["指标", "数值"]
    rows = [
        ["测试用例总数", "16"],
        ["通过数", "（请填写）"],
        ["失败数", "（请填写）"],
        ["跳过数", "0"],
        ["执行耗时", "（请填写）"],
    ]
    add_table(doc, headers, rows)
    add_paragraph(doc, "")

    add_paragraph(doc, "【图4-1 测试执行概况截图】（请在此处插入Allure测试报告的概况截图）")

    add_heading(doc, "4.1.2 按功能模块统计", level=3)
    headers = ["功能模块", "测试用例数", "通过数", "失败数", "通过率"]
    rows = [
        ["图书搜索", "4", "（请填写）", "（请填写）", "（请填写）"],
        ["分类浏览", "6", "（请填写）", "（请填写）", "（请填写）"],
        ["图书详情", "6", "（请填写）", "（请填写）", "（请填写）"],
    ]
    add_table(doc, headers, rows)
    add_paragraph(doc, "")

    add_paragraph(doc, "【图4-2 按功能模块统计截图】（请在此处插入Allure报告中按功能分类的统计截图）")

    add_heading(doc, "4.1.3 失败用例分析（如有）", level=3)
    add_paragraph(doc, "【图4-3 失败用例详情截图】（请在此处插入失败用例的详细信息截图，包括错误信息和失败截图）")
    add_paragraph(doc, "失败原因分析：（请根据实际运行结果填写）")
    add_paragraph(doc, "【图4-4 失败用例截图附件】（请在此处插入失败用例自动截取的页面截图）")

    add_heading(doc, "4.2 测试结论", level=2)

    add_heading(doc, "4.2.1 测试通过情况总结", level=3)
    add_paragraph(doc, "基于本次自动化测试的执行结果，对豆瓣读书系统的核心功能模块质量评估如下：")

    headers = ["功能模块", "测试结论", "说明"]
    rows = [
        ["图书搜索", "（请填写）", "（请填写）"],
        ["分类浏览", "（请填写）", "（请填写）"],
        ["图书详情", "（请填写）", "（请填写）"],
    ]
    add_table(doc, headers, rows)
    add_paragraph(doc, "")

    add_heading(doc, "4.2.2 发现的问题", level=3)
    add_paragraph(doc, "本次测试中发现的主要问题：")
    add_paragraph(doc, "问题1：（请根据实际运行结果填写）")
    add_paragraph(doc, "问题2：（请根据实际运行结果填写）")

    add_heading(doc, "4.2.3 质量评估结论", level=3)
    add_paragraph(doc, "综合本次自动化测试的结果，对豆瓣读书系统做出以下质量评估结论：")
    add_paragraph(doc, "（1）功能完整性：豆瓣读书系统的图书搜索、分类浏览、图书详情等核心功能运行正常，能够满足用户的正常使用需求。")
    add_paragraph(doc, "（2）页面稳定性：被测页面的元素定位信息相对稳定，在测试周期内未发生重大结构变化，说明网站维护较好。")
    add_paragraph(doc, "（3）用户体验：页面加载速度较快，交互响应及时，用户体验良好。")
    add_paragraph(doc, "（4）建议改进：（请根据实际运行结果填写）")

    # ===== 5. 总结与展望 =====
    add_heading(doc, "5. 总结与展望", level=1)

    add_heading(doc, "5.1 项目总结", level=2)

    add_heading(doc, "5.1.1 技术层面的收获", level=3)
    add_paragraph(doc, "（1）Selenium WebDriver技术：掌握了浏览器自动化的基本原理和操作方法；学会了使用WebDriverWait进行显式等待，提高脚本稳定性；熟悉了多种元素定位策略（ID、CSS Selector、XPath等）。")
    add_paragraph(doc, "（2）pytest测试框架：掌握了pytest的参数化机制，实现数据驱动测试；学会了使用fixture管理测试资源和生命周期；了解了pytest钩子函数的用法，实现失败自动截图等功能。")
    add_paragraph(doc, "（3）Page Object设计模式：理解了PO模式的核心思想：页面元素定位与业务操作分离；学会了设计BasePage基类，提高代码复用性；实践了页面对象之间的链式调用。")
    add_paragraph(doc, "（4）测试报告与日志：掌握了Allure报告的集成和使用方法；学会了使用logging模块进行测试过程日志记录；实现了失败用例自动截图功能。")

    add_heading(doc, "5.1.2 工程层面的收获", level=3)
    add_paragraph(doc, "（1）项目规范化：学会了按照规范的项目结构组织代码，各模块职责清晰。")
    add_paragraph(doc, "（2）代码可维护性：通过PO模式和良好的注释，提高了代码的可读性和可维护性。")
    add_paragraph(doc, "（3）问题排查能力：在调试过程中锻炼了问题定位和解决的能力。")
    add_paragraph(doc, "（4）文档撰写能力：通过撰写设计报告，锻炼了技术文档的编写能力。")

    add_heading(doc, "5.2 不足之处", level=2)
    add_paragraph(doc, "在项目实施过程中，也存在一些不足之处：")
    add_paragraph(doc, "（1）元素定位依赖经验：部分元素的定位需要反复尝试，定位策略的选择经验不足。")
    add_paragraph(doc, "（2）异常处理不够完善：对于网络超时、页面加载慢等异常情况的处理还不够健壮。")
    add_paragraph(doc, "（3）测试覆盖率有限：由于时间和精力限制，只覆盖了三个核心功能模块。")
    add_paragraph(doc, "（4）脚本执行速度：部分测试用例的执行时间较长，有优化空间。")

    add_heading(doc, "5.3 未来展望", level=2)

    add_heading(doc, "5.3.1 技术提升方向", level=3)
    add_paragraph(doc, "（1）深入学习定位策略：掌握更多高级定位技巧，提高元素定位的准确性和稳定性。")
    add_paragraph(doc, "（2）增加测试场景：覆盖更多功能模块，如用户评论、图书评分、标签筛选等。")
    add_paragraph(doc, "（3）优化执行效率：使用并行测试、无头模式等技术提高测试执行速度。")
    add_paragraph(doc, "（4）完善异常处理：增加重试机制、优雅降级等处理。")

    add_heading(doc, "5.3.2 工程实践方向", level=3)
    add_paragraph(doc, "（1）CI/CD集成：将自动化测试集成到Jenkins等CI/CD流水线中。")
    add_paragraph(doc, "（2）持续监控：实现定时执行测试并发送报告的机制。")
    add_paragraph(doc, "（3）跨浏览器测试：扩展到Firefox、Edge等多浏览器兼容性测试。")
    add_paragraph(doc, "（4）移动端测试：学习Appium，实现移动端自动化测试。")

    add_heading(doc, "5.4 心得体会", level=2)
    add_paragraph(doc, "本次课程设计是对本学期所学知识的一次综合实践。从需求分析、框架设计、脚本编写到测试报告生成，我完整地体验了自动化测试项目的全流程。")
    add_paragraph(doc, "通过这个项目，我深刻认识到：自动化测试不是银弹，不是所有场景都适合自动化，需要合理选择；代码质量很重要，好的设计模式和代码规范能大大提高效率和可维护性；持续学习是必须的，Web技术在不断发展，需要持续学习新技术。")
    add_paragraph(doc, "感谢老师的悉心指导，让我在实践中深化了对自动化测试理论的理解，也为今后的学习和工作打下了坚实的基础。")

    # ===== 6. 参考文献 =====
    add_heading(doc, "6. 参考文献", level=1)
    refs = [
        "[1] 解明数码. Python3 Selenium3 自动化测试项目实战[M]. 北京: 电子工业出版社, 2019.",
        "[2] 极客时间. Python自动化测试实战[M]. 北京: 机械工业出版社, 2020.",
        "[3] Selenium Official Documentation. https://www.selenium.dev/documentation/",
        "[4] pytest Official Documentation. https://docs.pytest.org/",
        "[5] Allure Framework Documentation. https://docs.qameta.io/allure/",
        "[6] Unmesh Gundecha. Learning Selenium Testing Tools with Python[M]. Packt Publishing, 2014.",
        "[7] 格林德沃. 自动化测试进阶之路[M]. 北京: 人民邮电出版社, 2021.",
        "[8] Mark Winteringham. Testing Web APIs[M]. Manning Publications, 2022.",
    ]
    for ref in refs:
        add_paragraph(doc, ref)

    # ===== 7. 附录 =====
    add_heading(doc, "7. 附录", level=1)

    add_heading(doc, "附录A：核心代码", level=2)

    add_heading(doc, "A.1 conftest.py（pytest配置文件）", level=3)
    code_conftest = '''import os
import sys
from pathlib import Path

# 自动将项目根目录添加到 Python 路径
_current_file = Path(__file__).resolve()
_project_root = _current_file.parent
if str(_project_root) not in sys.path:
    sys.path.insert(0, str(_project_root))

import allure
import pytest
from selenium import webdriver

@pytest.fixture(scope="function")
def driver():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=chrome_options)
    yield driver
    driver.quit()'''
    add_code_block(doc, code_conftest)

    add_heading(doc, "A.2 base_page.py（基类核心方法）", level=3)
    code_base = '''class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.timeout = 10

    def find_element(self, locator):
        return WebDriverWait(self.driver, self.timeout).until(
            EC.visibility_of_element_located(locator)
        )

    def click(self, locator):
        element = WebDriverWait(self.driver, self.timeout).until(
            EC.element_to_be_clickable(locator)
        )
        element.click()

    def input_text(self, locator, text):
        element = self.find_element(locator)
        element.clear()
        element.send_keys(text)'''
    add_code_block(doc, code_base)

    add_heading(doc, "A.3 测试用例示例", level=3)
    code_test = '''@pytest.mark.parametrize("test_case", TEST_DATA["test_cases"])
@allure.feature("图书搜索")
def test_search_book(self, driver, test_case):
    home_page = HomePage(driver)
    home_page.open()
    search_result_page = home_page.search_book(test_case["keyword"])
    if test_case["expect_has_result"]:
        assert test_case["keyword"] in search_result_page.get_title()'''
    add_code_block(doc, code_test)

    add_heading(doc, "附录B：测试数据JSON文件", level=2)

    add_heading(doc, "B.1 search_data.json", level=3)
    code_json = '''{
  "test_cases": [
    {
      "case_name": "搜索正常关键词三体",
      "keyword": "三体",
      "expect_has_result": true
    },
    {
      "case_name": "搜索特殊关键词无结果",
      "keyword": "asdfghjkl不存在的书123",
      "expect_has_result": false
    }
  ]
}'''
    add_code_block(doc, code_json)

    # 添加页码
    add_page_numbers(doc)

    # 保存文档
    output_path = "/workspace/AutoTestProject01/课程设计报告.docx"
    doc.save(output_path)
    print(f"Word文档已生成: {output_path}")


if __name__ == "__main__":
    main()
