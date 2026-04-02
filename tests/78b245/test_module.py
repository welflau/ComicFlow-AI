import pytest
from pathlib import Path
from bs4 import BeautifulSoup

class TestFrontendCollaboration:
    
    def test_index_html_exists(self):
        """测试前端主页文件是否存在"""
        index_path = Path("frontend/index.html")
        assert index_path.exists(), "index.html 文件不存在"
        assert index_path.is_file(), "index.html 不是一个有效的文件"
    
    def test_index_html_contains_collaboration_elements(self):
        """测试 index.html 是否包含实时协作相关的关键元素"""
        index_path = Path("frontend/index.html")
        assert index_path.exists(), "index.html 文件不存在"
        
        with open(index_path, 'r', encoding='utf-8') as f:
            content = f.read()
            soup = BeautifulSoup(content, 'html.parser')
        
        # 检查是否包含基本的HTML结构
        assert soup.find('html') is not None, "缺少 html 标签"
        assert soup.find('head') is not None, "缺少 head 标签"
        assert soup.find('body') is not None, "缺少 body 标签"
        
        # 检查是否包含实时协作相关元素
        collaboration_keywords = ['websocket', 'socket', 'collaboration', 'realtime', 'real-time', '协作', '实时']
        content_lower = content.lower()
        has_collaboration_keyword = any(keyword in content_lower for keyword in collaboration_keywords)
        assert has_collaboration_keyword, "HTML内容中未找到实时协作相关关键词"
    
    def test_index_html_has_script_tags(self):
        """测试 index.html 是否包含必要的脚本标签用于前端功能"""
        index_path = Path("frontend/index.html")
        assert index_path.exists(), "index.html 文件不存在"
        
        with open(index_path, 'r', encoding='utf-8') as f:
            content = f.read()
            soup = BeautifulSoup(content, 'html.parser')
        
        script_tags = soup.find_all('script')
        assert len(script_tags) > 0, "HTML文件中未找到任何script标签"
        
        # 检查是否有外部脚本引用或内联脚本
        has_external_script = any(script.get('src') for script in script_tags)
        has_inline_script = any(script.string and script.string.strip() for script in script_tags)
        
        assert has_external_script or has_inline_script, "未找到有效的JavaScript代码"
    
    def test_dev_notes_file_exists_and_readable(self):
        """测试开发文档是否存在且可读"""
        dev_notes_path = Path("docs/78b245/98354d/dev-notes.md")
        assert dev_notes_path.exists(), "开发文档 dev-notes.md 不存在"
        assert dev_notes_path.is_file(), "dev-notes.md 不是一个有效的文件"
        
        # 测试文件是否可读且不为空
        with open(dev_notes_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        assert len(content.strip()) > 0, "开发文档内容为空"
        assert content.count('\n') >= 5, "开发文档内容过少，可能不完整"
    
    def test_project_structure_integrity(self):
        """测试项目结构的完整性"""
        frontend_dir = Path("frontend")
        docs_dir = Path("docs/78b245/98354d")
        
        assert frontend_dir.exists(), "frontend 目录不存在"
        assert frontend_dir.is_dir(), "frontend 不是一个目录"
        
        assert docs_dir.exists(), "文档目录不存在"
        assert docs_dir.is_dir(), "docs/78b245/98354d 不是一个目录"
        
        # 检查关键文件
        required_files = [
            Path("frontend/index.html"),
            Path("docs/78b245/98354d/dev-notes.md")
        ]
        
        for file_path in required_files:
            assert file_path.exists(), f"必需文件 {file_path} 不存在"