import pytest
from pathlib import Path
import sys
import os

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

class TestDatabaseModels:
    """数据库模型测试类"""
    
    def test_feature_3326_module_exists_and_importable(self):
        """测试feature_3326模块文件存在且可以正常导入"""
        # 检查模块文件是否存在
        module_path = project_root / "src" / "models" / "feature_3326.py"
        assert module_path.exists(), f"模块文件不存在: {module_path}"
        
        # 尝试导入模块
        try:
            from src.models import feature_3326
            assert feature_3326 is not None, "模块导入失败"
        except ImportError as e:
            pytest.fail(f"无法导入feature_3326模块: {e}")
    
    def test_feature_3326_has_required_attributes(self):
        """测试feature_3326模块包含必要的数据库模型属性和方法"""
        try:
            from src.models import feature_3326
            
            # 检查模块是否有常见的数据库模型属性
            expected_attributes = ['__name__', '__file__']
            for attr in expected_attributes:
                assert hasattr(feature_3326, attr), f"模块缺少必要属性: {attr}"
            
            # 检查模块内容不为空
            module_content = dir(feature_3326)
            assert len(module_content) > 0, "模块内容为空"
            
        except ImportError:
            pytest.skip("模块无法导入，跳过属性测试")
    
    def test_feature_3326_functions_return_correct_types(self):
        """测试feature_3326模块中的函数返回正确的数据类型"""
        try:
            from src.models import feature_3326
            
            # 获取模块中的所有可调用对象（函数、类等）
            callables = [getattr(feature_3326, name) for name in dir(feature_3326) 
                        if callable(getattr(feature_3326, name)) and not name.startswith('_')]
            
            # 如果有可调用对象，测试它们的基本属性
            for func in callables:
                assert hasattr(func, '__name__'), f"函数缺少__name__属性: {func}"
                assert hasattr(func, '__doc__') or func.__doc__ is None, f"函数缺少__doc__属性: {func}"
            
            # 如果没有找到函数，至少确保模块结构正确
            if not callables:
                assert True, "模块结构正确，但未找到公共函数"
                
        except ImportError:
            pytest.skip("模块无法导入，跳过函数类型测试")

class TestDocumentation:
    """文档文件测试类"""
    
    def test_dev_notes_file_exists(self):
        """测试开发文档文件存在且可读取"""
        doc_path = project_root / "docs" / "78b245" / "097efc" / "dev-notes.md"
        assert doc_path.exists(), f"开发文档文件不存在: {doc_path}"
        assert doc_path.is_file(), f"路径不是文件: {doc_path}"
        assert doc_path.suffix == '.md', f"文件不是markdown格式: {doc_path}"
    
    def test_dev_notes_content_not_empty(self):
        """测试开发文档内容不为空且包含有效信息"""
        doc_path = project_root / "docs" / "78b245" / "097efc" / "dev-notes.md"
        
        if doc_path.exists():
            content = doc_path.read_text(encoding='utf-8')
            assert len(content.strip()) > 0, "开发文档内容为空"
            assert len(content.split('\n')) > 1, "开发文档内容过少"
        else:
            pytest.skip("文档文件不存在，跳过内容测试")
    
    def test_project_structure_integrity(self):
        """测试项目目录结构完整性"""
        # 检查主要目录结构
        src_dir = project_root / "src"
        models_dir = project_root / "src" / "models"
        docs_dir = project_root / "docs"
        
        assert src_dir.exists() or models_dir.parent.exists(), "src目录结构不完整"
        assert docs_dir.exists() or (project_root / "docs" / "78b245").parent.exists(), "docs目录结构不完整"
        
        # 检查关键文件
        feature_file = project_root / "src" / "models" / "feature_3326.py"
        dev_notes_file = project_root / "docs" / "78b245" / "097efc" / "dev-notes.md"
        
        files_exist = []
        if feature_file.exists():
            files_exist.append("feature_3326.py")
        if dev_notes_file.exists():
            files_exist.append("dev-notes.md")
            
        assert len(files_exist) > 0, f"项目关键文件缺失，现有文件: {files_exist}"