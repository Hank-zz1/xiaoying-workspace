# -*- coding: utf-8 -*-
"""
ZWCAD 绘图 v10: ezdxf 生成 DXF（完美中文） + COM 打开 ZWCAD
"""
import ezdxf
from ezdxf import units
from ezdxf.enums import TextEntityAlignment
import win32com.client

# ===== 新建 DXF =====
doc = ezdxf.new(dxfversion="R2010")
doc.units = units.MM
msp = doc.modelspace()

# ===== 文字样式 =====
# SHX + 大字体 (ZWCAD 标准中文方案)
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
    ly = doc.layers.add(name, color=props["color"], lineweight=props["lineweight"], linetype=lt)

# 加载中心线线型
try: doc.linetypes.add("CENTER", pattern="____ _ ____ _ ____ _ ____ _ ____ _ ", length=31.75)
except: pass

# ===== LTSCALE =====
doc.header["$LTSCALE"] = 0.25

# ===== 辅助函数 =====
def LN(x1,y1,x2,y2,layer):
    msp.add_line((x1,y1),(x2,y2), dxfattribs={"layer": layer})

def BOX(x1,y1,x2,y2,layer):
    LN(x1,y1,x2,y1,layer); LN(x2,y1,x2,y2,layer)
    LN(x2,y2,x1,y2,layer); LN(x1,y2,x1,y1,layer)

def TX(x,y,txt,h,style="SHX_CN",layer="文字",halign=0):
    a = msp.add_text(txt, dxfattribs={"style": style, "layer": layer, "height": h})
    if halign == 1:  # center
        a.set_placement((x,y), align=TextEntityAlignment.MIDDLE_CENTER)
    elif halign == 2:  # right
        a.set_placement((x,y), align=TextEntityAlignment.MIDDLE_RIGHT)
    else:
        a.set_placement((x,y))
    return a

def TXC(x,y,txt,h,style="SHX_CN",layer="文字"):
    return TX(x,y,txt,h,style,layer,halign=1)

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
dimstyle.dimtxsty = "SHX_CN"

# ===== A4 图框 297x210 =====
BOX(0,0,297,210,"细实线")
BOX(25,5,292,205,"粗实线")

# ===== 标题栏 180x56 =====
TBX, TBY = 112.0, 5.0
TW, TH = 180.0, 56.0
BOX(TBX,TBY,TBX+TW,TBY+TH,"粗实线")

cols = [10,16,22,32,46,60,70,84,98,112,130,150]
for w in cols:
    LN(TBX+w,TBY,TBX+w,TBY+TH,"细实线")
rows = [7,14,21,28,35,42,49]
for h in rows:
    LN(TBX,TBY+h,TBX+TW,TBY+h,"细实线")

# 图名区竖线
LN(TBX+98,TBY+21,TBX+98,TBY+49,"细实线")

# ===== 标题栏文字 =====
def CELL(xo,w,yo,h,txt,fs=2.0):
    TXC(TBX+xo+w/2, TBY+yo+h/2-fs*0.35, txt, fs)

# 所有标题栏文字
for args in [
    # 行7: y=49~56
    (0,10,49,56,"标记"),(10,6,49,56,"处数"),(16,6,49,56,"分区"),
    (22,10,49,56,"更改文件号"),(32,14,49,56,"签名"),(46,14,49,56,"年月日"),
    (60,10,49,56,"阶段标记"),(70,14,49,56,"重量"),(84,14,49,56,"比例"),
    # 行6: y=42~49
    (0,10,42,49,"设计"),(10,6,42,49,"标准化"),
    (22,10,42,49,"工艺"),(32,14,42,49,"批准"),
    (98,14,42,49,"共  张  第  张"),
    # 行5: y=35~42
    (0,10,35,42,"审核"),(10,6,35,42,"工艺"),
    # 行4: y=28~35
    (0,10,28,35,"批准"),
    (84,14,28,35,"1:1"),
]:
    CELL(*args)

# 图名大格
TXC(TBX+141,TBY+35,"图样名称",5.0)
TXC(TBX+141,TBY+14,"图样代号",3.0)

# ===== 零件图 (50x40 + 内槽20x15) =====
cx, cy = 158.5, 105.0
ox1,oy1 = cx-25, cy-20
ox2,oy2 = cx+25, cy+20
ix1,iy1 = cx-10, cy-7.5
ix2,iy2 = cx+10, cy+7.5

BOX(ox1,oy1,ox2,oy2,"粗实线")
BOX(ix1,iy1,ix2,iy2,"粗实线")

# ===== 中心线 =====
LN(cx-30,cy,cx+30,cy,"中心线")
LN(cx,oy1-5,cx,oy2+5,"中心线")

# ===== 尺寸标注 =====
msp.add_linear_dim(
    base=(ix1,iy1), p1=(ix1,iy1), p2=(ix2,iy1),
    location=(cx, oy1-13), dimstyle="CN_DIM"
)
msp.add_linear_dim(
    base=(ix2,iy1), p1=(ix2,iy1), p2=(ix2,iy2),
    location=(ox2+16, (iy1+iy2)/2), dimstyle="CN_DIM", angle=90
)
msp.add_linear_dim(
    base=(ox1,oy1), p1=(ox1,oy1), p2=(ox2,oy1),
    location=(cx, oy1-25), dimstyle="CN_DIM"
)
msp.add_linear_dim(
    base=(ox1,oy1), p1=(ox1,oy1), p2=(ox1,oy2),
    location=(ox1-25, (oy1+oy2)/2), dimstyle="CN_DIM", angle=90
)

# ===== 技术要求 =====
TX(25,175,"技术要求",4.0)
for i,line in enumerate([
    "1. 棱边倒角 C1；",
    "2. 未注尺寸公差按 GB/T1804-m 执行；",
    "3. 表面粗糙度为 Ra 3.2。",
]):
    TX(25,169-i*5,line,2.5)

# ===== 图纸信息 =====
TX(25,195,"共 1 张",3.5)
TX(25,189,"第 1 张",3.5)

# ===== 保存 DXF =====
path = "C:/Users/26011970/Desktop/zwcad_v10.dxf"
doc.saveas(path)
print("SAVED: " + path)

# ===== 用 ZWCAD 打开 =====
try:
    acad = win32com.client.Dispatch("ZWCAD.Application")
    acad.Visible = True
    acad.Documents.Open(path)
    print("Opened in ZWCAD")
except Exception as e:
    print("Cannot open ZWCAD: " + str(e)[:100])
    print("Manual: File -> Open -> " + path)

print("OK")