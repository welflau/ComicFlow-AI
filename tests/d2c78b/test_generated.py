import pytest
from pathlib import Path
import os
import re

class TestFrontendInfrastructure:
    
    def test_feature_file_exists(self):
        """测试前端功能文件是否存在"""
        project_root = Path.cwd()
        feature_file = project_root / "frontend" / "src" / "feature_8892.js"
        assert feature_file.exists(), f"功能文件 {feature_file} 不存在"
        assert feature_file.is_file(), f"{feature_file} 不是一个有效的文件"
    
    def test_dev_notes_documentation_exists(self):
        """测试开发文档是否存在且包含必要内容"""
        project_root = Path.cwd()
        doc_file = project_root / "frontend" / "docs" / "d2c78b" / "44b160" / "dev-notes.md"
        assert doc_file.exists(), f"开发文档 {doc_file} 不存在"
        
        content = doc_file.read_text(encoding='utf-8')
        assert len(content.strip()) > 0, "开发文档内容为空"
        assert any(keyword in content.lower() for keyword in ['feature', '功能', 'development', '开发']), "文档缺少关键开发信息"
    
    def test_frontend_structure_integrity(self):
        """测试前端项目结构完整性"""
        project_root = Path.cwd()
        frontend_dir = project_root / "frontend"
        
        assert frontend_dir.exists(), "frontend 目录不存在"
        assert frontend_dir.is_dir(), "frontend 不是一个目录"
        
        src_dir = frontend_dir / "src"
        docs_dir = frontend_dir / "docs"
        
        assert src_dir.exists(), "src 源码目录不存在"
        assert docs_dir.exists(), "docs 文档目录不存在"
    
    def test_feature_file_content_structure(self):
        """测试功能文件内容结构是否符合前端开发规范"""
        project_root = Path.cwd()
        feature_file = project_root / "frontend" / "src" / "feature_8892.js"
        
        if feature_file.exists():
            content = feature_file.read_text(encoding='utf-8')
            
            # 检查是否包含基本的JavaScript结构元素
            js_patterns = [
                r'function\s+\w+',  # 函数定义
                r'const\s+\w+',     # 常量定义
                r'let\s+\w+',       # 变量定义
                r'var\s+\w+',       # 变量定义
                r'export\s+',       # 导出语句
                r'import\s+',       # 导入语句
            ]
            
            has_js_structure = any(re.search(pattern, content) for pattern in js_patterns)
            assert has_js_structure or len(content.strip()) == 0, "JavaScript文件缺少基本的代码结构"
    
    def test_documentation_hierarchy(self):
        """测试文档目录层级结构是否正确"""
        project_root = Path.cwd()
        docs_path = project_root / "frontend" / "docs" / "d2c78b" / "44b160"
        
        assert docs_path.exists(), f"文档路径 {docs_path} 不存在"
        assert docs_path.is_dir(), f"{docs_path} 不是一个目录"
        
        # 检查是否有markdown文件
        md_files = list(docs_path.glob("*.md"))
        assert len(md_files) > 0, "文档目录中没有找到markdown文件"