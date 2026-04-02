# 架构设计 - WebSocket实时协作后端

## 架构模式
WebSocket实时协作架构

## 技术栈

- **language**: JavaScript
- **framework**: Node.js + Socket.IO

## 模块设计

### WebSocket服务器
职责: 处理WebSocket连接、房间管理、消息广播
- connection事件处理
- join-canvas房间加入
- canvas-update画布更新
- node-operation节点操作
- disconnect断开连接

### 协作状态管理器
职责: 管理画布状态、用户在线状态、操作冲突解决
- getCanvasState获取画布状态
- updateCanvasState更新画布状态
- getUsersInCanvas获取在线用户
- resolveConflict解决操作冲突

### 消息处理器
职责: 处理不同类型的协作消息、数据验证
- handleNodeMove处理节点移动
- handleNodeCreate处理节点创建
- handleNodeDelete处理节点删除
- handleConnection处理连线操作

### 持久化服务
职责: 画布状态持久化、操作日志记录
- saveCanvasState保存画布状态
- loadCanvasState加载画布状态
- logOperation记录操作日志

## 数据流
客户端通过Socket.IO连接WebSocket服务器 -> 加入特定画布房间 -> 发送操作消息(节点移动/创建/删除/连线) -> 服务器验证并广播给房间内其他用户 -> 协作状态管理器更新画布状态 -> 持久化服务保存状态到数据库 -> 其他客户端接收更新并同步画布

## 关键决策
- 使用Socket.IO作为WebSocket框架，提供更好的兼容性和重连机制
- 采用房间机制隔离不同画布的协作会话
- 实现操作时间戳机制解决并发冲突
- 使用内存缓存画布状态，定期持久化到数据库
- 支持用户光标位置实时同步增强协作体验
