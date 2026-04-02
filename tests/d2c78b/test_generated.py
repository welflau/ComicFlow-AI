import pytest
from pathlib import Path
from bs4 import BeautifulSoup

class TestFrontendComponents:
    
    def test_index_html_file_exists(self):
        """测试 index.html 文件是否存在"""
        index_file = Path("frontend") / "index.html"
        assert index_file.exists(), f"index.html 文件不存在: {index_file}"
        assert index_file.is_file(), f"index.html 不是一个有效文件: {index_file}"
    
    def test_index_html_contains_basic_structure(self):
        """测试 index.html 文件包含基本的 HTML 结构元素"""
        index_file = Path("frontend") / "index.html"
        
        with open(index_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        soup = BeautifulSoup(content, 'html.parser')
        
        # 检查基本HTML结构
        assert soup.find('html') is not None, "HTML文件缺少 <html> 标签"
        assert soup.find('head') is not None, "HTML文件缺少 <head> 标签"
        assert soup.find('body') is not None, "HTML文件缺少 <body> 标签"
        
        # 检查title标签
        title_tag = soup.find('title')
        assert title_tag is not None, "HTML文件缺少 <title> 标签"
        assert len(title_tag.get_text().strip()) > 0, "title标签内容为空"
    
    def test_index_html_contains_component_elements(self):
        """测试 index.html 文件包含组件库相关的关键元素"""
        index_file = Path("frontend") / "index.html"
        
        with open(index_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        soup = BeautifulSoup(content, 'html.parser')
        
        # 检查是否包含常见的组件库元素
        has_components = (
            soup.find(class_=lambda x: x and 'component' in x.lower()) or
            soup.find(class_=lambda x: x and 'btn' in x.lower()) or
            soup.find(class_=lambda x: x and 'card' in x.lower()) or
            soup.find('div', class_=True) or
            soup.find('button') or
            soup.find('input')
        )
        
        assert has_components is not None, "HTML文件中未找到组件相关元素"
    
    def test_dev_notes_file_exists(self):
        """测试开发文档文件是否存在"""
        dev_notes_file = Path("docs") / "d2c78b" / "676e7d" / "dev-notes.md"
        assert dev_notes_file.exists(), f"开发文档文件不存在: {dev_notes_file}"
        assert dev_notes_file.is_file(), f"开发文档不是一个有效文件: {dev_notes_file}"
    
    def test_dev_notes_contains_content(self):
        """测试开发文档文件包含有效内容"""
        dev_notes_file = Path("docs") / "d2c78b" / "676e7d" / "dev-notes.md"
        
        with open(dev_notes_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        assert len(content.strip()) > 0, "开发文档文件内容为空"
        
        # 检查是否包含常见的文档标记
        has_markdown_elements = (
            '#' in content or  # 标题
            '##' in content or  # 二级标题
            '```' in content or  # 代码块
            '- ' in content or  # 列表
            '* ' in content  # 列表
        )
        
        assert has_markdown_elements, "开发文档缺少常见的 Markdown 格式元素"
    
    def test_project_structure_integrity(self):
        """测试项目结构的完整性"""
        frontend_dir = Path("frontend")
        docs_dir = Path("docs")
        
        assert frontend_dir.exists(), "frontend 目录不存在"
        assert frontend_dir.is_dir(), "frontend 不是一个目录"
        
        assert docs_dir.exists(), "docs 目录不存在"
        assert docs_dir.is_dir(), "docs 不是一个目录"
        
        # 检查文档子目录结构
        docs_subdir = docs_dir / "d2c78b" / "676e7d"
        assert docs_subdir.exists(), f"文档子目录不存在: {docs_subdir}"
        assert docs_subdir.is_dir(), f"文档子目录不是一个目录: {docs_subdir}"