import pytest
from pathlib import Path
import re

class TestThreeJSCanvasInfrastructure:
    
    def test_index_html_file_exists(self):
        """测试 index.html 文件是否存在"""
        index_file = Path("frontend/index.html")
        assert index_file.exists(), "index.html 文件不存在"
        assert index_file.is_file(), "index.html 不是一个有效的文件"
    
    def test_index_html_contains_threejs_elements(self):
        """测试 index.html 文件是否包含 Three.js 相关的关键元素"""
        index_file = Path("frontend/index.html")
        assert index_file.exists(), "index.html 文件不存在"
        
        content = index_file.read_text(encoding='utf-8')
        
        # 检查是否包含 Three.js 库引用
        assert "three" in content.lower() or "threejs" in content.lower(), "HTML 文件中未找到 Three.js 相关引用"
        
        # 检查是否包含 canvas 元素或相关容器
        canvas_pattern = r'<canvas|canvas|webgl|renderer'
        assert re.search(canvas_pattern, content, re.IGNORECASE), "HTML 文件中未找到 canvas 或渲染器相关元素"
        
        # 检查基本 HTML 结构
        assert "<html" in content.lower(), "HTML 文件缺少 html 标签"
        assert "<head" in content.lower(), "HTML 文件缺少 head 标签"
        assert "<body" in content.lower(), "HTML 文件缺少 body 标签"
    
    def test_html_has_valid_structure(self):
        """测试 HTML 文件是否具有有效的基本结构和 Three.js 画布所需元素"""
        index_file = Path("frontend/index.html")
        assert index_file.exists(), "index.html 文件不存在"
        
        content = index_file.read_text(encoding='utf-8')
        
        # 检查是否包含脚本标签（用于加载 Three.js 或自定义脚本）
        script_pattern = r'<script.*?>'
        assert re.search(script_pattern, content, re.IGNORECASE), "HTML 文件中未找到 script 标签"
        
        # 检查是否有适合 3D 渲染的容器或配置
        container_patterns = [
            r'id\s*=\s*["\'].*?container.*?["\']',
            r'id\s*=\s*["\'].*?canvas.*?["\']',
            r'id\s*=\s*["\'].*?webgl.*?["\']',
            r'class\s*=\s*["\'].*?canvas.*?["\']'
        ]
        
        has_container = any(re.search(pattern, content, re.IGNORECASE) for pattern in container_patterns)
        assert has_container, "HTML 文件中未找到适合 Three.js 渲染的容器元素"
    
    def test_dev_notes_file_exists_and_has_content(self):
        """测试开发文档文件是否存在并包含有意义的内容"""
        dev_notes_file = Path("docs/78b245/91c481/dev-notes.md")
        assert dev_notes_file.exists(), "开发文档文件不存在"
        assert dev_notes_file.is_file(), "开发文档不是一个有效的文件"
        
        content = dev_notes_file.read_text(encoding='utf-8')
        assert len(content.strip()) > 0, "开发文档文件为空"
        assert len(content.strip()) > 50, "开发文档内容过少，可能不完整"
    
    def test_project_structure_completeness(self):
        """测试项目结构的完整性，确保关键文件都存在"""
        frontend_dir = Path("frontend")
        docs_dir = Path("docs")
        
        assert frontend_dir.exists(), "frontend 目录不存在"
        assert frontend_dir.is_dir(), "frontend 不是一个目录"
        
        assert docs_dir.exists(), "docs 目录不存在"
        assert docs_dir.is_dir(), "docs 不是一个目录"
        
        # 检查核心文件
        required_files = [
            Path("frontend/index.html"),
            Path("docs/78b245/91c481/dev-notes.md")
        ]
        
        for file_path in required_files:
            assert file_path.exists(), f"必需的文件 {file_path} 不存在"