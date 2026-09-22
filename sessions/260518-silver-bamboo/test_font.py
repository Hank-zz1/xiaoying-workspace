# -*- coding: utf-8 -*-
"""
ZWCAD 中文文字渲染最终诊断
通过 SendCommand + AutoLISP 直接用 ZWCAD 原生命令创建文字
绕过 Python COM 编码问题
"""
import win32com.client, pythoncom, time

def A3(x,y,z=0.0):
    return win32com.client.VARIANT(pythoncom.VT_ARRAY|pythoncom.VT_R8,(float(x),float(y),float(z)))

acad = win32com.client.Dispatch("ZWCAD.Application")
acad.Visible = True
doc = acad.ActiveDocument
if doc: doc.Close(False)
doc = acad.Documents.Add()

# ===== 方法1: SendCommand -STYLE 创建字体 =====
# 先用 -STYLE 设置当前文字样式
doc.SendCommand("-STYLE\nSHX_CN\ntxt.shx,gbcbig.shx\n\n\n\n\n\n\n")
time.sleep(0.3)

# ===== 方法2: 用 LISP (command) 创建文字 =====
# (command "_.TEXT" pt height rotation text)
doc.SendCommand('(command "_.TEXT" \'(30 180 0) "4" "0" "标记处数分区更改文件号")\n')
time.sleep(0.3)
doc.SendCommand('(command "_.TEXT" "" "签名年月日设计标准化")\n')
time.sleep(0.3)
doc.SendCommand('(command "_.TEXT" "" "工艺批准审核技术要求")\n')
time.sleep(0.3)

# ===== 方法3: 直接用 entmake 创建 TEXT entity =====
# (entmake '((0 . "TEXT")(10 30 170 0)(40 . 4)(1 . "entmake测试:图样名称图样代号")))
doc.SendCommand('(entmake (list (cons 0 "TEXT")(list 10 30 170 0)(cons 40 4)(cons 1 "entmake:共1张第1张棱边倒角C1")))\n')
time.sleep(0.3)

# ===== 方法4: Python AddText (对照组) =====
cn = doc.TextStyles.Add("TTF_SONGTI")
cn.FontFile = "SimSun"
ms = doc.ModelSpace
tx = ms.AddText("Python宋体:技术要求表面粗糙度", A3(30, 160, 0), 5.0)
tx.StyleName = "TTF_SONGTI"

tx2 = ms.AddText("Python SHX:标记处数签名年月日", A3(30, 150, 0), 5.0)
tx2.StyleName = "SHX_CN"

# ===== 方法5: 通过 SendCommand 设置 STYLE 为 SimSun =====
doc.SendCommand("-STYLE\nTTF_STYLE\nSimSun\n\n\n\n\n\n\n")
time.sleep(0.3)
doc.SendCommand('(command "_.TEXT" \'(30 140 0) "5" "0" "命令SimSun:图样名称图样代号")\n')
time.sleep(0.3)
doc.SendCommand('(command "_.TEXT" "" "设计审核批准")\n')
time.sleep(0.3)

# 保存
doc.SaveAs("C:/Users/26011970/Desktop/font_debug_final.dwg")
print("SAVED - check ZWCAD to see which method actually works")

# 导出每个文字的 StyleName 用于分析
ms2 = doc.ModelSpace
for i in range(1, ms2.Count+1):
    try:
        obj = ms2.Item(i)
        if obj.ObjectName == 'AcDbText':
            print(f'  [{obj.StyleName}] text={repr(obj.TextString[:30])}')
    except: pass