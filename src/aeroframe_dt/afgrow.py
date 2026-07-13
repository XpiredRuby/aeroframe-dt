"""AFGROW-neutral case packaging and output parsing.

AFGROW's interactive/project formats can vary by release. This module therefore
creates a source-controlled neutral case package and parses exported tabular
results rather than inventing a proprietary file format.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
import csv
import json
from pathlib import Path
from typing import Iterable


@dataclass(frozen=True)
class AFGROWCase:
    case_id: str
    model_type: str
    material_source: str
    spectrum_source: str
    initial_crack_m: float
    final_crack_m: float
    width_m: float
    stress_scale_Pa: float
    geometry_revision: str
    notes: str = ""

    def validate(self) -> None:
        required = (self.case_id, self.model_type, self.material_source, self.spectrum_source, self.geometry_revision)
        if any(not value.strip() for value in required):
            raise ValueError("AFGROW case identifiers and sources are required")
        if not 0 < self.initial_crack_m < self.final_crack_m < self.width_m:
            raise ValueError("require 0 < initial crack < final crack < width")
        if self.stress_scale_Pa <= 0:
            raise ValueError("stress_scale_Pa must be positive")

    def to_dict(self) -> dict:
        self.validate()
        return asdict(self)


def write_neutral_package(case: AFGROWCase, spectrum_rows: Iterable[dict], directory: str | Path) -> tuple[Path, Path, Path]:
    case.validate()
    root = Path(directory)
    root.mkdir(parents=True, exist_ok=True)
    case_path = root / "case.json"
    spectrum_path = root / "spectrum.csv"
    instructions_path = root / "AFGROW_IMPORT_INSTRUCTIONS.md"
    case_path.write_text(json.dumps(case.to_dict(), indent=2, sort_keys=True) + "\n", encoding="utf-8")
    rows = list(spectrum_rows)
    required = {"sequence", "cycles", "stress_max_Pa", "stress_min_Pa"}
    if not rows or any(required - set(row) for row in rows):
        raise ValueError("spectrum rows require sequence, cycles, stress_max_Pa, stress_min_Pa")
    with spectrum_path.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=sorted(required))
        writer.writeheader(); writer.writerows(rows)
    instructions_path.write_text(
        "# AFGROW Import/Execution Contract\n\n"
        "1. Create a new AFGROW model matching `case.json`.\n"
        "2. Select material data only from the recorded source; archive the exact source and units.\n"
        "3. Import or enter `spectrum.csv` without rescaling unless the scale is recorded.\n"
        "4. Save the native project beside this package.\n"
        "5. Export crack length versus cycles as CSV with columns `cycles,crack_length_m`.\n"
        "6. Export the run summary and warnings. Do not overwrite the pre-run package.\n"
        "7. Return the native project, exported CSV, summary, and software version.\n\n"
        "This workflow is damage-tolerance screening, not certification substantiation.\n",
        encoding="utf-8",
    )
    return case_path, spectrum_path, instructions_path


def parse_growth_csv(path: str | Path) -> list[tuple[float, float]]:
    rows: list[tuple[float, float]] = []
    with Path(path).open(newline="", encoding="utf-8") as stream:
        reader = csv.DictReader(stream)
        if not reader.fieldnames or not {"cycles", "crack_length_m"}.issubset(reader.fieldnames):
            raise ValueError("expected cycles and crack_length_m columns")
        for item in reader:
            cycles, crack = float(item["cycles"]), float(item["crack_length_m"])
            if cycles < 0 or crack <= 0:
                raise ValueError("invalid growth data")
            rows.append((cycles, crack))
    if len(rows) < 2:
        raise ValueError("at least two growth rows are required")
    if any(rows[i + 1][0] < rows[i][0] or rows[i + 1][1] < rows[i][1] for i in range(len(rows) - 1)):
        raise ValueError("cycles and crack length must be nondecreasing")
    return rows


def compare_growth_histories(reference: Iterable[tuple[float, float]], candidate: Iterable[tuple[float, float]]) -> dict:
    ref, cand = list(reference), list(candidate)
    if len(ref) != len(cand):
        raise ValueError("comparison histories must have equal sample counts")
    errors = []
    for (n_ref, a_ref), (n_cand, a_cand) in zip(ref, cand):
        if n_ref != n_cand:
            raise ValueError("cycle sample locations must match")
        errors.append(abs(a_cand - a_ref) / max(abs(a_ref), 1e-30))
    return {"samples": len(errors), "max_relative_error": max(errors), "mean_relative_error": sum(errors) / len(errors)}
