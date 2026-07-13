#!/usr/bin/env python3
"""Run a JSON pylon load case and emit a compact manifest."""

from __future__ import annotations

import json
import sys
from dataclasses import asdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from aeroframe_dt.loads import AppliedLoad, SupportModel, assemble_resultant, solve_two_station_supports  # noqa: E402
from aeroframe_dt.vector import vec3  # noqa: E402


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: run_load_model.py CASE.json", file=sys.stderr)
        return 2
    path = Path(sys.argv[1])
    data = json.loads(path.read_text(encoding="utf-8"))
    loads = [
        AppliedLoad(
            load_id=item["load_id"],
            point_m=vec3(item["point_m"]),
            force_N=vec3(item["force_N"]),
            free_moment_Nm=vec3(item.get("free_moment_Nm", [0, 0, 0])),
            provenance=item.get("provenance", "UNSPECIFIED"),
        )
        for item in data["loads"]
    ]
    resultant = assemble_resultant(loads, vec3(data.get("reference_m", [0, 0, 0])))
    model = SupportModel(**data["support_model"])
    solution = solve_two_station_supports(resultant, model)
    output = {
        "case_id": data["case_id"],
        "classification": data["classification"],
        "resultant": asdict(resultant),
        "support_solution": asdict(solution),
        "equilibrium": {
            "force_residual_norm_N": solution.residual_force_norm_N,
            "moment_residual_norm_Nm": solution.residual_moment_norm_Nm,
        },
    }
    print(json.dumps(output, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
