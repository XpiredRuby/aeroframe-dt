"""Solver-neutral compact result ingestion and validation."""
from __future__ import annotations

import csv
from dataclasses import asdict, dataclass
import json
from pathlib import Path
from typing import Iterable, Mapping


@dataclass(frozen=True)
class ResultRecord:
    run_id: str
    load_case_id: str
    geometry_revision: str
    mesh_revision: str
    solver: str
    solver_version: str
    quantity_id: str
    value: float
    units: str
    extraction_rule: str
    location: str
    status: str = "VALID"

    def validate(self) -> None:
        required = {
            "run_id": self.run_id,
            "load_case_id": self.load_case_id,
            "geometry_revision": self.geometry_revision,
            "mesh_revision": self.mesh_revision,
            "solver": self.solver,
            "solver_version": self.solver_version,
            "quantity_id": self.quantity_id,
            "units": self.units,
            "extraction_rule": self.extraction_rule,
            "location": self.location,
            "status": self.status,
        }
        missing = [key for key, value in required.items() if not str(value).strip()]
        if missing:
            raise ValueError(f"blank result fields: {', '.join(missing)}")

    def to_dict(self) -> dict:
        return asdict(self)


def read_long_csv(path: str | Path) -> list[ResultRecord]:
    rows: list[ResultRecord] = []
    with Path(path).open(newline="", encoding="utf-8") as stream:
        for item in csv.DictReader(stream):
            row = ResultRecord(
                run_id=item["run_id"], load_case_id=item["load_case_id"],
                geometry_revision=item["geometry_revision"], mesh_revision=item["mesh_revision"],
                solver=item["solver"], solver_version=item["solver_version"],
                quantity_id=item["quantity_id"], value=float(item["value"]), units=item["units"],
                extraction_rule=item["extraction_rule"], location=item["location"],
                status=item.get("status", "VALID"),
            )
            row.validate()
            rows.append(row)
    return rows


def write_long_csv(rows: Iterable[ResultRecord], path: str | Path) -> None:
    records = list(rows)
    for record in records:
        record.validate()
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    fields = list(ResultRecord.__dataclass_fields__)
    with target.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields)
        writer.writeheader()
        writer.writerows(record.to_dict() for record in records)


def validate_equilibrium(
    applied_force_N: tuple[float, float, float],
    applied_moment_Nm: tuple[float, float, float],
    reaction_force_N: tuple[float, float, float],
    reaction_moment_Nm: tuple[float, float, float],
    relative_tolerance: float = 1e-6,
    absolute_tolerance: float = 1e-9,
) -> dict:
    if relative_tolerance <= 0 or absolute_tolerance < 0:
        raise ValueError("invalid tolerances")
    force_residual = tuple(applied_force_N[i] + reaction_force_N[i] for i in range(3))
    moment_residual = tuple(applied_moment_Nm[i] + reaction_moment_Nm[i] for i in range(3))
    force_scale = max(*(abs(x) for x in applied_force_N + reaction_force_N), absolute_tolerance)
    moment_scale = max(*(abs(x) for x in applied_moment_Nm + reaction_moment_Nm), absolute_tolerance)
    force_fraction = max(abs(x) for x in force_residual) / force_scale
    moment_fraction = max(abs(x) for x in moment_residual) / moment_scale
    return {
        "force_residual_N": force_residual,
        "moment_residual_Nm": moment_residual,
        "force_residual_fraction": force_fraction,
        "moment_residual_fraction": moment_fraction,
        "relative_tolerance": relative_tolerance,
        "passed": force_fraction <= relative_tolerance and moment_fraction <= relative_tolerance,
    }


def metric_map(rows: Iterable[ResultRecord]) -> dict[str, float]:
    result: dict[str, float] = {}
    for row in rows:
        if row.quantity_id in result:
            raise ValueError(f"duplicate quantity_id: {row.quantity_id}")
        result[row.quantity_id] = row.value
    return result
