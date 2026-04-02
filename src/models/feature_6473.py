"""
数据库架构设计和环境搭建 - 数据模型
"""

FEATURE_6473_SCHEMA = {
    "table": "feature_6473",
    "columns": [
        {"name": "id", "type": "TEXT PRIMARY KEY"},
        {"name": "name", "type": "TEXT NOT NULL"},
        {"name": "created_at", "type": "TEXT NOT NULL"},
    ]
}
