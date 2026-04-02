const JWTUtils = require('../utils/jwt');
const User = require('../models/User');

// 验证访问令牌
const authenticateToken = async (req, res, next) => {
  try {
    const authHeader = req.headers['authorization'];
    const token = authHeader && authHeader.split(' ')[1]; // Bearer TOKEN

    if (!token) {
      return res.status(401).json({
        success: false,
        message: 'Access token required'
      });
    }

    const decoded = JWTUtils.verifyAccessToken(token);
    
    // 验证用户是否仍然存在且活跃
    const user = await User.findById(decoded.userId);
    if (!user || !user.isActive) {
      return res.status(401).json({
        success: false,
        message: 'User not found or inactive'
      });
    }

    req.user = user.toSafeObject();
    next();
  } catch (error) {
    return res.status(403).json({
      success: false,
      message: 'Invalid or expired token'
    });
  }
};

// 要求认证
const requireAuth = (req, res, next) => {
  authenticateToken(req, res, next);
};

// 要求特定角色
const requireRole = (roles) => {
  return (req, res, next) => {
    if (!req.user) {
      return res.status(401).json({
        success: false,
        message: 'Authentication required'
      });
    }

    if (!roles.includes(req.user.role)) {
      return res.status(403).json({
        success: false,
        message: 'Insufficient permissions'
      });
    }

    next();
  };
};

// 可选认证（不强制要求token）
const optionalAuth = async (req, res, next) => {
  try {
    const authHeader = req.headers['authorization'];
    const token = authHeader && authHeader.split(' ')[1];

    if (token) {
      const decoded = JWTUtils.verifyAccessToken(token);
      const user = await User.findById(decoded.userId);
      
      if (user && user.isActive) {
        req.user = user.toSafeObject();
      }
    }
    
    next();
  } catch (error) {
    // 忽略token验证错误，继续处理请求
    next();
  }
};

module.exports = {
  authenticateToken,
  requireAuth,
  requireRole,
  optionalAuth
};