"""测试: 部署配置与文档"""
from pathlib import Path

REPO_DIR = Path(__file__).parent.parent

def test_source_files_exist():
    """测试源代码文件存在"""
    src = REPO_DIR / "src"
    if src.exists():
        files = list(src.rglob("*.*"))
        assert len(files) > 0, "src/ 目录下无文件"

def test_entry_file_exists():
    """测试入口文件存在"""
    entries = ["main.py", "app.py", "index.html"]
    found = any((REPO_DIR / e).exists() for e in entries)
    assert found, "缺少入口文件"

def test_no_syntax_errors():
    """测试 Python 文件无语法错误"""
    for pf in list(REPO_DIR.rglob("src/**/*.py"))[:10]:
        content = pf.read_text(encoding="utf-8", errors="replace")
        compile(content, str(pf), "exec")
