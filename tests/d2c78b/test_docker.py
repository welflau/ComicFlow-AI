import pytest
from pathlib import Path
import os
import subprocess
import json
import yaml

class TestDockerDeployment:
    
    def test_dockerfile_exists_and_valid(self):
        """测试Dockerfile文件是否存在且包含必要的配置指令"""
        dockerfile_path = Path("Dockerfile")
        assert dockerfile_path.exists(), "Dockerfile文件不存在"
        
        content = dockerfile_path.read_text(encoding='utf-8')
        assert "FROM" in content, "Dockerfile缺少FROM指令"
        assert "WORKDIR" in content or "RUN" in content, "Dockerfile缺少基本配置指令"
        assert len(content.strip()) > 0, "Dockerfile内容为空"

    def test_docker_compose_configuration(self):
        """测试docker-compose配置文件是否存在且格式正确"""
        compose_files = [
            Path("docker-compose.yml"),
            Path("docker-compose.yaml"),
            Path("compose.yml"),
            Path("compose.yaml")
        ]
        
        compose_file = None
        for file_path in compose_files:
            if file_path.exists():
                compose_file = file_path
                break
        
        assert compose_file is not None, "未找到docker-compose配置文件"
        
        content = compose_file.read_text(encoding='utf-8')
        try:
            config = yaml.safe_load(content)
            assert isinstance(config, dict), "docker-compose配置格式无效"
            assert "services" in config, "docker-compose配置缺少services部分"
            assert len(config["services"]) > 0, "docker-compose配置中没有定义任何服务"
        except yaml.YAMLError:
            pytest.fail("docker-compose配置文件YAML格式错误")

    def test_deployment_scripts_executable(self):
        """测试部署相关脚本文件是否存在且可执行"""
        script_patterns = [
            "deploy.sh",
            "start.sh", 
            "build.sh",
            "run.sh"
        ]
        
        found_scripts = []
        for pattern in script_patterns:
            script_path = Path(pattern)
            if script_path.exists():
                found_scripts.append(script_path)
        
        assert len(found_scripts) > 0, "未找到任何部署脚本文件"
        
        for script in found_scripts:
            content = script.read_text(encoding='utf-8')
            assert content.startswith('#!/bin/bash') or content.startswith('#!/bin/sh'), f"脚本{script}缺少shebang声明"
            assert len(content.strip()) > 10, f"脚本{script}内容过短，可能不完整"

    def test_environment_configuration_files(self):
        """测试环境配置文件是否存在且包含必要配置项"""
        env_files = [
            Path(".env"),
            Path(".env.example"),
            Path("config.json"),
            Path("app.config")
        ]
        
        found_configs = [f for f in env_files if f.exists()]
        assert len(found_configs) > 0, "未找到任何环境配置文件"
        
        for config_file in found_configs:
            content = config_file.read_text(encoding='utf-8')
            assert len(content.strip()) > 0, f"配置文件{config_file}内容为空"
            
            if config_file.suffix == '.json':
                try:
                    json.loads(content)
                except json.JSONDecodeError:
                    pytest.fail(f"JSON配置文件{config_file}格式错误")

    def test_project_structure_for_containerization(self):
        """测试项目结构是否适合容器化部署"""
        current_dir = Path(".")
        
        # 检查是否有源代码目录
        source_dirs = ["src", "app", "web", "server", "client"]
        has_source = any((current_dir / d).exists() for d in source_dirs)
        
        # 检查是否有依赖管理文件
        dependency_files = [
            "requirements.txt", "package.json", "Pipfile", 
            "poetry.lock", "go.mod", "pom.xml", "Cargo.toml"
        ]
        has_dependencies = any((current_dir / f).exists() for f in dependency_files)
        
        assert has_source or has_dependencies, "项目缺少明确的源代码目录或依赖管理文件"
        
        # 检查是否有忽略文件
        ignore_files = [".dockerignore", ".gitignore"]
        has_ignore = any((current_dir / f).exists() for f in ignore_files)
        
        if not has_ignore:
            print("警告: 建议添加.dockerignore文件以优化构建过程")