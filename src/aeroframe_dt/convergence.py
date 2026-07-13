"""Mesh and numerical-convergence assessment utilities."""
from __future__ import annotations

from dataclasses import asdict, dataclass
from math import log
from typing import Iterable


@dataclass(frozen=True)
class ConvergencePoint:
    characteristic_size: float
    value: float
    dof: int | None = None
    run_id: str = ""


@dataclass(frozen=True)
class ConvergenceAssessment:
    monotonic: bool
    apparent_order: float | None
    extrapolated_value: float | None
    final_change_fraction: float
    gci_fine_fraction: float | None
    passed: bool
    tolerance_fraction: float
    notes: tuple[str, ...]

    def to_dict(self) -> dict:
        return asdict(self)


def _validate(points: list[ConvergencePoint]) -> None:
    if len(points) < 2:
        raise ValueError("at least two convergence points are required")
    if any(point.characteristic_size <= 0 for point in points):
        raise ValueError("characteristic sizes must be positive")
    if len({point.characteristic_size for point in points}) != len(points):
        raise ValueError("characteristic sizes must be unique")


def assess_convergence(
    points: Iterable[ConvergencePoint],
    tolerance_fraction: float = 0.02,
    safety_factor: float = 1.25,
) -> ConvergenceAssessment:
    rows = sorted(list(points), key=lambda item: item.characteristic_size, reverse=True)
    _validate(rows)
    if tolerance_fraction <= 0 or safety_factor <= 0:
        raise ValueError("tolerance and safety factor must be positive")

    values = [row.value for row in rows]
    differences = [values[i + 1] - values[i] for i in range(len(values) - 1)]
    nonzero = [delta for delta in differences if delta != 0]
    monotonic = not nonzero or all(delta > 0 for delta in nonzero) or all(delta < 0 for delta in nonzero)
    denom = max(abs(values[-1]), 1e-30)
    final_change = abs(values[-1] - values[-2]) / denom
    order = extrapolated = gci = None
    notes: list[str] = []

    if len(rows) >= 3:
        h1, h2, h3 = rows[-1].characteristic_size, rows[-2].characteristic_size, rows[-3].characteristic_size
        f1, f2, f3 = values[-1], values[-2], values[-3]
        r21, r32 = h2 / h1, h3 / h2
        if abs(r21 - r32) / max(r21, r32) <= 0.05 and r21 > 1.0 and (f2 - f1) != 0 and (f3 - f2) != 0:
            ratio = abs((f3 - f2) / (f2 - f1))
            if ratio > 0 and ratio != 1:
                order = log(ratio) / log(r21)
                if order > 0:
                    extrapolated = f1 + (f1 - f2) / (r21**order - 1.0)
                    gci = safety_factor * abs((f1 - f2) / max(abs(f1), 1e-30)) / (r21**order - 1.0)
                else:
                    notes.append("non-positive apparent order; Richardson extrapolation rejected")
        else:
            notes.append("last three meshes are not approximately uniformly refined")
    else:
        notes.append("three points are required for apparent order and GCI")

    if not monotonic:
        notes.append("response is non-monotonic; investigate modeling or extraction sensitivity")
    passed = final_change <= tolerance_fraction and monotonic
    if gci is not None:
        passed = passed and gci <= tolerance_fraction
    return ConvergenceAssessment(monotonic, order, extrapolated, final_change, gci, passed, tolerance_fraction, tuple(notes))


def compare_solver_results(reference: float, candidate: float, tolerance_fraction: float, absolute_floor: float = 1e-12) -> dict[str, float | bool]:
    if tolerance_fraction <= 0:
        raise ValueError("tolerance_fraction must be positive")
    denominator = max(abs(reference), abs(candidate), absolute_floor)
    difference = candidate - reference
    fraction = abs(difference) / denominator
    return {
        "reference": reference,
        "candidate": candidate,
        "difference": difference,
        "difference_fraction": fraction,
        "tolerance_fraction": tolerance_fraction,
        "passed": fraction <= tolerance_fraction,
    }
