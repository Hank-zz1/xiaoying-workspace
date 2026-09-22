# 海外冰箱竞品雷达 v2.0 — 多源架构方案

## 一、核心变化

| 旧版 (v1) | 新版 (v2) |
|-----------|-----------|
| 单一来源：官网抓取 | 三层来源：官网 + 电商 + 搜索 |
| 官网不可抓取 → 无数据 | 官网不可抓取 → 电商兜底 → 搜索兜底 |
| 仅输出型号 | 输出型号 + 价格 + 评论 + 新闻 |
| 统一 mode=scrape/search | 每品牌 3 个并行任务 |

## 二、多源架构

```
每个品牌 → 并行执行 3 条路径：
  ├── 路径1: 官网抓取 (scrape) — 已验证可抓取的 URL
  ├── 路径2: 电商搜索 (ecommerce) — Amazon 各站点
  └── 路径3: 新闻搜索 (news) — 博查中文 + Firecrawl 英文
```

## 三、数据源矩阵（按区域 × 品牌）

区域 → 品牌 → 官网URL(可抓取) / 电商URL / 新闻搜索词

### 澳洲 (Australia)
| 品牌 | 官网URL | 电商URL | 新闻搜索词 |
|------|---------|---------|-----------|
| 海信 | https://hisense.com.au/appliances/fridges-freezers/all | https://www.amazon.com.au/s?k=Hisense+refrigerator | Hisense Australia refrigerator 2026 new |
| 美的 | https://www.midea.com/au/refrigerator | https://www.amazon.com.au/s?k=Midea+refrigerator | Midea Australia refrigerator 2026 new |
| 三星 | (官网JS渲染) | https://www.amazon.com.au/s?k=Samsung+refrigerator | Samsung Australia refrigerator 2026 |
| LG | (官网反爬) | https://www.amazon.com.au/s?k=LG+refrigerator | LG Australia refrigerator 2026 new |
| 西屋 | https://www.westinghouse.com.au/fridges-and-freezers | https://www.amazon.com.au/s?k=Westinghouse+refrigerator | Westinghouse Australia refrigerator 2026 new |

### 欧洲 (Europe)
| 品牌 | 官网URL | 电商URL | 新闻搜索词 |
|------|---------|---------|-----------|
| 美的 | https://www.midea.com/de/kuehlen-gefrieren | https://www.amazon.de/s?k=Midea+K%C3%BChlschrank | Midea Europe Kühlschrank 2026 Neuheit |
| 海信 | (官网仅企业站) | https://www.amazon.de/s?k=Hisense+K%C3%BChlschrank | 海信 欧洲 冰箱 2026 新品 |
| 三星 | (官网JS渲染) | https://www.amazon.de/s?k=Samsung+K%C3%BChlschrank | Samsung Europe Kühlschrank 2026 |
| LG | (官网反爬) | https://www.amazon.de/s?k=LG+K%C3%BChlschrank | LG Europe Kühlschrank 2026 Neuheit |
| 松下 | (官网反爬) | https://www.amazon.de/s?k=Panasonic+K%C3%BChlschrank | Panasonic Europe refrigerator 2026 |
| 日立 | (官网404) | https://www.amazon.de/s?k=Hitachi+K%C3%BChlschrank | Hitachi Europe Kühlschrank 2026 |

### 美洲 (Americas)
| 品牌 | 官网URL | 电商URL | 新闻搜索词 |
|------|---------|---------|-----------|
| 海信 | https://www.hisense-usa.com/refrigerators | https://www.amazon.com/s?k=Hisense+refrigerator | Hisense USA refrigerator 2026 new |
| 美的 | (官网反爬) | https://www.amazon.com/s?k=Midea+refrigerator | Midea USA refrigerator 2026 new |
| 三星 | (官网JS渲染) | https://www.amazon.com/s?k=Samsung+refrigerator | Samsung USA refrigerator 2026 new |
| LG | (官网反爬) | https://www.amazon.com/s?k=LG+refrigerator | LG USA refrigerator 2026 new |

### 独联体 (CIS)
| 品牌 | 官网URL | 电商URL | 新闻搜索词 |
|------|---------|---------|-----------|
| 海信 | (无独立官网) | 暂无 | 海信 俄罗斯 冰箱 2026 新品 |
| 美的 | (无独立官网) | 暂无 | 美的 俄罗斯 冰箱 2026 新品 |
| 三星 | (官网JS渲染) | 暂无 | Samsung Russia refrigerator 2026 |
| LG | (官网反爬) | 暂无 | LG Russia refrigerator 2026 |

### 东南亚 (Southeast Asia)
| 品牌 | 官网URL | 电商URL | 新闻搜索词 |
|------|---------|---------|-----------|
| 海信 | (无独立官网) | 暂无 | 海信 东南亚 冰箱 2026 新品 |
| 美的 | (无独立官网) | 暂无 | 美的 东南亚 冰箱 2026 新品 |
| 三星 | (官网JS渲染) | 暂无 | Samsung Southeast Asia refrigerator 2026 |
| LG | (官网反爬) | 暂无 | LG Southeast Asia refrigerator 2026 |
| 松下 | (官网反爬) | 暂无 | Panasonic Asia refrigerator 2026 |

### 南亚 (South Asia)
| 品牌 | 官网URL | 电商URL | 新闻搜索词 |
|------|---------|---------|-----------|
| 海信 | (无独立官网) | 暂无 | 海信 印度 冰箱 2026 新品 |
| 美的 | (无独立官网) | 暂无 | 美的 印度 冰箱 2026 新品 |
| 三星 | (官网JS渲染) | 暂无 | Samsung India refrigerator 2026 |
| LG | (官网反爬) | 暂无 | LG India refrigerator 2026 |
| 海尔 | (无独立官网) | 暂无 | Haier India refrigerator 2026 |

### 中东非 (Middle East/Africa)
| 品牌 | 官网URL | 电商URL | 新闻搜索词 |
|------|---------|---------|-----------|
| 海信 | (无独立官网) | 暂无 | 海信 中东 冰箱 2026 新品 |
| 美的 | (无独立官网) | 暂无 | 美的 中东 冰箱 2026 新品 |
| 三星 | (官网JS渲染) | 暂无 | Samsung Middle East refrigerator 2026 |
| LG | (官网反爬) | 暂无 | LG Middle East refrigerator 2026 |

### 东亚 (East Asia)
| 品牌 | 官网URL | 电商URL | 新闻搜索词 |
|------|---------|---------|-----------|
| 海信 | (无独立官网) | 暂无 | 海信 日韩 冰箱 2026 新品 |
| 美的 | (无独立官网) | 暂无 | 美的 日韩 冰箱 2026 新品 |
| 三星 | (官网JS渲染) | 暂无 | Samsung Korea refrigerator 2026 |
| LG | (官网反爬) | 暂无 | LG Korea refrigerator 2026 |
| 松下 | (官网反爬) | 暂无 | Panasonic Japan refrigerator 2026 |
| 日立 | (官网404) | 暂无 | Hitachi Japan refrigerator 2026 |

## 四、数据源可用性实测总结

| 数据源类型 | 可抓取 | 不可抓取（原因） |
|-----------|--------|-----------------|
| Amazon 各站点 | ✅ 产品+价格+评论 | — |
| 美的官网 (DE) | ✅ 品类页 | 产品列表页 JS 渲染 |
| 海信 AU 官网 | ✅ | EU 仅企业站 |
| 三星官网 | — | 全站 JS 渲染 |
| LG 官网 | — | 全站反爬 |
| 松下官网 | — | 反爬 |
| 日立官网 | — | 404 |
| 西屋 AU 官网 | ✅ | — |
| MediaMarkt | — | 反爬 |
| Euronics | — | 反爬 |
| 博查中文搜索 | ✅ | 英文搜索效果差 |
| Firecrawl Search | ✅ | 部分区域无结果 |

## 五、每品牌搜索策略

每个品牌执行 3 轮搜索：
1. **scrape** — 官网 URL（如可抓取），提取产品型号和规格
2. **ecommerce** — Amazon 站点搜索，提取产品名/价格/评论数/上架时间
3. **news** — 博查中文搜索词 + Firecrawl 英文搜索词，提取新品发布新闻

每轮结果在代码01中合并，最终输出格式：
```json
{
  "brand": "三星",
  "region": "欧洲",
  "sources": {
    "official": { "url": "...", "models": [...], "status": "success|failed" },
    "ecommerce": { "url": "...", "products": [...], "status": "success|failed" },
    "news": { "articles": [...], "status": "success|failed" }
  }
}
```