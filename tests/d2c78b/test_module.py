import pytest
import json
import os
from pathlib import Path
from unittest.mock import patch, MagicMock
import sys

# 获取项目根目录
PROJECT_ROOT = Path(__file__).parent
BACKEND_DIR = PROJECT_ROOT / "backend"

class TestBackendInfrastructure:
    
    def test_package_json_exists_and_valid(self):
        """测试 package.json 文件是否存在且包含必要的配置信息"""
        package_json_path = BACKEND_DIR / "package.json"
        
        # 检查文件是否存在
        assert package_json_path.exists(), "package.json 文件不存在"
        
        # 检查文件是否为有效的 JSON 格式
        with open(package_json_path, 'r', encoding='utf-8') as f:
            package_data = json.load(f)
        
        # 检查必要的字段
        assert "name" in package_data, "package.json 缺少 name 字段"
        assert "version" in package_data, "package.json 缺少 version 字段"
        assert "dependencies" in package_data, "package.json 缺少 dependencies 字段"
        
        # 检查是否包含常见的后端依赖
        dependencies = package_data.get("dependencies", {})
        backend_packages = ["express", "mongoose", "dotenv", "cors"]
        found_packages = [pkg for pkg in backend_packages if pkg in dependencies]
        assert len(found_packages) > 0, "package.json 中未找到常见的后端依赖包"

    def test_server_js_structure_and_imports(self):
        """测试 server.js 文件是否存在且包含基本的服务器配置代码"""
        server_js_path = BACKEND_DIR / "server.js"
        
        # 检查文件是否存在
        assert server_js_path.exists(), "server.js 文件不存在"
        
        # 读取文件内容
        with open(server_js_path, 'r', encoding='utf-8') as f:
            server_content = f.read()
        
        # 检查是否包含基本的服务器配置
        required_imports = ["express", "require"]
        for import_item in required_imports:
            assert import_item in server_content, f"server.js 中缺少 {import_item} 相关代码"
        
        # 检查是否包含端口配置和服务器启动代码
        server_keywords = ["listen", "port", "app"]
        found_keywords = [keyword for keyword in server_keywords if keyword in server_content.lower()]
        assert len(found_keywords) >= 2, "server.js 中缺少基本的服务器启动配置"

    def test_env_file_and_database_config(self):
        """测试环境配置文件和数据库配置文件是否存在且格式正确"""
        env_path = BACKEND_DIR / ".env"
        db_config_path = BACKEND_DIR / "config" / "database.js"
        
        # 检查 .env 文件是否存在
        assert env_path.exists(), ".env 文件不存在"
        
        # 读取 .env 文件内容
        with open(env_path, 'r', encoding='utf-8') as f:
            env_content = f.read()
        
        # 检查是否包含数据库相关的环境变量
        env_variables = ["PORT", "DB", "DATABASE", "MONGO"]
        found_variables = [var for var in env_variables if var in env_content.upper()]
        assert len(found_variables) > 0, ".env 文件中缺少数据库相关的环境变量"
        
        # 检查数据库配置文件是否存在
        assert db_config_path.exists(), "config/database.js 文件不存在"
        
        # 读取数据库配置文件内容
        with open(db_config_path, 'r', encoding='utf-8') as f:
            db_config_content = f.read()
        
        # 检查是否包含数据库连接相关代码
        db_keywords = ["connect", "mongoose", "database", "module.exports"]
        found_db_keywords = [keyword for keyword in db_keywords if keyword.lower() in db_config_content.lower()]
        assert len(found_db_keywords) >= 2, "database.js 中缺少数据库连接相关配置"

    def test_user_model_structure(self):
        """测试用户模型文件是否存在且包含正确的模型定义"""
        user_model_path = BACKEND_DIR / "models" / "User.js"
        
        # 检查文件是否存在
        assert user_model_path.exists(), "models/User.js 文件不存在"
        
        # 读取用户模型文件内容
        with open(user_model_path, 'r', encoding='utf-8') as f:
            user_model_content = f.read()
        
        # 检查是否包含 Mongoose 模型相关代码
        model_keywords = ["schema", "model", "mongoose", "module.exports"]
        for keyword in model_keywords:
            assert keyword.lower() in user_model_content.lower(), f"User.js 中缺少 {keyword} 相关代码"
        
        # 检查是否包含用户模型的基本字段
        user_fields = ["name", "email", "password", "username"]
        found_fields = [field for field in user_fields if field.lower() in user_model_content.lower()]
        assert len(found_fields) >= 2, "User.js 中缺少基本的用户字段定义"

    def test_backend_directory_structure(self):
        """测试后端项目的目录结构是否完整"""
        # 检查主要目录是否存在
        required_dirs = ["config", "models"]
        for dir_name in required_dirs:
            dir_path = BACKEND_DIR / dir_name
            assert dir_path.exists() and dir_path.is_dir(), f"{dir_name} 目录不存在"
        
        # 检查主要文件是否存在
        required_files = ["package.json", "server.js", ".env"]
        for file_name in required_files:
            file_path = BACKEND_DIR / file_name
            assert file_path.exists() and file_path.is_file(), f"{file_name} 文件不存在"

    @patch('builtins.open')
    def test_config_files_can_be_imported(self, mock_open):
        """测试配置文件的导入功能和返回类型是否正确"""
        # 模拟数据库配置文件内容
        mock_db_config = """
        const mongoose = require('mongoose');
        
        const connectDB = async () => {
            try {
                await mongoose.connect(process.env.MONGODB_URI);
                console.log('MongoDB connected');
            } catch (error) {
                console.error(error);
            }
        };
        
        module.exports = connectDB;
        """
        
        mock_open.return_value.__enter__.return_value.read.return_value = mock_db_config
        
        db_config_path = BACKEND_DIR / "config" / "database.js"
        
        # 检查文件是否可以被读取
        if db_config_path.exists():
            with open