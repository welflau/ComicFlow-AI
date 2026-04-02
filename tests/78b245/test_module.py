import pytest
from pathlib import Path
from bs4 import BeautifulSoup

class TestFrontendFiles:
    """前端文件测试类"""
    
    def test_index_html_exists(self):
        """测试 index.html 文件是否存在"""
        index_path = Path("frontend/index.html")
        assert index_path.exists(), f"index.html 文件不存在: {index_path}"
        assert index_path.is_file(), f"index.html 不是一个文件: {index_path}"
    
    def test_index_html_contains_essential_elements(self):
        """测试 index.html 包含必要的 HTML 元素"""
        index_path = Path("frontend/index.html")
        
        # 确保文件存在
        if not index_path.exists():
            pytest.skip(f"跳过测试，文件不存在: {index_path}")
        
        with open(index_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        soup = BeautifulSoup(content, 'html.parser')
        
        # 检查基本 HTML 结构
        assert soup.find('html') is not None, "缺少 <html> 标签"
        assert soup.find('head') is not None, "缺少 <head> 标签"
        assert soup.find('body') is not None, "缺少 <body> 标签"
        
        # 检查标题
        title = soup.find('title')
        assert title is not None, "缺少 <title> 标签"
        assert title.get_text().strip() != "", "标题不能为空"
    
    def test_index_html_performance_related_content(self):
        """测试 index.html 包含性能优化相关的内容或元素"""
        index_path = Path("frontend/index.html")
        
        if not index_path.exists():
            pytest.skip(f"跳过测试，文件不存在: {index_path}")
        
        with open(index_path, 'r', encoding='utf-8') as f:
            content = f.read().lower()
        
        # 检查是否包含性能优化相关的关键词或元素
        performance_indicators = [
            'performance', '性能', 'optimization', '优化',
            'test', '测试', 'benchmark', 'speed',
            'async', 'defer', 'preload', 'prefetch'
        ]
        
        has_performance_content = any(keyword in content for keyword in performance_indicators)
        assert has_performance_content, "HTML 文件应包含性能优化相关的内容或属性"
    
    def test_dev_notes_file_exists(self):
        """测试开发文档文件是否存在"""
        dev_notes_path = Path("docs/78b245/c604e2/dev-notes.md")
        assert dev_notes_path.exists(), f"开发文档文件不存在: {dev_notes_path}"
        assert dev_notes_path.is_file(), f"dev-notes.md 不是一个文件: {dev_notes_path}"
    
    def test_dev_notes_content_structure(self):
        """测试开发文档包含有效的内容结构"""
        dev_notes_path = Path("docs/78b245/c604e2/dev-notes.md")
        
        if not dev_notes_path.exists():
            pytest.skip(f"跳过测试，文件不存在: {dev_notes_path}")
        
        with open(dev_notes_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 检查文件不为空
        assert content.strip() != "", "开发文档不能为空"
        
        # 检查是否包含 Markdown 格式的内容
        markdown_indicators = ['#', '##', '###', '-', '*', '```', '**', '__']
        has_markdown = any(indicator in content for indicator in markdown_indicators)
        assert has_markdown, "开发文档应包含 Markdown 格式的内容"
    
    def test_project_directory_structure(self):
        """测试项目目录结构的完整性"""
        # 检查主要目录是否存在
        frontend_dir = Path("frontend")
        docs_dir = Path("docs")
        
        assert frontend_dir.exists(), "frontend 目录不存在"
        assert docs_dir.exists(), "docs 目录不存在"
        
        # 检查嵌套文档目录结构
        nested_docs_dir = Path("docs/78b245/c604e2")
        assert nested_docs_dir.exists(), f"嵌套文档目录不存在: {nested_docs_dir}"
        assert nested_docs_dir.is_dir(), f"路径不是目录: {nested_docs_dir}"