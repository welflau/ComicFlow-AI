import pytest
from pathlib import Path
import re

class TestFrontendModule:
    
    def test_index_html_file_exists(self):
        """测试 index.html 文件是否存在"""
        index_file = Path("frontend/index.html")
        assert index_file.exists(), f"index.html 文件不存在: {index_file}"
        assert index_file.is_file(), f"index.html 不是一个文件: {index_file}"
    
    def test_index_html_contains_essential_elements(self):
        """测试 index.html 文件包含必要的HTML元素"""
        index_file = Path("frontend/index.html")
        
        # 确保文件存在
        assert index_file.exists(), "index.html 文件不存在"
        
        # 读取文件内容
        content = index_file.read_text(encoding='utf-8')
        
        # 检查基本HTML结构
        assert re.search(r'<html[^>]*>', content, re.IGNORECASE), "缺少 <html> 标签"
        assert re.search(r'<head[^>]*>', content, re.IGNORECASE), "缺少 <head> 标签"
        assert re.search(r'<body[^>]*>', content, re.IGNORECASE), "缺少 <body> 标签"
        
        # 检查节点系统相关元素
        assert re.search(r'<title[^>]*>.*节点.*</title>', content, re.IGNORECASE), "标题应包含'节点'关键词"
    
    def test_index_html_has_valid_structure(self):
        """测试 index.html 文件具有有效的HTML结构和节点系统功能元素"""
        index_file = Path("frontend/index.html")
        content = index_file.read_text(encoding='utf-8')
        
        # 检查是否包含节点系统相关的容器或脚本
        node_related_patterns = [
            r'node',
            r'canvas',
            r'svg',
            r'graph',
            r'diagram'
        ]
        
        has_node_elements = any(
            re.search(pattern, content, re.IGNORECASE) 
            for pattern in node_related_patterns
        )
        
        assert has_node_elements, "HTML文件应包含节点系统相关的元素（node、canvas、svg、graph或diagram）"
        
        # 检查是否有JavaScript引用或内联脚本
        has_script = re.search(r'<script[^>]*>', content, re.IGNORECASE)
        assert has_script, "节点系统应包含JavaScript脚本"
    
    def test_dev_notes_file_exists_and_readable(self):
        """测试开发文档文件是否存在且可读"""
        dev_notes_file = Path("docs/78b245/b2cdd4/dev-notes.md")
        
        assert dev_notes_file.exists(), f"开发文档文件不存在: {dev_notes_file}"
        assert dev_notes_file.is_file(), f"开发文档不是一个文件: {dev_notes_file}"
        
        # 检查文件是否可读且不为空
        content = dev_notes_file.read_text(encoding='utf-8')
        assert len(content.strip()) > 0, "开发文档文件不应为空"
        
        # 检查是否包含开发相关内容
        dev_keywords = ['开发', '节点', 'node', 'development', 'TODO', 'BUG', 'FEATURE']
        has_dev_content = any(keyword in content for keyword in dev_keywords)
        assert has_dev_content, "开发文档应包含开发相关的关键词"
    
    def test_frontend_directory_structure(self):
        """测试前端目录结构的完整性"""
        frontend_dir = Path("frontend")
        docs_dir = Path("docs/78b245/b2cdd4")
        
        assert frontend_dir.exists(), "frontend 目录不存在"
        assert frontend_dir.is_dir(), "frontend 应该是一个目录"
        
        assert docs_dir.exists(), "文档目录不存在"
        assert docs_dir.is_dir(), "docs/78b245/b2cdd4 应该是一个目录"
        
        # 检查关键文件
        required_files = [
            Path("frontend/index.html"),
            Path("docs/78b245/b2cdd4/dev-notes.md")
        ]
        
        for file_path in required_files:
            assert file_path.exists(), f"必需文件不存在: {file_path}"