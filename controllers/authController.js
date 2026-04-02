const jwt = require('jsonwebtoken');
const User = require('../models/User');
const AppError = require('../utils/AppError');
const catchAsync = require('../utils/catchAsync');

// 生成JWT令牌
const generateToken = (userId) => {
  return jwt.sign({ userId }, process.env.JWT_SECRET, {
    expiresIn: process.env.JWT_EXPIRE
  });
};

// 生成刷新令牌
const generateRefreshToken = (userId) => {
  return jwt.sign({ userId }, process.env.JWT_REFRESH_SECRET, {
    expiresIn: process.env.JWT_REFRESH_EXPIRE
  });
};

// 注册
exports.register = catchAsync(async (req, res, next) => {
  const { username, email, password } = req.body;

  // 检查用户是否已存在
  const existingUser = await User.findOne({
    $or: [{ email }, { username }]
  });

  if (existingUser) {
    if (existingUser.email === email) {
      return next(new AppError('该邮箱已被注册', 400));
    }
    if (existingUser.username === username) {
      return next(new AppError('该用户名已被使用', 400));
    }
  }

  // 创建新用户
  const user = await User.create({
    username,
    email,
    password
  });

  // 生成令牌
  const token = generateToken(user._id);
  const refreshToken = generateRefreshToken(user._id);

  // 保存刷新令牌
  await user.addRefreshToken(refreshToken);

  res.status(201).json({
    success: true,
    message: '注册成功',
    data: {
      user,
      token,
      refreshToken
    }
  });
});

// 登录
exports.login = catchAsync(async (req, res, next) => {
  const { email, password } = req.body;

  // 查找用户（包含密码字段）
  const user = await User.findOne({ email }).select('+password');

  if (!user) {
    return next(new AppError('邮箱或密码错误', 401));
  }

  // 检查账户是否被锁定
  if (user.isLocked()) {
    return next(new AppError('账户已被锁定，请稍后再试', 423));
  }

  // 检查账户是否激活
  if (!user.isActive) {
    return next(new AppError('账户已被禁用', 403));
  }

  // 验证密码
  const isPasswordValid = await user.comparePassword(password);

  if (!isPasswordValid) {
    // 增加登录尝试次数
    await user.incLoginAttempts();
    return next(new AppError('邮箱或密码错误', 401));
  }

  // 重置登录尝试次数
  if (user.loginAttempts > 0) {
    await user.resetLoginAttempts();
  }

  // 更新最后登录时间
  user.lastLogin = new Date();
  await user.save();

  // 生成令牌
  const token = generateToken(user._id);
  const refreshToken = generateRefreshToken(user._id);

  // 保存刷新令牌
  await user.addRefreshToken(refreshToken);

  res.json({
    success: true,
    message: '登录成功',
    data: {
      user,
      token,
      refreshToken
    }
  });
});

// 登出
exports.logout = catchAsync(async (req, res, next) => {
  const refreshToken = req.body.refreshToken;
  
  if (refreshToken) {
    // 从用户记录中移除刷新令牌
    await req.user.removeRefreshToken(refreshToken);
  }

  res.json({
    success: true,
    message: '登出成功'
  });
});

// 刷新令牌
exports.refreshToken = catchAsync(async (req, res, next) => {
  const { refreshToken } = req.body;

  if (!refreshToken) {
    return next(new AppError('刷新令牌不能为空', 400));
  }

  try {
    // 验证刷新令牌
    const decoded = jwt.verify(refreshToken, process.env.JWT_REFRESH_SECRET);
    
    // 查找用户
    const user = await User.findById(decoded.userId);
    if (!user) {
      return next(new AppError('用户不存在', 404));
    }

    // 检查刷新令牌是否存在于用户记录中
    const tokenExists = user.refreshTokens.some(rt => rt.token === refreshToken);
    if (!tokenExists) {
      return next(new AppError('无效的刷新令牌', 401));
    }

    // 生成新的访问令牌
    const newToken = generateToken(user._id);
    const newRefreshToken = generateRefreshToken(user._id);

    // 替换旧的刷新令牌
    await user.removeRefreshToken(refreshToken);
    await user.addRefreshToken(newRefreshToken);

    res.json({
      success: true,
      message: '令牌刷新成功',
      data: {
        token: newToken,
        refreshToken: newRefreshToken
      }
    });
  } catch (error) {
    return next(new AppError('无效的刷新令牌', 401));
  }
});

// 获取当前用户信息
exports.getMe = catchAsync(async (req, res, next) => {
  res.json({
    success: true,
    data: {
      user: req.user
    }
  });
});

// 修改密码
exports.changePassword = catchAsync(async (req, res, next) => {
  const { currentPassword, newPassword } = req.body;

  // 获取用户（包含密码）
  const user = await User.findById(req.user._id).select('+password');

  // 验证当前密码
  const isCurrentPasswordValid = await user.comparePassword(currentPassword);
  if (!isCurrentPasswordValid) {
    return next(new AppError('当前密码错误', 400));
  }

  // 检查新密码是否与当前密码相同
  const isSamePassword = await user.comparePassword(newPassword);
  if (isSamePassword) {
    return next(new AppError('新密码不能与当前密码相同', 400));
  }

  // 更新密码
  user.password = newPassword;
  await user.save();

  // 清除所有刷新令牌（强制重新登录）
  user.refreshTokens = [];
  await user.save();

  res.json({
    success: true,
    message: '密码修改成功，请重新登录'
  });
});

// 忘记密码
exports.forgotPassword = catchAsync(async (req, res, next) => {
  // 这里应该实现发送重置密码邮件的逻辑
  // 暂时返回成功消息
  res.json({
    success: true,
    message: '密码重置邮件已发送，请查收'
  });
});

// 重置密码
exports.resetPassword = catchAsync(async (req, res, next) => {
  // 这里应该实现重置密码的逻辑
  // 暂时返回成功消息
  res.json({
    success: true,
    message: '密码重置成功'
  });
});

// 验证邮箱
exports.verifyEmail = catchAsync(async (req, res, next) => {
  // 这里应该实现邮箱验证的逻辑
  // 暂时返回成功消息
  res.json({
    success: true,
    message: '邮箱验证成功'
  });
});

// 重新发送验证邮件
exports.resendVerification = catchAsync(async (req, res, next) => {
  // 这里应该实现重新发送验证邮件的逻辑
  // 暂时返回成功消息
  res.json({
    success: true,
    message: '验证邮件已重新发送'
  });
});