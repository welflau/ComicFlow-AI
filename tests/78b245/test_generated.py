import pytest
from pathlib import Path
from bs4 import BeautifulSoup
import os

class TestFrontendCollaboration:
    
    def test_index_html_file_exists(self):
        """测试前端主页文件是否存在"""
        index_path = Path("frontend") / "index.html"
        assert index_path.exists(), f"前端主页文件 {index_path} 不存在"
        assert index_path.is_file(), f"{index_path} 不是一个有效的文件"
    
    def test_index_html_contains_collaboration_elements(self):
        """测试HTML文件是否包含实时协作相关的关键元素"""
        index_path = Path("frontend") / "index.html"
        
        # 确保文件存在
        if not index_path.exists():
            pytest.skip(f"HTML文件 {index_path} 不存在，跳过内容测试")
        
        with open(index_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # 检查基本HTML结构
        assert soup.find('html'), "HTML文件缺少html标签"
        assert soup.find('head'), "HTML文件缺少head标签"
        assert soup.find('body'), "HTML文件缺少body标签"
        
        # 检查实时协作相关元素（常见的协作功能元素）
        collaboration_indicators = [
            'websocket', 'socket', 'collaboration', 'realtime', 'real-time',
            'collaborative', 'editor', 'chat', 'cursor', 'user', 'online'
        ]
        
        html_lower = html_content.lower()
        found_indicators = [indicator for indicator in collaboration_indicators if indicator in html_lower]
        
        assert len(found_indicators) > 0, f"HTML文件中未找到实时协作相关关键词，检查的关键词: {collaboration_indicators}"
    
    def test_dev_notes_documentation_exists(self):
        """测试开发文档是否存在并包含有效内容"""
        docs_path = Path("docs") / "78b245" / "98354d" / "dev-notes.md"
        
        assert docs_path.exists(), f"开发文档 {docs_path} 不存在"
        assert docs_path.is_file(), f"{docs_path} 不是一个有效的文件"
        
        with open(docs_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 检查文档不为空
        assert len(content.strip()) > 0, "开发文档内容为空"
        
        # 检查是否包含开发相关关键词
        dev_keywords = ['开发', 'development', 'api', 'function', '功能', '实现', 'implementation']
        content_lower = content.lower()
        found_keywords = [keyword for keyword in dev_keywords if keyword in content_lower]
        
        assert len(found_keywords) > 0, f"开发文档中未找到开发相关关键词，检查的关键词: {dev_keywords}"
    
    def test_html_has_valid_structure_for_collaboration(self):
        """测试HTML文件是否具有支持实时协作的有效结构"""
        index_path = Path("frontend") / "index.html"
        
        if not index_path.exists():
            pytest.skip(f"HTML文件 {index_path} 不存在，跳过结构测试")
        
        with open(index_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # 检查是否有JavaScript引用（实时协作通常需要JS）
        scripts = soup.find_all('script')
        assert len(scripts) > 0 or 'script' in html_content.lower(), "HTML文件中未找到JavaScript引用，实时协作功能可能无法正常工作"
        
        # 检查是否有容器元素（用于显示协作内容）
        container_elements = soup.find_all(['div', 'section', 'main', 'article'])
        assert len(container_elements) > 0, "HTML文件中未找到容器元素，缺少显示协作内容的区域"
        
        # 检查是否有表单或输入元素（协作通常需要用户输入）
        interactive_elements = soup.find_all(['input', 'textarea', 'button', 'form'])
        has_interactive = len(interactive_elements) > 0
        
        # 如果没有交互元素，至少应该有用于动态添加内容的容器
        if not has_interactive:
            divs_with_id = soup.find_all('div', id=True)
            divs_with_class = soup.find_all('div', class_=True)
            assert len(divs_with_id) > 0 or len(divs_with_class) > 0, "HTML文件缺少交互元素和可标识的容器，无法支持动态协作功能"
    
    def test_project_structure_completeness(self):
        """测试项目结构的完整性"""
        frontend_dir = Path("frontend")
        docs_dir = Path("docs")
        
        # 检查主要目录存在
        assert frontend_dir.exists(), "frontend目录不存在"
        
        # 检查核心文件存在
        index_file = frontend_dir / "index.html"
        dev_notes_file = docs_dir / "78b245" / "98354d" / "dev-notes.md"
        
        missing_files = []
        if not index_file.exists():
            missing_files.append(str(index_file))
        if not dev_notes_file.exists():
            missing_files.append(str(dev_notes_file))
        
        assert len(missing_files) == 0, f"以下核心文件缺失: {missing_files}"