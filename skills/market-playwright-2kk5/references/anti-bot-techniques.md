# 反爬技术详细参考

## 目录

1. [有效反爬措施](#有效反爬措施)
2. [无效反爬措施](#无效反爬措施)
3. [性能基准测试](#性能基准测试)
4. [Cloudflare 绕过策略](#cloudflare-绕过策略)
5. [浏览器指纹伪装详解](#浏览器指纹伪装详解)

---

## 有效反爬措施

### 1. 隐藏 navigator.webdriver ⭐ 必需

Cloudflare 等反爬系统通过检测 `navigator.webdriver` 判断是否为自动化浏览器。

```javascript
Object.defineProperty(navigator, 'webdriver', { get: () => false });
```

**关键**：必须在页面加载前注入（使用 `addInitScript`），否则页面脚本会先读到 `true`。

### 2. 真实 User-Agent

使用真实移动设备 UA（iPhone/Android），比桌面 Chrome 更不易被检测。移动端流量占比高，反爬系统对移动端通常更宽松。

### 3. 模拟人类行为

- 随机延迟（1-3 秒页面停留）
- 随机滚动距离
- 非匀速鼠标移动轨迹

### 4. 避免框架签名

Crawlee、Selenium 等高级框架有独特的网络请求模式和 JS 特征，容易被指纹检测识别。纯 Playwright 最接近原生浏览器行为。

### 5. 使用 addInitScript（Playwright 独有优势）

在页面 JS 执行前注入反检测代码。Puppeteer 的 `evaluateOnNewDocument` 功能类似，但 Playwright 的实现更稳定。

---

## 无效反爬措施

| 措施 | 原因 |
|------|------|
| 仅修改 User-Agent | 反爬系统检测多个指纹，不止 UA |
| 使用 Crawlee 等高级框架 | 框架特征明显，更易被检测 |
| Docker 隔离 | 对 Cloudflare 无效，检测的是浏览器指纹而非 IP 环境 |

---

## 性能基准测试

测试目标：Discuss.com.hk（Cloudflare 保护站点）

| 方法 | 速度 | 反爬能力 | 成功率 |
|------|------|---------|--------|
| 直接请求 (fetch) | ⚡ 最快 | ❌ 无 | 0% |
| Playwright Simple | 🚀 快 (3-5s) | ⚠️ 低 | 20% |
| **Playwright Stealth** | ⏱️ 中 (5-20s) | ✅ 中 | **100%** ✅ |
| Puppeteer Stealth | ⏱️ 中 | ✅ 中高 | ~80% |
| Crawlee (deep-scraper) | 🐢 慢 | ❌ 被检测 | 0% |

**结论：纯 Playwright + 反检测注入是最佳方案。框架越重，越容易被识别。**

---

## Cloudflare 绕过策略

### 基本策略

1. 使用 `playwright-stealth.js`
2. `WAIT_TIME` 设为 10000-15000（挑战页需要时间）
3. 尝试 `HEADLESS=false`（有头模式有时通过率更高）
4. 使用移动端 UA

### 高级策略

1. **代理 IP 轮换** — 使用住宅代理池，避免单一 IP 被封
2. **Cookie 管理** — 维持 Cloudflare clearance cookie，复用 session
3. **验证码处理** — 集成 2captcha / Anti-Captcha API 自动解验证码
4. **请求间隔** — 多次请求之间加入随机间隔（3-10 秒）

### Cloudflare 挑战页特征

- 页面标题包含 "Just a moment" 或 "Checking your browser"
- 有 JavaScript 计算挑战
- 通常 5-10 秒后自动跳转

---

## 浏览器指纹伪装详解

### navigator.webdriver

最关键的反检测项。自动化浏览器默认 `navigator.webdriver === true`，设为 false 后基础检测会认为这是正常浏览器。

### navigator.plugins

正常浏览器有 plugins 数组，自动化浏览器通常为空。伪造 3-5 个 plugins 即可通过检测。

### navigator.languages

设置合理的语言列表，与 User-Agent 和 `Accept-Language` 头保持一致。

### window.chrome

Playwright/Puppeteer 控制的浏览器缺少 `window.chrome` 对象，这是已知检测点。伪造为包含 `runtime`、`loadTimes`、`csi`、`app` 的对象。

### WebGL 渲染器

WebGL 参数 `37445` (UNMASKED_VENDOR_WEBGL) 和 `37446` (UNMASKED_RENDERER_WEBGL) 用于识别 GPU。伪造为常见值（Intel）避免被标记为虚拟机或自动化环境。

### Permissions API

`navigator.permissions.query` 的行为在自动化浏览器中有差异：正常浏览器对 `notifications` 查询返回与 `Notification.permission` 一致的结果，而自动化浏览器可能返回不一致。需要修补此行为。
