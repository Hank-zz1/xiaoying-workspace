#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""海尔产品研发流程 — 企划与研发职责分工 PPT 生成脚本"""

from pptx import Presentation
from pptx.util import Inches, Pt, Emu, Cm
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.dml.color import RGBColor as RgbColor
from pptx.oxml.ns import qn
import os

# 配色
PRIMARY = RgbColor(0x1E, 0x27, 0x61)
SECONDARY = RgbColor(0xCA, 0xDC, 0xFC)
WHITE = RgbColor(0xFF, 0xFF, 0xFF)
DARK = RgbColor(0x0D, 0x11, 0x17)
LIGHT = RgbColor(0xF6, 0xF8, 0xFA)
GOLD = RgbColor(0xD4, 0xAF, 0x37)
GREEN = RgbColor(0x2E, 0x7D, 0x32)
ORANGE = RgbColor(0xE6, 0x51, 0x00)
GRAY = RgbColor(0x6C, 0x75, 0x7D)
GREEN_LIGHT = RgbColor(0xE8, 0xF5, 0xE9)
ORANGE_LIGHT = RgbColor(0xFD, 0xE8, 0xD0)
GOLD_LIGHT = RgbColor(0xFB, 0xF3, 0xD5)

FONT = "Microsoft YaHei"

def set_slide_bg(slide, color):
    bg = slide.background
    fill = bg.fill
    fill.solid()
    fill.fore_color.rgb = color

def add_textbox(slide, left, top, width, height, text, font_size=14, color=DARK, bold=False, align=PP_ALIGN.LEFT, font_name=FONT):
    txBox = slide.shapes.add_textbox(Inches(left), Inches(top), Inches(width), Inches(height))
    tf = txBox.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = text
    p.font.size = Pt(font_size)
    p.font.color.rgb = color
    p.font.bold = bold
    p.font.name = font_name
    p.alignment = align
    return txBox

def add_round_rect(slide, left, top, width, height, fill_color, transparency=0):
    shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left), Inches(top), Inches(width), Inches(height))
    shape.fill.solid()
    shape.fill.fore_color.rgb = fill_color
    shape.line.fill.background()
    return shape

def add_rect(slide, left, top, width, height, fill_color):
    shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(left), Inches(top), Inches(width), Inches(height))
    shape.fill.solid()
    shape.fill.fore_color.rgb = fill_color
    shape.line.fill.background()
    return shape

def add_ellipse(slide, left, top, width, height, fill_color):
    shape = slide.shapes.add_shape(MSO_SHAPE.OVAL, Inches(left), Inches(top), Inches(width), Inches(height))
    shape.fill.solid()
    shape.fill.fore_color.rgb = fill_color
    shape.line.fill.background()
    return shape

def add_text_in_shape(shape, text, font_size=12, color=WHITE, bold=False, align=PP_ALIGN.CENTER, font_name=FONT):
    tf = shape.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = text
    p.font.size = Pt(font_size)
    p.font.color.rgb = color
    p.font.bold = bold
    p.font.name = font_name
    p.alignment = align

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)

# ====== SLIDE 1: 封面 ======
slide = prs.slides.add_slide(prs.slide_layouts[6])  # blank
set_slide_bg(slide, PRIMARY)
add_rect(slide, 0, 0, 13.333, 0.06, GOLD)
add_rect(slide, 0, 7.44, 13.333, 0.06, GOLD)
add_rect(slide, 0.8, 1.8, 0.06, 3.2, GOLD)

add_textbox(slide, 1.2, 1.8, 10, 1.0, "海尔产品研发流程", font_size=42, color=WHITE, bold=True)
add_textbox(slide, 1.2, 2.7, 10, 0.7, "企划与研发职责分工", font_size=28, color=SECONDARY, bold=True)
add_rect(slide, 1.2, 3.5, 2.5, 0.04, GOLD)
add_textbox(slide, 1.2, 3.8, 10, 0.5, "P0-P6 全流程阶段 · 六大环节 · 清晰职责边界", font_size=16, color=SECONDARY)
add_textbox(slide, 1.2, 5.5, 5, 0.4, "2026年5月", font_size=14, color=SECONDARY)

# ====== SLIDE 2: 目录 ======
slide = prs.slides.add_slide(prs.slide_layouts[6])
set_slide_bg(slide, LIGHT)
add_rect(slide, 0, 0, 13.333, 1.2, PRIMARY)
add_textbox(slide, 0.8, 0.3, 5, 0.6, "目录", font_size=32, color=WHITE, bold=True)

toc = [
    ("01", "流程总览", "P0-P6 六阶段全景图"),
    ("02", "P0 概念与定义", "企划主导 — 市场调研、立项论证"),
    ("03", "P1 调研与设计", "企划+研发协作 — 规格制定与工程准备"),
    ("04", "P2 开发与设计", "研发主导 — 详细设计、模具制作"),
    ("05", "P3 推敲验证", "研发主导 — 测试验证、认证闭环"),
    ("06", "P4 交付", "研发+企划协作 — 量产保障、市场推介"),
    ("07", "P5-P6 运营与退市", "成熟运营、产品退市"),
    ("08", "职责汇总", "企划 vs 研发 全景对比"),
]
for i, (num, title, desc) in enumerate(toc):
    y = 1.6 + i * 0.7
    circle = add_ellipse(slide, 0.8, y + 0.05, 0.45, 0.45, PRIMARY)
    add_text_in_shape(circle, num, font_size=14, color=WHITE, bold=True)
    add_textbox(slide, 1.5, y - 0.02, 4, 0.3, title, font_size=16, color=DARK, bold=True)
    add_textbox(slide, 1.5, y + 0.28, 8, 0.25, desc, font_size=12, color=GRAY)
    if i < len(toc) - 1:
        add_rect(slide, 1.5, y + 0.6, 10.5, 0.01, SECONDARY)

# ====== SLIDE 3: 流程总览 ======
slide = prs.slides.add_slide(prs.slide_layouts[6])
set_slide_bg(slide, LIGHT)
add_rect(slide, 0, 0, 13.333, 1.1, PRIMARY)
add_textbox(slide, 0.8, 0.25, 10, 0.6, "流程总览：P0-P6 六阶段全景图", font_size=28, color=WHITE, bold=True)

phases = [
    ("P0", "概念与定义", "企划", GREEN),
    ("P1", "调研与设计", "企划+研发", GOLD),
    ("P2", "开发与设计", "研发", ORANGE),
    ("P3", "推敲验证", "研发", ORANGE),
    ("P4", "交付", "研发+企划", GOLD),
    ("P5", "成熟运营", "研发+企划", GOLD),
    ("P6", "产品退市", "企划", GREEN),
]

for i, (pid, name, owner, clr) in enumerate(phases):
    x = 0.5 + i * 1.78
    w = 1.6
    card = add_round_rect(slide, x, 1.8, w, 3.5, WHITE)
    tag = add_round_rect(slide, x + 0.25, 2.0, 1.1, 0.5, PRIMARY)
    add_text_in_shape(tag, pid, font_size=18, color=WHITE, bold=True)
    add_textbox(slide, x + 0.05, 2.7, w - 0.1, 0.5, name, font_size=12, color=DARK, bold=True, align=PP_ALIGN.CENTER)
    own_tag = add_round_rect(slide, x + 0.15, 3.4, w - 0.3, 0.35, clr)
    add_text_in_shape(own_tag, owner, font_size=10, color=WHITE, bold=True)
    if i < len(phases) - 1:
        add_textbox(slide, x + w, 3.2, 0.35, 0.5, "→", font_size=20, color=PRIMARY, align=PP_ALIGN.CENTER)

# 图例
add_round_rect(slide, 0.5, 5.8, 0.3, 0.25, GREEN)
add_textbox(slide, 0.9, 5.8, 1.2, 0.25, "企划主导", font_size=10, color=GRAY)
add_round_rect(slide, 2.6, 5.8, 0.3, 0.25, GOLD)
add_textbox(slide, 3.0, 5.8, 1.5, 0.25, "企划+研发协作", font_size=10, color=GRAY)
add_round_rect(slide, 5.0, 5.8, 0.3, 0.25, ORANGE)
add_textbox(slide, 5.4, 5.8, 1.2, 0.25, "研发主导", font_size=10, color=GRAY)

# ====== SLIDE 4: P0 概念与定义 ======
slide = prs.slides.add_slide(prs.slide_layouts[6])
set_slide_bg(slide, LIGHT)
add_rect(slide, 0, 0, 13.333, 1.1, GREEN)
add_textbox(slide, 0.8, 0.15, 6, 0.5, "P0 概念与定义", font_size=28, color=WHITE, bold=True)
tag = add_round_rect(slide, 0.8, 0.7, 1.2, 0.3, WHITE)
add_text_in_shape(tag, "企划主导", font_size=11, color=GREEN, bold=True)

p0_items = [
    "企划书（含 MRD / 产品数据表）",
    "产品对手对阵表",
    "创意评审报告",
    "POD（立项报告 / 注册表 / 市场分析 / 预算表）",
    "差异点的分析报告",
    "外观效果图 / 外观图形评审意见书",
    "创意评审会",
]
for i, item in enumerate(p0_items):
    y = 1.5 + i * 0.75
    card = add_round_rect(slide, 0.8, y, 11.3, 0.6, WHITE)
    circle = add_ellipse(slide, 1.0, y + 0.1, 0.4, 0.4, GREEN)
    add_text_in_shape(circle, str(i + 1), font_size=13, color=WHITE, bold=True)
    add_textbox(slide, 1.6, y + 0.08, 10, 0.45, item, font_size=15, color=DARK)

note = add_round_rect(slide, 10.5, 6.3, 2.4, 0.6, GREEN_LIGHT)
add_text_in_shape(note, "100% 企划负责\n产品方向的源头", font_size=11, color=GREEN, bold=True)

# ====== SLIDE 5: P1 调研与设计 ======
slide = prs.slides.add_slide(prs.slide_layouts[6])
set_slide_bg(slide, LIGHT)
add_rect(slide, 0, 0, 13.333, 1.1, PRIMARY)
add_textbox(slide, 0.8, 0.15, 6, 0.5, "P1 调研与设计", font_size=28, color=WHITE, bold=True)
tag = add_round_rect(slide, 0.8, 0.7, 1.8, 0.3, WHITE)
add_text_in_shape(tag, "企划 + 研发协作", font_size=11, color=PRIMARY, bold=True)

# 左面板 - 企划
left_card = add_round_rect(slide, 0.5, 1.4, 5.8, 5.4, WHITE)
left_hdr = add_round_rect(slide, 0.5, 1.4, 5.8, 0.55, GREEN)
add_text_in_shape(left_hdr, "企划负责", font_size=18, color=WHITE, bold=True)
for i, item in enumerate([
    "产品技术规格书",
    "市场计划",
    "用户测试报告",
    "成本BOM",
]):
    y = 2.2 + i * 0.65
    add_textbox(slide, 1.3, y, 4.5, 0.5, f"• {item}", font_size=14, color=DARK)

# 右面板 - 研发
right_card = add_round_rect(slide, 6.8, 1.4, 5.8, 5.4, WHITE)
right_hdr = add_round_rect(slide, 6.8, 1.4, 5.8, 0.55, ORANGE)
add_text_in_shape(right_hdr, "研发负责", font_size=18, color=WHITE, bold=True)
for i, item in enumerate([
    "质量计划 / 采购计划 / 制造计划",
    "基本型号品质分析及改善计划",
    "3D设计图",
    "模型样机评审结论",
    "母本分析报告",
    "主关件清单",
    "新功能模块标准",
]):
    y = 2.2 + i * 0.65
    add_textbox(slide, 7.6, y, 4.5, 0.5, f"• {item}", font_size=13, color=DARK)

# ====== SLIDE 6: P2 开发与设计 ======
slide = prs.slides.add_slide(prs.slide_layouts[6])
set_slide_bg(slide, LIGHT)
add_rect(slide, 0, 0, 13.333, 1.1, ORANGE)
add_textbox(slide, 0.8, 0.15, 6, 0.5, "P2 开发与设计", font_size=28, color=WHITE, bold=True)
tag = add_round_rect(slide, 0.8, 0.7, 1.0, 0.3, WHITE)
add_text_in_shape(tag, "研发主导", font_size=11, color=ORANGE, bold=True)

p2_left = [
    "质量计划调整",
    "零部件图纸 / 零部件数据",
    "新品任务单",
    "零部件标准",
    "测试计划",
    "DFMEA分析",
    "新部品报验计划",
]
p2_right = [
    "设计雷区排查",
    "图纸评审和发布",
    "模块化设计项目确认",
    "新功能模块设计评审验证",
    "模具交互制作",
    "手工样机评审及问题闭环",
]

for i, item in enumerate(p2_left):
    y = 1.4 + i * 0.78
    add_round_rect(slide, 0.5, y, 5.8, 0.65, WHITE)
    add_rect(slide, 0.5, y, 0.08, 0.65, ORANGE)
    add_textbox(slide, 0.85, y + 0.08, 5.2, 0.5, item, font_size=14, color=DARK)

for i, item in enumerate(p2_right):
    y = 1.4 + i * 0.78
    add_round_rect(slide, 6.8, y, 5.8, 0.65, WHITE)
    add_rect(slide, 6.8, y, 0.08, 0.65, ORANGE)
    add_textbox(slide, 7.15, y + 0.08, 5.2, 0.5, item, font_size=14, color=DARK)

# ====== SLIDE 7: P3 推敲验证 ======
slide = prs.slides.add_slide(prs.slide_layouts[6])
set_slide_bg(slide, LIGHT)
add_rect(slide, 0, 0, 13.333, 1.1, ORANGE)
add_textbox(slide, 0.8, 0.15, 6, 0.5, "P3 推敲验证", font_size=28, color=WHITE, bold=True)
tag = add_round_rect(slide, 0.8, 0.7, 1.0, 0.3, WHITE)
add_text_in_shape(tag, "研发主导", font_size=11, color=ORANGE, bold=True)

p3_items = [
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
]
for i, item in enumerate(p3_items):
    y = 1.35 + i * 0.55
    add_round_rect(slide, 0.5, y, 12.1, 0.48, WHITE)
    add_rect(slide, 0.5, y, 0.06, 0.48, ORANGE)
    add_textbox(slide, 0.8, y + 0.04, 11.5, 0.4, item, font_size=13, color=DARK)

# ====== SLIDE 8: P4 交付 ======
slide = prs.slides.add_slide(prs.slide_layouts[6])
set_slide_bg(slide, LIGHT)
add_rect(slide, 0, 0, 13.333, 1.1, PRIMARY)
add_textbox(slide, 0.8, 0.15, 6, 0.5, "P4 交付", font_size=28, color=WHITE, bold=True)
tag = add_round_rect(slide, 0.8, 0.7, 1.8, 0.3, WHITE)
add_text_in_shape(tag, "研发 + 企划协作", font_size=11, color=PRIMARY, bold=True)

# 左面板
left_card = add_round_rect(slide, 0.5, 1.4, 5.8, 2.8, WHITE)
left_hdr = add_round_rect(slide, 0.5, 1.4, 5.8, 0.5, GREEN)
add_text_in_shape(left_hdr, "企划负责", font_size=16, color=WHITE, bold=True)
add_textbox(slide, 1.0, 2.2, 5, 0.5, "• 市场推介计划", font_size=14, color=DARK)
add_textbox(slide, 1.0, 2.8, 5, 0.5, "• 项目总结", font_size=14, color=DARK)

# 右面板
right_card = add_round_rect(slide, 6.8, 1.4, 5.8, 5.2, WHITE)
right_hdr = add_round_rect(slide, 6.8, 1.4, 5.8, 0.5, ORANGE)
add_text_in_shape(right_hdr, "研发负责", font_size=16, color=WHITE, bold=True)
for i, item in enumerate([
    "滚动计划 / 生产订单保障评审",
    "小批首批物料入厂检验",
    "小批首台样机评审",
    "商检出货报告",
    "售后培训 / 售后备件",
    "新品初期三个月质量问题跟踪",
    "QCL/QC/OQC 过程管控",
]):
    add_textbox(slide, 7.6, 2.2 + i * 0.55, 4.8, 0.45, f"• {item}", font_size=13, color=DARK)

# ====== SLIDE 9: P5-P6 运营与退市 ======
slide = prs.slides.add_slide(prs.slide_layouts[6])
set_slide_bg(slide, LIGHT)
add_rect(slide, 0, 0, 13.333, 1.1, PRIMARY)
add_textbox(slide, 0.8, 0.15, 10, 0.5, "P5 成熟运营 & P6 产品退市", font_size=28, color=WHITE, bold=True)

# P5
add_round_rect(slide, 0.5, 1.5, 12.1, 3.3, WHITE)
add_round_rect(slide, 0.5, 1.5, 12.1, 0.55, GOLD_LIGHT)
add_textbox(slide, 0.7, 1.55, 10, 0.45, "P5 成熟运营 — 研发主导 + 企划年度复审", font_size=16, color=GOLD, bold=True)

p5_items = [
    ("产品年内复审", "企划", GREEN),
    ("工程管理 / 跳闸型号评审", "研发", ORANGE),
    ("型号维度质量改善", "研发", ORANGE),
    ("老品4M1E变更管控", "研发", ORANGE),
    ("老品市场问题闭环", "研发", ORANGE),
]
for i, (item, owner, clr) in enumerate(p5_items):
    y = 2.3 + i * 0.55
    add_textbox(slide, 0.8, y, 8, 0.4, f"• {item}", font_size=13, color=DARK)
    tag2 = add_round_rect(slide, 9.5, y + 0.05, 0.85, 0.3, clr)
    add_text_in_shape(tag2, owner, font_size=10, color=WHITE, bold=True)

# P6
add_round_rect(slide, 0.5, 5.2, 12.1, 1.5, WHITE)
add_round_rect(slide, 0.5, 5.2, 12.1, 0.5, GREEN_LIGHT)
add_textbox(slide, 0.7, 5.23, 10, 0.45, "P6 产品退市 — 企划主导", font_size=16, color=GREEN, bold=True)
add_textbox(slide, 0.8, 5.9, 10, 0.5, "• 产品下市申请", font_size=15, color=DARK)

# ====== SLIDE 10: 职责汇总 ======
slide = prs.slides.add_slide(prs.slide_layouts[6])
set_slide_bg(slide, LIGHT)
add_rect(slide, 0, 0, 13.333, 1.1, PRIMARY)
add_textbox(slide, 0.8, 0.25, 8, 0.6, "职责汇总对比", font_size=28, color=WHITE, bold=True)

# 企划汇总
left_card = add_round_rect(slide, 0.5, 1.4, 5.8, 5.5, WHITE)
left_hdr = add_round_rect(slide, 0.5, 1.4, 5.8, 0.65, GREEN)
add_text_in_shape(left_hdr, "企划（产品规划）", font_size=20, color=WHITE, bold=True)
plan_items = [
    "P0：概念与定义（100%主导）",
    "P1：产品技术规格书 / 市场计划 / 成本BOM",
    "P4：市场推介计划 / 项目总结",
    "P5：产品年内复审",
    "P6：产品下市申请",
]
for i, item in enumerate(plan_items):
    add_textbox(slide, 0.8, 2.4 + i * 0.6, 5.2, 0.5, f"• {item}", font_size=13, color=DARK)
add_textbox(slide, 1.0, 5.7, 5, 0.8, "核心：定方向\n"做什么、卖给谁、多少钱"", font_size=13, color=GREEN, bold=True)

# 研发汇总
right_card = add_round_rect(slide, 6.8, 1.4, 5.8, 5.5, WHITE)
right_hdr = add_round_rect(slide, 6.8, 1.4, 5.8, 0.65, ORANGE)
add_text_in_shape(right_hdr, "研发（工程实现）", font_size=20, color=WHITE, bold=True)
rnd_items = [
    "P1：质量/采购/制造计划 / 3D设计",
    "P2：开发与设计（100%主导）",
    "P3：推敲验证（100%主导）",
    "P4：量产保障 / 售后 / 过程管控",
    "P5：工程管理 / 质量改善 / 变更管控",
]
for i, item in enumerate(rnd_items):
    add_textbox(slide, 7.1, 2.4 + i * 0.6, 5.2, 0.5, f"• {item}", font_size=13, color=DARK)
add_textbox(slide, 7.3, 5.7, 5, 0.8, "核心：管落地\n"怎么做、能不能做、质量过不过关"", font_size=13, color=ORANGE, bold=True)

# ====== SLIDE 11: 结束页 ======
slide = prs.slides.add_slide(prs.slide_layouts[6])
set_slide_bg(slide, PRIMARY)
add_rect(slide, 0, 0, 13.333, 0.06, GOLD)
add_rect(slide, 0, 7.44, 13.333, 0.06, GOLD)

add_textbox(slide, 0, 2.2, 13.333, 1.2, "感谢聆听", font_size=48, color=WHITE, bold=True, align=PP_ALIGN.CENTER)
add_rect(slide, 5.5, 3.5, 2.3, 0.04, GOLD)
add_textbox(slide, 0, 3.9, 13.333, 0.6, "海尔产品研发流程 · 企划与研发职责分工", font_size=16, color=SECONDARY, align=PP_ALIGN.CENTER)
add_textbox(slide, 0, 4.5, 13.333, 0.5, "企划定方向 · 研发管落地", font_size=14, color=GOLD, align=PP_ALIGN.CENTER)

# 保存
output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "海尔产品研发流程_企划与研发职责分工.pptx")
prs.save(output_path)
print(f"PPT saved to: {output_path}")
