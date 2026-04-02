# 架构设计 - Docker容器化配置

## 架构模式
容器化微服务架构

## 技术栈

- **language**: JavaScript/Node.js
- **framework**: Docker + Docker Compose
- **tools**: Docker, Docker Compose, Nginx, PostgreSQL, Redis

## 模块设计

### 前端容器配置
职责: 为现有的HTML/JS前端应用创建Docker镜像，配置Nginx服务器
- Dockerfile.frontend - 前端应用容器化配置
- nginx.conf - Nginx反向代理配置
- 静态资源服务接口

### 后端容器配置
职责: 为Node.js API服务创建Docker镜像，包含认证和用户管理功能
- Dockerfile.backend - 后端API容器化配置
- package.json - 依赖管理
- 健康检查接口

### 数据库容器配置
职责: 配置PostgreSQL和Redis数据库容器，包含初始化脚本
- init.sql - 数据库初始化脚本
- redis.conf - Redis配置文件
- 数据持久化卷映射

### 开发环境编排
职责: 使用Docker Compose编排所有服务，配置网络和数据卷
- docker-compose.yml - 服务编排配置
- docker-compose.dev.yml - 开发环境覆盖配置
- 环境变量配置文件

### 容器化工具脚本
职责: 提供容器管理的便捷脚本和开发工具
- scripts/docker-dev.sh - 开发环境启动脚本
- scripts/docker-build.sh - 镜像构建脚本
- 健康检查和日志查看工具

## 数据流
开发者通过docker-compose启动完整开发环境 -> Nginx容器提供前端静态文件服务 -> 前端通过反向代理访问后端API -> Node.js容器处理API请求 -> 连接PostgreSQL容器进行数据操作 -> Redis容器提供缓存和会话存储 -> 所有容器通过Docker网络通信，数据通过卷持久化

## 关键决策
- 使用多阶段构建优化镜像大小，前端使用Nginx作为Web服务器
- 采用Docker Compose编排服务，支持一键启动完整开发环境
- 配置开发和生产两套环境，通过环境变量区分配置
- 使用命名卷持久化数据库数据，避免容器重启数据丢失
- 配置健康检查确保服务可用性，设置合理的重启策略
- 前端容器复用现有的public/index.html，不改变现有页面结构
