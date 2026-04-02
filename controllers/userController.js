const User = require('../models/User');
const AppError = require('../utils/AppError');
const catchAsync = require('../utils/catchAsync');

// 获取用户资料
exports.getProfile = catchAsync(async (req, res, next) => {
  res.json({
    success: true,
    data: {
      user: req.user
    }
  });
});

// 更新用户资料
exports.updateProfile = catchAsync(async (req, res, next) => {
  const allowedFields = ['username', 'email', 'profile'];
  const updates = {};

  // 只允许更新指定字段
  Object.keys(req.body).forEach(key => {
    if (allowedFields.includes(key)) {
      updates[key] = req.body[key];
    }
  });

  // 检查用户名和邮箱是否已被使用
  if (updates.username || updates.email) {
    const query = {
      _id: { $ne: req.user._id }
    };

    if (updates.username) {
      query.username = updates.username;
    }
    if (updates.email) {
      query.email = updates.email;
    }

    const existingUser = await User.findOne(query);
    if (existingUser) {
      if (existingUser.username === updates.username) {
        return next(new AppError('该用户名已被使用', 400));
      }
      if (existingUser.email === updates.email) {
        return next(new AppError('该邮箱已被注册', 400));
      }
    }
  }

  // 更新用户信息
  const user = await User.findByIdAndUpdate(
    req.user._id,
    updates,
    { new: true, runValidators: true }
  );

  res.json({
    success: true,
    message: '资料更新成功',
    data: {
      user
    }
  });
});

// 上传头像
exports.uploadAvatar = catchAsync(async (req, res, next) => {
  // 这里应该实现文件上传逻辑
  // 暂时返回成功消息
  res.json({
    success: true,
    message: '头像上传成功',
    data: {
      avatar: 'https://example.com/avatar.jpg'
    }
  });
});

// 删除头像
exports.deleteAvatar = catchAsync(async (req, res, next) => {
  await User.findByIdAndUpdate(req.user._id, {
    avatar: ''
  });

  res.json({
    success: true,
    message: '头像删除成功'
  });
});

// 获取用户列表（管理员）
exports.getUsers = catchAsync(async (req, res, next) => {
  const page = parseInt(req.query.page) || 1;
  const limit = parseInt(req.query.limit) || 10;
  const skip = (page - 1) * limit;

  const query = {};
  
  // 搜索条件
  if (req.query.search) {
    const searchRegex = new RegExp(req.query.search, 'i');
    query.$or = [
      { username: searchRegex },
      { email: searchRegex }
    ];
  }

  // 角色筛选
  if (req.query.role) {
    query.role = req.query.role;
  }

  // 状态筛选
  if (req.query.isActive !== undefined) {
    query.isActive = req.query.isActive === 'true';
  }

  const users = await User.find(query)
    .sort({ createdAt: -1 })
    .skip(skip)
    .limit(limit);

  const total = await User.countDocuments(query);

  res.json({
    success: true,
    data: {
      users,
      pagination: {
        current: page,
        pages: Math.ceil(total / limit),
        total
      }
    }
  });
});

// 获取指定用户信息（管理员）
exports.getUserById = catchAsync(async (req, res, next) => {
  const user = await User.findById(req.params.id);
  
  if (!user) {
    return next(new AppError('用户不存在', 404));
  }

  res.json({
    success: true,
    data: {
      user
    }
  });
});

// 更新用户状态（管理员）
exports.updateUserStatus = catchAsync(async (req, res, next) => {
  const { isActive } = req.body;
  
  const user = await User.findByIdAndUpdate(
    req.params.id,
    { isActive },
    { new: true }
  );

  if (!user) {
    return next(new AppError('用户不存在', 404));
  }

  res.json({
    success: true,
    message: `用户已${isActive ? '激活' : '禁用'}`,
    data: {
      user
    }
  });
});

// 更新用户角色（管理员）
exports.updateUserRole = catchAsync(async (req, res, next) => {
  const { role } = req.body;
  
  // 不能修改自己的角色
  if (req.params.id === req.user._id.toString()) {
    return next(new AppError('不能修改自己的角色', 400));
  }

  const user = await User.findByIdAndUpdate(
    req.params.id,
    { role },
    { new: true }
  );

  if (!user) {
    return next(new AppError('用户不存在', 404));
  }

  res.json({
    success: true,
    message: '用户角色更新成功',
    data: {
      user
    }
  });
});

// 删除用户（管理员）
exports.deleteUser = catchAsync(async (req, res, next) => {
  // 不能删除自己
  if (req.params.id === req.user._id.toString()) {
    return next(new AppError('不能删除自己的账户', 400));
  }

  const user = await User.findByIdAndDelete(req.params.id);
  
  if (!user) {
    return next(new AppError('用户不存在', 404));
  }

  res.json({
    success: true,
    message: '用户删除成功'
  });
});

// 获取用户统计信息（管理员）
exports.getUserStats = catchAsync(async (req, res, next) => {
  const stats = await User.aggregate([
    {
      $group: {
        _id: null,
        totalUsers: { $sum: 1 },
        activeUsers: {
          $sum: { $cond: [{ $eq: ['$isActive', true] }, 1, 0] }
        },
        adminUsers: {
          $sum: { $cond: [{ $eq: ['$role', 'admin'] }, 1, 0] }
        },
        verifiedUsers: {
          $sum: { $cond: [{ $eq: ['$emailVerified', true] }, 1, 0] }
        }
      }
    }
  ]);

  // 获取最近30天的注册统计
  const thirtyDaysAgo = new Date();
  thirtyDaysAgo.setDate(thirtyDaysAgo.getDate() - 30);

  const recentRegistrations = await User.countDocuments({
    createdAt: { $gte: thirtyDaysAgo }
  });

  res.json({
    success: true,
    data: {
      ...stats[0],
      recentRegistrations
    }
  });
});