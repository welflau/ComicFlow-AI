import pytest
from pathlib import Path
import re

class TestSmartCanvasProject:
    """智能画布节点连线功能测试类"""
    
    def test_index_html_file_exists(self):
        """测试主页HTML文件是否存在"""
        index_file = Path("index.html")
        assert index_file.exists(), "index.html文件不存在"
        assert index_file.is_file(), "index.html不是一个有效的文件"
    
    def test_index_html_contains_canvas_elements(self):
        """测试HTML文件是否包含画布相关的关键元素"""
        index_file = Path("index.html")
        assert index_file.exists(), "index.html文件不存在"
        
        content = index_file.read_text(encoding='utf-8')
        
        # 检查是否包含canvas元素或相关容器
        canvas_patterns = [
            r'<canvas[^>]*>',
            r'id=["\'].*canvas.*["\']',
            r'class=["\'].*canvas.*["\']',
            r'<div[^>]*canvas[^>]*>',
            r'<svg[^>]*>'
        ]
        
        has_canvas_element = any(re.search(pattern, content, re.IGNORECASE) for pattern in canvas_patterns)
        assert has_canvas_element, "HTML文件中未找到画布相关元素(canvas/svg/canvas容器)"
    
    def test_index_html_contains_node_connection_features(self):
        """测试HTML文件是否包含节点连线相关的功能代码"""
        index_file = Path("index.html")
        assert index_file.exists(), "index.html文件不存在"
        
        content = index_file.read_text(encoding='utf-8')
        
        # 检查节点连线相关的关键词
        connection_keywords = [
            'node', 'connect', 'link', 'line', 'edge',
            'drag', 'drop', 'mouse', 'click', 'draw'
        ]
        
        found_keywords = []
        for keyword in connection_keywords:
            if re.search(keyword, content, re.IGNORECASE):
                found_keywords.append(keyword)
        
        assert len(found_keywords) >= 2, f"HTML文件中节点连线相关功能关键词不足，仅找到: {found_keywords}"
    
    def test_dev_notes_file_exists_and_readable(self):
        """测试开发文档文件是否存在且可读"""
        dev_notes_file = Path("docs/78b245/8151ec/dev-notes.md")
        assert dev_notes_file.exists(), "开发文档文件不存在"
        assert dev_notes_file.is_file(), "开发文档不是一个有效的文件"
        
        # 测试文件是否可读
        content = dev_notes_file.read_text(encoding='utf-8')
        assert len(content.strip()) > 0, "开发文档文件为空"
    
    def test_dev_notes_contains_bug_information(self):
        """测试开发文档是否包含BUG相关信息"""
        dev_notes_file = Path("docs/78b245/8151ec/dev-notes.md")
        assert dev_notes_file.exists(), "开发文档文件不存在"
        
        content = dev_notes_file.read_text(encoding='utf-8')
        
        # 检查BUG相关关键词
        bug_keywords = [
            'bug', 'issue', '问题', '错误', 'error',
            '断开', 'disconnect', '连线', 'connection',
            '节点', 'node', '修复', 'fix'
        ]
        
        found_keywords = []
        for keyword in bug_keywords:
            if re.search(keyword, content, re.IGNORECASE):
                found_keywords.append(keyword)
        
        assert len(found_keywords) >= 3, f"开发文档中BUG相关信息不足，仅找到关键词: {found_keywords}"
    
    def test_project_structure_integrity(self):
        """测试项目结构完整性"""
        # 检查主要文件是否都存在
        required_files = [
            Path("index.html"),
            Path("docs/78b245/8151ec/dev-notes.md")
        ]
        
        missing_files = []
        for file_path in required_files:
            if not file_path.exists():
                missing_files.append(str(file_path))
        
        assert len(missing_files) == 0, f"项目缺少必要文件: {missing_files}"
        
        # 检查docs目录结构
        docs_dir = Path("docs/78b245/8151ec")
        assert docs_dir.exists(), "文档目录结构不完整"
        assert docs_dir.is_dir(), "docs路径不是目录"