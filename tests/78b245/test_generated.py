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
                'workflow',
                'execute',
                'function',
                'addEventListener',
                'querySelector'
            ]
            
            found_keywords = []
            for keyword in workflow_keywords:
                if keyword in content.lower():
                    found_keywords.append(keyword)
            
            assert len(found_keywords) >= 2, f"JavaScript文件应包含工作流相关关键词，找到: {found_keywords}"
        else:
            pytest.skip("JavaScript文件不存在，跳过内容检查")
    
    def test_dev_notes_documentation_exists(self):
        """测试开发文档是否存在并包含有效内容"""
        project_root = Path(__file__).parent.parent
        docs_file = project_root / "frontend" / "docs" / "78b245" / "33bf13" / "dev-notes.md"
        
        assert docs_file.exists(), f"开发文档 {docs_file} 不存在"
        assert docs_file.is_file(), f"{docs_file} 不是一个有效的文件"
        
        content = docs_file.read_text(encoding='utf-8')
        assert len(content.strip()) > 0, "开发文档不能为空"
        
        # 检查是否包含常见的文档标记
        doc_indicators = ['#', '##', '###', '-', '*', 'feature', 'workflow', 'interface']
        has_doc_structure = any(indicator in content for indicator in doc_indicators)
        assert has_doc_structure, "开发文档应包含基本的文档结构标记"
    
    def test_frontend_directory_structure(self):
        """测试前端项目目录结构的完整性"""
        project_root = Path(__file__).parent.parent
        frontend_dir = project_root / "frontend"
        
        assert frontend_dir.exists(), "frontend目录必须存在"
        assert frontend_dir.is_dir(), "frontend必须是一个目录"
        
        # 检查关键目录结构
        src_dir = frontend_dir / "src"
        docs_dir = frontend_dir / "docs"
        
        assert src_dir.exists() or docs_dir.exists(), "至少应存在src或docs目录之一"
        
        if src_dir.exists():
            js_files = list(src_dir.glob("*.js"))
            assert len(js_files) > 0, "src目录应包含至少一个JavaScript文件"
    
    def test_file_permissions_and_accessibility(self):
        """测试文件权限和可访问性"""
        project_root = Path(__file__).parent.parent
        files_to_check = [
            project_root / "frontend" / "src" / "feature_497.js",
            project_root / "frontend" / "docs" / "78b245" / "33bf13" / "dev-notes.md"
        ]
        
        accessible_files = []
        for file_path in files_to_check:
            if file_path.exists():
                assert os.access(file_path, os.R_OK), f"文件 {file_path} 应该是可读的"
                accessible_files.append(file_path)
        
        assert len(accessible_files) > 0, "至少应有一个项目文件存在且可访问"