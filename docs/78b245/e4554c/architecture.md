# 架构设计 - [BUG] 智能画布节点无法拖拽连线

## 架构模式
事件驱动架构 + 状态管理模式

## 技术栈

- **language**: JavaScript
- **framework**: Three.js + 原生DOM

## 模块设计

### ConnectionManager
职责: 管理节点连线的创建、拖拽和渲染逻辑
- startConnection(sourceNode, connectionPoint)
- updateConnection(mousePosition)
- finishConnection(targetNode, connectionPoint)
- cancelConnection()
- renderTempConnection()

### NodeConnectionHandler
职责: 处理节点连接点的鼠标事件和交互状态
- onConnectionPointMouseDown(event)
- onConnectionPointMouseEnter(event)
- onConnectionPointMouseLeave(event)
- validateConnection(source, target)

### CanvasEventManager
职责: 统一管理画布上的鼠标事件和拖拽状态
- onMouseMove(event)
- onMouseUp(event)
- getMousePosition(event)
- updateDragState(state)

### ConnectionRenderer
职责: 负责连线的Three.js渲染和视觉效果
- createConnectionGeometry(startPos, endPos)
- updateConnectionMaterial(state)
- addConnectionToScene(connection)
- removeConnectionFromScene(connection)

## 数据流
用户点击节点连接点 -> NodeConnectionHandler捕获事件 -> ConnectionManager开始连线状态 -> CanvasEventManager监听鼠标移动 -> ConnectionRenderer实时渲染临时连线 -> 用户释放鼠标到目标节点 -> ConnectionManager验证并创建最终连线 -> 更新工作流状态

## 关键决策
- 在现有index.html中添加画布容器，保持现有认证系统不变
- 使用Three.js的Raycaster进行精确的鼠标拾取和节点检测
- 采用状态机模式管理连线拖拽的不同阶段（开始、拖拽中、完成、取消）
- 使用贝塞尔曲线渲染连线，提供平滑的视觉效果
- 实现连接点的视觉反馈（悬停高亮、连接状态指示）
- 添加连线类型验证，确保只有兼容的节点类型可以连接
