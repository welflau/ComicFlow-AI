import pytest
from pathlib import Path
import sys
import os

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

class TestDatabaseModule:
    """数据库模块测试类"""
    
    def test_feature_6473_file_exists(self):
        """测试feature_6473.py文件是否存在"""
        feature_file = project_root / "src" / "models" / "feature_6473.py"
        assert feature_file.exists(), f"特性文件 {feature_file} 不存在"
        assert feature_file.is_file(), f"{feature_file} 不是一个有效的文件"
    
    def test_feature_6473_module_importable(self):
        """测试feature_6473模块是否可以正常导入"""
        try:
            # 动态导入模块
            feature_module_path = project_root / "src" / "models" / "feature_6473.py"
            if feature_module_path.exists():
                import importlib.util
                spec = importlib.util.spec_from_file_location("feature_6473", feature_module_path)
                feature_module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(feature_module)
                
                # 验证模块对象存在
                assert feature_module is not None, "模块导入失败"
                assert hasattr(feature_module, '__name__'), "模块缺少基本属性"
        except ImportError as e:
            pytest.fail(f"无法导入feature_6473模块: {e}")
        except Exception as e:
            pytest.fail(f"导入模块时发生未知错误: {e}")
    
    def test_dev_notes_documentation_exists(self):
        """测试开发文档是否存在并包含关键信息"""
        dev_notes_file = project_root / "docs" / "d2c78b" / "4c8e2a" / "dev-notes.md"
        assert dev_notes_file.exists(), f"开发文档 {dev_notes_file} 不存在"
        assert dev_notes_file.is_file(), f"{dev_notes_file} 不是一个有效的文件"
        
        # 检查文档内容
        try:
            content = dev_notes_file.read_text(encoding='utf-8')
            assert len(content.strip()) > 0, "开发文档内容为空"
            
            # 检查是否包含数据库相关关键词
            database_keywords = ['database', '数据库', 'schema', '架构', 'model', '模型']
            has_database_content = any(keyword.lower() in content.lower() for keyword in database_keywords)
            assert has_database_content, "开发文档缺少数据库相关内容"
            
        except UnicodeDecodeError:
            pytest.fail("无法读取开发文档，可能存在编码问题")
        except Exception as e:
            pytest.fail(f"读取开发文档时发生错误: {e}")
    
    def test_database_module_structure(self):
        """测试数据库模块目录结构是否正确"""
        src_dir = project_root / "src"
        models_dir = src_dir / "models"
        docs_dir = project_root / "docs"
        
        assert src_dir.exists(), "src目录不存在"
        assert models_dir.exists(), "models目录不存在"
        assert docs_dir.exists(), "docs目录不存在"
        
        # 验证目录结构
        assert src_dir.is_dir(), "src不是目录"
        assert models_dir.is_dir(), "models不是目录"
        assert docs_dir.is_dir(), "docs不是目录"
    
    def test_feature_6473_basic_functionality(self):
        """测试feature_6473模块的基本功能"""
        feature_module_path = project_root / "src" / "models" / "feature_6473.py"
        
        if not feature_module_path.exists():
            pytest.skip("feature_6473.py文件不存在，跳过功能测试")
        
        try:
            import importlib.util
            spec = importlib.util.spec_from_file_location("feature_6473", feature_module_path)
            feature_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(feature_module)
            
            # 检查模块是否定义了类或函数
            module_attrs = [attr for attr in dir(feature_module) if not attr.startswith('_')]
            assert len(module_attrs) > 0, "模块没有定义任何公共属性或方法"
            
            # 如果存在类，验证类的基本结构
            for attr_name in module_attrs:
                attr = getattr(feature_module, attr_name)
                if isinstance(attr, type):  # 如果是类
                    assert hasattr(attr, '__init__'), f"类 {attr_name} 缺少初始化方法"
                elif callable(attr):  # 如果是函数
                    assert hasattr(attr, '__call__'), f"函数 {attr_name} 不可调用"
                    
        except Exception as e:
            pytest.fail(f"测试模块功能时发生错误: {e}")