# 架构设计 - 前端实时协作集成

## 架构模式
WebSocket实时协作集成架构

## 技术栈

- **language**: JavaScript
- **framework**: 原生JavaScript + WebSocket

## 模块设计

### WebSocketManager
职责: 管理WebSocket连接、消息发送接收、连接状态维护
- connect()
- disconnect()
- sendMessage(type, data)
- onMessage(callback)
- onConnectionChange(callback)

### CollaborationManager
职责: 协作功能核心逻辑、用户状态同步、操作冲突处理
- joinCanvas(canvasId)
- leaveCanvas()
- broadcastOperation(operation)
- handleRemoteOperation(operation)
- getUserList()

### CanvasCollaborationUI
职责: 协作相关UI组件、用户头像显示、在线状态指示
- showOnlineUsers(users)
- showUserCursor(userId, position)
- hideUserCursor(userId)
- showOperationFeedback(operation)

### OperationSynchronizer
职责: 操作同步、冲突解决、本地状态与远程状态合并
- syncNodeOperation(nodeId, operation)
- syncConnectionOperation(connectionId, operation)
- resolveConflict(localOp, remoteOp)
- applyRemoteOperation(operation)

## 数据流
用户在画布上进行操作 -> OperationSynchronizer捕获操作 -> CollaborationManager处理并通过WebSocketManager发送 -> 服务器广播给其他用户 -> 其他用户的WebSocketManager接收消息 -> CollaborationManager处理远程操作 -> OperationSynchronizer应用到本地画布 -> CanvasCollaborationUI更新协作状态显示

## 关键决策
- 在现有index.html中添加协作功能模块，保持原有认证系统不变
- 使用原生WebSocket API而非第三方库，保持技术栈一致性
- 采用操作转换(OT)算法处理并发编辑冲突
- 实现用户光标同步和实时状态显示
- 集成到现有的Three.js画布系统中
- 使用事件驱动架构确保与现有节点系统的兼容性
