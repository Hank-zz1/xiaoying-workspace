#!/usr/bin/env node
/**
 * Playwright Simple Scraper
 *
 * 简单动态网页抓取（无反爬措施）
 * - 等待 JS 渲染
 * - 提取页面文本
 * - JSON 输出
 *
 * Usage: node playwright-simple.js 
 * Env:   WAIT_TIME, HEADLESS
 */

const { chromium } = require('playwright');

const url = process.argv[2];
if (!url) {
  console.error('Usage: node playwright-simple.js ');
  process.exit(1);
}

const WAIT_TIME = parseInt(process.env.WAIT_TIME || '5000', 10);
const HEADLESS  = process.env.HEADLESS !== 'false';

(async () => {
  const startTime = Date.now();
  let browser;

  try {
    browser = await chromium.launch({ headless: HEADLESS });
    const page = await browser.newPage();

    console.error(`[*] Target: ${url}`);

    const response = await page.goto(url, {
      waitUntil: 'networkidle',
      timeout: 30000,
    });

    // 额外等待渲染
    if (WAIT_TIME > 0) {
      await page.waitForTimeout(WAIT_TIME);
    }

    const title = await page.title();
    const content = await page.evaluate(() => {
      document.querySelectorAll('script, style, noscript').forEach((el) => el.remove());
      return document.body ? document.body.innerText : '';
    });

    const status  = response ? response.status() : null;
    const elapsed = ((Date.now() - startTime) / 1000).toFixed(2);

    const result = {
      url,
      title,
      content: content.substring(0, 50000),
      status,
      elapsedSeconds: elapsed,
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
