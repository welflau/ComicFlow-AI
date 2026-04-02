"""测试: 基础组件库开发"""
import os
from pathlib import Path

REPO_DIR = Path(__file__).parent.parent

def test_index_html_exists():
    """测试入口文件存在"""
    assert (REPO_DIR / "index.html").exists(), "index.html 不存在"

def test_index_html_has_content():
    """测试入口文件有内容"""
    content = (REPO_DIR / "index.html").read_text(encoding="utf-8")
    assert len(content) > 100, "index.html 内容过少"
    assert "<html" in content.lower(), "缺少 HTML 标签"

def test_index_html_has_title():
    """测试页面有标题"""
    content = (REPO_DIR / "index.html").read_text(encoding="utf-8")
    assert "<title>" in content.lower(), "缺少 title 标签"

def test_has_css_styles():
    """测试页面包含样式"""
    content = (REPO_DIR / "index.html").read_text(encoding="utf-8")
    assert "<style" in content.lower() or "stylesheet" in content.lower(), "无 CSS 样式"
