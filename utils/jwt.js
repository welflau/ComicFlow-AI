const jwt = require('jsonwebtoken');

class JWTUtils {
  // 生成访问令牌
  static generateAccessToken(payload) {
    return jwt.sign(
      payload,
      process.env.JWT_SECRET,
      { 
        expiresIn: process.env.JWT_EXPIRE || '15m',
        issuer: 'auth-service',
        audience: 'auth-client'
      }
    );
  }

  // 生成刷新令牌
  static generateRefreshToken(payload) {
    return jwt.sign(
      payload,
      process.env.JWT_REFRESH_SECRET,
      { 
        expiresIn: process.env.JWT_REFRESH_EXPIRE || '7d',
        issuer: 'auth-service',
        audience: 'auth-client'
      }
    );
  }

  // 验证访问令牌
  static verifyAccessToken(token) {
    try {
      return jwt.verify(token, process.env.JWT_SECRET, {
        issuer: 'auth-service',
        audience: 'auth-client'
      });
    } catch (error) {
      throw new Error('Invalid access token');
    }
  }

  // 验证刷新令牌
  static verifyRefreshToken(token) {
    try {
      return jwt.verify(token, process.env.JWT_REFRESH_SECRET, {
        issuer: 'auth-service',
        audience: 'auth-client'
      });
    } catch (error) {
      throw new Error('Invalid refresh token');
    }
  }

  // 解码令牌（不验证）
  static decodeToken(token) {
    return jwt.decode(token);
  }

  // 生成令牌对
  static generateTokenPair(payload) {
    const accessToken = this.generateAccessToken(payload);
    const refreshToken = this.generateRefreshToken(payload);
    
    return {
      accessToken,
      refreshToken,
      tokenType: 'Bearer',
      expiresIn: process.env.JWT_EXPIRE || '15m'
    };
  }
}

module.exports = JWTUtils;