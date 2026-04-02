# 架构设计 - 数据库设计与建模

## 架构模式
数据库分层架构

## 技术栈

- **language**: JavaScript
- **framework**: Node.js + Mongoose/Sequelize

## 模块设计

### Canvas Model
职责: 画布数据模型，存储画布基本信息、配置和元数据
- createCanvas()
- updateCanvas()
- getCanvasById()
- deleteCanvas()
- getCanvasByUser()

### Node Model
职责: 节点数据模型，存储节点类型、位置、配置和状态信息
- createNode()
- updateNode()
- deleteNode()
- getNodesByCanvas()
- updateNodePosition()

### Connection Model
职责: 连线数据模型，存储节点间的连接关系和数据流向
- createConnection()
- deleteConnection()
- getConnectionsByCanvas()
- validateConnection()

### Workflow Model
职责: 工作流状态模型，存储执行状态、结果和历史记录
- createWorkflow()
- updateWorkflowStatus()
- getWorkflowHistory()
- saveExecutionResult()

### Collaboration Model
职责: 协作数据模型，存储实时编辑状态和用户操作记录
- createCollabSession()
- updateUserCursor()
- saveOperation()
- getActiveUsers()

## 数据流
用户通过现有认证系统登录后，可创建画布(Canvas)，在画布中添加节点(Node)和连线(Connection)，形成工作流(Workflow)。所有操作通过协作模型(Collaboration)实时同步给其他用户。数据库采用关系型设计，Canvas为主表，Node和Connection为子表，Workflow存储执行状态，Collaboration记录实时操作。

## 关键决策
- 扩展现有User模型，添加画布关联关系
- 采用MongoDB存储灵活的节点配置数据
- 使用Redis缓存实时协作状态
- 设计版本控制机制支持画布历史回滚
- 建立索引优化大量节点的查询性能
- 预留扩展字段支持未来节点类型增加
