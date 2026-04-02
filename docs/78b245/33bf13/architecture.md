# 架构设计 - 前端工作流执行界面

## 架构模式
基于现有HTML页面的增量扩展架构

## 技术栈

- **language**: JavaScript
- **framework**: 原生JS + Three.js + WebSocket

## 模块设计

### 工作流执行控制面板
职责: 在现有index.html中添加工作流执行控制区域，包括开始/暂停/停止按钮、执行进度显示
- startWorkflow()
- pauseWorkflow()
- stopWorkflow()
- getExecutionStatus()

### 节点状态可视化组件
职责: 扩展现有Three.js画布，为节点添加执行状态指示器（等待/执行中/完成/错误）
- updateNodeStatus(nodeId, status)
- renderStatusIndicator(node)
- animateNodeExecution(nodeId)

### 实时日志查看器
职责: 在页面底部添加可折叠的日志面板，实时显示工作流执行日志
- appendLog(message, level)
- clearLogs()
- filterLogs(level)
- exportLogs()

### WebSocket执行状态同步
职责: 扩展现有WebSocket连接，监听工作流执行状态变化并更新UI
- subscribeExecutionEvents()
- handleStatusUpdate(event)
- handleLogMessage(event)

### 执行历史管理
职责: 在现有用户界面中添加执行历史查看功能，支持查看历史执行记录
- loadExecutionHistory()
- showExecutionDetails(executionId)
- deleteExecutionRecord(executionId)

## 数据流
用户在现有画布界面点击执行按钮 -> 控制面板发送执行请求到后端工作流引擎 -> WebSocket接收执行状态更新 -> 更新Three.js画布中的节点状态视觉效果 -> 日志查看器实时显示执行日志 -> 执行完成后更新历史记录

## 关键决策
- 在现有index.html基础上扩展，保持原有认证系统和样式风格
- 复用现有Three.js画布架构，通过状态叠加方式显示执行状态
- 利用现有WebSocket连接，扩展消息类型支持执行状态同步
- 采用CSS Grid布局在现有容器中添加执行控制和日志区域
- 使用原生JavaScript实现，保持与现有代码技术栈一致
