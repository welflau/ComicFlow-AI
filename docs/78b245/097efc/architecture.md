# 架构设计 - 数据库设计与建模

## 架构模式
数据库建模架构

## 技术栈

- **language**: JavaScript/SQL
- **framework**: Node.js + MongoDB/PostgreSQL

## 模块设计

### Canvas Model
职责: 画布数据模型，存储画布基本信息、视图状态和元数据
- createCanvas(canvasData)
- updateCanvas(canvasId, updates)
- getCanvas(canvasId)
- deleteCanvas(canvasId)
- getCanvasByUser(userId)

### Node Model
职责: 节点数据模型，存储节点类型、位置、配置和状态信息
- createNode(nodeData)
- updateNode(nodeId, updates)
- getNode(nodeId)
- deleteNode(nodeId)
- getNodesByCanvas(canvasId)

### Connection Model
职责: 连线数据模型，存储节点间的连接关系和数据流配置
- createConnection(connectionData)
- updateConnection(connectionId, updates)
- getConnection(connectionId)
- deleteConnection(connectionId)
- getConnectionsByCanvas(canvasId)

### Workflow Model
职责: 工作流状态模型，存储执行状态、运行历史和调度信息
- createWorkflow(workflowData)
- updateWorkflowStatus(workflowId, status)
- getWorkflow(workflowId)
- getWorkflowHistory(workflowId)
- getActiveWorkflows()

### Collaboration Model
职责: 协作数据模型，存储用户权限、实时编辑状态和变更历史
- addCollaborator(canvasId, userId, permission)
- updateUserCursor(canvasId, userId, position)
- recordChange(canvasId, userId, changeData)
- getCollaborators(canvasId)
- getChangeHistory(canvasId)

## 数据流
用户通过画布操作触发数据变更 -> 数据模型验证和存储 -> WebSocket广播变更事件 -> 其他协作用户实时同步 -> 工作流引擎根据节点连接关系执行任务 -> 状态更新持久化到数据库

## 关键决策
- 基于现有User模型扩展，保持数据库配置一致性
- 采用文档型数据库存储复杂的节点配置和画布状态
- 使用关系型设计处理用户权限和协作关系
- 实现软删除机制支持版本历史和回滚
- 设计索引策略优化大画布的查询性能
- 预留扩展字段支持未来节点类型和功能迭代
