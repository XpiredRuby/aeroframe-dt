"""Lightweight STEP/AP242 exchange-file inventory and PMI continuity checks."""
from __future__ import annotations

from collections import Counter
from dataclasses import asdict, dataclass
import re
from pathlib import Path
from typing import Iterable


_ENTITY = re.compile(r"#\d+\s*=\s*([A-Z0-9_]+)\s*\(", re.I)
_SCHEMA = re.compile(r"FILE_SCHEMA\s*\(\s*\((.*?)\)\s*\)\s*;", re.I | re.S)

PMI_ENTITIES = {
    "DATUM", "DATUM_FEATURE", "DATUM_REFERENCE", "DATUM_REFERENCE_COMPARTMENT",
    "GEOMETRIC_TOLERANCE", "POSITION_TOLERANCE", "FLATNESS_TOLERANCE",
    "PERPENDICULARITY_TOLERANCE", "PARALLELISM_TOLERANCE", "PROFILE_TOLERANCE",
    "DIMENSIONAL_SIZE", "DIMENSIONAL_LOCATION", "SHAPE_ASPECT", "SHAPE_ASPECT_RELATIONSHIP",
    "PLUS_MINUS_TOLERANCE", "TOLERANCE_VALUE", "DRAUGHTING_MODEL",
}


@dataclass(frozen=True)
class StepInventory:
    path: str
    schemas: tuple[str, ...]
    entity_count: int
    entity_types: dict[str, int]
    pmi_entity_types: dict[str, int]
    likely_ap242: bool

    def to_dict(self) -> dict:
        return asdict(self)


def inventory_step_text(text: str, path: str = "") -> StepInventory:
    schemas: list[str] = []
    match = _SCHEMA.search(text)
    if match:
        schemas = [item.strip().strip("'").upper() for item in match.group(1).split(",")]
    counts = Counter(entity.upper() for entity in _ENTITY.findall(text))
    pmi = {name: counts[name] for name in sorted(PMI_ENTITIES) if counts[name]}
    likely = any("AP242" in schema or "MANAGED_MODEL_BASED" in schema for schema in schemas)
    return StepInventory(path, tuple(schemas), sum(counts.values()), dict(counts), pmi, likely)


def inventory_step_file(path: str | Path) -> StepInventory:
    file = Path(path)
    return inventory_step_text(file.read_text(encoding="utf-8", errors="replace"), file.as_posix())


def compare_pmi_inventory(native_characteristic_ids: Iterable[str], exchange: StepInventory, minimum_pmi_entities: int | None = None) -> dict:
    identifiers = [item for item in native_characteristic_ids if item]
    expected = minimum_pmi_entities if minimum_pmi_entities is not None else len(identifiers)
    observed = sum(exchange.pmi_entity_types.values())
    issues: list[str] = []
    if not exchange.likely_ap242:
        issues.append("FILE_SCHEMA does not identify an AP242/managed-model-based schema")
    if observed < expected:
        issues.append(f"PMI entity inventory {observed} is below expected floor {expected}")
    return {
        "native_characteristic_count": len(identifiers),
        "expected_pmi_entity_floor": expected,
        "exchange_pmi_entity_count": observed,
        "exchange_schemas": exchange.schemas,
        "issues": issues,
        "passed_inventory_screen": not issues,
        "limitation": "Entity inventory is not semantic PMI validation; use NIST test cases and a standards-compliant reader for final verification.",
    }
