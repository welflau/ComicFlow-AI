const express = require('express');
const jwt = require('jsonwebtoken');
const bcrypt = require('bcrypt');
const cors = require('cors');
const rateLimit = require('express-rate-limit');
const helmet = require('helmet');

const app = express();
const PORT = process.env.PORT || 3000;
const JWT_SECRET = process.env.JWT_SECRET || 'your-super-secret-jwt-key';
const JWT_REFRESH_SECRET = process.env.JWT_REFRESH_SECRET || 'your-super-secret-refresh-key';

// 中间件配置
app.use(helmet());
app.use(cors());
app.use(express.json({ limit: '10mb' }));
app.use(express.urlencoded({ extended: true }));

// 速率限制
const authLimiter = rateLimit({
    windowMs: 15 * 60 * 1000, // 15分钟
    max: 5, // 限制每个IP 15分钟内最多5次认证请求
    message: { error: '请求过于频繁，请稍后再试' },
    standardHeaders: true,
    legacyHeaders: false
});

// 模拟数据库（实际应用中应使用真实数据库）
let users = [
    {
        id: '1',
        username: 'admin',
        email: 'admin@example.com',
        password: '$2b$10$rQZ8kHWfQxwjKV.vQZ8kHWfQxwjKV.vQZ8kHWfQxwjKV.vQZ8kHWfQ', // 'admin123'
        role: 'admin',
        createdAt: new Date().toISOString(),
        lastLogin: null
    }
];

let refreshTokens = []; // 存储有效的刷新令牌

// JWT工具类
class JWTUtils {
    static generateAccessToken(payload) {
        return jwt.sign(payload, JWT_SECRET, { 
            expiresIn: '1h',
            issuer: 'auth-service',
            audience: 'auth-client'
        });
    }
    
    static generateRefreshToken(payload) {
        return jwt.sign(payload, JWT_REFRESH_SECRET, { 
            expiresIn: '7d',
            issuer: 'auth-service',
            audience: 'auth-client'
        });
    }
    
    static verifyToken(token, secret = JWT_SECRET) {
        try {
            return jwt.verify(token, secret, {
                issuer: 'auth-service',
                audience: 'auth-client'
            });
        } catch (error) {
            return null;
        }
    }
    
    static decodeToken(token) {
        try {
            return jwt.decode(token);
        } catch (error) {
            return null;
        }
    }
}

// 密码加密服务
class PasswordService {
    static async hashPassword(password) {
        const saltRounds = 12;
        return await bcrypt.hash(password, saltRounds);
    }
    
    static async comparePassword(password, hash) {
        return await bcrypt.compare(password, hash);
    }
}

// 用户模型
class UserModel {
    static async create(userData) {
        const existingUser = this.findByEmail(userData.email);
        if (existingUser) {
            throw new Error('邮箱已被注册');
        }
        
        const hashedPassword = await PasswordService.hashPassword(userData.password);
        const user = {
            id: Date.now().toString(),
            username: userData.username,
            email: userData.email,
            password: hashedPassword,
            role: userData.role || 'user',
            createdAt: new Date().toISOString(),
            lastLogin: null
        };
        
        users.push(user);
        
        // 返回用户信息（不包含密码）
        const { password, ...userInfo } = user;
        return userInfo;
    }
    
    static findByEmail(email) {
        return users.find(user => user.email === email);
    }
    
    static findById(id) {
        return users.find(user => user.id === id);
    }
    
    static async validatePassword(email, password) {
        const user = this.findByEmail(email);
        if (!user) return null;
        
        const isValid = await PasswordService.comparePassword(password, user.password);
        if (isValid) {
            // 更新最后登录时间
            user.lastLogin = new Date().toISOString();
            
            const { password: _, ...userInfo } = user;
            return userInfo;
        }
        return null;
    }
    
    static updateUser(id, updateData) {
        const userIndex = users.findIndex(user => user.id === id);
        if (userIndex === -1) return null;
        
        users[userIndex] = { ...users[userIndex], ...updateData };
        const { password, ...userInfo } = users[userIndex];
        return userInfo;
    }
}

// 认证中间件
class AuthMiddleware {
    static authenticateToken(req, res, next) {
        const authHeader = req.headers['authorization'];
        const token = authHeader && authHeader.split(' ')[1]; // Bearer TOKEN
        
        if (!token) {
            return res.status(401).json({ error: '访问令牌缺失' });
        }
        
        const payload = JWTUtils.verifyToken(token);
        if (!payload) {
            return res.status(403).json({ error: '访问令牌无效或已过期' });
        }
        
        req.user = payload;
        next();
    }
    
    static requireAuth(req, res, next) {
        AuthMiddleware.authenticateToken(req, res, next);
    }
    
    static requireRole(roles) {
        return (req, res, next) => {
            if (!req.user) {
                return res.status(401).json({ error: '未认证' });
            }
            
            const userRoles = Array.isArray(roles) ? roles : [roles];
            if (!userRoles.includes(req.user.role)) {
                return res.status(403).json({ error: '权限不足' });
            }
            
            next();
        };
    }
}

// 输入验证中间件
const validateRegistration = (req, res, next) => {
    const { username, email, password } = req.body;
    
    if (!username || username.length < 2) {
        return res.status(400).json({ error: '用户名至少需要2个字符' });
    }
    
    if (!email || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
        return res.status(400).json({ error: '请提供有效的邮箱地址' });
    }
    
    if (!password || password.length < 6) {
        return res.status(400).json({ error: '密码至少需要6个字符' });
    }
    
    next();
};

const validateLogin = (req, res, next) => {
    const { email, password } = req.body;
    
    if (!email || !password) {
        return res.status(400).json({ error: '邮箱和密码不能为空' });
    }
    
    next();
};

// 认证控制器
class AuthController {
    // 用户注册
    static async register(req, res) {
        try {
            const { username, email, password } = req.body;
            
            const user = await UserModel.create({ username, email, password });
            
            const accessToken = JWTUtils.generateAccessToken({
                userId: user.id,
                email: user.email,
                role: user.role
            });
            
            const refreshToken = JWTUtils.generateRefreshToken({
                userId: user.id
            });
            
            // 存储刷新令牌
            refreshTokens.push(refreshToken);
            
            res.status(201).json({
                message: '注册成功',
                user,
                accessToken,
                refreshToken
            });
        } catch (error) {
            res.status(400).json({ error: error.message });
        }
    }
    
    // 用户登录
    static async login(req, res) {
        try {
            const { email, password } = req.body;
            
            const user = await UserModel.validatePassword(email, password);
            if (!user) {
                return res.status(401).json({ error: '邮箱或密码错误' });
            }
            
            const accessToken = JWTUtils.generateAccessToken({
                userId: user.id,
                email: user.email,
                role: user.role
            });
            
            const refreshToken = JWTUtils.generateRefreshToken({
                userId: user.id
            });
            
            // 存储刷新令牌
            refreshTokens.push(refreshToken);
            
            res.json({
                message: '登录成功',
                user,
                accessToken,
                refreshToken
            });
        } catch (error) {
            res.status(500).json({ error: error.message });
        }
    }
    
    // 用户登出
    static logout(req, res) {
        const { refreshToken } = req.body;
        
        if (refreshToken) {
            // 从有效令牌列表中移除
            const tokenIndex = refreshTokens.indexOf(refreshToken);
            if (tokenIndex > -1) {
                refreshTokens.splice(tokenIndex, 1);
            }
        }
        
        res.json({ message: '登出成功' });
    }
    
    // 刷新访问令牌
    static refresh(req, res) {
        const { refreshToken } = req.body;
        
        if (!refreshToken) {
            return res.status(401).json({ error: '刷新令牌缺失' });
        }
        
        if (!refreshTokens.includes(refreshToken)) {
            return res.status(403).json({ error: '刷新令牌无效' });
        }
        
        const payload = JWTUtils.verifyToken(refreshToken, JWT_REFRESH_SECRET);
        if (!payload) {
            // 移除无效的刷新令牌
            const tokenIndex = refreshTokens.indexOf(refreshToken);
            if (tokenIndex > -1) {
                refreshTokens.splice(tokenIndex, 1);
            }
            return res.status(403).json({ error: '刷新令牌已过期' });
        }
        
        const user = UserModel.findById(payload.userId);
        if (!user) {
            return res.status(403).json({ error: '用户不存在' });
        }
        
        const { password, ...userInfo } = user;
        const newAccessToken = JWTUtils.generateAccessToken({
            userId: userInfo.id,
            email: userInfo.email,
            role: userInfo.role
        });
        
        res.json({
            message: '令牌刷新成功',
            user: userInfo,
            accessToken: newAccessToken
        });
    }
    
    // 获取当前用户信息
    static getCurrentUser(req, res) {
        const user = UserModel.findById(req.user.userId);
        if (!user) {
            return res.status(404).json({ error: '用户不存在' });
        }
        
        const { password, ...userInfo } = user;
        res.json({ user: userInfo });
    }
}

// 路由定义
app.post('/api/auth/register', authLimiter, validateRegistration, AuthController.register);
app.post('/api/auth/login', authLimiter, validateLogin, AuthController.login);
app.post('/api/auth/logout', AuthController.logout);
app.post('/api/auth/refresh', AuthController.refresh);
app.get('/api/auth/me', AuthMiddleware.requireAuth, AuthController.getCurrentUser);

// 受保护的路由示例
app.get('/api/admin/users', 
    AuthMiddleware.requireAuth, 
    AuthMiddleware.requireRole('admin'), 
    (req, res) => {
        const userList = users.map(({ password, ...user }) => user);
        res.json({ users: userList });
    }
);

app.get('/api/user/profile', 
    AuthMiddleware.requireAuth, 
    (req, res) => {
        const user = UserModel.findById(req.user.userId);
        if (!user) {
            return res.status(404).json({ error: '用户不存在' });
        }
        
        const { password, ...userInfo } = user;
        res.json({ profile: userInfo });
    }
);

// 健康检查端点
app.get('/api/health', (req, res) => {
    res.json({ 
        status: 'OK', 
        timestamp: new Date().toISOString(),
        uptime: process.uptime()
    });
});

// 错误处理中间件
app.use((error, req, res, next) => {
    console.error('Error:', error);
    res.status(500).json({ 
        error: '服务器内部错误',
        message: process.env.NODE_ENV === 'development' ? error.message : '请稍后重试'
    });
});

// 404处理
app.use('*', (req, res) => {
    res.status(404).json({ error: '接口不存在' });
});

// 启动服务器
app.listen(PORT, () => {
    console.log(`认证服务器运行在端口 ${PORT}`);
    console.log(`健康检查: http://localhost:${PORT}/api/health`);
});

// 优雅关闭
process.on('SIGTERM', () => {
    console.log('收到SIGTERM信号，正在关闭服务器...');
    process.exit(0);
});

process.on('SIGINT', () => {
    console.log('收到SIGINT信号，正在关闭服务器...');
    process.exit(0);
});

module.exports = app;