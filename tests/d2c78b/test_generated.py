import pytest
from pathlib import Path
import os
import sys
import importlib.util

class TestDeployConfiguration:
    """多环境部署配置测试类"""
    
    @pytest.fixture
    def project_root(self):
        """获取项目根目录"""
        return Path(__file__).parent.parent
    
    @pytest.fixture
    def deploy_module_path(self, project_root):
        """获取deploy模块路径"""
        return project_root / "deploy"
    
    def test_deploy_config_files_exist(self, deploy_module_path):
        """测试部署配置文件是否存在"""
        # 检查常见的部署配置文件
        config_files = [
            "config.py",
            "settings.py", 
            "__init__.py",
            "requirements.txt"
        ]
        
        for config_file in config_files:
            file_path = deploy_module_path / config_file
            if file_path.exists():
                assert file_path.is_file(), f"{config_file} 应该是一个文件"
                break
        else:
            # 如果没有找到任何配置文件，检查是否有其他配置文件
            config_extensions = ['.py', '.yaml', '.yml', '.json', '.ini']
            found_configs = []
            for ext in config_extensions:
                found_configs.extend(list(deploy_module_path.glob(f"*{ext}")))
            
            assert len(found_configs) > 0, "deploy模块中应该至少包含一个配置文件"
    
    def test_deploy_module_importable(self, deploy_module_path):
        """测试deploy模块是否可以正确导入"""
        # 将deploy模块路径添加到sys.path
        if str(deploy_module_path.parent) not in sys.path:
            sys.path.insert(0, str(deploy_module_path.parent))
        
        try:
            # 尝试导入deploy模块
            if (deploy_module_path / "__init__.py").exists():
                import deploy
                assert hasattr(deploy, '__name__'), "deploy模块应该有__name__属性"
            else:
                # 如果没有__init__.py，尝试导入具体的配置文件
                config_files = list(deploy_module_path.glob("*.py"))
                assert len(config_files) > 0, "deploy目录中应该包含Python配置文件"
                
                for config_file in config_files:
                    if config_file.name != "__pycache__":
                        spec = importlib.util.spec_from_file_location(
                            config_file.stem, config_file
                        )
                        if spec and spec.loader:
                            module = importlib.util.module_from_spec(spec)
                            spec.loader.exec_module(module)
                            assert module is not None, f"{config_file.name} 模块应该可以正确导入"
                            break
        except ImportError as e:
            pytest.fail(f"导入deploy模块失败: {e}")
    
    def test_environment_configuration_structure(self, deploy_module_path):
        """测试多环境配置结构是否正确"""
        # 检查是否存在不同环境的配置
        environment_indicators = [
            "dev", "development", "test", "testing", 
            "prod", "production", "staging"
        ]
        
        found_env_configs = []
        
        # 检查文件名中包含环境标识的配置文件
        for env in environment_indicators:
            env_files = list(deploy_module_path.glob(f"*{env}*"))
            found_env_configs.extend(env_files)
        
        # 检查是否有环境相关的目录
        for item in deploy_module_path.iterdir():
            if item.is_dir() and any(env in item.name.lower() for env in environment_indicators):
                found_env_configs.append(item)
        
        # 如果没有找到明确的环境配置，检查是否有通用配置文件
        if not found_env_configs:
            config_files = list(deploy_module_path.glob("*.py")) + list(deploy_module_path.glob("*.yaml")) + list(deploy_module_path.glob("*.json"))
            assert len(config_files) > 0, "应该至少包含一个配置文件用于多环境部署"
            
            # 检查配置文件内容是否包含环境相关配置
            for config_file in config_files:
                if config_file.suffix == '.py':
                    try:
                        content = config_file.read_text(encoding='utf-8')
                        env_keywords = ['environment', 'env', 'config', 'settings']
                        has_env_config = any(keyword.upper() in content.upper() for keyword in env_keywords)
                        if has_env_config:
                            found_env_configs.append(config_file)
                    except Exception:
                        continue
        
        assert len(found_env_configs) > 0, "多环境部署配置应该包含环境相关的配置文件或目录"
    
    def test_deployment_documentation_exists(self, project_root):
        """测试部署文档是否存在且包含关键信息"""
        # 检查文档目录
        docs_path = project_root / "docs"
        if not docs_path.exists():
            docs_path = project_root
        
        # 查找部署相关文档
        doc_patterns = ["*deploy*", "*deployment*", "*readme*", "*README*"]
        doc_extensions = [".md", ".txt", ".rst"]
        
        found_docs = []
        for pattern in doc_patterns:
            for ext in doc_extensions:
                found_docs.extend(list(docs_path.glob(f"{pattern}{ext}")))
        
        # 检查dev-notes.md文件
        dev_notes_path = docs_path / "d2c78b" / "4e5174" / "dev-notes.md"
        if dev_notes_path.exists():
            found_docs.append(dev_notes_path)
        
        assert len(found_docs) > 0, "应该存在部署相关的文档文件"
        
        # 检查文档内容是否包含部署相关关键词
        deployment_keywords = ["部署", "deploy", "environment", "配置", "config"]
        
        for doc_file in found_docs:
            try:
                content = doc_file.read_text(encoding='utf-8')
                has_deployment_info = any(keyword in content.lower() for keyword in deployment_keywords)
                if has_deployment_info:
                    assert len(content.strip()) > 0, f"{doc_file.name} 文档不应该为空"
                    return
            except Exception:
                continue
        
        pytest.fail("文档中应该包含部署相关的关键信息")