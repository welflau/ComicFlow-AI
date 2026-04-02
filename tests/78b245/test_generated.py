import pytest
from pathlib import Path
import re

class TestFrontendFiles:
    """前端文件测试类"""
    
    def test_index_html_exists(self):
        """测试index.html文件是否存在"""
        index_path = Path("frontend/index.html")
        assert index_path.exists(), f"index.html文件不存在: {index_path}"
        assert index_path.is_file(), f"index.html不是一个文件: {index_path}"
    
    def test_index_html_contains_essential_elements(self):
        """测试index.html文件包含必要的HTML元素"""
        index_path = Path("frontend/index.html")
        
        # 确保文件存在
        if not index_path.exists():
            pytest.skip(f"跳过测试，文件不存在: {index_path}")
        
        content = index_path.read_text(encoding='utf-8')
        
        # 检查基本HTML结构
        assert re.search(r'<html[^>]*>', content, re.IGNORECASE), "缺少<html>标签"
        assert re.search(r'<head[^>]*>', content, re.IGNORECASE), "缺少<head>标签"
        assert re.search(r'<body[^>]*>', content, re.IGNORECASE), "缺少<body>标签"
        
        # 检查性能优化相关元素
        performance_indicators = [
            r'<title[^>]*>',  # 页面标题
            r'<meta[^>]*charset',  # 字符编码
            r'<meta[^>]*viewport',  # 视口设置
        ]
        
        for indicator in performance_indicators:
            assert re.search(indicator, content, re.IGNORECASE), f"缺少性能优化相关元素: {indicator}"
    
    def test_dev_notes_file_exists_and_valid(self):
        """测试开发文档文件是否存在且包含有效内容"""
        dev_notes_path = Path("docs/78b245/c604e2/dev-notes.md")
        
        assert dev_notes_path.exists(), f"开发文档文件不存在: {dev_notes_path}"
        assert dev_notes_path.is_file(), f"开发文档不是一个文件: {dev_notes_path}"
        
        content = dev_notes_path.read_text(encoding='utf-8')
        
        # 检查文档不为空
        assert len(content.strip()) > 0, "开发文档内容为空"
        
        # 检查是否包含Markdown格式内容
        markdown_indicators = [
            r'^#\s+',  # 标题
            r'^\*\s+',  # 列表项
            r'^\-\s+',  # 列表项
            r'```',    # 代码块
            r'\*\*.*\*\*',  # 粗体
        ]
        
        has_markdown = any(re.search(indicator, content, re.MULTILINE) for indicator in markdown_indicators)
        assert has_markdown, "开发文档缺少Markdown格式内容"
    
    def test_frontend_directory_structure(self):
        """测试前端目录结构的完整性"""
        frontend_dir = Path("frontend")
        docs_dir = Path("docs/78b245/c604e2")
        
        assert frontend_dir.exists(), f"前端目录不存在: {frontend_dir}"
        assert frontend_dir.is_dir(), f"frontend不是一个目录: {frontend_dir}"
        
        assert docs_dir.exists(), f"文档目录不存在: {docs_dir}"
        assert docs_dir.is_dir(), f"docs目录不是一个目录: {docs_dir}"
        
        # 检查关键文件
        required_files = [
            Path("frontend/index.html"),
            Path("docs/78b245/c604e2/dev-notes.md")
        ]
        
        for file_path in required_files:
            assert file_path.exists(), f"必需文件缺失: {file_path}"
    
    def test_html_performance_optimization_features(self):
        """测试HTML文件中的性能优化特性"""
        index_path = Path("frontend/index.html")
        
        if not index_path.exists():
            pytest.skip(f"跳过测试，文件不存在: {index_path}")
        
        content = index_path.read_text(encoding='utf-8')
        
        # 检查性能优化相关特性
        performance_features = {
            'meta_viewport': r'<meta[^>]*name=["\']viewport["\'][^>]*>',
            'doctype': r'<!DOCTYPE\s+html>',
            'lang_attribute': r'<html[^>]*lang=["\'][^"\']+["\'][^>]*>',
        }
        
        found_features = []
        for feature_name, pattern in performance_features.items():
            if re.search(pattern, content, re.IGNORECASE):
                found_features.append(feature_name)
        
        # 至少应该有一些性能优化特性
        assert len(found_features) > 0, f"未发现任何性能优化特性，检查的特性: {list(performance_features.keys())}"