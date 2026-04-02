# 架构设计 - 用户认证模块开发

## 架构模式
分层架构 + JWT无状态认证

## 技术栈

- **language**: JavaScript/TypeScript
- **framework**: Node.js + Express

## 模块设计

### 认证控制器
职责: 处理用户注册、登录、登出请求，生成和验证JWT令牌
- POST /api/auth/register
- POST /api/auth/login
- POST /api/auth/logout
- POST /api/auth/refresh

### 用户模型
职责: 定义用户数据结构，提供用户CRUD操作方法
- User.create(userData)
- User.findByEmail(email)
- User.findById(id)
- User.validatePassword(password)

### JWT工具类
职责: JWT令牌的生成、验证、刷新功能
- generateAccessToken(payload)
- generateRefreshToken(payload)
- verifyToken(token)
- decodeToken(token)

### 认证中间件
职责: 验证请求中的JWT令牌，提取用户信息，权限检查
- authenticateToken(req, res, next)
- requireAuth(req, res, next)
- requireRole(roles)

### 密码加密服务
职责: 用户密码的哈希加密和验证
- hashPassword(password)
- comparePassword(password, hash)

## 数据流
用户提交登录信息 -> 认证控制器验证用户名密码 -> 密码加密服务比对哈希值 -> JWT工具类生成访问令牌和刷新令牌 -> 返回令牌给客户端 -> 后续请求携带令牌 -> 认证中间件验证令牌有效性 -> 提取用户信息注入请求上下文 -> 业务逻辑处理

## 关键决策
- 使用JWT无状态认证，避免服务端session存储
- 采用bcrypt进行密码哈希，安全强度设为12轮
- 实现双令牌机制：短期访问令牌(15分钟) + 长期刷新令牌(7天)
- 认证中间件支持可选认证和强制认证两种模式
- 用户密码字段在查询时默认排除，需要时显式包含
- 集成到现有Express路由系统，不影响已有API结构
