import pytest
from pathlib import Path
import re

class TestFrontend3DCanvas:
    
    def test_index_html_exists(self):
        """测试index.html文件是否存在"""
        frontend_dir = Path("frontend")
        index_file = frontend_dir / "index.html"
        assert index_file.exists(), f"index.html文件不存在于 {frontend_dir} 目录中"
        assert index_file.is_file(), "index.html应该是一个文件而不是目录"
    
    def test_index_html_contains_canvas_element(self):
        """测试index.html是否包含3D画布相关的关键元素"""
        frontend_dir = Path("frontend")
        index_file = frontend_dir / "index.html"
        
        with open(index_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 检查是否包含canvas元素
        assert '<canvas' in content.lower(), "HTML文件应该包含canvas元素用于3D渲染"
        
        # 检查是否包含3D相关的关键词
        canvas_keywords = ['webgl', 'three.js', '3d', 'canvas', 'gl']
        has_3d_keyword = any(keyword in content.lower() for keyword in canvas_keywords)
        assert has_3d_keyword, f"HTML文件应该包含3D相关关键词: {canvas_keywords}"
    
    def test_index_html_has_valid_structure(self):
        """测试index.html是否具有有效的HTML结构"""
        frontend_dir = Path("frontend")
        index_file = frontend_dir / "index.html"
        
        with open(index_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 检查基本HTML结构
        assert '<!doctype html>' in content.lower() or '<html' in content.lower(), "应该包含HTML文档声明或html标签"
        assert '<head>' in content.lower(), "应该包含head标签"
        assert '<body>' in content.lower(), "应该包含body标签"
        
        # 检查是否有标题
        title_pattern = r'<title[^>]*>.*?</title>'
        assert re.search(title_pattern, content, re.IGNORECASE | re.DOTALL), "应该包含title标签"
    
    def test_dev_notes_file_exists(self):
        """测试开发文档是否存在"""
        docs_path = Path("docs/d2c78b/738284/dev-notes.md")
        assert docs_path.exists(), f"开发文档不存在于 {docs_path}"
        assert docs_path.is_file(), "dev-notes.md应该是一个文件"
        assert docs_path.suffix == '.md', "开发文档应该是markdown格式"
    
    def test_dev_notes_contains_project_info(self):
        """测试开发文档是否包含项目相关信息"""
        docs_path = Path("docs/d2c78b/738284/dev-notes.md")
        
        with open(docs_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 检查是否包含3D画布相关内容
        project_keywords = ['3d', '画布', 'canvas', '组件', 'component']
        has_project_keyword = any(keyword in content.lower() for keyword in project_keywords)
        assert has_project_keyword, f"开发文档应该包含项目相关关键词: {project_keywords}"
        
        # 检查文档长度，确保不是空文件
        assert len(content.strip()) > 0, "开发文档不应该为空"
    
    def test_frontend_directory_structure(self):
        """测试前端目录结构是否合理"""
        frontend_dir = Path("frontend")
        assert frontend_dir.exists(), "frontend目录应该存在"
        assert frontend_dir.is_dir(), "frontend应该是一个目录"
        
        # 检查是否有常见的前端文件
        common_files = ['index.html']
        for file_name in common_files:
            file_path = frontend_dir / file_name
            if file_path.exists():
                assert file_path.is_file(), f"{file_name}应该是一个文件"