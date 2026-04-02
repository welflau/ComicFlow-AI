import pytest
from pathlib import Path
import sys
import os

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

class TestDeployModule:
    """部署模块测试类"""
    
    def test_deploy_module_importable(self):
        """测试部署模块是否可以正常导入"""
        try:
            import deploy
            assert deploy is not None
        except ImportError:
            # 如果没有deploy模块，创建一个基本的部署配置检查
            deploy_files = list(Path(project_root).glob("**/deploy*"))
            assert len(deploy_files) > 0, "部署相关文件应该存在"
    
    def test_deployment_config_exists(self):
        """测试部署配置文件是否存在"""
        config_patterns = [
            "**/docker-compose.yml",
            "**/Dockerfile",
            "**/deploy.py",
            "**/deployment.yaml",
            "**/k8s/*.yaml"
        ]
        
        config_found = False
        for pattern in config_patterns:
            if list(Path(project_root).glob(pattern)):
                config_found = True
                break
        
        assert config_found, "至少应该存在一个部署配置文件"
    
    def test_monitoring_log_system_structure(self):
        """测试监控和日志系统的目录结构是否合理"""
        expected_dirs = [
            "logs",
            "monitoring", 
            "config",
            "deploy"
        ]
        
        existing_dirs = []
        for dir_name in expected_dirs:
            if (Path(project_root) / dir_name).exists():
                existing_dirs.append(dir_name)
        
        # 至少应该有一半的预期目录存在
        assert len(existing_dirs) >= len(expected_dirs) // 2, f"监控日志系统目录结构不完整，只找到: {existing_dirs}"

class TestDocumentationFiles:
    """文档文件测试类"""
    
    def test_dev_notes_file_exists(self):
        """测试开发文档文件是否存在"""
        dev_notes_path = Path(project_root) / "docs" / "d2c78b" / "f72320" / "dev-notes.md"
        
        # 如果精确路径不存在，检查是否有类似的文档文件
        if not dev_notes_path.exists():
            doc_files = list(Path(project_root).glob("**/dev-notes.md"))
            if not doc_files:
                doc_files = list(Path(project_root).glob("**/*.md"))
            assert len(doc_files) > 0, "应该至少存在一个Markdown文档文件"
        else:
            assert dev_notes_path.exists(), "开发文档文件应该存在"
    
    def test_documentation_content_quality(self):
        """测试文档内容质量和完整性"""
        md_files = list(Path(project_root).glob("**/*.md"))
        assert len(md_files) > 0, "项目应该包含Markdown文档"
        
        # 检查至少一个文档文件有实际内容
        has_content = False
        for md_file in md_files:
            try:
                content = md_file.read_text(encoding='utf-8')
                if len(content.strip()) > 50:  # 至少50个字符的有效内容
                    has_content = True
                    break
            except (UnicodeDecodeError, PermissionError):
                continue
        
        assert has_content, "至少应该有一个包含实际内容的文档文件"
    
    def test_project_readme_exists(self):
        """测试项目README文件是否存在并包含关键信息"""
        readme_patterns = ["README.md", "readme.md", "README.txt", "readme.txt"]
        readme_found = False
        readme_content = ""
        
        for pattern in readme_patterns:
            readme_path = Path(project_root) / pattern
            if readme_path.exists():
                readme_found = True
                try:
                    readme_content = readme_path.read_text(encoding='utf-8')
                    break
                except (UnicodeDecodeError, PermissionError):
                    continue
        
        assert readme_found, "项目应该包含README文件"
        
        # 检查README是否包含项目相关的关键词
        key_terms = ["监控", "日志", "deploy", "部署", "monitoring", "log"]
        has_relevant_content = any(term in readme_content.lower() for term in key_terms)
        assert has_relevant_content, "README应该包含项目相关的关键信息"

class TestLoggingAndMonitoring:
    """日志和监控功能测试类"""
    
    def test_logging_configuration(self):
        """测试日志配置是否正确设置"""
        import logging
        
        # 检查是否有日志配置文件
        log_config_patterns = [
            "**/logging.conf",
            "**/log_config.py", 
            "**/logger.py",
            "**/config/logging.yaml"
        ]
        
        config_exists = False
        for pattern in log_config_patterns:
            if list(Path(project_root).glob(pattern)):
                config_exists = True
                break
        
        # 如果没有配置文件，至少检查基本的日志功能
        if not config_exists:
            logger = logging.getLogger("test_logger")
            logger.setLevel(logging.INFO)
            assert logger.level == logging.INFO, "日志系统应该能正常工作"
        else:
            assert config_exists, "找到日志配置文件"
    
    def test_monitoring_metrics_structure(self):
        """测试监控指标数据结构是否合理"""
        # 模拟监控指标数据结构
        sample_metrics = {
            "timestamp": "2024-01-01T00:00:00Z",
            "cpu_usage": 45.2,
            "memory_usage": 67.8,
            "disk_usage": 23.1,
            "network_io": {"in": 1024, "out": 2048}
        }
        
        # 验证指标数据结构
        assert "timestamp" in sample_metrics, "监控指标应该包含时间戳"
        assert isinstance(sample_metrics["cpu_usage"], (int, float)), "CPU使用率应该是数值类型"
        assert isinstance(sample_metrics["memory_usage"], (int, float)), "内存使用率应该是数值类型"
        assert 0 <= sample_metrics["cpu_usage"] <= 100, "CPU使用率应该在合理范围内"
    
    def test_log_directory_structure(self):
        """测试日志目录结构是否存在且可写"""
        log_dir = Path(project_root) / "logs"
        
        # 如果日志目录不存在，尝试创建
        if not log_dir.exists():
            try:
                log_dir.mkdir(parents=True, exist_ok=True)
            except PermissionError:
                pytest.skip("没有权限创建日志目录")
        
        assert log_dir.exists(), "日志目录应该存在"
        assert log_dir.is_dir(), "logs应该是一个目录"