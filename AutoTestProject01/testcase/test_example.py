"""
简单测试示例 - 用于快速生成 HTML 报告演示
"""
import pytest


def test_example_pass_1():
    """示例通过测试 1"""
    assert 1 + 1 == 2


def test_example_pass_2():
    """示例通过测试 2"""
    assert "hello".upper() == "HELLO"


def test_example_pass_3():
    """示例通过测试 3"""
    assert len([1, 2, 3]) == 3


def test_example_pass_4():
    """示例通过测试 4"""
    assert True is True