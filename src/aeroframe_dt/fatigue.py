"""Fatigue and damage-tolerance screening utilities.

All calculations are screening-level and require source-backed material data.
"""
from __future__ import annotations
from dataclasses import asdict, dataclass
from math import pi
from typing import Iterable

@dataclass(frozen=True)
class SpectrumBlock:
    cycles: float
    stress_max_Pa: float
    stress_min_Pa: float

@dataclass(frozen=True)
class FatigueResult:
    miner_damage: float
    blocks: list[dict[str, float]]
    life_blocks: float
    method: str
    def to_dict(self): return asdict(self)

def goodman_equivalent_amplitude(stress_max_Pa: float, stress_min_Pa: float, ultimate_Pa: float) -> float:
    if ultimate_Pa <= 0: raise ValueError('ultimate_Pa must be positive')
    sa = abs(stress_max_Pa-stress_min_Pa)/2
    sm = (stress_max_Pa+stress_min_Pa)/2
    if sm >= ultimate_Pa: return float('inf')
    return sa/(1-sm/ultimate_Pa)

def basquin_cycles(stress_amplitude_Pa: float, sigma_f_prime_Pa: float, b: float) -> float:
    if stress_amplitude_Pa <= 0 or sigma_f_prime_Pa <= 0: raise ValueError('stresses must be positive')
    if b >= 0: raise ValueError('Basquin exponent b must be negative')
    reversals = (stress_amplitude_Pa/sigma_f_prime_Pa)**(1/b)
    return reversals/2

def miner_damage(blocks: Iterable[SpectrumBlock], sigma_f_prime_Pa: float, b: float, ultimate_Pa: float) -> FatigueResult:
    rows=[]; damage=0.0
    for block in blocks:
        if block.cycles < 0: raise ValueError('cycles must be nonnegative')
        seq=goodman_equivalent_amplitude(block.stress_max_Pa, block.stress_min_Pa, ultimate_Pa)
        life=0.0 if seq == float('inf') else basquin_cycles(seq, sigma_f_prime_Pa, b)
        d=float('inf') if life == 0 else block.cycles/life
        damage += d
        rows.append({'cycles':block.cycles,'equivalent_amplitude_Pa':seq,'life_cycles':life,'damage':d})
    life_blocks=0.0 if damage == float('inf') else (float('inf') if damage == 0 else 1/damage)
    return FatigueResult(damage, rows, life_blocks, 'Goodman + Basquin + Palmgren-Miner screening')

def geometry_factor_edge_crack(a_m: float, width_m: float) -> float:
    if not 0 < a_m < width_m: raise ValueError('require 0 < a < width')
    x=a_m/width_m
    return 1.12 - 0.231*x + 10.55*x**2 - 21.72*x**3 + 30.39*x**4

def stress_intensity_range(delta_sigma_Pa: float, a_m: float, width_m: float, geometry_factor: float|None=None) -> float:
    if delta_sigma_Pa < 0: raise ValueError('delta_sigma_Pa must be nonnegative')
    y=geometry_factor_edge_crack(a_m,width_m) if geometry_factor is None else geometry_factor
    if y <= 0: raise ValueError('geometry factor must be positive')
    return y*delta_sigma_Pa*(pi*a_m)**0.5

def paris_growth_cycles(a0_m: float, af_m: float, delta_sigma_Pa: float, width_m: float, C: float, m: float, steps: int=4000) -> float:
    if not 0 < a0_m < af_m < width_m: raise ValueError('require 0 < a0 < af < width')
    if C <= 0 or m <= 0 or steps < 10: raise ValueError('invalid Paris parameters')
    da=(af_m-a0_m)/steps; cycles=0.0
    for i in range(steps):
        a=a0_m+(i+0.5)*da
        dk=stress_intensity_range(delta_sigma_Pa,a,width_m)
        cycles += da/(C*dk**m)
    return cycles

def critical_crack_size(fracture_toughness_Pa_sqrt_m: float, max_stress_Pa: float, width_m: float, tol: float=1e-10) -> float:
    if fracture_toughness_Pa_sqrt_m <= 0 or max_stress_Pa <= 0 or width_m <= 0: raise ValueError('inputs must be positive')
    lo,hi=1e-12,width_m*(1-1e-9)
    for _ in range(200):
        mid=(lo+hi)/2
        k=geometry_factor_edge_crack(mid,width_m)*max_stress_Pa*(pi*mid)**0.5
        if k < fracture_toughness_Pa_sqrt_m: lo=mid
        else: hi=mid
        if hi-lo < tol: break
    return (lo+hi)/2
