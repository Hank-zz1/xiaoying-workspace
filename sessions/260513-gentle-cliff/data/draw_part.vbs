Set cad = GetObject(, "ZWCAD.Application")
Set doc = cad.ActiveDocument
Set ms = doc.ModelSpace

Sub AddLine(x1, y1, x2, y2, layerName)
    Dim pt1(2), pt2(2)
    pt1(0) = x1 : pt1(1) = y1 : pt1(2) = 0
    pt2(0) = x2 : pt2(1) = y2 : pt2(2) = 0
    Dim obj
    Set obj = ms.AddLine(pt1, pt2)
    obj.Layer = layerName
End Sub

Sub AddCircle(cx, cy, r, layerName)
    Dim pt(2)
    pt(0) = cx : pt(1) = cy : pt(2) = 0
    Dim obj
    Set obj = ms.AddCircle(pt, r)
    obj.Layer = layerName
End Sub

Sub AddArc(cx, cy, r, startAng, endAng, layerName)
    Dim pt(2)
    pt(0) = cx : pt(1) = cy : pt(2) = 0
    Dim obj
    Set obj = ms.AddArc(pt, r, startAng, endAng)
    obj.Layer = layerName
End Sub

Sub AddHatch(layerName)
    ' We'll do hatch later - needs region creation
End Sub

' ====== Coordinate system: Y=0 is centerline ======
Dim bx, by
bx = 30 : by = 150

' ====== STAGE 1: Centerline ======
AddLine bx-15, by, bx+165, by, "中心线"

' ====== STAGE 2: Main outline (top half + bottom half) ======
' Segment definitions (x_start, x_end, radius):
' Seg1: Left small end D=18, L=12, chamfer 2x45°
' Seg2: D=24, L=25
' Seg3: D=30, L=18
' Seg4: D=36, L=15
' Seg5: Thread M24, L=30
' Seg6: Right end D=18, L=15

Dim x1,x2,r1,r2
' -- Seg1: Left end D=18 (r=9), L=12 --
x1 = bx : x2 = bx + 12 : r = 9
AddLine x1, by-r, x2, by-r, "实线"
AddLine x1, by+r, x2, by+r, "实线"
AddLine x1, by-r, x1, by+r, "实线"

' Chamfer 2x45 at left end
AddLine x1, by-r, x1+2, by-r-2, "实线"
AddLine x1, by+r, x1+2, by+r+2, "实线"

' -- Seg2: D=24 (r=12), L=25 --
x1 = bx+12 : x2 = bx+37 : r = 12
AddLine x1, by-r, x2, by-r, "实线"
AddLine x1, by+r, x2, by+r, "实线"
AddLine x1, by-9, x1, by+r, "实线"
AddLine x1, by+9, x1, by-r, "实线"

' -- Seg3: D=30 (r=15), L=18 --
x1 = bx+37 : x2 = bx+55 : r = 15
AddLine x1, by-r, x2, by-r, "实线"
AddLine x1, by+r, x2, by+r, "实线"
AddLine x1, by-12, x1, by+r, "实线"
AddLine x1, by+12, x1, by-r, "实线"

' -- Seg4: D=36 (r=18), L=15 --
x1 = bx+55 : x2 = bx+70 : r = 18
AddLine x1, by-r, x2, by-r, "实线"
AddLine x1, by+r, x2, by+r, "实线"
AddLine x1, by-15, x1, by+r, "实线"
AddLine x1, by+15, x1, by-r, "实线"

' -- Seg5: Thread M24 (r=12), L=30 --
x1 = bx+70 : x2 = bx+100 : r = 12
AddLine x1, by-r, x2, by-r, "螺纹"
AddLine x1, by+r, x2, by+r, "螺纹"
AddLine x1, by-18, x1, by+r, "实线"
AddLine x1, by+18, x1, by-r, "实线"

' Thread detail lines (thin lines for thread root)
r_thread = 10.0
For i = 1 To 14
    tx = x1 + i*2
    AddLine tx, by-r, tx, by-r_thread, "螺纹"
    AddLine tx, by+r, tx, by+r_thread, "螺纹"
Next
AddLine x1, by-r, x2, by-r_thread, "螺纹"
AddLine x1, by+r, x2, by+r_thread, "螺纹"

' -- Seg6: Right end D=18 (r=9), L=15 --
x1 = bx+100 : x2 = bx+115 : r = 9
AddLine x1, by-r, x2, by-r, "实线"
AddLine x1, by+r, x2, by+r, "实线"
AddLine x1, by-12, x1, by+r, "实线"
AddLine x1, by+12, x1, by-r, "实线"
AddLine x2, by-r, x2, by+r, "实线"

' Chamfer 2x45 at right end
AddLine x2, by-r, x2-2, by-r-2, "实线"
AddLine x2, by+r, x2-2, by+r+2, "实线"

' ====== STAGE 3: Key slot on Seg2 (D=24 section) ======
' Key slot on top of Seg2
kx1 = bx+17 : kx2 = bx+31
ky_top = by-12
AddLine kx1, ky_top, kx2, ky_top, "键槽"  ' top edge
AddLine kx1, ky_top, kx1, ky_top+4, "键槽"  ' left end
AddLine kx2, ky_top, kx2, ky_top+4, "键槽"  ' right end

' Bottom key slot
ky_bot = by+12
AddLine kx1, ky_bot, kx2, ky_bot, "键槽"
AddLine kx1, ky_bot, kx1, ky_bot-4, "键槽"
AddLine kx2, ky_bot, kx2, ky_bot-4, "键槽"

' ====== STAGE 4: Shoulder fillets ======
' R1 fillets at shoulder transitions
AddArc bx+12, by-10, 1.0, 3.14159, 4.71239, "实线" ' top left shoulder
AddArc bx+12, by+10, 1.0, 1.5708, 3.14159, "实线"  ' bottom left shoulder
AddArc bx+37, by-13.5, 1.5, 3.14159, 4.71239, "实线"
AddArc bx+37, by+13.5, 1.5, 1.5708, 3.14159, "实线"
AddArc bx+55, by-16.5, 1.5, 3.14159, 4.71239, "实线"
AddArc bx+55, by+16.5, 1.5, 1.5708, 3.14159, "实线"

' ====== STAGE 5: Hidden lines for internal features ======
' Hidden inner bore D=10 through center
bore_r = 5
AddLine bx+5, by-bore_r, bx+110, by-bore_r, "虚线"
AddLine bx+5, by+bore_r, bx+110, by+bore_r, "虚线"

' ====== STAGE 6: Section lines (hatch) for the segmented view ======
' Left side frame for section view
sx = bx + 140
sy = by - 30

' Section circle showing internal profile
AddCircle sx, sy, 15, "实线"
AddCircle sx, sy, 12, "实线"
AddCircle sx, sy, 5, "虚线"

' Cross centerline for section
AddLine sx-20, sy, sx+20, sy, "中心线"
AddLine sx, sy-20, sx, sy+20, "中心线"

' Hatch the section (solid section between r=5 and r=12)
' Create hatch boundary via points
Dim hatchPts(7), hatchPtsInner(3)
' We need to create regions for hatch - using circles
Dim outerLoop(0), innerLoop(0)
Set circ1 = ms.AddCircle(Array(sx, sy, 0), 12)
Set circ2 = ms.AddCircle(Array(sx, sy, 0), 5)
outerLoop(0) = circ1
innerLoop(0) = circ2

' Create region from outer circle
Dim outerRegion
Set outerRegion = doc.ModelSpace.AddRegion(outerLoop)
Dim innerRegion
Set innerRegion = doc.ModelSpace.AddRegion(innerLoop)

' Boolean subtract
outerRegion.Boolean 1, innerRegion

' Create hatch
Dim patternType, patternName, associativity
patternType = 1  ' Predefined
patternName = "ANSI31"
associativity = True
Dim hatchObj
Set hatchObj = ms.AddHatch(patternType, patternName, associativity)
hatchObj.PatternScale = 0.5
hatchObj.PatternAngle = 0.7854  ' 45 degrees
hatchObj.Layer = "剖面线"

Dim outerHatchLoop(0)
outerHatchLoop(0) = outerRegion
hatchObj.AppendOuterLoop outerHatchLoop
hatchObj.Evaluate

cad.Visible = True
MsgBox "Drawing complete! All lines, layers, and patterns drawn."
