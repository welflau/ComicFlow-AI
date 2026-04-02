# 架构设计 - 前端实时协作集成

## 架构模式
WebSocket实时协作集成架构

## 技术栈

- **language**: JavaScript
- **framework**: 原生JavaScript + WebSocket API

## 模块设计

### WebSocketManager
职责: 管理WebSocket连接、消息路由和连接状态
- connect()
- disconnect()
- send(message)
- onMessage(callback)
- onConnectionChange(callback)

### CollaborationEngine
职责: 处理协作事件、冲突解决和状态同步
- handleNodeUpdate(nodeData)
- handleConnectionUpdate(connectionData)
- broadcastChange(changeData)
- resolveConflict(conflictData)

### PresenceManager
职责: 管理用户在线状态、光标位置和选择状态
- updateUserPresence(userId, presenceData)
- showUserCursor(userId, position)
- hideUserCursor(userId)
- highlightUserSelection(userId, selection)

### ChangeTracker
职责: 跟踪画布变更、生成操作记录和支持撤销重做
- trackChange(changeType, data)
- generateChangeId()
- applyRemoteChange(change)
- getChangeHistory()

### CollaborationUI
职责: 在现有index.html中添加协作相关UI组件
- showOnlineUsers()
- displayUserCursors()
- showConflictDialog()
- updateConnectionStatus()

## 数据流
1. 用户在画布上进行操作(拖拽节点/创建连线) -> 2. ChangeTracker记录变更并生成唯一ID -> 3. CollaborationEngine处理变更数据 -> 4. WebSocketManager发送变更到服务器 -> 5. 服务器广播给其他用户 -> 6. 其他客户端接收变更 -> 7. CollaborationEngine应用远程变更到本地画布 -> 8. PresenceManager更新用户状态显示

## 关键决策
- 在现有index.html基础上扩展，添加协作功能相关的JavaScript模块
- 使用原生WebSocket API而非第三方库，保持技术栈一致性
- 采用操作变换(Operational Transformation)简化版本处理并发编辑冲突
- 在现有样式基础上添加协作UI组件(在线用户列表、用户光标等)
- 使用事件驱动架构，通过自定义事件在模块间通信
- 变更数据使用JSON格式，包含操作类型、时间戳、用户ID等元信息
- 在现有表单容器旁边添加画布协作区域，复用现有CSS样式
