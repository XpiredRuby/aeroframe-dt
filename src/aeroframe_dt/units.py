"""Explicit engineering-unit conversion into the SI calculation basis."""
from __future__ import annotations

from dataclasses import dataclass


_FACTORS_TO_SI = {
    "m": 1.0, "mm": 1e-3, "cm": 1e-2, "in": 0.0254, "ft": 0.3048,
    "N": 1.0, "kN": 1e3, "lbf": 4.4482216152605, "kip": 4448.2216152605,
    "Pa": 1.0, "kPa": 1e3, "MPa": 1e6, "GPa": 1e9, "psi": 6894.757293168, "ksi": 6_894_757.293168,
    "N*m": 1.0, "N*mm": 1e-3, "lbf*in": 0.1129848290276167, "lbf*ft": 1.3558179483314004,
    "kg": 1.0, "g": 1e-3, "lbm": 0.45359237,
    "kg/m3": 1.0, "lbm/in3": 27679.904710191,
}


@dataclass(frozen=True)
class Quantity:
    value: float
    unit: str

    def to_si(self) -> float:
        try:
            factor = _FACTORS_TO_SI[self.unit]
        except KeyError as exc:
            raise ValueError(f"unsupported unit: {self.unit}") from exc
        return float(self.value) * factor


def convert(value: float, from_unit: str, to_unit: str) -> float:
    try:
        from_factor = _FACTORS_TO_SI[from_unit]; to_factor = _FACTORS_TO_SI[to_unit]
    except KeyError as exc:
        raise ValueError(f"unsupported unit: {exc.args[0]}") from exc
    return float(value) * from_factor / to_factor


def supported_units() -> tuple[str, ...]:
    return tuple(sorted(_FACTORS_TO_SI))
