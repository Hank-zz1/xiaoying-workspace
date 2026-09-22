import sys
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

prs = Presentation()
prs.slide_width = Inches(10)
prs.slide_height = Inches(5.625)

# ===== Palette =====
NAVY = "1B2A4A"
GOLD = "D4A843"
WHITE = "FFFFFF"
LIGHT_GOLD = "F5E6C8"
DARK_BG = "0F1B33"
ACCENT_BLUE = "3B5998"
LIGHT_BLUE = "C8D6E5"
GRAY = "A0AEC0"
DARK_GRAY = "2D3748"

def add_bg(slide, color_hex):
    bg = slide.background
    fill = bg.fill
    fill.solid()
    fill.fore_color.rgb = RGBColor(*hex_to_rgb(color_hex))

def hex_to_rgb(h):
    return (int(h[0:2],16), int(h[2:4],16), int(h[4:6],16))

def add_rect(slide, x, y, w, h, fill_color, line_color=None, line_width=None):
    shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(x), Inches(y), Inches(w), Inches(h))
    shape.fill.solid()
    shape.fill.fore_color.rgb = RGBColor(*hex_to_rgb(fill_color))
    if line_color:
        shape.line.color.rgb = RGBColor(*hex_to_rgb(line_color))
        shape.line.width = Pt(line_width or 1)
    else:
        shape.line.fill.background()
    return shape

def add_rounded_rect(slide, x, y, w, h, fill_color):
    shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x), Inches(y), Inches(w), Inches(h))
    shape.fill.solid()
    shape.fill.fore_color.rgb = RGBColor(*hex_to_rgb(fill_color))
    shape.line.fill.background()
    return shape

def add_text(slide, text, x, y, w, h, font_size=18, color_hex=WHITE, bold=False, align=PP_ALIGN.LEFT, font_name="Calibri"):
    txBox = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = txBox.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = text
    p.font.size = Pt(font_size)
    p.font.color.rgb = RGBColor(*hex_to_rgb(color_hex))
    p.font.bold = bold
    p.font.name = font_name
    p.alignment = align
    return txBox

def add_gold_line(slide, x, y, w):
    shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(x), Inches(y), Inches(w), Inches(0.03))
    shape.fill.solid()
    shape.fill.fore_color.rgb = RGBColor(*hex_to_rgb(GOLD))
    shape.line.fill.background()

# ===== SLIDE 1: COVER =====
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide, DARK_BG)
add_rect(slide, 0, 0, 10, 0.08, GOLD)
add_rect(slide, 0, 5.545, 10, 0.08, GOLD)
add_rect(slide, 0.5, 0.8, 0.06, 3.5, GOLD)
add_text(slide, "2026 FIFA 世界杯", 1.0, 1.0, 8.5, 1.2, font_size=40, color_hex=WHITE, bold=True)
add_text(slide, "美 加 墨 三 国 联 合 承 办", 1.0, 2.1, 8.5, 0.6, font_size=22, color_hex=GOLD, bold=True)
add_gold_line(slide, 1.0, 2.8, 4.0)
add_text(slide, "2026年6月11日 - 7月19日  |  48支球队  |  16座城市  |  104场比赛", 1.0, 3.0, 8.5, 0.6, font_size=14, color_hex=LIGHT_GOLD)
add_text(slide, "赛 程 前 瞻 全 景 解 读", 1.0, 3.7, 8.5, 0.6, font_size=18, color_hex=WHITE, bold=True)
add_text(slide, "2026年4月", 7.5, 5.1, 2.0, 0.4, font_size=11, color_hex=GRAY)

# ===== SLIDE 2: 赛事概览 =====
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide, WHITE)
add_rect(slide, 0, 0, 10, 1.1, NAVY)
add_text(slide, "赛事概览", 0.6, 0.2, 5, 0.7, font_size=28, color_hex=WHITE, bold=True)
add_gold_line(slide, 0.6, 0.85, 2.5)
stats = [
    ("48支", "参赛球队", "首次扩军"),
    ("12个", "小组数量", "每组4队"),
    ("104场", "比赛场次", "较以往+63%"),
    ("16座", "举办城市", "美加墨三国"),
    ("39天", "赛程跨度", "6.11-7.19"),
    ("32强", "淘汰赛规模", "历史首次"),
]
for i, (val, label, note) in enumerate(stats):
    col = i % 3
    row = i // 3
    bx = 0.6 + col * 3.2
    by = 1.4 + row * 2.1
    add_rounded_rect(slide, bx, by, 2.9, 1.7, "F7F9FC")
    add_rect(slide, bx, by, 2.9, 0.06, GOLD)
    add_text(slide, val, bx + 0.15, by + 0.15, 2.6, 0.7, font_size=36, color_hex=NAVY, bold=True, align=PP_ALIGN.CENTER)
    add_text(slide, label, bx + 0.15, by + 0.8, 2.6, 0.4, font_size=14, color_hex=DARK_GRAY, bold=True, align=PP_ALIGN.CENTER)
    add_text(slide, note, bx + 0.15, by + 1.2, 2.6, 0.4, font_size=11, color_hex=GRAY, align=PP_ALIGN.CENTER)

# ===== SLIDE 3: 关键时间轴 =====
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide, DARK_BG)
add_rect(slide, 0, 0, 10, 1.1, "15203A")
add_text(slide, "关键时间轴", 0.6, 0.2, 5, 0.7, font_size=28, color_hex=WHITE, bold=True)
add_gold_line(slide, 0.6, 0.85, 2.5)
timeline = [
    ("6月12日", "揭幕战", "墨西哥 vs 南非\n墨西哥城·阿兹台克球场"),
    ("6月12-27日", "小组赛", "12个小组共72场比赛\n小组前2名+8个最佳第3晋级"),
    ("6月29-30日", "1/16决赛", "32支球队展开淘汰赛首战\n历史首次新增16强轮次"),
    ("7月2-4日", "1/8决赛", "16强决出8个席位\n强强对话上演"),
    ("7月8-9日", "1/4决赛", "8支球队争夺半决赛名额\n巅峰对决"),
    ("7月14日", "半决赛", "4支球队冲击决赛\n亚特兰大 / 达拉斯"),
    ("7月19日", "决赛", "纽约大都会球场\n见证新冠军的诞生"),
]
add_rect(slide, 5.0, 1.5, 0.03, 3.8, GOLD)
for i, (date, title, desc) in enumerate(timeline):
    y = 1.35 + i * 0.55
    dot = slide.shapes.add_shape(MSO_SHAPE.OVAL, Inches(4.92), Inches(y), Inches(0.18), Inches(0.18))
    dot.fill.solid()
    dot.fill.fore_color.rgb = RGBColor(*hex_to_rgb(GOLD))
    dot.line.fill.background()
    add_text(slide, date, 0.6, y - 0.05, 1.8, 0.35, font_size=13, color_hex=GOLD, bold=True)
    add_text(slide, title, 0.6, y + 0.25, 1.8, 0.3, font_size=12, color_hex=WHITE, bold=True)
    add_text(slide, desc, 5.3, y - 0.05, 4.3, 0.5, font_size=11, color_hex=LIGHT_GOLD)

# ===== SLIDE 4: 16座举办城市 =====
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide, WHITE)
add_rect(slide, 0, 0, 10, 1.1, NAVY)
add_text(slide, "16座举办城市", 0.6, 0.2, 5, 0.7, font_size=28, color_hex=WHITE, bold=True)
add_gold_line(slide, 0.6, 0.85, 2.5)
cities_data = [
    ("美国（11座）", ACCENT_BLUE, [
        "纽约 · 大都会球场 · 87,157人",
        "达拉斯 · AT&T球场 · 96,267人",
        "亚特兰大 · 奔驰球场 · 75,000人",
        "堪萨斯城 · 箭头球场 · 76,640人",
        "休斯顿 · NRG球场 · 72,220人",
        "旧金山 · 李维斯球场 · 70,909人",
        "洛杉矶 · SoFi球场 · 70,240人",
        "波士顿 · 吉列球场 · 70,000人",
        "西雅图 · 流明球场 · 69,000人",
        "费城 · 林肯金融球场 · 69,328人",
        "迈阿密 · 硬岩球场 · 67,518人",
    ]),
    ("加拿大（2座）", "27678C", [
        "温哥华 · 卑诗体育馆 · 54,500人",
        "多伦多 · BMO球场 · 45,500人",
    ]),
    ("墨西哥（3座）", "C4A000", [
        "墨西哥城 · 阿兹台克球场 · 87,523人",
        "蒙特雷 · BBVA球场 · 53,460人",
        "瓜达拉哈拉 · 阿克龙球场 · 48,071人",
    ]),
]
for ci, (title, accent_color, cities) in enumerate(cities_data):
    cx = 0.5 + ci * 3.2
    add_rounded_rect(slide, cx, 1.3, 2.95, 0.5, accent_color)
    add_text(slide, title, cx + 0.15, 1.35, 2.7, 0.4, font_size=14, color_hex=WHITE, bold=True)
    for j, city in enumerate(cities):
        y = 1.9 + j * 0.33
        add_rect(slide, cx + 0.1, y, 0.04, 0.04, accent_color)
        add_text(slide, city, cx + 0.25, y - 0.02, 2.6, 0.3, font_size=10, color_hex=DARK_GRAY)

# ===== SLIDE 5: 小组赛分组 A-F =====
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide, WHITE)
add_rect(slide, 0, 0, 10, 1.1, NAVY)
add_text(slide, "小组赛分组  A-F组", 0.6, 0.2, 6, 0.7, font_size=28, color_hex=WHITE, bold=True)
add_gold_line(slide, 0.6, 0.85, 2.5)
groups_af = [
    ("A组", "墨西哥城揭幕战", ["墨西哥", "南非", "韩国", "捷克"]),
    ("B组", "东道主加拿大", ["加拿大", "波黑", "卡塔尔", "瑞士"]),
    ("C组", "五星巴西登场", ["巴西", "摩洛哥", "海地", "苏格兰"]),
    ("D组", "美国主场优势", ["美国", "巴拉圭", "澳大利亚", "土耳其"]),
    ("E组", "日耳曼战车", ["德国", "库拉索", "科特迪瓦", "厄瓜多尔"]),
    ("F组", "全攻全守对决", ["荷兰", "日本", "瑞典", "突尼斯"]),
]
for i, (grp, tag, teams) in enumerate(groups_af):
    col = i % 3
    row = i // 3
    cx = 0.5 + col * 3.25
    cy = 1.3 + row * 2.15
    add_rounded_rect(slide, cx, cy, 3.05, 1.95, "F0F4F8")
    add_rect(slide, cx, cy, 3.05, 0.45, NAVY)
    add_text(slide, grp, cx + 0.15, cy + 0.05, 1.2, 0.35, font_size=14, color_hex=WHITE, bold=True)
    add_text(slide, tag, cx + 1.3, cy + 0.07, 1.5, 0.3, font_size=10, color_hex=GOLD)
    for j, team in enumerate(teams):
        ty = cy + 0.55 + j * 0.32
        dot = slide.shapes.add_shape(MSO_SHAPE.OVAL, Inches(cx + 0.2), Inches(ty), Inches(0.12), Inches(0.12))
        dot.fill.solid()
        dot.fill.fore_color.rgb = RGBColor(*hex_to_rgb(ACCENT_BLUE if j < 2 else GRAY))
        dot.line.fill.background()
        add_text(slide, team, cx + 0.4, ty - 0.02, 2.4, 0.28, font_size=12, color_hex=DARK_GRAY)

# ===== SLIDE 6: 小组赛分组 G-L =====
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide, WHITE)
add_rect(slide, 0, 0, 10, 1.1, NAVY)
add_text(slide, "小组赛分组  G-L组", 0.6, 0.2, 6, 0.7, font_size=28, color_hex=WHITE, bold=True)
add_gold_line(slide, 0.6, 0.85, 2.5)
groups_gl = [
    ("G组", "欧洲红魔首战", ["比利时", "埃及", "伊朗", "新西兰"]),
    ("H组", "传控西班牙", ["西班牙", "佛得角", "沙特", "乌拉圭"]),
    ("I组", "卫冕冠军法国", ["法国", "塞内加尔", "伊拉克", "挪威"]),
    ("J组", "潘帕斯雄鹰", ["阿根廷", "阿尔及利亚", "奥地利", "约旦"]),
    ("K组", "五盾军团", ["葡萄牙", "刚果(金)", "乌兹别克斯坦", "哥伦比亚"]),
    ("L组", "三狮军团", ["英格兰", "克罗地亚", "加纳", "巴拿马"]),
]
for i, (grp, tag, teams) in enumerate(groups_gl):
    col = i % 3
    row = i // 3
    cx = 0.5 + col * 3.25
    cy = 1.3 + row * 2.15
    add_rounded_rect(slide, cx, cy, 3.05, 1.95, "F0F4F8")
    add_rect(slide, cx, cy, 3.05, 0.45, NAVY)
    add_text(slide, grp, cx + 0.15, cy + 0.05, 1.2, 0.35, font_size=14, color_hex=WHITE, bold=True)
    add_text(slide, tag, cx + 1.3, cy + 0.07, 1.5, 0.3, font_size=10, color_hex=GOLD)
    for j, team in enumerate(teams):
        ty = cy + 0.55 + j * 0.32
        dot = slide.shapes.add_shape(MSO_SHAPE.OVAL, Inches(cx + 0.2), Inches(ty), Inches(0.12), Inches(0.12))
        dot.fill.solid()
        dot.fill.fore_color.rgb = RGBColor(*hex_to_rgb(ACCENT_BLUE if j < 2 else GRAY))
        dot.line.fill.background()
        add_text(slide, team, cx + 0.4, ty - 0.02, 2.4, 0.28, font_size=12, color_hex=DARK_GRAY)

# ===== SLIDE 7: 小组赛完整赛程 第一轮 =====
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide, DARK_BG)
add_rect(slide, 0, 0, 10, 1.1, "15203A")
add_text(slide, "小组赛第一轮赛程  6月12日-18日", 0.6, 0.2, 8, 0.7, font_size=24, color_hex=WHITE, bold=True)
add_gold_line(slide, 0.6, 0.85, 3.0)
sched_all = [
    ("6/12 03:00", "揭幕战", "墨西哥 vs 南非", "墨西哥城"),
    ("6/12 10:00", "A组", "韩国 vs 捷克", "瓜达拉哈拉"),
    ("6/13 03:00", "B组", "加拿大 vs 波黑", "多伦多"),
    ("6/13 09:00", "D组", "美国 vs 巴拉圭", "洛杉矶"),
    ("6/14 03:00", "B组", "卡塔尔 vs 瑞士", "旧金山"),
    ("6/14 06:00", "C组", "巴西 vs 摩洛哥", "纽约"),
    ("6/14 09:00", "C组", "海地 vs 苏格兰", "波士顿"),
    ("6/14 12:00", "D组", "澳大利亚 vs 土耳其", "温哥华"),
    ("6/15 01:00", "E组", "德国 vs 库拉索", "休斯顿"),
    ("6/15 04:00", "F组", "荷兰 vs 日本", "达拉斯"),
    ("6/15 07:00", "E组", "科特迪瓦 vs 厄瓜多尔", "费城"),
    ("6/15 10:00", "F组", "瑞典 vs 突尼斯", "蒙特雷"),
    ("6/16 00:00", "H组", "西班牙 vs 佛得角", "亚特兰大"),
    ("6/16 03:00", "G组", "比利时 vs 埃及", "西雅图"),
    ("6/16 06:00", "H组", "沙特 vs 乌拉圭", "迈阿密"),
    ("6/16 09:00", "G组", "伊朗 vs 新西兰", "洛杉矶"),
    ("6/17 03:00", "I组", "法国 vs 塞内加尔", "纽约"),
    ("6/17 06:00", "I组", "伊拉克 vs 挪威", "波士顿"),
    ("6/17 09:00", "J组", "阿根廷 vs 阿尔及利亚", "堪萨斯城"),
    ("6/17 12:00", "J组", "奥地利 vs 约旦", "旧金山"),
    ("6/18 01:00", "K组", "葡萄牙 vs 刚果(金)", "休斯顿"),
    ("6/18 04:00", "K组", "乌兹别克 vs 哥伦比亚", "达拉斯"),
    ("6/18 07:00", "L组", "英格兰 vs 克罗地亚", "亚特兰大"),
    ("6/18 09:00", "L组", "加纳 vs 巴拿马", "西雅图"),
]
for ci in range(2):
    bx = 0.5 + ci * 5.0
    start = ci * 12
    for i, (time, tag, match, venue) in enumerate(sched_all[start:start+12]):
        y = 1.25 + i * 0.35
        add_rounded_rect(slide, bx, y, 4.6, 0.32, "1A2844")
        add_text(slide, time, bx + 0.1, y + 0.02, 1.2, 0.28, font_size=9, color_hex=GOLD, bold=True)
        add_text(slide, tag, bx + 1.3, y + 0.02, 0.8, 0.28, font_size=8, color_hex=ACCENT_BLUE, bold=True)
        add_text(slide, match, bx + 2.1, y + 0.02, 1.6, 0.28, font_size=10, color_hex=WHITE, bold=True)
        add_text(slide, venue, bx + 3.6, y + 0.04, 0.9, 0.25, font_size=8, color_hex=GRAY)

# ===== SLIDE 8: 焦点对决前瞻 =====
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide, WHITE)
add_rect(slide, 0, 0, 10, 1.1, NAVY)
add_text(slide, "焦点对决前瞻", 0.6, 0.2, 5, 0.7, font_size=28, color_hex=WHITE, bold=True)
add_gold_line(slide, 0.6, 0.85, 2.5)
matchups = [
    ("巴西 vs 摩洛哥", "6月14日 · 纽约", "C组首轮", "桑巴军团迎战非洲劲旅，摩洛哥作为2022世界杯四强不容小觑"),
    ("荷兰 vs 日本", "6月15日 · 达拉斯", "F组首轮", "全攻全守对技术流，蓝武士能否再次创造奇迹"),
    ("法国 vs 塞内加尔", "6月17日 · 纽约", "I组首轮", "卫冕冠军出征，塞内加尔拥有马内等球星实力不俗"),
    ("阿根廷 vs 阿尔及利亚", "6月17日 · 堪萨斯城", "J组首轮", "潘帕斯雄鹰冲击卫冕之路，首战不可有任何闪失"),
    ("英格兰 vs 克罗地亚", "6月18日 · 亚特兰大", "L组首轮", "2018世界杯恩怨再现，L组强强对话"),
    ("挪威 vs 法国", "6月27日 · I组第3轮", "关键战", "哈兰德领衔的挪威挑战卫冕冠军，小组赛末轮焦点"),
]
for i, (match, time_tag, grp_tag, desc) in enumerate(matchups):
    col = i % 2
    row = i // 2
    bx = 0.5 + col * 4.9
    by = 1.3 + row * 1.45
    add_rounded_rect(slide, bx, by, 4.65, 1.3, "F7F9FC")
    add_rect(slide, bx, by, 4.65, 0.05, GOLD)
    add_rect(slide, bx + 0.05, by + 0.1, 0.05, 0.35, NAVY)
    add_text(slide, match, bx + 0.2, by + 0.05, 3.5, 0.35, font_size=16, color_hex=NAVY, bold=True)
    add_text(slide, f"{grp_tag}  |  {time_tag}", bx + 0.2, by + 0.35, 4.2, 0.25, font_size=9, color_hex=GRAY)
    add_text(slide, desc, bx + 0.15, by + 0.65, 4.3, 0.55, font_size=10, color_hex=DARK_GRAY)

# ===== SLIDE 9: 赛制变化解读 =====
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide, WHITE)
add_rect(slide, 0, 0, 10, 1.1, NAVY)
add_text(slide, "赛制变化解读", 0.6, 0.2, 5, 0.7, font_size=28, color_hex=WHITE, bold=True)
add_gold_line(slide, 0.6, 0.85, 2.5)
add_rounded_rect(slide, 0.5, 1.4, 4.3, 1.9, "F0F4F8")
add_text(slide, "旧赛制（32队时代）", 0.7, 1.5, 3.5, 0.4, font_size=16, color_hex=NAVY, bold=True)
add_gold_line(slide, 0.7, 1.85, 1.5)
old_items = ["32支球队参赛", "8个小组，每组4队", "小组赛共48场", "小组前2名晋级16强", "淘汰赛共16场", "总场次：64场", "赛程：32天"]
for i, item in enumerate(old_items):
    add_text(slide, "  " + item, 0.7, 1.95 + i * 0.25, 3.8, 0.25, font_size=11, color_hex=DARK_GRAY)
add_rounded_rect(slide, 5.2, 1.4, 4.3, 1.9, "F5F0E0")
add_text(slide, "新赛制（48队时代）", 5.4, 1.5, 3.5, 0.4, font_size=16, color_hex=NAVY, bold=True)
add_gold_line(slide, 5.4, 1.85, 1.5)
new_items = ["48支球队参赛（首次扩军）", "12个小组，每组4队", "小组赛共72场", "前2名+8个最佳第3晋级32强", "新增1/16决赛，淘汰赛共32场", "总场次：104场", "赛程：39天"]
for i, item in enumerate(new_items):
    add_text(slide, "  " + item, 5.4, 1.95 + i * 0.25, 3.8, 0.25, font_size=11, color_hex=DARK_GRAY)
add_rounded_rect(slide, 0.5, 3.6, 9.0, 1.7, NAVY)
add_text(slide, "关键变化", 0.7, 3.7, 2, 0.35, font_size=14, color_hex=GOLD, bold=True)
changes = [
    "小组赛出线规则：积分相同依次比较 净胜球 → 进球数 → 公平竞技分 → 抽签决定",
    "淘汰赛新增 1/16 决赛（32强），从32强直接到决赛的赛制成为历史",
    "比赛场次从64场增至104场，球员体能管理成为各队关键考量",
    "半决赛在亚特兰大和达拉斯举行，决赛在纽约大都会球场",
]
for i, c in enumerate(changes):
    add_text(slide, "• " + c, 0.7, 4.05 + i * 0.3, 8.5, 0.28, font_size=10, color_hex=LIGHT_GOLD)

# ===== SLIDE 10: 冠军热门分析 =====
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide, DARK_BG)
add_rect(slide, 0, 0, 10, 1.1, "15203A")
add_text(slide, "冠军热门分析", 0.6, 0.2, 5, 0.7, font_size=28, color_hex=WHITE, bold=True)
add_gold_line(slide, 0.6, 0.85, 2.5)
hot_teams = [
    ("阿根廷", "卫冕冠军", "梅西等核心球员，2022世界杯冠军", "J组出线无悬念，关键在淘汰赛"),
    ("法国", "卫冕亚军", "姆巴佩领衔的豪华锋线", "I组面临塞内加尔和挪威挑战"),
    ("巴西", "五星巴西", "维尼修斯、罗德里戈等新星", "C组需防摩洛哥黑马"),
    ("英格兰", "三狮军团", "贝林厄姆、萨卡、福登黄金一代", "L组克罗地亚是最大障碍"),
    ("西班牙", "传控王者", "亚马尔等新生代崛起", "H组乌拉圭不可轻视"),
    ("德国", "日耳曼战车", "穆西亚拉领衔，北美主场优势", "E组需稳扎稳打"),
    ("葡萄牙", "五盾军团", "莱奥、B费、B席进攻组合", "K组哥伦比亚是强敌"),
    ("荷兰", "全攻全守", "后防稳固，中场控制力强", "F组日本是潜在威胁"),
]
for i, (team, title, desc, note) in enumerate(hot_teams):
    col = i % 4
    row = i // 4
    bx = 0.4 + col * 2.4
    by = 1.3 + row * 2.1
    add_rounded_rect(slide, bx, by, 2.2, 1.9, "1A2844")
    add_rect(slide, bx, by, 2.2, 0.05, GOLD)
    add_text(slide, team, bx + 0.15, by + 0.15, 1.5, 0.35, font_size=16, color_hex=WHITE, bold=True)
    add_text(slide, title, bx + 0.15, by + 0.45, 1.8, 0.25, font_size=10, color_hex=GOLD, bold=True)
    add_text(slide, desc, bx + 0.15, by + 0.75, 1.9, 0.5, font_size=9, color_hex=LIGHT_GOLD)
    add_text(slide, note, bx + 0.15, by + 1.4, 1.9, 0.25, font_size=9, color_hex=GRAY)

# ===== SLIDE 11: 淘汰赛结构 =====
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide, WHITE)
add_rect(slide, 0, 0, 10, 1.1, NAVY)
add_text(slide, "淘汰赛对阵结构", 0.6, 0.2, 5, 0.7, font_size=28, color_hex=WHITE, bold=True)
add_gold_line(slide, 0.6, 0.85, 2.5)
bracket_stages = [
    ("阶段", "场次", "晋级", "日期"),
    ("1/16决赛", "16场", "32强 → 16强", "6月29-30日"),
    ("1/8决赛", "8场", "16强 → 8强", "7月2-4日"),
    ("1/4决赛", "4场", "8强 → 4强", "7月8-9日"),
    ("半决赛", "2场", "4强 → 2强", "7月14日"),
    ("三四名决赛", "1场", "季军争夺", "7月18日"),
    ("决赛", "1场", "冠军争夺", "7月19日"),
]
col_widths = [2.0, 1.5, 2.5, 2.5]
start_x = 1.5
start_y = 1.4
for i, (stage, matches, progress, date) in enumerate(bracket_stages):
    is_header = (i == 0)
    bg_color = NAVY if is_header else ("F7F9FC" if i % 2 == 1 else WHITE)
    text_color = WHITE if is_header else DARK_GRAY
    font_weight = True if is_header else False
    for ci, cell in enumerate([stage, matches, progress, date]):
        cx = start_x + sum(col_widths[:ci])
        add_rect(slide, cx + 0.05, start_y + i * 0.55, col_widths[ci] - 0.1, 0.52, bg_color, "E0E0E0", 0.5)
        add_text(slide, cell, cx + 0.1, start_y + i * 0.55 + 0.08, col_widths[ci] - 0.2, 0.35,
                 font_size=12, color_hex=text_color, bold=font_weight, align=PP_ALIGN.CENTER)

# ===== SLIDE 12: 亚洲球队展望 =====
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide, WHITE)
add_rect(slide, 0, 0, 10, 1.1, NAVY)
add_text(slide, "亚洲球队展望  9支参赛队创历史", 0.6, 0.2, 7, 0.7, font_size=26, color_hex=WHITE, bold=True)
add_gold_line(slide, 0.6, 0.85, 2.5)
asian_teams = [
    ("日本", "F组", "荷兰、瑞典、突尼斯", "技术细腻，旅欧球员众多，有望小组出线"),
    ("韩国", "A组", "墨西哥、南非、捷克", "孙兴慜领衔，揭幕战组别，力争出线"),
    ("伊朗", "G组", "比利时、埃及、新西兰", "亚洲传统强队，小组出线存在挑战"),
    ("澳大利亚", "D组", "美国、巴拉圭、土耳其", "身体优势，与东道主美国同组"),
    ("沙特", "H组", "西班牙、佛得角、乌拉圭", "技术流代表，与西班牙乌拉圭同组"),
    ("卡塔尔", "B组", "加拿大、波黑、瑞士", "东道主亚洲兄弟，经验是关键"),
    ("约旦", "J组", "阿根廷、阿尔及利亚、奥地利", "黑马之姿，与阿根廷同组挑战巨大"),
    ("伊拉克", "I组", "法国、塞内加尔、挪威", "时隔40年重返，与法国挪威同组"),
    ("乌兹别克斯坦", "K组", "葡萄牙、刚果(金)、哥伦比亚", "中亚铁骑，首次参赛需稳扎稳打"),
]
for i, (team, group, opponents, preview) in enumerate(asian_teams):
    col = i % 3
    row = i // 3
    bx = 0.4 + col * 3.2
    by = 1.3 + row * 1.4
    add_rounded_rect(slide, bx, by, 3.0, 1.25, "F7F9FC")
    add_rect(slide, bx, by, 3.0, 0.04, GOLD)
    add_rect(slide, bx + 0.08, by + 0.1, 0.04, 0.35, ACCENT_BLUE)
    add_text(slide, f"{team}  ·  {group}", bx + 0.2, by + 0.05, 2.0, 0.3, font_size=13, color_hex=NAVY, bold=True)
    add_text(slide, f"同组: {opponents}", bx + 0.15, by + 0.38, 2.7, 0.25, font_size=9, color_hex=GRAY)
    add_text(slide, preview, bx + 0.15, by + 0.68, 2.7, 0.5, font_size=10, color_hex=DARK_GRAY)

# ===== SLIDE 13: 观赛指南 =====
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide, DARK_BG)
add_rect(slide, 0, 0, 10, 1.1, "15203A")
add_text(slide, "观赛指南", 0.6, 0.2, 3, 0.7, font_size=28, color_hex=WHITE, bold=True)
add_gold_line(slide, 0.6, 0.85, 2.5)
guides = [
    ("时差提醒", "美东时间比北京时间晚12小时，大部分比赛在北京时间0:00-12:00进行，部分比赛需熬夜观看"),
    ("揭幕战", "北京时间6月12日凌晨3:00，墨西哥 vs 南非，墨西哥城阿兹台克球场"),
    ("决赛", "北京时间7月20日凌晨3:00，纽约大都会球场，见证新冠军诞生"),
    ("转播信息", "国内转播权由央视体育、咪咕视频等平台获得，关注官方渠道获取直播安排"),
    ("气候注意", "北美夏季炎热，部分比赛安排在室内场馆或晚间进行，注意防暑"),
]
for i, (title, desc) in enumerate(guides):
    y = 1.35 + i * 0.8
    add_rounded_rect(slide, 0.5, y, 9.0, 0.7, "1A2844")
    badge = slide.shapes.add_shape(MSO_SHAPE.OVAL, Inches(0.75), Inches(y + 0.12), Inches(0.35), Inches(0.35))
    badge.fill.solid()
    badge.fill.fore_color.rgb = RGBColor(*hex_to_rgb(GOLD))
    badge.line.fill.background()
    add_text(slide, str(i + 1), 0.78, y + 0.13, 0.3, 0.3, font_size=13, color_hex=NAVY, bold=True, align=PP_ALIGN.CENTER)
    add_text(slide, title, 1.3, y + 0.05, 1.2, 0.3, font_size=14, color_hex=GOLD, bold=True)
    add_text(slide, desc, 1.3, y + 0.35, 8.0, 0.3, font_size=11, color_hex=LIGHT_GOLD)

# ===== SLIDE 14: 结束页 =====
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide, DARK_BG)
add_rect(slide, 0, 0, 10, 0.08, GOLD)
add_rect(slide, 0, 5.545, 10, 0.08, GOLD)
add_rect(slide, 0, 0, 0.08, 5.625, GOLD)
add_rect(slide, 9.92, 0, 0.08, 5.625, GOLD)
add_text(slide, "2026 FIFA WORLD CUP", 1.0, 1.2, 8.0, 1.0, font_size=32, color_hex=GOLD, bold=True, align=PP_ALIGN.CENTER)
add_gold_line(slide, 2.5, 2.2, 5.0)
add_text(slide, "6月11日  —  7月19日", 1.0, 2.4, 8.0, 0.6, font_size=20, color_hex=WHITE, bold=True, align=PP_ALIGN.CENTER)
add_text(slide, "美国  ·  加拿大  ·  墨西哥", 1.0, 3.1, 8.0, 0.5, font_size=16, color_hex=LIGHT_GOLD, align=PP_ALIGN.CENTER)
add_text(slide, "足球的盛宴，世界的狂欢", 1.0, 3.8, 8.0, 0.5, font_size=14, color_hex=GRAY, align=PP_ALIGN.CENTER)
add_text(slide, "2026年4月制作", 1.0, 4.8, 8.0, 0.4, font_size=11, color_hex=GRAY, align=PP_ALIGN.CENTER)

# Save
output_path = r"C:\Users\26011970\.incaier-agent\workspaces\my-workspace\sessions\260420-early-thistle\data\2026美加墨世界杯赛程前瞻.pptx"
prs.save(output_path)
print(f"Saved to {output_path}")
