import pytest
from pathlib import Path
import os

class TestFrontendWorkflowInterface:
    
    def test_feature_497_js_file_exists(self):
        """测试前端工作流执行界面的核心JavaScript文件是否存在"""
        project_root = Path(__file__).parent.parent
        feature_file = project_root / "frontend" / "src" / "feature_497.js"
        assert feature_file.exists(), f"核心功能文件 {feature_file} 不存在"
        assert feature_file.is_file(), f"{feature_file} 不是一个有效的文件"
    
    def test_feature_497_js_contains_workflow_elements(self):
        """测试JavaScript文件包含工作流执行界面的关键代码元素"""
        project_root = Path(__file__).parent.parent
        feature_file = project_root / "frontend" / "src" / "feature_497.js"
        
        if feature_file.exists():
            content = feature_file.read_text(encoding='utf-8')
            
            # 检查工作流相关的关键词
            workflow_keywords = [
                'workflow', 'execute', 'process', 'task', 
                'function', 'class', 'const', 'let'
            ]
            
            found_keywords = [keyword for keyword in workflow_keywords if keyword in content.lower()]
            assert len(found_keywords) >= 3, f"JavaScript文件应包含至少3个工作流相关关键词，实际找到: {found_keywords}"
            
            # 检查文件不为空
            assert len(content.strip()) > 0, "JavaScript文件不应为空"
        else:
            pytest.skip("JavaScript文件不存在，跳过内容检查")
    
    def test_dev_notes_documentation_exists(self):
        """测试开发文档是否存在并包含有效内容"""
        project_root = Path(__file__).parent.parent
        doc_file = project_root / "frontend" / "docs" / "78b245" / "33bf13" / "dev-notes.md"
        
        assert doc_file.exists(), f"开发文档 {doc_file} 不存在"
        assert doc_file.is_file(), f"{doc_file} 不是一个有效的文件"
        
        content = doc_file.read_text(encoding='utf-8')
        assert len(content.strip()) > 0, "开发文档不应为空"
        
        # 检查文档是否包含常见的开发文档关键词
        doc_keywords = ['#', 'feature', 'workflow', 'interface', 'frontend']
        found_keywords = [keyword for keyword in doc_keywords if keyword.lower() in content.lower()]
        assert len(found_keywords) >= 2, f"开发文档应包含至少2个相关关键词，实际找到: {found_keywords}"
    
    def test_frontend_directory_structure(self):
        """测试前端项目目录结构是否正确"""
        project_root = Path(__file__).parent.parent
        frontend_dir = project_root / "frontend"
        
        assert frontend_dir.exists(), "frontend目录不存在"
        assert frontend_dir.is_dir(), "frontend应该是一个目录"
        
        # 检查src目录
        src_dir = frontend_dir / "src"
        assert src_dir.exists(), "src目录不存在"
        assert src_dir.is_dir(), "src应该是一个目录"
        
        # 检查docs目录
        docs_dir = frontend_dir / "docs"
        assert docs_dir.exists(), "docs目录不存在"
        assert docs_dir.is_dir(), "docs应该是一个目录"
    
    def test_html_interface_elements(self):
        """测试HTML界面文件是否包含工作流执行的关键元素"""
        project_root = Path(__file__).parent.parent
        frontend_dir = project_root / "frontend"
        
        # 查找HTML文件
        html_files = list(frontend_dir.rglob("*.html"))
        
        if html_files:
            html_file = html_files[0]  # 测试第一个找到的HTML文件
            content = html_file.read_text(encoding='utf-8')
            
            # 检查HTML基本结构
            html_elements = ['<html', '<head', '<body', '</html>']
            found_elements = [elem for elem in html_elements if elem.lower() in content.lower()]
            assert len(found_elements) >= 3, f"HTML文件应包含基本HTML结构元素，找到: {found_elements}"
            
            # 检查工作流界面相关元素
            interface_elements = ['button', 'div', 'form', 'input', 'script']
            found_interface = [elem for elem in interface_elements if elem.lower() in content.lower()]
            assert len(found_interface) >= 2, f"HTML文件应包含界面交互元素，找到: {found_interface}"
        else:
            pytest.skip("未找到HTML文件，跳过HTML元素检查")