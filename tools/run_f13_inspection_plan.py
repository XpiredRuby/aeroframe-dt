#!/usr/bin/env python3
"""F13 — validate the AF-DT-1000 Rev D inspection plan and quantify its structural effect.

Three things happen here, in order:

1.  Every row of ``inspection_quality/inspection_plan_AF-DT-1000_revD.csv`` is pushed
    through ``aeroframe_dt.inspection.InspectionCharacteristic.validate`` and screened
    against the 10:1 gauge-resolution rule.
2.  Measurement-system analysis on the two characteristics the margin is actually
    sensitive to: lug thickness and bore position.  The measurement data is
    SYNTHETIC_TEST_ONLY.
3.  A tolerance stack of the released tolerances onto the governing margin, evaluated
    on the real Melcon-Hoblit interaction rather than a linearisation, at the elastic
    contact ratio (the Rev D basis), the elastic-plastic ratio measured in
    F16, and the 7050-T7451 ratio measured in F24 (the released basis).

Run:  python tools/run_f13_inspection_plan.py
"""

from __future__ import annotations

import csv
import json
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from aeroframe_dt.inspection import (  # noqa: E402
    InspectionCharacteristic,
    capability,
    crossed_gage_rr,
)

PLAN = ROOT / "inspection_quality" / "inspection_plan_AF-DT-1000_revD.csv"
OUT = ROOT / "results" / "software_verification" / "f13_inspection_plan.json"

# --- Released margin state, docs/MARGIN_SUMMARY.md section 4 -------------------
RA_NOM = 0.3909          # axial load ratio at the elastic contact ratio
RTR_NOM = 0.7740         # transverse load ratio at the elastic contact ratio
T_NOM = 2.500            # in, lug thickness
T_LML = 2.480            # in, thickness at the low material limit
W_NOM = 4.000            # in, lug width
D_NOM = 2.000            # in, bore diameter at MMC
D_LMC = 2.002            # in, bore diameter at LMC
T_EFF_ELASTIC = 0.6809   # F7 elastic contact ratio, the Rev D basis
T_EFF_PLASTIC = 0.7300   # F16 elastic-plastic contact ratio, 7075-T7351
T_EFF_7050 = 0.6828      # F24 elastic-plastic contact ratio, 7050-T7451

# RA_NOM and RTR_NOM above are on the 7075-T7351 allowables the project originally
# carried (Ftu 65 ksi L, 66 ksi LT). F23 re-selected the material to 7050-T7451,
# whose MMPDS-2026 A-basis values at the 5.001-6.000 in band are 70 ksi in both
# directions. Load ratios scale inversely with the allowable, so the reference
# ratios rescale directly. Without this the stack returns a 7075 nominal against a
# 7050 margin, which is what F24 section 4 had to flag rather than quote.
FTU_L_7075, FTU_LT_7075 = 65.0, 66.0
FTU_L_7050, FTU_LT_7050 = 70.0, 70.0
RA_NOM_7050 = RA_NOM * FTU_L_7075 / FTU_L_7050
RTR_NOM_7050 = RTR_NOM * FTU_LT_7075 / FTU_LT_7050
F15_MS_AFTER = -0.370    # MS at e = 1.900 in on the elastic basis, F15
F15_DE = 0.600           # in, edge-distance loss in the F15 nonconformance
POS_TOL = 0.030          # in, diametral position zone at MMC
MMC_BONUS = 0.002        # in, maximum bonus tolerance from bore size

# Gauge R&R measurement sets are SYNTHETIC_TEST_ONLY.
SYNTHETIC_GAGE = {
    "AFDT-CHAR-006": {
        "tolerance": 0.040,
        "measurements": {
            "part1": {"opa": [2.4969, 2.4972], "opb": [2.4971, 2.4968]},
            "part2": {"opa": [2.5011, 2.5008], "opb": [2.5012, 2.5010]},
            "part3": {"opa": [2.5048, 2.5051], "opb": [2.5052, 2.5049]},
        },
    },
    "AFDT-CHAR-002": {
        "tolerance": 0.030,
        "measurements": {
            "part1": {"opa": [0.0041, 0.0044], "opb": [0.0043, 0.0040]},
            "part2": {"opa": [0.0109, 0.0112], "opb": [0.0113, 0.0110]},
            "part3": {"opa": [0.0188, 0.0191], "opb": [0.0192, 0.0189]},
        },
    },
}

# Synthetic run of 10 parts on the governing thickness characteristic.
SYNTHETIC_CAPABILITY = [2.5062, 2.4978, 2.5001, 2.5044, 2.4991,
                        2.5033, 2.5008, 2.4969, 2.5027, 2.4997]


def margin(ra: float, rtr: float) -> float:
    """Melcon-Hoblit axial/transverse interaction, exponents 1.6 and 0.625."""
    return 1.0 / (ra ** 1.6 + rtr ** 1.6) ** 0.625 - 1.0


def load_plan() -> list[dict[str, str]]:
    with PLAN.open(newline="", encoding="utf-8") as stream:
        return list(csv.DictReader(stream))


def validate_plan(rows: list[dict[str, str]]) -> tuple[list[str], list[dict]]:
    errors: list[str] = []
    screened: list[dict] = []
    seen: set[str] = set()
    for row in rows:
        cid = row["characteristic_id"]
        if cid in seen:
            errors.append(f"duplicate characteristic id {cid}")
        seen.add(cid)
        char = InspectionCharacteristic(
            characteristic_id=cid,
            requirement_id=row["requirement_id"],
            feature_id=row["feature_id"],
            nominal=float(row["nominal"]),
            lower_limit=float(row["lower_limit"]),
            upper_limit=float(row["upper_limit"]),
            units=row["units"],
            method=row["method"],
            instrument=row["instrument"],
            resolution=float(row["resolution"]),
            sampling_plan=row["sampling_plan"],
        )
        try:
            char.validate()
        except ValueError as exc:  # pragma: no cover - defensive
            errors.append(f"{cid}: {exc}")
            continue
        band = char.upper_limit - char.lower_limit
        ratio = char.resolution / band
        if ratio > 0.10:
            errors.append(
                f"{cid}: resolution {char.resolution} is {100 * ratio:.1f} percent "
                f"of the {band} band, above the 10 percent screen"
            )
        screened.append(
            {
                "characteristic_id": cid,
                "feature_id": char.feature_id,
                "tolerance_band": band,
                "units": char.units,
                "resolution_percent_of_band": round(100 * ratio, 2),
                "criticality": row["criticality"],
                "sampling_plan": char.sampling_plan,
            }
        )
    return errors, screened


def measurement_system_analysis() -> dict:
    results = {}
    for cid, block in SYNTHETIC_GAGE.items():
        rr = crossed_gage_rr(block["measurements"])
        gage_sigma = math.sqrt(rr.gage_rr_variance)
        ptr = 100.0 * 6.0 * gage_sigma / block["tolerance"]
        results[cid] = {
            "percent_gage_rr_of_total_variation": round(rr.percent_gage_rr, 2),
            "precision_to_tolerance_percent": round(ptr, 2),
            "repeatability_variance": rr.repeatability_variance,
            "reproducibility_variance": rr.reproducibility_variance,
            "part_variance": rr.part_variance,
            "verdict": "acceptable" if ptr <= 10.0 else
                       "marginal" if ptr <= 30.0 else "not capable",
            "data_class": "SYNTHETIC_TEST_ONLY",
        }
    return results


def process_capability() -> dict:
    cap = capability(SYNTHETIC_CAPABILITY, T_LML, T_NOM + (T_NOM - T_LML))
    return {
        "characteristic_id": "AFDT-CHAR-006",
        "count": cap.count,
        "mean": round(cap.mean, 5),
        "sample_std": round(cap.sample_std, 6),
        "cp": round(cap.cp, 3),
        "cpk": round(cap.cpk, 3),
        "verdict": "capable" if cap.cpk >= 1.33 else "not capable",
        "data_class": "SYNTHETIC_TEST_ONLY",
    }


def position_slope(ms_nom: float) -> float:
    """Bore-position sensitivity, anchored on the F15 nonconformance."""
    factor = (1.0 + F15_MS_AFTER) / (1.0 + margin(RA_NOM, RTR_NOM))
    ms_at_f15 = (1.0 + ms_nom) * factor - 1.0
    return (ms_nom - ms_at_f15) / F15_DE


def tolerance_stack(t_eff: float = T_EFF_ELASTIC,
                    ra_ref: float = RA_NOM,
                    rtr_ref: float = RTR_NOM) -> dict:
    """Stack the released tolerances onto the margin at the given contact ratio.

    Lug areas are linear in effective thickness, so both load ratios scale by t_eff.
    ``ra_ref``/``rtr_ref`` select the material basis; pass RA_NOM_7050/RTR_NOM_7050
    for the released 7050-T7451 configuration.
    """
    scale = T_EFF_ELASTIC / t_eff
    ra_nom, rtr_nom = ra_ref * scale, rtr_ref * scale
    ms_nom = margin(ra_nom, rtr_nom)
    dms_de = position_slope(ms_nom)

    # Thickness: every lug area is linear in t, so both load ratios scale by t_nom/t.
    ft = T_NOM / T_LML
    d_thickness = margin(ra_nom * ft, rtr_nom * ft) - ms_nom

    # Bore size at LMC: net-section area (w - D) * t falls 0.1 percent while bearing
    # area D * t rises 0.1 percent.  The adverse 0.1 percent is applied to BOTH ratios,
    # which bounds the term rather than resolving which mode governs.
    fd = (W_NOM - D_NOM) / (W_NOM - D_LMC)
    d_boresize = margin(ra_nom * fd, rtr_nom * fd) - ms_nom

    # Bore position: radial offset at LMC includes the full MMC bonus.
    radial = 0.5 * (POS_TOL + MMC_BONUS)
    d_position = -radial * dms_de

    terms = {"thickness": d_thickness, "bore_position": d_position, "bore_size": d_boresize}
    worst = sum(terms.values())
    rss = -math.sqrt(sum(value ** 2 for value in terms.values()))
    return {
        "t_eff_over_t": t_eff,
        "dms_de_per_in": round(dms_de, 4),
        "ms_nominal": round(ms_nom, 5),
        "terms": {key: round(value, 5) for key, value in terms.items()},
        "worst_case_delta": round(worst, 5),
        "ms_worst_case": round(ms_nom + worst, 5),
        "rss_delta": round(rss, 5),
        "ms_rss": round(ms_nom + rss, 5),
        "worst_case_consumption_percent": round(100 * abs(worst) / ms_nom, 1),
        "tolerance_scale_factor_to_zero_margin": round(ms_nom / abs(worst), 2),
        "bore_position_basis": "extrapolated from the F15 anchor, not derived; see PMI section 4.2",
    }


def main() -> int:
    rows = load_plan()
    errors, screened = validate_plan(rows)
    payload = {
        "component": "AF-DT-1000",
        "geometry_revision": "D",
        "load_revision": "C",
        "claim_boundary": "educational representative portfolio only, non-OEM non-certified",
        "characteristic_count": len(screened),
        "characteristics": screened,
        "measurement_system_analysis": measurement_system_analysis(),
        "process_capability": process_capability(),
        "tolerance_stack": tolerance_stack(T_EFF_7050, RA_NOM_7050, RTR_NOM_7050),
        "tolerance_stack_7075_plastic": tolerance_stack(T_EFF_PLASTIC),
        "tolerance_stack_elastic_basis": tolerance_stack(T_EFF_ELASTIC),
        "errors": errors,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    for error in errors:
        print(f"ERROR: {error}")
    print(f"Inspection plan OK: {len(screened)} characteristics, 0 validation errors"
          if not errors else "Inspection plan FAILED")
    for label, key in (("7075 elastic ", "tolerance_stack_elastic_basis"),
                       ("7075 plastic ", "tolerance_stack_7075_plastic"),
                       ("7050 RELEASED", "tolerance_stack")):
        st = payload[key]
        print(f"  {label}  t_eff/t {st['t_eff_over_t']:.4f}  dMS/de {st['dms_de_per_in']:.4f}  "
              f"MS {st['ms_nominal']:+.4f} -> {st['ms_worst_case']:+.4f}  "
              f"({st['worst_case_consumption_percent']} percent consumed)")
    print(f"Written: {OUT.relative_to(ROOT)}")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
