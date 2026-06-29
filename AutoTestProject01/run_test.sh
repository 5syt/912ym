#!/bin/bash

echo "========================================"
echo "  豆瓣读书自动化测试 - Allure 报告"
echo "========================================"
echo ""

PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$PROJECT_DIR"

echo "[1/4] 安装项目依赖..."
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "❌ 依赖安装失败，请检查网络连接或 requirements.txt"
    exit 1
fi
echo "✅ 依赖安装完成"
echo ""

echo "[2/4] 运行 pytest 测试并生成 Allure 结果..."
python -m pytest
if [ $? -ne 0 ]; then
    echo "⚠️  测试执行完成（存在失败用例）"
else
    echo "✅ 所有测试用例执行通过"
fi
echo ""

echo "[3/4] 生成 Allure HTML 报告..."
if command -v allure &> /dev/null; then
    allure generate report/allure-results -o report/allure-report --clean
    if [ $? -ne 0 ]; then
        echo "❌ Allure 报告生成失败"
        exit 1
    fi
    echo "✅ Allure HTML 报告生成完成"
else
    echo "⚠️  未检测到 Allure 命令行工具，跳过报告生成"
    echo "   请先安装 Allure: https://allurereport.org/docs/install/"
fi
echo ""

echo "[4/4] 完成！"
echo "========================================"
echo "  测试结果目录: $PROJECT_DIR/report/allure-results"
if command -v allure &> /dev/null; then
    echo "  HTML 报告路径: $PROJECT_DIR/report/allure-report/index.html"
    echo ""
    echo "  查看报告命令:"
    echo "    allure serve report/allure-results"
    echo "  或直接在浏览器中打开:"
    echo "    report/allure-report/index.html"
fi
echo "========================================"
