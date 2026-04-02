# 架构设计 - 节点系统开发

## 架构模式
基于Three.js的节点系统架构

## 技术栈

- **language**: JavaScript
- **framework**: Three.js + 原生HTML/CSS

## 模块设计

### NodeSystem
职责: 节点系统核心管理器，负责节点的创建、渲染、交互管理
- createNode(type, position)
- deleteNode(id)
- updateNodePosition(id, position)
- getNodeById(id)

### BaseNode
职责: 节点基类，定义节点的通用属性和方法
- render()
- setPosition(x, y)
- setSelected(boolean)
- getConnectors()

### InputNode
职责: 输入节点实现，处理数据输入和输出连接点
- setValue(value)
- getValue()
- getOutputConnector()

### ProcessNode
职责: 处理节点实现，具有输入输出连接点，执行数据处理逻辑
- process(inputData)
- getInputConnectors()
- getOutputConnectors()

### OutputNode
职责: 输出节点实现，接收处理结果并展示
- setResult(data)
- getInputConnector()
- display()

### DragController
职责: 节点拖拽交互控制器，处理鼠标事件和节点移动
- startDrag(node, event)
- updateDrag(event)
- endDrag()

### NodeRenderer
职责: 节点Three.js渲染器，负责节点的3D可视化
- renderNode(node)
- updateNodeVisual(node)
- highlightNode(node)

## 数据流
用户在画布上创建节点 -> NodeSystem创建对应类型节点实例 -> NodeRenderer渲染节点到Three.js场景 -> DragController监听鼠标事件处理拖拽 -> 节点位置更新触发重新渲染 -> 节点状态变化通过事件系统通知其他组件

## 关键决策
- 在现有index.html基础上添加Three.js画布容器，保持原有认证系统不变
- 采用工厂模式创建不同类型节点，便于扩展新节点类型
- 使用Three.js的Raycaster实现精确的节点选择和拖拽检测
- 节点渲染采用InstancedMesh优化性能，支持1000+节点流畅渲染
- 实现事件驱动的节点状态管理，为后续连线系统和工作流引擎做准备
- 节点几何体使用简单的立方体和圆柱体组合，确保渲染性能
