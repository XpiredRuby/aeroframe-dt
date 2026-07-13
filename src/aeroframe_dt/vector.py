"""Small dependency-free 3-D vector helpers."""

from __future__ import annotations

from math import sqrt
from typing import Iterable, Tuple

Vector3 = Tuple[float, float, float]


def vec3(values: Iterable[float]) -> Vector3:
    vals = tuple(float(v) for v in values)
    if len(vals) != 3:
        raise ValueError("Expected exactly three vector components")
    return vals  # type: ignore[return-value]


def add(a: Vector3, b: Vector3) -> Vector3:
    return (a[0] + b[0], a[1] + b[1], a[2] + b[2])


def sub(a: Vector3, b: Vector3) -> Vector3:
    return (a[0] - b[0], a[1] - b[1], a[2] - b[2])


def scale(a: Vector3, s: float) -> Vector3:
    return (a[0] * s, a[1] * s, a[2] * s)


def cross(a: Vector3, b: Vector3) -> Vector3:
    return (
        a[1] * b[2] - a[2] * b[1],
        a[2] * b[0] - a[0] * b[2],
        a[0] * b[1] - a[1] * b[0],
    )


def norm(a: Vector3) -> float:
    return sqrt(a[0] ** 2 + a[1] ** 2 + a[2] ** 2)
