import pytest
from pathlib import Path
from bs4 import BeautifulSoup
import re

class TestTicketStatusConsistency:
    """测试工单状态显示一致性的相关功能"""
    
    def test_index_html_file_exists(self):
        """测试主页HTML文件是否存在"""
        index_file = Path("index.html")
        assert index_file.exists(), "index.html文件不存在"
        assert index_file.is_file(), "index.html不是一个有效的文件"
    
    def test_index_html_contains_status_elements(self):
        """测试HTML文件是否包含工单状态相关的关键元素"""
        index_file = Path("index.html")
        
        # 如果文件不存在，跳过测试
        if not index_file.exists():
            pytest.skip("index.html文件不存在，跳过内容测试")
        
        with open(index_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 使用BeautifulSoup解析HTML
        soup = BeautifulSoup(content, 'html.parser')
        
        # 检查是否包含状态相关的元素
        status_keywords = ['状态', 'status', '测试中', 'testing', '测试通过', 'passed']
        found_keywords = []
        
        for keyword in status_keywords:
            if keyword in content.lower():
                found_keywords.append(keyword)
        
        assert len(found_keywords) > 0, f"HTML文件中未找到状态相关关键词: {status_keywords}"
        
        # 检查是否有可能导致状态显示不一致的元素
        # 查找可能的左侧和右侧状态显示区域
        left_elements = soup.find_all(attrs={"class": re.compile(r"left|sidebar|nav")})
        right_elements = soup.find_all(attrs={"class": re.compile(r"right|main|content")})
        
        # 至少应该有一些布局元素
        assert len(left_elements) > 0 or len(right_elements) > 0, "未找到可能的左右布局元素"
    
    def test_dev_notes_file_exists_and_contains_bug_info(self):
        """测试开发文档是否存在并包含BUG相关信息"""
        dev_notes_file = Path("docs/78b245/f13de8/dev-notes.md")
        
        assert dev_notes_file.exists(), "开发文档文件不存在"
        assert dev_notes_file.is_file(), "开发文档不是一个有效的文件"
        
        with open(dev_notes_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 检查是否包含BUG相关信息
        bug_keywords = ['bug', 'BUG', '工单', '状态', '不一致', '测试中', '测试通过']
        found_keywords = []
        
        for keyword in bug_keywords:
            if keyword in content:
                found_keywords.append(keyword)
        
        assert len(found_keywords) >= 2, f"开发文档中应包含更多BUG相关关键词，当前找到: {found_keywords}"
    
    def test_status_consistency_validation(self):
        """测试状态一致性验证逻辑"""
        # 模拟状态不一致的情况
        left_status = "测试中"
        right_status = "测试通过"
        
        def validate_status_consistency(left, right):
            """验证左右两侧状态是否一致"""
            return left == right
        
        # 测试不一致的情况
        assert not validate_status_consistency(left_status, right_status), "应该检测到状态不一致"
        
        # 测试一致的情况
        consistent_status = "测试中"
        assert validate_status_consistency(consistent_status, consistent_status), "相同状态应该返回一致"
    
    def test_status_normalization(self):
        """测试状态标准化功能，确保不同格式的状态能正确识别"""
        def normalize_status(status):
            """标准化状态字符串"""
            if not status:
                return ""
            
            status = status.strip().lower()
            status_mapping = {
                '测试中': 'testing',
                'testing': 'testing',
                '测试通过': 'passed',
                'passed': 'passed',
                'test passed': 'passed',
                '进行中': 'testing'
            }
            
            return status_mapping.get(status, status)
        
        # 测试各种状态格式的标准化
        assert normalize_status("测试中") == "testing"
        assert normalize_status("Testing") == "testing"
        assert normalize_status("测试通过") == "passed"
        assert normalize_status("PASSED") == "passed"
        assert normalize_status("  测试中  ") == "testing"
        
        # 测试标准化后的一致性检查
        left_normalized = normalize_status("测试中")
        right_normalized = normalize_status("Testing")
        assert left_normalized == right_normalized, "标准化后的状态应该一致"
    
    def test_project_structure_integrity(self):
        """测试项目结构完整性"""
        # 检查关键文件是否存在
        critical_files = [
            Path("index.html"),
            Path("docs/78b245/f13de8/dev-notes.md")
        ]
        
        missing_files = []
        for file_path in critical_files:
            if not file_path.exists():
                missing_files.append(str(file_path))
        
        assert len(missing_files) == 0, f"以下关键文件缺失: {missing_files}"
        
        # 检查docs目录结构
        docs_dir = Path("docs")
        if docs_dir.exists():
            assert docs_dir.is_dir(), "docs应该是一个目录"
            
            # 检查是否有合理的目录结构
            subdirs = [d for d in docs_dir.iterdir() if d.is_dir()]
            assert len(subdirs) > 0, "docs目录下应该包含子目录"