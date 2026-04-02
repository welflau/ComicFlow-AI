# 架构设计 - WebSocket实时协作后端

## 架构模式
WebSocket实时协作架构

## 技术栈

- **language**: JavaScript
- **framework**: Express.js + Socket.IO

## 模块设计

### WebSocket服务器
职责: 管理WebSocket连接、房间管理、消息广播
- connection事件处理
- joinCanvas房间加入
- leaveCanvas房间离开
- canvasUpdate画布更新广播

### 协作会话管理器
职责: 管理画布会话、用户状态、冲突解决
- createSession创建会话
- getUsersInSession获取会话用户
- handleConflict处理操作冲突
- syncCanvasState同步画布状态

### 操作事件处理器
职责: 处理画布操作事件、数据验证、状态更新
- handleNodeCreate节点创建
- handleNodeUpdate节点更新
- handleNodeDelete节点删除
- handleConnectionCreate连线创建

### 数据持久化服务
职责: 画布状态持久化、操作历史记录
- saveCanvasState保存画布状态
- loadCanvasState加载画布状态
- saveOperation保存操作记录
- getOperationHistory获取操作历史

## 数据流
客户端通过WebSocket连接到服务器 -> 加入特定画布房间 -> 发送操作事件(节点创建/更新/删除/连线) -> 服务器验证并广播给房间内其他用户 -> 同时持久化到数据库 -> 处理操作冲突并同步最终状态

## 关键决策
- 使用Socket.IO作为WebSocket库，提供更好的浏览器兼容性和重连机制
- 采用房间(Room)机制隔离不同画布的协作会话
- 实现操作事件驱动的架构，每个画布操作都作为事件处理
- 使用乐观锁机制处理并发操作冲突
- 在现有Express.js架构基础上集成WebSocket服务
- 复用现有的用户认证中间件进行WebSocket连接验证
