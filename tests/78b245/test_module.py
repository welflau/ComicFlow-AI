import pytest
from pathlib import Path
import re

class TestFrontendModule:
    
    def test_index_html_file_exists(self):
        """测试 index.html 文件是否存在"""
        index_file = Path("frontend/index.html")
        assert index_file.exists(), f"index.html 文件不存在: {index_file}"
        assert index_file.is_file(), f"index.html 不是一个有效文件: {index_file}"
    
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
        assert re.search(r'<title[^>]*>.*节点.*</title>', content, re.IGNORECASE), "标题中应包含'节点'关键词"
    
    def test_index_html_has_valid_structure(self):
        """测试 index.html 文件具有有效的HTML结构和节点系统相关功能"""
        index_file = Path("frontend/index.html")
        content = index_file.read_text(encoding='utf-8')
        
        # 检查是否包含节点系统相关的元素
        node_related_patterns = [
            r'node|节点',  # 节点相关文本
            r'<div[^>]*id[^>]*>',  # 包含id的div元素
            r'<script[^>]*>',  # JavaScript脚本
        ]
        
        for pattern in node_related_patterns:
            assert re.search(pattern, content, re.IGNORECASE), f"HTML内容应包含模式: {pattern}"
        
        # 检查HTML标签是否正确闭合
        open_tags = re.findall(r'<(\w+)[^>]*>', content)
        close_tags = re.findall(r'</(\w+)>', content)
        
        # 检查主要标签是否有对应的闭合标签
        main_tags = ['html', 'head', 'body']
        for tag in main_tags:
            if tag in open_tags:
                assert tag in close_tags, f"标签 <{tag}> 没有正确闭合"
    
    def test_dev_notes_file_exists_and_readable(self):
        """测试开发文档文件是否存在且可读"""
        dev_notes_file = Path("docs/78b245/b2cdd4/dev-notes.md")
        
        assert dev_notes_file.exists(), f"开发文档文件不存在: {dev_notes_file}"
        assert dev_notes_file.is_file(), f"开发文档不是一个有效文件: {dev_notes_file}"
        
        # 测试文件是否可读且非空
        content = dev_notes_file.read_text(encoding='utf-8')
        assert len(content.strip()) > 0, "开发文档文件不应为空"
        
        # 检查是否包含开发相关内容
        dev_keywords = ['开发', '节点', 'dev', 'node', '#']
        has_dev_content = any(keyword in content.lower() for keyword in dev_keywords)
        assert has_dev_content, "开发文档应包含开发相关关键词"
    
    def test_frontend_directory_structure(self):
        """测试前端目录结构的完整性"""
        frontend_dir = Path("frontend")
        docs_dir = Path("docs/78b245/b2cdd4")
        
        assert frontend_dir.exists(), "frontend 目录不存在"
        assert frontend_dir.is_dir(), "frontend 不是一个有效目录"
        
        assert docs_dir.exists(), "文档目录不存在"
        assert docs_dir.is_dir(), "文档路径不是一个有效目录"
        
        # 检查关键文件
        required_files = [
            Path("frontend/index.html"),
            Path("docs/78b245/b2cdd4/dev-notes.md")
        ]
        
        for file_path in required_files:
            assert file_path.exists(), f"必需文件不存在: {file_path}"