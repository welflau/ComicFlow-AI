import pytest
from pathlib import Path
import sys
import os

# 添加项目根目录到Python路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def test_main_module_can_be_imported():
    """测试main.py模块是否可以正常导入"""
    try:
        import main
        assert True
    except ImportError as e:
        pytest.fail(f"无法导入main模块: {e}")

def test_main_file_exists():
    """测试main.py文件是否存在于backend目录中"""
    backend_dir = project_root / "backend"
    main_file = backend_dir / "main.py"
    assert main_file.exists(), f"main.py文件不存在于路径: {main_file}"
    assert main_file.is_file(), f"main.py不是一个有效的文件: {main_file}"

def test_dev_notes_file_exists_and_contains_content():
    """测试开发文档文件是否存在并包含相关内容"""
    docs_file = project_root / "docs" / "d2c78b" / "e0ab1e" / "dev-notes.md"
    assert docs_file.exists(), f"开发文档文件不存在于路径: {docs_file}"
    
    content = docs_file.read_text(encoding='utf-8')
    assert len(content.strip()) > 0, "开发文档文件内容为空"
    
    # 检查是否包含对象存储相关的关键词
    keywords = ["对象存储", "storage", "backend", "服务", "集成"]
    has_relevant_content = any(keyword in content for keyword in keywords)
    assert has_relevant_content, "开发文档应包含对象存储服务相关内容"

def test_main_module_structure():
    """测试main.py模块的基本结构和功能"""
    backend_dir = project_root / "backend"
    main_file = backend_dir / "main.py"
    
    if main_file.exists():
        # 临时添加backend目录到路径
        sys.path.insert(0, str(backend_dir))
        try:
            import main
            # 检查模块是否有基本的属性或函数
            module_attrs = dir(main)
            assert len(module_attrs) > 0, "main模块应该包含一些属性或函数"
        except Exception as e:
            pytest.fail(f"导入main模块时发生错误: {e}")
        finally:
            sys.path.remove(str(backend_dir))

def test_project_directory_structure():
    """测试项目目录结构是否正确"""
    # 检查backend目录存在
    backend_dir = project_root / "backend"
    assert backend_dir.exists(), "backend目录应该存在"
    assert backend_dir.is_dir(), "backend应该是一个目录"
    
    # 检查docs目录结构存在
    docs_dir = project_root / "docs" / "d2c78b" / "e0ab1e"
    assert docs_dir.exists(), "文档目录结构应该存在"
    assert docs_dir.is_dir(), "docs/d2c78b/e0ab1e应该是一个目录"

def test_file_permissions_and_readability():
    """测试关键文件的权限和可读性"""
    main_file = project_root / "backend" / "main.py"
    docs_file = project_root / "docs" / "d2c78b" / "e0ab1e" / "dev-notes.md"
    
    if main_file.exists():
        assert os.access(main_file, os.R_OK), "main.py文件应该可读"
        
    if docs_file.exists():
        assert os.access(docs_file, os.R_OK), "dev-notes.md文件应该可读"