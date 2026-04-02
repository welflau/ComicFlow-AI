# 架构设计 - [BUG] [BUG] 智能画布节点连线断开问题

## 架构模式
分层架构 + 组件化设计

## 技术栈

- **language**: JavaScript
- **framework**: Three.js + WebGL + 原生JS

## 模块设计

### ConnectionRenderer
职责: 负责连线的Three.js渲染逻辑，包括贝塞尔曲线生成、材质管理、渲染优化
- renderConnection(startNode, endNode, connectionType)
- updateConnectionPath(connectionId, newPath)
- removeConnection(connectionId)
- refreshAllConnections()

### NodePositionManager
职责: 管理节点位置计算和坐标转换，确保连线端点准确定位
- getNodeConnectionPoint(nodeId, portType)
- updateNodePosition(nodeId, position)
- screenToWorldCoords(screenX, screenY)
- worldToScreenCoords(worldX, worldY)

### CanvasCoordinateSystem
职责: 处理画布缩放、平移时的坐标系统转换和连线更新
- onCanvasTransform(scale, offsetX, offsetY)
- updateConnectionsOnTransform()
- getTransformMatrix()
- applyTransformToConnections()

### ConnectionStateManager
职责: 管理连线状态、层级关系和渲染顺序
- setConnectionState(connectionId, state)
- updateRenderOrder()
- handleConnectionHover(connectionId)
- validateConnectionIntegrity()

### CanvasDebugger
职责: 提供连线渲染调试工具和错误诊断功能
- debugConnectionPath(connectionId)
- validateNodePositions()
- logRenderingErrors()
- showConnectionBounds(connectionId)

## 数据流
用户拖拽节点时 -> NodePositionManager更新节点坐标 -> CanvasCoordinateSystem处理坐标转换 -> ConnectionRenderer重新计算连线路径 -> ConnectionStateManager更新渲染状态 -> Three.js渲染引擎绘制连线 -> CanvasDebugger监控渲染质量

## 关键决策
- 使用贝塞尔曲线替代直线连接，提供更好的视觉效果和路径平滑度
- 实现双缓冲渲染机制，避免连线闪烁和断开问题
- 建立独立的坐标系统管理器，统一处理画布变换时的坐标转换
- 采用连线状态机模式，确保连线在不同状态下的正确显示
- 集成调试工具，便于快速定位和修复连线渲染问题
- 在现有index.html基础上添加画布容器和Three.js初始化代码
