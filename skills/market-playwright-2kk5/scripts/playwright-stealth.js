#!/usr/bin/env node
/**
 * Playwright Stealth Scraper
 *
 * 反爬绕过网页抓取脚本
 * - 隐藏 navigator.webdriver
 * - 注入真实设备 User-Agent
 * - 随机延迟模拟人类行为
 * - 截图与 HTML 保存
 *
 * Usage: node playwright-stealth.js 
 * Env:   HEADLESS, WAIT_TIME, USER_AGENT, SAVE_HTML, SCREENSHOT_PATH, HTML_PATH
 */

const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

// ─── 参数解析 ───
const url = process.argv[2];
if (!url) {
  console.error('Usage: node playwright-stealth.js ');
  process.exit(1);
}

const HEADLESS        = process.env.HEADLESS !== 'false';
const WAIT_TIME       = parseInt(process.env.WAIT_TIME || '8000', 10);
const SAVE_HTML       = process.env.SAVE_HTML === 'true';
const SCREENSHOT_PATH = process.env.SCREENSHOT_PATH || path.join(process.cwd(), 'screenshot.png');
const HTML_PATH       = process.env.HTML_PATH || path.join(process.cwd(), 'page.html');

// ─── 真实设备 UA 池 ───
const USER_AGENTS = [
  'Mozilla/5.0 (iPhone; CPU iPhone OS 17_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Mobile/15E148 Safari/604.1',
  'Mozilla/5.0 (Linux; Android 14; Pixel 8 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36',
  'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
];
const USER_AGENT = process.env.USER_AGENT || USER_AGENTS[Math.floor(Math.random() * USER_AGENTS.length)];

// ─── 工具函数 ───
const randomDelay = (min, max) => Math.floor(Math.random() * (max - min + 1)) + min;

(async () => {
  const startTime = Date.now();
  let browser;

  try {
    // 启动浏览器（禁用自动化控制特征）
    browser = await chromium.launch({
      headless: HEADLESS,
      args: [
        '--disable-blink-features=AutomationControlled',
        '--no-sandbox',
        '--disable-setuid-sandbox',
      ],
    });

    // 判断设备类型
    const isMobile = USER_AGENT.includes('iPhone') || USER_AGENT.includes('Android');

    // 创建浏览器上下文（模拟真实设备指纹）
    const context = await browser.newContext({
      userAgent: USER_AGENT,
      viewport: isMobile
        ? { width: 390, height: 844 }
        : { width: 1920, height: 1080 },
      deviceScaleFactor: isMobile ? 3 : 1,
      isMobile: isMobile,
      hasTouch: isMobile,
      locale: 'zh-CN',
      timezoneId: 'Asia/Shanghai',
      extraHTTPHeaders: {
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
      },
    });

    // ─── 反检测注入（在页面 JS 执行前运行）───
    await context.addInitScript(() => {
      // 1. 隐藏 navigator.webdriver（最关键）
      Object.defineProperty(navigator, 'webdriver', { get: () => false });

      // 2. 伪造 plugins（空数组是自动化特征）
      Object.defineProperty(navigator, 'plugins', { get: () => [1, 2, 3, 4, 5] });

      // 3. 伪造 languages
      Object.defineProperty(navigator, 'languages', { get: () => ['zh-CN', 'zh', 'en'] });

      // 4. 伪造 window.chrome（Playwright 缺失此对象）
      window.chrome = { runtime: {}, loadTimes: () => {}, csi: () => {}, app: {} };

      // 5. 修补 Permissions API
      const originalQuery = window.navigator.permissions.query;
      window.navigator.permissions.query = (parameters) =>
        parameters.name === 'notifications'
          ? Promise.resolve({ state: Notification.permission })
          : originalQuery(parameters);

      // 6. 伪造 WebGL 渲染器信息
      const getParameter = WebGLRenderingContext.prototype.getParameter;
      WebGLRenderingContext.prototype.getParameter = function (parameter) {
        if (parameter === 37445) return 'Intel Inc.';
        if (parameter === 37446) return 'Intel Iris OpenGL Engine';
        return getParameter.call(this, parameter);
      };
    });

    const page = await context.newPage();

    // ─── 访问目标 ───
    console.error(`[*] Target: ${url}`);
    console.error(`[*] UA: ${USER_AGENT.substring(0, 60)}...`);
    console.error(`[*] Headless: ${HEADLESS} | Mobile: ${isMobile}`);

    const response = await page.goto(url, {
      waitUntil: 'networkidle',
      timeout: 30000,
    });

    // 随机延迟（模拟人类阅读）
    await page.waitForTimeout(randomDelay(1000, 3000));

    // 额外等待（用于 Cloudflare 挑战页）
    if (WAIT_TIME > 3000) {
      await page.waitForTimeout(WAIT_TIME - 3000);
    }

    // 随机滚动（模拟人类浏览）
    const scrollDist = randomDelay(100, 500);
    await page.evaluate((dist) => window.scrollBy(0, dist), scrollDist);
    await page.waitForTimeout(randomDelay(500, 1500));

    // ─── 提取页面内容 ───
    const title = await page.title();
    const content = await page.evaluate(() => {
      document.querySelectorAll('script, style, noscript').forEach((el) => el.remove());
      return document.body ? document.body.innerText : '';
    });

    const status   = response ? response.status() : null;
    const elapsed  = ((Date.now() - startTime) / 1000).toFixed(2);

    // 截图
    await page.screenshot({ path: SCREENSHOT_PATH, fullPage: false });
    console.error(`[*] Screenshot: ${SCREENSHOT_PATH}`);

    // 保存 HTML（可选）
    if (SAVE_HTML) {
      const html = await page.content();
      fs.writeFileSync(HTML_PATH, html, 'utf-8');
      console.error(`[*] HTML saved: ${HTML_PATH}`);
    }

    // ─── 输出 JSON 结果 ───
    const result = {
      url,
      title,
      content: content.substring(0, 50000),
      status,
      elapsedSeconds: elapsed,
      screenshot: SCREENSHOT_PATH,
      userAgent: USER_AGENT,
      timestamp: new Date().toISOString(),
    };

    console.log(JSON.stringify(result, null, 2));
    console.error(`[*] Done in ${elapsed}s | Status: ${status}`);

  } catch (err) {
    console.error(`[!] Error: ${err.message}`);
    console.log(JSON.stringify({
      url,
      error: err.message,
      elapsedSeconds: ((Date.now() - startTime) / 1000).toFixed(2),
      timestamp: new Date().toISOString(),
    }, null, 2));
    process.exitCode = 1;
  } finally {
    if (browser) await browser.close();
  }
})();
