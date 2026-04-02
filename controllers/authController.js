const User = require('../models/User');
const JWTUtils = require('../utils/jwt');
const PasswordService = require('../services/passwordService');
const { validationResult } = require('express-validator');

class AuthController {
  // 用户注册
  static async register(req, res) {
    try {
      // 验证输入
      const errors = validationResult(req);
      if (!errors.isEmpty()) {
        return res.status(400).json({
          success: false,
          message: 'Validation failed',
          errors: errors.array()
        });
      }

      const { username, email, password, role = 'user' } = req.body;

      // 检查用户是否已存在
      const existingUser = await User.findOne({
        $or: [{ email }, { username }]
      });

      if (existingUser) {
        return res.status(409).json({
          success: false,
          message: 'User already exists with this email or username'
        });
      }

      // 验证密码强度
      const passwordValidation = PasswordService.validatePasswordStrength(password);
      if (!passwordValidation.isValid) {
        return res.status(400).json({
          success: false,
          message: 'Password does not meet requirements',
          errors: passwordValidation.errors
        });
      }

      // 创建用户
      const user = await User.createUser({
        username,
        email,
        password,
        role
      });

      // 生成令牌
      const tokenPair = JWTUtils.generateTokenPair({
        userId: user._id,
        email: user.email,
        role: user.role
      });

      // 保存刷新令牌
      user.refreshTokens.push({ token: tokenPair.refreshToken });
      await user.save();

      res.status(201).json({
        success: true,
        message: 'User registered successfully',
        data: {
          user: user.toSafeObject(),
          tokens: tokenPair
        }
      });
    } catch (error) {
      console.error('Registration error:', error);
      res.status(500).json({
        success: false,
        message: 'Registration failed'
      });
    }
  }

  // 用户登录
  static async login(req, res) {
    try {
      const errors = validationResult(req);
      if (!errors.isEmpty()) {
        return res.status(400).json({
          success: false,
          message: 'Validation failed',
          errors: errors.array()
        });
      }

      const { email, password } = req.body;

      // 查找用户
      const user = await User.findByEmail(email);
      if (!user) {
        return res.status(401).json({
          success: false,
          message: 'Invalid credentials'
        });
      }

      // 检查用户是否活跃
      if (!user.isActive) {
        return res.status(401).json({
          success: false,
          message: 'Account is deactivated'
        });
      }

      // 验证密码
      const isValidPassword = await user.validatePassword(password);
      if (!isValidPassword) {
        return res.status(401).json({
          success: false,
          message: 'Invalid credentials'
        });
      }

      // 生成令牌
      const tokenPair = JWTUtils.generateTokenPair({
        userId: user._id,
        email: user.email,
        role: user.role
      });

      // 保存刷新令牌
      user.refreshTokens.push({ token: tokenPair.refreshToken });
      await user.save();

      res.json({
        success: true,
        message: 'Login successful',
        data: {
          user: user.toSafeObject(),
          tokens: tokenPair
        }
      });
    } catch (error) {
      console.error('Login error:', error);
      res.status(500).json({
        success: false,
        message: 'Login failed'
      });
    }
  }

  // 刷新令牌
  static async refresh(req, res) {
    try {
      const { refreshToken } = req.body;

      if (!refreshToken) {
        return res.status(401).json({
          success: false,
          message: 'Refresh token required'
        });
      }

      // 验证刷新令牌
      const decoded = JWTUtils.verifyRefreshToken(refreshToken);
      
      // 查找用户并验证刷新令牌
      const user = await User.findById(decoded.userId);
      if (!user || !user.isActive) {
        return res.status(401).json({
          success: false,
          message: 'User not found or inactive'
        });
      }

      const tokenExists = user.refreshTokens.some(t => t.token === refreshToken);
      if (!tokenExists) {
        return res.status(401).json({
          success: false,
          message: 'Invalid refresh token'
        });
      }

      // 生成新的令牌对
      const newTokenPair = JWTUtils.generateTokenPair({
        userId: user._id,
        email: user.email,
        role: user.role
      });

      // 移除旧的刷新令牌，添加新的
      user.refreshTokens = user.refreshTokens.filter(t => t.token !== refreshToken);
      user.refreshTokens.push({ token: newTokenPair.refreshToken });
      await user.save();

      res.json({
        success: true,
        message: 'Token refreshed successfully',
        data: {
          tokens: newTokenPair
        }
      });
    } catch (error) {
      console.error('Token refresh error:', error);
      res.status(401).json({
        success: false,
        message: 'Token refresh failed'
      });
    }
  }

  // 用户登出
  static async logout(req, res) {
    try {
      const { refreshToken } = req.body;
      const userId = req.user?.id;

      if (userId && refreshToken) {
        const user = await User.findById(userId);
        if (user) {
          user.refreshTokens = user.refreshTokens.filter(t => t.token !== refreshToken);
          await user.save();
        }
      }

      res.json({
        success: true,
        message: 'Logout successful'
      });
    } catch (error) {
      console.error('Logout error:', error);
      res.status(500).json({
        success: false,
        message: 'Logout failed'
      });
    }
  }

  // 登出所有设备
  static async logoutAll(req, res) {
    try {
      const userId = req.user.id;
      
      const user = await User.findById(userId);
      if (user) {
        user.refreshTokens = [];
        await user.save();
      }

      res.json({
        success: true,
        message: 'Logged out from all devices'
      });
    } catch (error) {
      console.error('Logout all error:', error);
      res.status(500).json({
        success: false,
        message: 'Logout all failed'
      });
    }
  }
}

module.exports = AuthController;