import pytest
from pathlib import Path
import json
import os
from unittest.mock import patch, mock_open

class TestUserAuthModule:
    """用户认证模块测试类"""
    
    @pytest.fixture
    def project_root(self):
        """获取项目根目录路径"""
        return Path(__file__).parent.parent
    
    def test_html_file_exists_and_contains_auth_elements(self, project_root):
        """测试HTML文件存在且包含用户认证相关的关键元素"""
        html_file = project_root / "api" / "index.html"
        
        # 检查文件是否存在
        assert html_file.exists(), f"HTML文件不存在: {html_file}"
        
        # 读取HTML内容并检查关键元素
        content = html_file.read_text(encoding='utf-8')
        
        # 检查是否包含用户认证相关的关键元素
        auth_keywords = ['login', 'password', 'username', 'auth', 'signin', 'user']
        found_keywords = [keyword for keyword in auth_keywords if keyword.lower() in content.lower()]
        
        assert len(found_keywords) > 0, f"HTML文件中未找到用户认证相关元素，期望包含: {auth_keywords}"
        assert '<html' in content.lower(), "HTML文件格式不正确，缺少html标签"
        assert '<body' in content.lower(), "HTML文件格式不正确，缺少body标签"
    
    def test_server_js_file_structure_and_auth_functions(self, project_root):
        """测试server.js文件存在且包含用户认证相关的函数结构"""
        server_file = project_root / "api" / "server.js"
        
        # 检查文件是否存在
        assert server_file.exists(), f"server.js文件不存在: {server_file}"
        
        # 读取JavaScript内容
        content = server_file.read_text(encoding='utf-8')
        
        # 检查是否包含Node.js服务器相关代码
        server_keywords = ['express', 'app', 'listen', 'port', 'require']
        found_server_keywords = [keyword for keyword in server_keywords if keyword in content]
        assert len(found_server_keywords) >= 2, f"server.js文件缺少基本服务器结构，期望包含: {server_keywords}"
        
        # 检查是否包含用户认证相关的路由或函数
        auth_functions = ['login', 'auth', 'user', 'password', 'token', 'session']
        found_auth_functions = [func for func in auth_functions if func.lower() in content.lower()]
        assert len(found_auth_functions) > 0, f"server.js文件中未找到用户认证相关功能，期望包含: {auth_functions}"
    
    def test_package_json_contains_required_dependencies(self, project_root):
        """测试package.json文件存在且包含用户认证模块所需的依赖包"""
        package_file = project_root / "api" / "package.json"
        
        # 检查文件是否存在
        assert package_file.exists(), f"package.json文件不存在: {package_file}"
        
        # 解析JSON内容
        content = package_file.read_text(encoding='utf-8')
        package_data = json.loads(content)
        
        # 检查基本字段
        required_fields = ['name', 'version']
        for field in required_fields:
            assert field in package_data, f"package.json缺少必要字段: {field}"
        
        # 检查是否包含认证相关的依赖包
        dependencies = package_data.get('dependencies', {})
        dev_dependencies = package_data.get('devDependencies', {})
        all_dependencies = {**dependencies, **dev_dependencies}
        
        # 常见的用户认证相关依赖包
        auth_packages = ['express', 'jsonwebtoken', 'bcrypt', 'passport', 'express-session', 'cors']
        found_packages = [pkg for pkg in auth_packages if pkg in all_dependencies]
        
        assert len(found_packages) > 0, f"package.json中未找到用户认证相关依赖包，期望包含: {auth_packages}"
    
    def test_env_example_file_contains_auth_config(self, project_root):
        """测试.env.example文件存在且包含用户认证相关的配置项"""
        env_file = project_root / "api" / ".env.example"
        
        # 检查文件是否存在
        assert env_file.exists(), f".env.example文件不存在: {env_file}"
        
        # 读取环境变量配置内容
        content = env_file.read_text(encoding='utf-8')
        
        # 检查是否包含认证相关的环境变量
        auth_env_vars = ['SECRET', 'JWT', 'TOKEN', 'AUTH', 'PASSWORD', 'DATABASE', 'PORT']
        found_vars = []
        
        for var in auth_env_vars:
            if var in content.upper():
                found_vars.append(var)
        
        assert len(found_vars) > 0, f".env.example文件中未找到用户认证相关配置，期望包含: {auth_env_vars}"
        
        # 检查文件格式是否正确（KEY=VALUE格式）
        lines = [line.strip() for line in content.split('\n') if line.strip() and not line.startswith('#')]
        if lines:  # 如果有非注释行
            assert any('=' in line for line in lines), ".env.example文件格式不正确，应使用KEY=VALUE格式"
    
    def test_documentation_file_exists_and_readable(self, project_root):
        """测试开发文档文件存在且可读取，包含项目相关信息"""
        doc_file = project_root / "api" / "docs" / "d2c78b" / "c9b476" / "dev-notes.md"
        
        # 检查文件是否存在
        assert doc_file.exists(), f"开发文档文件不存在: {doc_file}"
        
        # 检查文件是否可读且不为空
        content = doc_file.read_text(encoding='utf-8')
        assert len(content.strip()) > 0, "开发文档文件为空"
        
        # 检查是否包含开发相关的关键词
        dev_keywords = ['api', 'auth', 'user', 'login', 'development', 'todo', 'note']
        found_keywords = [keyword for keyword in dev_keywords if keyword.lower() in content.lower()]
        
        assert len(found_keywords) > 0, f"开发文档中未找到相关内容，期望包含: {dev_keywords}"