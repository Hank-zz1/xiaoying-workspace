# 澳洲冰箱品牌新品监控 - 基线数据
# 创建日期: 2026-06-15 15:00 GMT+8
# 更新日期: 2026-06-15 17:00 GMT+8 (最终版)

## 1. 海信 Hisense ✅ 直接抓取
- **监控URL**: https://hisense.com.au/appliances/fridges-freezers/all?sortCode=newestArrival-desc&currentPage=0
- **方法**: firecrawl_scrape markdown 格式，提取第一个产品
- **第一个产品**: HRFD537SW | 544L PureFlex French Door Fridge Stainless Steel | French Door | $1,499
- **标签**: Sleek Water Dispenser, Durable Inverter, Large Capacity, ConnectLife Enabled, Premium Flatdoor Design
- **2026 筛选备用**: https://hisense.com.au/appliances/fridges-freezers/all?sortCode=newestArrival-desc&currentPage=0&tvReleaseYear=2026
- **判断逻辑**: 第一个产品型号变化 = 有新品

## 2. 美的 Midea ✅ 直接抓取
- **监控URL**: https://www.midea.com/au/refrigerator
- **方法**: firecrawl_scrape markdown 格式，提取第一个产品
- **第一个产品**: MERS791MYEDXAP | Midea 592L Side by Side Fridge Stainless | Side by Side | 592L
- **Coming Soon 产品**: MDRS925FIM45AP | Midea Space Master 700L Side by Side Fridge (需关注是否变为可购买)
- **判断逻辑**: 第一个产品型号变化 = 有新品；或 Coming Soon 产品消失/变为可购买

## 3. 三星 Samsung ✅ JSON 提取（主页）
- **监控URL**: https://www.samsung.com/au/refrigerators/
- **方法**: firecrawl_scrape json 格式 + jsonOptions.prompt，提取带 "New" badge 的产品
- **已知带 New 标签产品**:
  - SRT3300B (RT32K503JB1/SA) | 326L Top Mount Refrigerator | **New**
  - SRF5300SD (RF44A5202SL/SA) | 495L French Door Refrigerator | **New** (New Slim Fit Range)
- **判断逻辑**: "New" 标签产品列表变化（新增/减少/替换）= 有新品

## 4. LG ⚠️ 搜索监控（官网反爬）
- **监控URL**: https://www.lg.com/au/fridge-freezers/all-fridge-freezers/
- **方法**: bocha_web_search + bocha_ai_search 搜索 "LG Australia new fridge 2026"
- **已知最新型号**:
  - GF-V700BSLC | 642L French Door Fridge with InstaView | $4,799
  - GF-L570MBNL | 506L Slim French Door Fridge | Ice & Water
- **数据采集问题**: 官网有反爬保护 (document_antibot)，所有抓取方式均失败
- **判断逻辑**: 搜索到新 LG 冰箱型号（GF-/GS- 前缀）且不在已知列表中 = 有新品

## 5. 西屋 Westinghouse ✅ JSON 提取
- **监控URL**: https://www.westinghouse.com.au/fridges-and-freezers
- **方法**: firecrawl_extract json 格式，提取全部产品列表
- **当前 Featured Products 列表**:
  - WHE6874SA | 609L French door fridge - Stainless steel | **DISCONTINUED**
  - WHE5204SC | 491L French door fridge - Stainless steel
  - WBE4504SC | 425L bottom freezer fridge - Stainless steel
  - WBE5300BC | 496L bottom freezer fridge - Dark stainless steel
  - WQE6000SB | 541L quad door fridge - Stainless steel
- **判断逻辑**: Featured Products 列表变化（新增/移除/状态变化）= 有新品