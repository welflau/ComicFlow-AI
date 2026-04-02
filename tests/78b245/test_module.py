import pytest
from pathlib import Path
import re

class TestFrontendCollaborationIntegration:
    
    def test_index_html_file_exists(self):
        """测试前端主页文件是否存在"""
        frontend_dir = Path("frontend")
        index_file = frontend_dir / "index.html"
        assert index_file.exists(), f"前端主页文件 {index_file} 不存在"
        assert index_file.is_file(), f"{index_file} 不是一个有效的文件"
    
    def test_index_html_contains_collaboration_elements(self):
        """测试HTML文件是否包含实时协作相关的关键元素"""
        frontend_dir = Path("frontend")
        index_file = frontend_dir / "index.html"
        
        # 确保文件存在
        assert index_file.exists(), f"HTML文件 {index_file} 不存在"
        
        # 读取HTML内容
        content = index_file.read_text(encoding='utf-8')
        
        # 检查基本HTML结构
        assert '<html' in content.lower(), "HTML文件缺少html标签"
        assert '<head>' in content.lower() or '<head ' in content.lower(), "HTML文件缺少head标签"
        assert '<body>' in content.lower() or '<body ' in content.lower(), "HTML文件缺少body标签"
        
        # 检查实时协作相关元素
        collaboration_keywords = [
            'websocket', 'socket', 'collaboration', 'realtime', 'real-time',
            'collaborative', 'editor', 'chat', 'users', 'online'
        ]
        
        content_lower = content.lower()
        found_keywords = [keyword for keyword in collaboration_keywords if keyword in content_lower]
        assert len(found_keywords) > 0, f"HTML文件中未找到实时协作相关关键词，期望包含: {collaboration_keywords}"
    
    def test_index_html_has_valid_structure(self):
        """测试HTML文件是否具有有效的文档结构和必要的前端协作功能元素"""
        frontend_dir = Path("frontend")
        index_file = frontend_dir / "index.html"
        
        content = index_file.read_text(encoding='utf-8')
        
        # 检查是否包含JavaScript相关内容（实时协作通常需要JS）
        js_indicators = ['<script', 'javascript', '.js', 'function', 'var ', 'let ', 'const ']
        has_js = any(indicator in content.lower() for indicator in js_indicators)
        assert has_js, "HTML文件中未找到JavaScript相关内容，实时协作功能可能无法正常工作"
        
        # 检查是否有用户界面元素
        ui_elements = ['<div', '<input', '<button', '<textarea', '<canvas', 'id=', 'class=']
        found_ui_elements = [element for element in ui_elements if element in content.lower()]
        assert len(found_ui_elements) >= 2, f"HTML文件中UI元素不足，找到: {found_ui_elements}"
        
        # 检查是否有CSS样式（提升用户体验）
        has_css = '<style' in content.lower() or '.css' in content.lower() or 'stylesheet' in content.lower()
        assert has_css, "HTML文件中未找到CSS样式相关内容"
    
    def test_dev_notes_documentation_exists(self):
        """测试开发文档是否存在并包含有用信息"""
        docs_path = Path("docs/78b245/98354d/dev-notes.md")
        
        assert docs_path.exists(), f"开发文档 {docs_path} 不存在"
        assert docs_path.is_file(), f"{docs_path} 不是一个有效的文件"
        
        # 检查文档内容
        content = docs_path.read_text(encoding='utf-8')
        assert len(content.strip()) > 0, "开发文档内容为空"
        
        # 检查是否包含开发相关信息
        dev_keywords = ['开发', '协作', '实时', '前端', 'frontend', 'development', 'collaboration', 'realtime']
        content_lower = content.lower()
        found_dev_keywords = [keyword for keyword in dev_keywords if keyword in content_lower]
        assert len(found_dev_keywords) > 0, f"开发文档中未找到相关开发信息，期望包含: {dev_keywords}"
    
    def test_frontend_directory_structure(self):
        """测试前端目录结构是否合理"""
        frontend_dir = Path("frontend")
        
        assert frontend_dir.exists(), "frontend目录不存在"
        assert frontend_dir.is_dir(), "frontend不是一个目录"
        
        # 检查目录中是否有文件
        files_in_frontend = list(frontend_dir.iterdir())
        assert len(files_in_frontend) > 0, "frontend目录为空"
        
        # 确保index.html在frontend目录中
        index_file = frontend_dir / "index.html"
        assert index_file in files_in_frontend, "index.html文件不在frontend目录中"