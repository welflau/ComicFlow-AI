import pytest
from pathlib import Path
from bs4 import BeautifulSoup

class TestFrontendModule:
    
    def test_index_html_file_exists(self):
        """测试index.html文件是否存在"""
        frontend_dir = Path(__file__).parent / "frontend"
        index_file = frontend_dir / "index.html"
        assert index_file.exists(), f"index.html文件不存在: {index_file}"
        assert index_file.is_file(), f"index.html不是一个有效文件: {index_file}"
    
    def test_index_html_contains_essential_elements(self):
        """测试index.html文件包含必要的HTML元素"""
        frontend_dir = Path(__file__).parent / "frontend"
        index_file = frontend_dir / "index.html"
        
        if not index_file.exists():
            pytest.skip("index.html文件不存在，跳过内容测试")
        
        with open(index_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        soup = BeautifulSoup(content, 'html.parser')
        
        # 检查基本HTML结构
        assert soup.find('html') is not None, "缺少html标签"
        assert soup.find('head') is not None, "缺少head标签"
        assert soup.find('body') is not None, "缺少body标签"
        
        # 检查性能优化相关元素
        title = soup.find('title')
        assert title is not None, "缺少title标签"
        
        # 检查是否包含性能优化相关的关键词
        page_text = content.lower()
        performance_keywords = ['性能', 'performance', '优化', 'optimization']
        has_performance_content = any(keyword in page_text for keyword in performance_keywords)
        assert has_performance_content, "页面内容应包含性能优化相关关键词"
    
    def test_dev_notes_markdown_file_exists_and_valid(self):
        """测试开发文档markdown文件是否存在且包含有效内容"""
        docs_dir = Path(__file__).parent / "docs" / "78b245" / "c604e2"
        dev_notes_file = docs_dir / "dev-notes.md"
        
        assert dev_notes_file.exists(), f"开发文档不存在: {dev_notes_file}"
        assert dev_notes_file.is_file(), f"开发文档不是有效文件: {dev_notes_file}"
        
        with open(dev_notes_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 检查文件不为空
        assert len(content.strip()) > 0, "开发文档内容不能为空"
        
        # 检查是否包含markdown格式内容
        markdown_indicators = ['#', '##', '###', '-', '*', '```', '**', '__']
        has_markdown_format = any(indicator in content for indicator in markdown_indicators)
        assert has_markdown_format, "开发文档应包含markdown格式内容"
        
        # 检查是否包含开发相关关键词
        dev_keywords = ['开发', '测试', 'test', 'dev', '性能', '优化', 'performance']
        content_lower = content.lower()
        has_dev_content = any(keyword in content_lower for keyword in dev_keywords)
        assert has_dev_content, "开发文档应包含开发或测试相关内容"
    
    def test_frontend_directory_structure(self):
        """测试前端目录结构的完整性"""
        frontend_dir = Path(__file__).parent / "frontend"
        docs_dir = Path(__file__).parent / "docs"
        
        # 检查主要目录存在
        assert frontend_dir.exists() or docs_dir.exists(), "项目目录结构不完整"
        
        # 如果frontend目录存在，检查其结构
        if frontend_dir.exists():
            assert frontend_dir.is_dir(), "frontend应该是一个目录"
            
            # 检查是否有HTML文件
            html_files = list(frontend_dir.glob("*.html"))
            assert len(html_files) > 0, "frontend目录应包含至少一个HTML文件"
        
        # 检查docs目录结构
        if docs_dir.exists():
            assert docs_dir.is_dir(), "docs应该是一个目录"
            
            # 检查是否有markdown文件
            md_files = list(docs_dir.rglob("*.md"))
            assert len(md_files) > 0, "docs目录应包含至少一个markdown文件"
    
    def test_html_performance_optimization_features(self):
        """测试HTML文件是否包含性能优化特性"""
        frontend_dir = Path(__file__).parent / "frontend"
        index_file = frontend_dir / "index.html"
        
        if not index_file.exists():
            pytest.skip("index.html文件不存在，跳过性能优化测试")
        
        with open(index_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        soup = BeautifulSoup(content, 'html.parser')
        
        # 检查性能优化相关的HTML特性
        performance_checks = []
        
        # 检查是否有meta viewport标签（移动端优化）
        viewport_meta = soup.find('meta', attrs={'name': 'viewport'})
        if viewport_meta:
            performance_checks.append("包含viewport meta标签")
        
        # 检查是否有压缩或优化相关的注释
        comments = soup.find_all(string=lambda text: isinstance(text, str) and 
                                ('优化' in text or 'optimization' in text or 'performance' in text))
        if comments:
            performance_checks.append("包含性能优化相关注释")
        
        # 检查是否有异步加载的脚本
        async_scripts = soup.find_all('script', attrs={'async': True})
        defer_scripts = soup.find_all('script', attrs={'defer': True})
        if async_scripts or defer_scripts:
            performance_checks.append("包含异步加载脚本")
        
        # 至少应该有一个性能优化特性或者相关内容
        content_lower = content.lower()
        has_performance_content = any(keyword in content_lower for keyword in 
                                    ['性能', 'performance', '优化', 'optimization', '测试', 'test'])
        
        assert len(performance_checks) > 0 or has_performance_content, \
            f"HTML文件应包含性能优化特性或相关内容。当前检查结果: {performance_checks}"