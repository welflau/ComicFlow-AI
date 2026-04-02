import pytest
from pathlib import Path
from bs4 import BeautifulSoup

class TestFrontendModule:
    
    def test_index_html_file_exists(self):
        """测试 index.html 文件是否存在"""
        index_file = Path("frontend") / "index.html"
        assert index_file.exists(), f"index.html 文件不存在: {index_file}"
        assert index_file.is_file(), f"{index_file} 不是一个有效的文件"
    
    def test_index_html_contains_essential_elements(self):
        """测试 index.html 文件包含必要的HTML元素"""
        index_file = Path("frontend") / "index.html"
        
        # 确保文件存在
        assert index_file.exists(), "index.html 文件不存在"
        
        # 读取并解析HTML内容
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
        connection_keywords = ['连线', 'connection', 'connect', 'line', 'link']
        has_connection_keyword = any(keyword in page_text for keyword in connection_keywords)
        assert has_connection_keyword, "HTML内容中未找到连线系统相关的关键词"
    
    def test_dev_notes_file_exists_and_readable(self):
        """测试开发文档文件是否存在且可读取"""
        dev_notes_file = Path("docs") / "78b245" / "7d7081" / "dev-notes.md"
        
        # 检查文件是否存在
        assert dev_notes_file.exists(), f"开发文档文件不存在: {dev_notes_file}"
        assert dev_notes_file.is_file(), f"{dev_notes_file} 不是一个有效的文件"
        
        # 检查文件是否可读取且不为空
        with open(dev_notes_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        assert len(content.strip()) > 0, "开发文档文件内容为空"
        assert content.strip().startswith('#') or 'dev' in content.lower() or '开发' in content, "文档内容不符合开发文档格式"
    
    def test_frontend_directory_structure(self):
        """测试前端目录结构的完整性"""
        frontend_dir = Path("frontend")
        docs_dir = Path("docs")
        
        # 检查主要目录是否存在
        assert frontend_dir.exists(), "frontend 目录不存在"
        assert frontend_dir.is_dir(), "frontend 不是一个目录"
        assert docs_dir.exists(), "docs 目录不存在"
        assert docs_dir.is_dir(), "docs 不是一个目录"
        
        # 检查文档子目录结构
        nested_docs_dir = docs_dir / "78b245" / "7d7081"
        assert nested_docs_dir.exists(), f"文档子目录不存在: {nested_docs_dir}"
        assert nested_docs_dir.is_dir(), f"{nested_docs_dir} 不是一个目录"
    
    def test_index_html_has_connection_interface_elements(self):
        """测试 index.html 包含连线系统界面相关元素"""
        index_file = Path("frontend") / "index.html"
        
        with open(index_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        soup = BeautifulSoup(content, 'html.parser')
        
        # 检查是否包含可能的连线界面元素
        interface_elements = [
            soup.find_all('canvas'),  # 画布元素，常用于连线绘制
            soup.find_all('svg'),     # SVG元素，也常用于连线
            soup.find_all('div'),     # 容器元素
            soup.find_all('button'),  # 按钮元素
        ]
        
        # 至少应该有一些基本的界面元素
        total_elements = sum(len(elements) for elements in interface_elements)
        assert total_elements > 0, "HTML中缺少基本的界面元素"
        
        # 检查是否有JavaScript引用（连线系统通常需要JavaScript）
        scripts = soup.find_all('script')
        has_js = len(scripts) > 0 or 'script' in content.lower()
        # 这里不强制要求，但可以作为提示
        if not has_js:
            print("提示: HTML中未发现JavaScript引用，连线系统可能需要JavaScript支持")