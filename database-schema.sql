-- 工作流画布系统数据库设计
-- 数据库: workflow_canvas

-- 用户表
CREATE TABLE users (
    id VARCHAR(24) PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    avatar_url VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- 画布表
CREATE TABLE canvases (
    id VARCHAR(24) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    owner_id VARCHAR(24) NOT NULL,
    view_state JSON COMMENT '视图状态（缩放、平移等）',
    metadata JSON COMMENT '元数据信息',
    is_public BOOLEAN DEFAULT FALSE,
    tags JSON COMMENT '标签列表',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (owner_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_owner_id (owner_id),
    INDEX idx_created_at (created_at)
);

-- 节点表
CREATE TABLE nodes (
    id VARCHAR(24) PRIMARY KEY,
    canvas_id VARCHAR(24) NOT NULL,
    type VARCHAR(50) NOT NULL COMMENT '节点类型',
    name VARCHAR(100) NOT NULL,
    position JSON NOT NULL COMMENT '节点位置坐标 {x, y}',
    size JSON COMMENT '节点尺寸 {width, height}',
    config JSON COMMENT '节点配置参数',
    status VARCHAR(20) DEFAULT 'inactive' COMMENT '节点状态',
    input_ports JSON COMMENT '输入端口配置',
    output_ports JSON COMMENT '输出端口配置',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (canvas_id) REFERENCES canvases(id) ON DELETE CASCADE,
    INDEX idx_canvas_id (canvas_id),
    INDEX idx_type (type)
);

-- 连线表
CREATE TABLE connections (
    id VARCHAR(24) PRIMARY KEY,
    canvas_id VARCHAR(24) NOT NULL,
    source_node_id VARCHAR(24) NOT NULL,
    source_port VARCHAR(50) NOT NULL,
    target_node_id VARCHAR(24) NOT NULL,
    target_port VARCHAR(50) NOT NULL,
    data_mapping JSON COMMENT '数据映射配置',
    condition JSON COMMENT '连接条件',
    style JSON COMMENT '连线样式',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (canvas_id) REFERENCES canvases(id) ON DELETE CASCADE,
    FOREIGN KEY (source_node_id) REFERENCES nodes(id) ON DELETE CASCADE,
    FOREIGN KEY (target_node_id) REFERENCES nodes(id) ON DELETE CASCADE,
    INDEX idx_canvas_id (canvas_id),
    INDEX idx_source_node (source_node_id),
    INDEX idx_target_node (target_node_id)
);

-- 工作流表
CREATE TABLE workflows (
    id VARCHAR(24) PRIMARY KEY,
    canvas_id VARCHAR(24) NOT NULL,
    name VARCHAR(100) NOT NULL,
    status VARCHAR(20) DEFAULT 'inactive' COMMENT '执行状态: inactive, running, completed, failed, paused',
    start_time TIMESTAMP NULL,
    end_time TIMESTAMP NULL,
    execution_log JSON COMMENT '执行日志',
    schedule JSON COMMENT '调度配置',
    variables JSON COMMENT '工作流变量',
    trigger_type VARCHAR(20) DEFAULT 'manual' COMMENT '触发类型: manual, scheduled, webhook',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (canvas_id) REFERENCES canvases(id) ON DELETE CASCADE,
    INDEX idx_canvas_id (canvas_id),
    INDEX idx_status (status),
    INDEX idx_start_time (start_time)
);

-- 协作表
CREATE TABLE collaborations (
    id VARCHAR(24) PRIMARY KEY,
    canvas_id VARCHAR(24) NOT NULL,
    user_id VARCHAR(24) NOT NULL,
    permission VARCHAR(20) NOT NULL COMMENT '权限级别: owner, editor, viewer',
    cursor_position JSON COMMENT '光标位置',
    is_online BOOLEAN DEFAULT FALSE,
    last_activity TIMESTAMP NULL,
    changes JSON COMMENT '变更记录',
    invited_by VARCHAR(24),
    joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (canvas_id) REFERENCES canvases(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (invited_by) REFERENCES users(id) ON DELETE SET NULL,
    UNIQUE KEY unique_canvas_user (canvas_id, user_id),
    INDEX idx_canvas_id (canvas_id),
    INDEX idx_user_id (user_id),
    INDEX idx_is_online (is_online)
);

-- 变更历史表
CREATE TABLE change_history (
    id VARCHAR(24) PRIMARY KEY,
    canvas_id VARCHAR(24) NOT NULL,
    user_id VARCHAR(24) NOT NULL,
    action VARCHAR(50) NOT NULL COMMENT '操作类型: create, update, delete, move',
    target_type VARCHAR(20) NOT NULL COMMENT '目标类型: node, connection, canvas',
    target_id VARCHAR(24) COMMENT '目标ID',
    old_data JSON COMMENT '变更前数据',
    new_data JSON COMMENT '变更后数据',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (canvas_id) REFERENCES canvases(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_canvas_id (canvas_id),
    INDEX idx_user_id (user_id),
    INDEX idx_created_at (created_at),
    INDEX idx_target (target_type, target_id)
);

-- 工作流执行历史表
CREATE TABLE workflow_executions (
    id VARCHAR(24) PRIMARY KEY,
    workflow_id VARCHAR(24) NOT NULL,
    status VARCHAR(20) NOT NULL,
    start_time TIMESTAMP NOT NULL,
    end_time TIMESTAMP NULL,
    duration INT COMMENT '执行时长（秒）',
    trigger_type VARCHAR(20) NOT NULL,
    trigger_data JSON COMMENT '触发数据',
    execution_log JSON COMMENT '详细执行日志',
    error_message TEXT COMMENT '错误信息',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (workflow_id) REFERENCES workflows(id) ON DELETE CASCADE,
    INDEX idx_workflow_id (workflow_id),
    INDEX idx_status (status),
    INDEX idx_start_time (start_time)
);

-- 节点模板表
CREATE TABLE node_templates (
    id VARCHAR(24) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    category VARCHAR(50) NOT NULL,
    description TEXT,
    icon VARCHAR(255),
    config_schema JSON COMMENT '配置参数模式',
    input_schema JSON COMMENT '输入端口模式',
    output_schema JSON COMMENT '输出端口模式',
    is_system BOOLEAN DEFAULT FALSE COMMENT '是否系统模板',
    created_by VARCHAR(24),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (created_by) REFERENCES users(id) ON DELETE SET NULL,
    INDEX idx_category (category),
    INDEX idx_is_system (is_system)
);

-- 创建视图：用户画布统计
CREATE VIEW user_canvas_stats AS
SELECT 
    u.id as user_id,
    u.username,
    COUNT(c.id) as total_canvases,
    COUNT(CASE WHEN c.is_public = TRUE THEN 1 END) as public_canvases,
    MAX(c.updated_at) as last_canvas_update
FROM users u
LEFT JOIN canvases c ON u.id = c.owner_id
GROUP BY u.id, u.username;

-- 创建视图：画布活跃度统计
CREATE VIEW canvas_activity_stats AS
SELECT 
    c.id as canvas_id,
    c.name as canvas_name,
    COUNT(DISTINCT n.id) as node_count,
    COUNT(DISTINCT conn.id) as connection_count,
    COUNT(DISTINCT col.user_id) as collaborator_count,
    MAX(ch.created_at) as last_change_time
FROM canvases c
LEFT JOIN nodes n ON c.id = n.canvas_id
LEFT JOIN connections conn ON c.id = conn.canvas_id
LEFT JOIN collaborations col ON c.id = col.canvas_id
LEFT JOIN change_history ch ON c.id = ch.canvas_id
GROUP BY c.id, c.name;

-- 插入示例数据
INSERT INTO users (id, username, email, password_hash) VALUES
('user_001', 'admin', 'admin@example.com', '$2b$10$example_hash'),
('user_002', 'designer', 'designer@example.com', '$2b$10$example_hash'),
('user_003', 'developer', 'developer@example.com', '$2b$10$example_hash');

INSERT INTO node_templates (id, name, category, description, config_schema, input_schema, output_schema, is_system) VALUES
('template_001', 'HTTP请求', 'network', '发送HTTP请求', '{"url": {"type": "string", "required": true}, "method": {"type": "string", "enum": ["GET", "POST", "PUT", "DELETE"]}}', '[]', '[{"name": "response", "type": "object"}]', TRUE),
('template_002', '数据转换', 'transform', '数据格式转换', '{"mapping": {"type": "object"}}', '[{"name": "input", "type": "any"}]', '[{"name": "output", "type": "any"}]', TRUE),
('template_003', '条件判断', 'logic', '根据条件分支执行', '{"condition": {"type": "string", "required": true}}', '[{"name": "input", "type": "any"}]', '[{"name": "true", "type": "any"}, {"name": "false", "type": "any"}]', TRUE);