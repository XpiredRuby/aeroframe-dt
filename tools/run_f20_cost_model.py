#!/usr/bin/env python3
"""F20 - recurring cost model for AF-DT-1000.

The project has optimised on mass and margin and has never costed anything. This
script builds the missing recurring cost estimate and, more importantly, derives the
raw stock envelope that the cost depends on - which turns out to have a consequence
for the material allowables, not just for the price.

HONESTY BOUNDARY. Two very different classes of number appear here:

  DERIVED   - envelope, part volume, buy-to-fly, removed volume, machined area.
              These follow from the frozen Rev D geometry and are checkable.
  ASSUMED   - every currency rate, every cutting rate, every inspection time.
              No public source was available, so each is declared as a
              low/nominal/high triple and the answer is reported as a range.
              These are ASSUMED_COST_BASIS. They are not quotations and must not
              be cited as though they were.

The conclusions the document draws are the ones that survive the full assumed range,
i.e. the ones that depend on ratios rather than on absolute rates.

Run:  python tools/run_f20_cost_model.py
Out:  results/f20_cost_model.json
      results/f20_cost_breakdown.csv
"""

from __future__ import annotations

import csv
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results"

# --------------------------------------------------------------------------
# DERIVED - Rev D geometry, inches. Mirrors cad/build_revD.py exactly.
# --------------------------------------------------------------------------
P = {
    "d_pin": 2.000, "t_lug": 2.500, "w_lug": 4.000, "e_center": 2.500,
    "t_flange": 1.000, "t_web": 2.500, "r_blend": 0.500, "g_y": 4.000,
    "p_x": 1.500, "L_station": 16.000, "d_fast": 0.250, "web_height": 3.000,
}

DENSITY_LB_IN3 = 0.101          # 7075 aluminium, standard handbook value
ROUGH_STOCK_PER_FACE_IN = 0.060  # F13 operation 030
N_FASTENER_HOLES = 8             # rarray(4, 2)


def geometry() -> dict:
    """Envelope, part volume and buy-to-fly, all from the frozen parameters."""
    L, W_f, t_f = P["L_station"], P["w_lug"] + 2.0, P["t_flange"]
    lug_h = 2 * P["e_center"]

    envelope = {
        "x_in": L,
        "y_in": W_f,
        "z_in": t_f + P["web_height"] + lug_h,
    }
    envelope["volume_in3"] = envelope["x_in"] * envelope["y_in"] * envelope["z_in"]

    # billet = envelope + rough stock on every face
    billet = {k.replace("_in", "_in"): envelope[k] + 2 * ROUGH_STOCK_PER_FACE_IN
              for k in ("x_in", "y_in", "z_in")}
    billet["volume_in3"] = billet["x_in"] * billet["y_in"] * billet["z_in"]

    # part volume, prismatic decomposition. Fillets are NOT added: they add
    # material, so this is a slight under-estimate of the part and therefore a
    # slight over-estimate of buy-to-fly. Stated, not hidden.
    v_flange = L * W_f * t_f
    v_web = P["w_lug"] * P["t_web"] * P["web_height"]
    v_lug = P["w_lug"] * P["t_lug"] * lug_h
    v_bore = math.pi * (P["d_pin"] / 2) ** 2 * P["t_lug"]
    v_fast = N_FASTENER_HOLES * math.pi * (P["d_fast"] / 2) ** 2 * t_f
    v_part = v_flange + v_web + v_lug - v_bore - v_fast

    return {
        "envelope": envelope,
        "billet": billet,
        "part_volume_in3": v_part,
        "part_mass_lb": v_part * DENSITY_LB_IN3,
        "part_mass_kg": v_part * DENSITY_LB_IN3 * 0.453592,
        "removed_volume_in3": billet["volume_in3"] - v_part,
        "buy_to_fly": billet["volume_in3"] / v_part,
        "material_utilisation_pct": 100.0 * v_part / billet["volume_in3"],
        "min_stock_thickness_in": min(envelope["x_in"], envelope["y_in"],
                                      envelope["z_in"]),
    }


# --------------------------------------------------------------------------
# ASSUMED_COST_BASIS - every entry is (low, nominal, high). No source exists.
# --------------------------------------------------------------------------
ASSUMED = {
    "plate_usd_per_lb":        (4.00, 7.00, 12.00),
    "scrap_credit_usd_per_lb": (0.30, 0.50, 0.80),
    "machine_rate_usd_per_hr": (85.0, 120.0, 180.0),
    "inspect_rate_usd_per_hr": (70.0, 95.0, 140.0),
    "rough_mrr_in3_per_min":   (6.0, 12.0, 20.0),
    "finish_in2_per_min":      (2.0, 4.0, 8.0),
    "setup_hr_per_lot":        (3.0, 6.0, 12.0),
    "cmm_min_per_characteristic": (3.0, 6.0, 12.0),
    "fpi_min_per_part":        (8.0, 15.0, 25.0),
    "bore_special_min_per_part": (5.0, 10.0, 20.0),
}

N_CHARACTERISTICS = 10   # F13 inspection plan, Rev D
LOT_SIZES = [1, 5, 25, 100]


def finished_area_in2(geo: dict) -> float:
    """Approximate finished surface area to be finish-machined."""
    L, W_f, t_f = P["L_station"], P["w_lug"] + 2.0, P["t_flange"]
    lug_h = 2 * P["e_center"]
    blade_h = P["web_height"] + lug_h
    a_flange = 2 * L * W_f + 2 * (L + W_f) * t_f
    a_blade = 2 * P["w_lug"] * blade_h + 2 * P["t_lug"] * blade_h
    a_bore = math.pi * P["d_pin"] * P["t_lug"]
    a_fast = N_FASTENER_HOLES * math.pi * P["d_fast"] * t_f
    return a_flange + a_blade + a_bore + a_fast


def cost(geo: dict, level: int, lot: int) -> dict:
    """level 0/1/2 = low/nominal/high of every assumed rate."""
    a = {k: v[level] for k, v in ASSUMED.items()}

    billet_lb = geo["billet"]["volume_in3"] * DENSITY_LB_IN3
    chip_lb = geo["removed_volume_in3"] * DENSITY_LB_IN3

    material = billet_lb * a["plate_usd_per_lb"]
    scrap_credit = -chip_lb * a["scrap_credit_usd_per_lb"]

    rough_hr = (geo["removed_volume_in3"] / a["rough_mrr_in3_per_min"]) / 60.0
    finish_hr = (finished_area_in2(geo) / a["finish_in2_per_min"]) / 60.0
    setup_hr = a["setup_hr_per_lot"] / lot
    machining = (rough_hr + finish_hr + setup_hr) * a["machine_rate_usd_per_hr"]

    insp_hr = (N_CHARACTERISTICS * a["cmm_min_per_characteristic"]
               + a["fpi_min_per_part"] + a["bore_special_min_per_part"]) / 60.0
    inspection = insp_hr * a["inspect_rate_usd_per_hr"]

    total = material + scrap_credit + machining + inspection
    return {
        "lot_size": lot,
        "material_usd": material,
        "scrap_credit_usd": scrap_credit,
        "machining_usd": machining,
        "inspection_usd": inspection,
        "total_usd": total,
        "rough_hr": rough_hr, "finish_hr": finish_hr,
        "setup_hr_per_part": setup_hr, "inspection_hr": insp_hr,
        "material_pct": 100 * material / total,
        "machining_pct": 100 * machining / total,
        "inspection_pct": 100 * inspection / total,
    }


def envelope_sensitivity(geo: dict) -> dict:
    """The question F11 never asked: does removing FINISHED mass remove COST?

    Two hypothetical 10% changes are compared at nominal rates:
      A. 10% of finished mass pocketed out of the part, envelope unchanged.
      B. the blade height reduced so the ENVELOPE shrinks 10% in z.
    """
    base = cost(geo, 1, 25)

    # A - pocketing: part volume down 10%, billet unchanged, more metal removed
    geo_a = json.loads(json.dumps(geo))
    geo_a["part_volume_in3"] *= 0.90
    geo_a["removed_volume_in3"] = (geo_a["billet"]["volume_in3"]
                                   - geo_a["part_volume_in3"])
    cost_a = cost(geo_a, 1, 25)

    # B - envelope reduction in z, part volume down by the same 10%
    geo_b = json.loads(json.dumps(geo))
    geo_b["billet"]["z_in"] *= 0.90
    geo_b["billet"]["volume_in3"] = (geo_b["billet"]["x_in"] * geo_b["billet"]["y_in"]
                                     * geo_b["billet"]["z_in"])
    geo_b["part_volume_in3"] *= 0.90
    geo_b["removed_volume_in3"] = (geo_b["billet"]["volume_in3"]
                                   - geo_b["part_volume_in3"])
    cost_b = cost(geo_b, 1, 25)

    return {
        "baseline_usd": base["total_usd"],
        "pocketing_10pct_mass_usd": cost_a["total_usd"],
        "pocketing_delta_pct": 100 * (cost_a["total_usd"] - base["total_usd"])
                               / base["total_usd"],
        "envelope_10pct_usd": cost_b["total_usd"],
        "envelope_delta_pct": 100 * (cost_b["total_usd"] - base["total_usd"])
                              / base["total_usd"],
    }


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    geo = geometry()

    cases = {}
    for name, level in (("low", 0), ("nominal", 1), ("high", 2)):
        cases[name] = [cost(geo, level, lot) for lot in LOT_SIZES]

    result = {
        "component": "AF-DT-1000",
        "geometry_revision": "D",
        "class": "ASSUMED_COST_BASIS - rates are declared assumptions, not quotations",
        "geometry": geo,
        "assumed_rates_low_nominal_high": ASSUMED,
        "cost_by_lot": cases,
        "envelope_vs_mass": envelope_sensitivity(geo),
    }
    (OUT / "f20_cost_model.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    with (OUT / "f20_cost_breakdown.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["rate_case", "lot_size", "material_usd", "scrap_credit_usd",
                    "machining_usd", "inspection_usd", "total_usd",
                    "material_pct", "machining_pct", "inspection_pct"])
        for name, rows in cases.items():
            for r in rows:
                w.writerow([name, r["lot_size"]] +
                           [f"{r[k]:.2f}" for k in
                            ("material_usd", "scrap_credit_usd", "machining_usd",
                             "inspection_usd", "total_usd", "material_pct",
                             "machining_pct", "inspection_pct")])

    e = geo["envelope"]
    print(f"envelope        : {e['x_in']:.3f} x {e['y_in']:.3f} x {e['z_in']:.3f} in")
    print(f"min stock thick : {geo['min_stock_thickness_in']:.3f} in "
          f"<-- compare against the 2.001-2.500 in allowable band")
    print(f"part volume     : {geo['part_volume_in3']:.2f} in^3  "
          f"({geo['part_mass_kg']:.2f} kg)")
    print(f"buy-to-fly      : {geo['buy_to_fly']:.2f}   "
          f"utilisation {geo['material_utilisation_pct']:.1f}%")
    for name in ("low", "nominal", "high"):
        r = cases[name][2]   # lot of 25
        print(f"lot 25, {name:7s}: ${r['total_usd']:8.0f}  "
              f"mat {r['material_pct']:.0f}%  mach {r['machining_pct']:.0f}%  "
              f"insp {r['inspection_pct']:.0f}%")
    s = result["envelope_vs_mass"]
    print(f"-10% finished mass by pocketing : {s['pocketing_delta_pct']:+.1f}% cost")
    print(f"-10% envelope height            : {s['envelope_delta_pct']:+.1f}% cost")
    print("Written: results/f20_cost_model.json, results/f20_cost_breakdown.csv")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
