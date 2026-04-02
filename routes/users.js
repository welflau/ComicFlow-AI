const express = require('express');
const { body } = require('express-validator');
const userController = require('../controllers/userController');
const auth = require('../middleware/auth');
const adminAuth = require('../middleware/adminAuth');
const validate = require('../middleware/validate');

const router = express.Router();

// 更新用户资料验证规则
const updateProfileValidation = [
  body('username')
    .optional()
    .isLength({ min: 3, max: 20 })
    .withMessage('用户名长度必须在3-20个字符之间')
    .matches(/^[a-zA-Z0-9_]+$/)
    .withMessage('用户名只能包含字母、数字和下划线'),
  body('email')
    .optional()
    .isEmail()
    .withMessage('请输入有效的邮箱地址')
    .normalizeEmail(),
  body('profile.firstName')
    .optional()
    .isLength({ max: 50 })
    .withMessage('名字不能超过50个字符'),
  body('profile.lastName')
    .optional()
    .isLength({ max: 50 })
    .withMessage('姓氏不能超过50个字符'),
  body('profile.phone')
    .optional()
    .matches(/^[\d\-\+\(\)\s]+$/)
    .withMessage('请输入有效的电话号码'),
  body('profile.bio')
    .optional()
    .isLength({ max: 500 })
    .withMessage('个人简介不能超过500个字符'),
  body('profile.website')
    .optional()
    .isURL()
    .withMessage('请输入有效的网站地址')
];

// 获取当前用户资料
router.get('/profile', auth, userController.getProfile);

// 更新用户资料
router.put('/profile', auth, updateProfileValidation, validate, userController.updateProfile);

// 上传头像
router.post('/avatar', auth, userController.uploadAvatar);

// 删除头像
router.delete('/avatar', auth, userController.deleteAvatar);

// 获取用户列表（管理员）
router.get('/', auth, adminAuth, userController.getUsers);

// 获取指定用户信息（管理员）
router.get('/:id', auth, adminAuth, userController.getUserById);

// 更新用户状态（管理员）
router.put('/:id/status', auth, adminAuth, [
  body('isActive').isBoolean().withMessage('状态必须是布尔值')
], validate, userController.updateUserStatus);

// 更新用户角色（管理员）
router.put('/:id/role', auth, adminAuth, [
  body('role').isIn(['user', 'admin']).withMessage('角色必须是user或admin')
], validate, userController.updateUserRole);

// 删除用户（管理员）
router.delete('/:id', auth, adminAuth, userController.deleteUser);

// 获取用户统计信息（管理员）
router.get('/stats/overview', auth, adminAuth, userController.getUserStats);

module.exports = router;