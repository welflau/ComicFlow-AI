import pytest
from pathlib import Path
import re

class TestSmartCanvasNodeCreation:
    
    def test_html_file_exists(self):
        """测试智能画布的HTML文件是否存在"""
        html_file = Path("index.html")
        assert html_file.exists(), "index.html文件不存在"
        assert html_file.is_file(), "index.html不是一个有效的文件"
    
    def test_html_contains_canvas_elements(self):
        """测试HTML文件是否包含画布相关的关键元素"""
        html_file = Path("index.html")
        assert html_file.exists(), "HTML文件不存在"
        
        content = html_file.read_text(encoding='utf-8')
        
        # 检查是否包含canvas相关元素
        canvas_patterns = [
            r'<canvas',
            r'canvas',
            r'node',
            r'create',
            r'智能画布|canvas|节点|node'
        ]
        
        found_elements = []
        for pattern in canvas_patterns:
            if re.search(pattern, content, re.IGNORECASE):
                found_elements.append(pattern)
        
        assert len(found_elements) > 0, f"HTML文件中未找到画布相关元素，检查的模式: {canvas_patterns}"
    
    def test_html_has_javascript_functionality(self):
        """测试HTML文件是否包含JavaScript功能代码"""
        html_file = Path("index.html")
        assert html_file.exists(), "HTML文件不存在"
        
        content = html_file.read_text(encoding='utf-8')
        
        # 检查JavaScript相关功能
        js_patterns = [
            r'<script',
            r'function',
            r'addEventListener',
            r'createElement',
            r'onclick|onload|event'
        ]
        
        js_found = []
        for pattern in js_patterns:
            if re.search(pattern, content, re.IGNORECASE):
                js_found.append(pattern)
        
        assert len(js_found) > 0, f"HTML文件中未找到JavaScript功能代码，检查的模式: {js_patterns}"
    
    def test_dev_notes_file_exists(self):
        """测试开发文档文件是否存在"""
        docs_file = Path("docs/78b245/8f9441/dev-notes.md")
        assert docs_file.exists(), "开发文档文件不存在"
        assert docs_file.is_file(), "dev-notes.md不是一个有效的文件"
    
    def test_dev_notes_contains_bug_info(self):
        """测试开发文档是否包含BUG相关信息"""
        docs_file = Path("docs/78b245/8f9441/dev-notes.md")
        assert docs_file.exists(), "开发文档文件不存在"
        
        content = docs_file.read_text(encoding='utf-8')
        
        # 检查是否包含BUG相关信息
        bug_patterns = [
            r'BUG|bug|错误|失效|问题',
            r'节点创建|node.*create|创建.*节点',
            r'智能画布|canvas',
            r'修复|fix|解决|solution'
        ]
        
        bug_info_found = []
        for pattern in bug_patterns:
            if re.search(pattern, content, re.IGNORECASE):
                bug_info_found.append(pattern)
        
        assert len(bug_info_found) >= 2, f"开发文档中BUG相关信息不足，找到的模式: {bug_info_found}"
    
    def test_project_structure_integrity(self):
        """测试项目结构完整性"""
        # 检查主要文件是否存在
        required_files = [
            Path("index.html"),
            Path("docs/78b245/8f9441/dev-notes.md")
        ]
        
        missing_files = []
        for file_path in required_files:
            if not file_path.exists():
                missing_files.append(str(file_path))
        
        assert len(missing_files) == 0, f"缺少必要文件: {missing_files}"
        
        # 检查docs目录结构
        docs_dir = Path("docs/78b245/8f9441")
        assert docs_dir.exists(), "文档目录结构不完整"
        assert docs_dir.is_dir(), "docs路径不是目录"