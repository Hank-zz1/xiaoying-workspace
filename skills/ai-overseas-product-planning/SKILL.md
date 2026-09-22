---
name: AI海外产品企划全流程智能平台
description: AI驱动的海外产品企划全流程自动化技能。覆盖情报搜集、竞品分析、需求预测、企划文档生成、汇报PPT制作五大模块。当用户要求"准备海外产品企划"、"AI企划"、"海外竞品分析"、"企划报告"、"企划PPT"或类似需求时使用此技能。
---

# AI海外产品企划全流程智能平台

## 技能概述

本技能通过AI技术将海外产品企划全流程自动化，覆盖**情报搜集 → 竞品分析 → 需求预测 → 企划文档 → 汇报PPT**五大模块，实现企划周期从5-7天缩短至1-2天，综合效率提升约70%。

**适用场景：** 海外冰箱产品企划、竞品对标分析、市场需求调研、企划文档撰写、汇报材料制作

---

## 品类聚焦：海外冰箱

本技能默认聚焦**海外冰箱**品类，涵盖：
- **家用冰箱**（对开门、法式多门、十字门、嵌入式、法式底置冷冻等）
- **商用冰箱**（展示柜、后厨冷柜、饮料柜、医药冰箱等）
- **细分市场**（红酒柜、冰吧、车载冰箱等）

### 冰箱品类搜索词模板

1. **全球市场规模与趋势**
   ```
   搜索词：2025 2026 refrigerator market size trends global CAGR
   搜索词：global refrigerator industry analysis 2025 2026
   搜索词：智能冰箱 海外市场趋势 2025 2026
   ```

2. **各区域市场需求**
   ```
   搜索词：refrigerator market North America Europe Asia demand 2025
   搜索词：side-by-side refrigerator trends USA 2025
   搜索词：European refrigerator market energy efficiency 2025
   搜索词：Southeast Asia refrigerator demand growth 2025
   搜索词：Middle East refrigerator market high ambient 2025
   ```

3. **技术趋势与创新**
   ```
   搜索词：smart refrigerator AI technology 2025 IoT connected
   搜索词：refrigerator energy efficiency inverter compressor 2025
   搜索词：refrigerator eco-friendly refrigerant R600a R290 2025
   搜索词：嵌入式冰箱 趋势 2025
   搜索词：wine cooler refrigerator market 2025
   ```

4. **法规与认证**
   ```
   搜索词：refrigerator CE certification Energy Star compliance
   搜索词：EU refrigerator energy label 2025 regulation
   搜索词：refrigerator F-Gas R290 R600a regulation Europe
   搜索词：refrigerator MEPS standard North America 2025
   搜索词：SASO refrigerator certification Saudi Arabia
   ```

5. **竞品动态**
   ```
   搜索词：Samsung LG Bosch Whirlpool refrigerator 2025 new models
   搜索词：海尔 冰箱 海外 2025 新品
   搜索词：refrigerator price comparison USA Europe 2025
   搜索词：best refrigerator brands 2025 consumer report
   ```

### 冰箱关键竞品品牌

**全球品牌：**
- Samsung 三星（Family Hub智能冰箱、Bespoke系列）
- LG（InstaView、ThinQ智能冰箱）
- Bosch 博世（嵌入式、Serie 6/8系列）
- Whirlpool 惠而浦（北美市场主力）
- Electrolux 伊莱克斯（欧洲市场）
- Liebherr 利勃海尔（高端嵌入式）

**中国品牌出海：**
- Haier 海尔（法式对开门、嵌入式、Cafe系列）
- Hisense 海信（多门、对开门）
- Midea 美的（多门、法式）
- TCL（对开门、十字门）

**差异化品牌：**
- Sub-Zero（北美高端嵌入式）
- Thermador（北美高端）
- SMEG（欧洲复古设计）
- Godrej（印度市场）

---

## 工作流程

### 阶段一：AI海外情报搜集

使用 `bocha_ai_search` 和 `bocha_web_search` 并行搜索以下维度的信息：

1. **全球市场规模与趋势**
   ```
   搜索词：2025 2026 {品类} market size trends global CAGR
   搜索词：制冷设备市场环境分析 2025 2026
   ```

2. **各区域市场需求**
   ```
   搜索词：{品类} North America Europe Asia market demand 2025
   搜索词：{区域}制冷产品市场趋势 需求
   ```

3. **行业技术趋势**
   ```
   搜索词：{品类} AI technology application 2025 smart solutions
   搜索词：制冷技术 智能化 趋势 2025 2026
   ```

4. **法规与认证要求**
   ```
   搜索词：{品类} CE certification Energy Star F-Gas regulation compliance
   搜索词：制冷设备出口 法规标准 CE认证
   ```

5. **竞品动态**
   ```
   搜索词：Haier Midea Carrier Daikin Gree {品类} 2025 new products
   搜索词：{主要竞品品牌} {品类} 2025 新品 技术参数 价格
   ```

**输出：** 将搜索结果整理为结构化情报报告（JSON格式），包含：
- 全球市场规模与增长数据
- 行业核心趋势（通常5条）
- 各区域市场需求差异（北美/欧洲/东南亚/中东）
- 技术革新方向
- 海外法规与认证要求
- AI应用机会

### 阶段二：AI竞品智能对标

基于阶段一收集的竞品数据，生成结构化竞品对标表：

```python
# 输出JSON格式
{
  "rows": [
    {
      "brand": "品牌名",
      "product": "核心产品",
      "region": "目标区域",
      "key_feature": "核心功能/技术亮点",
      "refrigerant": "制冷剂类型",
      "energy_rating": "能效等级",
      "price_range": "价格区间",
      "certification": "认证信息",
      "innovation": "创新点"
    }
  ]
}
```

**关键竞品（制冷行业参考）：**
- 海尔 Haier（AI制冷机房、MRV多联机、热泵）
- 开利 Carrier（商用制冷、纯电冷机、Inverter技术）
- 大金 Daikin（MARUTTO云平台、HVAC管理）
- 格力 Gree（双热源热泵、G-AI2.0技术）
- 特灵 Trane（商用冷水机组）
- 比泽尔 Bitzer（CO₂跨临界压缩）
- GEA（氨/CO₂天然工质系统）
- 卡乐 Carel（智能控制器）

### 阶段三：AI需求预测分析

基于市场情报数据，输出需求预测分析报告：

1. **各区域市场规模预测**（增速、关键驱动力、产品偏好）
2. **全球技术趋势分析**（影响程度、时间线、详细解读）
3. **产品开发优先级建议**（P0立即启动 → P1近期 → P2中期 → P3长期）
4. **SWOT分析**（优势、挑战、机会）

**输出格式：** JSON结构化报告，包含区域预测、趋势分析、优先级建议。

### 阶段四：企划文档生成

使用 `transform_data` 工具配合 `python-docx` 生成Word企划文档：

```python
from docx import Document
import sys

doc = Document()
doc.add_heading('标题', level=0)
doc.add_heading('一、一级标题', level=1)
# ... 使用标准模板格式生成
doc.save(sys.argv[-1])
```

**企划文档标准结构：**
1. 作品概述（名称、类型、核心理念）
2. 痛点与提效对比（表格）
3. 方案架构（五大模块说明）
4. 市场洞察（规模、趋势、区域差异）
5. 竞品对标分析（表格）
6. 产品开发优先级建议（P0-P3）
7. 法规合规清单（表格）
8. SWOT分析
9. AI赋能效果（提效数据表格）
10. 总结与展望

### 阶段五：汇报PPT生成

使用 `transform_data` 工具配合 `python-pptx` 生成PPT：

```python
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)
# 使用标准配色：深蓝(DARK_BLUE)、青色(CYAN)、绿色(GREEN)、橙色(ORANGE)
# 生成10页标准幻灯片
prs.save(sys.argv[-1])
```

**PPT标准结构（10页）：**
1. 封面（深蓝背景，主标题+副标题）
2. 核心痛点与AI解决方案（Before/After对比卡片）
3. 方案架构（五大模块卡片）
4. AI情报搜集成果（关键数据+趋势）
5. 区域市场需求差异（2x2区域卡片）
6. 竞品智能对标（3x2品牌卡片）
7. 产品开发优先级建议（2x3产品卡片）
8. 法规合规清单（表格）
9. AI赋能提效成果（时间轴+汇总）
10. 总结与展望（双栏布局）

---

## 快速执行命令

### 完整流程执行

```python
# 1. 并行搜索5个维度
bocha_ai_search(query="{品类} 市场趋势 2025 2026")
bocha_ai_search(query="{品类} market size North America Europe Asia")
bocha_ai_search(query="{品类} AI technology application 2025")
bocha_ai_search(query="{品类} CE Energy Star F-Gas regulation")
bocha_ai_search(query="竞品品牌 {品类} 2025 新品")

# 2. 生成情报报告JSON → transform_data
# 3. 生成竞品对标表JSON → transform_data
# 4. 生成需求预测JSON → transform_data
# 5. 生成HTML看板 → transform_data
# 6. 生成Word文档 → transform_data (python-docx)
# 7. 生成PPT → transform_data (python-pptx)
```

### 依赖检查

```bash
# 检查Python环境
python --version  # 或 python3 / py

# 安装依赖
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
pip install python-docx python-pptx openpyxl Pillow lxml
```

---

## 配色方案（PPT参考）

| 颜色 | RGB值 | 用途 |
|------|-------|------|
| 深蓝 | (10, 22, 40) | 背景/标题 |
| 中蓝 | (30, 58, 95) | 辅助色 |
| 青色 | (0, 188, 212) | 强调色 |
| 绿色 | (46, 204, 113) | 正面数据 |
| 橙色 | (245, 166, 35) | 警告/关注 |
| 红色 | (229, 62, 62) | P0优先级/负面 |
| 紫色 | (155, 89, 182) | 补充色 |

---

## 行业知识库

### 海外法规关键时间点
- **F-Gas新规 (EU 2024/2174)**：2025年1月1日生效
- **ISO 18483:2025**：离心式制冷剂压缩机性能标准，2025年发布

### 关键市场数据
- 全球商用制冷市场：2024年约$385亿，2034年预计$616亿（CAGR 4.8%）
- 全球工业制冷市场：2023年¥147亿，2029年预计¥203亿（CAGR 5.4%）
- 欧洲热泵市场：CAGR超30%
- AI节能技术：可实现25-30%能效提升

### 区域市场优先级
| 区域 | 增速 | 优先级 | 关键需求 |
|------|------|--------|----------|
| 欧洲 | 5.0-6.5% | P0 | F-Gas合规、热泵、环保制冷剂 |
| 北美 | 4.5-5.5% | P0 | 超低温、ENERGY STAR、双热源 |
| 东南亚 | 6.0-8.0% | P1 | 性价比、高温适应、冷链 |
| 中东 | 4.0-5.5% | P2 | 大制冷量、抗腐蚀 |

---

## 交付物清单模板

每次执行本技能后，应生成以下交付物：

| 文件 | 格式 | 说明 |
|------|------|------|
| 企划文档 | .docx | 完整企划方案报告 |
| 汇报PPT | .pptx | 10页标准演示文稿 |
| 市场情报看板 | .html | 交互式数据看板 |
| 竞品对标表 | .json | 结构化竞品数据 |
| 需求预测报告 | .json | 区域预测与优先级建议 |
| 参赛报名摘要 | .md | 报名用信息汇总 |

---

## 注意事项

1. **安全合规**：全程使用内部AI工具，不使用外部大模型，符合企业信息安全要求
2. **数据来源**：通过搜索API采集公开市场数据，确保数据时效性
3. **格式规范**：Word文档使用底层自动格式注入，不要手动设置字体/字号/行距
4. **PPT配色**：保持深蓝+青色主题，避免纯文本幻灯片，每张幻灯片需有视觉元素
