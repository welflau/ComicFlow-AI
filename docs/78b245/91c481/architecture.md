# 架构设计 - Three.js画布基础架构

## 架构模式
模块化组件架构

## 技术栈

- **language**: JavaScript
- **framework**: Three.js + 原生JS

## 模块设计

### CanvasEngine
职责: Three.js画布核心引擎，管理场景、相机、渲染器
- init()
- render()
- resize()
- dispose()

### CameraController
职责: 相机控制器，处理缩放、平移、边界限制
- zoom(delta)
- pan(x, y)
- setPosition(x, y, z)
- getBounds()

### InteractionManager
职责: 交互事件管理，处理鼠标、触摸、键盘事件
- onMouseDown()
- onMouseMove()
- onWheel()
- bindEvents()

### ViewportManager
职责: 视口管理，处理画布尺寸、坐标转换
- updateSize()
- screenToWorld(x, y)
- worldToScreen(x, y)

### PerformanceOptimizer
职责: 性能优化，LOD管理、视锥剔除、帧率控制
- updateLOD()
- cullObjects()
- throttleRender()

## 数据流
用户交互事件 -> InteractionManager -> CameraController -> CanvasEngine -> Three.js渲染器 -> GPU渲染。ViewportManager负责坐标系转换，PerformanceOptimizer在渲染前进行优化处理。

## 关键决策
- 在现有index.html基础上添加画布容器，保持原有认证系统不变
- 使用Three.js OrthographicCamera实现2D无限画布效果
- 采用模块化设计，每个功能独立封装便于后续扩展节点系统
- 使用requestAnimationFrame优化渲染性能
- 实现基于距离的LOD系统支持1000+对象渲染
- 预留WebSocket接口为后续协作功能做准备
