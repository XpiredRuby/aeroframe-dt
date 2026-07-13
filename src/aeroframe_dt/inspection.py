"""Inspection planning, measurement-system screening, capability, and NCR workflows."""
from __future__ import annotations

from dataclasses import asdict, dataclass
from math import sqrt
from statistics import mean, stdev
from typing import Iterable, Mapping, Sequence


@dataclass(frozen=True)
class InspectionCharacteristic:
    characteristic_id: str
    requirement_id: str
    feature_id: str
    nominal: float
    lower_limit: float
    upper_limit: float
    units: str
    method: str
    instrument: str
    resolution: float
    sampling_plan: str

    def validate(self) -> None:
        if not self.lower_limit < self.upper_limit:
            raise ValueError("lower_limit must be less than upper_limit")
        if not self.lower_limit <= self.nominal <= self.upper_limit:
            raise ValueError("nominal must lie within limits")
        if self.resolution <= 0:
            raise ValueError("instrument resolution must be positive")
        for value in (self.characteristic_id, self.requirement_id, self.feature_id, self.units, self.method, self.instrument, self.sampling_plan):
            if not value.strip():
                raise ValueError("inspection fields must not be blank")


@dataclass(frozen=True)
class CapabilityResult:
    count: int
    mean: float
    sample_std: float
    cp: float
    cpk: float
    lower_limit: float
    upper_limit: float

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass(frozen=True)
class GageRRResult:
    repeatability_variance: float
    reproducibility_variance: float
    part_variance: float
    gage_rr_variance: float
    total_variance: float
    percent_gage_rr: float

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass(frozen=True)
class Nonconformance:
    ncr_id: str
    characteristic_id: str
    detected_value: float
    requirement: str
    containment: str
    structural_assessment: str
    disposition: str
    root_cause: str
    corrective_action: str
    reverification: str
    geometry_revision: str
    status: str

    def validate(self) -> None:
        for key, value in asdict(self).items():
            if isinstance(value, str) and not value.strip():
                raise ValueError(f"{key} must not be blank")


def capability(values: Sequence[float], lower_limit: float, upper_limit: float) -> CapabilityResult:
    if len(values) < 2:
        raise ValueError("at least two measurements are required")
    if lower_limit >= upper_limit:
        raise ValueError("invalid specification limits")
    avg = mean(values)
    sigma = stdev(values)
    if sigma == 0:
        cp = cpk = float("inf")
    else:
        cp = (upper_limit - lower_limit) / (6 * sigma)
        cpk = min((upper_limit - avg) / (3 * sigma), (avg - lower_limit) / (3 * sigma))
    return CapabilityResult(len(values), avg, sigma, cp, cpk, lower_limit, upper_limit)


def crossed_gage_rr(measurements: Mapping[str, Mapping[str, Sequence[float]]]) -> GageRRResult:
    """Balanced crossed gage R&R screening using variance components.

    Input shape: part -> operator -> repeated measurements. The implementation
    requires the same operators and repeat count for every part.
    """
    if len(measurements) < 2:
        raise ValueError("at least two parts are required")
    operators = None
    repeat_count = None
    for part, by_operator in measurements.items():
        current = tuple(sorted(by_operator))
        operators = current if operators is None else operators
        if current != operators:
            raise ValueError("all parts must use the same operators")
        for values in by_operator.values():
            repeat_count = len(values) if repeat_count is None else repeat_count
            if len(values) != repeat_count or repeat_count < 2:
                raise ValueError("balanced repeated measurements are required")
    assert operators is not None and repeat_count is not None

    cell_means: dict[tuple[str, str], float] = {}
    repeat_ss = 0.0
    for part, by_operator in measurements.items():
        for operator, values in by_operator.items():
            avg = mean(values)
            cell_means[(part, operator)] = avg
            repeat_ss += sum((value - avg) ** 2 for value in values)
    repeat_df = len(measurements) * len(operators) * (repeat_count - 1)
    repeat_var = repeat_ss / repeat_df

    part_means = {part: mean(cell_means[(part, op)] for op in operators) for part in measurements}
    operator_means = {op: mean(cell_means[(part, op)] for part in measurements) for op in operators}
    grand = mean(cell_means.values())
    part_var_observed = sum((value - grand) ** 2 for value in part_means.values()) / (len(part_means) - 1)
    operator_var_observed = (
        sum((value - grand) ** 2 for value in operator_means.values()) / (len(operator_means) - 1)
        if len(operator_means) > 1 else 0.0
    )
    part_var = max(0.0, part_var_observed - repeat_var / (len(operators) * repeat_count))
    operator_var = max(0.0, operator_var_observed - repeat_var / (len(measurements) * repeat_count))
    gage_var = repeat_var + operator_var
    total = gage_var + part_var
    percent = 0.0 if total == 0 else 100 * sqrt(gage_var / total)
    return GageRRResult(repeat_var, operator_var, part_var, gage_var, total, percent)


def disposition_complete(ncr: Nonconformance) -> bool:
    ncr.validate()
    return ncr.status.upper() in {"CLOSED", "ACCEPTED", "REWORKED", "SCRAPPED"}
