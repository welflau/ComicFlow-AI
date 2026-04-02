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
            # 如果没有找到任何配置文件，检查是否有其他常见文件
            existing_files = list(deploy_module_path.glob("*.py"))
            assert len(existing_files) > 0, "deploy目录中应该至少包含一个Python文件"
    
    def test_deploy_module_importable(self, deploy_module_path):
        """测试deploy模块是否可以正常导入"""
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
                assert len(config_files) > 0, "应该至少有一个Python配置文件可以导入"
                
                for config_file in config_files:
                    spec = importlib.util.spec_from_file_location(
                        config_file.stem, config_file
                    )
                    if spec and spec.loader:
                        module = importlib.util.module_from_spec(spec)
                        spec.loader.exec_module(module)
                        assert module is not None, f"{config_file.name} 应该可以成功导入"
                        break
        except ImportError as e:
            pytest.fail(f"导入deploy模块失败: {e}")
    
    def test_environment_config_structure(self, deploy_module_path):
        """测试多环境配置结构是否正确"""
        # 检查是否存在不同环境的配置
        env_indicators = [
            "dev", "test", "prod", "staging",
            "development", "production", "local"
        ]
        
        found_env_configs = []
        
        # 检查文件名中是否包含环境标识
        for py_file in deploy_module_path.glob("*.py"):
            file_content = ""
            try:
                file_content = py_file.read_text(encoding='utf-8')
            except:
                try:
                    file_content = py_file.read_text(encoding='gbk')
                except:
                    continue
            
            # 检查文件内容是否包含环境配置
            for env in env_indicators:
                if env.upper() in file_content or env.lower() in file_content:
                    found_env_configs.append(env)
                    break
        
        # 或者检查是否有专门的环境配置文件夹
        env_dirs = [d for d in deploy_module_path.iterdir() 
                   if d.is_dir() and any(env in d.name.lower() for env in env_indicators)]
        
        # 或者检查配置文件中是否有环境相关的变量
        config_files = list(deploy_module_path.glob("*.py"))
        has_env_config = False
        
        for config_file in config_files:
            try:
                content = config_file.read_text(encoding='utf-8')
                env_keywords = ['ENVIRONMENT', 'ENV', 'DEBUG', 'DATABASE_URL', 'API_URL']
                if any(keyword in content for keyword in env_keywords):
                    has_env_config = True
                    break
            except:
                continue
        
        assert (len(found_env_configs) > 0 or len(env_dirs) > 0 or has_env_config), \
            "应该包含多环境配置相关的文件或设置"
    
    def test_deployment_documentation_exists(self, project_root):
        """测试部署文档是否存在且包含关键信息"""
        # 查找文档文件
        doc_paths = [
            project_root / "docs" / "d2c78b" / "4e5174" / "dev-notes.md",
            project_root / "README.md",
            project_root / "docs" / "README.md",
            project_root / "deploy" / "README.md"
        ]
        
        found_doc = None
        for doc_path in doc_paths:
            if doc_path.exists():
                found_doc = doc_path
                break
        
        assert found_doc is not None, "应该存在部署相关的文档文件"
        
        # 检查文档内容是否包含部署相关信息
        try:
            content = found_doc.read_text(encoding='utf-8')
        except:
            content = found_doc.read_text(encoding='gbk')
        
        deploy_keywords = [
            '部署', 'deploy', 'environment', '环境', 
            'config', '配置', 'setup', '安装'
        ]
        
        found_keywords = [kw for kw in deploy_keywords if kw.lower() in content.lower()]
        assert len(found_keywords) > 0, f"文档应该包含部署相关的关键词，找到的关键词: {found_keywords}"
    
    def test_configuration_values_type(self, deploy_module_path):
        """测试配置值的类型是否正确"""
        config_files = list(deploy_module_path.glob("*.py"))
        
        for config_file in config_files:
            try:
                spec = importlib.util.spec_from_file_location(
                    config_file.stem, config_file
                )
                if spec and spec.loader:
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)
                    
                    # 检查常见配置项的类型
                    if hasattr(module, 'DEBUG'):
                        assert isinstance(module.DEBUG, bool), "DEBUG配置应该是布尔类型"
                    
                    if hasattr(module, 'PORT'):
                        assert isinstance(module.PORT, int), "PORT配置应该是整数类型"
                    
                    if hasattr(module, 'HOST'):
                        assert isinstance(module.HOST, str), "HOST配置应该是字符串类型"
                    
                    # 如果有配置字典，检查其结构
                    config_attrs =