#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""情绪冰仓·黑马大赛路演PPT生成脚本"""

from pptx import Presentation
from pptx.util import Inches, Pt, Emu, Cm
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.dml.color import RGBColor
from pptx.oxml.ns import qn
import os

# ===== 配色方案 =====
P = {
    "primary": RGBColor(0x1B, 0x3A, 0x4B),
    "secondary": RGBColor(0xE8, 0x6A, 0x4D),
    "accent": RGBColor(0xF5, 0xB0, 0x41),
    "light": RGBColor(0xF8, 0xF6, 0xF0),
    "dark": RGBColor(0x1E, 0x1E, 0x1E),
    "ice": RGBColor(0xCF, 0xE0, 0xE8),
    "grey": RGBColor(0x7F, 0x8C, 0x8D),
    "white": RGBColor(0xFF, 0xFF, 0xFF),
    "green": RGBColor(0x27, 0xAE, 0x60),
    "red": RGBColor(0xE7, 0x4C, 0x3C),
}
FONT = "Microsoft YaHei"
PAGE_W = Cm(33.867)  # 13.33 inches
PAGE_H = Cm(19.05)   # 7.5 inches

# ===== 辅助函数 =====
def set_bg(slide, color):
    """设置幻灯片背景色"""
    bg = slide.background
    fill = bg.fill
    fill.solid()
    fill.fore_color.rgb = color

def add_rect(slide, x, y, w, h, fill_color, round_corners=False):
    """添加矩形"""
    shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE if round_corners else MSO_SHAPE.RECTANGLE, Cm(x), Cm(y), Cm(w), Cm(h))
    shape.fill.solid()
    shape.fill.fore_color.rgb = fill_color
    shape.line.fill.background()
    return shape

def add_textbox(slide, x, y, w, h, text, font_size=12, color=None, bold=False, align=PP_ALIGN.LEFT, font=FONT, valign=MSO_ANCHOR.TOP):
    """添加文本框"""
    txBox = slide.shapes.add_textbox(Cm(x), Cm(y), Cm(w), Cm(h))
    txBox.text_frame.word_wrap = True
    tf = txBox.text_frame
    tf.auto_size = None
    p = tf.paragraphs[0]
    p.text = text
    p.font.size = Pt(font_size)
    p.font.name = font
    p.font.bold = bold
    p.alignment = align
    if color:
        p.font.color.rgb = color
    # Set vertical anchor
    txBox.text_frame.paragraphs[0].font.name = font
    try:
        tfPr = txBox.text_frame._txBody.find(qn('a:bodyPr'))
        if tfPr is not None:
            v_map = {MSO_ANCHOR.TOP: 't', MSO_ANCHOR.MIDDLE: 'ctr', MSO_ANCHOR.BOTTOM: 'b'}
            tfPr.set('anchor', v_map.get(valign, 't'))
    except:
        pass
    return txBox

def add_multiline_textbox(slide, x, y, w, h, lines, font_size=11, color=None, bold=False, line_spacing=1.3):
    """添加多行文本框"""
    txBox = slide.shapes.add_textbox(Cm(x), Cm(y), Cm(w), Cm(h))
    txBox.text_frame.word_wrap = True
    tf = txBox.text_frame
    tf.auto_size = None
    for i, line in enumerate(lines):
        if i == 0:
            p = tf.paragraphs[0]
        else:
            p = tf.add_paragraph()
        p.text = line
        p.font.size = Pt(font_size)
        p.font.name = FONT
        p.font.bold = bold
        if color:
            p.font.color.rgb = color
        p.space_after = Pt(2)
    return txBox

def add_section_header(slide, number, title):
    """添加统一的章节头部"""
    add_rect(slide, 0, 0, 33.867, 3.048, P["primary"])
    add_textbox(slide, 2.0, 0.5, 25, 2.0, f"{number}  {title}", font_size=24, color=P["white"], bold=True)

def add_ellipse_bullet(slide, x, y, text, font_size=11, color=P["dark"], bullet_color=P["secondary"]):
    """添加带圆点符号的文本"""
    shape = slide.shapes.add_shape(MSO_SHAPE.OVAL, Cm(x), Cm(y + 0.1), Cm(0.35), Cm(0.35))
    shape.fill.solid()
    shape.fill.fore_color.rgb = bullet_color
    shape.line.fill.background()
    add_textbox(slide, x + 0.55, y, 13, 1.0, text, font_size=font_size, color=color)

def make_table(slide, x, y, w, rows, col_widths, row_heights, header_color=P["primary"]):
    """创建表格"""
    n_rows = len(rows)
    n_cols = len(rows[0])
    table_shape = slide.shapes.add_table(n_rows, n_cols, Cm(x), Cm(y), Cm(w), Cm(sum(row_heights)))
    table = table_shape.table
    for ci, cw in enumerate(col_widths):
        table.columns[ci].width = Cm(cw)
    for ri, rh in enumerate(row_heights):
        table.rows[ri].height = Cm(rh)
    for ri, row in enumerate(rows):
        for ci, cell_data in enumerate(row):
            cell = table.cell(ri, ci)
            cell.text = ""
            p = cell.text_frame.paragraphs[0]
            p.text = cell_data.get("text", "")
            p.font.size = Pt(cell_data.get("font_size", 10))
            p.font.name = FONT
            p.font.bold = cell_data.get("bold", False)
            p.alignment = cell_data.get("align", PP_ALIGN.CENTER)
            opts = cell_data.get("options", {})
            if opts.get("color"):
                p.font.color.rgb = opts["color"]
            elif "color" in cell_data:
                p.font.color.rgb = cell_data["color"]
            else:
                p.font.color.rgb = P["dark"]
            # Cell fill
            fill_color = cell_data.get("fill_color", None)
            if fill_color:
                cell.fill.solid()
                cell.fill.fore_color.rgb = fill_color
            # Vertical alignment
            cell.vertical_anchor = MSO_ANCHOR.MIDDLE
    return table_shape

def add_circle_num(slide, x, y, num, fill_color, size=0.7):
    """添加圆形数字标记"""
    shape = slide.shapes.add_shape(MSO_SHAPE.OVAL, Cm(x), Cm(y), Cm(size), Cm(size))
    shape.fill.solid()
    shape.fill.fore_color.rgb = fill_color
    shape.line.fill.background()
    tf = shape.text_frame
    tf.word_wrap = False
    p = tf.paragraphs[0]
    p.text = str(num)
    p.font.size = Pt(14)
    p.font.name = FONT
    p.font.bold = True
    p.font.color.rgb = P["white"]
    p.alignment = PP_ALIGN.CENTER
    tf.paragraphs[0].alignment = PP_ALIGN.CENTER
    return shape

# ===== 主函数 =====
def create_ppt():
    prs = Presentation()
    prs.slide_width = PAGE_W
    prs.slide_height = PAGE_H

    # ===== Slide 1: 封面 =====
    slide = prs.slides.add_slide(prs.slide_layouts[6])  # blank layout
    set_bg(slide, P["primary"])
    add_rect(slide, 0, 0, 33.867, 0.2, P["accent"])
    add_rect(slide, 0, 18.85, 33.867, 0.2, P["accent"])
    add_rect(slide, 2.0, 3.8, 0.15, 7.1, P["secondary"])
    add_textbox(slide, 3.0, 3.8, 25, 3.5, "情绪冰仓", font_size=54, color=P["white"], bold=True)
    add_textbox(slide, 3.0, 7.3, 25, 2.0, "一杯饮尽松弛感", font_size=28, color=P["accent"])
    add_textbox(slide, 3.0, 9.6, 25, 1.5, "黑马大赛商业路演方案", font_size=16, color=P["ice"])
    add_textbox(slide, 3.0, 14.0, 25, 1.3, "2026年7月  |  海尔制冷·情绪冰仓项目组", font_size=13, color=P["grey"])

    # ===== Slide 2: 目录 =====
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_bg(slide, P["light"])
    add_rect(slide, 0, 0, 33.867, 0.15, P["primary"])
    add_textbox(slide, 2.0, 1.0, 12, 1.8, "目录", font_size=30, color=P["primary"], bold=True)
    add_rect(slide, 2.0, 2.9, 3.8, 0.1, P["secondary"])

    toc_items = [
        ("01", "项目背景与市场机会", "年轻人冰饮需求与情绪消费趋势"),
        ("02", "用户洞察与场景分析", "目标用户画像与核心消费场景"),
        ("03", "竞品分析与市场缺口", "现有冰吧产品的不足与我们的机会"),
        ("04", "产品设计与创新亮点", "四大核心功能 + 智能化增强层"),
        ("05", "场景-功能-情绪模式映射", "四模情绪切换与场景联动"),
        ("06", "技术架构与实现路径", "七大技术系统与可行性"),
        ("07", "商业模式与营销策略", "盈利模式、渠道策略与品牌传播"),
        ("08", "财务分析", "成本结构、收入预测与融资方案"),
        ("09", "风险评估与退出机制", "风险识别与应对策略"),
        ("10", "团队架构与推进计划", "核心团队与关键里程碑"),
    ]
    for i, (num, title, desc) in enumerate(toc_items):
        col = 2.0 if i < 5 else 17.5
        j = i if i < 5 else i - 5
        yy = 3.8 + j * 1.45
        add_rect(slide, col, yy, 1.4, 1.05, P["primary"], round_corners=True)
        add_textbox(slide, col, yy, 1.4, 1.05, num, font_size=13, color=P["white"], bold=True, align=PP_ALIGN.CENTER, valign=MSO_ANCHOR.MIDDLE)
        add_textbox(slide, col + 1.8, yy - 0.05, 11.5, 0.7, title, font_size=13, color=P["dark"], bold=True)
        add_textbox(slide, col + 1.8, yy + 0.6, 11.5, 0.55, desc, font_size=10, color=P["grey"])

    # ===== Slide 3: 项目背景与市场机会 =====
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_bg(slide, P["white"])
    add_section_header(slide, "01", "项目背景与市场机会")

    cards = [
        ("4.2亿", "中国Z世代人口", "核心目标消费群体"),
        ("68%", "愿意为情绪价值付费", "悦己消费成为主流趋势"),
        ("35%", "冰吧品类年增速", "远高于传统冰箱增速"),
    ]
    for i, (num, label, sub) in enumerate(cards):
        cx = 2.0 + i * 10.4
        add_rect(slide, cx, 3.8, 9.6, 5.0, P["light"], round_corners=True)
        add_textbox(slide, cx, 4.0, 9.6, 2.0, num, font_size=32, color=P["secondary"], bold=True, align=PP_ALIGN.CENTER)
        add_textbox(slide, cx, 5.8, 9.6, 1.1, label, font_size=14, color=P["dark"], bold=True, align=PP_ALIGN.CENTER)
        add_textbox(slide, cx, 6.8, 9.6, 1.0, sub, font_size=11, color=P["grey"], align=PP_ALIGN.CENTER)

    add_textbox(slide, 2.0, 9.6, 30, 1.3, "三大趋势驱动情绪冰仓需求", font_size=16, color=P["primary"], bold=True)
    trends = [
        "生活方式升级：年轻人冷饮需求从解渴上升为生活仪式，需要场景依赖的精细化、高品质冰饮存储",
        "情绪消费崛起：悦己消费成为主流，"松弛感、解压、氛围感、仪式感"成为核心购买驱动力",
        "冰吧品类蓝海：冰吧并非概念空白，是一个已有成交但仍缺少面向年轻情绪场景产品的细分市场",
    ]
    for i, t in enumerate(trends):
        add_ellipse_bullet(slide, 2.0, 11.0 + i * 1.65, t, font_size=12, color=P["dark"])

    add_textbox(slide, 2.0, 16.8, 30, 1.0, "数据来源：即时零售冰品酒饮消费洞察报告2025、2026中国食品饮料十大趋势、小红书平台冰吧相关笔记分析", font_size=9, color=P["grey"])

    # ===== Slide 4: 用户洞察与场景分析 =====
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_bg(slide, P["white"])
    add_section_header(slide, "02", "用户洞察与场景分析")

    add_textbox(slide, 2.0, 3.8, 15, 1.3, "核心用户画像", font_size=16, color=P["primary"], bold=True)
    personas = [
        ("独居/租房青年", "追求生活品质，小空间也能精致生活，冰吧是"家的仪式感"入口"),
        ("社交型小两口", "经常在家招待朋友，酒饮/调酒/冷饮需求高频，冰吧是社交场景核心设备"),
        ("运动/养生青年", "运动后补水补能、熬夜后补给，对功能饮料、电解质水有精准温控需求"),
        ("沉浸式娱乐爱好者", "看球、电竞、追剧等场景，需要快速取用冰饮，氛围感烘托观影体验"),
    ]
    for i, (title, desc) in enumerate(personas):
        py = 5.3 + i * 2.15
        add_rect(slide, 2.0, py, 14.0, 1.75, P["light"], round_corners=True)
        add_rect(slide, 2.0, py, 0.15, 1.75, P["secondary"])
        add_textbox(slide, 2.8, py + 0.12, 12.5, 0.75, title, font_size=12, color=P["primary"], bold=True)
        add_textbox(slide, 2.8, py + 0.9, 12.5, 0.75, desc, font_size=10, color=P["grey"])

    add_textbox(slide, 18.3, 3.8, 14, 1.3, "核心消费场景（小红书高频词）", font_size=16, color=P["primary"], bold=True)
    scenarios = [
        ("夏天", "最高频"), ("追剧", "高频"), ("运动", "高频"), ("宅家", "高频"),
        ("客厅", "高频"), ("聚会", "中频"), ("电竞", "中频"), ("微醺", "中频"),
    ]
    for i, (word, freq) in enumerate(scenarios):
        col = 18.3 + (i % 2) * 7.1
        row = i // 2
        sy = 5.3 + row * 2.15
        is_top = freq == "最高频"
        bg_c = P["secondary"] if is_top else P["light"]
        txt_c = P["white"] if is_top else P["dark"]
        sub_c = P["white"] if is_top else P["grey"]
        add_rect(slide, col, sy, 6.35, 1.75, bg_c, round_corners=True)
        add_textbox(slide, col, sy + 0.12, 6.35, 0.9, word, font_size=14, color=txt_c, bold=True, align=PP_ALIGN.CENTER)
        add_textbox(slide, col, sy + 0.95, 6.35, 0.6, freq, font_size=10, color=sub_c, align=PP_ALIGN.CENTER)

    add_textbox(slide, 18.3, 14.2, 14, 2.5, "场景洞察：冰饮需求集中在降温放松、追剧/赛事陪伴、运动后恢复、朋友小聚这几类时刻。用户需要快速拿取、清楚分类、视觉展示和即时可喝状态。", font_size=11, color=P["dark"])

    # ===== Slide 5: 竞品分析 =====
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_bg(slide, P["white"])
    add_section_header(slide, "03", "竞品分析与市场缺口")

    # Table data
    headers = ["维度", "传统冰吧", "卡萨帝冰吧", "哈士奇冰吧", "情绪冰仓（我们）"]
    rows_data = [
        ["温控精度", "粗糙 ±3°C", "电子 ±1°C", "电子 ±1°C", "多温区 ±0.5°C"],
        ["氛围灯光", "无/单色", "单色", "无", "RGB情绪模式+音乐律动"],
        ["可视化分区", "无", "基础", "透明窗", "色温分区+透视窗+标签"],
        ["电控调光玻璃", "无", "无", "无", "APP一键雾化"],
        ["智能库存识别", "无", "无", "无", "AI酒标识别+到期提醒"],
        ["家居融合设计", "一般", "较好", "复古风格", "可换面板+嵌入+黄金比例"],
        ["静音水平", "40dB+", "38dB", "38dB", "≤28dB 夜间≤22dB"],
        ["情绪交互", "无", "无", "无", "触控屏+语音+情绪模式"],
    ]

    n_rows = len(rows_data) + 1
    n_cols = len(headers)
    tbl_shape = slide.shapes.add_table(n_rows, n_cols, Cm(2.0), Cm(3.8), Cm(29.8), Cm(0.5 * n_rows))
    tbl = tbl_shape.table
    col_ws = [5.0, 4.5, 5.0, 5.0, 10.3]
    for ci, cw in enumerate(col_ws):
        tbl.columns[ci].width = Cm(cw)

    # Header row
    for ci, h in enumerate(headers):
        cell = tbl.cell(0, ci)
        cell.text = ""
        p = cell.text_frame.paragraphs[0]
        p.text = h
        p.font.size = Pt(11)
        p.font.name = FONT
        p.font.bold = True
        p.font.color.rgb = P["white"]
        p.alignment = PP_ALIGN.CENTER
        cell.fill.solid()
        cell.fill.fore_color.rgb = P["primary"]
        cell.vertical_anchor = MSO_ANCHOR.MIDDLE

    # Data rows
    for ri, row in enumerate(rows_data):
        for ci, val in enumerate(row):
            cell = tbl.cell(ri + 1, ci)
            cell.text = ""
            p = cell.text_frame.paragraphs[0]
            p.text = val
            p.font.size = Pt(10)
            p.font.name = FONT
            p.alignment = PP_ALIGN.CENTER
            cell.vertical_anchor = MSO_ANCHOR.MIDDLE
            if ci == 4:  # Our column
                p.font.color.rgb = P["secondary"]
                p.font.bold = True
            else:
                p.font.color.rgb = P["dark"]
            if ri % 2 == 0:
                cell.fill.solid()
                cell.fill.fore_color.rgb = P["light"]

    add_textbox(slide, 2.0, 16.0, 30, 1.8, "市场缺口：现有冰吧产品普遍缺乏"情绪价值"设计，没有针对年轻人情绪场景的专属产品。我们的机会在于将冰吧从"功能设备"升级为"情绪家具"。", font_size=12, color=P["primary"], bold=True)

    # ===== Slide 6: 产品设计 =====
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_bg(slide, P["white"])
    add_section_header(slide, "04", "产品设计与创新亮点")

    features = [
        ("01", "可视化分区", "三色温LED分区照明\n透明玻璃层架+45°透视抽屉\n磁吸标签+阶梯式门搁架\n3秒定位，减少翻找40%", P["secondary"]),
        ("02", "低噪夜间体验", "磁悬浮变频压缩机 ≤28dB\n夜间模式 ≤22dB\n软启动/软停机零冲击音\n底部2700K暖光氛围灯", P["accent"]),
        ("03", "DIY小料/冰杯适配", "模块化托盘+酱料格\n304不锈钢冰杯速冷抽屉\n风味冰块DIY水盒\n磁性侧壁+快拆门搁架", P["green"]),
        ("04", "家居化外观", "4种面板可选（木纹/岩板）\nR8圆角+无拉手极简\n3:2黄金比例+嵌入式踢脚线\n顶部置物台面承重30kg", P["primary"]),
    ]
    for i, (icon, title, desc, color) in enumerate(features):
        fx = 2.0 + i * 7.8
        add_rect(slide, fx, 3.8, 7.0, 7.5, P["light"], round_corners=True)
        add_rect(slide, fx + 0.6, 4.3, 1.5, 1.5, color, round_corners=True)
        add_textbox(slide, fx + 0.6, 4.3, 1.5, 1.5, icon, font_size=16, color=P["white"], bold=True, align=PP_ALIGN.CENTER, valign=MSO_ANCHOR.MIDDLE)
        add_textbox(slide, fx + 2.5, 4.4, 4.0, 1.3, title, font_size=15, color=P["dark"], bold=True)
        add_multiline_textbox(slide, fx + 0.6, 6.3, 5.8, 4.5, desc.split("\n"), font_size=10, color=P["grey"])

    add_textbox(slide, 2.0, 12.2, 30, 1.3, "智能化增强层（不喧宾夺主）", font_size=16, color=P["primary"], bold=True)
    smart_feats = [
        "极简触控屏：门板嵌入，低调不突兀，支持情绪模式一键切换",
        "语音交互：顶部微光指示灯，轻声提醒（门未关/长开门预警），不打扰",
        "电控调光玻璃：APP一键切换透明/雾化，保护藏酒隐私+展示切换",
        "AI库存识别：柜内摄像头+云端酒标比对，到期提醒+智能推荐",
    ]
    for i, sf in enumerate(smart_feats):
        sx = 2.0 + (i % 2) * 15.5
        sy = 13.8 + (i // 2) * 1.4
        add_ellipse_bullet(slide, sx, sy, sf, font_size=11, color=P["dark"], bullet_color=P["accent"])

    # ===== Slide 7: 场景-模式映射 =====
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_bg(slide, P["white"])
    add_section_header(slide, "05", "场景-功能-情绪模式映射")

    modes = [
        ("微醺模式", "独处/约会小酌", "红葡12°C/白葡8°C", "暖琥珀色呼吸灯", P["secondary"]),
        ("冰爽模式", "运动后/夏日降温", "饮料3°C快速制冷", "冰蓝色流动光效", RGBColor(0x29, 0x80, 0xB9)),
        ("养生模式", "熬夜补给/日常调理", "功能饮5°C/面膜2°C", "暖白柔和常亮光", P["green"]),
        ("派对模式", "朋友聚会/看球电竞", "啤酒4°C/冰杯-18°C", "RGB音乐律动灯光", RGBColor(0x8E, 0x44, 0xAD)),
    ]
    for i, (name, scene, temp, light, color) in enumerate(modes):
        mx = 2.0 + i * 7.8
        add_rect(slide, mx, 3.8, 7.0, 9.5, P["light"], round_corners=True)
        add_rect(slide, mx, 3.8, 7.0, 1.8, color, round_corners=True)
        add_textbox(slide, mx, 3.8, 7.0, 1.8, name, font_size=16, color=P["white"], bold=True, align=PP_ALIGN.CENTER, valign=MSO_ANCHOR.MIDDLE)
        details = [f"场景：{scene}", f"温控：{temp}", f"灯光：{light}"]
        for j, d in enumerate(details):
            add_textbox(slide, mx + 0.5, 6.2 + j * 1.4, 6.0, 1.1, d, font_size=10, color=P["dark"])

    add_textbox(slide, 2.0, 14.2, 30, 1.5, "一键切换：用户可通过门板触控屏或手机APP一键切换情绪模式，灯光、温度、氛围同步匹配，实现"一杯饮尽松弛感"的完整体验。", font_size=12, color=P["primary"], bold=True)

    # Mapping table
    add_textbox(slide, 2.0, 15.7, 15, 1.0, "场景-功能-分类映射", font_size=14, color=P["primary"], bold=True)
    mapping_rows = [
        [{"text": "场景需求", "font_size": 10, "bold": True, "color": P["white"], "fill_color": P["primary"]},
         {"text": "功能分类", "font_size": 10, "bold": True, "color": P["white"], "fill_color": P["primary"]},
         {"text": "核心实现", "font_size": 10, "bold": True, "color": P["white"], "fill_color": P["primary"]}],
        [{"text": "最佳口感", "font_size": 10}, {"text": "分温精储", "font_size": 10}, {"text": "多温区独立风道+风门精确控制", "font_size": 10}],
        [{"text": "氛围感/出片", "font_size": 10}, {"text": "空间氛围", "font_size": 10}, {"text": "RGB氛围灯+透明视窗+电控调光", "font_size": 10}],
        [{"text": "情绪满足", "font_size": 10}, {"text": "情绪模式", "font_size": 10}, {"text": "一键切换微醺/冰爽/养生/派对模式", "font_size": 10}],
        [{"text": "仪式感/便利", "font_size": 10}, {"text": "高频顺手", "font_size": 10}, {"text": "模块化托盘+快拆搁架+可视化分区", "font_size": 10}],
    ]
    make_table(slide, 2.0, 16.6, 29.8, mapping_rows, [6.3, 6.3, 17.2], [0.5, 0.45, 0.45, 0.45, 0.45])

    # ===== Slide 8: 技术架构 =====
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_bg(slide, P["white"])
    add_section_header(slide, "06", "技术架构与实现路径")

    techs = [
        ("1", "智能氛围灯光系统", "RGBW LED灯珠+独立MCU驱动，APP调色盘+音乐律动+情绪模式联动"),
        ("2", "电控调光玻璃", "三层夹胶玻璃+调光膜，断电自动雾化，Wi-Fi远程遥控切换"),
        ("3", "AI智能库存识别", "低功耗广角摄像头+云端酒标比对，到期提醒+智能推荐+APP可视化"),
        ("4", "精细化多温区", "多风道独立送风+步进电机风门，冷藏/微冻/暖藏三区独立控温"),
        ("5", "静音与减震系统", "变频压缩机+磁悬浮轴承+多重减震阻尼，橡木酒架吸振"),
        ("6", "家居融合模块化", "底部散热+标准模数搁架+可拆卸磁吸面板，自由嵌入+多材质可选"),
        ("7", "UVC除菌净化", "离子杀菌模块+抗菌门条+干湿分离+HCS生态膜隔离"),
    ]
    for i, (num, title, desc) in enumerate(techs):
        col = 2.0 + (i % 2) * 15.5
        row = i // 2
        ty = 3.8 + row * 2.0
        add_rect(slide, col, ty, 1.1, 1.1, P["primary"], round_corners=True)
        add_textbox(slide, col, ty, 1.1, 1.1, num, font_size=14, color=P["white"], bold=True, align=PP_ALIGN.CENTER, valign=MSO_ANCHOR.MIDDLE)
        add_textbox(slide, col + 1.5, ty - 0.05, 12.5, 0.75, title, font_size=12, color=P["primary"], bold=True)
        add_textbox(slide, col + 1.5, ty + 0.7, 12.5, 0.9, desc, font_size=10, color=P["grey"])

    add_textbox(slide, 2.0, 16.5, 30, 1.5, "技术可行性：以上七项技术均基于成熟方案，核心硬件（LED驱动、调光膜、变频压缩机、NTC温控）供应链完善，软件端（APP、云端识别）可复用现有IoT平台能力。", font_size=12, color=P["primary"], bold=True)

    # ===== Slide 9: 商业模式 =====
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_bg(slide, P["white"])
    add_section_header(slide, "07", "商业模式与营销策略")

    # Pricing
    add_textbox(slide, 2.0, 3.8, 14, 1.3, "产品定价策略", font_size=16, color=P["primary"], bold=True)
    pricing = [
        ("基础款", "1,999-2,499", "可视化分区+分温精储+静音", False),
        ("进阶款", "2,999-3,499", "+RGB氛围灯+情绪模式+电控玻璃", False),
        ("旗舰款", "3,999-4,999", "+AI库存识别+语音+可换面板", True),
    ]
    for i, (tier, price, features, is_flagship) in enumerate(pricing):
        py = 5.3 + i * 1.9
        bg = P["primary"] if is_flagship else P["light"]
        txt_c = P["white"] if is_flagship else P["primary"]
        feat_c = P["ice"] if is_flagship else P["grey"]
        add_rect(slide, 2.0, py, 14.0, 1.5, bg, round_corners=True)
        add_textbox(slide, 2.5, py + 0.12, 3.0, 1.3, tier, font_size=13, color=txt_c, bold=True)
        add_textbox(slide, 5.5, py + 0.12, 3.8, 1.3, price, font_size=13, color=P["secondary"], bold=True)
        add_textbox(slide, 9.5, py + 0.12, 5.8, 1.3, features, font_size=10, color=feat_c)

    # Revenue Model
    add_textbox(slide, 18.3, 3.8, 14, 1.3, "盈利模式", font_size=16, color=P["primary"], bold=True)
    revenue = [
        "硬件销售：三级定价覆盖不同消费力，预计毛利率35-45%",
        "配件耗材：DIY模块托盘、风味冰格、替换面板等复购收入",
        "平台分成：饮品推荐与即时零售平台合作导流分成",
        "会员订阅：AI库存管理+智能推荐高级功能订阅（9.9元/月）",
    ]
    for i, r in enumerate(revenue):
        add_ellipse_bullet(slide, 18.3, 5.6 + i * 1.4, r, font_size=10, color=P["dark"])

    # Marketing
    add_textbox(slide, 2.0, 11.1, 30, 1.3, "营销与渠道策略", font_size=16, color=P["primary"], bold=True)
    channels = [
        ("线上种草", "小红书/抖音 KOL种草，\n京东/天猫旗舰店首发", P["secondary"]),
        ("线下体验", "海尔智慧家庭体验店\n+城市快闪店", P["accent"]),
        ("跨界联名", "精酿啤酒品牌/即饮茶\n品牌联名定制款", P["green"]),
        ("社群运营", "私域社群+饮品DIY内容\n+用户UGC激励", RGBColor(0x8E, 0x44, 0xAD)),
    ]
    for i, (title, desc, color) in enumerate(channels):
        cx = 2.0 + i * 7.8
        add_rect(slide, cx, 12.7, 7.0, 4.0, P["light"], round_corners=True)
        add_rect(slide, cx + 2.2, 13.1, 2.5, 0.12, color)
        add_textbox(slide, cx, 13.5, 7.0, 1.0, title, font_size=14, color=P["dark"], bold=True, align=PP_ALIGN.CENTER)
        add_multiline_textbox(slide, cx + 0.5, 14.6, 6.0, 1.5, desc.split("\n"), font_size=10, color=P["grey"])

    # ===== Slide 10: 财务分析 =====
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_bg(slide, P["white"])
    add_section_header(slide, "08", "财务分析")

    # Investment
    add_textbox(slide, 2.0, 3.8, 14, 1.3, "首年度投入预算", font_size=16, color=P["primary"], bold=True)
    cost_items = [
        ("研发费用（模具+样机+认证）", "200万", False),
        ("模具开发（3款面板+结构件）", "150万", False),
        ("首批量产（1000台）", "300万", False),
        ("营销推广（线上+线下）", "100万", False),
        ("团队人力（10人×12月）", "200万", False),
        ("合计", "950万", True),
    ]
    for i, (item, amount, is_total) in enumerate(cost_items):
        cy = 5.3 + i * 1.15
        bg = P["primary"] if is_total else P["light"]
        txt_c = P["white"] if is_total else P["dark"]
        amt_c = P["accent"] if is_total else P["secondary"]
        add_rect(slide, 2.0, cy, 14.0, 0.95, bg, round_corners=True)
        add_textbox(slide, 2.5, cy + 0.05, 9.5, 0.85, item, font_size=11, color=txt_c, bold=is_total)
        add_textbox(slide, 12.2, cy + 0.05, 3.3, 0.85, amount, font_size=12, color=amt_c, bold=True, align=PP_ALIGN.RIGHT)

    # Revenue Forecast
    add_textbox(slide, 18.3, 3.8, 14, 1.3, "三年收入预测", font_size=16, color=P["primary"], bold=True)
    forecast_rows = [
        [{"text": "", "font_size": 10, "bold": True, "color": P["white"], "fill_color": P["primary"]},
         {"text": "第1年", "font_size": 10, "bold": True, "color": P["white"], "fill_color": P["primary"]},
         {"text": "第2年", "font_size": 10, "bold": True, "color": P["white"], "fill_color": P["primary"]},
         {"text": "第3年", "font_size": 10, "bold": True, "color": P["white"], "fill_color": P["primary"]}],
        [{"text": "销量（台）", "font_size": 10}, {"text": "3,000", "font_size": 10}, {"text": "12,000", "font_size": 10}, {"text": "30,000", "font_size": 10}],
        [{"text": "硬件收入", "font_size": 10}, {"text": "900万", "font_size": 10}, {"text": "3,600万", "font_size": 10}, {"text": "9,000万", "font_size": 10}],
        [{"text": "配件+服务收入", "font_size": 10}, {"text": "50万", "font_size": 10}, {"text": "300万", "font_size": 10}, {"text": "1,200万", "font_size": 10}],
        [{"text": "总营收", "font_size": 10, "bold": True}, {"text": "950万", "font_size": 10, "bold": True}, {"text": "3,900万", "font_size": 10, "bold": True}, {"text": "1.02亿", "font_size": 10, "bold": True, "color": P["secondary"]}],
    ]
    make_table(slide, 18.3, 5.3, 14.0, forecast_rows, [3.8, 3.4, 3.4, 3.4], [0.55, 0.55, 0.55, 0.55, 0.55])

    # Funding Plan
    add_textbox(slide, 18.3, 10.1, 14, 1.3, "融资计划", font_size=16, color=P["primary"], bold=True)
    fund_items = [
        "天使轮融资：500万元，出让10%股权",
        "资金用途：产品研发40% + 模具30% + 营销20% + 运营10%",
        "预计第2年实现盈亏平衡，第3年净利润率达15%",
        "退出路径：3-5年内被海尔集团收购或独立IPO",
    ]
    for i, f in enumerate(fund_items):
        add_ellipse_bullet(slide, 18.3, 11.8 + i * 1.25, f, font_size=10, color=P["dark"], bullet_color=P["accent"])

    # ===== Slide 11: 风险评估 =====
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_bg(slide, P["white"])
    add_section_header(slide, "09", "风险评估与应对策略")

    risks = [
        ("市场需求不及预期", "中", "中", "首批1000台小批量试产，通过预售验证需求；保留快速迭代能力"),
        ("竞品快速跟进", "高", "中", "依托海尔品牌+渠道壁垒，6个月窗口期建立用户心智；持续迭代情绪模式"),
        ("供应链成本上涨", "中", "中", "核心零部件多供应商备份；模块化设计降低定制件比例"),
        ("技术实现难度", "低", "低", "七项技术均为成熟方案，无卡脖子环节；分阶段发布，降低技术风险"),
        ("品牌认知度不足", "中", "高", "依托海尔母品牌背书，小红书/抖音内容种草建立"情绪冰仓"独立IP"),
        ("渠道拓展困难", "低", "中", "复用海尔现有渠道体系；同时布局线上DTC模式降低渠道依赖"),
    ]

    risk_rows = [
        [{"text": "风险因素", "font_size": 10, "bold": True, "color": P["white"], "fill_color": P["primary"]},
         {"text": "等级", "font_size": 10, "bold": True, "color": P["white"], "fill_color": P["primary"]},
         {"text": "影响", "font_size": 10, "bold": True, "color": P["white"], "fill_color": P["primary"]},
         {"text": "应对策略", "font_size": 10, "bold": True, "color": P["white"], "fill_color": P["primary"]}],
    ]
    level_colors = {"高": P["red"], "中": P["accent"], "低": P["green"]}
    for ri, (risk, level, impact, strategy) in enumerate(risks):
        bg = P["light"] if ri % 2 == 0 else P["white"]
        risk_rows.append([
            {"text": risk, "font_size": 10, "fill_color": bg, "align": PP_ALIGN.LEFT},
            {"text": level, "font_size": 10, "fill_color": bg, "color": level_colors.get(level, P["dark"]), "bold": True},
            {"text": impact, "font_size": 10, "fill_color": bg},
            {"text": strategy, "font_size": 9, "fill_color": bg, "align": PP_ALIGN.LEFT},
        ])

    make_table(slide, 2.0, 3.8, 29.8, risk_rows, [6.3, 2.0, 2.0, 19.5], [0.6, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0])

    # ===== Slide 12: 团队与里程碑 =====
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_bg(slide, P["white"])
    add_section_header(slide, "10", "团队架构与推进计划")

    add_textbox(slide, 2.0, 3.8, 14, 1.3, "核心团队", font_size=16, color=P["primary"], bold=True)
    team = [
        ("任泓博", "产品经理", "制冷海外市场产品"),
        ("刘子涵", "产品企划", "制冷海外产品企划"),
        ("臧炳松", "竞品分析", "GMTP"),
        ("安文滨", "机构工程师", "制冷机构"),
        ("王洪博", "结构工程师", "制冷结构"),
        ("王志康", "结构工程师", "制冷结构"),
        ("李兆木", "暖通工程师", "制冷暖通"),
        ("鹿宝祥", "暖通工程师", "制冷暖通"),
        ("赵姝钧", "财务分析", "财务"),
    ]
    for i, (name, role, dept) in enumerate(team):
        col = 2.0 + (i % 3) * 4.8
        row = i // 3
        ty = 5.3 + row * 1.65
        add_rect(slide, col, ty, 4.3, 1.25, P["light"], round_corners=True)
        add_textbox(slide, col, ty + 0.05, 4.3, 0.7, f"{name}  {role}", font_size=9, color=P["primary"], bold=True, align=PP_ALIGN.CENTER)
        add_textbox(slide, col, ty + 0.7, 4.3, 0.5, dept, font_size=8, color=P["grey"], align=PP_ALIGN.CENTER)

    add_textbox(slide, 18.3, 3.8, 14, 1.3, "关键里程碑", font_size=16, color=P["primary"], bold=True)
    milestones = [
        ("7/13", "入职报到", False),
        ("7/16", "黑马大赛初赛", True),
        ("7/20", "黑马大赛决赛", True),
        ("8-9月", "产品详细设计+样机开发", False),
        ("10-11月", "模具开发+小批量试产", False),
        ("12月", "首批1000台预售上线", False),
        ("2027 Q1", "正式量产+全渠道发售", False),
        ("2027 Q2", "目标：月销1000台", False),
    ]
    for i, (date, event, highlight) in enumerate(milestones):
        my = 5.3 + i * 1.4
        dot_color = P["secondary"] if highlight else P["primary"]
        # Dot
        shape = slide.shapes.add_shape(MSO_SHAPE.OVAL, Cm(18.3), Cm(my + 0.25), Cm(0.4), Cm(0.4))
        shape.fill.solid()
        shape.fill.fore_color.rgb = dot_color
        shape.line.fill.background()
        # Line
        if i < len(milestones) - 1:
            shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Cm(18.45), Cm(my + 0.65), Cm(0.1), Cm(0.75))
            shape.fill.solid()
            shape.fill.fore_color.rgb = P["ice"]
            shape.line.fill.background()
        add_textbox(slide, 19.1, my, 3.3, 0.9, date, font_size=11, color=dot_color, bold=True)
        add_textbox(slide, 22.5, my, 10, 0.9, event, font_size=11, color=P["dark"])

    # ===== Slide 13: 感谢页 =====
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_bg(slide, P["primary"])
    add_rect(slide, 0, 0, 33.867, 0.2, P["accent"])
    add_rect(slide, 0, 18.85, 33.867, 0.2, P["accent"])
    add_textbox(slide, 0, 5.0, 33.867, 3.8, "谢谢", font_size=60, color=P["white"], bold=True, align=PP_ALIGN.CENTER)
    add_textbox(slide, 0, 8.8, 33.867, 2.0, "情绪冰仓 · 一杯饮尽松弛感", font_size=24, color=P["accent"], align=PP_ALIGN.CENTER)
    add_rect(slide, 14.0, 11.4, 5.9, 0.1, P["secondary"])
    add_textbox(slide, 0, 12.7, 33.867, 1.3, "海尔制冷 · 情绪冰仓项目组  |  2026年7月", font_size=13, color=P["ice"], align=PP_ALIGN.CENTER)
    add_textbox(slide, 0, 14.0, 33.867, 1.3, "联系方式：renhongbo@haier.com", font_size=12, color=P["grey"], align=PP_ALIGN.CENTER)

    # ===== 保存 =====
    output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "情绪冰仓_黑马大赛路演PPT.pptx")
    prs.save(output_path)
    print(f"PPT已保存至: {output_path}")
    return output_path

if __name__ == "__main__":
    create_ppt()