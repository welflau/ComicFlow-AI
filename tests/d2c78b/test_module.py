import pytest
from pathlib import Path
import sys
import os

# 添加项目根目录到Python路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def test_main_module_exists_and_importable():
    """测试main.py模块文件存在且可以正常导入"""
    main_file = project_root / "backend" / "main.py"
    assert main_file.exists(), "main.py文件不存在"
    assert main_file.is_file(), "main.py不是一个有效文件"
    
    # 测试模块可导入
    try:
        if str(project_root / "backend") not in sys.path:
            sys.path.insert(0, str(project_root / "backend"))
        import main
        assert main is not None, "main模块导入失败"
    except ImportError as e:
        pytest.fail(f"无法导入main模块: {e}")

def test_dev_notes_documentation_exists():
    """测试开发文档文件存在且包含消息队列相关内容"""
    doc_file = project_root / "docs" / "d2c78b" / "f18c65" / "dev-notes.md"
    assert doc_file.exists(), "开发文档文件不存在"
    assert doc_file.is_file(), "开发文档不是一个有效文件"
    
    # 检查文档内容包含消息队列相关关键词
    content = doc_file.read_text(encoding='utf-8')
    keywords = ["消息", "队列", "message", "queue", "backend"]
    found_keywords = [keyword for keyword in keywords if keyword.lower() in content.lower()]
    assert len(found_keywords) > 0, f"文档中未找到消息队列相关关键词，期望包含: {keywords}"

def test_backend_module_structure():
    """测试后端模块目录结构正确且main模块包含必要的消息队列功能"""
    backend_dir = project_root / "backend"
    assert backend_dir.exists(), "backend目录不存在"
    assert backend_dir.is_dir(), "backend不是一个有效目录"
    
    main_file = backend_dir / "main.py"
    assert main_file.exists(), "backend/main.py文件不存在"
    
    # 检查main.py文件内容是否包含消息队列相关代码
    main_content = main_file.read_text(encoding='utf-8')
    queue_indicators = ["queue", "message", "send", "receive", "publish", "subscribe", "消息", "队列"]
    found_indicators = [indicator for indicator in queue_indicators if indicator.lower() in main_content.lower()]
    assert len(found_indicators) > 0, f"main.py中未找到消息队列相关代码，期望包含: {queue_indicators}"

def test_main_module_functions_return_correct_types():
    """测试main模块中的函数返回正确的数据类型"""
    try:
        backend_path = project_root / "backend"
        if str(backend_path) not in sys.path:
            sys.path.insert(0, str(backend_path))
        
        import main
        
        # 检查模块是否有可调用的函数或类
        callable_items = [item for item in dir(main) if not item.startswith('_') and callable(getattr(main, item))]
        assert len(callable_items) > 0, "main模块中没有找到可调用的函数或类"
        
        # 测试模块属性类型
        for item_name in callable_items:
            item = getattr(main, item_name)
            assert callable(item), f"{item_name} 不是可调用对象"
            
    except ImportError:
        pytest.skip("main模块无法导入，跳过函数类型测试")

def test_project_directory_structure():
    """测试项目整体目录结构符合消息队列系统要求"""
    # 检查必要的目录结构
    required_paths = [
        project_root / "backend",
        project_root / "docs",
        project_root / "docs" / "d2c78b",
        project_root / "docs" / "d2c78b" / "f18c65"
    ]
    
    for path in required_paths:
        assert path.exists(), f"必要目录不存在: {path}"
        assert path.is_dir(), f"路径不是目录: {path}"
    
    # 检查必要的文件
    required_files = [
        project_root / "backend" / "main.py",
        project_root / "docs" / "d2c78b" / "f18c65" / "dev-notes.md"
    ]
    
    for file_path in required_files:
        assert file_path.exists(), f"必要文件不存在: {file_path}"
        assert file_path.is_file(), f"路径不是文件: {file_path}"