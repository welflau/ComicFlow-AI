import pytest
from pathlib import Path
from bs4 import BeautifulSoup
import os

class TestFrontendCollaboration:
    
    def test_index_html_file_exists(self):
        """测试前端主页HTML文件是否存在"""
        project_root = Path(__file__).parent
        index_file = project_root / "frontend" / "index.html"
        assert index_file.exists(), f"index.html文件不存在: {index_file}"
        assert index_file.is_file(), f"index.html不是一个有效文件: {index_file}"
    
    def test_index_html_contains_collaboration_elements(self):
        """测试HTML文件是否包含实时协作相关的关键元素"""
        project_root = Path(__file__).parent
        index_file = project_root / "frontend" / "index.html"
        
        with open(index_file, 'r', encoding='utf-8') as f:
            content = f.read()
            soup = BeautifulSoup(content, 'html.parser')
        
        # 检查是否包含基本HTML结构
        assert soup.find('html') is not None, "HTML文件缺少html标签"
        assert soup.find('head') is not None, "HTML文件缺少head标签"
        assert soup.find('body') is not None, "HTML文件缺少body标签"
        
        # 检查是否包含实时协作相关元素
        collaboration_keywords = ['websocket', 'socket', 'collaboration', 'realtime', 'real-time', '协作', '实时']
        content_lower = content.lower()
        
        has_collaboration_element = any(keyword in content_lower for keyword in collaboration_keywords)
        assert has_collaboration_element, "HTML文件中未找到实时协作相关的关键词"
    
    def test_dev_notes_documentation_exists(self):
        """测试开发文档是否存在并包含有效内容"""
        project_root = Path(__file__).parent
        dev_notes_file = project_root / "docs" / "78b245" / "98354d" / "dev-notes.md"
        
        assert dev_notes_file.exists(), f"开发文档不存在: {dev_notes_file}"
        assert dev_notes_file.is_file(), f"dev-notes.md不是一个有效文件: {dev_notes_file}"
        
        # 检查文档内容
        with open(dev_notes_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        assert len(content.strip()) > 0, "开发文档内容为空"
        assert len(content) > 50, "开发文档内容过短，可能不完整"
    
    def test_html_has_valid_structure_for_collaboration(self):
        """测试HTML文件是否具有支持实时协作的有效结构"""
        project_root = Path(__file__).parent
        index_file = project_root / "frontend" / "index.html"
        
        with open(index_file, 'r', encoding='utf-8') as f:
            content = f.read()
            soup = BeautifulSoup(content, 'html.parser')
        
        # 检查是否有JavaScript引用或内联脚本
        scripts = soup.find_all('script')
        assert len(scripts) > 0, "HTML文件中未找到JavaScript脚本，实时协作功能可能无法实现"
        
        # 检查是否有用于协作的容器元素
        potential_containers = soup.find_all(['div', 'section', 'main'])
        assert len(potential_containers) > 0, "HTML文件中未找到可能用于协作内容的容器元素"
        
        # 检查是否有表单或输入元素用于用户交互
        interactive_elements = soup.find_all(['input', 'textarea', 'button', 'form'])
        assert len(interactive_elements) > 0, "HTML文件中未找到用户交互元素，协作功能可能受限"
    
    def test_project_structure_completeness(self):
        """测试项目结构的完整性"""
        project_root = Path(__file__).parent
        
        # 检查frontend目录存在
        frontend_dir = project_root / "frontend"
        assert frontend_dir.exists(), "frontend目录不存在"
        assert frontend_dir.is_dir(), "frontend不是一个目录"
        
        # 检查docs目录结构存在
        docs_dir = project_root / "docs" / "78b245" / "98354d"
        assert docs_dir.exists(), "文档目录结构不完整"
        assert docs_dir.is_dir(), "文档路径不是一个目录"
        
        # 检查关键文件都存在
        required_files = [
            frontend_dir / "index.html",
            docs_dir / "dev-notes.md"
        ]
        
        for file_path in required_files:
            assert file_path.exists(), f"必需文件不存在: {file_path}"