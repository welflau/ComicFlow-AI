import pytest
from pathlib import Path
import re

class TestFrontendWorkflowInterface:
    
    def test_index_html_file_exists(self):
        """测试主页HTML文件是否存在"""
        index_file = Path("frontend") / "index.html"
        assert index_file.exists(), f"主页文件 {index_file} 不存在"
        assert index_file.is_file(), f"{index_file} 不是一个有效的文件"
    
    def test_index_html_contains_workflow_elements(self):
        """测试HTML文件是否包含工作流执行界面的关键元素"""
        index_file = Path("frontend") / "index.html"
        
        with open(index_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 检查基本HTML结构
        assert '<html' in content.lower(), "HTML文件缺少html标签"
        assert '<head>' in content.lower(), "HTML文件缺少head标签"
        assert '<body>' in content.lower(), "HTML文件缺少body标签"
        
        # 检查工作流相关的关键元素
        workflow_keywords = ['workflow', '工作流', 'execute', '执行', 'button', 'input']
        found_keywords = [keyword for keyword in workflow_keywords if keyword in content.lower()]
        assert len(found_keywords) >= 2, f"HTML文件应包含更多工作流相关元素，当前只找到: {found_keywords}"
    
    def test_dev_notes_documentation_exists(self):
        """测试开发文档是否存在并包含有效内容"""
        dev_notes_file = Path("docs") / "78b245" / "33bf13" / "dev-notes.md"
        
        assert dev_notes_file.exists(), f"开发文档 {dev_notes_file} 不存在"
        assert dev_notes_file.is_file(), f"{dev_notes_file} 不是一个有效的文件"
        
        with open(dev_notes_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 检查文档不为空且包含有意义的内容
        assert len(content.strip()) > 0, "开发文档不能为空"
        assert len(content.strip()) > 50, "开发文档内容过少，应包含更详细的说明"
        
        # 检查是否包含开发相关的关键词
        dev_keywords = ['frontend', '前端', 'workflow', '工作流', 'interface', '界面']
        found_dev_keywords = [keyword for keyword in dev_keywords if keyword in content.lower()]
        assert len(found_dev_keywords) >= 1, f"开发文档应包含项目相关的关键词，当前找到: {found_dev_keywords}"
    
    def test_html_structure_validity(self):
        """测试HTML文件的基本结构有效性"""
        index_file = Path("frontend") / "index.html"
        
        with open(index_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 检查HTML标签是否正确闭合
        html_open = content.lower().count('<html')
        html_close = content.lower().count('</html>')
        assert html_open == html_close, "HTML标签未正确闭合"
        
        head_open = content.lower().count('<head>')
        head_close = content.lower().count('</head>')
        assert head_open == head_close, "HEAD标签未正确闭合"
        
        body_open = content.lower().count('<body>')
        body_close = content.lower().count('</body>')
        assert body_open == body_close, "BODY标签未正确闭合"
    
    def test_frontend_directory_structure(self):
        """测试前端目录结构是否合理"""
        frontend_dir = Path("frontend")
        
        assert frontend_dir.exists(), "frontend目录不存在"
        assert frontend_dir.is_dir(), "frontend应该是一个目录"
        
        # 检查目录中是否有必要的文件
        files_in_frontend = list(frontend_dir.iterdir())
        assert len(files_in_frontend) > 0, "frontend目录不能为空"
        
        # 检查是否有index.html文件
        index_exists = any(f.name == 'index.html' for f in files_in_frontend)
        assert index_exists, "frontend目录中必须包含index.html文件"