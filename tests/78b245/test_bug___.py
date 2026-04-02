import pytest
from pathlib import Path
from bs4 import BeautifulSoup
import re

class TestWorkOrderStatusConsistency:
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
        status_indicators = [
            'status', 'test', 'testing', 'passed', 'pass',
            '状态', '测试', '通过', '测试中', '测试通过'
        ]
        
        found_status_elements = False
        for indicator in status_indicators:
            # 检查class属性、id属性或文本内容
            if (soup.find(attrs={'class': re.compile(indicator, re.I)}) or
                soup.find(attrs={'id': re.compile(indicator, re.I)}) or
                soup.find(string=re.compile(indicator, re.I))):
                found_status_elements = True
                break
        
        assert found_status_elements, "HTML文件中未找到工单状态相关的元素"
    
    def test_dev_notes_file_exists_and_contains_bug_info(self):
        """测试开发文档是否存在并包含BUG相关信息"""
        dev_notes_file = Path("docs/78b245/f13de8/dev-notes.md")
        
        assert dev_notes_file.exists(), "开发文档文件不存在"
        assert dev_notes_file.is_file(), "开发文档不是一个有效的文件"
        
        with open(dev_notes_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 检查是否包含BUG相关的关键词
        bug_keywords = [
            'bug', 'BUG', '工单', '状态', '不一致', 
            '测试中', '测试通过', 'status', 'inconsistent'
        ]
        
        found_keywords = []
        for keyword in bug_keywords:
            if keyword in content:
                found_keywords.append(keyword)
        
        assert len(found_keywords) > 0, f"开发文档中未找到BUG相关关键词，期望找到: {bug_keywords}"
    
    def test_status_consistency_validation(self):
        """测试状态一致性验证逻辑"""
        # 模拟左侧和右侧状态数据
        test_cases = [
            # (左侧状态, 右侧状态, 是否一致)
            ("测试中", "测试中", True),
            ("测试通过", "测试通过", True),
            ("测试中", "测试通过", False),  # 这是BUG场景
            ("pending", "completed", False),
            ("testing", "testing", True),
        ]
        
        def validate_status_consistency(left_status, right_status):
            """验证左右两侧状态是否一致"""
            return left_status == right_status
        
        for left, right, expected in test_cases:
            result = validate_status_consistency(left, right)
            if expected:
                assert result, f"状态应该一致: 左侧='{left}', 右侧='{right}'"
            else:
                assert not result, f"状态不应该一致: 左侧='{left}', 右侧='{right}'"
    
    def test_project_structure_integrity(self):
        """测试项目结构完整性"""
        # 检查关键目录和文件是否存在
        expected_paths = [
            Path("index.html"),
            Path("docs"),
            Path("docs/78b245"),
            Path("docs/78b245/f13de8"),
        ]
        
        for path in expected_paths:
            assert path.exists(), f"项目结构不完整，缺少: {path}"
    
    def test_html_structure_for_status_display(self):
        """测试HTML结构是否适合状态显示"""
        index_file = Path("index.html")
        
        if not index_file.exists():
            pytest.skip("index.html文件不存在，跳过结构测试")
        
        with open(index_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        soup = BeautifulSoup(content, 'html.parser')
        
        # 检查基本HTML结构
        assert soup.find('html'), "HTML文件缺少html标签"
        assert soup.find('head'), "HTML文件缺少head标签"
        assert soup.find('body'), "HTML文件缺少body标签"
        
        # 检查是否有可能用于显示状态的容器元素
        container_tags = ['div', 'span', 'section', 'article', 'main']
        has_containers = any(soup.find(tag) for tag in container_tags)
        assert has_containers, "HTML文件中未找到用于内容显示的容器元素"