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
            
            # 检查常见的部署配置文件
            common_deploy_files = [
                "requirements.txt",
                "Dockerfile",
                "docker-compose.yml",
                "config.py",
                "__init__.py"
            ]
            
            existing_files = []
            for file_name in common_deploy_files:
                file_path = deploy_module_path / file_name
                if file_path.exists():
                    existing_files.append(file_name)
            
            # 至少应该存在一个部署相关文件
            assert len(existing_files) > 0, f"deploy目录中未找到常见的部署配置文件: {common_deploy_files}"
        else:
            # 如果deploy目录不存在，检查是否有deploy.py文件
            deploy_file_path = Path("deploy.py")
            assert deploy_file_path.exists(), "既没有deploy目录也没有deploy.py文件"
    
    def test_documentation_content_validity(self):
        """测试文档内容的有效性和完整性"""
        docs_base_path = Path("docs")
        
        if docs_base_path.exists():
            # 检查文档目录结构
            target_doc_path = docs_base_path / "78b245" / "b949fa" / "dev-notes.md"
            
            if target_doc_path.exists():
                # 读取文档内容并检查关键信息
                content = target_doc_path.read_text(encoding='utf-8')
                
                # 检查文档不为空
                assert len(content.strip()) > 0, "开发笔记文档内容为空"
                
                # 检查是否包含常见的开发文档关键词
                dev_keywords = [
                    "部署", "配置", "环境", "安装", "运行",
                    "deploy", "config", "setup", "install", "run"
                ]
                
                found_keywords = []
                content_lower = content.lower()
                for keyword in dev_keywords:
                    if keyword.lower() in content_lower:
                        found_keywords.append(keyword)
                
                assert len(found_keywords) > 0, f"文档中未找到开发相关关键词: {dev_keywords}"
            else:
                # 如果目标文档不存在，检查docs目录下是否有其他文档文件
                doc_files = list(docs_base_path.rglob("*.md"))
                doc_files.extend(list(docs_base_path.rglob("*.txt")))
                doc_files.extend(list(docs_base_path.rglob("*.rst")))
                
                assert len(doc_files) > 0, "docs目录中未找到任何文档文件"
        else:
            # 如果docs目录不存在，检查项目根目录下的README文件
            readme_files = [
                Path("README.md"),
                Path("README.txt"),
                Path("README.rst"),
                Path("readme.md")
            ]
            
            existing_readme = [f for f in readme_files if f.exists()]
            assert len(existing_readme) > 0, "未找到项目文档文件（README或docs目录）"

    def test_deploy_module_importability(self):
        """测试部署模块是否可以正确导入"""
        try:
            # 尝试导入deploy模块
            if Path("deploy/__init__.py").exists():
                import deploy
                assert hasattr(deploy, '__name__'), "deploy模块导入失败"
            elif Path("deploy.py").exists():
                import deploy
                assert hasattr(deploy, '__name__'), "deploy.py文件导入失败"
            else:
                # 如果没有deploy模块，跳过此测试
                pytest.skip("未找到可导入的deploy模块")
        except ImportError as e:
            pytest.fail(f"导入deploy模块失败: {e}")

    def test_project_configuration_files(self):
        """测试项目配置文件的存在性和有效性"""
        config_files = [
            "setup.py",
            "pyproject.toml",
            "requirements.txt",
            "Pipfile",
            "environment.yml",
            "config.ini",
            "config.yaml",
            "config.json"
        ]
        
        existing_configs = []
        for config_file in config_files:
            config_path = Path(config_file)
            if config_path.exists():
                existing_configs.append(config_file)
                
                # 检查文件不为空
                if config_path.stat().st_size > 0:
                    assert True, f"配置文件 {config_file} 存在且不为空"
        
        # 至少应该存在一个配置文件
        assert len(existing_configs) > 0, f"未找到任何项目配置文件: {config_files}"