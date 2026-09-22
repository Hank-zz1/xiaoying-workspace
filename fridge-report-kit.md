# 澳新冰箱新品监控 · 统一抓取模式（2026-08-27 起生效）

> 本文件是**模式契约**。所有 AU / NZ 冰箱监控任务按下述方式执行；不涉及品牌差异的内容直接引用本文件。

## 0. 环境背景

- **禁用 `firecrawl_scrape` 和 `browser_tool` 抓取官网**。统一使用工作区根目录的 `fridge_stealth_scrape.py`（隐身 Playwright 抓取）。
- 固定 Python：`C:/Users/26011970/AppData/Local/Programs/IncaierAgents/resources/vendor/python/python.exe`（已内置 playwright，无需安装任何东西）。
- 执行方式：任务先在工作区根目录 `cd C:/Users/26011970/.incaier-agent/workspaces/my-workspace`，再运行
  `"<固定Python路径>" fridge_stealth_scrape.py "<URL>" [选项]`。
- 输出为**单行 JSON**：`jsonld_items`（产品名+URL）、`hrefs`（过滤后的链接）、`models`（型号正则命中）、`title`、`content_length`、`nav_error`（有值即抓取失败）。

## 1. 各站点模式速查表

| 站点 | URL | 选项 | 要点 |
|------|-----|------|------|
| 海信 AU | `https://hisense.com.au/appliances/fridges-freezers/all` | `--mode=hrefs --href-kw=product` | 官网全量；型号前缀 HR（如 HRCD615TBWV） |
| 海信 NZ | `https://hisense.co.nz/appliances/fridge/` | 同上 | **旧 URL `/kitchen-appliances/fridges/` 为 404**；型号前缀 HR/HRTF |
| 美的 AU | `https://www.binglee.com.au/products/midea` | `--mode=hrefs --href-kw=midea` | 官网 JS 重渲染，用 Bing Lee 替代；型号 MDRT/MDRS/MDRF/BCD/MDRB |
| 三星 AU | `https://www.samsung.com/au/refrigerators/all-refrigerators/` | `--mode=jsonld` | **产品数据在 JSON-LD**（解决了旧版"不可抓取"问题）；型号 RF/RB/RZ/RI |
| 三星 NZ | `https://www.samsung.com/nz/refrigerators/all-refrigerators/` | `--mode=jsonld` | 同上 |
| LG AU | `https://www.lg.com/au/fridges/` | `--headed --wait=8` | Akamai 强反爬，**必须 --headed** |
| LG NZ | `https://www.lg.com/nz/fridges/` | `--headed --wait=8` | 同上；被限流时等 20-60 秒重跑（脚本自带退避） |
| 西屋 AU | `https://www.westinghouse.com.au/fridges-and-freezers/fridges/` | `--mode=hrefs --href-kw=westinghouse` | 型号 WHE/WQE/WSE/WBE/WTM 等 |

## 2. 通用纪律

1. **永远带回归验证**：`nav_error` 非空 → 该品牌按老模式（搜索兜底）处理一次，并在报告里标注「隐身抓取失败 xx，已回退搜索」。
2. **截图留证**：对疑似新品 / 状态变化的单品页面加 `--shot`，保存 `fridge_scrape.png`。
3. **LG 被限流时**：AKAMAI 是**整机 IP 封禁**（连普通 HTTP 请求都会超时/reset，非浏览器指纹问题），应对方法只有「等待 + 重试」或换时段。不要为了提高成功率疯狂重试。
4. **禁止爬单品的非必要想象**：以页面实际返回的型号/名称为准，不允许在报告里编造型号。

## 3. 基线文件约定（重要）

- **唯一基线文件**：`C:/Users/26011970/.incaier-agent/workspaces/my-workspace/data/au-fridge-baseline-2026-06-15.md`
  - 之前散落在各会话 data/ 里的副本全部忽略、不要再引用。
  - 该文件含 **AUS 市场和 NZ 市场两大节**；本次已按新抓取数据重建 NZ 节。
- **每次监控**：读基线 → 抓取 → 对比 → 有变化才推送（每日汇总任务除外：无变化也发简短卡片）→ 有变化则更新基线。
- **模型/型号字段**：用表格行「| 型号 | 名称 | ... |」，型号只记录官网页面 URL slug 中出现的正式型号码，无法确认型号时写「待确认」。

## 4. 已知陷阱

- 美的官网 `www.midea.com/au/refrigerator` 的 Top Mount 是 JS 动态渲染，抓不到全量 → 用 Bing Lee 页面替代（链接见上表）。
- Hisense AU 官方统计 53 个产品但页面分页；`--scroll=4` 可触发更多懒加载。
- Samsung 不要用 `--mode=hrefs`（链接里没有型号），必须用 `--mode=jsonld`。
- LG NZ 抓取失败时 `final_url` 会是 `chrome-error://chromewebdata/`，这是浏览器错误页，不算抓取成功。
- 飞书推送卡片格式沿用工区既有约定：蓝色模板、标题「🔔 <市场>冰箱新品巡检 - <日期>」、底部「由 Incaier Agent 自动巡检」。