# 架构设计 - 开发工具链配置

## 架构模式
开发工具链配置架构

## 技术栈

- **language**: JavaScript/Node.js
- **framework**: Express + 原生前端

## 模块设计

### ESLint配置模块
职责: JavaScript代码质量检查和规范约束
- .eslintrc.js - ESLint配置文件
- .eslintignore - 忽略文件配置
- package.json scripts - lint命令集成

### Prettier配置模块
职责: 代码格式化和美化
- .prettierrc - Prettier配置文件
- .prettierignore - 忽略文件配置
- package.json scripts - format命令集成

### Git Hooks配置模块
职责: Git提交前自动执行代码检查和格式化
- .husky/ - Git hooks配置目录
- lint-staged配置 - 暂存文件处理
- pre-commit hook - 提交前检查

### EditorConfig配置模块
职责: 统一编辑器配置和代码风格
- .editorconfig - 编辑器配置文件

### VSCode配置模块
职责: 开发环境配置和插件推荐
- .vscode/settings.json - 工作区设置
- .vscode/extensions.json - 推荐插件
- .vscode/launch.json - 调试配置

## 数据流
开发者编写代码 -> Git提交触发pre-commit hook -> 执行lint-staged -> 运行ESLint检查代码质量 -> 运行Prettier格式化代码 -> 检查通过后允许提交 -> CI/CD流水线进一步验证

## 关键决策
- 采用ESLint + Prettier组合确保代码质量和格式一致性
- 使用Husky管理Git hooks，在提交前自动执行代码检查
- 配置lint-staged只对暂存文件执行检查，提高效率
- 基于现有Express后端和原生前端架构配置相应的代码规范
- 集成VSCode配置提供统一的开发体验
- 建立分层的代码规范：基础规范 + 项目特定规范
