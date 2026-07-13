Option Explicit

Dim swApp As SldWorks.SldWorks
Dim swModel As SldWorks.ModelDoc2
Dim swEqMgr As SldWorks.EquationMgr

Sub main()
    Set swApp = Application.SldWorks
    Set swModel = swApp.ActiveDoc
    If swModel Is Nothing Then Err.Raise vbObjectError + 1, , "Open a part document first."
    If swModel.GetType <> swDocPART Then Err.Raise vbObjectError + 2, , "Active document must be a part."
    swModel.SetTitle2 "AFDT_FITTING"
    Set swEqMgr = swModel.GetEquationMgr
    Call UpsertEquation(swEqMgr, ""lug_width" = 100mm")
    Call UpsertEquation(swEqMgr, ""hole_diameter" = 40mm")
    Call UpsertEquation(swEqMgr, ""lug_thickness" = 20mm")
    Call UpsertEquation(swEqMgr, ""edge_distance" = 55mm")
    Call UpsertEquation(swEqMgr, ""flange_thickness" = 16mm")
    Call UpsertEquation(swEqMgr, ""blend_radius" = 12mm")
    swEqMgr.EvaluateAll
    swModel.EditRebuild3
    swModel.Save3 swSaveAsOptions_Silent, 0, 0
End Sub

Private Sub UpsertEquation(ByVal mgr As SldWorks.EquationMgr, ByVal expression As String)
    Dim i As Long
    Dim variableName As String
    variableName = Split(expression, "=")(0)
    For i = 0 To mgr.GetCount - 1
        If Trim(Split(mgr.Equation(i), "=")(0)) = Trim(variableName) Then
            mgr.Equation(i) = expression
            Exit Sub
        End If
    Next i
    mgr.Add3 -1, expression, True, swInConfigurationOpts_e.swAllConfiguration, Empty
End Sub
