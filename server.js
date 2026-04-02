const express = require('express');
const http = require('http');
const socketIo = require('socket.io');
const path = require('path');

const app = express();
const server = http.createServer(app);
const io = socketIo(server, {
    cors: {
        origin: "*",
        methods: ["GET", "POST"]
    }
});

// 静态文件服务
app.use(express.static(path.join(__dirname)));

// 存储连接的用户和系统状态
const connectedUsers = new Map();
const systemState = {
    nodes: [],
    connections: [],
    workflows: []
};

// 测试相关的数据存储
const testSessions = new Map();
const performanceMetrics = [];

// Socket.IO 连接处理
io.on('connection', (socket) => {
    console.log('用户连接:', socket.id);
    
    // 用户加入
    socket.on('user-join', (userData) => {
        connectedUsers.set(socket.id, {
            id: socket.id,
            name: userData.name || `用户${socket.id.slice(0, 6)}`,
            joinTime: Date.now()
        });
        
        // 发送当前系统状态
        socket.emit('system-state', systemState);
        
        // 通知其他用户
        socket.broadcast.emit('user-joined', connectedUsers.get(socket.id));
        
        console.log(`用户 ${userData.name} 加入系统`);
    });
    
    // 节点操作同步
    socket.on('node-created', (nodeData) => {
        systemState.nodes.push(nodeData);
        socket.broadcast.emit('node-created', nodeData);
        console.log('节点创建:', nodeData.id);
    });
    
    socket.on('node-updated', (nodeData) => {
        const nodeIndex = systemState.nodes.findIndex(n => n.id === nodeData.id);
        if (nodeIndex !== -1) {
            systemState.nodes[nodeIndex] = { ...systemState.nodes[nodeIndex], ...nodeData };
            socket.broadcast.emit('node-updated', nodeData);
        }
    });
    
    socket.on('node-deleted', (nodeId) => {
        systemState.nodes = systemState.nodes.filter(n => n.id !== nodeId);
        systemState.connections = systemState.connections.filter(c => c.from !== nodeId && c.to !== nodeId);
        socket.broadcast.emit('node-deleted', nodeId);
        console.log('节点删除:', nodeId);
    });
    
    // 连接操作同步
    socket.on('connection-created', (connectionData) => {
        systemState.connections.push(connectionData);
        socket.broadcast.emit('connection-created', connectionData);
    });
    
    socket.on('connection-deleted', (connectionId) => {
        systemState.connections = systemState.connections.filter(c => c.id !== connectionId);
        socket.broadcast.emit('connection-deleted', connectionId);
    });
    
    // 工作流操作同步
    socket.on('workflow-created', (workflowData) => {
        systemState.workflows.push(workflowData);
        socket.broadcast.emit('workflow-created', workflowData);
    });
    
    socket.on('workflow-executed', (executionData) => {
        socket.broadcast.emit('workflow-executed', executionData);
        console.log('工作流执行:', executionData.workflowId);
    });
    
    // 测试相关事件处理
    socket.on('test-session-start', (sessionData) => {
        const sessionId = `test-${Date.now()}-${socket.id}`;
        testSessions.set(sessionId, {
            id: sessionId,
            userId: socket.id,
            startTime: Date.now(),
            tests: [],
            status: 'running'
        });
        
        socket.emit('test-session-created', { sessionId });
        console.log('测试会话开始:', sessionId);
    });
    
    socket.on('test-result', (testData) => {
        const session = Array.from(testSessions.values()).find(s => s.userId === socket.id && s.status === 'running');
        if (session) {
            session.tests.push({
                ...testData,
                timestamp: Date.now()
            });
        }
        
        // 广播测试结果给其他用户（用于协作测试）
        socket.broadcast.emit('test-result-broadcast', {
            userId: socket.id,
            ...testData
        });
    });
    
    socket.on('test-session-end', (sessionData) => {
        const session = Array.from(testSessions.values()).find(s => s.userId === socket.id && s.status === 'running');
        if (session) {
            session.status = 'completed';
            session.endTime = Date.now();
            session.duration = session.endTime - session.startTime;
            
            // 生成测试报告
            const report = generateTestReport(session);
            socket.emit('test-report', report);
            
            console.log(`测试会话完成: ${session.id}, 耗时: ${session.duration}ms`);
        }
    });
    
    // 性能指标收集
    socket.on('performance-metrics', (metrics) => {
        const metricsData = {
            userId: socket.id,
            timestamp: Date.now(),
            ...metrics
        };
        
        performanceMetrics.push(metricsData);
        
        // 保持最近1000条记录
        if (performanceMetrics.length > 1000) {
            performanceMetrics.shift();
        }
        
        // 广播性能指标给其他用户
        socket.broadcast.emit('performance-metrics-broadcast', metricsData);
    });
    
    // 协作冲突解决
    socket.on('conflict-resolution', (conflictData) => {
        const resolution = resolveConflict(conflictData);
        
        // 通知所有用户冲突解决结果
        io.emit('conflict-resolved', {
            conflictId: conflictData.id,
            resolution: resolution,
            timestamp: Date.now()
        });
        
        console.log('冲突解决:', conflictData.id, resolution);
    });
    
    // Ping/Pong 用于延迟测试
    socket.on('ping', (timestamp) => {
        socket.emit('pong', timestamp);
    });
    
    // 用户断开连接
    socket.on('disconnect', () => {
        const user = connectedUsers.get(socket.id);
        if (user) {
            connectedUsers.delete(socket.id);
            socket.broadcast.emit('user-left', user);
            console.log(`用户 ${user.name} 离开系统`);
        }
        
        // 清理用户的测试会话
        for (const [sessionId, session] of testSessions.entries()) {
            if (session.userId === socket.id && session.status === 'running') {
                session.status = 'interrupted';
                session.endTime = Date.now();
                testSessions.delete(sessionId);
            }
        }
    });
});

// 测试报告生成函数
function generateTestReport(session) {
    const tests = session.tests;
    const summary = {
        total: tests.length,
        passed: tests.filter(t => t.result === true).length,
        failed: tests.filter(t => t.result === false).length,
        duration: session.duration
    };
    
    summary.passRate = summary.total > 0 ? (summary.passed / summary.total * 100).toFixed(2) : 0;
    
    const categories = {};
    tests.forEach(test => {
        if (!categories[test.category]) {
            categories[test.category] = { passed: 0, failed: 0, total: 0 };
        }
        categories[test.category].total++;
        if (test.result) {
            categories[test.category].passed++;
        } else {
            categories[test.category].failed++;
        }
    });
    
    return {
        sessionId: session.id,
        timestamp: new Date().toISOString(),
        summary,
        categories,
        tests,
        performanceMetrics: getRecentPerformanceMetrics(session.userId, session.startTime, session.endTime)
    };
}

// 获取指定时间范围内的性能指标
function getRecentPerformanceMetrics(userId, startTime, endTime) {
    return performanceMetrics.filter(metric => 
        metric.userId === userId && 
        metric.timestamp >= startTime && 
        metric.timestamp <= endTime
    );
}

// 冲突解决函数
function resolveConflict(conflictData) {
    // 简单的冲突解决策略：
    // 1. 时间戳优先（最新的更改获胜）
    // 2. 用户优先级（如果设置了的话）
    // 3. 操作类型优先级
    
    const { type, changes } = conflictData;
    
    if (changes.length <= 1) {
        return changes[0] || null;
    }
    
    // 按时间戳排序，选择最新的
    const sortedChanges = changes.sort((a, b) => b.timestamp - a.timestamp);
    
    return {
        selectedChange: sortedChanges[0],
        reason: 'latest_timestamp',
        rejectedChanges: sortedChanges.slice(1)
    };
}

// API 端点
app.get('/api/system-status', (req, res) => {
    res.json({
        connectedUsers: connectedUsers.size,
        totalNodes: systemState.nodes.length,
        totalConnections: systemState.connections.length,
        totalWorkflows: systemState.workflows.length,
        activeSessions: Array.from(testSessions.values()).filter(s => s.status === 'running').length,
        uptime: process.uptime()
    });
});

app.get('/api/performance-metrics', (req, res) => {
    const recentMetrics = performanceMetrics.slice(-100); // 最近100条记录
    res.json(recentMetrics);
});

app.get('/api/test-sessions', (req, res) => {
    const sessions = Array.from(testSessions.values()).map(session => ({
        id: session.id,
        userId: session.userId,
        status: session.status,
        startTime: session.startTime,
        endTime: session.endTime,
        duration: session.duration,
        testCount: session.tests.length
    }));
    res.json(sessions);
});

app.get('/api/test-report/:sessionId', (req, res) => {
    const session = testSessions.get(req.params.sessionId);
    if (!session) {
        return res.status(404).json({ error: 'Session not found' });
    }
    
    const report = generateTestReport(session);
    res.json(report);
});

// 错误处理
app.use((err, req, res, next) => {
    console.error('服务器错误:', err);
    res.status(500).json({ error: 'Internal server error' });
});

// 启动服务器
const PORT = process.env.PORT || 3000;
server.listen(PORT, () => {
    console.log(`服务器运行在端口 ${PORT}`);
    console.log(`访问 http://localhost:${PORT} 查看应用`);
});

// 优雅关闭
process.on('SIGTERM', () => {
    console.log('收到 SIGTERM 信号，正在关闭服务器...');
    server.close(() => {
        console.log('服务器已关闭');
        process.exit(0);
    });
});

process.on('SIGINT', () => {
    console.log('收到 SIGINT 信号，正在关闭服务器...');
    server.close(() => {
        console.log('服务器已关闭');
        process.exit(0);
    });
});