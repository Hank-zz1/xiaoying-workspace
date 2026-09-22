On Error Resume Next
Set cad = GetObject(, "ZWCAD.Application")
If Err.Number <> 0 Then
    Set cad = CreateObject("ZWCAD.Application")
End If
On Error GoTo 0

cad.Visible = True
Set doc = cad.Documents.Open("C:\Users\26011970\Desktop\AAA.dxf")
doc.SaveAs "C:\Users\26011970\Desktop\AAA.dwg", 13
doc.Close
MsgBox "Saved as AAA.dwg on Desktop"
