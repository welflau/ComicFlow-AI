import pytest
from pathlib import Path
import os

class TestFeature2795Documentation:
    """测试 feature_2795 相关文档和文件的存在性和内容"""
    
    def test_feature_js_file_exists(self):
        """测试 feature_2795.js 文件是否存在"""
        project_root = Path.cwd()
        js_file = project_root / "src" / "feature_2795.js"
        assert js_file.exists(), f"JavaScript文件不存在: {js_file}"
        assert js_file.is_file(), f"路径不是文件: {js_file}"
    
    def test_dev_notes_markdown_exists(self):
        """测试开发文档 dev-notes.md 文件是否存在"""
        project_root = Path.cwd()
        doc_file = project_root / "docs" / "d2c78b" / "7687ff" / "dev-notes.md"
        assert doc_file.exists(), f"开发文档不存在: {doc_file}"
        assert doc_file.is_file(), f"路径不是文件: {doc_file}"
    
    def test_js_file_contains_valid_content(self):
        """测试 JavaScript 文件包含有效的代码内容"""
        project_root = Path.cwd()
        js_file = project_root / "src" / "feature_2795.js"
        
        if js_file.exists():
            content = js_file.read_text(encoding='utf-8')
            # 检查是否包含基本的JavaScript关键字或结构
            js_keywords = ['function', 'const', 'let', 'var', 'class', 'export', 'import']
            has_js_content = any(keyword in content for keyword in js_keywords)
            assert has_js_content, "JavaScript文件应包含有效的代码内容"
            assert len(content.strip()) > 0, "JavaScript文件不应为空"
    
    def test_markdown_file_contains_documentation(self):
        """测试 Markdown 文档包含有效的文档内容"""
        project_root = Path.cwd()
        doc_file = project_root / "docs" / "d2c78b" / "7687ff" / "dev-notes.md"
        
        if doc_file.exists():
            content = doc_file.read_text(encoding='utf-8')
            # 检查是否包含Markdown格式的内容
            markdown_indicators = ['#', '##', '###', '-', '*', '```', '**', '__']
            has_markdown_content = any(indicator in content for indicator in markdown_indicators)
            assert has_markdown_content, "Markdown文件应包含格式化的文档内容"
            assert len(content.strip()) > 0, "文档文件不应为空"
    
    def test_project_structure_integrity(self):
        """测试项目目录结构的完整性"""
        project_root = Path.cwd()
        
        # 检查src目录存在
        src_dir = project_root / "src"
        assert src_dir.exists() and src_dir.is_dir(), "src目录应该存在"
        
        # 检查docs目录结构存在
        docs_dir = project_root / "docs" / "d2c78b" / "7687ff"
        assert docs_dir.exists() and docs_dir.is_dir(), "文档目录结构应该存在"
        
        # 检查目录权限
        assert os.access(src_dir, os.R_OK), "src目录应该可读"
        assert os.access(docs_dir, os.R_OK), "docs目录应该可读"