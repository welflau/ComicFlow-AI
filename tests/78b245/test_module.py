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
        """测试部署模块的目录结构是否正确"""
        deploy_module_path = Path("deploy")
        
        # 检查deploy模块目录是否存在
        if deploy_module_path.exists():
            assert deploy_module_path.is_dir(), "deploy应该是一个目录"
            
            # 检查是否包含Python模块文件
            python_files = list(deploy_module_path.glob("*.py"))
            init_file = deploy_module_path / "__init__.py"
            
            # 至少应该有__init__.py文件使其成为Python包
            assert init_file.exists() or len(python_files) > 0, "deploy模块应包含Python文件"
        else:
            # 如果deploy目录不存在，检查是否有deploy.py文件
            deploy_file = Path("deploy.py")
            assert deploy_file.exists(), "deploy模块或deploy.py文件应该存在"
    
    def test_documentation_content_validity(self):
        """测试文档内容是否包含部署相关的关键信息"""
        docs_dir = Path("docs")
        
        # 查找所有markdown文档文件
        md_files = []
        if docs_dir.exists():
            md_files = list(docs_dir.rglob("*.md"))
        
        # 检查dev-notes.md文件内容
        dev_notes_path = Path("docs/78b245/b949fa/dev-notes.md")
        if dev_notes_path.exists():
            content = dev_notes_path.read_text(encoding='utf-8')
            
            # 检查文档是否包含部署相关关键词
            deploy_keywords = ['部署', 'deploy', '配置', 'config', '环境', 'environment']
            has_deploy_content = any(keyword in content.lower() for keyword in deploy_keywords)
            
            assert len(content.strip()) > 0, "开发笔记文档不应为空"
            assert has_deploy_content, "文档应包含部署相关内容"
        else:
            # 如果指定文件不存在，检查是否有其他相关文档
            assert len(md_files) > 0, "项目应包含文档文件"
    
    def test_deploy_configuration_files(self):
        """测试部署配置文件是否存在且格式正确"""
        config_files = [
            "requirements.txt",
            "setup.py", 
            "pyproject.toml",
            "Dockerfile",
            "docker-compose.yml",
            ".env.example"
        ]
        
        existing_config_files = []
        for config_file in config_files:
            config_path = Path(config_file)
            if config_path.exists():
                existing_config_files.append(config_file)
                assert config_path.is_file(), f"{config_file}应该是文件"
                
                # 检查文件不为空
                if config_path.suffix in ['.txt', '.yml', '.yaml', '.toml']:
                    content = config_path.read_text(encoding='utf-8')
                    assert len(content.strip()) > 0, f"{config_file}不应为空"
        
        # 至少应该有一个配置文件存在
        assert len(existing_config_files) > 0, "项目应包含至少一个部署配置文件"
    
    def test_project_structure_integrity(self):
        """测试项目整体结构的完整性"""
        project_root = Path(".")
        
        # 检查基本的项目文件
        essential_items = []
        
        # 检查是否有Python文件
        py_files = list(project_root.glob("*.py"))
        if len(py_files) > 0:
            essential_items.extend(py_files)
        
        # 检查是否有子目录
        subdirs = [p for p in project_root.iterdir() if p.is_dir() and not p.name.startswith('.')]
        essential_items.extend(subdirs)
        
        # 检查docs目录结构
        docs_path = Path("docs")
        if docs_path.exists():
            assert docs_path.is_dir(), "docs应该是目录"
            
            # 检查docs下的子目录结构
            subdir_78b245 = docs_path / "78b245"
            if subdir_78b245.exists():
                assert subdir_78b245.is_dir(), "78b245应该是目录"
                
                subdir_b949fa = subdir_78b245 / "b949fa"
                if subdir_b949fa.exists():
                    assert subdir_b949fa.is_dir(), "b949fa应该是目录"
        
        assert len(essential_items) > 0, "项目应包含基本的文件或目录结构"