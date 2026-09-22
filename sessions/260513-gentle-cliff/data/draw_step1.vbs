Set cad = GetObject(, "ZWCAD.Application")
Set doc = cad.ActiveDocument
Set ms = doc.ModelSpace

' Base point
bx = 30 : by = 150

' Helper sub
Sub AddLine(x1, y1, x2, y2, layerName)
    Dim pt1(2), pt2(2)
    pt1(0) = x1 : pt1(1) = y1 : pt1(2) = 0
    pt2(0) = x2 : pt2(1) = y2 : pt2(2) = 0
    Dim lineObj
    Set lineObj = ms.AddLine(pt1, pt2)
    lineObj.Layer = layerName
End Sub

' ====== STEP 1: Centerline ======
AddLine bx-20, by, bx+380, by, "中心线"

' ====== STEP 2: Main shaft body (outside profile) ======
' Left end cap D=20, L=15
AddLine bx, by-10, bx+15, by-10, "实线"    ' top
AddLine bx, by+10, bx+15, by+10, "实线"    ' bottom
AddLine bx, by-10, bx, by+10, "实线"       ' left face

' Chamfer on left
AddLine bx, by-10, bx+2, by-12, "实线"
AddLine bx, by+10, bx+2, by+12, "实线"

' Next segment D=25, L=30
AddLine bx+15, by-12.5, bx+45, by-12.5, "实线"
AddLine bx+15, by+12.5, bx+45, by+12.5, "实线"
AddLine bx+15, by-10, bx+15, by+12.5, "实线"
AddLine bx+15, by+10, bx+15, by-12.5, "实线"

' Next segment D=30, L=25
AddLine bx+45, by-15, bx+70, by-15, "实线"
AddLine bx+45, by+15, bx+70, by+15, "实线"
AddLine bx+45, by-12.5, bx+45, by+15, "实线"
AddLine bx+45, by+12.5, bx+45, by-15, "实线"

' Next segment D=35, L=20
AddLine bx+70, by-17.5, bx+90, by-17.5, "实线"
AddLine bx+70, by+17.5, bx+90, by+17.5, "实线"
AddLine bx+70, by-15, bx+70, by+17.5, "实线"
AddLine bx+70, by+15, bx+70, by-17.5, "实线"

' Thread segment D=25, L=35
AddLine bx+90, by-12.5, bx+125, by-12.5, "螺纹"
AddLine bx+90, by+12.5, bx+125, by+12.5, "螺纹"
AddLine bx+90, by-17.5, bx+90, by+12.5, "实线"
AddLine bx+90, by+17.5, bx+90, by-12.5, "实线"

' Right end cap D=20, L=20
AddLine bx+125, by-10, bx+145, by-10, "实线"
AddLine bx+125, by+10, bx+145, by+10, "实线"
AddLine bx+125, by-12.5, bx+125, by+10, "实线"
AddLine bx+125, by+12.5, bx+125, by-10, "实线"

' Right face
AddLine bx+145, by-10, bx+145, by+10, "实线"

' Chamfer on right
AddLine bx+145, by-10, bx+143, by-12, "实线"
AddLine bx+145, by+10, bx+143, by+12, "实线"

cad.Visible = True
MsgBox "Step 1 Complete: Outline drawn"
