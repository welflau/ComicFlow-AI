import pytest
from pathlib import Path
from bs4 import BeautifulSoup

class TestFrontendNodeSystem:
    
    def test_index_html_file_exists(self):
        """测试 index.html 文件是否存在"""
        frontend_dir = Path(__file__).parent / "frontend"
        index_file = frontend_dir / "index.html"
        assert index_file.exists(), f"index.html 文件不存在于路径: {index_file}"
        assert index_file.is_file(), f"{index_file} 不是一个有效的文件"
    
    def test_index_html_contains_essential_elements(self):
        """测试 index.html 文件包含必要的HTML元素和节点系统相关内容"""
        frontend_dir = Path(__file__).parent / "frontend"
        index_file = frontend_dir / "index.html"
        
        with open(index_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        soup = BeautifulSoup(content, 'html.parser')
        
        # 检查基本HTML结构
        assert soup.find('html'), "HTML文件缺少html标签"
        assert soup.find('head'), "HTML文件缺少head标签"
        assert soup.find('body'), "HTML文件缺少body标签"
        
        # 检查节点系统相关元素
        title = soup.find('title')
        assert title, "HTML文件缺少title标签"
        
        # 检查是否包含节点系统相关的关键词
        page_text = content.lower()
        node_keywords = ['node', 'system', '节点', '系统']
        has_node_content = any(keyword in page_text for keyword in node_keywords)
        assert has_node_content, "HTML文件应包含节点系统相关的内容"
    
    def test_dev_notes_documentation_exists(self):
        """测试开发文档是否存在并包含有效内容"""
        docs_dir = Path(__file__).parent / "docs" / "78b245" / "b2cdd4"
        dev_notes_file = docs_dir / "dev-notes.md"
        
        assert dev_notes_file.exists(), f"开发文档不存在于路径: {dev_notes_file}"
        assert dev_notes_file.is_file(), f"{dev_notes_file} 不是一个有效的文件"
        
        with open(dev_notes_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 检查文档不为空
        assert len(content.strip()) > 0, "开发文档不应为空"
        
        # 检查是否包含开发相关的关键词
        content_lower = content.lower()
        dev_keywords = ['dev', 'development', '开发', 'note', '笔记', 'todo', 'bug', 'feature']
        has_dev_content = any(keyword in content_lower for keyword in dev_keywords)
        assert has_dev_content, "开发文档应包含开发相关的内容"
    
    def test_html_file_structure_and_syntax(self):
        """测试HTML文件的结构完整性和基本语法正确性"""
        frontend_dir = Path(__file__).parent / "frontend"
        index_file = frontend_dir / "index.html"
        
        with open(index_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 使用BeautifulSoup解析，如果语法严重错误会抛出异常
        soup = BeautifulSoup(content, 'html.parser')
        
        # 检查DOCTYPE声明
        doctype_exists = '<!doctype' in content.lower() or '<!DOCTYPE' in content
        assert doctype_exists, "HTML文件应包含DOCTYPE声明"
        
        # 检查字符编码设置
        meta_charset = soup.find('meta', attrs={'charset': True}) or soup.find('meta', attrs={'http-equiv': 'Content-Type'})
        assert meta_charset, "HTML文件应包含字符编码设置"
    
    def test_project_directory_structure(self):
        """测试项目目录结构的完整性"""
        project_root = Path(__file__).parent
        
        # 检查frontend目录存在
        frontend_dir = project_root / "frontend"
        assert frontend_dir.exists(), "frontend目录不存在"
        assert frontend_dir.is_dir(), "frontend应该是一个目录"
        
        # 检查docs目录结构存在
        docs_dir = project_root / "docs" / "78b245" / "b2cdd4"
        assert docs_dir.exists(), "docs目录结构不完整"
        assert docs_dir.is_dir(), "docs路径应该是一个目录"
        
        # 检查关键文件都存在
        required_files = [
            frontend_dir / "index.html",
            docs_dir / "dev-notes.md"
        ]
        
        for file_path in required_files:
            assert file_path.exists(), f"必需文件不存在: {file_path}"