# 架构设计 - 后端工作流引擎核心API

## 架构模式
RESTful API + 工作流引擎

## 技术栈

- **language**: Node.js
- **framework**: Express.js

## 模块设计

### models/Canvas.js
职责: 画布数据模型，管理画布基本信息、节点和连线数据
- create(canvasData)
- findById(id)
- update(id, data)
- delete(id)
- addNode(canvasId, nodeData)
- removeNode(canvasId, nodeId)
- addConnection(canvasId, connectionData)

### models/WorkflowExecution.js
职责: 工作流执行记录模型，跟踪工作流运行状态和结果
- create(executionData)
- findById(id)
- updateStatus(id, status)
- getExecutionHistory(canvasId)

### controllers/canvasController.js
职责: 画布CRUD操作控制器，处理画布相关的HTTP请求
- createCanvas(req, res)
- getCanvas(req, res)
- updateCanvas(req, res)
- deleteCanvas(req, res)
- getUserCanvases(req, res)

### controllers/workflowController.js
职责: 工作流执行控制器，处理工作流运行和调度请求
- executeWorkflow(req, res)
- getExecutionStatus(req, res)
- stopExecution(req, res)
- getExecutionHistory(req, res)

### services/workflowEngine.js
职责: 工作流引擎核心服务，负责节点调度、执行和状态管理
- executeCanvas(canvasId)
- validateWorkflow(canvasData)
- executeNode(nodeData, inputs)
- getNodeDependencies(canvasData, nodeId)
- updateExecutionStatus(executionId, status)

### services/nodeExecutor.js
职责: 节点执行器，根据节点类型执行具体的处理逻辑
- executeInputNode(nodeData)
- executeProcessNode(nodeData, inputs)
- executeOutputNode(nodeData, inputs)
- validateNodeInputs(nodeData, inputs)

### routes/canvas.js
职责: 画布相关路由定义，映射HTTP请求到控制器方法
- POST /api/canvas
- GET /api/canvas/:id
- PUT /api/canvas/:id
- DELETE /api/canvas/:id
- GET /api/user/canvases

### routes/workflow.js
职责: 工作流相关路由定义，处理工作流执行请求
- POST /api/workflow/execute/:canvasId
- GET /api/workflow/status/:executionId
- POST /api/workflow/stop/:executionId
- GET /api/workflow/history/:canvasId

## 数据流
用户通过画布API创建/编辑画布 -> 画布数据存储到Canvas模型 -> 用户触发工作流执行 -> workflowEngine验证工作流并创建执行记录 -> 按依赖关系调度节点执行 -> nodeExecutor执行具体节点逻辑 -> 更新执行状态到WorkflowExecution模型 -> 返回执行结果给用户

## 关键决策
- 基于现有Express.js架构扩展，保持与用户认证系统的一致性
- 采用MongoDB存储画布和工作流数据，支持复杂的嵌套结构
- 工作流引擎采用基于依赖图的调度算法，支持并行执行
- 节点执行采用策略模式，便于扩展不同类型的节点处理器
- 执行状态采用状态机模式管理：pending -> running -> completed/failed
- 复用现有的认证中间件和错误处理机制
- 为后续WebSocket实时协作预留接口扩展点
