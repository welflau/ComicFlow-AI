import pytest
from pathlib import Path
import os

class TestFeature2795Documentation:
    """测试 feature_2795 相关文档和文件的存在性和内容"""
    
    def test_feature_2795_js_file_exists(self):
        """测试 feature_2795.js 文件是否存在"""
        js_file_path = Path("src") / "feature_2795.js"
        assert js_file_path.exists(), f"JavaScript文件 {js_file_path} 不存在"
        assert js_file_path.is_file(), f"{js_file_path} 不是一个有效的文件"
    
    def test_dev_notes_markdown_file_exists(self):
        """测试开发文档 markdown 文件是否存在"""
        docs_path = Path("docs") / "d2c78b" / "7687ff" / "dev-notes.md"
        assert docs_path.exists(), f"开发文档 {docs_path} 不存在"
        assert docs_path.is_file(), f"{docs_path} 不是一个有效的文件"
    
    def test_feature_2795_js_content_structure(self):
        """测试 feature_2795.js 文件内容包含基本的 JavaScript 结构元素"""
        js_file_path = Path("src") / "feature_2795.js"
        
        if js_file_path.exists():
            content = js_file_path.read_text(encoding='utf-8')
            
            # 检查是否包含常见的 JavaScript 关键字或结构
            js_keywords = ['function', 'const', 'let', 'var', 'class', 'export', 'import']
            has_js_content = any(keyword in content for keyword in js_keywords)
            
            assert has_js_content, "JavaScript文件应该包含基本的 JavaScript 代码结构"
            assert len(content.strip()) > 0, "JavaScript文件不应该为空"
        else:
            pytest.skip("JavaScript文件不存在，跳过内容测试")
    
    def test_dev_notes_markdown_content_structure(self):
        """测试开发文档 markdown 文件内容包含文档基本结构"""
        docs_path = Path("docs") / "d2c78b" / "7687ff" / "dev-notes.md"
        
        if docs_path.exists():
            content = docs_path.read_text(encoding='utf-8')
            
            # 检查是否包含 Markdown 常见元素
            markdown_elements = ['#', '##', '###', '-', '*', '```', '**', '__']
            has_markdown_content = any(element in content for element in markdown_elements)
            
            assert len(content.strip()) > 0, "开发文档不应该为空"
            # 如果文件不为空，应该包含一些 markdown 格式元素
            if len(content.strip()) > 10:
                assert has_markdown_content, "开发文档应该包含 Markdown 格式元素"
        else:
            pytest.skip("开发文档不存在，跳过内容测试")
    
    def test_project_directory_structure(self):
        """测试项目目录结构的完整性"""
        # 检查 src 目录存在
        src_dir = Path("src")
        assert src_dir.exists() and src_dir.is_dir(), "src 目录应该存在"
        
        # 检查 docs 目录存在
        docs_dir = Path("docs")
        assert docs_dir.exists() and docs_dir.is_dir(), "docs 目录应该存在"
        
        # 检查 docs 子目录结构
        docs_subdir = Path("docs") / "d2c78b" / "7687ff"
        assert docs_subdir.exists() and docs_subdir.is_dir(), f"文档子目录 {docs_subdir} 应该存在"