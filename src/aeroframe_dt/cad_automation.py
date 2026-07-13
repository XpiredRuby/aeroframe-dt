"""CAD parameter validation and human-reviewable macro generation."""
from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Mapping


@dataclass(frozen=True)
class CADParameter:
    name: str
    value: float
    units: str
    minimum: float | None = None
    maximum: float | None = None
    description: str = ""

    def validate(self) -> None:
        if not self.name.strip() or not self.units.strip():
            raise ValueError("CAD parameter name and units are required")
        if self.minimum is not None and self.value < self.minimum:
            raise ValueError(f"{self.name} is below minimum")
        if self.maximum is not None and self.value > self.maximum:
            raise ValueError(f"{self.name} is above maximum")
        if self.minimum is not None and self.maximum is not None and self.minimum > self.maximum:
            raise ValueError(f"{self.name} has invalid bounds")


def read_parameter_table(path: str | Path) -> list[CADParameter]:
    rows: list[CADParameter] = []
    with Path(path).open(newline="", encoding="utf-8") as stream:
        for item in csv.DictReader(stream):
            param = CADParameter(
                name=item["name"], value=float(item["value"]), units=item["units"],
                minimum=float(item["minimum"]) if item.get("minimum", "").strip() else None,
                maximum=float(item["maximum"]) if item.get("maximum", "").strip() else None,
                description=item.get("description", ""),
            )
            param.validate(); rows.append(param)
    if len({row.name for row in rows}) != len(rows):
        raise ValueError("duplicate CAD parameter names")
    return rows


def solidworks_global_variables_macro(parameters: Iterable[CADParameter], document_title: str = "AFDT_FITTING") -> str:
    """Generate VBA source that writes SolidWorks global variables/equations.

    The macro intentionally does not create production geometry automatically;
    it establishes controlled global variables in an open part document.
    """
    rows = list(parameters)
    for row in rows: row.validate()
    lines = [
        "Option Explicit",
        "",
        "Dim swApp As SldWorks.SldWorks",
        "Dim swModel As SldWorks.ModelDoc2",
        "Dim swEqMgr As SldWorks.EquationMgr",
        "",
        "Sub main()",
        "    Set swApp = Application.SldWorks",
        "    Set swModel = swApp.ActiveDoc",
        "    If swModel Is Nothing Then Err.Raise vbObjectError + 1, , \"Open a part document first.\"",
        "    If swModel.GetType <> swDocPART Then Err.Raise vbObjectError + 2, , \"Active document must be a part.\"",
        f"    swModel.SetTitle2 \"{document_title}\"",
        "    Set swEqMgr = swModel.GetEquationMgr",
    ]
    for row in rows:
        unit = {"m": "m", "mm": "mm", "deg": "deg", "rad": "rad"}.get(row.units, row.units)
        expression = f'\"{row.name}\" = {row.value:.12g}{unit}'
        lines.append(f"    Call UpsertEquation(swEqMgr, \"{expression}\")")
    lines.extend([
        "    swEqMgr.EvaluateAll",
        "    swModel.EditRebuild3",
        "    swModel.Save3 swSaveAsOptions_Silent, 0, 0",
        "End Sub",
        "",
        "Private Sub UpsertEquation(ByVal mgr As SldWorks.EquationMgr, ByVal expression As String)",
        "    Dim i As Long",
        "    Dim variableName As String",
        "    variableName = Split(expression, \"=\")(0)",
        "    For i = 0 To mgr.GetCount - 1",
        "        If Trim(Split(mgr.Equation(i), \"=\")(0)) = Trim(variableName) Then",
        "            mgr.Equation(i) = expression",
        "            Exit Sub",
        "        End If",
        "    Next i",
        "    mgr.Add3 -1, expression, True, swInConfigurationOpts_e.swAllConfiguration, Empty",
        "End Sub",
        "",
    ])
    return "\n".join(lines)


def freecad_parameter_macro(parameters: Iterable[CADParameter], spreadsheet_name: str = "Parameters") -> str:
    rows = list(parameters)
    for row in rows: row.validate()
    lines = [
        "# AeroFrame-DT FreeCAD parameter-sheet macro",
        "import FreeCAD as App",
        "doc = App.ActiveDocument or App.newDocument('AeroFrame_DT')",
        f"sheet = doc.getObject('{spreadsheet_name}') or doc.addObject('Spreadsheet::Sheet', '{spreadsheet_name}')",
    ]
    for index, row in enumerate(rows, start=2):
        lines.extend([
            f"sheet.set('A{index}', {row.name!r})",
            f"sheet.set('B{index}', {str(row.value) + ' ' + row.units!r})",
            f"sheet.setAlias('B{index}', {row.name!r})",
            f"sheet.set('C{index}', {row.description!r})",
        ])
    lines.extend(["doc.recompute()", "doc.saveAs('AeroFrame_DT_parameters.FCStd')", ""])
    return "\n".join(lines)


def validate_functional_constraints(values: Mapping[str, float]) -> list[str]:
    """Return geometry-constraint violations for common fitting parameters."""
    violations: list[str] = []
    required = {"lug_width_m", "hole_diameter_m", "lug_thickness_m", "edge_distance_m", "flange_thickness_m"}
    missing = required - set(values)
    if missing:
        return [f"missing parameter: {name}" for name in sorted(missing)]
    if values["lug_width_m"] <= values["hole_diameter_m"]:
        violations.append("lug width must exceed hole diameter")
    if values["edge_distance_m"] < 1.5 * values["hole_diameter_m"]:
        violations.append("edge distance is below the provisional 1.5D screening floor")
    if min(values[name] for name in required) <= 0:
        violations.append("all geometric dimensions must be positive")
    return violations
