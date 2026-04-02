import pytest
from pathlib import Path
from bs4 import BeautifulSoup

class TestFrontendModule:
    
    def test_index_html_file_exists(self):
        """测试 index.html 文件是否存在"""
        index_file = Path("frontend") / "index.html"
        assert index_file.exists(), f"index.html 文件不存在: {index_file}"
        assert index_file.is_file(), f"index.html 不是一个有效文件: {index_file}"
    
    def test_index_html_contains_essential_elements(self):
        """测试 index.html 文件包含必要的HTML元素"""
        index_file = Path("frontend") / "index.html"
        
        with open(index_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        soup = BeautifulSoup(content, 'html.parser')
        
        # 检查基本HTML结构
        assert soup.find('html') is not None, "缺少 <html> 标签"
        assert soup.find('head') is not None, "缺少 <head> 标签"
        assert soup.find('body') is not None, "缺少 <body> 标签"
        
        # 检查连线系统相关元素
        title = soup.find('title')
        assert title is not None, "缺少 <title> 标签"
        
        # 检查是否包含连线系统相关的关键词
        page_text = content.lower()
        connection_keywords = ['连线', 'connection', 'link', 'connect']
        has_connection_keyword = any(keyword in page_text for keyword in connection_keywords)
        assert has_connection_keyword, "页面内容中未找到连线系统相关关键词"
    
    def test_dev_notes_documentation_exists(self):
        """测试开发文档是否存在并包含有效内容"""
        dev_notes_file = Path("docs") / "78b245" / "7d7081" / "dev-notes.md"
        
        assert dev_notes_file.exists(), f"开发文档不存在: {dev_notes_file}"
        assert dev_notes_file.is_file(), f"开发文档不是有效文件: {dev_notes_file}"
        
        with open(dev_notes_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 检查文档不为空
        assert len(content.strip()) > 0, "开发文档内容为空"
        
        # 检查是否包含开发相关的关键词
        dev_keywords = ['开发', 'development', 'dev', '功能', 'feature', '模块', 'module']
        content_lower = content.lower()
        has_dev_keyword = any(keyword in content_lower for keyword in dev_keywords)
        assert has_dev_keyword, "开发文档中未找到开发相关关键词"
    
    def test_frontend_directory_structure(self):
        """测试前端目录结构的完整性"""
        frontend_dir = Path("frontend")
        docs_dir = Path("docs")
        
        assert frontend_dir.exists(), "frontend 目录不存在"
        assert frontend_dir.is_dir(), "frontend 不是一个目录"
        
        assert docs_dir.exists(), "docs 目录不存在"
        assert docs_dir.is_dir(), "docs 不是一个目录"
        
        # 检查文档目录结构
        nested_docs_dir = docs_dir / "78b245" / "7d7081"
        assert nested_docs_dir.exists(), f"嵌套文档目录不存在: {nested_docs_dir}"
        assert nested_docs_dir.is_dir(), f"嵌套文档路径不是目录: {nested_docs_dir}"
    
    def test_index_html_has_interactive_elements(self):
        """测试 index.html 包含交互元素，适合连线系统功能"""
        index_file = Path("frontend") / "index.html"
        
        with open(index_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        soup = BeautifulSoup(content, 'html.parser')
        
        # 检查是否有JavaScript相关元素（连线系统通常需要交互）
        scripts = soup.find_all('script')
        canvas_elements = soup.find_all('canvas')
        svg_elements = soup.find_all('svg')
        div_elements = soup.find_all('div')
        
        # 至少应该有一些交互元素或容器
        interactive_elements_count = len(scripts) + len(canvas_elements) + len(svg_elements) + len(div_elements)
        assert interactive_elements_count > 0, "页面缺少交互元素，连线系统需要JavaScript、Canvas、SVG或容器元素"