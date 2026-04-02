# 架构设计 - 后端基础架构搭建

## 架构模式
分层架构 + MVC模式

## 技术栈

- **language**: JavaScript (Node.js)
- **framework**: Express.js

## 模块设计

### 应用入口层
职责: 服务器启动、中间件配置、全局错误处理
- app.js
- server.js
- middleware/index.js

### 路由层
职责: API路由定义、请求分发、参数验证
- routes/auth.js
- routes/users.js
- routes/index.js

### 控制器层
职责: 业务逻辑处理、请求响应、数据转换
- controllers/authController.js
- controllers/userController.js

### 中间件层
职责: 身份验证、日志记录、CORS处理、错误捕获
- middleware/auth.js
- middleware/logger.js
- middleware/cors.js
- middleware/errorHandler.js

### 数据库连接层
职责: 数据库连接池管理、连接配置
- config/database.js
- models/index.js

### 配置管理层
职责: 环境变量管理、应用配置
- config/index.js
- .env.example

## 数据流
客户端请求 -> Express路由 -> 中间件验证 -> 控制器处理 -> 数据库操作 -> 响应返回。支持JWT认证流程：登录请求 -> 验证用户 -> 生成Token -> 返回认证信息。后续请求携带Token -> 中间件验证 -> 业务处理

## 关键决策
- 选择Express.js作为Web框架，成熟稳定且生态丰富
- 采用分层架构，职责分离便于维护和扩展
- 使用JWT进行无状态身份认证
- 集成helmet、cors等安全中间件
- 预留数据库连接接口，支持后续PostgreSQL集成
- 建立统一的错误处理和日志记录机制
- 使用dotenv管理环境配置，支持多环境部署
