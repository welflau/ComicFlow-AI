# 架构设计 - 后端工作流引擎核心API

## 架构模式
分层架构 + 微服务模式

## 技术栈

- **language**: Node.js
- **framework**: Express.js + Socket.io

## 模块设计

### 工作流控制器
职责: 处理画布CRUD、节点管理、工作流执行等HTTP请求
- POST /api/workflows - 创建工作流
- GET /api/workflows/:id - 获取工作流
- PUT /api/workflows/:id - 更新工作流
- DELETE /api/workflows/:id - 删除工作流
- POST /api/workflows/:id/execute - 执行工作流
- GET /api/workflows/:id/status - 获取执行状态

### 节点控制器
职责: 管理工作流中的节点增删改查操作
- POST /api/workflows/:id/nodes - 添加节点
- PUT /api/workflows/:id/nodes/:nodeId - 更新节点
- DELETE /api/workflows/:id/nodes/:nodeId - 删除节点
- POST /api/workflows/:id/connections - 创建连线
- DELETE /api/workflows/:id/connections/:connId - 删除连线

### 工作流执行引擎
职责: 负责工作流的调度执行、状态管理和结果处理
- executeWorkflow(workflowId)
- pauseWorkflow(workflowId)
- resumeWorkflow(workflowId)
- getExecutionStatus(workflowId)

### 实时协作服务
职责: 基于Socket.io处理多人协作的实时同步
- onCanvasJoin(workflowId, userId)
- onNodeUpdate(workflowId, nodeData)
- onConnectionUpdate(workflowId, connectionData)
- broadcastChange(workflowId, changeData)

### 工作流数据模型
职责: 定义工作流、节点、连线的数据结构和数据库操作
- Workflow.create(data)
- Workflow.findById(id)
- Node.create(workflowId, nodeData)
- Connection.create(workflowId, connectionData)

## 数据流
客户端通过HTTP API进行工作流CRUD操作 -> 控制器验证请求并调用数据模型 -> 数据持久化到数据库 -> 工作流执行时，执行引擎按拓扑顺序调度节点 -> 实时协作通过WebSocket双向同步画布状态变更 -> 所有操作结果通过统一的响应格式返回

## 关键决策
- 复用现有的Express.js架构和认证中间件，确保与用户系统集成
- 采用MongoDB存储工作流数据，支持复杂的嵌套节点结构
- 使用Socket.io实现实时协作，与现有HTTP服务共享端口
- 工作流执行采用异步队列模式，支持长时间运行的任务
- 节点执行状态使用Redis缓存，提高查询性能
- 在现有路由结构基础上新增/api/workflows路由组
