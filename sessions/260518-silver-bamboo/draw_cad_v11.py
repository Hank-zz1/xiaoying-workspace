# -*- coding: utf-8 -*-
"""
ZWCAD 绘图 v11: ezdxf 生成 DXF + 线宽显示 + 细节修正
"""
import ezdxf
from ezdxf import units
from ezdxf.enums import TextEntityAlignment
import os, time

# ===== 新建 DXF =====
doc = ezdxf.new(dxfversion="R2010")
doc.units = units.MM
msp = doc.modelspace()

# ===== 文字样式 =====
cn_style = doc.styles.add("SHX_CN", font="txt.shx")
cn_style.dxf.bigfont = "gbcbig.shx"
cn_style.dxf.width = 0.7

# ===== 图层 =====
LY = {
    "粗实线": {"color": 7, "lineweight": 50},
    "细实线": {"color": 2, "lineweight": 0},
    "中心线": {"color": 1, "lineweight": 0, "linetype": "CENTER"},
    "标注":   {"color": 4, "lineweight": 0},
    "文字":   {"color": 7, "lineweight": 0},
}
for name, props in LY.items():
    lt = props.pop("linetype", "Continuous")
    doc.layers.add(name, color=props["color"], lineweight=props["lineweight"], linetype=lt)

# 中心线线型
try: doc.linetypes.add("CENTER", pattern="____ _ ____ _ ____ _ ____ _ ____ _ ", length=31.75)
except: pass

# ===== 全局设置 =====
doc.header["$LTSCALE"] = 0.25
doc.header["$LWDISPLAY"] = 1  # 显示线宽

# ===== 辅助函数 =====
def LN(x1, y1, x2, y2, layer):
    msp.add_line((x1, y1), (x2, y2), dxfattribs={"layer": layer})

def BOX(x1, y1, x2, y2, layer):
    LN(x1, y1, x2, y1, layer)
    LN(x2, y1, x2, y2, layer)
    LN(x2, y2, x1, y2, layer)
    LN(x1, y2, x1, y1, layer)

def TX(x, y, txt, h, style="SHX_CN", layer="文字", halign=0):
    a = msp.add_text(txt, dxfattribs={"style": style, "layer": layer, "height": h})
    if halign == 1:
        a.set_placement((x, y), align=TextEntityAlignment.MIDDLE_CENTER)
    elif halign == 2:
        a.set_placement((x, y), align=TextEntityAlignment.MIDDLE_RIGHT)
    else:
        a.set_placement((x, y))
    return a

def TXC(x, y, txt, h, style="SHX_CN", layer="文字"):
    return TX(x, y, txt, h, style, layer, halign=1)

# ===== DIM 样式 =====
dimstyle = doc.dimstyles.add("CN_DIM")
dimstyle.dimtxt = 3.0
dimstyle.dimasz = 2.5
dimstyle.dimexe = 1.5
dimstyle.dimexo = 0.6
dimstyle.dimgap = 0.6
dimstyle.dimtad = 1
dimstyle.dimtih = 0
dimstyle.dimtoh = 0
dimstyle.dimtxsty = "SHX_CN"

# ===== A4 图框 297x210 =====
BOX(0, 0, 297, 210, "细实线")
BOX(25, 5, 292, 205, "粗实线")

# ===== 标题栏 GB/T 10609.1 — 180x56 位于右下角 =====
TBX, TBY = 112.0, 5.0
TW, TH = 180.0, 56.0
BOX(TBX, TBY, TBX + TW, TBY + TH, "粗实线")

# 列划分 (X方向偏移累计)
col_offsets = [10, 16, 22, 32, 46, 60, 70, 84, 98, 112, 130, 150]
for w in col_offsets:
    LN(TBX + w, TBY, TBX + w, TBY + TH, "细实线")

# 行划分 (Y方向偏移累计, 从下往上)
row_offsets = [7, 14, 21, 28, 35, 42, 49]
for h in row_offsets:
    LN(TBX, TBY + h, TBX + TW, TBY + h, "细实线")

# 图名区竖分隔 (x=TBX+98, y=21~49)
LN(TBX + 98, TBY + 21, TBX + 98, TBY + 49, "细实线")

# ===== 标题栏文字 — 用 CELL 居中放置 =====
def CELL(xo, w, yo, h, txt, fs=2.0):
    """在单元格 (TBX+xo, TBY+yo) 宽w高h 内居中放置文字"""
    TXC(TBX + xo + w / 2, TBY + yo + h / 2 - fs * 0.35, txt, fs)

# 顶部签名行 (y=49~56, h=7)
for args in [
    (0, 10, "标记"), (10, 6, "处数"), (16, 6, "分区"),
    (22, 10, "更改文件号"), (32, 14, "签名"), (46, 14, "年月日"),
    (60, 10, "阶段标记"), (70, 14, "重量"), (84, 14, "比例"),
]:
    CELL(args[0], args[1], 49, 7, args[2])

# 第二行 (y=42~49, h=7)
for args in [
    (0, 10, "设计"), (10, 6, "标准化"),
    (22, 10, "工艺"), (32, 14, "批准"),
]:
    CELL(args[0], args[1], 42, 7, args[2])
# 共X张第X张
CELL(98, 32, 42, 7, "共  张  第  张")

# 第三行 (y=35~42, h=7)
for args in [
    (0, 10, "审核"), (10, 6, "日期"),
]:
    CELL(args[0], args[1], 35, 7, args[2])

# 第四行 (y=28~35, h=7)
CELL(0, 10, 28, 7, "批准")
CELL(84, 14, 28, 7, "1:1")

# 图名大格
TXC(TBX + 141, TBY + 35, "图样名称", 5.5)
TXC(TBX + 141, TBY + 14, "图样代号", 3.5)

# ===== 零件图: 50x40 外框 + 20x15 内槽 =====
cx, cy = 158.5, 105.0
ox1, oy1 = cx - 25, cy - 20
ox2, oy2 = cx + 25, cy + 20
ix1, iy1 = cx - 10, cy - 7.5
ix2, iy2 = cx + 10, cy + 7.5

BOX(ox1, oy1, ox2, oy2, "粗实线")
BOX(ix1, iy1, ix2, iy2, "粗实线")

# ===== 中心线 =====
LN(cx - 30, cy, cx + 30, cy, "中心线")
LN(cx, oy1 - 5, cx, oy2 + 5, "中心线")

# ===== 尺寸标注 =====
# 内槽宽度 20 (水平)
msp.add_linear_dim(
    base=(ix1, iy1), p1=(ix1, iy1), p2=(ix2, iy1),
    location=(cx, oy1 - 13), dimstyle="CN_DIM"
)
# 内槽高度 15 (垂直)
msp.add_linear_dim(
    base=(ix2, iy1), p1=(ix2, iy1), p2=(ix2, iy2),
    location=(ox2 + 16, (iy1 + iy2) / 2), dimstyle="CN_DIM", angle=90
)
# 外框宽度 50 (水平)
msp.add_linear_dim(
    base=(ox1, oy1), p1=(ox1, oy1), p2=(ox2, oy1),
    location=(cx, oy1 - 25), dimstyle="CN_DIM"
)
# 外框高度 40 (垂直)
msp.add_linear_dim(
    base=(ox1, oy1), p1=(ox1, oy1), p2=(ox1, oy2),
    location=(ox1 - 25, (oy1 + oy2) / 2), dimstyle="CN_DIM", angle=90
)

# ===== 技术要求 =====
TX(25, 175, "技术要求", 4.0)
reqs = [
    "1. 棱边倒角 C1；",
    "2. 未注尺寸公差按 GB/T1804-m 执行；",
    "3. 表面粗糙度为 Ra 3.2。",
]
for i, line in enumerate(reqs):
    TX(25, 169 - i * 5, line, 2.5)

# ===== 图纸信息 =====
TX(25, 195, "共 1 张", 3.5)
TX(25, 189, "第 1 张", 3.5)

# ===== 保存 DXF =====
path = "C:/Users/26011970/Desktop/zwcad_v11.dxf"
doc.saveas(path)
print("SAVED: " + path)

# ===== 用 ZWCAD 打开 =====
try:
    import win32com.client
    acad = win32com.client.Dispatch("ZWCAD.Application")
    acad.Visible = True
    # 如果目标文件已被占用，先关掉
    for d in acad.Documents:
        try:
            if d.FullName.replace("\\", "/").lower() == path.lower():
                d.Close(False)
        except:
            pass
    acad.Documents.Open(path)
    print("Opened in ZWCAD")
except Exception as e:
    print("Cannot open ZWCAD: " + str(e)[:120])
    print("Manual: File -> Open -> " + path)

print("OK - v11")