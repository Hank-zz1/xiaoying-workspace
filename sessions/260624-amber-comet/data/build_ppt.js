const pptxgen = require("pptxgenjs");
const path = require("path");

const palette = {
  primary: "1B3A4B",
  secondary: "E86A4D",
  accent: "F5B041",
  light: "F8F6F0",
  dark: "1E1E1E",
  ice: "CFE0E8",
  grey: "7F8C8D",
  white: "FFFFFF",
  green: "27AE60",
  red: "E74C3C",
};

const FONT = "Microsoft YaHei";
const PAGE_W = 13.33;
const PAGE_H = 7.5;

async function main() {
  const pptx = new pptxgen();
  pptx.layout = "LAYOUT_WIDE";
  pptx.author = "情绪冰仓团队";
  pptx.title = "情绪冰仓·一杯饮尽松弛感";

  // ============ Slide 1: Cover ============
  let s = pptx.addSlide();
  s.background = { color: palette.primary };
  s.addShape("rect", { x: 0, y: 0, w: 13.33, h: 0.08, fill: { color: palette.accent } });
  s.addShape("rect", { x: 0, y: 7.42, w: 13.33, h: 0.08, fill: { color: palette.accent } });
  s.addShape("rect", { x: 0.8, y: 1.5, w: 0.06, h: 2.8, fill: { color: palette.secondary } });
  s.addText("情绪冰仓", { x: 1.2, y: 1.5, w: 10, h: 1.4, fontSize: 54, fontFace: FONT, color: palette.white, bold: true });
  s.addText("一杯饮尽松弛感", { x: 1.2, y: 2.9, w: 10, h: 0.8, fontSize: 28, fontFace: FONT, color: palette.accent, bold: false });
  s.addText("黑马大赛商业路演方案", { x: 1.2, y: 3.8, w: 10, h: 0.6, fontSize: 16, fontFace: FONT, color: palette.ice });
  s.addText("2026年7月  |  海尔制冷·情绪冰仓项目组", { x: 1.2, y: 5.5, w: 10, h: 0.5, fontSize: 13, fontFace: FONT, color: palette.grey });

  // ============ Slide 2: TOC ============
  s = pptx.addSlide();
  s.background = { color: palette.light };
  s.addShape("rect", { x: 0, y: 0, w: 13.33, h: 0.06, fill: { color: palette.primary } });
  s.addText("目录", { x: 0.8, y: 0.4, w: 5, h: 0.7, fontSize: 30, fontFace: FONT, color: palette.primary, bold: true });
  s.addShape("rect", { x: 0.8, y: 1.15, w: 1.5, h: 0.04, fill: { color: palette.secondary } });

  const tocItems = [
    { num: "01", title: "项目背景与市场机会", desc: "年轻人冰饮需求与情绪消费趋势" },
    { num: "02", title: "用户洞察与场景分析", desc: "目标用户画像与核心消费场景" },
    { num: "03", title: "竞品分析与市场缺口", desc: "现有冰吧产品的不足与我们的机会" },
    { num: "04", title: "产品设计与创新亮点", desc: "四大核心功能 + 智能化增强层" },
    { num: "05", title: "技术架构与实现路径", desc: "七大技术系统与可行性" },
    { num: "06", title: "商业模式与营销策略", desc: "盈利模式、渠道策略与品牌传播" },
    { num: "07", title: "财务分析", desc: "成本结构、收入预测与融资方案" },
    { num: "08", title: "风险评估与退出机制", desc: "风险识别与应对策略" },
    { num: "09", title: "团队架构与推进计划", desc: "核心团队与关键里程碑" },
  ];

  const startY = 1.5;
  const itemH = 0.58;
  tocItems.forEach((item, i) => {
    const y = startY + i * itemH;
    const col = i < 5 ? 0.8 : 7.0;
    const j = i < 5 ? i : i - 5;
    const yy = startY + j * itemH;
    s.addShape("roundRect", { x: col, y: yy, w: 0.55, h: 0.42, fill: { color: palette.primary }, rectRound: 0.08 });
    s.addText(item.num, { x: col, y: yy, w: 0.55, h: 0.42, fontSize: 13, fontFace: FONT, color: palette.white, bold: true, align: "center", valign: "middle" });
    s.addText(item.title, { x: col + 0.7, y: yy - 0.02, w: 4.5, h: 0.28, fontSize: 13, fontFace: FONT, color: palette.dark, bold: true });
    s.addText(item.desc, { x: col + 0.7, y: yy + 0.24, w: 4.5, h: 0.22, fontSize: 10, fontFace: FONT, color: palette.grey });
  });

  // ============ Slide 3: Project Background ============
  s = pptx.addSlide();
  s.background = { color: palette.white };
  s.addShape("rect", { x: 0, y: 0, w: 13.33, h: 1.2, fill: { color: palette.primary } });
  s.addText("01  项目背景与市场机会", { x: 0.8, y: 0.2, w: 10, h: 0.8, fontSize: 24, fontFace: FONT, color: palette.white, bold: true });

  // Three big number cards
  const cards = [
    { num: "4.2亿", label: "中国Z世代人口", sub: "核心目标消费群体" },
    { num: "68%", label: "愿意为情绪价值付费", sub: "悦己消费成为主流趋势" },
    { num: "35%", label: "冰吧品类年增速", sub: "远高于传统冰箱增速" },
  ];
  cards.forEach((c, i) => {
    const cx = 0.8 + i * 4.1;
    s.addShape("roundRect", { x: cx, y: 1.5, w: 3.8, h: 2.0, fill: { color: palette.light }, rectRound: 0.12 });
    s.addText(c.num, { x: cx, y: 1.6, w: 3.8, h: 0.8, fontSize: 32, fontFace: FONT, color: palette.secondary, bold: true, align: "center" });
    s.addText(c.label, { x: cx, y: 2.3, w: 3.8, h: 0.45, fontSize: 14, fontFace: FONT, color: palette.dark, bold: true, align: "center" });
    s.addText(c.sub, { x: cx, y: 2.7, w: 3.8, h: 0.4, fontSize: 11, fontFace: FONT, color: palette.grey, align: "center" });
  });

  s.addText("三大趋势驱动情绪冰仓需求", { x: 0.8, y: 3.8, w: 12, h: 0.5, fontSize: 16, fontFace: FONT, color: palette.primary, bold: true });
  const trends = [
    "生活方式升级：年轻人冷饮需求从解渴上升为生活仪式，需要场景依赖的精细化、高品质冰饮存储",
    "情绪消费崛起：悦己消费成为主流，"松弛感、解压、氛围感、仪式感"成为核心购买驱动力",
    "冰吧品类蓝海：冰吧并非概念空白，是一个已有成交但仍缺少面向年轻情绪场景产品的细分市场",
  ];
  trends.forEach((t, i) => {
    s.addShape("ellipse", { x: 0.8, y: 4.45 + i * 0.65, w: 0.18, h: 0.18, fill: { color: palette.secondary } });
    s.addText(t, { x: 1.15, y: 4.35 + i * 0.65, w: 11.5, h: 0.5, fontSize: 12, fontFace: FONT, color: palette.dark });
  });

  s.addText("数据来源：即时零售冰品酒饮消费洞察报告2025、2026中国食品饮料十大趋势、小红书平台冰吧相关笔记分析", { x: 0.8, y: 6.6, w: 12, h: 0.4, fontSize: 9, fontFace: FONT, color: palette.grey, italic: true });

  // ============ Slide 4: User Insights ============
  s = pptx.addSlide();
  s.background = { color: palette.white };
  s.addShape("rect", { x: 0, y: 0, w: 13.33, h: 1.2, fill: { color: palette.primary } });
  s.addText("02  用户洞察与场景分析", { x: 0.8, y: 0.2, w: 10, h: 0.8, fontSize: 24, fontFace: FONT, color: palette.white, bold: true });

  s.addText("核心用户画像", { x: 0.8, y: 1.5, w: 6, h: 0.5, fontSize: 16, fontFace: FONT, color: palette.primary, bold: true });
  const personas = [
    { title: "独居/租房青年", desc: "追求生活品质，小空间也能精致生活，冰吧是"家的仪式感"入口" },
    { title: "社交型小两口", desc: "经常在家招待朋友，酒饮/调酒/冷饮需求高频，冰吧是社交场景核心设备" },
    { title: "运动/养生青年", desc: "运动后补水补能、熬夜后补给，对功能饮料、电解质水有精准温控需求" },
    { title: "沉浸式娱乐爱好者", desc: "看球、电竞、追剧等场景，需要快速取用冰饮，氛围感烘托观影体验" },
  ];
  personas.forEach((p, i) => {
    const py = 2.1 + i * 0.85;
    s.addShape("roundRect", { x: 0.8, y: py, w: 5.5, h: 0.7, fill: { color: palette.light }, rectRound: 0.08 });
    s.addShape("roundRect", { x: 0.8, y: py, w: 0.06, h: 0.7, fill: { color: palette.secondary }, rectRound: 0.03 });
    s.addText(p.title, { x: 1.1, y: py + 0.05, w: 5, h: 0.3, fontSize: 12, fontFace: FONT, color: palette.primary, bold: true });
    s.addText(p.desc, { x: 1.1, y: py + 0.35, w: 5, h: 0.3, fontSize: 10, fontFace: FONT, color: palette.grey });
  });

  s.addText("核心消费场景（小红书高频词）", { x: 7.2, y: 1.5, w: 5.5, h: 0.5, fontSize: 16, fontFace: FONT, color: palette.primary, bold: true });
  const scenarios = [
    { word: "夏天", freq: "最高频" },
    { word: "追剧", freq: "高频" },
    { word: "运动", freq: "高频" },
    { word: "宅家", freq: "高频" },
    { word: "客厅", freq: "高频" },
    { word: "聚会", freq: "中频" },
    { word: "电竞", freq: "中频" },
    { word: "微醺", freq: "中频" },
  ];
  scenarios.forEach((sc, i) => {
    const col = i % 2;
    const row = Math.floor(i / 2);
    const sx = 7.2 + col * 2.8;
    const sy = 2.1 + row * 0.85;
    s.addShape("roundRect", { x: sx, y: sy, w: 2.5, h: 0.7, fill: { color: sc.freq === "最高频" ? palette.secondary : palette.light }, rectRound: 0.08 });
    s.addText(sc.word, { x: sx, y: sy + 0.05, w: 2.5, h: 0.35, fontSize: 14, fontFace: FONT, color: sc.freq === "最高频" ? palette.white : palette.dark, bold: true, align: "center" });
    s.addText(sc.freq, { x: sx, y: sy + 0.38, w: 2.5, h: 0.25, fontSize: 10, fontFace: FONT, color: sc.freq === "最高频" ? palette.white : palette.grey, align: "center" });
  });

  s.addText("场景洞察：冰饮需求集中在降温放松、追剧/赛事陪伴、运动后恢复、朋友小聚这几类时刻。用户需要快速拿取、清楚分类、视觉展示和即时可喝状态。", { x: 7.2, y: 5.6, w: 5.5, h: 1.0, fontSize: 11, fontFace: FONT, color: palette.dark });

  // ============ Slide 5: Competitive Analysis ============
  s = pptx.addSlide();
  s.background = { color: palette.white };
  s.addShape("rect", { x: 0, y: 0, w: 13.33, h: 1.2, fill: { color: palette.primary } });
  s.addText("03  竞品分析与市场缺口", { x: 0.8, y: 0.2, w: 10, h: 0.8, fontSize: 24, fontFace: FONT, color: palette.white, bold: true });

  // Comparison table
  const tableData = [
    [{ text: "维度", options: { bold: true, color: palette.white, fontSize: 11 } },
     { text: "传统冰吧", options: { bold: true, color: palette.white, fontSize: 11 } },
     { text: "卡萨帝冰吧", options: { bold: true, color: palette.white, fontSize: 11 } },
     { text: "哈士奇冰吧", options: { bold: true, color: palette.white, fontSize: 11 } },
     { text: "情绪冰仓（我们）", options: { bold: true, color: palette.white, fontSize: 11 } }],
    [{ text: "温控精度", options: { fontSize: 10 } }, { text: "粗糙 ±3°C", options: { fontSize: 10 } }, { text: "电子 ±1°C", options: { fontSize: 10 } }, { text: "电子 ±1°C", options: { fontSize: 10 } }, { text: "多温区 ±0.5°C", options: { fontSize: 10, color: palette.secondary, bold: true } }],
    [{ text: "氛围灯光", options: { fontSize: 10 } }, { text: "无/单色", options: { fontSize: 10 } }, { text: "单色", options: { fontSize: 10 } }, { text: "无", options: { fontSize: 10 } }, { text: "RGB情绪模式+音乐律动", options: { fontSize: 10, color: palette.secondary, bold: true } }],
    [{ text: "可视化分区", options: { fontSize: 10 } }, { text: "无", options: { fontSize: 10 } }, { text: "基础", options: { fontSize: 10 } }, { text: "透明窗", options: { fontSize: 10 } }, { text: "色温分区+透视窗+标签", options: { fontSize: 10, color: palette.secondary, bold: true } }],
    [{ text: "电控调光玻璃", options: { fontSize: 10 } }, { text: "无", options: { fontSize: 10 } }, { text: "无", options: { fontSize: 10 } }, { text: "无", options: { fontSize: 10 } }, { text: "APP一键雾化", options: { fontSize: 10, color: palette.secondary, bold: true } }],
    [{ text: "智能库存识别", options: { fontSize: 10 } }, { text: "无", options: { fontSize: 10 } }, { text: "无", options: { fontSize: 10 } }, { text: "无", options: { fontSize: 10 } }, { text: "AI酒标识别+到期提醒", options: { fontSize: 10, color: palette.secondary, bold: true } }],
    [{ text: "家居融合设计", options: { fontSize: 10 } }, { text: "一般", options: { fontSize: 10 } }, { text: "较好", options: { fontSize: 10 } }, { text: "复古风格", options: { fontSize: 10 } }, { text: "可换面板+嵌入+黄金比例", options: { fontSize: 10, color: palette.secondary, bold: true } }],
    [{ text: "静音水平", options: { fontSize: 10 } }, { text: "40dB+", options: { fontSize: 10 } }, { text: "38dB", options: { fontSize: 10 } }, { text: "38dB", options: { fontSize: 10 } }, { text: "≤28dB 夜间≤22dB", options: { fontSize: 10, color: palette.secondary, bold: true } }],
    [{ text: "情绪交互", options: { fontSize: 10 } }, { text: "无", options: { fontSize: 10 } }, { text: "无", options: { fontSize: 10 } }, { text: "无", options: { fontSize: 10 } }, { text: "触控屏+语音+情绪模式", options: { fontSize: 10, color: palette.secondary, bold: true } }],
  ];

  const tblRows = tableData.map((row, ri) => {
    const bgColor = ri === 0 ? palette.primary : (ri % 2 === 0 ? palette.light : palette.white);
    return row.map((cell) => ({ ...cell, options: { ...cell.options, fill: { color: bgColor }, fontFace: FONT, align: "center", valign: "middle" } }));
  });

  s.addTable(tblRows, { x: 0.8, y: 1.5, w: 11.73, colW: [2.0, 1.8, 2.0, 2.0, 3.93], rowH: [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5], border: { type: "solid", pt: 0.5, color: palette.ice } });

  s.addText("市场缺口：现有冰吧产品普遍缺乏"情绪价值"设计，没有针对年轻人情绪场景的专属产品。我们的机会在于将冰吧从"功能设备"升级为"情绪家具"。", { x: 0.8, y: 6.3, w: 11.73, h: 0.7, fontSize: 12, fontFace: FONT, color: palette.primary, bold: true });

  // ============ Slide 6: Product Design ============
  s = pptx.addSlide();
  s.background = { color: palette.white };
  s.addShape("rect", { x: 0, y: 0, w: 13.33, h: 1.2, fill: { color: palette.primary } });
  s.addText("04  产品设计与创新亮点", { x: 0.8, y: 0.2, w: 10, h: 0.8, fontSize: 24, fontFace: FONT, color: palette.white, bold: true });

  const features = [
    { icon: "01", title: "可视化分区", desc: "三色温LED分区照明\n透明玻璃层架+45°透视抽屉\n磁吸标签+阶梯式门搁架\n3秒定位，减少翻找40%", color: palette.secondary },
    { icon: "02", title: "低噪夜间体验", desc: "磁悬浮变频压缩机 ≤28dB\n夜间模式 ≤22dB\n软启动/软停机零冲击音\n底部2700K暖光氛围灯", color: palette.accent },
    { icon: "03", title: "DIY小料/冰杯适配", desc: "模块化托盘+酱料格\n304不锈钢冰杯速冷抽屉\n风味冰块DIY水盒\n磁性侧壁+快拆门搁架", color: palette.green },
    { icon: "04", title: "家居化外观", desc: "4种面板可选（木纹/岩板）\nR8圆角+无拉手极简\n3:2黄金比例+嵌入式踢脚线\n顶部置物台面承重30kg", color: palette.primary },
  ];

  features.forEach((f, i) => {
    const fx = 0.8 + i * 3.1;
    s.addShape("roundRect", { x: fx, y: 1.5, w: 2.8, h: 3.0, fill: { color: palette.light }, rectRound: 0.12 });
    s.addShape("roundRect", { x: fx + 0.25, y: 1.7, w: 0.6, h: 0.6, fill: { color: f.color }, rectRound: 0.1 });
    s.addText(f.icon, { x: fx + 0.25, y: 1.7, w: 0.6, h: 0.6, fontSize: 16, fontFace: FONT, color: palette.white, bold: true, align: "center", valign: "middle" });
    s.addText(f.title, { x: fx + 1.0, y: 1.75, w: 1.6, h: 0.5, fontSize: 15, fontFace: FONT, color: palette.dark, bold: true });
    s.addText(f.desc, { x: fx + 0.25, y: 2.5, w: 2.3, h: 1.8, fontSize: 10, fontFace: FONT, color: palette.grey, lineSpacingMultiple: 1.5 });
  });

  s.addText("智能化增强层（不喧宾夺主）", { x: 0.8, y: 4.8, w: 12, h: 0.5, fontSize: 16, fontFace: FONT, color: palette.primary, bold: true });
  const smartFeats = [
    "极简触控屏：门板嵌入，低调不突兀，支持情绪模式一键切换",
    "语音交互：顶部微光指示灯，轻声提醒（门未关/长开门预警），不打扰",
    "电控调光玻璃：APP一键切换透明/雾化，保护藏酒隐私+展示切换",
    "AI库存识别：柜内摄像头+云端酒标比对，到期提醒+智能推荐",
  ];
  smartFeats.forEach((sf, i) => {
    const sx = 0.8 + (i % 2) * 6.1;
    const sy = 5.4 + Math.floor(i / 2) * 0.55;
    s.addShape("ellipse", { x: sx, y: sy + 0.12, w: 0.14, h: 0.14, fill: { color: palette.accent } });
    s.addText(sf, { x: sx + 0.3, y: sy, w: 5.5, h: 0.45, fontSize: 11, fontFace: FONT, color: palette.dark });
  });

  // ============ Slide 7: Scenario-Mode Mapping ============
  s = pptx.addSlide();
  s.background = { color: palette.white };
  s.addShape("rect", { x: 0, y: 0, w: 13.33, h: 1.2, fill: { color: palette.primary } });
  s.addText("05  场景-功能-情绪模式映射", { x: 0.8, y: 0.2, w: 10, h: 0.8, fontSize: 24, fontFace: FONT, color: palette.white, bold: true });

  const modes = [
    { name: "微醺模式", scene: "独处/约会小酌", temp: "红葡12°C/白葡8°C", light: "暖琥珀色呼吸灯", color: palette.secondary },
    { name: "冰爽模式", scene: "运动后/夏日降温", temp: "饮料3°C快速制冷", light: "冰蓝色流动光效", color: "2980B9" },
    { name: "养生模式", scene: "熬夜补给/日常调理", temp: "功能饮5°C/面膜2°C", light: "暖白柔和常亮光", color: palette.green },
    { name: "派对模式", scene: "朋友聚会/看球电竞", temp: "啤酒4°C/冰杯-18°C", light: "RGB音乐律动灯光", color: "8E44AD" },
  ];

  modes.forEach((m, i) => {
    const mx = 0.8 + i * 3.1;
    s.addShape("roundRect", { x: mx, y: 1.5, w: 2.8, h: 3.8, fill: { color: palette.light }, rectRound: 0.12 });
    s.addShape("roundRect", { x: mx, y: 1.5, w: 2.8, h: 0.7, fill: { color: m.color }, rectRound: 0.12 });
    s.addText(m.name, { x: mx, y: 1.5, w: 2.8, h: 0.7, fontSize: 16, fontFace: FONT, color: palette.white, bold: true, align: "center", valign: "middle" });
    const details = [
      "场景：" + m.scene,
      "温控：" + m.temp,
      "灯光：" + m.light,
    ];
    details.forEach((d, j) => {
      s.addText(d, { x: mx + 0.2, y: 2.45 + j * 0.55, w: 2.4, h: 0.45, fontSize: 10, fontFace: FONT, color: palette.dark });
    });
  });

  s.addText("一键切换：用户可通过门板触控屏或手机APP一键切换情绪模式，灯光、温度、氛围同步匹配，实现"一杯饮尽松弛感"的完整体验。", { x: 0.8, y: 5.6, w: 11.73, h: 0.6, fontSize: 12, fontFace: FONT, color: palette.primary, bold: true });

  // Scenario-feature mapping table
  s.addText("场景-功能-分类映射", { x: 0.8, y: 6.2, w: 6, h: 0.4, fontSize: 14, fontFace: FONT, color: palette.primary, bold: true });
  const mappingData = [
    [{ text: "场景需求", options: { bold: true, color: palette.white, fontSize: 10, fill: { color: palette.primary }, fontFace: FONT } },
     { text: "功能分类", options: { bold: true, color: palette.white, fontSize: 10, fill: { color: palette.primary }, fontFace: FONT } },
     { text: "核心实现", options: { bold: true, color: palette.white, fontSize: 10, fill: { color: palette.primary }, fontFace: FONT } }],
    [{ text: "最佳口感", options: { fontSize: 10, fontFace: FONT } }, { text: "分温精储", options: { fontSize: 10, fontFace: FONT } }, { text: "多温区独立风道+风门精确控制", options: { fontSize: 10, fontFace: FONT } }],
    [{ text: "氛围感/出片", options: { fontSize: 10, fontFace: FONT } }, { text: "空间氛围", options: { fontSize: 10, fontFace: FONT } }, { text: "RGB氛围灯+透明视窗+电控调光", options: { fontSize: 10, fontFace: FONT } }],
    [{ text: "情绪满足", options: { fontSize: 10, fontFace: FONT } }, { text: "情绪模式", options: { fontSize: 10, fontFace: FONT } }, { text: "一键切换微醺/冰爽/养生/派对模式", options: { fontSize: 10, fontFace: FONT } }],
    [{ text: "仪式感/便利", options: { fontSize: 10, fontFace: FONT } }, { text: "高频顺手", options: { fontSize: 10, fontFace: FONT } }, { text: "模块化托盘+快拆搁架+可视化分区", options: { fontSize: 10, fontFace: FONT } }],
  ];
  s.addTable(mappingData, { x: 0.8, y: 6.55, w: 11.73, colW: [2.5, 2.5, 6.73], rowH: [0.3, 0.28, 0.28, 0.28, 0.28], border: { type: "solid", pt: 0.5, color: palette.ice } });

  // ============ Slide 8: Technical Architecture ============
  s = pptx.addSlide();
  s.background = { color: palette.white };
  s.addShape("rect", { x: 0, y: 0, w: 13.33, h: 1.2, fill: { color: palette.primary } });
  s.addText("05  技术架构与实现路径", { x: 0.8, y: 0.2, w: 10, h: 0.8, fontSize: 24, fontFace: FONT, color: palette.white, bold: true });

  const techs = [
    { num: "1", title: "智能氛围灯光系统", desc: "RGBW LED灯珠+独立MCU驱动，APP调色盘+音乐律动+情绪模式联动" },
    { num: "2", title: "电控调光玻璃", desc: "三层夹胶玻璃+调光膜，断电自动雾化，Wi-Fi远程遥控切换" },
    { num: "3", title: "AI智能库存识别", desc: "低功耗广角摄像头+云端酒标比对，到期提醒+智能推荐+APP可视化" },
    { num: "4", title: "精细化多温区", desc: "多风道独立送风+步进电机风门，冷藏/微冻/暖藏三区独立控温" },
    { num: "5", title: "静音与减震系统", desc: "变频压缩机+磁悬浮轴承+多重减震阻尼，橡木酒架吸振" },
    { num: "6", title: "家居融合模块化", desc: "底部散热+标准模数搁架+可拆卸磁吸面板，自由嵌入+多材质可选" },
    { num: "7", title: "UVC除菌净化", desc: "离子杀菌模块+抗菌门条+干湿分离+HCS生态膜隔离" },
  ];

  techs.forEach((t, i) => {
    const col = i % 2;
    const row = Math.floor(i / 2);
    const tx = 0.8 + col * 6.1;
    const ty = 1.5 + row * 0.78;
    s.addShape("roundRect", { x: tx, y: ty, w: 0.45, h: 0.45, fill: { color: palette.primary }, rectRound: 0.08 });
    s.addText(t.num, { x: tx, y: ty, w: 0.45, h: 0.45, fontSize: 14, fontFace: FONT, color: palette.white, bold: true, align: "center", valign: "middle" });
    s.addText(t.title, { x: tx + 0.6, y: ty - 0.02, w: 5, h: 0.3, fontSize: 12, fontFace: FONT, color: palette.primary, bold: true });
    s.addText(t.desc, { x: tx + 0.6, y: ty + 0.28, w: 5, h: 0.35, fontSize: 10, fontFace: FONT, color: palette.grey });
  });

  s.addText("技术可行性：以上七项技术均基于成熟方案，核心硬件（LED驱动、调光膜、变频压缩机、NTC温控）供应链完善，软件端（APP、云端识别）可复用现有IoT平台能力。", { x: 0.8, y: 6.5, w: 11.73, h: 0.6, fontSize: 12, fontFace: FONT, color: palette.primary, bold: true });

  // ============ Slide 9: Business Model ============
  s = pptx.addSlide();
  s.background = { color: palette.white };
  s.addShape("rect", { x: 0, y: 0, w: 13.33, h: 1.2, fill: { color: palette.primary } });
  s.addText("06  商业模式与营销策略", { x: 0.8, y: 0.2, w: 10, h: 0.8, fontSize: 24, fontFace: FONT, color: palette.white, bold: true });

  // Pricing strategy
  s.addText("产品定价策略", { x: 0.8, y: 1.5, w: 5.5, h: 0.5, fontSize: 16, fontFace: FONT, color: palette.primary, bold: true });
  const pricing = [
    { tier: "基础款", price: "1,999-2,499", features: "可视化分区+分温精储+静音" },
    { tier: "进阶款", price: "2,999-3,499", features: "+RGB氛围灯+情绪模式+电控玻璃" },
    { tier: "旗舰款", price: "3,999-4,999", features: "+AI库存识别+语音+可换面板" },
  ];
  pricing.forEach((p, i) => {
    const py = 2.1 + i * 0.75;
    s.addShape("roundRect", { x: 0.8, y: py, w: 5.5, h: 0.6, fill: { color: i === 2 ? palette.primary : palette.light }, rectRound: 0.08 });
    s.addText(p.tier, { x: 1.0, y: py + 0.05, w: 1.2, h: 0.5, fontSize: 13, fontFace: FONT, color: i === 2 ? palette.white : palette.primary, bold: true });
    s.addText(p.price, { x: 2.2, y: py + 0.05, w: 1.5, h: 0.5, fontSize: 13, fontFace: FONT, color: palette.secondary, bold: true });
    s.addText(p.features, { x: 3.8, y: py + 0.05, w: 2.3, h: 0.5, fontSize: 10, fontFace: FONT, color: i === 2 ? palette.ice : palette.grey });
  });

  // Revenue model
  s.addText("盈利模式", { x: 7.2, y: 1.5, w: 5.5, h: 0.5, fontSize: 16, fontFace: FONT, color: palette.primary, bold: true });
  const revenue = [
    "硬件销售：三级定价覆盖不同消费力，预计毛利率35-45%",
    "配件耗材：DIY模块托盘、风味冰格、替换面板等复购收入",
    "平台分成：饮品推荐与即时零售平台合作导流分成",
    "会员订阅：AI库存管理+智能推荐高级功能订阅（9.9元/月）",
  ];
  revenue.forEach((r, i) => {
    s.addShape("ellipse", { x: 7.2, y: 2.2 + i * 0.55, w: 0.14, h: 0.14, fill: { color: palette.secondary } });
    s.addText(r, { x: 7.5, y: 2.1 + i * 0.55, w: 5.2, h: 0.45, fontSize: 10, fontFace: FONT, color: palette.dark });
  });

  // Marketing channels
  s.addText("营销与渠道策略", { x: 0.8, y: 4.4, w: 12, h: 0.5, fontSize: 16, fontFace: FONT, color: palette.primary, bold: true });
  const channels = [
    { title: "线上种草", desc: "小红书/抖音 KOL种草，京东/天猫旗舰店首发", color: palette.secondary },
    { title: "线下体验", desc: "海尔智慧家庭体验店+城市快闪店", color: palette.accent },
    { title: "跨界联名", desc: "精酿啤酒品牌/即饮茶品牌联名定制款", color: palette.green },
    { title: "社群运营", desc: "私域社群+饮品DIY内容+用户UGC激励", color: "8E44AD" },
  ];
  channels.forEach((ch, i) => {
    const cx = 0.8 + i * 3.1;
    s.addShape("roundRect", { x: cx, y: 5.0, w: 2.8, h: 1.6, fill: { color: palette.light }, rectRound: 0.12 });
    s.addShape("roundRect", { x: cx + 0.9, y: 5.15, w: 1.0, h: 0.05, fill: { color: ch.color }, rectRound: 0.02 });
    s.addText(ch.title, { x: cx, y: 5.35, w: 2.8, h: 0.4, fontSize: 14, fontFace: FONT, color: palette.dark, bold: true, align: "center" });
    s.addText(ch.desc, { x: cx + 0.2, y: 5.8, w: 2.4, h: 0.6, fontSize: 10, fontFace: FONT, color: palette.grey, align: "center" });
  });

  // ============ Slide 10: Financial Analysis ============
  s = pptx.addSlide();
  s.background = { color: palette.white };
  s.addShape("rect", { x: 0, y: 0, w: 13.33, h: 1.2, fill: { color: palette.primary } });
  s.addText("07  财务分析", { x: 0.8, y: 0.2, w: 10, h: 0.8, fontSize: 24, fontFace: FONT, color: palette.white, bold: true });

  // Investment
  s.addText("首年度投入预算", { x: 0.8, y: 1.5, w: 5.5, h: 0.5, fontSize: 16, fontFace: FONT, color: palette.primary, bold: true });
  const costItems = [
    { item: "研发费用（模具+样机+认证）", amount: "200万" },
    { item: "模具开发（3款面板+结构件）", amount: "150万" },
    { item: "首批量产（1000台）", amount: "300万" },
    { item: "营销推广（线上+线下）", amount: "100万" },
    { item: "团队人力（10人×12月）", amount: "200万" },
    { item: "合计", amount: "950万", isTotal: true },
  ];
  costItems.forEach((c, i) => {
    const cy = 2.1 + i * 0.45;
    const bg = c.isTotal ? palette.primary : palette.light;
    s.addShape("roundRect", { x: 0.8, y: cy, w: 5.5, h: 0.38, fill: { color: bg }, rectRound: 0.06 });
    s.addText(c.item, { x: 1.0, y: cy + 0.02, w: 3.8, h: 0.34, fontSize: 11, fontFace: FONT, color: c.isTotal ? palette.white : palette.dark, bold: c.isTotal });
    s.addText(c.amount, { x: 4.8, y: cy + 0.02, w: 1.3, h: 0.34, fontSize: 12, fontFace: FONT, color: c.isTotal ? palette.accent : palette.secondary, bold: true, align: "right" });
  });

  // Revenue forecast
  s.addText("三年收入预测", { x: 7.2, y: 1.5, w: 5.5, h: 0.5, fontSize: 16, fontFace: FONT, color: palette.primary, bold: true });
  const forecastData = [
    [{ text: "", options: { bold: true, color: palette.white, fontSize: 10, fill: { color: palette.primary }, fontFace: FONT } },
     { text: "第1年", options: { bold: true, color: palette.white, fontSize: 10, fill: { color: palette.primary }, fontFace: FONT } },
     { text: "第2年", options: { bold: true, color: palette.white, fontSize: 10, fill: { color: palette.primary }, fontFace: FONT } },
     { text: "第3年", options: { bold: true, color: palette.white, fontSize: 10, fill: { color: palette.primary }, fontFace: FONT } }],
    [{ text: "销量（台）", options: { fontSize: 10, fontFace: FONT } }, { text: "3,000", options: { fontSize: 10, fontFace: FONT } }, { text: "12,000", options: { fontSize: 10, fontFace: FONT } }, { text: "30,000", options: { fontSize: 10, fontFace: FONT } }],
    [{ text: "硬件收入", options: { fontSize: 10, fontFace: FONT } }, { text: "900万", options: { fontSize: 10, fontFace: FONT } }, { text: "3,600万", options: { fontSize: 10, fontFace: FONT } }, { text: "9,000万", options: { fontSize: 10, fontFace: FONT } }],
    [{ text: "配件+服务收入", options: { fontSize: 10, fontFace: FONT } }, { text: "50万", options: { fontSize: 10, fontFace: FONT } }, { text: "300万", options: { fontSize: 10, fontFace: FONT } }, { text: "1,200万", options: { fontSize: 10, fontFace: FONT } }],
    [{ text: "总营收", options: { fontSize: 10, fontFace: FONT, bold: true } }, { text: "950万", options: { fontSize: 10, fontFace: FONT, bold: true } }, { text: "3,900万", options: { fontSize: 10, fontFace: FONT, bold: true } }, { text: "1.02亿", options: { fontSize: 10, fontFace: FONT, bold: true, color: palette.secondary } }],
  ];
  s.addTable(forecastData, { x: 7.2, y: 2.1, w: 5.5, colW: [1.5, 1.33, 1.33, 1.34], rowH: [0.35, 0.35, 0.35, 0.35, 0.35], border: { type: "solid", pt: 0.5, color: palette.ice } });

  s.addText("融资计划", { x: 7.2, y: 4.0, w: 5.5, h: 0.5, fontSize: 16, fontFace: FONT, color: palette.primary, bold: true });
  const fundItems = [
    "天使轮融资：500万元，出让10%股权",
    "资金用途：产品研发40% + 模具30% + 营销20% + 运营10%",
    "预计第2年实现盈亏平衡，第3年净利润率达15%",
    "退出路径：3-5年内被海尔集团收购或独立IPO",
  ];
  fundItems.forEach((f, i) => {
    s.addShape("ellipse", { x: 7.2, y: 4.65 + i * 0.5, w: 0.14, h: 0.14, fill: { color: palette.accent } });
    s.addText(f, { x: 7.5, y: 4.55 + i * 0.5, w: 5.2, h: 0.45, fontSize: 10, fontFace: FONT, color: palette.dark });
  });

  // ============ Slide 11: Risk Assessment ============
  s = pptx.addSlide();
  s.background = { color: palette.white };
  s.addShape("rect", { x: 0, y: 0, w: 13.33, h: 1.2, fill: { color: palette.primary } });
  s.addText("08  风险评估与应对策略", { x: 0.8, y: 0.2, w: 10, h: 0.8, fontSize: 24, fontFace: FONT, color: palette.white, bold: true });

  const risks = [
    { risk: "市场需求不及预期", level: "中", impact: "中", strategy: "首批1000台小批量试产，通过预售验证需求；保留快速迭代能力" },
    { risk: "竞品快速跟进", level: "高", impact: "中", strategy: "依托海尔品牌+渠道壁垒，6个月窗口期建立用户心智；持续迭代情绪模式" },
    { risk: "供应链成本上涨", level: "中", impact: "中", strategy: "核心零部件多供应商备份；模块化设计降低定制件比例" },
    { risk: "技术实现难度", level: "低", impact: "低", strategy: "七项技术均为成熟方案，无卡脖子环节；分阶段发布，降低技术风险" },
    { risk: "品牌认知度不足", level: "中", impact: "高", strategy: "依托海尔母品牌背书，小红书/抖音内容种草建立"情绪冰仓"独立IP" },
    { risk: "渠道拓展困难", level: "低", impact: "中", strategy: "复用海尔现有渠道体系；同时布局线上DTC模式降低渠道依赖" },
  ];

  const riskHeaders = [
    { text: "风险因素", options: { bold: true, color: palette.white, fontSize: 10, fill: { color: palette.primary }, fontFace: FONT, align: "center" } },
    { text: "等级", options: { bold: true, color: palette.white, fontSize: 10, fill: { color: palette.primary }, fontFace: FONT, align: "center" } },
    { text: "影响", options: { bold: true, color: palette.white, fontSize: 10, fill: { color: palette.primary }, fontFace: FONT, align: "center" } },
    { text: "应对策略", options: { bold: true, color: palette.white, fontSize: 10, fill: { color: palette.primary }, fontFace: FONT, align: "center" } },
  ];

  const riskRows = risks.map((r, i) => {
    const bg = i % 2 === 0 ? palette.light : palette.white;
    const levelColor = r.level === "高" ? palette.red : (r.level === "中" ? palette.accent : palette.green);
    return [
      { text: r.risk, options: { fontSize: 10, fontFace: FONT, fill: { color: bg }, align: "left" } },
      { text: r.level, options: { fontSize: 10, fontFace: FONT, fill: { color: bg }, color: levelColor, bold: true, align: "center" } },
      { text: r.impact, options: { fontSize: 10, fontFace: FONT, fill: { color: bg }, align: "center" } },
      { text: r.strategy, options: { fontSize: 9, fontFace: FONT, fill: { color: bg }, align: "left" } },
    ];
  });

  s.addTable([riskHeaders, ...riskRows], { x: 0.8, y: 1.5, w: 11.73, colW: [2.5, 0.8, 0.8, 7.63], rowH: [0.4, 0.65, 0.65, 0.65, 0.65, 0.65, 0.65], border: { type: "solid", pt: 0.5, color: palette.ice } });

  // ============ Slide 12: Team & Timeline ============
  s = pptx.addSlide();
  s.background = { color: palette.white };
  s.addShape("rect", { x: 0, y: 0, w: 13.33, h: 1.2, fill: { color: palette.primary } });
  s.addText("09  团队架构与推进计划", { x: 0.8, y: 0.2, w: 10, h: 0.8, fontSize: 24, fontFace: FONT, color: palette.white, bold: true });

  // Team
  s.addText("核心团队", { x: 0.8, y: 1.5, w: 5.5, h: 0.5, fontSize: 16, fontFace: FONT, color: palette.primary, bold: true });
  const team = [
    { name: "任泓博", role: "产品经理", dept: "制冷海外市场产品" },
    { name: "刘子涵", role: "产品企划", dept: "制冷海外产品企划" },
    { name: "臧炳松", role: "竞品分析", dept: "GMTP" },
    { name: "安文滨", role: "机构工程师", dept: "制冷机构" },
    { name: "王洪博", role: "结构工程师", dept: "制冷结构" },
    { name: "王志康", role: "结构工程师", dept: "制冷结构" },
    { name: "李兆木", role: "暖通工程师", dept: "制冷暖通" },
    { name: "鹿宝祥", role: "暖通工程师", dept: "制冷暖通" },
    { name: "赵姝钧", role: "财务分析", dept: "财务" },
  ];
  team.forEach((m, i) => {
    const col = i % 3;
    const row = Math.floor(i / 3);
    const tx = 0.8 + col * 1.9;
    const ty = 2.1 + row * 0.65;
    s.addShape("roundRect", { x: tx, y: ty, w: 1.7, h: 0.5, fill: { color: palette.light }, rectRound: 0.06 });
    s.addText(m.name + "  " + m.role, { x: tx, y: ty + 0.02, w: 1.7, h: 0.28, fontSize: 9, fontFace: FONT, color: palette.primary, bold: true, align: "center" });
    s.addText(m.dept, { x: tx, y: ty + 0.28, w: 1.7, h: 0.2, fontSize: 8, fontFace: FONT, color: palette.grey, align: "center" });
  });

  // Timeline
  s.addText("关键里程碑", { x: 7.2, y: 1.5, w: 5.5, h: 0.5, fontSize: 16, fontFace: FONT, color: palette.primary, bold: true });
  const milestones = [
    { date: "7/13", event: "入职报到" },
    { date: "7/16", event: "黑马大赛初赛", highlight: true },
    { date: "7/20", event: "黑马大赛决赛", highlight: true },
    { date: "8-9月", event: "产品详细设计+样机开发" },
    { date: "10-11月", event: "模具开发+小批量试产" },
    { date: "12月", event: "首批1000台预售上线" },
    { date: "2027 Q1", event: "正式量产+全渠道发售" },
    { date: "2027 Q2", event: "目标：月销1000台" },
  ];
  milestones.forEach((m, i) => {
    const my = 2.1 + i * 0.55;
    const dotColor = m.highlight ? palette.secondary : palette.primary;
    s.addShape("ellipse", { x: 7.2, y: my + 0.1, w: 0.16, h: 0.16, fill: { color: dotColor } });
    if (i < milestones.length - 1) {
      s.addShape("rect", { x: 7.27, y: my + 0.26, w: 0.02, h: 0.29, fill: { color: palette.ice } });
    }
    s.addText(m.date, { x: 7.5, y: my, w: 1.3, h: 0.35, fontSize: 11, fontFace: FONT, color: dotColor, bold: true });
    s.addText(m.event, { x: 8.8, y: my, w: 4, h: 0.35, fontSize: 11, fontFace: FONT, color: palette.dark });
  });

  // ============ Slide 13: Thank You ============
  s = pptx.addSlide();
  s.background = { color: palette.primary };
  s.addShape("rect", { x: 0, y: 0, w: 13.33, h: 0.08, fill: { color: palette.accent } });
  s.addShape("rect", { x: 0, y: 7.42, w: 13.33, h: 0.08, fill: { color: palette.accent } });
  s.addText("谢谢", { x: 0, y: 2.0, w: 13.33, h: 1.5, fontSize: 60, fontFace: FONT, color: palette.white, bold: true, align: "center" });
  s.addText("情绪冰仓 · 一杯饮尽松弛感", { x: 0, y: 3.5, w: 13.33, h: 0.8, fontSize: 24, fontFace: FONT, color: palette.accent, align: "center" });
  s.addShape("rect", { x: 5.5, y: 4.5, w: 2.33, h: 0.04, fill: { color: palette.secondary } });
  s.addText("海尔制冷 · 情绪冰仓项目组  |  2026年7月", { x: 0, y: 5.0, w: 13.33, h: 0.5, fontSize: 13, fontFace: FONT, color: palette.ice, align: "center" });
  s.addText("联系方式：renhongbo@haier.com", { x: 0, y: 5.5, w: 13.33, h: 0.5, fontSize: 12, fontFace: FONT, color: palette.grey, align: "center" });

  // Save
  const outputPath = path.join(__dirname, "情绪冰仓_黑马大赛路演PPT.pptx");
  await pptx.writeFile({ fileName: outputPath });
  console.log("PPT saved to: " + outputPath);
}

main().catch(err => { console.error(err); process.exit(1); });