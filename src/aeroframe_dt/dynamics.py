"""Analytical modal, buckling, and vibration screening utilities."""
from __future__ import annotations

from dataclasses import asdict, dataclass
from math import pi, sqrt


@dataclass(frozen=True)
class ModeComparison:
    mode: int
    analytical_Hz: float
    numerical_Hz: float
    difference_fraction: float
    passed: bool

    def to_dict(self) -> dict:
        return asdict(self)


def cantilever_bending_frequency_Hz(
    mode: int,
    length_m: float,
    elastic_modulus_Pa: float,
    second_moment_m4: float,
    mass_per_length_kg_per_m: float,
) -> float:
    roots = {1: 1.875104068711961, 2: 4.694091132974174, 3: 7.854757438237612, 4: 10.995540734875466}
    if mode not in roots:
        raise ValueError("mode must be 1 through 4")
    if min(length_m, elastic_modulus_Pa, second_moment_m4, mass_per_length_kg_per_m) <= 0:
        raise ValueError("all properties must be positive")
    beta = roots[mode]
    omega = beta**2 * sqrt(elastic_modulus_Pa * second_moment_m4 / mass_per_length_kg_per_m) / length_m**2
    return omega / (2 * pi)


def euler_column_buckling_load_N(
    elastic_modulus_Pa: float,
    second_moment_m4: float,
    length_m: float,
    effective_length_factor: float = 1.0,
) -> float:
    if min(elastic_modulus_Pa, second_moment_m4, length_m, effective_length_factor) <= 0:
        raise ValueError("all properties must be positive")
    return pi**2 * elastic_modulus_Pa * second_moment_m4 / (effective_length_factor * length_m) ** 2


def single_dof_transmissibility(frequency_ratio: float, damping_ratio: float) -> float:
    if frequency_ratio < 0 or damping_ratio < 0:
        raise ValueError("frequency and damping ratios must be nonnegative")
    numerator = sqrt(1 + (2 * damping_ratio * frequency_ratio) ** 2)
    denominator = sqrt((1 - frequency_ratio**2) ** 2 + (2 * damping_ratio * frequency_ratio) ** 2)
    return numerator / denominator


def compare_frequency(mode: int, analytical_Hz: float, numerical_Hz: float, tolerance_fraction: float = 0.05) -> ModeComparison:
    if min(analytical_Hz, numerical_Hz, tolerance_fraction) <= 0:
        raise ValueError("frequencies and tolerance must be positive")
    difference = abs(numerical_Hz - analytical_Hz) / analytical_Hz
    return ModeComparison(mode, analytical_Hz, numerical_Hz, difference, difference <= tolerance_fraction)
