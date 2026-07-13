"""Dependency-free design-of-experiments and robust ranking tools."""
from __future__ import annotations

from dataclasses import asdict, dataclass
from itertools import product
from math import prod
from typing import Callable, Iterable, Mapping, Sequence


@dataclass(frozen=True)
class DesignVariable:
    name: str
    low: float
    high: float
    levels: int = 3

    def values(self) -> tuple[float, ...]:
        if self.high <= self.low or self.levels < 2:
            raise ValueError(f"invalid variable definition for {self.name}")
        step = (self.high - self.low) / (self.levels - 1)
        return tuple(self.low + i * step for i in range(self.levels))


@dataclass(frozen=True)
class CandidateResult:
    candidate_id: str
    variables: Mapping[str, float]
    mass_kg: float
    nominal_margin: float
    robust_margin: float
    manufacturable: bool
    constraints: Mapping[str, float]
    objective: float

    def to_dict(self) -> dict:
        return asdict(self)


def full_factorial(variables: Sequence[DesignVariable]) -> list[dict[str, float]]:
    if not variables:
        raise ValueError("at least one design variable is required")
    names = [variable.name for variable in variables]
    if len(set(names)) != len(names):
        raise ValueError("design variable names must be unique")
    return [dict(zip(names, values)) for values in product(*(variable.values() for variable in variables))]


def evaluate_candidates(
    designs: Iterable[Mapping[str, float]],
    evaluator: Callable[[Mapping[str, float]], Mapping[str, float | bool]],
    mass_weight: float = 1.0,
    margin_weight: float = 1.0,
) -> list[CandidateResult]:
    if mass_weight < 0 or margin_weight < 0:
        raise ValueError("weights must be nonnegative")
    rows: list[CandidateResult] = []
    for index, design in enumerate(designs, start=1):
        response = evaluator(design)
        mass = float(response["mass_kg"])
        nominal = float(response["nominal_margin"])
        robust = float(response.get("robust_margin", nominal))
        manufacturable = bool(response.get("manufacturable", True))
        constraints = {str(k): float(v) for k, v in dict(response.get("constraints", {})).items()}
        infeasible_penalty = 1e6 if not manufacturable or any(value < 0 for value in constraints.values()) else 0.0
        objective = mass_weight * mass - margin_weight * robust + infeasible_penalty
        rows.append(CandidateResult(f"CAND-{index:04d}", dict(design), mass, nominal, robust, manufacturable, constraints, objective))
    return sorted(rows, key=lambda row: (row.objective, row.mass_kg, -row.robust_margin))


def pareto_front(rows: Iterable[CandidateResult]) -> list[CandidateResult]:
    candidates = list(rows)
    front: list[CandidateResult] = []
    for candidate in candidates:
        if not candidate.manufacturable or any(value < 0 for value in candidate.constraints.values()):
            continue
        dominated = any(
            other.candidate_id != candidate.candidate_id
            and other.mass_kg <= candidate.mass_kg
            and other.robust_margin >= candidate.robust_margin
            and (other.mass_kg < candidate.mass_kg or other.robust_margin > candidate.robust_margin)
            for other in candidates
            if other.manufacturable and all(value >= 0 for value in other.constraints.values())
        )
        if not dominated:
            front.append(candidate)
    return sorted(front, key=lambda row: (row.mass_kg, -row.robust_margin))
