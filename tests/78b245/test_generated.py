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
            
            # 检查是否包含canvas标签或相关容器
            canvas_patterns = [
                r'<canvas[^>]*>',
                r'class=["\'][^"\']*canvas[^"\']*["\']',
                r'id=["\'][^"\']*canvas[^"\']*["\']',
                r'<div[^>]*canvas[^>]*>',
                r'<svg[^>]*>'
            ]
            
            has_canvas_element = any(re.search(pattern, content, re.IGNORECASE) 
                                   for pattern in canvas_patterns)
            assert has_canvas_element, "HTML文件中未找到画布相关元素"
    
    def test_html_contains_drag_functionality(self):
        """测试HTML文件是否包含拖拽功能相关代码"""
        html_file = Path("index.html")
        if html_file.exists():
            content = html_file.read_text(encoding='utf-8')
            
            # 检查拖拽相关的关键词
            drag_patterns = [
                r'draggable\s*=\s*["\']true["\']',
                r'ondrag\w*\s*=',
                r'addEventListener\s*\(\s*["\']drag',
                r'drag\w*\s*:',
                r'onmouse\w*\s*=',
                r'addEventListener\s*\(\s*["\']mouse',
                r'\.drag\w*\(',
                r'dragstart|dragend|dragover|drop'
            ]
            
            has_drag_functionality = any(re.search(pattern, content, re.IGNORECASE) 
                                       for pattern in drag_patterns)
            assert has_drag_functionality, "HTML文件中未找到拖拽功能相关代码"
    
    def test_dev_notes_file_exists(self):
        """测试开发文档文件是否存在"""
        docs_file = Path("docs/78b245/e4554c/dev-notes.md")
        assert docs_file.exists(), "开发文档文件不存在"
        assert docs_file.is_file(), "开发文档不是一个有效的文件"
    
    def test_dev_notes_contains_bug_info(self):
        """测试开发文档是否包含BUG相关信息"""
        docs_file = Path("docs/78b245/e4554c/dev-notes.md")
        if docs_file.exists():
            content = docs_file.read_text(encoding='utf-8')
            
            # 检查是否包含BUG相关描述
            bug_keywords = ['bug', 'BUG', '问题', '错误', '拖拽', '连线', '节点', 'drag', 'node', 'connect']
            has_bug_info = any(keyword in content for keyword in bug_keywords)
            assert has_bug_info, "开发文档中未找到BUG相关信息"
    
    def test_project_structure_integrity(self):
        """测试项目结构完整性"""
        # 检查项目根目录结构
        root_files = ['index.html']
        for file_name in root_files:
            file_path = Path(file_name)
            assert file_path.exists(), f"项目根目录缺少必要文件: {file_name}"
        
        # 检查docs目录结构
        docs_dir = Path("docs")
        assert docs_dir.exists(), "docs目录不存在"
        assert docs_dir.is_dir(), "docs不是一个有效的目录"
        
        # 检查具体的文档路径
        dev_notes_path = Path("docs/78b245/e4554c/dev-notes.md")
        assert dev_notes_path.exists(), "开发文档路径不完整"