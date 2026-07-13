"""Source-gated material and fastener trade studies."""
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Iterable, Mapping


@dataclass(frozen=True)
class MaterialCandidate:
    material_id: str
    name: str
    product_form: str
    heat_treatment: str
    density_kg_m3: float
    elastic_modulus_Pa: float
    poisson: float
    tension_allowable_Pa: float | None
    shear_allowable_Pa: float | None
    bearing_allowable_Pa: float | None
    source_id: str
    source_class: str
    corrosion_note: str
    manufacturing_note: str

    def validate(self, require_allowables: bool = False) -> None:
        for value in (self.material_id, self.name, self.product_form, self.heat_treatment, self.source_id, self.source_class):
            if not value.strip(): raise ValueError("material identification and source fields are required")
        if min(self.density_kg_m3, self.elastic_modulus_Pa) <= 0 or not -1 < self.poisson < 0.5:
            raise ValueError("invalid physical properties")
        allowables = (self.tension_allowable_Pa, self.shear_allowable_Pa, self.bearing_allowable_Pa)
        if require_allowables and any(value is None for value in allowables):
            raise ValueError(f"{self.material_id} lacks required allowables")
        if any(value is not None and value <= 0 for value in allowables):
            raise ValueError("allowables must be positive when supplied")


@dataclass(frozen=True)
class FastenerCandidate:
    fastener_id: str
    specification: str
    material: str
    diameter_m: float
    shear_allowable_N: float | None
    tension_allowable_N: float | None
    preload_target_N: float | None
    source_id: str
    source_class: str
    notes: str = ""

    def validate(self, require_allowables: bool = False) -> None:
        if not all(value.strip() for value in (self.fastener_id, self.specification, self.material, self.source_id, self.source_class)):
            raise ValueError("fastener identification and source fields are required")
        if self.diameter_m <= 0: raise ValueError("fastener diameter must be positive")
        values = (self.shear_allowable_N, self.tension_allowable_N, self.preload_target_N)
        if require_allowables and any(value is None for value in values[:2]): raise ValueError("fastener allowables are required")
        if any(value is not None and value <= 0 for value in values): raise ValueError("fastener capacities must be positive")


def rank_materials(
    candidates: Iterable[MaterialCandidate],
    volume_m3: float,
    demand_tension_Pa: float,
    demand_shear_Pa: float,
    demand_bearing_Pa: float,
    safety_factor: float = 1.0,
) -> list[dict]:
    if min(volume_m3, safety_factor) <= 0 or min(demand_tension_Pa, demand_shear_Pa, demand_bearing_Pa) < 0:
        raise ValueError("invalid trade inputs")
    rows: list[dict] = []
    for candidate in candidates:
        candidate.validate(require_allowables=True)
        margins = {
            "tension_margin": candidate.tension_allowable_Pa / (max(demand_tension_Pa, 1e-30) * safety_factor) - 1,
            "shear_margin": candidate.shear_allowable_Pa / (max(demand_shear_Pa, 1e-30) * safety_factor) - 1,
            "bearing_margin": candidate.bearing_allowable_Pa / (max(demand_bearing_Pa, 1e-30) * safety_factor) - 1,
        }
        governing = min(margins.values())
        rows.append({
            **asdict(candidate), "mass_kg": candidate.density_kg_m3 * volume_m3,
            **margins, "governing_margin": governing, "feasible": governing >= 0,
        })
    return sorted(rows, key=lambda row: (not row["feasible"], row["mass_kg"], -row["governing_margin"]))


def rank_fasteners(candidates: Iterable[FastenerCandidate], shear_demand_N: float, tension_demand_N: float, exponent: float = 2.0) -> list[dict]:
    if min(shear_demand_N, tension_demand_N) < 0 or exponent <= 0: raise ValueError("invalid fastener trade inputs")
    rows: list[dict] = []
    for candidate in candidates:
        candidate.validate(require_allowables=True)
        index = (shear_demand_N / candidate.shear_allowable_N) ** exponent + (tension_demand_N / candidate.tension_allowable_N) ** exponent
        margin = float("inf") if index == 0 else 1 / index - 1
        rows.append({**asdict(candidate), "interaction_index": index, "margin": margin, "feasible": margin >= 0})
    return sorted(rows, key=lambda row: (not row["feasible"], row["diameter_m"], -row["margin"]))
