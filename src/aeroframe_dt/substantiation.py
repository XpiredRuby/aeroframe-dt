"""Integrated representative fitting substantiation pipeline."""
from __future__ import annotations

from dataclasses import asdict, dataclass
import json
from math import sqrt
from pathlib import Path
from typing import Any, Mapping

from .hand_calcs import (
    CheckResult, factored_stress, fastener_group_shear, fastener_group_tension,
    joint_slip_check, lug_net_section, pin_shear, projected_bearing,
    rectangular_plate_bending, resultant_2d, shear_tension_interaction,
    tension_with_explicit_prying, two_plane_shear_out,
)
from .loads import Resultant, SupportModel, solve_two_station_supports
from .margins import build_margin_rows, governing_row


@dataclass(frozen=True)
class SubstantiationResult:
    case_id: str
    geometry_revision: str
    selected_fitting_reaction_N: tuple[float, float, float]
    equilibrium_force_residual_N: tuple[float, float, float]
    equilibrium_moment_residual_Nm: tuple[float, float, float]
    checks: tuple[dict[str, Any], ...]
    governing_check: dict[str, Any] | None
    status: str
    claim_level: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _required(mapping: Mapping[str, Any], keys: set[str], label: str) -> None:
    missing = sorted(key for key in keys if key not in mapping)
    if missing:
        raise KeyError(f"{label} missing: {', '.join(missing)}")


def run_substantiation(case: Mapping[str, Any]) -> SubstantiationResult:
    _required(case, {"case_id", "classification", "geometry_revision", "resultant", "support_model", "geometry", "allowables", "fasteners", "factors", "traceability"}, "case")
    if case["classification"] not in {"SYNTHETIC_TEST_ONLY", "SOURCE_BACKED_REPRESENTATIVE"}:
        raise ValueError("classification must prevent OEM/certification misrepresentation")
    resultant_data = case["resultant"]
    resultant = Resultant(tuple(resultant_data["force_N"]), tuple(resultant_data["moment_Nm"]), tuple(resultant_data.get("reference_m", (0, 0, 0))))
    support = SupportModel(**case["support_model"])
    solution = solve_two_station_supports(resultant, support)
    rx, ry, rz = solution.selected_forward_fitting_reaction_N
    lug_load = sqrt(rx * rx + rz * rz)
    g, a, f, factors = case["geometry"], case["allowables"], case["fasteners"], case["factors"]
    _required(g, {"lug_width_m", "hole_diameter_m", "lug_thickness_m", "edge_distance_center_m", "flange_width_m", "flange_thickness_m", "flange_moment_Nm"}, "geometry")
    _required(a, {"lug_tension_Pa", "bearing_Pa", "shear_out_Pa", "pin_shear_Pa", "flange_bending_Pa", "fastener_shear_N", "fastener_tension_N"}, "allowables")
    _required(f, {"positions_m", "diameter_m", "shear_planes", "direct_tension_N", "moment_x_Nm", "moment_y_Nm", "prying_factor", "friction_coefficient", "preload_per_fastener_N", "slip_planes", "preload_loss_factor"}, "fasteners")
    _required(factors, {"safety_factor", "fitting_factor", "fitting_factor_source", "interaction_exponent"}, "factors")
    sf = float(factors["safety_factor"])

    checks: list[CheckResult] = [
        lug_net_section(lug_load, g["lug_width_m"], g["hole_diameter_m"], g["lug_thickness_m"], a["lug_tension_Pa"], sf),
        projected_bearing(lug_load, g["hole_diameter_m"], g["lug_thickness_m"], a["bearing_Pa"], sf),
        two_plane_shear_out(lug_load, g["edge_distance_center_m"], g["hole_diameter_m"], g["lug_thickness_m"], a["shear_out_Pa"], sf),
        pin_shear(lug_load, f["diameter_m"], int(f["shear_planes"]), a["pin_shear_Pa"], sf),
        rectangular_plate_bending(g["flange_moment_Nm"], g["flange_width_m"], g["flange_thickness_m"], a["flange_bending_Pa"], sf),
    ]
    nominal_lug = checks[0].demand
    checks.append(factored_stress(nominal_lug, factors["fitting_factor"], a["lug_tension_Pa"], sf, "lug_factored_net_section", factors["fitting_factor_source"]))

    positions = [tuple(item) for item in f["positions_m"]]
    shear_loads = fastener_group_shear(positions, (rx, ry), resultant.moment_Nm[2] * factors.get("forward_fastener_moment_share", 1.0))
    tension_loads = fastener_group_tension(positions, f["direct_tension_N"], f["moment_x_Nm"], f["moment_y_Nm"])
    for index, (shear, tension) in enumerate(zip(shear_loads, tension_loads), start=1):
        augmented = tension_with_explicit_prying(max(0.0, tension), prying_factor=f["prying_factor"])
        checks.append(shear_tension_interaction(resultant_2d(shear), a["fastener_shear_N"], augmented, a["fastener_tension_N"], factors["interaction_exponent"], f"fastener_{index:02d}_interaction"))
    checks.append(joint_slip_check(resultant_2d((rx, ry)), f["friction_coefficient"], f["preload_per_fastener_N"], len(positions), int(f["slip_planes"]), f["preload_loss_factor"], sf))

    rows = build_margin_rows([check.to_dict() for check in checks], case["traceability"])
    governing = governing_row(rows)
    status = "UNASSESSED" if governing is None else ("PASS" if governing["margin"] >= 0 else "FAIL")
    return SubstantiationResult(
        case["case_id"], case["geometry_revision"], solution.selected_forward_fitting_reaction_N,
        solution.residual_force_N, solution.residual_moment_Nm, tuple(rows), governing, status, case["classification"],
    )


def run_substantiation_file(input_path: str | Path, output_path: str | Path) -> SubstantiationResult:
    result = run_substantiation(json.loads(Path(input_path).read_text(encoding="utf-8")))
    target = Path(output_path); target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(result.to_dict(), indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return result
