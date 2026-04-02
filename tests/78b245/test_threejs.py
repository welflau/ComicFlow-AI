import pytest
from pathlib import Path
import re

class TestThreeJSCanvasInfrastructure:
    
    def test_html_file_exists(self):
        """测试 HTML 文件是否存在"""
        html_file = Path("frontend/index.html")
        assert html_file.exists(), f"HTML 文件不存在: {html_file}"
        assert html_file.is_file(), f"路径不是文件: {html_file}"
    
    def test_html_contains_threejs_elements(self):
        """测试 HTML 文件是否包含 Three.js 相关的关键元素"""
        html_file = Path("frontend/index.html")
        
        if not html_file.exists():
            pytest.skip("HTML 文件不存在，跳过内容测试")
        
        content = html_file.read_text(encoding='utf-8')
        
        # 检查基本 HTML 结构
        assert '<html' in content.lower(), "HTML 文件缺少 html 标签"
        assert '<head>' in content.lower() or '<head ' in content.lower(), "HTML 文件缺少 head 标签"
        assert '<body>' in content.lower() or '<body ' in content.lower(), "HTML 文件缺少 body 标签"
        
        # 检查 Three.js 相关元素
        threejs_indicators = [
            'three.js',
            'three.min.js',
            'canvas',
            'webgl',
            'scene',
            'camera',
            'renderer'
        ]
        
        content_lower = content.lower()
        found_indicators = [indicator for indicator in threejs_indicators if indicator in content_lower]
        
        assert len(found_indicators) > 0, f"HTML 文件中未找到 Three.js 相关元素，检查的关键词: {threejs_indicators}"
    
    def test_dev_notes_file_exists_and_contains_content(self):
        """测试开发文档文件是否存在并包含有效内容"""
        dev_notes_file = Path("docs/78b245/91c481/dev-notes.md")
        
        assert dev_notes_file.exists(), f"开发文档文件不存在: {dev_notes_file}"
        assert dev_notes_file.is_file(), f"路径不是文件: {dev_notes_file}"
        
        content = dev_notes_file.read_text(encoding='utf-8')
        
        # 检查文件不为空
        assert len(content.strip()) > 0, "开发文档文件内容为空"
        
        # 检查是否包含 Markdown 格式的内容
        markdown_indicators = [
            '#',  # 标题
            '##', # 二级标题
            '```', # 代码块
            '*', # 列表或强调
            '-', # 列表
            '[', # 链接
        ]
        
        has_markdown = any(indicator in content for indicator in markdown_indicators)
        assert has_markdown, "开发文档文件似乎不包含 Markdown 格式内容"
    
    def test_project_structure_integrity(self):
        """测试项目结构的完整性"""
        # 检查主要目录结构
        frontend_dir = Path("frontend")
        docs_dir = Path("docs")
        
        assert frontend_dir.exists(), "frontend 目录不存在"
        assert frontend_dir.is_dir(), "frontend 不是目录"
        
        assert docs_dir.exists(), "docs 目录不存在"
        assert docs_dir.is_dir(), "docs 不是目录"
        
        # 检查文档子目录结构
        specific_docs_dir = Path("docs/78b245/91c481")
        assert specific_docs_dir.exists(), f"特定文档目录不存在: {specific_docs_dir}"
        assert specific_docs_dir.is_dir(), f"路径不是目录: {specific_docs_dir}"
    
    def test_html_file_encoding_and_syntax(self):
        """测试 HTML 文件编码和基本语法正确性"""
        html_file = Path("frontend/index.html")
        
        if not html_file.exists():
            pytest.skip("HTML 文件不存在，跳过语法测试")
        
        # 测试文件可以用 UTF-8 编码读取
        try:
            content = html_file.read_text(encoding='utf-8')
        except UnicodeDecodeError:
            pytest.fail("HTML 文件无法用 UTF-8 编码读取")
        
        # 基本语法检查
        content_lower = content.lower()
        
        # 检查 DOCTYPE 声明
        has_doctype = '<!doctype' in content_lower or '<!DOCTYPE' in content
        
        # 检查基本标签配对（简单检查）
        html_open = content_lower.count('<html')
        html_close = content_lower.count('</html>')
        
        if html_open > 0:
            assert html_close > 0, "HTML 标签未正确闭合"
        
        head_open = content_lower.count('<head')
        head_close = content_lower.count('</head>')
        
        if head_open > 0:
            assert head_close > 0, "HEAD 标签未正确闭合"