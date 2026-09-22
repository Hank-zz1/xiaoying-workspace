# -*- coding: utf-8 -*-
"""
ZWCAD 绘图 v12: 完整机械工程图 — A4图框 + GB/T 10609.1标题栏 + 零件图 + 标注 + 技术要求
"""
import ezdxf
from ezdxf import units
from ezdxf.enums import TextEntityAlignment
import os, sys

# ===== 新建 DXF =====
doc = ezdxf.new(dxfversion="R2010")
doc.units = units.MM
msp = doc.modelspace()

# ===== 文字样式: SHX + 大字体 (ZWCAD 中文方案) =====
cn = doc.styles.add("SHX_CN", font="txt.shx")
cn.dxf.bigfont = "gbcbig.shx"
cn.dxf.width = 0.7

# ===== 图层 =====
layer_defs = [
    ("粗实线", 7, 50, "Continuous"),
    ("细实线", 2, 0,  "Continuous"),
    ("中心线", 1, 0,  "CENTER"),
    ("标注",   4, 0,  "Continuous"),
    ("文字",   7, 0,  "Continuous"),
]
for name, color, lw, lt in layer_defs:
    doc.layers.add(name, color=color, lineweight=lw, linetype=lt)

# 中心线线型
try:
    doc.linetypes.add("CENTER", pattern="____ _ ____ _ ____ _ ____ _ ____ _ ", length=31.75)
except:
    pass

# ===== 全局设置 =====
doc.header["$LTSCALE"]  = 0.3
doc.header["$LWDISPLAY"] = 1  # 显示线宽

# ===== 辅助绘图函数 =====
def LN(x1, y1, x2, y2, layer):
    msp.add_line((x1, y1), (x2, y2), dxfattribs={"layer": layer})

def BOX(x1, y1, x2, y2, layer):
    LN(x1, y1, x2, y1, layer)
    LN(x2, y1, x2, y2, layer)
    LN(x2, y2, x1, y2, layer)
    LN(x1, y2, x1, y1, layer)

def TX(x, y, txt, h, halign=0, layer="文字"):
    """halign: 0=左下, 1=居中, 2=右对齐"""
    a = msp.add_text(txt, dxfattribs={"style": "SHX_CN", "layer": layer, "height": h})
    if halign == 1:
        a.set_placement((x, y), align=TextEntityAlignment.MIDDLE_CENTER)
    elif halign == 2:
        a.set_placement((x, y), align=TextEntityAlignment.MIDDLE_RIGHT)
    else:
        a.set_placement((x, y))
    return a

def TXC(x, y, txt, h, layer="文字"):
    return TX(x, y, txt, h, halign=1, layer=layer)

# ===== 标注样式 =====
dim = doc.dimstyles.add("CN_DIM")
dim.dimtxt   = 3.0
dim.dimasz   = 2.5
dim.dimexe   = 1.5
dim.dimexo   = 0.5
dim.dimgap   = 0.8
dim.dimtad   = 1      # 文字在尺寸线上方
dim.dimtih   = 0      # 不强制文字水平
dim.dimtoh   = 0      # 外侧文字也不强制水平
dim.dimtxsty = "SHX_CN"

# ============================================================
# 1. A4 图框 (297×210)
# ============================================================
BOX(0, 0, 297, 210, "细实线")        # 外框 (细)
BOX(25, 5, 292, 205, "粗实线")       # 内框 (粗, 左边25, 其余5)

# ============================================================
# 2. 标题栏 GB/T 10609.1 — 180×56, 右下角
# ============================================================
TBX, TBY = 112.0, 5.0
TW, TH   = 180.0, 56.0

BOX(TBX, TBY, TBX + TW, TBY + TH, "粗实线")   # 外框(粗)

# 列划分 (x 累计偏移)
cols = [10, 16, 22, 32, 46, 60, 70, 84, 98, 112, 130, 150]
for w in cols:
    LN(TBX + w, TBY, TBX + w, TBY + TH, "细实线")

# 行划分 (y 累计偏移, 从下往上, 间隔7mm共8行)
for i in range(1, 8):
    y = TBY + i * 7
    LN(TBX, y, TBX + TW, y, "细实线")

# 图名区竖分隔
LN(TBX + 98, TBY + 21, TBX + 98, TBY + 49, "细实线")

# ---- 标题栏文字 ----
def CELL(xo, w, yo, h, txt, fs=2.5):
    """单元格居中"""
    TXC(TBX + xo + w / 2, TBY + yo + h / 2 - fs * 0.35, txt, fs)

# Row 8 (y=49~56): 标记/处数/分区/更改文件号/签名/年月日/阶段标记/重量/比例
rs8 = [
    (0,10,"标记"), (10,6,"处数"), (16,6,"分区"),
    (22,10,"更改文件号"), (32,14,"签名"), (46,14,"年月日"),
    (60,10,"阶段标记"), (70,14,"重量"), (84,14,"比例"),
]
for xo, w, txt in rs8: CELL(xo, w, 49, 7, txt)

# Row 7 (y=42~49): 设计/标准化/.../共X张第X张
for xo, w, txt in [(0,10,"设计"), (10,6,"标准化"), (22,10,"工艺"), (32,14,"批准")]:
    CELL(xo, w, 42, 7, txt)
CELL(98, 32, 42, 7, "共  张  第  张")

# Row 6 (y=35~42): 审核/日期
CELL(0, 10, 35, 7, "审核")
CELL(10, 6, 35, 7, "日期")

# Row 5 (y=28~35): 批准 + 1:1
CELL(0, 10, 28, 7, "批准")
CELL(84, 14, 28, 7, "1:1")

# 图名大格
TXC(TBX + 141, TBY + 35, "图样名称", 5.5)
TXC(TBX + 141, TBY + 14, "图样代号", 3.5)

# ============================================================
# 3. 零件图: 50×40 外框 + 20×15 内槽
# ============================================================
cx, cy = 158.5, 115.0   # 零件中心
ox1, oy1 = cx - 25, cy - 20   # 外框左下
ox2, oy2 = cx + 25, cy + 20   # 外框右上
ix1, iy1 = cx - 10, cy - 7.5  # 内槽左下
ix2, iy2 = cx + 10, cy + 7.5  # 内槽右上

BOX(ox1, oy1, ox2, oy2, "粗实线")   # 外框
BOX(ix1, iy1, ix2, iy2, "粗实线")   # 内槽

# ============================================================
# 4. 中心线 (超出零件 5mm)
# ============================================================
LN(cx - 30, cy, cx + 30, cy, "中心线")        # 水平中心线
LN(cx, oy1 - 5, cx, oy2 + 5, "中心线")        # 垂直中心线

# ============================================================
# 5. 尺寸标注
# ============================================================
# 20 — 内槽宽度 (下方)
msp.add_linear_dim(
    base=(ix1, iy1), p1=(ix1, iy1), p2=(ix2, iy1),
    location=(cx, oy1 - 13), dimstyle="CN_DIM"
)
# 50 — 外框宽度 (更下方)
msp.add_linear_dim(
    base=(ox1, oy1), p1=(ox1, oy1), p2=(ox2, oy1),
    location=(cx, oy1 - 25), dimstyle="CN_DIM"
)
# 15 — 内槽高度 (右侧)
msp.add_linear_dim(
    base=(ix2, iy1), p1=(ix2, iy1), p2=(ix2, iy2),
    location=(ox2 + 16, (iy1 + iy2) / 2), dimstyle="CN_DIM", angle=90
)
# 40 — 外框高度 (左侧)
msp.add_linear_dim(
    base=(ox1, oy1), p1=(ox1, oy1), p2=(ox1, oy2),
    location=(ox1 - 25, (oy1 + oy2) / 2), dimstyle="CN_DIM", angle=90
)

# ============================================================
# 6. 技术要求
# ============================================================
TX(30, 185, "技术要求", 4.0)
reqs = [
    "1. 棱边倒角 C1；",
    "2. 未注尺寸公差按 GB/T1804-m 执行；",
    "3. 表面粗糙度为 Ra 3.2。",
]
for i, line in enumerate(reqs):
    TX(30, 178 - i * 5, line, 2.5)

# ============================================================
# 7. 图纸信息
# ============================================================
TX(30, 198, "共 1 张", 3.5)
TX(30, 192, "第 1 张", 3.5)

# ============================================================
# 保存 & 打开
# ============================================================
path = "C:/Users/26011970/Desktop/zwcad_v12.dxf"
doc.saveas(path)
print("SAVED: " + path)

try:
    import win32com.client
    acad = win32com.client.Dispatch("ZWCAD.Application")
    acad.Visible = True
    # 关闭已占用的同名文件
    for d in list(acad.Documents):
        try:
            if d.FullName.replace("\\", "/").lower() == path.lower():
                d.Close(False)
        except:
            pass
    acad.Documents.Open(path)
    # 执行 zoom extents
    try: acad.ZoomExtents()
    except: pass
    print("Opened in ZWCAD")
except Exception as e:
    print("ZWCAD COM error: " + str(e)[:120])
    print("请手动打开: " + path)

print("v12 done — " + str(len(list(msp))) + " entities")