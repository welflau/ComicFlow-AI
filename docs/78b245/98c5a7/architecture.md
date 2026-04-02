# 架构设计 - [BUG] [BUG] 智能画布节点连线断开问题

## 架构模式
基于Three.js的智能画布连线系统修复架构

## 技术栈

- **language**: JavaScript
- **framework**: Three.js + WebGL

## 模块设计

### ConnectionRenderer
职责: 负责Three.js连线的渲染逻辑，包括线条几何体创建、材质管理和渲染更新
- createConnection(startNode, endNode)
- updateConnectionGeometry(connection)
- removeConnection(connectionId)
- refreshAllConnections()

### NodePositionTracker
职责: 跟踪节点位置变化，确保连线端点坐标准确计算
- trackNodePosition(nodeId, position)
- getNodeConnectionPoints(nodeId)
- updateConnectionEndpoints(nodeId)
- calculateBezierControlPoints(start, end)

### CanvasCoordinateSystem
职责: 处理画布缩放和平移时的坐标转换，确保连线在不同视图状态下正确显示
- worldToScreen(worldPos)
- screenToWorld(screenPos)
- updateViewMatrix(zoom, pan)
- transformConnectionCoordinates(connection)

### ConnectionStateManager
职责: 管理连线状态和生命周期，处理连线的创建、更新、删除
- createConnectionState(startNodeId, endNodeId)
- updateConnectionState(connectionId, state)
- validateConnection(startNode, endNode)
- cleanupOrphanedConnections()

### RenderLayerManager
职责: 管理WebGL渲染层级，确保连线在正确的渲染层显示
- setConnectionRenderOrder()
- updateRenderLayers()
- handleDepthTesting()
- optimizeRenderBatches()

## 数据流
用户拖拽节点时，NodePositionTracker捕获位置变化 -> CanvasCoordinateSystem计算新的世界坐标 -> ConnectionStateManager更新相关连线状态 -> ConnectionRenderer重新计算连线几何体 -> RenderLayerManager确保正确渲染层级 -> Three.js渲染引擎更新画布显示

## 关键决策
- 使用Three.js的BufferGeometry优化连线渲染性能，支持1000+节点的流畅显示
- 采用贝塞尔曲线算法绘制连线，提供更好的视觉效果和数据流向表示
- 实现连线的分层渲染机制，解决WebGL渲染层级问题
- 建立节点位置变化的观察者模式，确保连线实时跟随节点移动
- 在现有index.html基础上添加Three.js画布容器，保持现有页面结构不变
- 使用requestAnimationFrame优化渲染循环，避免连线显示异常和断开问题
