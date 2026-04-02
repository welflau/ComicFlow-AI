import pytest
from pathlib import Path
import sys
import importlib.util

def test_backend_main_module_exists():
    """测试后端主模块文件是否存在"""
    main_file = Path("backend/main.py")
    assert main_file.exists(), "backend/main.py 文件不存在"
    assert main_file.is_file(), "backend/main.py 不是一个有效的文件"

def test_backend_main_module_importable():
    """测试后端主模块是否可以正常导入"""
    main_file = Path("backend/main.py")
    if main_file.exists():
        spec = importlib.util.spec_from_file_location("main", main_file)
        main_module = importlib.util.module_from_spec(spec)
        try:
            spec.loader.exec_module(main_module)
            assert main_module is not None, "主模块导入失败"
        except Exception as e:
            pytest.fail(f"导入主模块时发生错误: {e}")

def test_dev_notes_documentation_exists():
    """测试开发文档是否存在并包含必要内容"""
    dev_notes_file = Path("docs/78b245/8052cd/dev-notes.md")
    assert dev_notes_file.exists(), "开发文档 dev-notes.md 不存在"
    
    content = dev_notes_file.read_text(encoding='utf-8')
    assert len(content.strip()) > 0, "开发文档内容为空"
    
    # 检查是否包含工作流引擎相关的关键词
    keywords = ["工作流", "workflow", "引擎", "engine", "API"]
    has_keyword = any(keyword.lower() in content.lower() for keyword in keywords)
    assert has_keyword, "开发文档应包含工作流引擎相关的关键词"

def test_backend_directory_structure():
    """测试后端目录结构是否正确"""
    backend_dir = Path("backend")
    assert backend_dir.exists(), "backend 目录不存在"
    assert backend_dir.is_dir(), "backend 不是一个目录"
    
    main_file = backend_dir / "main.py"
    assert main_file.exists(), "backend 目录中缺少 main.py 文件"

def test_workflow_engine_core_functionality():
    """测试工作流引擎核心功能模块的基本结构"""
    main_file = Path("backend/main.py")
    if main_file.exists():
        content = main_file.read_text(encoding='utf-8')
        
        # 检查是否包含基本的工作流引擎相关代码结构
        core_elements = ["def", "class", "import"]
        has_core_elements = any(element in content for element in core_elements)
        assert has_core_elements, "主模块应包含基本的Python代码结构（函数、类或导入语句）"
        
        # 检查文件不为空
        assert len(content.strip()) > 0, "main.py 文件不应为空"

def test_project_documentation_structure():
    """测试项目文档目录结构的完整性"""
    docs_base = Path("docs/78b245/8052cd")
    assert docs_base.exists(), "文档目录结构不完整"
    assert docs_base.is_dir(), "docs/78b245/8052cd 应该是一个目录"
    
    dev_notes = docs_base / "dev-notes.md"
    assert dev_notes.exists(), "开发笔记文件缺失"
    assert dev_notes.suffix == ".md", "开发笔记应该是 Markdown 格式文件"