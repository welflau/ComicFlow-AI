# 架构设计 - 连线系统开发

## 架构模式
基于现有HTML页面的增量扩展架构

## 技术栈

- **language**: JavaScript
- **framework**: 原生JavaScript + Three.js

## 模块设计

### ConnectionSystem
职责: 管理节点间连线的创建、渲染、交互和数据流向
- createConnection(sourceNode, targetNode, connectionType)
- removeConnection(connectionId)
- updateConnectionPath(connectionId)
- validateConnection(source, target)
- getConnectionsByNode(nodeId)

### ConnectionRenderer
职责: 基于Three.js渲染连线的视觉效果和动画
- renderConnection(connection)
- updateConnectionGeometry(connection)
- animateDataFlow(connection)
- highlightConnection(connectionId)
- renderConnectionPreview(startPoint, endPoint)

### ConnectionInteraction
职责: 处理连线相关的用户交互事件
- startConnectionDrag(sourcePort)
- updateConnectionPreview(mousePosition)
- completeConnection(targetPort)
- selectConnection(connectionId)
- deleteSelectedConnection()

### DataFlowVisualizer
职责: 可视化数据在连线中的流向和状态
- showDataFlow(connectionId, data)
- animateFlowParticles(connection)
- updateFlowDirection(connectionId)
- highlightActiveFlow(connectionId)

## 数据流
用户在节点端口上开始拖拽 -> ConnectionInteraction捕获事件并创建预览连线 -> ConnectionRenderer实时渲染预览路径 -> 用户拖拽到目标端口时ConnectionSystem验证连接有效性 -> 创建正式连线对象并存储 -> ConnectionRenderer渲染最终连线 -> DataFlowVisualizer根据工作流状态显示数据流向动画

## 关键决策
- 在现有index.html中添加连线系统相关的JavaScript代码，保持单页面架构
- 使用Three.js的Line和CatmullRomCurve3实现平滑连线渲染
- 采用贝塞尔曲线算法计算连线路径，支持自动避障
- 实现连线的分层渲染，支持不同类型连线的视觉区分
- 使用事件委托机制处理连线交互，提高性能
- 集成到现有的画布缩放和平移系统中，确保连线跟随节点移动
- 支持多种连接类型：数据连接、控制连接、触发连接等
- 实现连线状态管理，支持激活、错误、禁用等状态可视化
