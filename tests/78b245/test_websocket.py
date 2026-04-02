import pytest
from pathlib import Path
import json
import re
import sys
import os

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

class TestWebSocketCollaborationBackend:
    
    def test_server_js_file_exists_and_contains_websocket_logic(self):
        """测试server.js文件是否存在并包含WebSocket相关逻辑"""
        server_file = project_root / "server.js"
        assert server_file.exists(), "server.js文件不存在"
        
        content = server_file.read_text(encoding='utf-8')
        
        # 检查是否包含WebSocket相关关键词
        websocket_keywords = ['websocket', 'ws', 'socket', 'connection', 'message']
        found_keywords = [keyword for keyword in websocket_keywords 
                         if keyword.lower() in content.lower()]
        assert len(found_keywords) >= 2, f"server.js应包含WebSocket相关关键词，找到: {found_keywords}"
        
        # 检查是否包含端口监听逻辑
        port_patterns = [r'listen\s*\(\s*\d+', r'port\s*[:=]\s*\d+', r'PORT']
        has_port_config = any(re.search(pattern, content, re.IGNORECASE) 
                             for pattern in port_patterns)
        assert has_port_config, "server.js应包含端口配置"

    def test_package_json_contains_required_dependencies(self):
        """测试package.json文件是否存在并包含必要的依赖项"""
        package_file = project_root / "package.json"
        assert package_file.exists(), "package.json文件不存在"
        
        with open(package_file, 'r', encoding='utf-8') as f:
            package_data = json.load(f)
        
        # 检查基本字段
        assert 'name' in package_data, "package.json应包含name字段"
        assert 'version' in package_data, "package.json应包含version字段"
        
        # 检查依赖项
        dependencies = package_data.get('dependencies', {})
        dev_dependencies = package_data.get('devDependencies', {})
        all_deps = {**dependencies, **dev_dependencies}
        
        # WebSocket相关依赖
        websocket_deps = ['ws', 'socket.io', 'websocket', 'express']
        found_deps = [dep for dep in websocket_deps if dep in all_deps]
        assert len(found_deps) >= 1, f"package.json应包含WebSocket相关依赖，找到: {found_deps}"

    def test_index_html_contains_collaboration_elements(self):
        """测试index.html文件是否存在并包含协作相关的HTML元素"""
        html_file = project_root / "index.html"
        assert html_file.exists(), "index.html文件不存在"
        
        content = html_file.read_text(encoding='utf-8')
        
        # 检查基本HTML结构
        assert '<html' in content.lower(), "应包含html标签"
        assert '<head' in content.lower(), "应包含head标签"
        assert '<body' in content.lower(), "应包含body标签"
        
        # 检查协作相关元素
        collaboration_keywords = ['websocket', 'socket', 'collaboration', 'real-time', 'realtime', 'connect']
        found_keywords = [keyword for keyword in collaboration_keywords 
                         if keyword.lower() in content.lower()]
        assert len(found_keywords) >= 1, f"HTML应包含协作相关关键词，找到: {found_keywords}"
        
        # 检查JavaScript引用或内联脚本
        has_script = '<script' in content.lower()
        assert has_script, "HTML应包含JavaScript脚本标签"

    def test_dev_notes_documentation_exists(self):
        """测试开发文档是否存在并包含有用信息"""
        docs_file = project_root / "docs" / "78b245" / "f0e90c" / "dev-notes.md"
        assert docs_file.exists(), "开发文档dev-notes.md不存在"
        
        content = docs_file.read_text(encoding='utf-8')
        assert len(content.strip()) > 0, "开发文档不应为空"
        
        # 检查是否包含开发相关信息
        dev_keywords = ['websocket', 'server', 'client', 'api', 'setup', 'install', 'run', 'start']
        found_keywords = [keyword for keyword in dev_keywords 
                         if keyword.lower() in content.lower()]
        assert len(found_keywords) >= 2, f"开发文档应包含开发相关信息，找到: {found_keywords}"

    def test_project_structure_completeness(self):
        """测试项目结构的完整性"""
        required_files = [
            "server.js",
            "package.json", 
            "index.html",
            "docs/78b245/f0e90c/dev-notes.md"
        ]
        
        missing_files = []
        for file_path in required_files:
            full_path = project_root / file_path
            if not full_path.exists():
                missing_files.append(file_path)
        
        assert len(missing_files) == 0, f"缺少必要文件: {missing_files}"
        
        # 检查docs目录结构
        docs_dir = project_root / "docs"
        assert docs_dir.exists() and docs_dir.is_dir(), "docs目录应存在"

    def test_server_file_syntax_validity(self):
        """测试server.js文件的基本语法有效性"""
        server_file = project_root / "server.js"
        assert server_file.exists(), "server.js文件不存在"
        
        content = server_file.read_text(encoding='utf-8')
        
        # 检查基本JavaScript语法元素
        js_patterns = [
            r'require\s*\(',  # CommonJS require
            r'import\s+.*from',  # ES6 import
            r'function\s+\w+',  # 函数定义
            r'const\s+\w+',  # const声明
            r'let\s+\w+',  # let声明
            r'var\s+\w+'  # var声明
        ]
        
        found_patterns = [pattern for pattern in js_patterns 
                         if re.search(pattern, content)]
        assert len(found_patterns) >= 1, "server.js应包含有效的JavaScript语法结构"
        
        # 检查括号匹配（简单检查）
        open_braces = content.count('{')
        close_braces = content.count('}')
        open_parens = content.count('(')
        close_parens = content.count(')')
        
        assert abs(open_braces - close_braces) <= 2, "大括号应基本匹配"
        assert abs(open_parens - close_parens) <= 2, "小括号应基本匹配"