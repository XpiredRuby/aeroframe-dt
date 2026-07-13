"""Predeclared structural-result extraction operations.

These utilities favor integrated resultants, weighted averages, and structural
linearization over unconverged local maxima.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from math import sqrt
from statistics import mean
from typing import Iterable, Sequence


Vector3 = tuple[float, float, float]


@dataclass(frozen=True)
class LinearizedStress:
    membrane_Pa: float
    bending_gradient_Pa_per_m: float
    inner_surface_Pa: float
    outer_surface_Pa: float
    rms_residual_Pa: float

    def to_dict(self) -> dict:
        return asdict(self)


def weighted_average(values: Sequence[float], weights: Sequence[float]) -> float:
    if len(values) != len(weights) or not values:
        raise ValueError("values and weights must be equal and nonempty")
    if any(weight < 0 for weight in weights):
        raise ValueError("weights must be nonnegative")
    total = sum(weights)
    if total <= 0:
        raise ValueError("weight sum must be positive")
    return sum(value * weight for value, weight in zip(values, weights)) / total


def percentile(values: Sequence[float], fraction: float) -> float:
    if not values or not 0 <= fraction <= 1:
        raise ValueError("nonempty values and fraction in [0,1] required")
    ordered = sorted(values)
    index = fraction * (len(ordered) - 1)
    lo = int(index); hi = min(lo + 1, len(ordered) - 1); alpha = index - lo
    return ordered[lo] * (1 - alpha) + ordered[hi] * alpha


def integrate_tractions(tractions_Pa: Sequence[Vector3], tributary_areas_m2: Sequence[float]) -> Vector3:
    if len(tractions_Pa) != len(tributary_areas_m2) or not tractions_Pa:
        raise ValueError("tractions and areas must be equal and nonempty")
    if any(area < 0 for area in tributary_areas_m2):
        raise ValueError("areas must be nonnegative")
    return tuple(sum(traction[i] * area for traction, area in zip(tractions_Pa, tributary_areas_m2)) for i in range(3))  # type: ignore[return-value]


def integrate_force_moment(
    points_m: Sequence[Vector3], forces_N: Sequence[Vector3], reference_m: Vector3 = (0.0, 0.0, 0.0)
) -> tuple[Vector3, Vector3]:
    if len(points_m) != len(forces_N) or not points_m:
        raise ValueError("points and forces must be equal and nonempty")
    force = [0.0, 0.0, 0.0]; moment = [0.0, 0.0, 0.0]
    for point, item in zip(points_m, forces_N):
        for i in range(3): force[i] += item[i]
        rx, ry, rz = (point[i] - reference_m[i] for i in range(3)); fx, fy, fz = item
        moment[0] += ry * fz - rz * fy
        moment[1] += rz * fx - rx * fz
        moment[2] += rx * fy - ry * fx
    return tuple(force), tuple(moment)  # type: ignore[return-value]


def linearize_stress_through_thickness(coordinates_m: Sequence[float], stresses_Pa: Sequence[float]) -> LinearizedStress:
    """Least-squares membrane+bending fit across a thickness path."""
    if len(coordinates_m) != len(stresses_Pa) or len(coordinates_m) < 2:
        raise ValueError("at least two aligned samples are required")
    zbar = mean(coordinates_m); sbar = mean(stresses_Pa)
    denominator = sum((z - zbar) ** 2 for z in coordinates_m)
    if denominator <= 0:
        raise ValueError("coordinates must span a nonzero thickness")
    gradient = sum((z - zbar) * (s - sbar) for z, s in zip(coordinates_m, stresses_Pa)) / denominator
    membrane = sbar - gradient * zbar
    fitted = [membrane + gradient * z for z in coordinates_m]
    rms = sqrt(sum((actual - fit) ** 2 for actual, fit in zip(stresses_Pa, fitted)) / len(fitted))
    zmin, zmax = min(coordinates_m), max(coordinates_m)
    return LinearizedStress(membrane, gradient, membrane + gradient * zmin, membrane + gradient * zmax, rms)


def extraction_summary(values: Sequence[float], weights: Sequence[float] | None = None) -> dict:
    if not values:
        raise ValueError("values are required")
    return {
        "count": len(values),
        "minimum": min(values),
        "maximum": max(values),
        "mean": mean(values),
        "weighted_mean": None if weights is None else weighted_average(values, weights),
        "p95": percentile(values, .95),
        "p99": percentile(values, .99),
        "warning": "Maximum values require mesh-convergence and singularity review before use in margins.",
    }
