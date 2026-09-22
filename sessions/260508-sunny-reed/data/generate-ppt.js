const pptxgen = require("pptxgenjs");

async function main() {
  const pptx = new pptxgen();
  pptx.defineLayout({ name: "LAYOUT_16x9", width: 13.33, height: 7.5 });
  pptx.layout = "LAYOUT_16x9";

  const palette = {
    primary: "1E2761",
    secondary: "CADCFC",
    accent: "FFFFFF",
    dark: "0D1117",
    light: "F6F8FA",
    gold: "D4AF37",
    green: "2E7D32",
    orange: "E65100",
    gray: "6C757D",
  };

  const FONT = "Microsoft YaHei";

  // ============ SLIDE 1: 封面 ============
  let slide = pptx.addSlide();
  slide.background = { color: palette.primary };
  // 顶部装饰线
  slide.addShape("rect", { x: 0, y: 0, w: 13.33, h: 0.06, fill: { color: palette.gold } });
  // 左侧装饰竖线
  slide.addShape("rect", { x: 0.8, y: 1.8, w: 0.06, h: 3.2, fill: { color: palette.gold } });
  // 主标题
  slide.addText(`海尔产品研发流程`, {
    x: 1.2, y: 1.8, w: 10, h: 1.0,
    fontSize: 42, fontFace: FONT, color: palette.accent, bold: true,
  });
  // 副标题
  slide.addText(`企划与研发职责分工`, {
    x: 1.2, y: 2.7, w: 10, h: 0.7,
    fontSize: 28, fontFace: FONT, color: palette.secondary, bold: true,
  });
  // 分隔线
  slide.addShape("rect", { x: 1.2, y: 3.5, w: 2.5, h: 0.04, fill: { color: palette.gold } });
  // 描述
  slide.addText(`P0-P6 全流程阶段 · 六大环节 · 清晰职责边界`, {
    x: 1.2, y: 3.8, w: 10, h: 0.5,
    fontSize: 16, fontFace: FONT, color: palette.secondary,
  });
  // 底部信息
  slide.addText(`2026年5月`, {
    x: 1.2, y: 5.5, w: 5, h: 0.4,
    fontSize: 14, fontFace: FONT, color: palette.secondary,
  });
  // 底部装饰线
  slide.addShape("rect", { x: 0, y: 7.44, w: 13.33, h: 0.06, fill: { color: palette.gold } });

  // ============ SLIDE 2: 目录 ============
  slide = pptx.addSlide();
  slide.background = { color: palette.light };
  // 顶部装饰条
  slide.addShape("rect", { x: 0, y: 0, w: 13.33, h: 1.2, fill: { color: palette.primary } });
  slide.addText(`目录`, {
    x: 0.8, y: 0.3, w: 5, h: 0.6,
    fontSize: 32, fontFace: FONT, color: palette.accent, bold: true,
  });

  const tocItems = [
    { num: "01", title: "流程总览", desc: "P0-P6 六阶段全景图" },
    { num: "02", title: "P0 概念与定义", desc: "企划主导 — 市场调研、立项论证" },
    { num: "03", title: "P1 调研与设计", desc: "企划+研发协作 — 规格制定与工程准备" },
    { num: "04", title: "P2 开发与设计", desc: "研发主导 — 详细设计、模具制作" },
    { num: "05", title: "P3 推敲验证", desc: "研发主导 — 测试验证、认证闭环" },
    { num: "06", title: "P4 交付", desc: "研发+企划 — 量产保障、市场推介" },
    { num: "07", title: "P5-P6 运营与退市", desc: "成熟运营、产品退市" },
    { num: "08", title: "职责汇总", desc: "企划 vs 研发 全景对比" },
  ];

  tocItems.forEach((item, i) => {
    const y = 1.6 + i * 0.7;
    // 编号圆形
    slide.addShape("ellipse", { x: 0.8, y: y + 0.05, w: 0.45, h: 0.45, fill: { color: palette.primary } });
    slide.addText(item.num, {
      x: 0.8, y: y + 0.05, w: 0.45, h: 0.45,
      fontSize: 14, fontFace: FONT, color: palette.accent, bold: true, align: "center", valign: "middle",
    });
    // 标题
    slide.addText(item.title, {
      x: 1.5, y: y - 0.02, w: 4, h: 0.3,
      fontSize: 16, fontFace: FONT, color: palette.dark, bold: true,
    });
    // 描述
    slide.addText(item.desc, {
      x: 1.5, y: y + 0.28, w: 8, h: 0.25,
      fontSize: 12, fontFace: FONT, color: palette.gray,
    });
    // 底部细线
    if (i < tocItems.length - 1) {
      slide.addShape("rect", { x: 1.5, y: y + 0.6, w: 10.5, h: 0.01, fill: { color: palette.secondary, transparency: 50 } });
    }
  });

  // ============ SLIDE 3: 流程总览 ============
  slide = pptx.addSlide();
  slide.background = { color: palette.light };
  slide.addShape("rect", { x: 0, y: 0, w: 13.33, h: 1.1, fill: { color: palette.primary } });
  slide.addText(`流程总览：P0-P6 六阶段全景图`, {
    x: 0.8, y: 0.25, w: 10, h: 0.6,
    fontSize: 28, fontFace: FONT, color: palette.accent, bold: true,
  });

  const phases = [
    { id: "P0", name: "概念与定义", owner: "企划", color: palette.green },
    { id: "P1", name: "调研与设计", owner: "企划+研发", color: palette.gold },
    { id: "P2", name: "开发与设计", owner: "研发", color: palette.orange },
    { id: "P3", name: "推敲验证", owner: "研发", color: palette.orange },
    { id: "P4", name: "交付", owner: "研发+企划", color: palette.gold },
    { id: "P5", name: "成熟运营", owner: "研发+企划", color: palette.gold },
    { id: "P6", name: "产品退市", owner: "企划", color: palette.green },
  ];

  phases.forEach((p, i) => {
    const x = 0.5 + i * 1.78;
    const w = 1.6;
    // 卡片背景
    slide.addShape("roundRect", { x: x, y: 1.8, w: w, h: 3.8, fill: { color: palette.accent }, shadow: { type: "outer", blur: 3, offset: 1, color: "000000", opacity: 0.15 }, rectRound: 0.1 });
    // 阶段编号
    slide.addShape("roundRect", { x: x + 0.3, y: 2.0, w: 1.0, h: 0.5, fill: { color: palette.primary }, rectRound: 0.05 });
    slide.addText(p.id, {
      x: x + 0.3, y: 2.0, w: 1.0, h: 0.5,
      fontSize: 18, fontFace: FONT, color: palette.accent, bold: true, align: "center", valign: "middle",
    });
    // 阶段名称
    slide.addText(p.name, {
      x: x + 0.1, y: 2.7, w: w - 0.2, h: 0.5,
      fontSize: 14, fontFace: FONT, color: palette.dark, bold: true, align: "center",
    });
    // 归属标签
    slide.addShape("roundRect", { x: x + 0.15, y: 3.3, w: w - 0.3, h: 0.4, fill: { color: p.color, transparency: 20 }, rectRound: 0.05 });
    slide.addText(p.owner, {
      x: x + 0.15, y: 3.3, w: w - 0.3, h: 0.4,
      fontSize: 11, fontFace: FONT, color: p.color, bold: true, align: "center", valign: "middle",
    });
    // 箭头（除最后一个）
    if (i < phases.length - 1) {
      slide.addText(`→`, {
        x: x + w, y: 3.3, w: 0.3, h: 0.5,
        fontSize: 20, fontFace: FONT, color: palette.primary, align: "center", valign: "middle",
      });
    }
  });

  // 底部图例
  slide.addShape("roundRect", { x: 0.5, y: 6.0, w: 0.3, h: 0.25, fill: { color: palette.green, transparency: 20 }, rectRound: 0.03 });
  slide.addText(`企划主导`, { x: 0.9, y: 6.0, w: 1.2, h: 0.25, fontSize: 11, fontFace: FONT, color: palette.gray });
  slide.addShape("roundRect", { x: 2.5, y: 6.0, w: 0.3, h: 0.25, fill: { color: palette.gold, transparency: 20 }, rectRound: 0.03 });
  slide.addText(`企划+研发协作`, { x: 2.9, y: 6.0, w: 1.5, h: 0.25, fontSize: 11, fontFace: FONT, color: palette.gray });
  slide.addShape("roundRect", { x: 4.8, y: 6.0, w: 0.3, h: 0.25, fill: { color: palette.orange, transparency: 20 }, rectRound: 0.03 });
  slide.addText(`研发主导`, { x: 5.2, y: 6.0, w: 1.2, h: 0.25, fontSize: 11, fontFace: FONT, color: palette.gray });

  // ============ SLIDE 4: P0 概念与定义 ============
  slide = pptx.addSlide();
  slide.background = { color: palette.light };
  slide.addShape("rect", { x: 0, y: 0, w: 13.33, h: 1.1, fill: { color: palette.green } });
  slide.addText(`P0 概念与定义`, {
    x: 0.8, y: 0.15, w: 6, h: 0.5,
    fontSize: 28, fontFace: FONT, color: palette.accent, bold: true,
  });
  slide.addShape("roundRect", { x: 0.8, y: 0.7, w: 1.2, h: 0.3, fill: { color: palette.accent, transparency: 30 }, rectRound: 0.05 });
  slide.addText(`企划主导`, {
    x: 0.8, y: 0.7, w: 1.2, h: 0.3,
    fontSize: 12, fontFace: FONT, color: palette.accent, bold: true, align: "center", valign: "middle",
  });

  const p0Items = [
    "企划书（含 MRD / 产品数据表）",
    "产品对手对阵表",
    "创意评审报告",
    "POD（立项报告 / 注册表 / 市场分析 / 预算表）",
    "差异点的分析报告",
    "外观效果图 / 外观图形评审意见书",
    "创意评审会",
  ];

  p0Items.forEach((item, i) => {
    const y = 1.5 + i * 0.75;
    slide.addShape("roundRect", { x: 0.8, y: y, w: 11.5, h: 0.6, fill: { color: palette.accent }, shadow: { type: "outer", blur: 2, offset: 1, color: "000000", opacity: 0.1 }, rectRound: 0.08 });
    // 序号
    slide.addShape("ellipse", { x: 1.0, y: y + 0.1, w: 0.4, h: 0.4, fill: { color: palette.green } });
    slide.addText(`${i + 1}`, {
      x: 1.0, y: y + 0.1, w: 0.4, h: 0.4,
      fontSize: 13, fontFace: FONT, color: palette.accent, bold: true, align: "center", valign: "middle",
    });
    slide.addText(item, {
      x: 1.6, y: y, w: 10.5, h: 0.6,
      fontSize: 15, fontFace: FONT, color: palette.dark, valign: "middle",
    });
  });

  // 右侧标注
  slide.addShape("roundRect", { x: 10.5, y: 6.2, w: 2.3, h: 0.7, fill: { color: palette.green, transparency: 15 }, rectRound: 0.08 });
  slide.addText(`100% 企划负责\n产品方向的源头`, {
    x: 10.5, y: 6.2, w: 2.3, h: 0.7,
    fontSize: 12, fontFace: FONT, color: palette.green, bold: true, align: "center", valign: "middle",
  });

  // ============ SLIDE 5: P1 调研与设计 ============
  slide = pptx.addSlide();
  slide.background = { color: palette.light };
  slide.addShape("rect", { x: 0, y: 0, w: 13.33, h: 1.1, fill: { color: palette.primary } });
  slide.addText(`P1 调研与设计`, {
    x: 0.8, y: 0.15, w: 6, h: 0.5,
    fontSize: 28, fontFace: FONT, color: palette.accent, bold: true,
  });
  slide.addShape("roundRect", { x: 0.8, y: 0.7, w: 1.6, h: 0.3, fill: { color: palette.accent, transparency: 30 }, rectRound: 0.05 });
  slide.addText(`企划 + 研发协作`, {
    x: 0.8, y: 0.7, w: 1.6, h: 0.3,
    fontSize: 11, fontFace: FONT, color: palette.accent, bold: true, align: "center", valign: "middle",
  });

  // 左栏 - 企划
  slide.addShape("roundRect", { x: 0.5, y: 1.4, w: 5.8, h: 5.5, fill: { color: palette.accent }, shadow: { type: "outer", blur: 2, offset: 1, color: "000000", opacity: 0.1 }, rectRound: 0.1 });
  slide.addShape("roundRect", { x: 0.5, y: 1.4, w: 5.8, h: 0.55, fill: { color: palette.green }, rectRound: 0.1 });
  slide.addText(`企划负责`, {
    x: 0.7, y: 1.42, w: 5, h: 0.5,
    fontSize: 18, fontFace: FONT, color: palette.accent, bold: true, valign: "middle",
  });

  const p1Plan = [
    "产品技术规格书",
    "市场计划",
    "用户测试报告",
    "成本BOM",
  ];
  p1Plan.forEach((item, i) => {
    const y = 2.2 + i * 0.65;
    slide.addShape("ellipse", { x: 0.8, y: y + 0.12, w: 0.25, h: 0.25, fill: { color: palette.green } });
    slide.addText(item, {
      x: 1.2, y: y, w: 4.5, h: 0.5,
      fontSize: 14, fontFace: FONT, color: palette.dark, valign: "middle",
    });
  });

  // 右栏 - 研发
  slide.addShape("roundRect", { x: 6.8, y: 1.4, w: 5.8, h: 5.5, fill: { color: palette.accent }, shadow: { type: "outer", blur: 2, offset: 1, color: "000000", opacity: 0.1 }, rectRound: 0.1 });
  slide.addShape("roundRect", { x: 6.8, y: 1.4, w: 5.8, h: 0.55, fill: { color: palette.orange }, rectRound: 0.1 });
  slide.addText(`研发负责`, {
    x: 7.0, y: 1.42, w: 5, h: 0.5,
    fontSize: 18, fontFace: FONT, color: palette.accent, bold: true, valign: "middle",
  });

  const p1Rnd = [
    "质量计划 / 采购计划 / 制造计划",
    "基本型号品质分析及改善计划",
    "3D设计图",
    "模型样机评审结论",
    "母本分析报告",
    "主关件清单",
    "新功能模块标准",
  ];
  p1Rnd.forEach((item, i) => {
    const y = 2.2 + i * 0.65;
    slide.addShape("ellipse", { x: 7.1, y: y + 0.12, w: 0.25, h: 0.25, fill: { color: palette.orange } });
    slide.addText(item, {
      x: 7.5, y: y, w: 4.5, h: 0.5,
      fontSize: 14, fontFace: FONT, color: palette.dark, valign: "middle",
    });
  });

  // ============ SLIDE 6: P2 开发与设计 ============
  slide = pptx.addSlide();
  slide.background = { color: palette.light };
  slide.addShape("rect", { x: 0, y: 0, w: 13.33, h: 1.1, fill: { color: palette.orange } });
  slide.addText(`P2 开发与设计`, {
    x: 0.8, y: 0.15, w: 6, h: 0.5,
    fontSize: 28, fontFace: FONT, color: palette.accent, bold: true,
  });
  slide.addShape("roundRect", { x: 0.8, y: 0.7, w: 1.0, h: 0.3, fill: { color: palette.accent, transparency: 30 }, rectRound: 0.05 });
  slide.addText(`研发主导`, {
    x: 0.8, y: 0.7, w: 1.0, h: 0.3,
    fontSize: 11, fontFace: FONT, color: palette.accent, bold: true, align: "center", valign: "middle",
  });

  const p2Col1 = [
    "质量计划调整",
    "零部件图纸 / 零部件数据",
    "新品任务单",
    "零部件标准",
    "测试计划",
    "DFMEA分析",
    "新部品报验计划",
  ];
  const p2Col2 = [
    "设计雷区排查",
    "图纸评审和发布",
    "模块化设计项目确认",
    "新功能模块设计评审验证",
    "模具交互制作",
    "手工样机评审及问题闭环",
  ];

  // 列1
  p2Col1.forEach((item, i) => {
    const y = 1.4 + i * 0.78;
    slide.addShape("roundRect", { x: 0.5, y: y, w: 5.8, h: 0.65, fill: { color: palette.accent }, shadow: { type: "outer", blur: 2, offset: 1, color: "000000", opacity: 0.08 }, rectRound: 0.06 });
    slide.addShape("roundRect", { x: 0.5, y: y, w: 0.08, h: 0.65, fill: { color: palette.orange }, rectRound: 0.05 });
    slide.addText(item, {
      x: 0.8, y: y, w: 5.3, h: 0.65,
      fontSize: 14, fontFace: FONT, color: palette.dark, valign: "middle",
    });
  });
  // 列2
  p2Col2.forEach((item, i) => {
    const y = 1.4 + i * 0.78;
    slide.addShape("roundRect", { x: 6.8, y: y, w: 5.8, h: 0.65, fill: { color: palette.accent }, shadow: { type: "outer", blur: 2, offset: 1, color: "000000", opacity: 0.08 }, rectRound: 0.06 });
    slide.addShape("roundRect", { x: 6.8, y: y, w: 0.08, h: 0.65, fill: { color: palette.orange }, rectRound: 0.05 });
    slide.addText(item, {
      x: 7.1, y: y, w: 5.3, h: 0.65,
      fontSize: 14, fontFace: FONT, color: palette.dark, valign: "middle",
    });
  });

  // ============ SLIDE 7: P3 推敲验证 ============
  slide = pptx.addSlide();
  slide.background = { color: palette.light };
  slide.addShape("rect", { x: 0, y: 0, w: 13.33, h: 1.1, fill: { color: palette.orange } });
  slide.addText(`P3 推敲验证`, {
    x: 0.8, y: 0.15, w: 6, h: 0.5,
    fontSize: 28, fontFace: FONT, color: palette.accent, bold: true,
  });
  slide.addShape("roundRect", { x: 0.8, y: 0.7, w: 1.0, h: 0.3, fill: { color: palette.accent, transparency: 30 }, rectRound: 0.05 });
  slide.addText(`研发主导`, {
    x: 0.8, y: 0.7, w: 1.0, h: 0.3,
    fontSize: 11, fontFace: FONT, color: palette.accent, bold: true, align: "center", valign: "middle",
  });

  const p3Items = [
    "零部件数据及标准 / 工艺文件及BOM准确性",
    "测试计划实施闭环 / DFMEA分析实施闭环",
    "设计雷区排查闭环",
    "3C证书或生产许可证 / 能效备案证明",
    "CTQ参数一致性确认",
    "用户模拟问题闭环",
    "模具验收 / 试验样机评审及问题闭环",
    "工艺样机评审及问题闭环",
    "工艺文件下发到位",
    "印刷品封样 / 抽样合格",
  ];

  p3Items.forEach((item, i) => {
    const y = 1.35 + i * 0.55;
    slide.addShape("roundRect", { x: 0.5, y: y, w: 12.1, h: 0.48, fill: { color: palette.accent }, shadow: { type: "outer", blur: 1, offset: 1, color: "000000", opacity: 0.06 }, rectRound: 0.05 });
    slide.addShape("roundRect", { x: 0.5, y: y, w: 0.06, h: 0.48, fill: { color: palette.orange }, rectRound: 0.05 });
    slide.addText(item, {
      x: 0.8, y: y, w: 11.6, h: 0.48,
      fontSize: 13, fontFace: FONT, color: palette.dark, valign: "middle",
    });
  });

  // ============ SLIDE 8: P4 交付 ============
  slide = pptx.addSlide();
  slide.background = { color: palette.light };
  slide.addShape("rect", { x: 0, y: 0, w: 13.33, h: 1.1, fill: { color: palette.primary } });
  slide.addText(`P4 交付`, {
    x: 0.8, y: 0.15, w: 6, h: 0.5,
    fontSize: 28, fontFace: FONT, color: palette.accent, bold: true,
  });
  slide.addShape("roundRect", { x: 0.8, y: 0.7, w: 1.6, h: 0.3, fill: { color: palette.accent, transparency: 30 }, rectRound: 0.05 });
  slide.addText(`研发 + 企划协作`, {
    x: 0.8, y: 0.7, w: 1.6, h: 0.3,
    fontSize: 11, fontFace: FONT, color: palette.accent, bold: true, align: "center", valign: "middle",
  });

  // 左栏 - 企划
  slide.addShape("roundRect", { x: 0.5, y: 1.4, w: 5.8, h: 3.0, fill: { color: palette.accent }, shadow: { type: "outer", blur: 2, offset: 1, color: "000000", opacity: 0.1 }, rectRound: 0.1 });
  slide.addShape("roundRect", { x: 0.5, y: 1.4, w: 5.8, h: 0.5, fill: { color: palette.green }, rectRound: 0.1 });
  slide.addText(`企划负责`, {
    x: 0.7, y: 1.42, w: 5, h: 0.48,
    fontSize: 16, fontFace: FONT, color: palette.accent, bold: true, valign: "middle",
  });
  const p4Plan = ["市场推介计划", "项目总结"];
  p4Plan.forEach((item, i) => {
    slide.addText(`· ${item}`, {
      x: 0.8, y: 2.2 + i * 0.5, w: 5, h: 0.4,
      fontSize: 14, fontFace: FONT, color: palette.dark, valign: "middle",
    });
  });

  // 右栏 - 研发
  slide.addShape("roundRect", { x: 6.8, y: 1.4, w: 5.8, h: 5.3, fill: { color: palette.accent }, shadow: { type: "outer", blur: 2, offset: 1, color: "000000", opacity: 0.1 }, rectRound: 0.1 });
  slide.addShape("roundRect", { x: 6.8, y: 1.4, w: 5.8, h: 0.5, fill: { color: palette.orange }, rectRound: 0.1 });
  slide.addText(`研发负责`, {
    x: 7.0, y: 1.42, w: 5, h: 0.48,
    fontSize: 16, fontFace: FONT, color: palette.accent, bold: true, valign: "middle",
  });
  const p4Rnd = [
    "滚动计划 / 生产订单保障评审",
    "小批首批物料入厂检验",
    "小批首台样机评审",
    "商检出货报告",
    "售后培训 / 售后备件",
    "新品初期三个月质量问题跟踪",
    "QCL/QC/OQC 过程管控",
  ];
  p4Rnd.forEach((item, i) => {
    slide.addText(`· ${item}`, {
      x: 7.1, y: 2.2 + i * 0.55, w: 5.2, h: 0.45,
      fontSize: 13, fontFace: FONT, color: palette.dark, valign: "middle",
    });
  });

  // ============ SLIDE 9: P5-P6 运营与退市 ============
  slide = pptx.addSlide();
  slide.background = { color: palette.light };
  slide.addShape("rect", { x: 0, y: 0, w: 13.33, h: 1.1, fill: { color: palette.primary } });
  slide.addText(`P5 成熟运营 & P6 产品退市`, {
    x: 0.8, y: 0.15, w: 10, h: 0.5,
    fontSize: 28, fontFace: FONT, color: palette.accent, bold: true,
  });

  // P5 区块
  slide.addShape("roundRect", { x: 0.5, y: 1.5, w: 12.1, h: 3.2, fill: { color: palette.accent }, shadow: { type: "outer", blur: 2, offset: 1, color: "000000", opacity: 0.08 }, rectRound: 0.1 });
  slide.addShape("roundRect", { x: 0.5, y: 1.5, w: 12.1, h: 0.55, fill: { color: palette.primary, transparency: 20 }, rectRound: 0.1 });
  slide.addText(`P5 成熟运营 — 研发主导 + 企划年度复审`, {
    x: 0.8, y: 1.55, w: 10, h: 0.45,
    fontSize: 17, fontFace: FONT, color: palette.primary, bold: true, valign: "middle",
  });

  const p5Items = [
    { text: "产品年内复审", owner: "企划", clr: palette.green },
    { text: "工程管理 / 跳闸型号评审", owner: "研发", clr: palette.orange },
    { text: "型号维度质量改善", owner: "研发", clr: palette.orange },
    { text: "老品4M1E变更管控", owner: "研发", clr: palette.orange },
    { text: "老品市场问题闭环", owner: "研发", clr: palette.orange },
  ];
  p5Items.forEach((item, i) => {
    const y = 2.3 + i * 0.55;
    slide.addText(`· ${item.text}`, {
      x: 0.8, y: y, w: 8, h: 0.4,
      fontSize: 13, fontFace: FONT, color: palette.dark, valign: "middle",
    });
    slide.addShape("roundRect", { x: 9.5, y: y + 0.05, w: 0.8, h: 0.3, fill: { color: item.clr, transparency: 20 }, rectRound: 0.05 });
    slide.addText(item.owner, {
      x: 9.5, y: y + 0.05, w: 0.8, h: 0.3,
      fontSize: 10, fontFace: FONT, color: item.clr, bold: true, align: "center", valign: "middle",
    });
  });

  // P6 区块
  slide.addShape("roundRect", { x: 0.5, y: 5.1, w: 12.1, h: 1.5, fill: { color: palette.accent }, shadow: { type: "outer", blur: 2, offset: 1, color: "000000", opacity: 0.08 }, rectRound: 0.1 });
  slide.addShape("roundRect", { x: 0.5, y: 5.1, w: 12.1, h: 0.5, fill: { color: palette.green, transparency: 20 }, rectRound: 0.1 });
  slide.addText(`P6 产品退市 — 企划主导`, {
    x: 0.8, y: 5.13, w: 10, h: 0.45,
    fontSize: 17, fontFace: FONT, color: palette.green, bold: true, valign: "middle",
  });
  slide.addText(`· 产品下市申请`, {
    x: 0.8, y: 5.8, w: 10, h: 0.5,
    fontSize: 15, fontFace: FONT, color: palette.dark, valign: "middle",
  });

  // ============ SLIDE 10: 职责汇总 ============
  slide = pptx.addSlide();
  slide.background = { color: palette.light };
  slide.addShape("rect", { x: 0, y: 0, w: 13.33, h: 1.1, fill: { color: palette.primary } });
  slide.addText(`职责汇总对比`, {
    x: 0.8, y: 0.25, w: 8, h: 0.6,
    fontSize: 28, fontFace: FONT, color: palette.accent, bold: true,
  });

  // 企划汇总卡片
  slide.addShape("roundRect", { x: 0.5, y: 1.4, w: 5.8, h: 5.5, fill: { color: palette.accent }, shadow: { type: "outer", blur: 3, offset: 1, color: "000000", opacity: 0.1 }, rectRound: 0.12 });
  slide.addShape("roundRect", { x: 0.5, y: 1.4, w: 5.8, h: 0.65, fill: { color: palette.green }, rectRound: 0.12 });
  slide.addText(`企划（产品规划）`, {
    x: 0.7, y: 1.45, w: 4, h: 0.55,
    fontSize: 20, fontFace: FONT, color: palette.accent, bold: true, valign: "middle",
  });

  const planSummary = [
    "P0：概念与定义（100%主导）",
    "P1：产品技术规格书 / 市场计划 / 成本BOM",
    "P4：市场推介计划 / 项目总结",
    "P5：产品年内复审",
    "P6：产品下市申请",
  ];
  planSummary.forEach((item, i) => {
    slide.addText(`· ${item}`, {
      x: 0.8, y: 2.4 + i * 0.6, w: 5.2, h: 0.5,
      fontSize: 13, fontFace: FONT, color: palette.dark, valign: "middle",
    });
  });
  slide.addText(`核心：定方向\n"做什么、卖给谁、多少钱"`, {
    x: 0.8, y: 5.6, w: 5, h: 0.9,
    fontSize: 13, fontFace: FONT, color: palette.green, bold: true, valign: "middle",
  });

  // 研发汇总卡片
  slide.addShape("roundRect", { x: 6.8, y: 1.4, w: 5.8, h: 5.5, fill: { color: palette.accent }, shadow: { type: "outer", blur: 3, offset: 1, color: "000000", opacity: 0.1 }, rectRound: 0.12 });
  slide.addShape("roundRect", { x: 6.8, y: 1.4, w: 5.8, h: 0.65, fill: { color: palette.orange }, rectRound: 0.12 });
  slide.addText(`研发（工程实现）`, {
    x: 7.0, y: 1.45, w: 4, h: 0.55,
    fontSize: 20, fontFace: FONT, color: palette.accent, bold: true, valign: "middle",
  });

  const rndSummary = [
    "P1：质量/采购/制造计划 / 3D设计",
    "P2：开发与设计（100%主导）",
    "P3：推敲验证（100%主导）",
    "P4：量产保障 / 售后 / 过程管控",
    "P5：工程管理 / 质量改善 / 变更管控",
  ];
  rndSummary.forEach((item, i) => {
    slide.addText(`· ${item}`, {
      x: 7.1, y: 2.4 + i * 0.6, w: 5.2, h: 0.5,
      fontSize: 13, fontFace: FONT, color: palette.dark, valign: "middle",
    });
  });
  slide.addText(`核心：管落地\n"怎么做、能不能做、质量过不过关"`, {
    x: 7.1, y: 5.6, w: 5, h: 0.9,
    fontSize: 13, fontFace: FONT, color: palette.orange, bold: true, valign: "middle",
  });

  // ============ SLIDE 11: 结束页 ============
  slide = pptx.addSlide();
  slide.background = { color: palette.primary };
  slide.addShape("rect", { x: 0, y: 0, w: 13.33, h: 0.06, fill: { color: palette.gold } });
  slide.addShape("rect", { x: 0, y: 7.44, w: 13.33, h: 0.06, fill: { color: palette.gold } });

  slide.addText(`感谢聆听`, {
    x: 0, y: 2.2, w: 13.33, h: 1.2,
    fontSize: 48, fontFace: FONT, color: palette.accent, bold: true, align: "center", valign: "middle",
  });
  slide.addShape("rect", { x: 5.5, y: 3.5, w: 2.3, h: 0.04, fill: { color: palette.gold } });
  slide.addText(`海尔产品研发流程 · 企划与研发职责分工`, {
    x: 0, y: 3.9, w: 13.33, h: 0.6,
    fontSize: 16, fontFace: FONT, color: palette.secondary, align: "center", valign: "middle",
  });
  slide.addText(`企划定方向 · 研发管落地`, {
    x: 0, y: 4.5, w: 13.33, h: 0.5,
    fontSize: 14, fontFace: FONT, color: palette.gold, align: "center", valign: "middle",
  });

  // 保存
  const path = require("path");
  const outputPath = path.join(__dirname, "海尔产品研发流程_企划与研发职责分工.pptx");
  await pptx.writeFile({ fileName: outputPath });
  console.log(`PPT saved to: ${outputPath}`);
}
main();
