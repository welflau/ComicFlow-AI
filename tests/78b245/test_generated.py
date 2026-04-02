import pytest
import json
from pathlib import Path
from unittest.mock import patch, MagicMock
import sys
import os

# 添加项目根目录到Python路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

class TestWebSocketCollaborationBackend:
    
    def test_project_files_exist(self):
        """测试项目必要文件是否存在"""
        project_root = Path(__file__).parent
        
        # 检查核心文件是否存在
        server_file = project_root / "server.js"
        package_file = project_root / "package.json"
        index_file = project_root / "index.html"
        dev_notes_file = project_root / "docs" / "78b245" / "f0e90c" / "dev-notes.md"
        
        assert server_file.exists(), "server.js 文件不存在"
        assert package_file.exists(), "package.json 文件不存在"
        assert index_file.exists(), "index.html 文件不存在"
        assert dev_notes_file.exists(), "开发文档文件不存在"

    def test_package_json_configuration(self):
        """测试package.json配置文件内容是否包含必要的WebSocket依赖和脚本"""
        project_root = Path(__file__).parent
        package_file = project_root / "package.json"
        
        assert package_file.exists(), "package.json 文件不存在"
        
        with open(package_file, 'r', encoding='utf-8') as f:
            package_data = json.load(f)
        
        # 检查是否包含WebSocket相关依赖
        dependencies = package_data.get('dependencies', {})
        dev_dependencies = package_data.get('devDependencies', {})
        all_deps = {**dependencies, **dev_dependencies}
        
        # 检查常见的WebSocket库
        websocket_libs = ['ws', 'socket.io', 'websocket', 'uws']
        has_websocket_lib = any(lib in all_deps for lib in websocket_libs)
        
        assert has_websocket_lib, "package.json 中未找到WebSocket相关依赖"
        
        # 检查启动脚本
        scripts = package_data.get('scripts', {})
        assert 'start' in scripts or 'dev' in scripts, "package.json 中缺少启动脚本"

    def test_html_file_contains_websocket_elements(self):
        """测试HTML文件是否包含WebSocket协作相关的关键元素"""
        project_root = Path(__file__).parent
        index_file = project_root / "index.html"
        
        assert index_file.exists(), "index.html 文件不存在"
        
        with open(index_file, 'r', encoding='utf-8') as f:
            html_content = f.read().lower()
        
        # 检查HTML基本结构
        assert '<html' in html_content, "HTML文件缺少html标签"
        assert '<head>' in html_content, "HTML文件缺少head标签"
        assert '<body>' in html_content, "HTML文件缺少body标签"
        
        # 检查WebSocket相关元素
        websocket_indicators = [
            'websocket',
            'socket.io',
            'ws://',
            'wss://',
            'onmessage',
            'send(',
            'connect'
        ]
        
        has_websocket_code = any(indicator in html_content for indicator in websocket_indicators)
        assert has_websocket_code, "HTML文件中未找到WebSocket相关代码"
        
        # 检查协作相关元素
        collaboration_elements = [
            'input',
            'textarea',
            'contenteditable',
            'chat',
            'message',
            'user'
        ]
        
        has_collaboration_elements = any(element in html_content for element in collaboration_elements)
        assert has_collaboration_elements, "HTML文件中未找到协作相关的UI元素"

    def test_server_js_file_structure(self):
        """测试server.js文件是否包含WebSocket服务器的基本结构"""
        project_root = Path(__file__).parent
        server_file = project_root / "server.js"
        
        assert server_file.exists(), "server.js 文件不存在"
        
        with open(server_file, 'r', encoding='utf-8') as f:
            server_content = f.read()
        
        # 检查Node.js require语句
        node_indicators = [
            'require(',
            'const ',
            'let ',
            'var '
        ]
        has_node_syntax = any(indicator in server_content for indicator in node_indicators)
        assert has_node_syntax, "server.js 文件缺少Node.js基本语法"
        
        # 检查WebSocket服务器相关代码
        websocket_server_indicators = [
            'WebSocket',
            'socket.io',
            'ws',
            'Server',
            'listen',
            'on(',
            'connection'
        ]
        
        has_websocket_server = any(indicator in server_content for indicator in websocket_server_indicators)
        assert has_websocket_server, "server.js 文件中未找到WebSocket服务器相关代码"
        
        # 检查端口监听
        port_indicators = [
            'listen(',
            'port',
            '3000',
            '8080',
            'PORT'
        ]
        
        has_port_config = any(indicator in server_content for indicator in port_indicators)
        assert has_port_config, "server.js 文件中未找到端口监听配置"

    def test_development_documentation_exists(self):
        """测试开发文档是否存在并包含有用信息"""
        project_root = Path(__file__).parent
        dev_notes_file = project_root / "docs" / "78b245" / "f0e90c" / "dev-notes.md"
        
        assert dev_notes_file.exists(), "开发文档文件不存在"
        
        with open(dev_notes_file, 'r', encoding='utf-8') as f:
            doc_content = f.read().lower()
        
        # 检查文档是否为空
        assert len(doc_content.strip()) > 0, "开发文档文件为空"
        
        # 检查是否包含开发相关信息
        dev_keywords = [
            'websocket',
            '协作',
            'collaboration',
            '实时',
            'real-time',
            'server',
            'client',
            'api',
            '安装',
            'install',
            '运行',
            'run',
            '启动',
            'start'
        ]
        
        has_dev_info = any(keyword in doc_content for keyword in dev_keywords)
        assert has_dev_info, "开发文档中未找到相关的开发信息"

    @patch('subprocess.run')
    def test_mock_server_startup(self, mock_subprocess):
        """模拟测试服务器启动流程是否正确"""
        project_root = Path(__file__).parent
        server_file = project_root / "server.js"
        package_file = project_root / "package.json"
        
        # 确保文件存在
        assert server_file.exists(), "server.js 文件不存在"
        assert package_file.exists(), "package