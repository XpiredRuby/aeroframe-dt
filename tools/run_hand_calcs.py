#!/usr/bin/env python3
"""Run selected hand calculations from a JSON case."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from aeroframe_dt import hand_calcs as hc  # noqa: E402


FUNCTIONS = {
    "lug_net_section": hc.lug_net_section,
    "projected_bearing": hc.projected_bearing,
    "two_plane_shear_out": hc.two_plane_shear_out,
    "pin_shear": hc.pin_shear,
    "rectangular_plate_bending": hc.rectangular_plate_bending,
    "shear_tension_interaction": hc.shear_tension_interaction,
}


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: run_hand_calcs.py CASE.json", file=sys.stderr)
        return 2
    data = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    results = []
    for item in data["checks"]:
        name = item["function"]
        try:
            function = FUNCTIONS[name]
        except KeyError as exc:
            raise ValueError(f"Unsupported hand-calculation function: {name}") from exc
        result = function(**item["arguments"])
        results.append(result.to_dict())
    print(json.dumps({"case_id": data["case_id"], "classification": data["classification"], "results": results}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
