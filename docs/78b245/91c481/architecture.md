# 架构设计 - Three.js画布基础架构

## 架构模式
基于Three.js的画布渲染架构

## 技术栈

- **language**: JavaScript
- **framework**: Three.js + 原生HTML/CSS

## 模块设计

### CanvasRenderer
职责: 基于Three.js的画布渲染引擎，负责场景初始化、相机控制、渲染循环
- init(container)
- render()
- resize(width, height)
- dispose()

### CameraController
职责: 相机控制器，处理缩放、平移、边界限制等交互
- enableControls()
- disableControls()
- setZoomLimits(min, max)
- setPanLimits(bounds)
- resetView()

### ViewportManager
职责: 视口管理器，处理无限画布的视口裁剪和性能优化
- updateViewport(camera)
- getVisibleBounds()
- isInViewport(object)
- optimizeRendering()

### InteractionHandler
职责: 交互事件处理器，统一管理鼠标、触摸、键盘事件
- bindEvents(canvas)
- unbindEvents()
- onPointerDown(event)
- onPointerMove(event)
- onPointerUp(event)
- onWheel(event)

### CanvasApp
职责: 画布应用主控制器，整合各个模块并提供统一API
- initialize()
- start()
- stop()
- getRenderer()
- getCamera()

## 数据流
用户交互事件 -> InteractionHandler -> CameraController -> ViewportManager -> CanvasRenderer -> Three.js渲染管线 -> 画布显示。ViewportManager持续监控视口变化，优化渲染性能。所有模块通过CanvasApp统一协调。

## 关键决策
- 在现有index.html中添加画布容器div，保持现有页面结构不变
- 使用Three.js OrthographicCamera实现2D画布效果，便于后续节点系统集成
- 采用模块化设计，每个功能独立封装，便于后续扩展节点和连线系统
- 使用requestAnimationFrame优化渲染循环，确保60fps流畅体验
- 实现视口裁剪机制，支持1000+节点的高性能渲染
- 预留事件系统接口，为后续节点拖拽、连线功能做准备
