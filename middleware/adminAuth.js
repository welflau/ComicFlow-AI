const AppError = require('../utils/AppError');

module.exports = (req, res, next) => {
  if (req.user.role !== 'admin') {
    return next(new AppError('需要管理员权限', 403));
  }
  next();
};