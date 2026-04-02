import pytest
from pathlib import Path
import re

class TestSmartCanvasProject:
    """智能画布节点连线功能测试类"""
    
    def test_index_html_file_exists(self):
        """测试主页HTML文件是否存在"""
        index_file = Path("index.html")
        assert index_file.exists(), "index.html文件不存在"
        assert index_file.is_file(), "index.html不是有效文件"
    
    def test_index_html_contains_canvas_elements(self):
        """测试HTML文件是否包含画布相关的关键元素"""
        index_file = Path("index.html")
        assert index_file.exists(), "index.html文件不存在"
        
        content = index_file.read_text(encoding='utf-8')
        
        # 检查是否包含画布相关元素
        canvas_keywords = [
            'canvas',
            'node',
            'connection',
            'line'
        ]
        
        found_keywords = []
        for keyword in canvas_keywords:
            if keyword.lower() in content.lower():
                found_keywords.append(keyword)
        
        assert len(found_keywords) >= 2, f"HTML文件缺少画布相关关键元素，只找到: {found_keywords}"
    
    def test_dev_notes_documentation_exists(self):
        """测试开发文档是否存在并包含BUG修复相关内容"""
        dev_notes_file = Path("docs/78b245/b1ca57/dev-notes.md")
        assert dev_notes_file.exists(), "开发文档文件不存在"
        assert dev_notes_file.is_file(), "dev-notes.md不是有效文件"
        
        content = dev_notes_file.read_text(encoding='utf-8')
        
        # 检查文档是否包含BUG修复相关内容
        bug_keywords = [
            'bug',
            '修复',
            '连线',
            '节点',
            '断开',
            'fix'
        ]
        
        found_keywords = []
        for keyword in bug_keywords:
            if keyword.lower() in content.lower():
                found_keywords.append(keyword)
        
        assert len(found_keywords) >= 3, f"开发文档缺少BUG修复相关内容，只找到: {found_keywords}"
    
    def test_html_structure_validity(self):
        """测试HTML文件结构的基本有效性"""
        index_file = Path("index.html")
        assert index_file.exists(), "index.html文件不存在"
        
        content = index_file.read_text(encoding='utf-8')
        
        # 检查基本HTML结构
        assert '<html' in content.lower(), "缺少HTML标签"
        assert '<head' in content.lower(), "缺少HEAD标签"
        assert '<body' in content.lower(), "缺少BODY标签"
        
        # 检查HTML标签是否配对
        html_open = content.lower().count('<html')
        html_close = content.lower().count('</html>')
        assert html_open == html_close, "HTML标签不配对"
    
    def test_project_file_structure(self):
        """测试项目文件结构的完整性"""
        required_files = [
            Path("index.html"),
            Path("docs/78b245/b1ca57/dev-notes.md")
        ]
        
        missing_files = []
        for file_path in required_files:
            if not file_path.exists():
                missing_files.append(str(file_path))
        
        assert len(missing_files) == 0, f"缺少必要文件: {missing_files}"
    
    def test_canvas_connection_bug_documentation(self):
        """测试节点连线断开BUG的文档记录是否完整"""
        dev_notes_file = Path("docs/78b245/b1ca57/dev-notes.md")
        
        if dev_notes_file.exists():
            content = dev_notes_file.read_text(encoding='utf-8')
            
            # 检查是否记录了具体的BUG描述
            connection_issues = [
                '连线断开',
                'connection',
                'disconnect',
                '节点连接',
                'node connection'
            ]
            
            found_issues = []
            for issue in connection_issues:
                if issue.lower() in content.lower():
                    found_issues.append(issue)
            
            assert len(found_issues) >= 1, f"文档中未找到节点连线相关问题描述: {found_issues}"
        else:
            pytest.skip("开发文档文件不存在，跳过此测试")