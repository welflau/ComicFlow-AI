import pytest
from pathlib import Path
import re

class TestSmartCanvasProject:
    
    def test_html_file_exists(self):
        """测试HTML文件是否存在"""
        html_file = Path("index.html")
        assert html_file.exists(), "index.html文件不存在"
        assert html_file.is_file(), "index.html不是一个有效的文件"
    
    def test_html_contains_canvas_elements(self):
        """测试HTML文件是否包含画布相关的关键元素"""
        html_file = Path("index.html")
        if html_file.exists():
            content = html_file.read_text(encoding='utf-8')
            
            # 检查是否包含canvas标签或相关画布元素
            canvas_patterns = [
                r'<canvas',
                r'canvas',
                r'node',
                r'connection',
                r'link'
            ]
            
            found_canvas_elements = any(re.search(pattern, content, re.IGNORECASE) 
                                     for pattern in canvas_patterns)
            assert found_canvas_elements, "HTML文件中未找到画布相关元素"
        else:
            pytest.skip("HTML文件不存在，跳过内容测试")
    
    def test_dev_notes_file_exists_and_contains_bug_info(self):
        """测试开发文档是否存在并包含BUG相关信息"""
        dev_notes_file = Path("docs/78b245/98c5a7/dev-notes.md")
        assert dev_notes_file.exists(), "开发文档文件不存在"
        assert dev_notes_file.is_file(), "开发文档不是一个有效的文件"
        
        content = dev_notes_file.read_text(encoding='utf-8')
        
        # 检查是否包含BUG相关关键词
        bug_keywords = ['bug', 'BUG', '问题', '连线', '断开', '节点']
        found_bug_info = any(keyword in content for keyword in bug_keywords)
        assert found_bug_info, "开发文档中未找到BUG相关信息"
    
    def test_html_structure_validity(self):
        """测试HTML文件结构的基本有效性"""
        html_file = Path("index.html")
        if html_file.exists():
            content = html_file.read_text(encoding='utf-8')
            
            # 检查基本HTML结构
            assert '<html' in content.lower() or '<!doctype html' in content.lower(), "缺少HTML声明"
            assert '<head' in content.lower(), "缺少head标签"
            assert '<body' in content.lower(), "缺少body标签"
            
            # 检查标签是否配对（简单检查）
            open_tags = len(re.findall(r'<(?!/)(?!!)(?!\?)[^>]*>', content))
            close_tags = len(re.findall(r'</[^>]*>', content))
            self_closing_tags = len(re.findall(r'<[^>]*/>', content))
            
            # 允许一定的标签不匹配（考虑自闭合标签）
            tag_difference = abs(open_tags - close_tags - self_closing_tags)
            assert tag_difference <= 5, f"HTML标签配对可能存在问题，差异: {tag_difference}"
        else:
            pytest.skip("HTML文件不存在，跳过结构测试")
    
    def test_project_directory_structure(self):
        """测试项目目录结构是否合理"""
        # 检查根目录文件
        root_files = ['index.html']
        for file_name in root_files:
            file_path = Path(file_name)
            if file_path.exists():
                assert file_path.is_file(), f"{file_name} 应该是一个文件"
        
        # 检查docs目录结构
        docs_dir = Path("docs")
        if docs_dir.exists():
            assert docs_dir.is_dir(), "docs应该是一个目录"
            
            # 检查嵌套目录
            nested_dir = Path("docs/78b245/98c5a7")
            if nested_dir.exists():
                assert nested_dir.is_dir(), "嵌套目录结构应该正确"