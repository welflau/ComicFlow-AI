const jwt = require('jsonwebtoken');
const User = require('../models/User');
const AppError = require('../utils/AppError');
const catchAsync = require('../utils/catchAsync');

module.exports = catchAsync(async (req, res, next) => {
  // 获取token
  let token;
  if (req.headers.authorization && req.headers.authorization.startsWith('Bearer')) {
    token = req.headers.authorization.split(' ')[1];
  }

  if (!token) {
    return next(new AppError('请先登录', 401));
  }

  try {
    // 验证token
    const decoded = jwt.verify(token, process.env.JWT_SECRET);
    
    // 查找用户
    const user = await User.findById(decoded.userId);
    if (!user) {
      return next(new AppError('用户不存在', 401));
    }

    // 检查用户是否被禁用
    if (!user.isActive) {
      return next(new AppError('账户已被禁用', 403));
    }

    // 将用户信息添加到请求对象
    req.user = user;
    next();
  } catch (error) {
    if (error.name === 'JsonWebTokenError') {
      return next(new AppError('无效的令牌', 401));
    }
    if (error.name === 'TokenExpiredError') {
      return next(new AppError('令牌已过期', 401));
    }
    return next(new AppError('令牌验证失败', 401));
  }
});