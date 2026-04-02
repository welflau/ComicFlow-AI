# 用户认证系统后端

基于 Node.js + Express + MongoDB 构建的用户认证系统后端服务。

## 功能特性

- ✅ 用户注册/登录
- ✅ JWT 令牌认证
- ✅ 刷新令牌机制
- ✅ 密码加密存储
- ✅ 账户锁定机制
- ✅ 用户资料管理
- ✅ 管理员权限控制
- ✅ 输入验证
- ✅ 错误处理
- ✅ 安全中间件
- ✅ 请求速率限制

## 技术栈

- **Node.js** - 运行环境
- **Express** - Web 框架
- **MongoDB** - 数据库
- **Mongoose** - ODM
- **JWT** - 身份认证
- **bcryptjs** - 密码加密
- **express-validator** - 输入验证
- **helmet** - 安全头
- **cors** - 跨域处理
- **morgan** - 请求日志

## 快速开始

### 1. 安装依赖

```bash
npm install
```

### 2. 环境配置

复制 `.env` 文件并修改配置：

```bash
cp .env .env.local
```

主要配置项：
- `MONGODB_URI` - MongoDB 连接字符串
- `JWT_SECRET` - JWT 密钥
- `JWT_REFRESH_SECRET` - 刷新令牌密钥
- `PORT` - 服务器端口

### 3. 启动服务

开发模式：
```bash
npm run dev
```

生产模式：
```bash
npm start
```

## API 文档

### 认证相关

#### 注册
```http
POST /api/auth/register
Content-Type: application/json

{
  "username": "testuser",
  "email": "test@example.com",
  "password": "Password123"
}
```

#### 登录
```http
POST /api/auth/login
Content-Type: application/json

{
  "email": "test@example.com",
  "password": "Password123"
}
```

#### 刷新令牌
```http
POST /api/auth/refresh
Content-Type: application/json

{
  "refreshToken": "your_refresh_token"
}
```

#### 获取当前用户
```http
GET /api/auth/me
Authorization: Bearer your_access_token
```

### 用户管理

#### 更新资料
```http
PUT /api/users/profile
Authorization: Bearer your_access_token
Content-Type: application/json

{
  "username": "newusername",
  "profile": {
    "firstName": "John",
    "lastName": "Doe"
  }
}
```

#### 获取用户列表（管理员）
```http
GET /api/users?page=1&limit=10&search=keyword
Authorization: Bearer admin_access_token
```

## 项目结构

```
├── config/
│   └── database.js          # 数据库配置
├── controllers/
│   ├── authController.js    # 认证控制器
│   └── userController.js    # 用户控制器
├── middleware/
│   ├── auth.js             # 认证中间件
│   ├── adminAuth.js        # 管理员权限中间件
│   ├── validate.js         # 验证中间件
│   └── errorHandler.js     # 错误处理中间件
├── models/
│   └── User.js             # 用户模型
├── routes/
│   ├── auth.js             # 认证路由
│   └── users.js            # 用户路由
├── utils/
│   ├── AppError.js         # 自定义错误类
│   └── catchAsync.js       # 异步错误捕获
├── .env                    # 环境变量
├── .gitignore             # Git 忽略文件
├── package.json           # 项目配置
├── server.js              # 入口文件
└── README.md              # 项目说明
```

## 安全特性

- **密码加密**：使用 bcryptjs 进行密码哈希
- **JWT 认证**：访问令牌 + 刷新令牌机制
- **账户锁定**：连续登录失败后锁定账户
- **输入验证**：使用 express-validator 验证输入
- **安全头**：使用 helmet 设置安全 HTTP 头
- **速率限制**：防止暴力攻击
- **CORS 配置**：控制跨域访问

## 部署

### 环境要求
- Node.js 16+
- MongoDB 4.4+

### 生产环境配置
1. 设置环境变量 `NODE_ENV=production`
2. 使用强密码作为 JWT 密钥
3. 配置 MongoDB 连接字符串
4. 设置适当的 CORS 源
5. 配置反向代理（如 Nginx）

## 许可证

MIT License