import pytest
from pathlib import Path
import yaml
import subprocess
import os
import stat

class TestCIPipeline:
    """测试CI流水线配置"""
    
    def test_ci_workflow_file_exists_and_valid(self):
        """测试CI工作流文件存在且配置有效"""
        ci_file = Path(".github/workflows/ci.yml")
        assert ci_file.exists(), "CI工作流文件不存在"
        
        with open(ci_file, 'r', encoding='utf-8') as f:
            ci_config = yaml.safe_load(f)
        
        assert 'name' in ci_config, "CI配置缺少name字段"
        assert 'on' in ci_config, "CI配置缺少触发条件"
        assert 'jobs' in ci_config, "CI配置缺少jobs定义"
        
        # 检查是否包含基本的CI步骤
        jobs = ci_config['jobs']
        assert len(jobs) > 0, "CI配置没有定义任何job"
        
        first_job = list(jobs.values())[0]
        assert 'steps' in first_job, "CI job缺少steps定义"
        
        steps = first_job['steps']
        step_names = [step.get('name', '') for step in steps]
        assert any('checkout' in name.lower() or 'actions/checkout' in str(step.get('uses', '')) for step in steps), "CI流程缺少代码检出步骤"

    def test_cd_workflow_file_exists_and_valid(self):
        """测试CD工作流文件存在且配置有效"""
        cd_file = Path(".github/workflows/cd.yml")
        assert cd_file.exists(), "CD工作流文件不存在"
        
        with open(cd_file, 'r', encoding='utf-8') as f:
            cd_config = yaml.safe_load(f)
        
        assert 'name' in cd_config, "CD配置缺少name字段"
        assert 'on' in cd_config, "CD配置缺少触发条件"
        assert 'jobs' in cd_config, "CD配置缺少jobs定义"
        
        # 检查CD触发条件是否合理（通常在push到main分支时触发）
        trigger_config = cd_config['on']
        if isinstance(trigger_config, dict):
            assert 'push' in trigger_config or 'workflow_dispatch' in trigger_config, "CD配置缺少合适的触发条件"

    def test_pr_check_workflow_file_exists_and_valid(self):
        """测试PR检查工作流文件存在且配置有效"""
        pr_file = Path(".github/workflows/pr-check.yml")
        assert pr_file.exists(), "PR检查工作流文件不存在"
        
        with open(pr_file, 'r', encoding='utf-8') as f:
            pr_config = yaml.safe_load(f)
        
        assert 'name' in pr_config, "PR检查配置缺少name字段"
        assert 'on' in pr_config, "PR检查配置缺少触发条件"
        assert 'jobs' in pr_config, "PR检查配置缺少jobs定义"
        
        # 检查是否在PR事件时触发
        trigger_config = pr_config['on']
        if isinstance(trigger_config, dict):
            assert 'pull_request' in trigger_config, "PR检查配置应该在pull_request事件时触发"
        elif isinstance(trigger_config, list):
            assert 'pull_request' in trigger_config, "PR检查配置应该在pull_request事件时触发"

class TestBuildScripts:
    """测试构建脚本"""
    
    def test_build_script_exists_and_executable(self):
        """测试构建脚本存在且可执行"""
        build_script = Path("scripts/build.sh")
        assert build_script.exists(), "构建脚本不存在"
        
        # 检查文件是否可执行
        file_stat = build_script.stat()
        assert file_stat.st_mode & stat.S_IEXEC, "构建脚本没有执行权限"
        
        # 检查脚本内容基本结构
        with open(build_script, 'r', encoding='utf-8') as f:
            content = f.read()
        
        assert content.startswith('#!/bin/bash') or content.startswith('#!/bin/sh'), "构建脚本缺少shebang"
        assert len(content.strip()) > 0, "构建脚本内容为空"

    def test_test_script_exists_and_executable(self):
        """测试测试脚本存在且可执行"""
        test_script = Path("scripts/test.sh")
        assert test_script.exists(), "测试脚本不存在"
        
        # 检查文件是否可执行
        file_stat = test_script.stat()
        assert file_stat.st_mode & stat.S_IEXEC, "测试脚本没有执行权限"
        
        # 检查脚本内容基本结构
        with open(test_script, 'r', encoding='utf-8') as f:
            content = f.read()
        
        assert content.startswith('#!/bin/bash') or content.startswith('#!/bin/sh'), "测试脚本缺少shebang"
        assert len(content.strip()) > 0, "测试脚本内容为空"

    def test_scripts_directory_structure(self):
        """测试脚本目录结构完整性"""
        scripts_dir = Path("scripts")
        assert scripts_dir.exists(), "scripts目录不存在"
        assert scripts_dir.is_dir(), "scripts不是目录"
        
        required_scripts = ["build.sh", "test.sh"]
        for script_name in required_scripts:
            script_path = scripts_dir / script_name
            assert script_path.exists(), f"必需的脚本 {script_name} 不存在"

class TestWorkflowIntegration:
    """测试工作流集成"""
    
    def test_workflow_files_yaml_syntax(self):
        """测试所有工作流文件的YAML语法正确性"""
        workflow_dir = Path(".github/workflows")
        if not workflow_dir.exists():
            pytest.skip("工作流目录不存在")
        
        yaml_files = list(workflow_dir.glob("*.yml")) + list(workflow_dir.glob("*.yaml"))
        assert len(yaml_files) > 0, "没有找到任何工作流文件"
        
        for yaml_file in yaml_files:
            try:
                with open(yaml_file, 'r', encoding='utf-8') as f:
                    yaml.safe_load(f)
            except yaml.YAMLError as e:
                pytest.fail(f"工作流文件 {yaml_file.name} YAML语法错误: {e}")

    def test_github_workflows_directory_structure(self):
        """测试GitHub工作流目录结构正确性"""
        github_dir = Path(".github")
        assert github_dir.exists(), ".github目录不存在"
        
        workflows_dir = github_dir / "workflows"
        assert workflows_dir.exists(), ".github/workflows目录不存在"
        assert workflows_dir.is_dir(), ".github/workflows不是目录"
        
        expected_workflows = ["ci.yml", "cd.