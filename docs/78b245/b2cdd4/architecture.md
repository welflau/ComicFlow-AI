# 架构设计 - 节点系统开发

## 架构模式
组件化模块架构

## 技术栈

- **language**: JavaScript
- **framework**: 原生JS + Three.js

## 模块设计

### NodeSystem
职责: 节点系统核心管理器，负责节点的创建、删除、类型管理
- createNode(type, position)
- deleteNode(nodeId)
- getNodeById(nodeId)
- getAllNodes()
- registerNodeType(type, config)

### BaseNode
职责: 节点基类，定义节点的通用属性和方法
- render()
- update()
- setPosition(x, y)
- getPosition()
- addPort(type, name)
- removePort(portId)

### InputNode
职责: 输入节点实现，处理数据输入和用户交互
- setValue(value)
- getValue()
- validateInput()
- onInputChange(callback)

### ProcessNode
职责: 处理节点实现，执行数据处理逻辑
- process(inputData)
- setProcessFunction(fn)
- getOutputData()
- onProcessComplete(callback)

### OutputNode
职责: 输出节点实现，处理结果输出和显示
- displayResult(data)
- exportData(format)
- setDisplayMode(mode)
- onOutputReady(callback)

### DragController
职责: 处理节点拖拽交互，包括拖拽开始、移动、结束
- enableDrag(node)
- disableDrag(node)
- onDragStart(callback)
- onDragMove(callback)
- onDragEnd(callback)

### NodeRenderer
职责: 负责节点的Three.js渲染，包括几何体、材质、文本
- renderNode(node, scene)
- updateNodeVisual(node)
- createNodeGeometry(type)
- updateNodePosition(node, position)

## 数据流
用户在画布上右键创建节点 -> NodeSystem创建对应类型节点实例 -> NodeRenderer在Three.js场景中渲染节点 -> DragController监听鼠标事件处理拖拽 -> 节点位置更新触发渲染器重绘 -> 节点状态变化通过事件系统通知其他组件

## 关键决策
- 在现有index.html基础上添加画布容器和节点系统脚本
- 使用Three.js的Mesh对象表示节点，便于3D渲染和交互检测
- 采用工厂模式创建不同类型节点，便于扩展新节点类型
- 使用事件驱动架构处理节点交互，降低模块间耦合
- 节点拖拽使用Raycaster进行3D空间的鼠标拾取
- 节点渲染采用实例化几何体优化性能，支持1000+节点渲染
