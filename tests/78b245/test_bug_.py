import pytest
from pathlib import Path
import re


class TestSmartCanvasProject:
    """智能画布节点连线断开问题测试类"""
    
    def test_index_html_file_exists(self):
        """测试index.html文件是否存在"""
        index_file = Path("index.html")
        assert index_file.exists(), "index.html文件不存在"
        assert index_file.is_file(), "index.html不是一个有效的文件"
    
    def test_index_html_contains_canvas_elements(self):
        """测试index.html文件是否包含画布相关的关键元素"""
        index_file = Path("index.html")
        assert index_file.exists(), "index.html文件不存在"
        
        content = index_file.read_text(encoding='utf-8')
        
        # 检查是否包含canvas标签或相关画布元素
        canvas_patterns = [
            r'<canvas[^>]*>',
            r'canvas',
            r'node',
            r'connection',
            r'link'
        ]
        
        has_canvas_element = any(re.search(pattern, content, re.IGNORECASE) for pattern in canvas_patterns)
        assert has_canvas_element, "index.html文件中未找到画布相关元素"
        
        # 检查是否包含基本的HTML结构
        assert '<html' in content.lower() or '<!doctype html' in content.lower(), "缺少HTML文档声明"
    
    def test_dev_notes_file_exists_and_contains_bug_info(self):
        """测试开发文档是否存在并包含BUG相关信息"""
        dev_notes_file = Path("docs/78b245/8151ec/dev-notes.md")
        assert dev_notes_file.exists(), "开发文档文件不存在"
        assert dev_notes_file.is_file(), "开发文档不是一个有效的文件"
        
        content = dev_notes_file.read_text(encoding='utf-8')
        
        # 检查是否包含BUG相关关键词
        bug_keywords = [
            '节点',
            '连线',
            '断开',
            'bug',
            'BUG',
            '问题',
            '修复'
        ]
        
        found_keywords = [keyword for keyword in bug_keywords if keyword in content]
        assert len(found_keywords) > 0, f"开发文档中未找到相关BUG描述关键词: {bug_keywords}"
    
    def test_project_structure_integrity(self):
        """测试项目结构完整性"""
        # 检查docs目录结构
        docs_dir = Path("docs")
        assert docs_dir.exists(), "docs目录不存在"
        assert docs_dir.is_dir(), "docs不是一个有效的目录"
        
        # 检查嵌套目录结构
        nested_dir = Path("docs/78b245/8151ec")
        assert nested_dir.exists(), "嵌套目录结构不完整"
        assert nested_dir.is_dir(), "嵌套路径不是有效目录"
    
    def test_html_file_basic_structure(self):
        """测试HTML文件基本结构完整性"""
        index_file = Path("index.html")
        content = index_file.read_text(encoding='utf-8')
        
        # 检查基本HTML标签
        essential_tags = ['<head', '<body', '</html>']
        missing_tags = [tag for tag in essential_tags if tag.lower() not in content.lower()]
        
        assert len(missing_tags) == 0, f"HTML文件缺少基本标签: {missing_tags}"
        
        # 检查是否有JavaScript相关内容（智能画布通常需要JS）
        js_indicators = ['<script', 'javascript', '.js']
        has_js = any(indicator in content.lower() for indicator in js_indicators)
        assert has_js, "HTML文件中未找到JavaScript相关内容，智能画布功能可能无法正常工作"