"""Load-case taxonomy, scaling, combination, and provenance validation."""
from __future__ import annotations

from dataclasses import asdict, dataclass, field
import csv
import json
from pathlib import Path
from typing import Iterable, Mapping

from .loads import AppliedLoad, Resultant, assemble_resultant


VALID_LEVELS = {"SERVICE", "LIMIT", "ULTIMATE", "FATIGUE", "BENCHMARK", "SYNTHETIC"}


@dataclass(frozen=True)
class LoadCase:
    case_id: str
    title: str
    level: str
    coordinate_frame: str
    revision: str
    source_id: str
    source_class: str
    loads: tuple[AppliedLoad, ...]
    scale_factor: float = 1.0
    tags: tuple[str, ...] = ()
    notes: str = ""

    def validate(self) -> None:
        if not self.case_id.strip():
            raise ValueError("case_id is required")
        if self.level.upper() not in VALID_LEVELS:
            raise ValueError(f"unsupported load level: {self.level}")
        for name, value in {
            "coordinate_frame": self.coordinate_frame,
            "revision": self.revision,
            "source_id": self.source_id,
            "source_class": self.source_class,
        }.items():
            if not value.strip():
                raise ValueError(f"{name} is required")
        if self.scale_factor <= 0:
            raise ValueError("scale_factor must be positive")
        if not self.loads:
            raise ValueError("at least one applied load is required")

    def resultant(self, reference_m: tuple[float, float, float] = (0.0, 0.0, 0.0)) -> Resultant:
        self.validate()
        scaled = [
            AppliedLoad(
                load_id=load.load_id,
                point_m=load.point_m,
                force_N=tuple(self.scale_factor * x for x in load.force_N),
                free_moment_Nm=tuple(self.scale_factor * x for x in load.free_moment_Nm),
                provenance=load.provenance,
            )
            for load in self.loads
        ]
        return assemble_resultant(scaled, reference_m)

    def to_dict(self) -> dict:
        payload = asdict(self)
        payload["loads"] = [asdict(load) for load in self.loads]
        return payload


@dataclass(frozen=True)
class LoadCombination:
    combination_id: str
    factors: Mapping[str, float]
    level: str
    revision: str
    rationale: str

    def validate(self, cases: Mapping[str, LoadCase]) -> None:
        if self.level.upper() not in VALID_LEVELS:
            raise ValueError(f"unsupported load level: {self.level}")
        if not self.factors:
            raise ValueError("combination factors are required")
        missing = sorted(set(self.factors) - set(cases))
        if missing:
            raise KeyError(f"unknown load cases: {', '.join(missing)}")
        if not self.revision or not self.rationale:
            raise ValueError("revision and rationale are required")


def combine_resultants(
    combination: LoadCombination,
    cases: Mapping[str, LoadCase],
    reference_m: tuple[float, float, float] = (0.0, 0.0, 0.0),
) -> Resultant:
    combination.validate(cases)
    fx = fy = fz = mx = my = mz = 0.0
    for case_id, factor in combination.factors.items():
        result = cases[case_id].resultant(reference_m)
        fx += factor * result.force_N[0]
        fy += factor * result.force_N[1]
        fz += factor * result.force_N[2]
        mx += factor * result.moment_Nm[0]
        my += factor * result.moment_Nm[1]
        mz += factor * result.moment_Nm[2]
    return Resultant((fx, fy, fz), (mx, my, mz), reference_m)


def load_cases_from_json(path: str | Path) -> dict[str, LoadCase]:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    rows = data["load_cases"] if isinstance(data, dict) else data
    cases: dict[str, LoadCase] = {}
    for row in rows:
        loads = tuple(
            AppliedLoad(
                load_id=item["load_id"],
                point_m=tuple(float(x) for x in item["position_m"]),
                force_N=tuple(float(x) for x in item["force_N"]),
                free_moment_Nm=tuple(float(x) for x in item.get("free_moment_Nm", (0.0, 0.0, 0.0))),
                provenance=item.get("source", row["source_id"]),
            )
            for item in row["loads"]
        )
        case = LoadCase(
            case_id=row["case_id"],
            title=row["title"],
            level=row["level"],
            coordinate_frame=row["coordinate_frame"],
            revision=row["revision"],
            source_id=row["source_id"],
            source_class=row["source_class"],
            loads=loads,
            scale_factor=float(row.get("scale_factor", 1.0)),
            tags=tuple(row.get("tags", [])),
            notes=row.get("notes", ""),
        )
        case.validate()
        if case.case_id in cases:
            raise ValueError(f"duplicate case_id: {case.case_id}")
        cases[case.case_id] = case
    return cases


def write_resultant_csv(cases: Iterable[LoadCase], path: str | Path) -> None:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    fields = [
        "case_id", "title", "level", "revision", "source_id", "source_class",
        "fx_N", "fy_N", "fz_N", "mx_Nm", "my_Nm", "mz_Nm", "claim_level",
    ]
    with target.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields)
        writer.writeheader()
        for case in cases:
            result = case.resultant()
            writer.writerow({
                "case_id": case.case_id,
                "title": case.title,
                "level": case.level,
                "revision": case.revision,
                "source_id": case.source_id,
                "source_class": case.source_class,
                "fx_N": result.force_N[0], "fy_N": result.force_N[1], "fz_N": result.force_N[2],
                "mx_Nm": result.moment_Nm[0], "my_Nm": result.moment_Nm[1], "mz_Nm": result.moment_Nm[2],
                "claim_level": "SYNTHETIC_TEST_ONLY" if case.level.upper() == "SYNTHETIC" else "SOURCE_GATED",
            })
