# 久坐提醒 App — 实施方案

## 功能概览

| 功能 | 说明 |
|------|------|
| 倒计时计时器 | 默认 45 分钟，可自定义（5-120 分钟） |
| 桌面通知 | 计时结束时通过浏览器 Notification API 弹出提醒 |
| 开始 / 暂停 / 重置 | 基础计时控制 |
| 休息计时 | 提醒后自动进入 5 分钟休息倒计时 |
| 今日统计 | 记录当日完成的工作周期次数 |
| LocalStorage 持久化 | 配置和统计数据不丢失 |

## 技术选型

| 项 | 选型 | 理由 |
|----|------|------|
| 框架 | **React 18 + TypeScript** | 组件化、类型安全 |
| 构建 | **Vite 5** | 极速 HMR，零配置起步 |
| 样式 | **CSS Modules** | 零运行时、天然隔离 |
| 通知 | **Notification API** | 浏览器原生，无需安装 |
| 持久化 | **LocalStorage** | 简单够用 |
| 图标 | **SVG 内联** | 零依赖 |

## 组件树

```
App
├── Header              — 标题 + 日期
├── TimerCircle          — 环形进度条 + 倒计时数字
├── TimerControls        — 开始/暂停、重置按钮
├── DurationSelector     — 自定义时长滑块
└── StatsPanel           — 今日统计卡片
```

## 目录结构

```
sit-reminder/
├── index.html
├── package.json
├── vite.config.ts
├── tsconfig.json
└── src/
    ├── main.tsx
    ├── App.tsx
    ├── App.module.css
    ├── components/
    │   ├── TimerCircle.tsx / .css
    │   ├── TimerControls.tsx / .css
    │   ├── DurationSelector.tsx / .css
    │   └── StatsPanel.tsx / .css
    ├── hooks/
    │   ├── useTimer.ts
    │   └── useNotification.ts
    └── utils/
        └── storage.ts
```

## 核心逻辑

### useTimer Hook
- `duration` — 工作时长（秒）
- `timeLeft` — 剩余时间（秒）
- `status` — `idle | running | paused | resting`
- 每 1 秒 tick，到 0 触发 onComplete 回调
- 休息模式：5 分钟倒计时

### 通知流程
1. 工作计时到 0 → 请求 Notification 权限 → 弹通知"该起来活动了！"
2. 自动进入休息模式（5 分钟）
3. 休息结束 → 弹通知"可以继续工作了" → 回到 idle

### 数据存储
```ts
interface StoredData {
  duration: number;      // 工作时长（秒）
  todayCount: number;    // 今日完成次数
  todayDate: string;     // 日期，用于跨天重置
}
```

## 实施步骤

1. **初始化项目** — Vite + React + TypeScript 脚手架
2. **实现 useTimer hook** — 核心计时逻辑
3. **实现 TimerCircle 组件** — SVG 环形进度条
4. **实现控制组件** — 按钮 + 时长选择
5. **实现 StatsPanel** — 今日统计
6. **集成 Notification** — 桌面提醒
7. **整体样式打磨** — 视觉效果

## 预览

纯 Web 应用，启动 `npm run dev` 后在浏览器中直接使用。支持 Chrome/Firefox/Edge。