---
name: "Playwright 反爬绕过"
description: "Playwright 隐身网页抓取技能，支持反爬绕过、浏览器指纹伪装、验证码处理。适用于 Cloudflare 5秒盾、403 拦截、navigator.webdriver 检测等反爬场景。当需要抓取受反爬保护的网站、遇到 Cloudflare 拦截或 403 错误、需要隐藏自动化痕迹时使用。"
globs: ["*.js", "*.ts"]
alwaysAllow: ["Bash"]
---

# Playwright 反爬绕过

基于 Playwright 的隐身网页抓取技能，根据目标网站的反爬级别选择最优方案。

## 用例矩阵

| 目标网站 | 反爬级别 | 推荐方案 | 脚本 |
|---------|---------|---------|------|
| 普通静态站点 | 低 | 直接请求 | 无需脚本 |
| 动态渲染站点 | 中 | Playwright Simple | `scripts/playwright-simple.js` |
| Cloudflare/反爬保护 | 高 | **Playwright Stealth** ⭐ | `scripts/playwright-stealth.js` |

## 环境准备

```bash
cd 
npm install
npx playwright install chromium
```

## 快速开始

### 1. 动态渲染站点（无反爬）

```bash
node scripts/playwright-simple.js "https://example.com"
```

输出 JSON：`{ url, title, content, elapsedSeconds }`

### 2. 反爬保护站点（Cloudflare 等）⭐

```bash
node scripts/playwright-stealth.js "https://target-site.com"
```

核心反爬措施：
- 隐藏 `navigator.webdriver`（设为 false）
- 注入真实设备 User-Agent（iPhone/Android）
- 随机延迟模拟人类行为
- 自动截图与 HTML 保存

### 3. 环境变量配置

```bash
# 有头模式（有时成功率更高）
HEADLESS=false node scripts/playwright-stealth.js URL

# 自定义等待时间（毫秒）
WAIT_TIME=15000 node scripts/playwright-stealth.js URL

# 自定义 User-Agent
USER_AGENT="Mozilla/5.0 ..." node scripts/playwright-stealth.js URL

# 保存 HTML 快照
SAVE_HTML=true node scripts/playwright-stealth.js URL

# 自定义截图路径
SCREENSHOT_PATH=/path/to/shot.png node scripts/playwright-stealth.js URL
```

## 最佳实践

1. **先试简单方案** — 能用普通请求就不要启动浏览器
2. **动态渲染用 Simple** — 需要等待 JS 时用 `playwright-simple.js`
3. **被拦截用 Stealth** — 遇到 403/Cloudflare 用 `playwright-stealth.js`
4. **有头模式兜底** — `HEADLESS=false` 有时通过率更高
5. **加大等待时间** — Cloudflare 挑战页需要 10-15 秒
6. **避免高级框架** — Crawlee/Selenium 更易被检测，纯 Playwright 最隐蔽

## 故障排除

| 问题 | 解决方案 |
|------|---------|
| 403 Forbidden | 切换到 `playwright-stealth.js` |
| Cloudflare 挑战页 | 增大 `WAIT_TIME`，尝试 `HEADLESS=false`，考虑代理 IP |
| 空白页面 | 增大等待时间，检查是否需要登录 |
| 超时 | 检查网络，尝试 `waitUntil: 'domcontentloaded'` |

## 详细参考

反爬技术原理、有效/无效措施对比、性能基准测试数据，详见 `references/anti-bot-techniques.md`。
