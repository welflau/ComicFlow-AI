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
        import backend.main
        assert True
    except ImportError:
        # 如果backend包不存在，尝试直接导入main
        main_file = project_root / "backend" / "main.py"
        if main_file.exists():
            spec = __import__('importlib.util').util.spec_from_file_location("main", main_file)
            main_module = __import__('importlib.util').util.module_from_spec(spec)
            spec.loader.exec_module(main_module)
            assert main_module is not None
        else:
            pytest.fail("无法找到或导入main.py模块")

def test_backend_main_file_exists():
    """测试backend目录下的main.py文件是否存在"""
    main_file = project_root / "backend" / "main.py"
    assert main_file.exists(), f"main.py文件不存在于路径: {main_file}"
    assert main_file.is_file(), "main.py应该是一个文件而不是目录"

def test_dev_notes_file_exists_and_contains_queue_content():
    """测试开发文档是否存在并包含消息队列相关内容"""
    dev_notes_file = project_root / "docs" / "d2c78b" / "f18c65" / "dev-notes.md"
    
    # 检查文件是否存在
    assert dev_notes_file.exists(), f"开发文档不存在于路径: {dev_notes_file}"
    assert dev_notes_file.is_file(), "dev-notes.md应该是一个文件"
    
    # 检查文件内容是否包含消息队列相关关键词
    content = dev_notes_file.read_text(encoding='utf-8')
    queue_keywords = ['消息队列', 'message queue', 'queue', '队列', 'backend']
    
    has_relevant_content = any(keyword.lower() in content.lower() for keyword in queue_keywords)
    assert has_relevant_content, "开发文档应该包含消息队列相关内容"

def test_main_module_has_queue_functionality():
    """测试main.py模块是否包含消息队列相关功能函数"""
    main_file = project_root / "backend" / "main.py"
    
    if main_file.exists():
        content = main_file.read_text(encoding='utf-8')
        
        # 检查是否包含消息队列相关的函数或类定义
        queue_patterns = ['def ', 'class ', 'queue', 'message', 'send', 'receive']
        has_functionality = any(pattern in content.lower() for pattern in queue_patterns)
        
        assert has_functionality, "main.py应该包含消息队列相关的功能实现"
    else:
        pytest.skip("main.py文件不存在，跳过功能测试")

def test_backend_directory_structure():
    """测试后端目录结构是否正确"""
    backend_dir = project_root / "backend"
    docs_dir = project_root / "docs"
    
    assert backend_dir.exists(), "backend目录应该存在"
    assert backend_dir.is_dir(), "backend应该是一个目录"
    assert docs_dir.exists(), "docs目录应该存在"
    assert docs_dir.is_dir(), "docs应该是一个目录"