# -*- coding: utf-8 -*-
"""情绪冰仓·一杯饮尽松弛感 — 路演PPT v2"""

from pptx import Presentation
from pptx.util import Inches, Pt, Emu, Cm
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR, MSO_AUTOSIZE
from pptx.enum.shapes import MSO_SHAPE
from pptx.oxml.ns import qn
import os

# ── Paths ──────────────────────────────────────────
DATA_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT = os.path.join(DATA_DIR, "Chill_冷柜_路演PPT_v2.pptx")
IMG = lambda f: os.path.join(DATA_DIR, f)

# ── Constants ───────────────────────────────────────
W = Inches(13.33)
H = Inches(7.5)
BLANK = MSO_SHAPE.RECTANGLE

# ── Colors ──────────────────────────────────────────
BG    = RGBColor(0x0A, 0x0A, 0x0F)
CARD  = RGBColor(0x12, 0x12, 0x1A)
CARD2 = RGBColor(0x18, 0x18, 0x22)
CYAN  = RGBColor(0x00, 0xD4, 0xFF)
GREEN = RGBColor(0x00, 0xE6, 0x76)
AMBER = RGBColor(0xFF, 0x91, 0x00)
WHITE = RGBColor(0xEA, 0xEA, 0xEA)
GRAY  = RGBColor(0x88, 0x88, 0x99)
PURPLE= RGBColor(0x7C, 0x3A, 0xED)
ROSE  = RGBColor(0xFF, 0x5E, 0x7E)
CYAN_DIM = RGBColor(0x00, 0x8A, 0xA8)

# ── Presentation ────────────────────────────────────
prs = Presentation()
prs.slide_width = W
prs.slide_height = H
layout = prs.slide_layouts[6]  # blank

# ── Helpers ─────────────────────────────────────────
def bg(slide, color=BG):
    slide.background.fill.solid()
    slide.background.fill.fore_color.rgb = color

def rect(slide, l, t, w, h, color, rx=None):
    s = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE if rx else BLANK, l, t, w, h)
    s.fill.solid(); s.fill.fore_color.rgb = color
    s.line.fill.background()
    if rx: s.adjustments[0] = rx
    return s

def txt(slide, l, t, w, h, text, sz=Pt(14), clr=WHITE, bold=False, align=PP_ALIGN.LEFT, font='Microsoft YaHei', anchor=MSO_ANCHOR.TOP):
    tb = slide.shapes.add_textbox(l, t, w, h)
    tf = tb.text_frame; tf.word_wrap = True
    tf.auto_size = None
    p = tf.paragraphs[0]
    p.text = text; p.font.size = sz; p.font.color.rgb = clr
    p.font.bold = bold; p.font.name = font; p.alignment = align
    return tb

def mtxt(slide, l, t, w, h, lines, sz=Pt(12), clr=WHITE, bold_first=False, font='Microsoft YaHei', spacing=Pt(6)):
    """Multi-line text box"""
    tb = slide.shapes.add_textbox(l, t, w, h)
    tf = tb.text_frame; tf.word_wrap = True
    tf.auto_size = None
    for i, line in enumerate(lines):
        if i == 0:
            p = tf.paragraphs[0]
        else:
            p = tf.add_paragraph()
        p.text = line
        p.font.size = sz
        p.font.color.rgb = clr
        p.font.name = font
        p.font.bold = (bold_first and i == 0)
        p.space_after = spacing
        p.alignment = PP_ALIGN.LEFT
    return tb

def pic(slide, path, l, t, w, h=None):
    if h:
        return slide.shapes.add_picture(path, l, t, w, h)
    return slide.shapes.add_picture(path, l, t, w)

def accent_line(slide, l, t, w, color=CYAN, h=Inches(0.03)):
    return rect(slide, l, t, w, h, color)

def page_number(slide, num):
    txt(slide, Inches(12.3), Inches(7.1), Inches(0.8), Inches(0.3),
        f"{num:02d} / 12", sz=Pt(9), clr=GRAY, align=PP_ALIGN.RIGHT)

def icon_circle(slide, l, t, color, label="", r=Inches(0.22)):
    """Colored circle with label"""
    s = slide.shapes.add_shape(MSO_SHAPE.OVAL, l, t, r, r)
    s.fill.solid(); s.fill.fore_color.rgb = color
    s.line.fill.background()
    if label:
        txt(slide, l + r + Inches(0.12), t + Inches(0.01), Inches(2), r,
            label, sz=Pt(13), clr=WHITE, bold=False)
    return s

# ═══════════════════════════════════════════════════════════════
# SLIDE 1: COVER
# ═══════════════════════════════════════════════════════════════
s = prs.slides.add_slide(layout)
bg(s)
# Full-bleed cover image
pic(s, IMG("chill_cover.png"), Inches(0), Inches(0), Inches(13.33), Inches(7.5))
# Dark gradient overlay (bottom to top)
overlay = rect(s, Inches(0), Inches(0), Inches(13.33), Inches(7.5), RGBColor(0x0A, 0x0A, 0x0F))
overlay.fill.fore_color.rgb = RGBColor(0x0A, 0x0A, 0x0F)
# Make overlay semi-transparent via XML
from pptx.oxml.ns import nsmap
solidFill = overlay.fill._fill
srgb = solidFill.find(qn('a:solidFill')).find(qn('a:srgbClr'))
if srgb is not None:
    alpha = srgb.makeelement(qn('a:alpha'), {'val': '40000'})  # 25% opacity
    srgb.append(alpha)

# Title
txt(s, Inches(1.5), Inches(2.2), Inches(10.3), Inches(1.0),
    "情绪冰仓", sz=Pt(60), clr=WHITE, bold=True, align=PP_ALIGN.LEFT)
accent_line(s, Inches(1.5), Inches(3.3), Inches(3.0), CYAN, Inches(0.04))
txt(s, Inches(1.5), Inches(3.5), Inches(10.3), Inches(0.7),
    "一杯饮尽松弛感", sz=Pt(32), clr=CYAN, bold=False, align=PP_ALIGN.LEFT)
txt(s, Inches(1.5), Inches(4.4), Inches(10.3), Inches(0.5),
    "年轻人的第一台情绪饮料柜  |  2026 海尔智家黑客马拉松", sz=Pt(16), clr=GRAY, align=PP_ALIGN.LEFT)
txt(s, Inches(1.5), Inches(5.1), Inches(10.3), Inches(0.4),
    "制冷产业第1组", sz=Pt(14), clr=RGBColor(0xAA, 0xAA, 0xBB), align=PP_ALIGN.LEFT)

# ═══════════════════════════════════════════════════════════════
# SLIDE 2: PAIN POINTS
# ═══════════════════════════════════════════════════════════════
s = prs.slides.add_slide(layout)
bg(s)
txt(s, Inches(0.8), Inches(0.5), Inches(5), Inches(0.6), "年轻人的冰箱，不懂我", sz=Pt(36), clr=WHITE, bold=True)
accent_line(s, Inches(0.8), Inches(1.15), Inches(2.5), CYAN, Inches(0.04))

pain_points = [
    ("01", "酒放冰箱串味", "红酒和剩菜共存，\n打开冰箱那一刻，什么心情都没了", AMBER),
    ("02", "温度一刀切", "啤酒不够冰、红酒太冷、\n养生茶饮没地方放，分区全靠塑料袋", CYAN),
    ("03", "氛围感为零", "深夜想来一杯，打开冰箱\n只有刺眼的白光和嗡嗡的噪音", PURPLE),
]
for i, (num, title, desc, color) in enumerate(pain_points):
    x = Inches(0.8 + i * 4.0)
    y = Inches(1.8)
    card_w = Inches(3.6)
    card_h = Inches(3.8)
    rect(s, x, y, card_w, card_h, CARD, rx=0.05)
    # Number
    txt(s, x + Inches(0.3), y + Inches(0.3), Inches(1.0), Inches(0.8),
        num, sz=Pt(48), clr=color, bold=True)
    # Title
    txt(s, x + Inches(0.3), y + Inches(1.3), card_w - Inches(0.6), Inches(0.5),
        title, sz=Pt(20), clr=WHITE, bold=True)
    accent_line(s, x + Inches(0.3), y + Inches(1.85), Inches(1.0), color, Inches(0.03))
    # Description
    txt(s, x + Inches(0.3), y + Inches(2.1), card_w - Inches(0.6), Inches(1.5),
        desc, sz=Pt(13), clr=GRAY)

txt(s, Inches(0.8), Inches(6.2), Inches(11), Inches(0.4),
    "Z世代年轻人独居比例持续上升，但传统冰箱/冷柜从未为"一个人的精致生活"设计过", sz=Pt(12), clr=GRAY)
page_number(s, 2)

print("Slides 1-2 done")

# ═══════════════════════════════════════════════════════════════
# SLIDE 3: SOLUTION
# ═══════════════════════════════════════════════════════════════
s = prs.slides.add_slide(layout)
bg(s)
# Left text area
txt(s, Inches(0.8), Inches(0.5), Inches(5), Inches(0.6), "不只是冷柜", sz=Pt(36), clr=WHITE, bold=True)
accent_line(s, Inches(0.8), Inches(1.15), Inches(2.5), CYAN, Inches(0.04))
txt(s, Inches(0.8), Inches(1.5), Inches(5.5), Inches(0.5),
    "是懂你情绪的私人饮品管家", sz=Pt(20), clr=CYAN, bold=False)

features = [
    ("专业分温精储", "红葡萄酒/白葡萄酒/啤酒/零卡饮料\n功能饮料/养生饮品，各有专属温区"),
    ("RGB情绪氛围灯", "4种灯光模式自动匹配饮品类型\n微醺暖光 / 冰爽蓝光 / 养生绿光 / 熬夜紫光"),
    ("透明视窗+静音", "全透明钢化玻璃门，拿取一目了然\n35dB静音运行，不打扰深夜独处"),
]
for i, (title, desc) in enumerate(features):
    y = Inches(2.3 + i * 1.6)
    icon_circle(s, Inches(0.8), y, CYAN, "")
    txt(s, Inches(1.4), y, Inches(5), Inches(0.35), title, sz=Pt(16), clr=WHITE, bold=True)
    txt(s, Inches(1.4), y + Inches(0.35), Inches(5), Inches(0.9),
        desc, sz=Pt(12), clr=GRAY)

# Right image
pic(s, IMG("chill_img_1.png"), Inches(7.0), Inches(1.0), Inches(5.8), Inches(5.5))
page_number(s, 3)

# ═══════════════════════════════════════════════════════════════
# SLIDE 4: MARKET DATA
# ═══════════════════════════════════════════════════════════════
s = prs.slides.add_slide(layout)
bg(s)
txt(s, Inches(0.8), Inches(0.5), Inches(5), Inches(0.6), "为什么是现在", sz=Pt(36), clr=WHITE, bold=True)
accent_line(s, Inches(0.8), Inches(1.15), Inches(2.5), CYAN, Inches(0.04))

data_cards = [
    ("4500亿", "情绪消费市场规模", "Z世代为情绪买单的意愿\n是上一代的3.2倍", CYAN),
    ("2.3亿", "中国独居成年人", "一人食/一人饮场景爆发\n精致独处成为新生活方式", GREEN),
    ("67%", "愿意为氛围付费", "年轻消费者愿为产品设计\n和情绪体验支付溢价", AMBER),
]
for i, (num, title, desc, color) in enumerate(data_cards):
    x = Inches(0.8 + i * 4.0)
    y = Inches(1.8)
    card_w = Inches(3.6)
    card_h = Inches(3.2)
    rect(s, x, y, card_w, card_h, CARD, rx=0.05)
    # Number
    txt(s, x + Inches(0.3), y + Inches(0.3), card_w - Inches(0.6), Inches(0.8),
        num, sz=Pt(44), clr=color, bold=True)
    # Title
    txt(s, x + Inches(0.3), y + Inches(1.2), card_w - Inches(0.6), Inches(0.4),
        title, sz=Pt(16), clr=WHITE, bold=True)
    accent_line(s, x + Inches(0.3), y + Inches(1.65), Inches(1.0), color, Inches(0.03))
    # Desc
    txt(s, x + Inches(0.3), y + Inches(1.9), card_w - Inches(0.6), Inches(1.1),
        desc, sz=Pt(12), clr=GRAY)

# Bottom line
txt(s, Inches(0.8), Inches(5.5), Inches(11.5), Inches(0.8),
    "数据来源：艾瑞咨询《2025中国情绪消费白皮书》、国家统计局、京东消费报告",
    sz=Pt(10), clr=GRAY)
page_number(s, 4)

print("Slides 3-4 done")

# ═══════════════════════════════════════════════════════════════
# SLIDE 5: PRODUCT HARDWARE
# ═══════════════════════════════════════════════════════════════
s = prs.slides.add_slide(layout)
bg(s)
txt(s, Inches(0.8), Inches(0.5), Inches(5), Inches(0.6), "硬核产品力", sz=Pt(36), clr=WHITE, bold=True)
accent_line(s, Inches(0.8), Inches(1.15), Inches(2.5), CYAN, Inches(0.04))

# Left: product image
pic(s, IMG("chill_img_1.png"), Inches(0.8), Inches(1.6), Inches(5.8), Inches(5.2))

# Right: spec cards
specs = [
    ("温区", "4个独立温区\n6°C红葡萄酒 / 4°C白葡萄酒\n2°C啤酒 / 8°C养生饮品"),
    ("灯光", "RGB全彩氛围灯\n4种预设模式 + 自定义\n1600万色可选"),
    ("容量", "68L紧凑机身\n可容纳24罐饮料+4瓶酒\n适合1-2人使用"),
    ("交互", "触摸面板 + 手机App\n开门感应亮灯\n智能提醒饮品保质期"),
]
for i, (label, desc) in enumerate(specs):
    x = Inches(7.2 + (i % 2) * 3.0)
    y = Inches(1.6 + (i // 2) * 2.7)
    card_w = Inches(2.7)
    card_h = Inches(2.4)
    rect(s, x, y, card_w, card_h, CARD, rx=0.05)
    txt(s, x + Inches(0.2), y + Inches(0.2), card_w - Inches(0.4), Inches(0.3),
        label, sz=Pt(14), clr=CYAN, bold=True)
    txt(s, x + Inches(0.2), y + Inches(0.6), card_w - Inches(0.4), Inches(1.6),
        desc, sz=Pt(11), clr=GRAY)
page_number(s, 5)

# ═══════════════════════════════════════════════════════════════
# SLIDE 6: 4 MODES
# ═══════════════════════════════════════════════════════════════
s = prs.slides.add_slide(layout)
bg(s)
txt(s, Inches(0.8), Inches(0.5), Inches(5), Inches(0.6), "四种情绪模式", sz=Pt(36), clr=WHITE, bold=True)
accent_line(s, Inches(0.8), Inches(1.15), Inches(2.5), CYAN, Inches(0.04))
txt(s, Inches(0.8), Inches(1.4), Inches(11), Inches(0.4),
    "一键切换，灯光+温度自动匹配你的当下心情", sz=Pt(14), clr=GRAY)

modes = [
    ("微醺时刻", "6°C | 暖橙光", "下班后的红酒时光\n柔和暖光，慢慢放松", AMBER),
    ("冰爽派对", "2°C | 冰蓝光", "周末朋友来家\n啤酒透心凉，氛围拉满", CYAN),
    ("养生模式", "8°C | 自然绿", "枸杞茶、人参饮\n恒温保存，随时滋养", GREEN),
    ("熬夜补给", "4°C | 霓虹紫", "深夜赶工打游戏\n功能饮料冰镇即取", PURPLE),
]
for i, (title, sub, desc, color) in enumerate(modes):
    x = Inches(0.8 + i * 3.1)
    y = Inches(2.2)
    card_w = Inches(2.8)
    card_h = Inches(3.8)
    rect(s, x, y, card_w, card_h, CARD, rx=0.05)
    # Top accent bar
    rect(s, x, y, card_w, Inches(0.06), color)
    txt(s, x + Inches(0.2), y + Inches(0.4), card_w - Inches(0.4), Inches(0.4),
        title, sz=Pt(18), clr=WHITE, bold=True)
    txt(s, x + Inches(0.2), y + Inches(0.9), card_w - Inches(0.4), Inches(0.3),
        sub, sz=Pt(11), clr=color, bold=True)
    txt(s, x + Inches(0.2), y + Inches(1.5), card_w - Inches(0.4), Inches(1.8),
        desc, sz=Pt(12), clr=GRAY)

# Bottom: modes image
pic(s, IMG("chill_modes.png"), Inches(2.0), Inches(6.2), Inches(9.3), Inches(1.2))
page_number(s, 6)

print("Slides 5-6 done")

# ═══════════════════════════════════════════════════════════════
# SLIDE 7: FULL SCENE
# ═══════════════════════════════════════════════════════════════
s = prs.slides.add_slide(layout)
bg(s)
# Full-bleed scene image
pic(s, IMG("chill_img_2.png"), Inches(0), Inches(0), Inches(13.33), Inches(7.5))
# Overlay
overlay2 = rect(s, Inches(0), Inches(0), Inches(13.33), Inches(7.5), RGBColor(0x0A, 0x0A, 0x0F))
solidFill2 = overlay2.fill._fill
srgb2 = solidFill2.find(qn('a:solidFill')).find(qn('a:srgbClr'))
if srgb2 is not None:
    alpha2 = srgb2.makeelement(qn('a:alpha'), {'val': '28000'})
    srgb2.append(alpha2)

# Quote
txt(s, Inches(1.5), Inches(2.5), Inches(10.3), Inches(1.0),
    "回到家，打开冰仓的那一抹光，\n就是一天中最松弛的时刻。",
    sz=Pt(28), clr=WHITE, bold=False, align=PP_ALIGN.LEFT)
accent_line(s, Inches(1.5), Inches(4.0), Inches(2.0), CYAN, Inches(0.04))
page_number(s, 7)

# ═══════════════════════════════════════════════════════════════
# SLIDE 8: SOCIAL + SOLO
# ═══════════════════════════════════════════════════════════════
s = prs.slides.add_slide(layout)
bg(s)
# Left: Solo
rect(s, Inches(0.5), Inches(0.5), Inches(5.9), Inches(6.5), CARD, rx=0.05)
pic(s, IMG("chill_img_3.png"), Inches(0.7), Inches(0.7), Inches(5.5), Inches(3.2))
txt(s, Inches(0.8), Inches(4.1), Inches(5.3), Inches(0.5),
    "独处模式", sz=Pt(24), clr=CYAN, bold=True)
txt(s, Inches(0.8), Inches(4.7), Inches(5.3), Inches(1.5),
    "一人食、一人饮、一人宅\n打开喜欢的饮料，打开喜欢的剧\n冰仓的微光是最佳陪伴\n不被打扰的私人时刻",
    sz=Pt(13), clr=GRAY)

# Right: Social
rect(s, Inches(6.9), Inches(0.5), Inches(5.9), Inches(6.5), CARD, rx=0.05)
pic(s, IMG("chill_img_2.png"), Inches(7.1), Inches(0.7), Inches(5.5), Inches(3.2))
txt(s, Inches(7.2), Inches(4.1), Inches(5.3), Inches(0.5),
    "社交模式", sz=Pt(24), clr=AMBER, bold=True)
txt(s, Inches(7.2), Inches(4.7), Inches(5.3), Inches(1.5),
    "朋友聚会、游戏之夜、看球赛\n冰仓秒变氛围制造机\n冰啤酒随手拿，RGB灯光燥起来\n让每一次聚会都更有仪式感",
    sz=Pt(13), clr=GRAY)

page_number(s, 8)

print("Slides 7-8 done")

# ═══════════════════════════════════════════════════════════════
# SLIDE 9: BUSINESS MODEL
# ═══════════════════════════════════════════════════════════════
s = prs.slides.add_slide(layout)
bg(s)
txt(s, Inches(0.8), Inches(0.5), Inches(5), Inches(0.6), "商业模式", sz=Pt(36), clr=WHITE, bold=True)
accent_line(s, Inches(0.8), Inches(1.15), Inches(2.5), CYAN, Inches(0.04))

# Left: pricing
rect(s, Inches(0.5), Inches(1.5), Inches(5.9), Inches(5.4), CARD, rx=0.05)
txt(s, Inches(0.8), Inches(1.7), Inches(5.3), Inches(0.5),
    "定价策略", sz=Pt(20), clr=CYAN, bold=True)

pricing = [
    "基础款：¥1,299 — 2温区 + 单色灯",
    "标准款：¥1,799 — 4温区 + 4模式RGB灯",
    "Pro款：¥2,299 — 6温区 + 全彩RGB + App控制",
]
for i, p in enumerate(pricing):
    txt(s, Inches(0.8), Inches(2.5 + i * 0.6), Inches(5.3), Inches(0.5),
        p, sz=Pt(13), clr=WHITE)

txt(s, Inches(0.8), Inches(4.5), Inches(5.3), Inches(0.5),
    "渠道策略", sz=Pt(20), clr=CYAN, bold=True)
channels = ["线上：天猫/京东/抖音电商 + 小红书种草", "线下：海尔门店体验区 + 潮玩集合店"]
for i, ch in enumerate(channels):
    txt(s, Inches(0.8), Inches(5.1 + i * 0.5), Inches(5.3), Inches(0.4),
        ch, sz=Pt(12), clr=GRAY)

# Right: revenue
rect(s, Inches(6.9), Inches(1.5), Inches(5.9), Inches(5.4), CARD, rx=0.05)
txt(s, Inches(7.2), Inches(1.7), Inches(5.3), Inches(0.5),
    "收入预测", sz=Pt(20), clr=GREEN, bold=True)

rev_data = [
    ("Year 1", "5万台", "¥8000万"),
    ("Year 2", "15万台", "¥2.4亿"),
    ("Year 3", "30万台", "¥4.8亿"),
]
for i, (year, vol, rev) in enumerate(rev_data):
    y = Inches(2.5 + i * 1.3)
    rect(s, Inches(7.2), y, Inches(5.3), Inches(1.1), CARD2, rx=0.05)
    txt(s, Inches(7.5), y + Inches(0.1), Inches(1.5), Inches(0.35),
        year, sz=Pt(14), clr=CYAN, bold=True)
    txt(s, Inches(9.2), y + Inches(0.1), Inches(1.3), Inches(0.35),
        vol, sz=Pt(22), clr=WHITE, bold=True, align=PP_ALIGN.CENTER)
    txt(s, Inches(10.8), y + Inches(0.1), Inches(1.5), Inches(0.35),
        rev, sz=Pt(22), clr=GREEN, bold=True, align=PP_ALIGN.RIGHT)

txt(s, Inches(7.2), Inches(6.5), Inches(5.3), Inches(0.3),
    "预计毛利率 35%+，第二年起实现盈利", sz=Pt(11), clr=GRAY)

page_number(s, 9)

# ═══════════════════════════════════════════════════════════════
# SLIDE 10: COMPETITIVE ADVANTAGE
# ═══════════════════════════════════════════════════════════════
s = prs.slides.add_slide(layout)
bg(s)
txt(s, Inches(0.8), Inches(0.5), Inches(5), Inches(0.6), "为什么是我们", sz=Pt(36), clr=WHITE, bold=True)
accent_line(s, Inches(0.8), Inches(1.15), Inches(2.5), CYAN, Inches(0.04))

advantages = [
    ("01", "海尔供应链", "依托海尔全球领先的制冷技术\n和成熟供应链体系\n成本优势+品质保证", CYAN),
    ("02", "情绪洞察先行", "深入Z世代生活方式研究\n不只是卖冷柜，是卖情绪体验\n差异化定位，避开价格战", AMBER),
    ("03", "快速迭代能力", "模块化设计支持快速迭代\n通过App OTA持续更新灯光模式\n建立用户粘性和品牌忠诚度", GREEN),
]
for i, (num, title, desc, color) in enumerate(advantages):
    y = Inches(1.6 + i * 1.8)
    rect(s, Inches(0.5), y, Inches(12.3), Inches(1.6), CARD, rx=0.05)
    txt(s, Inches(0.8), y + Inches(0.2), Inches(0.8), Inches(0.8),
        num, sz=Pt(40), clr=color, bold=True)
    txt(s, Inches(1.8), y + Inches(0.2), Inches(5), Inches(0.4),
        title, sz=Pt(20), clr=WHITE, bold=True)
    txt(s, Inches(1.8), y + Inches(0.7), Inches(10), Inches(0.8),
        desc, sz=Pt(12), clr=GRAY)

page_number(s, 10)

print("Slides 9-10 done")

# ═══════════════════════════════════════════════════════════════
# SLIDE 11: TEAM
# ═══════════════════════════════════════════════════════════════
s = prs.slides.add_slide(layout)
bg(s)
txt(s, Inches(0.8), Inches(0.5), Inches(5), Inches(0.6), "我们的团队", sz=Pt(36), clr=WHITE, bold=True)
accent_line(s, Inches(0.8), Inches(1.15), Inches(2.5), CYAN, Inches(0.04))

# Team members
members = [
    ("任泓博", "产品负责人"), ("刘子涵", "技术负责人"),
    ("李兆木", "供应链"), ("鹿宝祥", "市场策略"),
    ("安文滨", "用户体验"), ("王洪博", "工业设计"),
    ("王志康", "软件开发"), ("臧炳松", "品牌传播"),
    ("赵妹钧", "数据分析"),
]
for i, (name, role) in enumerate(members):
    col = i % 4
    row = i // 4
    x = Inches(0.8 + col * 3.1)
    y = Inches(1.8 + row * 1.8)
    card_w = Inches(2.8)
    rect(s, x, y, card_w, Inches(1.5), CARD, rx=0.05)
    # Avatar circle placeholder
    icon_circle(s, x + Inches(0.15), y + Inches(0.25), CYAN, "", Inches(0.35))
    txt(s, x + Inches(0.7), y + Inches(0.25), card_w - Inches(0.9), Inches(0.35),
        name, sz=Pt(16), clr=WHITE, bold=True)
    txt(s, x + Inches(0.7), y + Inches(0.65), card_w - Inches(0.9), Inches(0.3),
        role, sz=Pt(11), clr=GRAY)

# Mentor
txt(s, Inches(0.8), Inches(5.8), Inches(11), Inches(0.4),
    "导师：吴凌霄", sz=Pt(16), clr=CYAN, bold=True)
txt(s, Inches(0.8), Inches(6.3), Inches(11), Inches(0.4),
    "制冷产业第1组  |  2026海尔智家黑客马拉松创业大赛  |  新研发&管理赛道",
    sz=Pt(11), clr=GRAY)
page_number(s, 11)

# ═══════════════════════════════════════════════════════════════
# SLIDE 12: CLOSE
# ═══════════════════════════════════════════════════════════════
s = prs.slides.add_slide(layout)
bg(s)
# Background image
pic(s, IMG("chill_cover.png"), Inches(0), Inches(0), Inches(13.33), Inches(7.5))
overlay3 = rect(s, Inches(0), Inches(0), Inches(13.33), Inches(7.5), RGBColor(0x0A, 0x0A, 0x0F))
solidFill3 = overlay3.fill._fill
srgb3 = solidFill3.find(qn('a:solidFill')).find(qn('a:srgbClr'))
if srgb3 is not None:
    alpha3 = srgb3.makeelement(qn('a:alpha'), {'val': '50000'})
    srgb3.append(alpha3)

txt(s, Inches(2), Inches(2.2), Inches(9.3), Inches(1.0),
    "情绪冰仓", sz=Pt(52), clr=WHITE, bold=True, align=PP_ALIGN.CENTER)
txt(s, Inches(2), Inches(3.3), Inches(9.3), Inches(0.7),
    "一杯饮尽松弛感", sz=Pt(28), clr=CYAN, bold=False, align=PP_ALIGN.CENTER)
accent_line(s, Inches(5.4), Inches(4.2), Inches(2.5), CYAN, Inches(0.04))
txt(s, Inches(2), Inches(4.6), Inches(9.3), Inches(0.5),
    "Thank You", sz=Pt(24), clr=GRAY, align=PP_ALIGN.CENTER)
txt(s, Inches(2), Inches(5.4), Inches(9.3), Inches(0.5),
    "制冷产业第1组  |  期待您的宝贵意见", sz=Pt(14), clr=GRAY, align=PP_ALIGN.CENTER)

page_number(s, 12)

# ═══════════════════════════════════════════════════════════════
# SAVE
# ═══════════════════════════════════════════════════════════════
prs.save(OUTPUT)
print(f"\nDONE! Saved to: {OUTPUT}")
print(f"Total slides: {len(prs.slides)}")