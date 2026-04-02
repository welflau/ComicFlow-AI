import pytest
from pathlib import Path
import re

class TestFrontendFiles:
    
    def test_index_html_exists(self):
        """测试 index.html 文件是否存在"""
        index_path = Path("frontend/index.html")
        assert index_path.exists(), f"index.html 文件不存在: {index_path}"
        assert index_path.is_file(), f"index.html 不是一个文件: {index_path}"
    
    def test_index_html_contains_essential_elements(self):
        """测试 index.html 文件包含必要的 HTML 元素"""
        index_path = Path("frontend/index.html")
        
        # 确保文件存在
        if not index_path.exists():
            pytest.skip("index.html 文件不存在，跳过内容测试")
        
        content = index_path.read_text(encoding='utf-8')
        
        # 检查基本 HTML 结构
        assert re.search(r'<html[^>]*>', content, re.IGNORECASE), "缺少 <html> 标签"
        assert re.search(r'<head[^>]*>', content, re.IGNORECASE), "缺少 <head> 标签"
        assert re.search(r'<body[^>]*>', content, re.IGNORECASE), "缺少 <body> 标签"
        
        # 检查性能优化相关元素
        assert re.search(r'<title[^>]*>.*</title>', content, re.IGNORECASE), "缺少 <title> 标签"
        
        # 检查是否包含性能优化相关的关键词
        performance_keywords = ['性能', 'performance', '优化', 'optimization', '测试', 'test']
        content_lower = content.lower()
        has_performance_keyword = any(keyword.lower() in content_lower for keyword in performance_keywords)
        assert has_performance_keyword, "HTML 内容应包含性能优化或测试相关的关键词"
    
    def test_dev_notes_markdown_exists_and_valid(self):
        """测试开发文档 markdown 文件是否存在且格式正确"""
        dev_notes_path = Path("docs/78b245/c604e2/dev-notes.md")
        
        assert dev_notes_path.exists(), f"开发文档不存在: {dev_notes_path}"
        assert dev_notes_path.is_file(), f"开发文档不是一个文件: {dev_notes_path}"
        
        content = dev_notes_path.read_text(encoding='utf-8')
        
        # 检查文件不为空
        assert len(content.strip()) > 0, "开发文档内容不能为空"
        
        # 检查是否包含 markdown 格式的标题
        has_markdown_header = re.search(r'^#+\s+.+', content, re.MULTILINE)
        assert has_markdown_header, "开发文档应包含 markdown 格式的标题"
        
        # 检查是否包含开发相关的关键词
        dev_keywords = ['开发', '性能', '优化', '测试', 'dev', 'performance', 'optimization', 'test']
        content_lower = content.lower()
        has_dev_keyword = any(keyword.lower() in content_lower for keyword in dev_keywords)
        assert has_dev_keyword, "开发文档应包含开发、性能或测试相关的内容"
    
    def test_frontend_directory_structure(self):
        """测试前端目录结构的完整性"""
        frontend_dir = Path("frontend")
        docs_dir = Path("docs/78b245/c604e2")
        
        assert frontend_dir.exists(), "frontend 目录不存在"
        assert frontend_dir.is_dir(), "frontend 不是一个目录"
        
        assert docs_dir.exists(), "docs 目录结构不完整"
        assert docs_dir.is_dir(), "docs 路径不是一个目录"
        
        # 检查关键文件是否都存在
        required_files = [
            Path("frontend/index.html"),
            Path("docs/78b245/c604e2/dev-notes.md")
        ]
        
        for file_path in required_files:
            assert file_path.exists(), f"必需的文件不存在: {file_path}"
    
    def test_html_performance_optimization_hints(self):
        """测试 HTML 文件是否包含性能优化相关的标签或属性"""
        index_path = Path("frontend/index.html")
        
        if not index_path.exists():
            pytest.skip("index.html 文件不存在，跳过性能优化测试")
        
        content = index_path.read_text(encoding='utf-8')
        
        # 检查性能优化相关的 HTML 特性
        performance_indicators = [
            r'<meta[^>]*viewport[^>]*>',  # 响应式设计
            r'<link[^>]*rel=["\']stylesheet["\'][^>]*>',  # CSS 链接
            r'<script[^>]*>',  # JavaScript
            r'defer|async',  # 异步加载
            r'preload|prefetch',  # 资源预加载
        ]
        
        found_indicators = []
        for indicator in performance_indicators:
            if re.search(indicator, content, re.IGNORECASE):
                found_indicators.append(indicator)
        
        # 至少应该包含一些基本的 HTML 结构元素
        assert len(found_indicators) > 0, "HTML 文件应包含一些基本的性能优化元素（如 meta 标签、CSS 或 JS 引用等）"