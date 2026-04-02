const express = require('express');
const { body } = require('express-validator');
const authController = require('../controllers/authController');
const auth = require('../middleware/auth');
const validate = require('../middleware/validate');

const router = express.Router();

// 注册验证规则
const registerValidation = [
  body('username')
    .isLength({ min: 3, max: 20 })
    .withMessage('用户名长度必须在3-20个字符之间')
    .matches(/^[a-zA-Z0-9_]+$/)
    .withMessage('用户名只能包含字母、数字和下划线'),
  body('email')
    .isEmail()
    .withMessage('请输入有效的邮箱地址')
    .normalizeEmail(),
  body('password')
    .isLength({ min: 6 })
    .withMessage('密码至少6个字符')
    .matches(/^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)/)
    .withMessage('密码必须包含至少一个大写字母、一个小写字母和一个数字')
];

// 登录验证规则
const loginValidation = [
  body('email')
    .isEmail()
    .withMessage('请输入有效的邮箱地址')
    .normalizeEmail(),
  body('password')
    .notEmpty()
    .withMessage('密码不能为空')
];

// 修改密码验证规则
const changePasswordValidation = [
  body('currentPassword')
    .notEmpty()
    .withMessage('当前密码不能为空'),
  body('newPassword')
    .isLength({ min: 6 })
    .withMessage('新密码至少6个字符')
    .matches(/^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)/)
    .withMessage('新密码必须包含至少一个大写字母、一个小写字母和一个数字')
];

// 注册
router.post('/register', registerValidation, validate, authController.register);

// 登录
router.post('/login', loginValidation, validate, authController.login);

// 登出
router.post('/logout', auth, authController.logout);

// 刷新令牌
router.post('/refresh', authController.refreshToken);

// 获取当前用户信息
router.get('/me', auth, authController.getMe);

// 修改密码
router.put('/change-password', auth, changePasswordValidation, validate, authController.changePassword);

// 忘记密码
router.post('/forgot-password', [
  body('email').isEmail().withMessage('请输入有效的邮箱地址').normalizeEmail()
], validate, authController.forgotPassword);

// 重置密码
router.post('/reset-password', [
  body('token').notEmpty().withMessage('重置令牌不能为空'),
  body('password')
    .isLength({ min: 6 })
    .withMessage('密码至少6个字符')
    .matches(/^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)/)
    .withMessage('密码必须包含至少一个大写字母、一个小写字母和一个数字')
], validate, authController.resetPassword);

// 验证邮箱
router.get('/verify-email/:token', authController.verifyEmail);

// 重新发送验证邮件
router.post('/resend-verification', auth, authController.resendVerification);

module.exports = router;