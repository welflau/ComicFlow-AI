# 架构设计 - 对象存储服务集成

## 架构模式
微服务架构 - 对象存储服务层

## 技术栈

- **language**: Node.js
- **framework**: Express/Fastify + AWS SDK/阿里云OSS SDK

## 模块设计

### StorageService
职责: 封装对象存储操作，提供统一的文件上传下载接口
- uploadFile(file, bucket, key)
- downloadFile(bucket, key)
- deleteFile(bucket, key)
- generatePresignedUrl(bucket, key, expires)
- listFiles(bucket, prefix)

### FileController
职责: 处理文件相关的HTTP请求，调用StorageService
- POST /api/files/upload
- GET /api/files/:fileId
- DELETE /api/files/:fileId
- GET /api/files/:fileId/url
- GET /api/files

### FileModel
职责: 文件元数据的数据库模型
- create(fileMetadata)
- findById(id)
- findByUserId(userId)
- updateStatus(id, status)
- delete(id)

### UploadMiddleware
职责: 处理文件上传的中间件，包括文件验证和多部分解析
- validateFileType(allowedTypes)
- validateFileSize(maxSize)
- parseMultipart()
- generateUniqueKey()

## 数据流
客户端通过multipart/form-data上传文件 -> UploadMiddleware验证文件 -> FileController接收请求 -> StorageService上传到OSS/S3 -> FileModel保存元数据到数据库 -> 返回文件ID和访问URL给客户端。下载时通过文件ID查询元数据，生成预签名URL或直接返回文件流

## 关键决策
- 使用适配器模式支持多种对象存储服务(AWS S3, 阿里云OSS, 腾讯云COS)
- 文件上传采用预签名URL方式减少服务器负载
- 文件元数据存储在PostgreSQL中，包含文件路径、大小、类型等信息
- 实现文件分片上传支持大文件处理
- 添加文件访问权限控制和临时访问链接
- 配置CDN加速文件访问性能
