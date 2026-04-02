const express = require('express');
const http = require('http');
const socketIo = require('socket.io');
const cors = require('cors');
const path = require('path');

const app = express();
const server = http.createServer(app);
const io = socketIo(server, {
  cors: {
    origin: "*",
    methods: ["GET", "POST"]
  }
});

// 中间件
app.use(cors());
app.use(express.json());
app.use(express.static(path.join(__dirname, 'public')));

// 协作会话管理器
class CollaborationSessionManager {
  constructor() {
    this.sessions = new Map(); // canvasId -> session
    this.userSessions = new Map(); // socketId -> canvasId
  }

  createSession(canvasId) {
    if (!this.sessions.has(canvasId)) {
      this.sessions.set(canvasId, {
        id: canvasId,
        users: new Map(),
        canvasState: {
          nodes: [],
          connections: []
        },
        operations: [],
        lastUpdate: Date.now()
      });
    }
    return this.sessions.get(canvasId);
  }

  getUsersInSession(canvasId) {
    const session = this.sessions.get(canvasId);
    return session ? Array.from(session.users.values()) : [];
  }

  addUserToSession(socketId, canvasId, userInfo) {
    const session = this.createSession(canvasId);
    session.users.set(socketId, {
      socketId,
      ...userInfo,
      joinedAt: Date.now()
    });
    this.userSessions.set(socketId, canvasId);
    return session;
  }

  removeUserFromSession(socketId) {
    const canvasId = this.userSessions.get(socketId);
    if (canvasId) {
      const session = this.sessions.get(canvasId);
      if (session) {
        session.users.delete(socketId);
        if (session.users.size === 0) {
          // 如果没有用户了，可以选择保留会话或删除
          // this.sessions.delete(canvasId);
        }
      }
      this.userSessions.delete(socketId);
    }
    return canvasId;
  }

  handleConflict(canvasId, operation) {
    const session = this.sessions.get(canvasId);
    if (!session) return null;

    // 简单的冲突解决：最后写入获胜
    session.operations.push({
      ...operation,
      timestamp: Date.now(),
      id: this.generateOperationId()
    });

    // 保留最近100个操作
    if (session.operations.length > 100) {
      session.operations = session.operations.slice(-100);
    }

    return operation;
  }

  syncCanvasState(canvasId, state) {
    const session = this.sessions.get(canvasId);
    if (session) {
      session.canvasState = { ...state };
      session.lastUpdate = Date.now();
    }
  }

  generateOperationId() {
    return Date.now().toString(36) + Math.random().toString(36).substr(2);
  }
}

// 操作事件处理器
class OperationEventHandler {
  constructor(sessionManager, dataPersistence) {
    this.sessionManager = sessionManager;
    this.dataPersistence = dataPersistence;
  }

  handleNodeCreate(canvasId, nodeData, userId) {
    const operation = {
      type: 'node_create',
      canvasId,
      userId,
      data: nodeData,
      timestamp: Date.now()
    };

    const resolvedOperation = this.sessionManager.handleConflict(canvasId, operation);
    if (resolvedOperation) {
      // 更新会话状态
      const session = this.sessionManager.sessions.get(canvasId);
      if (session) {
        session.canvasState.nodes.push(nodeData);
      }
      
      // 异步保存
      this.dataPersistence.saveOperation(operation);
    }

    return resolvedOperation;
  }

  handleNodeUpdate(canvasId, nodeData, userId) {
    const operation = {
      type: 'node_update',
      canvasId,
      userId,
      data: nodeData,
      timestamp: Date.now()
    };

    const resolvedOperation = this.sessionManager.handleConflict(canvasId, operation);
    if (resolvedOperation) {
      // 更新会话状态
      const session = this.sessionManager.sessions.get(canvasId);
      if (session) {
        const nodeIndex = session.canvasState.nodes.findIndex(n => n.id === nodeData.id);
        if (nodeIndex !== -1) {
          session.canvasState.nodes[nodeIndex] = { ...session.canvasState.nodes[nodeIndex], ...nodeData };
        }
      }
      
      this.dataPersistence.saveOperation(operation);
    }

    return resolvedOperation;
  }

  handleNodeDelete(canvasId, nodeId, userId) {
    const operation = {
      type: 'node_delete',
      canvasId,
      userId,
      data: { nodeId },
      timestamp: Date.now()
    };

    const resolvedOperation = this.sessionManager.handleConflict(canvasId, operation);
    if (resolvedOperation) {
      // 更新会话状态
      const session = this.sessionManager.sessions.get(canvasId);
      if (session) {
        session.canvasState.nodes = session.canvasState.nodes.filter(n => n.id !== nodeId);
        session.canvasState.connections = session.canvasState.connections.filter(
          c => c.sourceId !== nodeId && c.targetId !== nodeId
        );
      }
      
      this.dataPersistence.saveOperation(operation);
    }

    return resolvedOperation;
  }

  handleConnectionCreate(canvasId, connectionData, userId) {
    const operation = {
      type: 'connection_create',
      canvasId,
      userId,
      data: connectionData,
      timestamp: Date.now()
    };

    const resolvedOperation = this.sessionManager.handleConflict(canvasId, operation);
    if (resolvedOperation) {
      // 更新会话状态
      const session = this.sessionManager.sessions.get(canvasId);
      if (session) {
        session.canvasState.connections.push(connectionData);
      }
      
      this.dataPersistence.saveOperation(operation);
    }

    return resolvedOperation;
  }
}

// 数据持久化服务（内存版本，生产环境应使用数据库）
class DataPersistenceService {
  constructor() {
    this.canvasStates = new Map();
    this.operations = [];
  }

  async saveCanvasState(canvasId, state) {
    this.canvasStates.set(canvasId, {
      ...state,
      lastSaved: Date.now()
    });
    return true;
  }

  async loadCanvasState(canvasId) {
    return this.canvasStates.get(canvasId) || {
      nodes: [],
      connections: [],
      lastSaved: Date.now()
    };
  }

  async saveOperation(operation) {
    this.operations.push(operation);
    // 保留最近1000个操作
    if (this.operations.length > 1000) {
      this.operations = this.operations.slice(-1000);
    }
    return true;
  }

  async getOperationHistory(canvasId, limit = 50) {
    return this.operations
      .filter(op => op.canvasId === canvasId)
      .slice(-limit);
  }
}

// 初始化服务
const sessionManager = new CollaborationSessionManager();
const dataPersistence = new DataPersistenceService();
const operationHandler = new OperationEventHandler(sessionManager, dataPersistence);

// WebSocket服务器
io.on('connection', (socket) => {
  console.log('用户连接:', socket.id);

  // 加入画布房间
  socket.on('joinCanvas', async (data) => {
    try {
      const { canvasId, userInfo } = data;
      
      // 离开之前的房间
      const previousCanvasId = sessionManager.userSessions.get(socket.id);
      if (previousCanvasId) {
        socket.leave(previousCanvasId);
        sessionManager.removeUserFromSession(socket.id);
        socket.to(previousCanvasId).emit('userLeft', {
          userId: socket.id,
          canvasId: previousCanvasId
        });
      }

      // 加入新房间
      socket.join(canvasId);
      const session = sessionManager.addUserToSession(socket.id, canvasId, userInfo);
      
      // 加载画布状态
      const canvasState = await dataPersistence.loadCanvasState(canvasId);
      sessionManager.syncCanvasState(canvasId, canvasState);
      
      // 发送当前画布状态给新用户
      socket.emit('canvasStateSync', {
        canvasState: session.canvasState,
        users: sessionManager.getUsersInSession(canvasId)
      });
      
      // 通知其他用户有新用户加入
      socket.to(canvasId).emit('userJoined', {
        user: { socketId: socket.id, ...userInfo },
        canvasId
      });
      
      console.log(`用户 ${socket.id} 加入画布 ${canvasId}`);
    } catch (error) {
      console.error('加入画布失败:', error);
      socket.emit('error', { message: '加入画布失败' });
    }
  });

  // 离开画布房间
  socket.on('leaveCanvas', () => {
    const canvasId = sessionManager.removeUserFromSession(socket.id);
    if (canvasId) {
      socket.leave(canvasId);
      socket.to(canvasId).emit('userLeft', {
        userId: socket.id,
        canvasId
      });
      console.log(`用户 ${socket.id} 离开画布 ${canvasId}`);
    }
  });

  // 画布更新事件
  socket.on('canvasUpdate', async (data) => {
    try {
      const canvasId = sessionManager.userSessions.get(socket.id);
      if (!canvasId) {
        socket.emit('error', { message: '未加入任何画布' });
        return;
      }

      const { type, payload } = data;
      let operation = null;

      switch (type) {
        case 'node_create':
          operation = operationHandler.handleNodeCreate(canvasId, payload, socket.id);
          break;
        case 'node_update':
          operation = operationHandler.handleNodeUpdate(canvasId, payload, socket.id);
          break;
        case 'node_delete':
          operation = operationHandler.handleNodeDelete(canvasId, payload.nodeId, socket.id);
          break;
        case 'connection_create':
          operation = operationHandler.handleConnectionCreate(canvasId, payload, socket.id);
          break;
        default:
          console.log('未知操作类型:', type);
          return;
      }

      if (operation) {
        // 广播给房间内其他用户
        socket.to(canvasId).emit('canvasUpdate', {
          type,
          payload,
          userId: socket.id,
          timestamp: operation.timestamp
        });

        // 异步保存画布状态
        const session = sessionManager.sessions.get(canvasId);
        if (session) {
          dataPersistence.saveCanvasState(canvasId, session.canvasState);
        }
      }
    } catch (error) {
      console.error('处理画布更新失败:', error);
      socket.emit('error', { message: '更新失败' });
    }
  });

  // 获取操作历史
  socket.on('getOperationHistory', async (data) => {
    try {
      const { canvasId, limit } = data;
      const history = await dataPersistence.getOperationHistory(canvasId, limit);
      socket.emit('operationHistory', { canvasId, history });
    } catch (error) {
      console.error('获取操作历史失败:', error);
      socket.emit('error', { message: '获取历史失败' });
    }
  });

  // 用户断开连接
  socket.on('disconnect', () => {
    const canvasId = sessionManager.removeUserFromSession(socket.id);
    if (canvasId) {
      socket.to(canvasId).emit('userLeft', {
        userId: socket.id,
        canvasId
      });
    }
    console.log('用户断开连接:', socket.id);
  });
});

// API路由
app.get('/api/canvas/:canvasId', async (req, res) => {
  try {
    const { canvasId } = req.params;
    const canvasState = await dataPersistence.loadCanvasState(canvasId);
    res.json({ success: true, data: canvasState });
  } catch (error) {
    res.status(500).json({ success: false, message: error.message });
  }
});

app.post('/api/canvas/:canvasId', async (req, res) => {
  try {
    const { canvasId } = req.params;
    const { canvasState } = req.body;
    await dataPersistence.saveCanvasState(canvasId, canvasState);
    res.json({ success: true });
  } catch (error) {
    res.status(500).json({ success: false, message: error.message });
  }
});

app.get('/api/canvas/:canvasId/users', (req, res) => {
  try {
    const { canvasId } = req.params;
    const users = sessionManager.getUsersInSession(canvasId);
    res.json({ success: true, data: users });
  } catch (error) {
    res.status(500).json({ success: false, message: error.message });
  }
});

// 提供静态文件
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'index.html'));
});

const PORT = process.env.PORT || 3000;
server.listen(PORT, () => {
  console.log(`服务器运行在端口 ${PORT}`);
});