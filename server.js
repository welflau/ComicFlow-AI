const express = require('express');
const http = require('http');
const socketIo = require('socket.io');
const path = require('path');
const fs = require('fs').promises;

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

// 协作状态管理器
class CollaborationStateManager {
  constructor() {
    this.canvasStates = new Map(); // canvasId -> state
    this.usersInCanvas = new Map(); // canvasId -> Set of users
    this.userSockets = new Map(); // socketId -> user info
  }

  getCanvasState(canvasId) {
    if (!this.canvasStates.has(canvasId)) {
      this.canvasStates.set(canvasId, {
        nodes: new Map(),
        connections: new Map(),
        lastUpdated: Date.now()
      });
    }
    return this.canvasStates.get(canvasId);
  }

  updateCanvasState(canvasId, operation) {
    const state = this.getCanvasState(canvasId);
    
    switch (operation.type) {
      case 'node-create':
        state.nodes.set(operation.data.id, operation.data);
        break;
      case 'node-update':
        if (state.nodes.has(operation.data.id)) {
          const existingNode = state.nodes.get(operation.data.id);
          state.nodes.set(operation.data.id, { ...existingNode, ...operation.data });
        }
        break;
      case 'node-delete':
        state.nodes.delete(operation.data.id);
        // 删除相关连接
        for (let [connId, conn] of state.connections) {
          if (conn.sourceId === operation.data.id || conn.targetId === operation.data.id) {
            state.connections.delete(connId);
          }
        }
        break;
      case 'connection-create':
        state.connections.set(operation.data.id, operation.data);
        break;
      case 'connection-delete':
        state.connections.delete(operation.data.id);
        break;
    }
    
    state.lastUpdated = Date.now();
    return state;
  }

  getUsersInCanvas(canvasId) {
    return Array.from(this.usersInCanvas.get(canvasId) || []);
  }

  addUserToCanvas(canvasId, socketId, userInfo) {
    if (!this.usersInCanvas.has(canvasId)) {
      this.usersInCanvas.set(canvasId, new Set());
    }
    this.usersInCanvas.get(canvasId).add(socketId);
    this.userSockets.set(socketId, { ...userInfo, canvasId });
  }

  removeUserFromCanvas(socketId) {
    const userInfo = this.userSockets.get(socketId);
    if (userInfo) {
      const canvasUsers = this.usersInCanvas.get(userInfo.canvasId);
      if (canvasUsers) {
        canvasUsers.delete(socketId);
      }
      this.userSockets.delete(socketId);
    }
    return userInfo;
  }

  resolveConflict(operation1, operation2) {
    // 简单的时间戳冲突解决策略
    return operation1.timestamp > operation2.timestamp ? operation1 : operation2;
  }
}

// 消息处理器
class MessageHandler {
  constructor(stateManager, persistenceService) {
    this.stateManager = stateManager;
    this.persistenceService = persistenceService;
  }

  handleNodeMove(canvasId, data, socket) {
    const operation = {
      type: 'node-update',
      data: { id: data.nodeId, x: data.x, y: data.y },
      timestamp: Date.now(),
      userId: socket.id
    };
    
    this.stateManager.updateCanvasState(canvasId, operation);
    socket.to(canvasId).emit('node-moved', {
      nodeId: data.nodeId,
      x: data.x,
      y: data.y,
      userId: socket.id
    });
    
    this.persistenceService.logOperation(canvasId, operation);
  }

  handleNodeCreate(canvasId, data, socket) {
    const nodeData = {
      id: data.id || `node_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
      type: data.type,
      x: data.x,
      y: data.y,
      title: data.title,
      createdBy: socket.id,
      createdAt: Date.now()
    };
    
    const operation = {
      type: 'node-create',
      data: nodeData,
      timestamp: Date.now(),
      userId: socket.id
    };
    
    this.stateManager.updateCanvasState(canvasId, operation);
    socket.to(canvasId).emit('node-created', nodeData);
    
    this.persistenceService.logOperation(canvasId, operation);
    return nodeData;
  }

  handleNodeDelete(canvasId, data, socket) {
    const operation = {
      type: 'node-delete',
      data: { id: data.nodeId },
      timestamp: Date.now(),
      userId: socket.id
    };
    
    this.stateManager.updateCanvasState(canvasId, operation);
    socket.to(canvasId).emit('node-deleted', { nodeId: data.nodeId, userId: socket.id });
    
    this.persistenceService.logOperation(canvasId, operation);
  }

  handleConnection(canvasId, data, socket) {
    const connectionData = {
      id: data.id || `conn_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
      sourceId: data.sourceId,
      targetId: data.targetId,
      createdBy: socket.id,
      createdAt: Date.now()
    };
    
    const operation = {
      type: 'connection-create',
      data: connectionData,
      timestamp: Date.now(),
      userId: socket.id
    };
    
    this.stateManager.updateCanvasState(canvasId, operation);
    socket.to(canvasId).emit('connection-created', connectionData);
    
    this.persistenceService.logOperation(canvasId, operation);
    return connectionData;
  }
}

// 持久化服务
class PersistenceService {
  constructor() {
    this.dataDir = path.join(__dirname, 'data');
    this.ensureDataDir();
  }

  async ensureDataDir() {
    try {
      await fs.mkdir(this.dataDir, { recursive: true });
    } catch (error) {
      console.error('Failed to create data directory:', error);
    }
  }

  async saveCanvasState(canvasId, state) {
    try {
      const filePath = path.join(this.dataDir, `canvas_${canvasId}.json`);
      const serializedState = {
        nodes: Object.fromEntries(state.nodes),
        connections: Object.fromEntries(state.connections),
        lastUpdated: state.lastUpdated
      };
      await fs.writeFile(filePath, JSON.stringify(serializedState, null, 2));
    } catch (error) {
      console.error('Failed to save canvas state:', error);
    }
  }

  async loadCanvasState(canvasId) {
    try {
      const filePath = path.join(this.dataDir, `canvas_${canvasId}.json`);
      const data = await fs.readFile(filePath, 'utf8');
      const parsed = JSON.parse(data);
      return {
        nodes: new Map(Object.entries(parsed.nodes)),
        connections: new Map(Object.entries(parsed.connections)),
        lastUpdated: parsed.lastUpdated
      };
    } catch (error) {
      console.log('No existing canvas state found, creating new one');
      return {
        nodes: new Map(),
        connections: new Map(),
        lastUpdated: Date.now()
      };
    }
  }

  async logOperation(canvasId, operation) {
    try {
      const logPath = path.join(this.dataDir, `log_${canvasId}.jsonl`);
      const logEntry = JSON.stringify({ ...operation, timestamp: Date.now() }) + '\n';
      await fs.appendFile(logPath, logEntry);
    } catch (error) {
      console.error('Failed to log operation:', error);
    }
  }
}

// 初始化服务
const stateManager = new CollaborationStateManager();
const persistenceService = new PersistenceService();
const messageHandler = new MessageHandler(stateManager, persistenceService);

// WebSocket连接处理
io.on('connection', (socket) => {
  console.log('User connected:', socket.id);

  // 加入画布房间
  socket.on('join-canvas', async (data) => {
    const { canvasId, userInfo } = data;
    
    // 加入Socket.IO房间
    socket.join(canvasId);
    
    // 添加用户到状态管理器
    stateManager.addUserToCanvas(canvasId, socket.id, userInfo);
    
    // 加载并发送当前画布状态
    const canvasState = await persistenceService.loadCanvasState(canvasId);
    stateManager.canvasStates.set(canvasId, canvasState);
    
    socket.emit('canvas-state', {
      nodes: Object.fromEntries(canvasState.nodes),
      connections: Object.fromEntries(canvasState.connections)
    });
    
    // 通知其他用户有新用户加入
    socket.to(canvasId).emit('user-joined', {
      userId: socket.id,
      userInfo: userInfo
    });
    
    // 发送当前在线用户列表
    const onlineUsers = stateManager.getUsersInCanvas(canvasId);
    socket.emit('online-users', onlineUsers);
    
    console.log(`User ${socket.id} joined canvas ${canvasId}`);
  });

  // 节点移动
  socket.on('node-move', (data) => {
    const userInfo = stateManager.userSockets.get(socket.id);
    if (userInfo) {
      messageHandler.handleNodeMove(userInfo.canvasId, data, socket);
    }
  });

  // 节点创建
  socket.on('node-create', (data) => {
    const userInfo = stateManager.userSockets.get(socket.id);
    if (userInfo) {
      const nodeData = messageHandler.handleNodeCreate(userInfo.canvasId, data, socket);
      socket.emit('node-create-confirm', nodeData);
    }
  });

  // 节点删除
  socket.on('node-delete', (data) => {
    const userInfo = stateManager.userSockets.get(socket.id);
    if (userInfo) {
      messageHandler.handleNodeDelete(userInfo.canvasId, data, socket);
    }
  });

  // 创建连接
  socket.on('connection-create', (data) => {
    const userInfo = stateManager.userSockets.get(socket.id);
    if (userInfo) {
      const connectionData = messageHandler.handleConnection(userInfo.canvasId, data, socket);
      socket.emit('connection-create-confirm', connectionData);
    }
  });

  // 画布更新（批量操作）
  socket.on('canvas-update', (data) => {
    const userInfo = stateManager.userSockets.get(socket.id);
    if (userInfo) {
      socket.to(userInfo.canvasId).emit('canvas-updated', {
        ...data,
        userId: socket.id
      });
    }
  });

  // 用户断开连接
  socket.on('disconnect', async () => {
    const userInfo = stateManager.removeUserFromCanvas(socket.id);
    
    if (userInfo) {
      // 保存画布状态
      const canvasState = stateManager.getCanvasState(userInfo.canvasId);
      await persistenceService.saveCanvasState(userInfo.canvasId, canvasState);
      
      // 通知其他用户
      socket.to(userInfo.canvasId).emit('user-left', {
        userId: socket.id
      });
      
      console.log(`User ${socket.id} left canvas ${userInfo.canvasId}`);
    }
    
    console.log('User disconnected:', socket.id);
  });

  // 心跳检测
  socket.on('ping', () => {
    socket.emit('pong');
  });
});

// 定期保存画布状态
setInterval(async () => {
  for (let [canvasId, state] of stateManager.canvasStates) {
    await persistenceService.saveCanvasState(canvasId, state);
  }
}, 30000); // 每30秒保存一次

const PORT = process.env.PORT || 3000;
server.listen(PORT, () => {
  console.log(`WebSocket collaboration server running on port ${PORT}`);
});