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
        has_main = "<main" in content.lower() or "<div" in content.lower()
        assert has_title or has_main, "HTML文件缺少标题或主要内容区域"

    def test_server_js_file_structure_and_syntax(self):
        """测试server.js文件结构和语法正确性"""
        server_file = Path("server.js")
        assert server_file.exists(), "server.js文件不存在"
        
        content = server_file.read_text(encoding='utf-8')
        assert content.strip(), "server.js文件内容为空"
        
        # 检查Node.js服务器常见模块导入
        common_imports = ["require", "express", "http", "app", "server"]
        has_server_code = any(keyword in content for keyword in common_imports)
        assert has_server_code, "server.js文件不包含服务器相关代码"
        
        # 检查是否有端口监听或路由定义
        has_listen = "listen" in content
        has_route = any(method in content for method in ["get", "post", "put", "delete", "use"])
        assert has_listen or has_route, "server.js文件缺少端口监听或路由定义"

    def test_package_json_structure_and_dependencies(self):
        """测试package.json文件结构和依赖配置"""
        package_file = Path("package.json")
        assert package_file.exists(), "package.json文件不存在"
        
        try:
            package_data = json.loads(package_file.read_text(encoding='utf-8'))
        except json.JSONDecodeError:
            pytest.fail("package.json文件格式不正确，无法解析JSON")
        
        # 检查必要字段
        assert "name" in package_data, "package.json缺少name字段"
        assert "version" in package_data, "package.json缺少version字段"
        
        # 检查脚本或依赖
        has_scripts = "scripts" in package_data and package_data["scripts"]
        has_dependencies = "dependencies" in package_data and package_data["dependencies"]
        has_dev_dependencies = "devDependencies" in package_data and package_data["devDependencies"]
        
        assert has_scripts or has_dependencies or has_dev_dependencies, \
            "package.json缺少scripts、dependencies或devDependencies配置"

    def test_documentation_file_exists_and_readable(self):
        """测试文档文件是否存在且可读"""
        doc_file = Path("docs/78b245/b1efbf/dev-notes.md")
        assert doc_file.exists(), "开发文档文件不存在"
        
        content = doc_file.read_text(encoding='utf-8')
        assert content.strip(), "文档文件内容为空"
        
        # 检查Markdown基本格式
        has_markdown_elements = any(marker in content for marker in ["#", "##", "###", "*", "-", "`"])
        assert has_markdown_elements, "文档文件不包含Markdown格式元素"

    def test_project_file_structure_integrity(self):
        """测试项目文件结构完整性"""
        required_files = [
            Path("index.html"),
            Path("server.js"), 
            Path("package.json"),
            Path("docs/78b245/b1efbf/dev-notes.md")
        ]
        
        missing_files = []
        for file_path in required_files:
            if not file_path.exists():
                missing_files.append(str(file_path))
        
        assert not missing_files, f"缺少必要文件: {', '.join(missing_files)}"
        
        # 检查docs目录结构
        docs_dir = Path("docs")
        assert docs_dir.is_dir(), "docs目录不存在或不是目录"
        
        nested_dir = Path("docs/78b245/b1efbf")
        assert nested_dir.is_dir(), "文档嵌套目录结构不正确"

    def test_node_modules_and_dependencies_compatibility(self):
        """测试Node.js依赖兼容性（如果存在node_modules）"""
        package_file = Path("package.json")
        if not package_file.exists():
            pytest.skip("package.json不存在，跳过依赖测试")
        
        node_modules = Path("node_modules")
        package_lock = Path("package-lock.json")
        yarn_lock = Path("yarn.lock")
        
        # 如果存在锁文件，检查依赖一致性
        if package_lock.exists() or yarn_lock.exists():
            assert node_modules.exists(), "存在锁文件但缺少node_modules目录"
            
            if node_modules.exists():
                # 检查node_modules不为空
                module_contents = list(node_modules.iterdir())
                assert module_contents, "node_modules目录为空"