"""Dependency-free Monte Carlo and robust-design helpers."""
from __future__ import annotations
from dataclasses import dataclass
from random import Random
from statistics import mean, pstdev
from typing import Callable

@dataclass(frozen=True)
class UniformVariable:
    name:str; low:float; high:float
    def sample(self,rng:Random)->float:
        if self.high<=self.low: raise ValueError('high must exceed low')
        return rng.uniform(self.low,self.high)

def monte_carlo(model:Callable[[dict[str,float]],float], variables:list[UniformVariable], samples:int=1000, seed:int=1)->dict:
    if samples<2: raise ValueError('samples must be >=2')
    rng=Random(seed); values=[]
    for _ in range(samples): values.append(float(model({v.name:v.sample(rng) for v in variables})))
    ordered=sorted(values)
    def q(p): return ordered[round(p*(samples-1))]
    return {'samples':samples,'seed':seed,'mean':mean(values),'std':pstdev(values),'min':ordered[0],'p05':q(.05),'p50':q(.5),'p95':q(.95),'max':ordered[-1]}

def rank_robust_designs(candidates:list[dict], evaluator:Callable[[dict],dict], minimum_p05_margin:float=0.0)->list[dict]:
    out=[]
    for c in candidates:
        metrics=evaluator(c); feasible=metrics['p05_margin']>=minimum_p05_margin
        out.append({**c,**metrics,'robust_feasible':feasible})
    return sorted(out,key=lambda x:(not x['robust_feasible'],x.get('mass_kg',float('inf')),-x['p05_margin']))


@dataclass(frozen=True)
class NormalVariable:
    name: str
    mean: float
    std: float
    lower: float | None = None
    upper: float | None = None
    def sample(self, rng: Random) -> float:
        if self.std <= 0: raise ValueError('std must be positive')
        for _ in range(10000):
            value = rng.gauss(self.mean, self.std)
            if (self.lower is None or value >= self.lower) and (self.upper is None or value <= self.upper): return value
        raise RuntimeError('truncated normal sampling failed')

@dataclass(frozen=True)
class TriangularVariable:
    name: str
    low: float
    mode: float
    high: float
    def sample(self, rng: Random) -> float:
        if not self.low <= self.mode <= self.high or self.low == self.high: raise ValueError('require low <= mode <= high')
        return rng.triangular(self.low, self.high, self.mode)

def probability_of_failure(values: list[float], threshold: float = 0.0, failure_when_below: bool = True) -> float:
    if not values: raise ValueError('values are required')
    failures = sum(value < threshold if failure_when_below else value > threshold for value in values)
    return failures / len(values)

def latin_hypercube(model: Callable[[dict[str,float]],float], variables: list[UniformVariable], samples: int = 1000, seed: int = 1) -> dict:
    if samples < 2 or not variables: raise ValueError('samples >=2 and variables required')
    rng = Random(seed)
    columns: dict[str, list[float]] = {}
    for variable in variables:
        if variable.high <= variable.low: raise ValueError('high must exceed low')
        samples_u = [(i + rng.random()) / samples for i in range(samples)]
        rng.shuffle(samples_u)
        columns[variable.name] = [variable.low + u * (variable.high - variable.low) for u in samples_u]
    values = [float(model({variable.name: columns[variable.name][i] for variable in variables})) for i in range(samples)]
    ordered = sorted(values)
    def q(p): return ordered[round(p*(samples-1))]
    return {'samples':samples,'seed':seed,'method':'latin_hypercube','mean':mean(values),'std':pstdev(values),'min':ordered[0],'p05':q(.05),'p50':q(.5),'p95':q(.95),'max':ordered[-1]}
