# 架构设计 - 前端基础架构搭建

## 架构模式
渐进式前端架构迁移

## 技术栈

- **language**: TypeScript
- **framework**: Vue3 + Vite
- **styling**: Tailwind CSS
- **3d_engine**: Three.js

## 模块设计

### Vue3项目初始化
职责: 创建Vue3+TS+Vite项目结构，保留现有认证功能
- vite.config.ts配置
- tsconfig.json配置
- main.ts入口文件
- App.vue根组件

### 认证页面Vue化
职责: 将现有public/index.html的认证功能迁移为Vue组件
- AuthForm.vue组件
- useAuth.ts组合式API
- auth.service.ts服务层

### Three.js集成模块
职责: 集成Three.js并创建3D画布基础组件
- ThreeCanvas.vue组件
- useThree.ts组合式API
- three.service.ts服务层

### Tailwind CSS配置
职责: 配置Tailwind CSS并迁移现有样式
- tailwind.config.js配置
- main.css样式入口
- 组件样式类定义

### 路由系统
职责: 配置Vue Router，建立认证和主应用路由
- router/index.ts路由配置
- views/Auth.vue认证页面
- views/Dashboard.vue主页面

## 数据流
用户访问 -> Vue Router路由判断 -> 未认证跳转Auth.vue(复用现有认证逻辑) -> 认证成功进入Dashboard.vue -> Three.js画布初始化 -> 与后端API交互保持现有接口不变

## 关键决策
- 保留现有认证逻辑和API接口，仅将前端UI迁移到Vue3
- 采用组合式API(Composition API)提高代码复用性
- Three.js封装为Vue组件，便于状态管理和生命周期控制
- Tailwind CSS采用渐进式迁移，先保留关键样式后逐步优化
- 使用Vite作为构建工具，提供快速开发体验
- TypeScript配置为严格模式，确保代码质量
