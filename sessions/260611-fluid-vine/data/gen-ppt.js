const pptxgen = require("pptxgenjs");
const path = require("path");

const P = {
  primary: "1E2761",
  secondary: "CADCFC",
  accent: "FFFFFF",
  dark: "0D1117",
  orange: "FA7800",
  lightBg: "F5F7FA",
  gray: "6B7280",
  teal: "0EA5A9",
};

// Helper: add page title bar
function addTitleBar(slide, title) {
  slide.addShape("rect", { x: 0, y: 0, w: 13.33, h: 0.06, fill: { color: P.orange } });
  slide.addText(title, { x: 0.8, y: 0.3, w: 11, h: 0.65, fontSize: 28, bold: true, color: P.primary, fontFace: "Microsoft YaHei" });
  slide.addShape("rect", { x: 0.8, y: 0.9, w: 1.5, h: 0.04, fill: { color: P.orange } });
}

// Helper: card
function addCard(slide, x, y, w, h, color, shadow) {
  slide.addShape("roundRect", {
    x, y, w, h,
    fill: { color: P.accent },
    rectRound: 0.1,
    shadow: shadow ? { type: "outer", blur: 5, offset: 2, color: "000000", opacity: 0.08 } : undefined
  });
}

async function main() {
  const pptx = new pptxgen();
  pptx.layout = { width: 13.33, height: 7.5 };
  pptx.author = "海尔智家创新团队";
  pptx.title = "心有灵犀 - AI情绪感知智能家电";

  // ========== S1: 封面 ==========
  {
    const s = pptx.addSlide();
    s.background = { color: P.primary };
    s.addShape("rect", { x: 0, y: 0, w: 13.33, h: 0.06, fill: { color: P.orange } });
    s.addShape("rect", { x: 1.2, y: 1.5, w: 0.07, h: 2.8, fill: { color: P.orange } });
    s.addShape("rect", { x: 0, y: 7.0, w: 13.33, h: 0.5, fill: { color: P.orange, transparency: 80 } });
    s.addText("海尔智家 · 创无限 AI无界", { x: 1.5, y: 1.2, w: 8, h: 0.5, fontSize: 14, color: P.secondary, fontFace: "Microsoft YaHei" });
    s.addText("心有灵犀", { x: 1.5, y: 1.7, w: 9, h: 1.3, fontSize: 56, bold: true, color: P.accent, fontFace: "Microsoft YaHei" });
    s.addText("基于AI情绪感知的新一代智能家电生态", { x: 1.5, y: 3.1, w: 9, h: 0.7, fontSize: 22, color: P.secondary, fontFace: "Microsoft YaHei" });
    s.addText("新研发&管理赛道 | 课题方向：家电+情绪价值", { x: 1.5, y: 4.0, w: 8, h: 0.4, fontSize: 14, color: P.secondary, fontFace: "Microsoft YaHei" });
    s.addText("2026年6月 | 海尔智家", { x: 1.5, y: 6.5, w: 6, h: 0.4, fontSize: 12, color: P.secondary, fontFace: "Microsoft YaHei" });
  }

  // ========== S2: 目录 ==========
  {
    const s = pptx.addSlide();
    s.background = { color: P.accent };
    s.addShape("rect", { x: 0, y: 0, w: 13.33, h: 0.06, fill: { color: P.orange } });
    s.addText("目 录", { x: 0.8, y: 0.3, w: 5, h: 0.8, fontSize: 32, bold: true, color: P.primary, fontFace: "Microsoft YaHei" });
    s.addShape("rect", { x: 0.8, y: 1.05, w: 1.2, h: 0.04, fill: { color: P.orange } });

    const toc = [
      ["01", "市场洞察", "情绪经济与智能家居双风口交汇"],
      ["02", "用户痛点", "2.6亿Z世代的孤独经济与情感需求"],
      ["03", "产品概念", "AI情绪感知智能家电生态全景"],
      ["04", "核心技术", "多模态情绪识别+大模型引擎"],
      ["05", "应用场景", "四大生活场景的情绪解决方案"],
      ["06", "商业模式", "竞争优势与商业价值分析"],
      ["07", "实施路线", "团队组建与分阶段落地计划"],
    ];
    toc.forEach((t, i) => {
      const col = i < 4 ? 0 : 1;
      const row = i < 4 ? i : i - 4;
      const x = 0.8 + col * 6.2;
      const y = 1.5 + row * 1.3;
      s.addShape("roundRect", { x, y, w: 0.6, h: 0.6, fill: { color: P.primary }, rectRound: 0.12 });
      s.addText(t[0], { x, y: y + 0.03, w: 0.6, h: 0.54, fontSize: 16, bold: true, color: P.accent, fontFace: "Microsoft YaHei", align: "center" });
      s.addText(t[1], { x: x + 0.8, y, w: 4.5, h: 0.35, fontSize: 15, bold: true, color: P.primary, fontFace: "Microsoft YaHei" });
      s.addText(t[2], { x: x + 0.8, y: y + 0.33, w: 4.5, h: 0.3, fontSize: 11, color: P.gray, fontFace: "Microsoft YaHei" });
    });
  }

  // ========== S3: 市场洞察 ==========
  {
    const s = pptx.addSlide();
    s.background = { color: P.lightBg };
    addTitleBar(s, "市场洞察：双风口交汇");

    // 左侧卡 - 情绪经济
    addCard(s, 0.5, 1.3, 5.9, 5.6);
    s.addShape("rect", { x: 0.5, y: 1.3, w: 5.9, h: 0.65, fill: { color: P.orange, transparency: 85 }, rectRound: 0.1 });
    s.addText("情绪经济爆发", { x: 0.8, y: 1.35, w: 5, h: 0.55, fontSize: 17, bold: true, color: P.orange, fontFace: "Microsoft YaHei" });

    const eData = [
      { val: "80%+", sub: "消费者每月至少一次\n情绪消费（知萌2026）" },
      { val: "2.8亿", sub: "中国Z世代人口\n推动情绪消费新潮流" },
      { val: "40%+", sub: "年轻人愿为情绪价值\n和兴趣付费" },
    ];
    eData.forEach((d, i) => {
      const y = 2.2 + i * 1.5;
      s.addShape("roundRect", { x: 0.8, y, w: 5.3, h: 1.2, fill: { color: P.lightBg }, rectRound: 0.08 });
      s.addText(d.val, { x: 0.8, y: y + 0.08, w: 1.6, h: 1.04, fontSize: 26, bold: true, color: P.orange, fontFace: "Microsoft YaHei", align: "center" });
      s.addText(d.sub, { x: 2.5, y: y + 0.1, w: 3.5, h: 1.0, fontSize: 12, color: P.dark, fontFace: "Microsoft YaHei", lineSpacing: 20 });
    });

    // 右侧卡 - 智能家居
    addCard(s, 6.9, 1.3, 5.9, 5.6);
    s.addShape("rect", { x: 6.9, y: 1.3, w: 5.9, h: 0.65, fill: { color: P.primary, transparency: 85 }, rectRound: 0.1 });
    s.addText("智能家居蓝海", { x: 7.2, y: 1.35, w: 5, h: 0.55, fontSize: 17, bold: true, color: P.primary, fontFace: "Microsoft YaHei" });

    const sData = [
      { val: "1,475亿$", sub: "2025全球智能家居规模\nCAGR高达21.4%" },
      { val: "7,938亿¥", sub: "2025中国智能家电市场\n持续高速增长" },
      { val: "AI+情绪", sub: "2025行业关键词\n家电学会"共情"" },
    ];
    sData.forEach((d, i) => {
      const y = 2.2 + i * 1.5;
      s.addShape("roundRect", { x: 7.2, y, w: 5.3, h: 1.2, fill: { color: P.lightBg }, rectRound: 0.08 });
      s.addText(d.val, { x: 7.2, y: y + 0.08, w: 1.8, h: 1.04, fontSize: 26, bold: true, color: P.primary, fontFace: "Microsoft YaHei", align: "center" });
      s.addText(d.sub, { x: 9.1, y: y + 0.1, w: 3.3, h: 1.0, fontSize: 12, color: P.dark, fontFace: "Microsoft YaHei", lineSpacing: 20 });
    });

    // 交叉标签
    s.addShape("roundRect", { x: 4.3, y: 5.8, w: 4.73, h: 0.6, fill: { color: P.orange }, rectRound: 0.12 });
    s.addText("情绪经济 × 智能家居 = 万亿级新赛道", { x: 4.3, y: 5.85, w: 4.73, h: 0.5, fontSize: 14, bold: true, color: P.accent, fontFace: "Microsoft YaHei", align: "center" });
  }

  // ========== S4: 用户痛点 ==========
  {
    const s = pptx.addSlide();
    s.background = { color: P.primary };
    s.addShape("rect", { x: 0, y: 0, w: 13.33, h: 0.06, fill: { color: P.orange } });
    s.addText("用户痛点：Z世代的孤独与压力", { x: 0.8, y: 0.3, w: 11, h: 0.7, fontSize: 28, bold: true, color: P.accent, fontFace: "Microsoft YaHei" });
    s.addShape("rect", { x: 0.8, y: 0.95, w: 1.5, h: 0.04, fill: { color: P.orange } });

    const pains = [
      { icon: "\u{1F614}", title: "独居孤独感", desc: "中国独居人口超1.25亿\n空巢青年下班无人交流\n情感陪伴需求急剧增长", stat: "1.25亿", lab: "独居人口" },
      { icon: "\u{1F630}", title: "高压焦虑", desc: "超70%职场人存在焦虑\n996压力无处释放\n家庭场景亟需情绪出口", stat: "70%+", lab: "职场焦虑率" },
      { icon: "\u{1F319}", title: "睡眠障碍", desc: "中国超3亿人睡眠障碍\n入睡困难与情绪高度相关\n卧室环境急需智能升级", stat: "3亿+", lab: "睡眠障碍人群" },
      { icon: "\u{1F494}", title: "情感断连", desc: "数字社交替代真实互动\n家人之间关系日渐疏离\n家电不懂用户的真实情绪", stat: "83%", lab: "愿与AI建联系" },
    ];

    pains.forEach((p, i) => {
      const x = 0.4 + i * 3.2;
      // 卡片背景
      s.addShape("roundRect", { x, y: 1.3, w: 3.0, h: 5.6, fill: { color: P.accent, transparency: 92 }, rectRound: 0.12 });
      // 图标圆
      s.addShape("ellipse", { x: x + 0.95, y: 1.5, w: 1.1, h: 1.1, fill: { color: P.orange, transparency: 20 } });
      s.addText(p.icon, { x: x + 0.95, y: 1.55, w: 1.1, h: 1.0, fontSize: 32, align: "center" });
      // 标题
      s.addText(p.title, { x: x + 0.2, y: 2.8, w: 2.6, h: 0.4, fontSize: 16, bold: true, color: P.accent, fontFace: "Microsoft YaHei", align: "center" });
      // 描述
      s.addText(p.desc, { x: x + 0.15, y: 3.3, w: 2.7, h: 1.6, fontSize: 12, color: P.secondary, fontFace: "Microsoft YaHei", align: "center", lineSpacing: 22 });
      // 数据卡片
      s.addShape("roundRect", { x: x + 0.4, y: 5.2, w: 2.2, h: 1.2, fill: { color: P.accent, transparency: 88 }, rectRound: 0.08 });
      s.addText(p.stat, { x: x + 0.4, y: 5.25, w: 2.2, h: 0.6, fontSize: 22, bold: true, color: P.orange, fontFace: "Microsoft YaHei", align: "center" });
      s.addText(p.lab, { x: x + 0.4, y: 5.85, w: 2.2, h: 0.4, fontSize: 11, color: P.secondary, fontFace: "Microsoft YaHei", align: "center" });
    });
  }

  // ========== S5: 产品概念 ==========
  {
    const s = pptx.addSlide();
    s.background = { color: P.accent };
    addTitleBar(s, "产品概念：AI情绪感知家电生态");
    s.addText("构建一个"读懂情绪、主动关怀、无声陪伴"的智能家电生态系统", { x: 0.8, y: 1.15, w: 11, h: 0.4, fontSize: 13, color: P.gray, fontFace: "Microsoft YaHei" });

    const products = [
      { name: "情绪感知空调", sub: "EmoSense AC", desc: "多模态传感感知用户情绪状态\n自动调节温度/湿度/灯光/香薰\n一句话"我心情不好"即可触发", feat: "语音情绪识别 · 体态分析 · 自适应调节", clr: P.primary },
      { name: "智能陪伴音箱", sub: "SoulMate Speaker", desc: "基于AI大模型的共情对话引擎\n主动问候、情感聊天、情绪疏导\n记住用户偏好，越聊越懂你", feat: "共情对话 · 记忆画像 · 主动关怀", clr: P.orange },
      { name: "智能睡眠系统", sub: "DreamCare System", desc: "监测睡眠质量与睡前情绪波动\n联动床垫/灯光/窗帘/香薰\n打造最适配的情绪助眠环境", feat: "情绪监测 · 智能唤醒 · 全屋联动", clr: P.teal },
      { name: "家庭情绪中枢", sub: "HomeEmo Hub", desc: "全屋情绪数据汇聚与分析平台\n为每个家庭成员建情绪健康档案\n异常情绪预警，守护家人心理", feat: "全屋感知 · 家庭画像 · 健康预警", clr: P.primary },
    ];

    products.forEach((p, i) => {
      const x = 0.3 + i * 3.25;
      addCard(s, x, 1.8, 3.05, 5.1);
      s.addShape("rect", { x, y: 1.8, w: 3.05, h: 0.08, fill: { color: p.clr }, rectRound: 0.1 });
      s.addText(p.name, { x: x + 0.15, y: 2.05, w: 2.4, h: 0.4, fontSize: 16, bold: true, color: P.dark, fontFace: "Microsoft YaHei" });
      s.addText(p.sub, { x: x + 0.15, y: 2.4, w: 2.4, h: 0.28, fontSize: 10, italic: true, color: p.clr, fontFace: "Microsoft YaHei" });
      s.addText(p.desc, { x: x + 0.15, y: 2.85, w: 2.75, h: 2.0, fontSize: 12, color: P.gray, fontFace: "Microsoft YaHei", lineSpacing: 24 });
      s.addShape("roundRect", { x: x + 0.15, y: 5.05, w: 2.75, h: 1.1, fill: { color: P.lightBg }, rectRound: 0.06 });
      s.addText(p.feat, { x: x + 0.25, y: 5.1, w: 2.55, h: 1.0, fontSize: 10, color: p.clr, fontFace: "Microsoft YaHei", lineSpacing: 18 });
      s.addShape("ellipse", { x: x + 2.45, y: 2.0, w: 0.4, h: 0.4, fill: { color: p.clr } });
      s.addText(String(i + 1), { x: x + 2.45, y: 2.0, w: 0.4, h: 0.4, fontSize: 14, bold: true, color: P.accent, fontFace: "Microsoft YaHei", align: "center" });
    });
  }

  // ========== S6: 核心技术 ==========
  {
    const s = pptx.addSlide();
    s.background = { color: P.lightBg };
    addTitleBar(s, "核心技术：多模态情绪识别引擎");

    const layers = [
      { name: "感知层", items: ["语音情绪识别", "视觉表情分析", "生理信号采集", "环境多模态传感"], y: 1.3, clr: P.primary },
      { name: "理解层", items: ["情感计算引擎", "DeepSeek大模型", "用户画像构建", "场景意图推理"], y: 3.2, clr: P.orange },
      { name: "响应层", items: ["自适应环境调控", "共情对话生成", "主动关怀策略", "智能场景联动"], y: 5.1, clr: P.teal },
    ];

    layers.forEach((l) => {
      // 层标签
      s.addShape("roundRect", { x: 0.5, y: l.y, w: 1.5, h: 1.5, fill: { color: l.clr }, rectRound: 0.12 });
      s.addText(l.name, { x: 0.5, y: l.y + 0.4, w: 1.5, h: 0.7, fontSize: 17, bold: true, color: P.accent, fontFace: "Microsoft YaHei", align: "center" });
      // 技术项 - 2行 x 2列
      l.items.forEach((item, j) => {
        const col = j % 2;
        const row = Math.floor(j / 2);
        const cx = 2.4 + col * 5.3;
        const cy = l.y + row * 0.8;
        s.addShape("roundRect", { x: cx, y: cy, w: 5.0, h: 0.65, fill: { color: P.accent }, rectRound: 0.08, shadow: { type: "outer", blur: 3, offset: 1, color: "000000", opacity: 0.06 } });
        // 编号
        const num = j + 1;
        const hexNum = String.fromCodePoint(0x2775 + j);
        const numChars = ["\u{2780}", "\u{2781}", "\u{2782}", "\u{2783}"];
        s.addShape("ellipse", { x: cx + 0.1, y: cy + 0.1, w: 0.4, h: 0.45, fill: { color: l.clr, transparency: 18 } });
        s.addText(numChars[j], { x: cx + 0.1, y: cy + 0.1, w: 0.4, h: 0.45, fontSize: 14, color: l.clr, fontFace: "Microsoft YaHei", align: "center" });
        s.addText(item, { x: cx + 0.6, y: cy + 0.05, w: 4.2, h: 0.55, fontSize: 14, color: P.primary, fontFace: "Microsoft YaHei" });
      });
    });

    // 箭头连接
    s.addText("\u{25BC}", { x: 1.1, y: 2.85, w: 0.3, h: 0.3, fontSize: 14, color: P.gray, align: "center" });
    s.addText("\u{25BC}", { x: 1.1, y: 4.75, w: 0.3, h: 0.3, fontSize: 14, color: P.gray, align: "center" });
  }

  // ========== S7: 应用场景 ==========
  {
    const s = pptx.addSlide();
    s.background = { color: P.accent };
    addTitleBar(s, "应用场景：四大情绪生活场景");

    const scenes = [
      { title: "下班回家", emoji: "\u{1F3E0}", desc: "空调通过语音情绪检测识别疲惫\n自动切换"舒压模式"\n释放薰衣草香薰\n播放舒缓白噪音", clr: P.primary },
      { title: "深夜难眠", emoji: "\u{1F4A4}", desc: "睡眠系统感知睡前焦虑情绪\n联动调节灯光色温至暖黄\n播放引导冥想音频\n智能调控卧室温湿度", clr: P.teal },
      { title: "独自用餐", emoji: "\u{1F372}", desc: "陪伴音箱主动开启聊天模式\n根据心情推荐食谱与音乐\n营造温馨用餐氛围\n让独处也变得温暖", clr: P.orange },
      { title: "家庭互动", emoji: "\u{1F46A}", desc: "家庭情绪中枢显示各成员情绪\n当检测到家人情绪低落\n主动建议互动活动\n促进家庭成员情感连接", clr: P.primary },
    ];

    scenes.forEach((sc, i) => {
      const x = 0.3 + i * 3.25;
      addCard(s, x, 1.3, 3.05, 5.6);
      s.addShape("rect", { x, y: 1.3, w: 3.05, h: 0.8, fill: { color: sc.clr, transparency: 90 }, rectRound: 0.1 });
      s.addText(sc.emoji, { x: x + 0.15, y: 1.35, w: 0.6, h: 0.7, fontSize: 28, align: "center" });
      s.addText(sc.title, { x: x + 0.75, y: 1.4, w: 2.1, h: 0.6, fontSize: 17, bold: true, color: P.dark, fontFace: "Microsoft YaHei" });
      s.addShape("rect", { x: x + 0.2, y: 2.3, w: 2.65, h: 0.03, fill: { color: sc.clr, transparency: 60 } });
      s.addText(sc.desc, { x: x + 0.2, y: 2.55, w: 2.65, h: 3.8, fontSize: 13, color: P.gray, fontFace: "Microsoft YaHei", lineSpacing: 36 });
    });
  }

  // ========== S8: 商业模式 ==========
  {
    const s = pptx.addSlide();
    s.background = { color: P.lightBg };
    addTitleBar(s, "商业模式与竞争优势");

    // 商业模式 - 左侧
    s.addShape("roundRect", { x: 0.5, y: 1.2, w: 6.0, h: 0.55, fill: { color: P.primary }, rectRound: 0.08 });
    s.addText("商业模式", { x: 0.5, y: 1.23, w: 6.0, h: 0.5, fontSize: 16, bold: true, color: P.accent, fontFace: "Microsoft YaHei", align: "center" });

    const bizItems = [
      { label: "硬件销售", desc: "情绪感知系列家电产品直销，高毛利定价策略" },
      { label: "订阅服务", desc: "情绪健康报告/个性关怀方案 月费制会员服务" },
      { label: "数据增值", desc: "脱敏情绪数据赋能产品研发与精准营销" },
      { label: "生态分成", desc: "与香薰/音乐/冥想等内容服务商平台分成" },
    ];
    bizItems.forEach((b, i) => {
      const y = 1.95 + i * 1.15;
      addCard(s, 0.5, y, 6.0, 1.0);
      s.addShape("roundRect", { x: 0.7, y: y + 0.2, w: 0.6, h: 0.6, fill: { color: P.orange, transparency: 20 }, rectRound: 0.1 });
      s.addText(String(i + 1), { x: 0.7, y: y + 0.22, w: 0.6, h: 0.55, fontSize: 16, bold: true, color: P.orange, fontFace: "Microsoft YaHei", align: "center" });
      s.addText(b.label, { x: 1.5, y: y + 0.08, w: 4.8, h: 0.35, fontSize: 15, bold: true, color: P.primary, fontFace: "Microsoft YaHei" });
      s.addText(b.desc, { x: 1.5, y: y + 0.45, w: 4.8, h: 0.4, fontSize: 12, color: P.gray, fontFace: "Microsoft YaHei" });
    });

    // 竞争优势 - 右侧
    s.addShape("roundRect", { x: 7.0, y: 1.2, w: 5.83, h: 0.55, fill: { color: P.orange }, rectRound: 0.08 });
    s.addText("核心竞争优势", { x: 7.0, y: 1.23, w: 5.83, h: 0.5, fontSize: 16, bold: true, color: P.accent, fontFace: "Microsoft YaHei", align: "center" });

    const advItems = [
      { title: "先发优势", desc: "家电行业率先系统化布局情绪价值赛道，抢占用户心智" },
      { title: "技术壁垒", desc: "自研多模态情绪识别引擎+海尔DeepSeek融合，精准度业界领先" },
      { title: "生态协同", desc: "依托海尔智慧家庭完整产品矩阵，实现全屋情绪感知无缝联动" },
      { title: "数据飞轮", desc: "海量用户情绪数据反哺模型迭代，越用越准，形成持续竞争优势" },
    ];
    advItems.forEach((a, i) => {
      const y = 1.95 + i * 1.15;
      addCard(s, 7.0, y, 5.83, 1.0);
      s.addText(a.title, { x: 7.2, y: y + 0.08, w: 5.4, h: 0.35, fontSize: 15, bold: true, color: P.orange, fontFace: "Microsoft YaHei" });
      s.addText(a.desc, { x: 7.2, y: y + 0.45, w: 5.4, h: 0.4, fontSize: 12, color: P.gray, fontFace: "Microsoft YaHei" });
    });
  }

  // ========== S9: 实施路线图 ==========
  {
    const s = pptx.addSlide();
    s.background = { color: P.primary };
    s.addShape("rect", { x: 0, y: 0, w: 13.33, h: 0.06, fill: { color: P.orange } });
    s.addText("实施路线图", { x: 0.8, y: 0.3, w: 11, h: 0.7, fontSize: 28, bold: true, color: P.accent, fontFace: "Microsoft YaHei" });
    s.addShape("rect", { x: 0.8, y: 0.95, w: 1.5, h: 0.04, fill: { color: P.orange } });

    const phases = [
      {
        phase: "Phase 1", time: "2026 Q3-Q4", title: "MVP验证",
        items: [
          "完成情绪感知空调原型机开发",
          "搭建多模态情绪数据采集系统",
          "招募100名种子用户内测",
          "验证核心情绪识别准确率达85%+",
        ]
      },
      {
        phase: "Phase 2", time: "2027 H1", title: "产品化",
        items: [
          "情绪感知空调正式量产上市",
          "推出智能陪伴音箱V1.0",
          "接入海尔智家App生态",
          "完成第一轮市场反馈迭代",
        ]
      },
      {
        phase: "Phase 3", time: "2027 H2", title: "生态扩展",
        items: [
          "智能睡眠系统 + 家庭情绪中枢上线",
          "开放情绪数据API，引入内容服务商",
          "覆盖10万+家庭，营收突破5亿",
          "启动海外市场（东南亚/中东）试点",
        ]
      },
    ];

    phases.forEach((p, i) => {
      const x = 0.5 + i * 4.2;
      addCard(s, x, 1.3, 3.9, 5.2);
      // 阶段头
      s.addShape("rect", { x, y: 1.3, w: 3.9, h: 0.8, fill: { color: P.orange, transparency: 70 }, rectRound: 0.1 });
      s.addText(p.phase, { x: x + 0.2, y: 1.35, w: 1.5, h: 0.4, fontSize: 12, color: P.orange, fontFace: "Microsoft YaHei" });
      s.addText(p.title, { x: x + 0.2, y: 1.6, w: 3.5, h: 0.45, fontSize: 22, bold: true, color: P.accent, fontFace: "Microsoft YaHei" });
      // 时间标签
      s.addShape("roundRect", { x: x + 2.6, y: 1.4, w: 1.15, h: 0.35, fill: { color: P.accent, transparency: 85 }, rectRound: 0.06 });
      s.addText(p.time, { x: x + 2.6, y: 1.4, w: 1.15, h: 0.35, fontSize: 10, bold: true, color: P.accent, fontFace: "Microsoft YaHei", align: "center" });
      // 任务列表
      p.items.forEach((item, j) => {
        const cy = 2.4 + j * 0.85;
        s.addShape("ellipse", { x: x + 0.3, y: cy + 0.15, w: 0.2, h: 0.2, fill: { color: P.orange } });
        s.addText(item, { x: x + 0.65, y: cy, w: 3.0, h: 0.6, fontSize: 12, color: P.secondary, fontFace: "Microsoft YaHei", lineSpacing: 18 });
      });
    });

    // 团队信息
    s.addText("团队配置：产品经理1人 + AI算法工程师2人 + 硬件工程师2人 + UI/UX设计师1人 + 市场1人 = 6-9人", { x: 0.5, y: 6.8, w: 12, h: 0.4, fontSize: 12, color: P.secondary, fontFace: "Microsoft YaHei", align: "center" });
  }

  // ========== S10: 致谢 ==========
  {
    const s = pptx.addSlide();
    s.background = { color: P.primary };
    s.addShape("rect", { x: 0, y: 0, w: 13.33, h: 0.06, fill: { color: P.orange } });
    s.addShape("rect", { x: 0, y: 7.0, w: 13.33, h: 0.5, fill: { color: P.orange, transparency: 80 } });
    // 装饰
    s.addShape("rect", { x: 5.5, y: 1.8, w: 2.33, h: 0.04, fill: { color: P.orange } });
    s.addText("谢谢聆听", { x: 2, y: 2.2, w: 9.33, h: 1.2, fontSize: 48, bold: true, color: P.accent, fontFace: "Microsoft YaHei", align: "center" });
    s.addText("心有灵犀——让家电读懂你的心", { x: 2, y: 3.5, w: 9.33, h: 0.6, fontSize: 18, color: P.secondary, fontFace: "Microsoft YaHei", align: "center" });
    s.addShape("rect", { x: 5.5, y: 4.3, w: 2.33, h: 0.04, fill: { color: P.orange } });
    s.addText("海尔智家 | 创无限 · AI无界 | 让创想无界产品创意大赛", { x: 2, y: 4.7, w: 9.33, h: 0.5, fontSize: 13, color: P.secondary, fontFace: "Microsoft YaHei", align: "center" });
    s.addText("知识产权声明：本项目为原创方案，参加海尔智家2026"创无限·AI无界"创新大赛", { x: 2, y: 5.5, w: 9.33, h: 0.5, fontSize: 11, color: P.secondary, fontFace: "Microsoft YaHei", align: "center" });
  }

  // 保存
  const outputPath = path.join(__dirname, "心有灵犀_AI情绪感知智能家电_路演PPT.pptx");
  await pptx.writeFile({ fileName: outputPath });
  console.log("Done: " + outputPath);
}

main().catch(console.error);