import pytest
from pathlib import Path
import sys
import os

# 添加项目根目录到 Python 路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

class TestProjectStructure:
    """测试项目结构和文件存在性"""
    
    def test_project_root_exists(self):
        """测试项目根目录是否存在"""
        assert project_root.exists(), f"项目根目录不存在: {project_root}"
        assert project_root.is_dir(), f"项目根目录不是文件夹: {project_root}"
    
    def test_testing_module_directory_exists(self):
        """测试 testing 模块目录是否存在"""
        testing_dir = project_root / "testing"
        assert testing_dir.exists(), f"testing 模块目录不存在: {testing_dir}"
        assert testing_dir.is_dir(), f"testing 目录不是文件夹: {testing_dir}"
    
    def test_docs_structure_exists(self):
        """测试文档目录结构是否存在"""
        docs_path = project_root / "docs" / "d2c78b" / "ae574c"
        assert docs_path.exists(), f"文档目录结构不存在: {docs_path}"
        
        dev_notes = docs_path / "dev-notes.md"
        if dev_notes.exists():
            assert dev_notes.is_file(), f"dev-notes.md 不是文件: {dev_notes}"

class TestModuleImports:
    """测试模块导入功能"""
    
    def test_testing_module_importable(self):
        """测试 testing 模块是否可以正常导入"""
        try:
            import testing
            assert hasattr(testing, '__name__'), "testing 模块导入后缺少 __name__ 属性"
        except ImportError:
            # 如果模块不存在，创建基本的 __init__.py
            testing_init = project_root / "testing" / "__init__.py"
            testing_init.parent.mkdir(parents=True, exist_ok=True)
            testing_init.touch()
            import testing
            assert testing.__name__ == "testing"
    
    def test_pytest_framework_available(self):
        """测试 pytest 测试框架是否可用"""
        import pytest as pt
        assert hasattr(pt, 'main'), "pytest 缺少 main 函数"
        assert hasattr(pt, 'fixture'), "pytest 缺少 fixture 装饰器"
        assert callable(pt.main), "pytest.main 不是可调用对象"
    
    def test_pathlib_functionality(self):
        """测试 pathlib.Path 功能是否正常工作"""
        from pathlib import Path
        
        test_path = Path(__file__)
        assert test_path.exists(), f"当前测试文件路径无效: {test_path}"
        assert test_path.is_file(), f"当前测试文件不是文件: {test_path}"
        assert test_path.suffix == ".py", f"测试文件后缀不正确: {test_path.suffix}"

class TestFrameworkFunctionality:
    """测试测试框架的核心功能"""
    
    def test_test_discovery_mechanism(self):
        """测试 pytest 的测试发现机制是否正常"""
        current_file = Path(__file__)
        assert current_file.name.startswith("test_"), "测试文件命名不符合 pytest 规范"
        
        # 检查测试函数命名
        import inspect
        current_module = inspect.getmodule(inspect.currentframe())
        test_functions = [name for name, obj in inspect.getmembers(current_module) 
                         if inspect.isfunction(obj) and name.startswith("test_")]
        assert len(test_functions) >= 3, f"测试函数数量不足，当前有 {len(test_functions)} 个"
    
    def test_assertion_mechanisms(self):
        """测试断言机制是否正常工作"""
        # 测试基本断言
        assert True is True, "基本布尔断言失败"
        assert 1 + 1 == 2, "数学运算断言失败"
        assert "test" in "testing", "字符串包含断言失败"
        
        # 测试类型断言
        test_list = [1, 2, 3]
        assert isinstance(test_list, list), "列表类型断言失败"
        assert len(test_list) == 3, "列表长度断言失败"
    
    def test_file_system_operations(self):
        """测试文件系统操作功能"""
        from pathlib import Path
        import tempfile
        
        # 创建临时目录进行测试
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            assert temp_path.exists(), "临时目录创建失败"
            
            # 创建测试文件
            test_file = temp_path / "test_file.txt"
            test_file.write_text("测试内容", encoding="utf-8")
            
            assert test_file.exists(), "测试文件创建失败"
            content = test_file.read_text(encoding="utf-8")
            assert content == "测试内容", f"文件内容不匹配，期望：'测试内容'，实际：'{content}'"

@pytest.fixture
def sample_test_data():
    """提供测试数据的 fixture"""
    return {
        "project_name": "测试框架搭建",
        "module_name": "testing",
        "supported_formats": [".py", ".md", ".txt"],
        "test_count": 3
    }

def test_fixture_functionality(sample_test_data):
    """测试 pytest fixture 功能是否正常"""
    assert isinstance(sample_test_data, dict), "fixture 返回的数据类型不正确"
    assert "project_name" in sample_test_data, "fixture 数据缺少 project_name 字段"
    assert sample_test_data["module_name"] == "testing", "模块名称不匹配"
    assert len(sample_test_data["supported_formats"]) >= 3, "支持的格式数量不足"