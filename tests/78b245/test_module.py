import pytest
from pathlib import Path
from bs4 import BeautifulSoup

class TestFrontendNodeSystem:
    
    def test_index_html_file_exists(self):
        """测试 index.html 文件是否存在"""
        frontend_dir = Path(__file__).parent / "frontend"
        index_file = frontend_dir / "index.html"
        assert index_file.exists(), "index.html 文件不存在"
        assert index_file.is_file(), "index.html 不是一个有效的文件"
    
    def test_index_html_contains_essential_elements(self):
        """测试 index.html 文件包含必要的HTML元素"""
        frontend_dir = Path(__file__).parent / "frontend"
        index_file = frontend_dir / "index.html"
        
        with open(index_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        soup = BeautifulSoup(content, 'html.parser')
        
        # 检查基本HTML结构
        assert soup.find('html') is not None, "缺少 html 标签"
        assert soup.find('head') is not None, "缺少 head 标签"
        assert soup.find('body') is not None, "缺少 body 标签"
        
        # 检查节点系统相关元素
        title = soup.find('title')
        assert title is not None, "缺少 title 标签"
        
        # 检查是否包含节点系统相关的关键词
        page_text = content.lower()
        node_keywords = ['node', 'system', '节点', '系统']
        has_node_keyword = any(keyword in page_text for keyword in node_keywords)
        assert has_node_keyword, "页面内容中缺少节点系统相关关键词"
    
    def test_dev_notes_markdown_file_exists_and_valid(self):
        """测试开发文档 markdown 文件存在且包含有效内容"""
        docs_dir = Path(__file__).parent / "docs" / "78b245" / "b2cdd4"
        dev_notes_file = docs_dir / "dev-notes.md"
        
        assert dev_notes_file.exists(), "dev-notes.md 文件不存在"
        assert dev_notes_file.is_file(), "dev-notes.md 不是一个有效的文件"
        
        with open(dev_notes_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 检查文件不为空
        assert len(content.strip()) > 0, "dev-notes.md 文件内容为空"
        
        # 检查是否包含 markdown 格式的标题
        lines = content.split('\n')
        has_markdown_header = any(line.strip().startswith('#') for line in lines)
        assert has_markdown_header, "dev-notes.md 缺少 markdown 格式的标题"
        
        # 检查是否包含开发相关关键词
        content_lower = content.lower()
        dev_keywords = ['dev', 'development', '开发', 'note', '笔记', 'todo', 'feature']
        has_dev_keyword = any(keyword in content_lower for keyword in dev_keywords)
        assert has_dev_keyword, "开发文档中缺少开发相关关键词"
    
    def test_index_html_has_valid_structure_for_node_system(self):
        """测试 index.html 具有适合节点系统的有效结构"""
        frontend_dir = Path(__file__).parent / "frontend"
        index_file = frontend_dir / "index.html"
        
        with open(index_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        soup = BeautifulSoup(content, 'html.parser')
        
        # 检查是否有容器元素用于节点渲染
        container_selectors = ['#app', '.app', '#container', '.container', '#node-container', '.node-system']
        has_container = any(soup.select(selector) for selector in container_selectors)
        assert has_container, "缺少用于节点系统的容器元素"
        
        # 检查是否引入了必要的脚本或样式
        scripts = soup.find_all('script')
        styles = soup.find_all(['style', 'link'])
        
        assert len(scripts) > 0 or len(styles) > 0, "缺少必要的脚本或样式文件引用"
    
    def test_project_directory_structure(self):
        """测试项目目录结构的完整性"""
        project_root = Path(__file__).parent
        
        # 检查 frontend 目录存在
        frontend_dir = project_root / "frontend"
        assert frontend_dir.exists() and frontend_dir.is_dir(), "frontend 目录不存在"
        
        # 检查 docs 目录结构存在
        docs_dir = project_root / "docs" / "78b245" / "b2cdd4"
        assert docs_dir.exists() and docs_dir.is_dir(), "docs 目录结构不完整"
        
        # 检查关键文件存在
        required_files = [
            frontend_dir / "index.html",
            docs_dir / "dev-notes.md"
        ]
        
        for file_path in required_files:
            assert file_path.exists(), f"必需文件 {file_path} 不存在"