# 架构设计 - 前端工作流执行界面

## 架构模式
基于现有HTML页面的模块化扩展

## 技术栈

- **language**: JavaScript
- **framework**: 原生JavaScript + Three.js

## 模块设计

### WorkflowExecutionPanel
职责: 工作流执行控制面板，提供启动、暂停、停止、重置等操作
- startWorkflow(workflowId)
- pauseWorkflow()
- stopWorkflow()
- resetWorkflow()
- getExecutionStatus()

### ExecutionStatusDisplay
职责: 实时显示工作流执行状态，包括节点状态、进度条、执行时间等
- updateNodeStatus(nodeId, status)
- updateProgress(percentage)
- updateExecutionTime(duration)
- showExecutionSummary()

### ExecutionLogViewer
职责: 显示工作流执行日志，支持过滤、搜索、导出功能
- appendLog(logEntry)
- filterLogs(level, nodeId)
- searchLogs(keyword)
- exportLogs(format)
- clearLogs()

### WorkflowExecutionAPI
职责: 与后端工作流引擎通信，处理执行请求和状态同步
- executeWorkflow(workflowData)
- subscribeToExecutionEvents()
- getExecutionHistory(workflowId)
- cancelExecution(executionId)

### ExecutionVisualization
职责: 在Three.js画布上可视化显示执行状态，节点高亮、数据流动画等
- highlightExecutingNode(nodeId)
- showDataFlow(fromNode, toNode, data)
- updateNodeVisualState(nodeId, state)
- playExecutionAnimation()

## 数据流
用户在执行控制面板触发工作流执行 -> WorkflowExecutionAPI发送执行请求到后端 -> 通过WebSocket接收执行状态更新 -> ExecutionStatusDisplay更新界面状态 -> ExecutionLogViewer显示执行日志 -> ExecutionVisualization在画布上可视化执行过程 -> 所有状态变化实时同步到协作用户

## 关键决策
- 在现有index.html基础上添加工作流执行界面，不重新设计页面结构
- 复用现有的WebSocket连接进行执行状态实时同步
- 执行控制面板采用浮动面板设计，不影响画布操作
- 日志查看器支持分级显示（错误、警告、信息、调试）
- 执行状态通过Three.js画布节点颜色和动画直观展示
- 支持执行历史记录查看和重放功能
- 采用事件驱动架构，各模块通过自定义事件通信
