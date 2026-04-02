import pytest
from pathlib import Path
import json
import subprocess
import sys
import os

class TestSystemIntegration:
    
    def test_html_file_exists_and_contains_key_elements(self):
        """测试HTML文件是否存在并包含关键元素"""
        html_file = Path("index.html")
        assert html_file.exists(), "index.html文件不存在"
        
        content = html_file.read_text(encoding='utf-8')
        assert content.strip(), "HTML文件内容为空"
        
        # 检查HTML基本结构
        assert "<html" in content.lower(), "HTML文件缺少html标签"
        assert "<head" in content.lower(), "HTML文件缺少head标签"
        assert "<body" in content.lower(), "HTML文件缺少body标签"
        
        # 检查是否包含标题或主要内容区域
        has_title = "<title" in content.lower()
        has_h1 = "<h1" in content.lower()
        has_main = "<main" in content.lower() or "<div" in content.lower()
        
        assert has_title or has_h1, "HTML文件缺少标题元素"
        assert has_main, "HTML文件缺少主要内容区域"

    def test_package_json_structure_and_dependencies(self):
        """测试package.json文件结构和依赖配置是否正确"""
        package_file = Path("package.json")
        assert package_file.exists(), "package.json文件不存在"
        
        try:
            package_data = json.loads(package_file.read_text(encoding='utf-8'))
        except json.JSONDecodeError:
            pytest.fail("package.json文件格式不正确")
        
        # 检查基本字段
        assert "name" in package_data, "package.json缺少name字段"
        assert "version" in package_data, "package.json缺少version字段"
        
        # 检查脚本或依赖
        has_scripts = "scripts" in package_data and isinstance(package_data["scripts"], dict)
        has_dependencies = "dependencies" in package_data and isinstance(package_data["dependencies"], dict)
        has_dev_dependencies = "devDependencies" in package_data and isinstance(package_data["devDependencies"], dict)
        
        assert has_scripts or has_dependencies or has_dev_dependencies, "package.json缺少scripts或dependencies配置"

    def test_server_js_syntax_and_basic_structure(self):
        """测试server.js文件语法正确性和基本结构"""
        server_file = Path("server.js")
        assert server_file.exists(), "server.js文件不存在"
        
        content = server_file.read_text(encoding='utf-8')
        assert content.strip(), "server.js文件内容为空"
        
        # 检查基本的Node.js服务器结构
        has_require_or_import = "require(" in content or "import " in content
        has_server_setup = any(keyword in content.lower() for keyword in [
            "express", "http", "server", "listen", "createserver"
        ])
        
        assert has_require_or_import, "server.js缺少模块导入语句"
        assert has_server_setup, "server.js缺少服务器设置相关代码"
        
        # 简单的语法检查 - 检查括号匹配
        open_braces = content.count('{')
        close_braces = content.count('}')
        open_parens = content.count('(')
        close_parens = content.count(')')
        
        assert abs(open_braces - close_braces) <= 1, "server.js可能存在大括号不匹配"
        assert abs(open_parens - close_parens) <= 1, "server.js可能存在小括号不匹配"

    def test_documentation_structure_and_content(self):
        """测试文档目录结构和开发文档内容完整性"""
        docs_dir = Path("docs")
        assert docs_dir.exists() and docs_dir.is_dir(), "docs目录不存在"
        
        # 检查嵌套目录结构
        nested_dir = docs_dir / "78b245" / "b1efbf"
        assert nested_dir.exists() and nested_dir.is_dir(), "文档嵌套目录结构不正确"
        
        dev_notes_file = nested_dir / "dev-notes.md"
        assert dev_notes_file.exists(), "开发文档dev-notes.md不存在"
        
        content = dev_notes_file.read_text(encoding='utf-8')
        assert content.strip(), "开发文档内容为空"
        
        # 检查Markdown文档基本结构
        has_headers = any(line.startswith('#') for line in content.split('\n'))
        has_content_lines = len([line for line in content.split('\n') if line.strip()]) >= 3
        
        assert has_headers, "开发文档缺少标题结构"
        assert has_content_lines, "开发文档内容过少"

    def test_project_file_integration_consistency(self):
        """测试项目文件之间的集成一致性"""
        # 检查所有核心文件是否存在
        core_files = [
            Path("index.html"),
            Path("server.js"), 
            Path("package.json"),
            Path("docs/78b245/b1efbf/dev-notes.md")
        ]
        
        missing_files = [f for f in core_files if not f.exists()]
        assert not missing_files, f"缺少核心文件: {[str(f) for f in missing_files]}"
        
        # 检查HTML和server.js的关联性
        html_content = Path("index.html").read_text(encoding='utf-8')
        server_content = Path("server.js").read_text(encoding='utf-8')
        
        # 检查是否有静态文件服务或路由配置
        serves_static = any(keyword in server_content.lower() for keyword in [
            "static", "public", "index.html", "sendfile"
        ])
        
        # 检查HTML是否引用了可能的API端点或资源
        has_api_calls = any(keyword in html_content.lower() for keyword in [
            "fetch(", "ajax", "api/", "/api", "xmlhttprequest"
        ])
        
        # 至少应该有静态文件服务或API交互的迹象
        integration_indicators = serves_static or has_api_calls
        assert integration_indicators, "前后端文件缺少明显的集成关联"