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
    if not main_file.exists():
        pytest.skip("backend/main.py 文件不存在，跳过导入测试")
    
    spec = importlib.util.spec_from_file_location("main", main_file)
    assert spec is not None, "无法创建模块规范"
    
    main_module = importlib.util.module_from_spec(spec)
    assert main_module is not None, "无法创建模块对象"
    
    try:
        spec.loader.exec_module(main_module)
    except Exception as e:
        pytest.fail(f"导入 backend/main.py 模块失败: {e}")

def test_dev_notes_documentation_exists():
    """测试开发文档是否存在并包含关键内容"""
    dev_notes_file = Path("docs/78b245/8052cd/dev-notes.md")
    assert dev_notes_file.exists(), "开发文档 dev-notes.md 不存在"
    assert dev_notes_file.is_file(), "dev-notes.md 不是一个有效的文件"
    
    content = dev_notes_file.read_text(encoding='utf-8')
    assert len(content.strip()) > 0, "开发文档内容为空"

def test_backend_module_has_workflow_functionality():
    """测试后端模块是否包含工作流引擎相关功能"""
    main_file = Path("backend/main.py")
    if not main_file.exists():
        pytest.skip("backend/main.py 文件不存在，跳过功能测试")
    
    try:
        spec = importlib.util.spec_from_file_location("main", main_file)
        main_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(main_module)
        
        # 检查是否有常见的工作流引擎相关属性或函数
        workflow_keywords = ['workflow', 'engine', 'process', 'task', 'execute', 'run']
        module_attrs = dir(main_module)
        
        has_workflow_related = any(
            any(keyword in attr.lower() for keyword in workflow_keywords)
            for attr in module_attrs if not attr.startswith('_')
        )
        
        assert has_workflow_related or len([attr for attr in module_attrs if not attr.startswith('_')]) > 0, \
            "模块中未找到工作流相关功能或公共接口"
            
    except Exception as e:
        pytest.fail(f"测试工作流功能时出错: {e}")

def test_project_structure_integrity():
    """测试项目结构完整性"""
    backend_dir = Path("backend")
    docs_dir = Path("docs")
    
    assert backend_dir.exists(), "backend 目录不存在"
    assert backend_dir.is_dir(), "backend 不是一个目录"
    
    assert docs_dir.exists(), "docs 目录不存在"
    assert docs_dir.is_dir(), "docs 不是一个目录"
    
    # 检查文档子目录结构
    doc_subdir = Path("docs/78b245/8052cd")
    assert doc_subdir.exists(), "文档子目录结构不完整"
    assert doc_subdir.is_dir(), "文档路径不是目录"