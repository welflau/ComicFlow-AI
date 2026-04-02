# 架构设计 - 连线系统开发

## 架构模式
基于现有HTML页面的增量扩展架构

## 技术栈

- **language**: JavaScript
- **framework**: 原生JavaScript + Three.js

## 模块设计

### ConnectionSystem
职责: 管理节点间连线的创建、渲染和交互
- createConnection(sourceNode, targetNode, connectionType)
- deleteConnection(connectionId)
- updateConnectionPath(connectionId)
- validateConnection(source, target)

### ConnectionRenderer
职责: 基于Three.js渲染连线的视觉效果
- renderConnection(connection)
- updateConnectionGeometry(connection)
- highlightConnection(connectionId)
- animateDataFlow(connectionId)

### ConnectionInteraction
职责: 处理连线相关的用户交互
- startConnectionDrag(sourcePort)
- updateConnectionPreview(mousePosition)
- completeConnection(targetPort)
- selectConnection(connectionId)

### DataFlowVisualizer
职责: 可视化数据在连线中的流动
- showDataFlow(connectionId, data)
- animateFlowParticles(connection)
- updateFlowDirection(connectionId)
- pauseDataFlow(connectionId)

## 数据流
用户在画布上拖拽创建连线 -> ConnectionInteraction捕获交互事件 -> ConnectionSystem验证连接有效性并创建连线对象 -> ConnectionRenderer使用Three.js渲染连线几何体 -> DataFlowVisualizer添加数据流动画效果 -> 连线状态通过WebSocket同步给其他协作用户

## 关键决策
- 在现有index.html中添加连线系统相关的JavaScript代码，保持单页面架构
- 使用Three.js的BufferGeometry创建高性能的连线渲染，支持贝塞尔曲线和直线两种类型
- 采用端口(Port)概念，每个节点有输入输出端口，连线只能在兼容端口间创建
- 实现连线的分层渲染：背景层(普通连线)、高亮层(选中连线)、动画层(数据流)
- 使用颜色编码区分不同数据类型的连线：蓝色(数据)、绿色(控制流)、红色(错误)
- 连线交互采用射线检测(Raycasting)实现精确的鼠标悬停和点击检测
- 数据流动画使用粒子系统，沿连线路径移动小球表示数据传输
