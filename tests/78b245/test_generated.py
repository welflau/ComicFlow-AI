import pytest
from pathlib import Path
import os
import sys

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

class TestDeployConfiguration:
    """部署配置与文档测试类"""
    
    def test_dev_notes_file_exists(self):
        """测试开发笔记文档文件是否存在"""
        dev_notes_path = Path("docs/78b245/b949fa/dev-notes.md")
        assert dev_notes_path.exists(), f"开发笔记文档文件不存在: {dev_notes_path}"
        assert dev_notes_path.is_file(), f"路径不是文件: {dev_notes_path}"
    
    def test_deploy_module_structure(self):
        """测试部署模块目录结构是否完整"""
        deploy_module_path = Path("deploy")
        
        # 检查deploy模块目录是否存在
        if deploy_module_path.exists():
            assert deploy_module_path.is_dir(), "deploy应该是一个目录"
        
        # 检查文档目录结构
        docs_path = Path("docs")
        assert docs_path.exists(), "docs目录应该存在"
        
        # 检查特定的文档子目录
        specific_doc_path = Path("docs/78b245/b949fa")
        assert specific_doc_path.exists(), f"特定文档目录应该存在: {specific_doc_path}"
    
    def test_dev_notes_content_validity(self):
        """测试开发笔记文档内容的有效性"""
        dev_notes_path = Path("docs/78b245/b949fa/dev-notes.md")
        
        if dev_notes_path.exists():
            content = dev_notes_path.read_text(encoding='utf-8')
            
            # 检查文件不为空
            assert len(content.strip()) > 0, "开发笔记文档不应为空"
            
            # 检查是否包含常见的开发文档关键词
            common_keywords = ['部署', 'deploy', '配置', 'config', '环境', 'environment', '文档', 'documentation']
            has_relevant_content = any(keyword in content.lower() for keyword in common_keywords)
            
            # 如果文档很短，可能是占位符，不强制要求关键词
            if len(content.strip()) > 50:
                assert has_relevant_content, "开发笔记应包含相关的部署或配置内容"
    
    def test_project_configuration_files(self):
        """测试项目配置文件是否存在"""
        possible_config_files = [
            Path("requirements.txt"),
            Path("setup.py"),
            Path("pyproject.toml"),
            Path("Dockerfile"),
            Path("docker-compose.yml"),
            Path("config.py"),
            Path("settings.py")
        ]
        
        existing_configs = [f for f in possible_config_files if f.exists()]
        
        # 至少应该有一个配置文件存在
        assert len(existing_configs) > 0, "项目应该包含至少一个配置文件"
    
    def test_deploy_directory_permissions(self):
        """测试部署相关目录的访问权限"""
        docs_path = Path("docs")
        
        if docs_path.exists():
            # 检查目录是否可读
            assert os.access(docs_path, os.R_OK), "docs目录应该可读"
            
            # 检查开发笔记文件是否可读
            dev_notes_path = Path("docs/78b245/b949fa/dev-notes.md")
            if dev_notes_path.exists():
                assert os.access(dev_notes_path, os.R_OK), "开发笔记文件应该可读"