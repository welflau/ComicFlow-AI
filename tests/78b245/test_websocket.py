import pytest
import json
from pathlib import Path
import subprocess
import sys
import os

class TestWebSocketCollaborationBackend:
    """WebSocket实时协作后端测试类"""
    
    @pytest.fixture
    def project_root(self):
        """获取项目根目录"""
        return Path(__file__).parent
    
    def test_html_file_exists_and_contains_websocket_elements(self, project_root):
        """测试HTML文件是否存在并包含WebSocket相关的关键元素"""
        html_file = project_root / "index.html"
        
        # 检查文件是否存在
        assert html_file.exists(), f"HTML文件不存在: {html_file}"
        
        # 读取HTML内容
        html_content = html_file.read_text(encoding='utf-8')
        
        # 检查是否包含WebSocket相关的关键元素
        assert "websocket" in html_content.lower() or "ws://" in html_content or "wss://" in html_content, "HTML文件中未找到WebSocket相关内容"
        assert "<script" in html_content, "HTML文件中未找到script标签"
        assert "<!DOCTYPE html>" in html_content or "<html" in html_content, "HTML文件格式不正确"
    
    def test_package_json_structure_and_dependencies(self, project_root):
        """测试package.json文件结构是否正确并包含必要的依赖"""
        package_json_file = project_root / "package.json"
        
        # 检查文件是否存在
        assert package_json_file.exists(), f"package.json文件不存在: {package_json_file}"
        
        # 解析JSON内容
        with open(package_json_file, 'r', encoding='utf-8') as f:
            package_data = json.load(f)
        
        # 检查基本结构
        assert isinstance(package_data, dict), "package.json应该是一个JSON对象"
        assert "name" in package_data, "package.json中缺少name字段"
        assert "version" in package_data, "package.json中缺少version字段"
        
        # 检查是否包含WebSocket相关依赖
        dependencies = package_data.get("dependencies", {})
        dev_dependencies = package_data.get("devDependencies", {})
        all_deps = {**dependencies, **dev_dependencies}
        
        websocket_related = any(
            dep_name in ["ws", "websocket", "socket.io", "express", "node-websocket"]
            for dep_name in all_deps.keys()
        )
        assert websocket_related, "package.json中未找到WebSocket相关依赖"
    
    def test_server_js_file_structure_and_websocket_functionality(self, project_root):
        """测试server.js文件是否存在并包含WebSocket服务器功能代码"""
        server_js_file = project_root / "server.js"
        
        # 检查文件是否存在
        assert server_js_file.exists(), f"server.js文件不存在: {server_js_file}"
        
        # 读取服务器代码内容
        server_content = server_js_file.read_text(encoding='utf-8')
        
        # 检查是否包含WebSocket服务器相关代码
        websocket_indicators = [
            "require(",  # Node.js模块导入
            "WebSocket",  # WebSocket类或对象
            "ws",  # WebSocket库
            "socket.io",  # Socket.IO库
            "server",  # 服务器相关
            "listen",  # 监听端口
        ]
        
        found_indicators = sum(1 for indicator in websocket_indicators if indicator in server_content)
        assert found_indicators >= 3, f"server.js文件中WebSocket相关代码不足，仅找到{found_indicators}个关键指标"
        
        # 检查是否有端口配置
        port_indicators = ["port", "PORT", "3000", "8080"]
        has_port_config = any(indicator in server_content for indicator in port_indicators)
        assert has_port_config, "server.js文件中未找到端口配置"
    
    def test_documentation_file_exists_and_readable(self, project_root):
        """测试开发文档是否存在且可读取"""
        docs_file = project_root / "docs" / "78b245" / "f0e90c" / "dev-notes.md"
        
        # 检查文件是否存在
        assert docs_file.exists(), f"开发文档不存在: {docs_file}"
        
        # 检查文件是否可读
        doc_content = docs_file.read_text(encoding='utf-8')
        assert len(doc_content.strip()) > 0, "开发文档内容为空"
        
        # 检查是否包含开发相关内容
        dev_keywords = ["websocket", "协作", "实时", "backend", "server", "api", "功能"]
        found_keywords = sum(1 for keyword in dev_keywords if keyword.lower() in doc_content.lower())
        assert found_keywords >= 2, f"开发文档中相关关键词不足，仅找到{found_keywords}个"
    
    def test_project_file_structure_completeness(self, project_root):
        """测试项目文件结构的完整性"""
        required_files = [
            "server.js",
            "package.json", 
            "index.html"
        ]
        
        required_dirs = [
            "docs",
            "docs/78b245",
            "docs/78b245/f0e90c"
        ]
        
        # 检查必需文件
        for file_name in required_files:
            file_path = project_root / file_name
            assert file_path.exists(), f"必需文件缺失: {file_name}"
            assert file_path.is_file(), f"{file_name}不是有效文件"
        
        # 检查必需目录
        for dir_name in required_dirs:
            dir_path = project_root / dir_name
            assert dir_path.exists(), f"必需目录缺失: {dir_name}"
            assert dir_path.is_dir(), f"{dir_name}不是有效目录"