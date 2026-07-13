"""Compact, defensive NASTRAN F06 text parsing helpers."""
from __future__ import annotations
import re
_FLOAT=r'[-+]?\d*\.?\d+(?:[EeDd][-+]?\d+)?'
def _f(s): return float(s.replace('D','E'))
def parse_grid_point_force_balance(text:str)->list[dict]:
    rows=[]
    pat=re.compile(rf'^\s*(\d+)\s+([A-Z0-9_-]+)\s+({_FLOAT})\s+({_FLOAT})\s+({_FLOAT})\s+({_FLOAT})\s+({_FLOAT})\s+({_FLOAT})\s*$',re.M)
    for m in pat.finditer(text):
        rows.append({'grid':int(m.group(1)),'source':m.group(2),'fx':_f(m.group(3)),'fy':_f(m.group(4)),'fz':_f(m.group(5)),'mx':_f(m.group(6)),'my':_f(m.group(7)),'mz':_f(m.group(8))})
    return rows
def resultant(rows:list[dict])->dict:
    return {k:sum(r[k] for r in rows) for k in ('fx','fy','fz','mx','my','mz')}


def parse_real_eigenvalues(text: str) -> list[dict]:
    """Parse compact REAL EIGENVALUES table rows from F06 text.

    Supports rows containing mode, extraction order, eigenvalue, radians,
    cycles, and generalized mass/stiffness. The parser ignores unrelated rows.
    """
    rows: list[dict] = []
    pattern = re.compile(
        rf"^\s*(\d+)\s+(\d+)\s+({_FLOAT})\s+({_FLOAT})\s+({_FLOAT})\s+({_FLOAT})\s+({_FLOAT})\s*$",
        re.M,
    )
    in_table = False
    for line in text.splitlines():
        upper = line.upper()
        if "REAL EIGENVALUES" in upper:
            in_table = True
            continue
        if in_table and ("PAGE" in upper or "EIGENVECTOR" in upper):
            in_table = False
        if not in_table:
            continue
        match = pattern.match(line)
        if match:
            rows.append({
                "mode": int(match.group(1)), "extraction_order": int(match.group(2)),
                "eigenvalue": _f(match.group(3)), "radians": _f(match.group(4)),
                "cycles_Hz": _f(match.group(5)), "generalized_mass": _f(match.group(6)),
                "generalized_stiffness": _f(match.group(7)),
            })
    return rows


def parse_buckling_eigenvalues(text: str) -> list[dict]:
    """Parse buckling eigenvalue rows from common F06 table excerpts."""
    rows: list[dict] = []
    in_table = False
    pattern = re.compile(rf"^\s*(\d+)\s+(?:\d+\s+)?({_FLOAT})\s*$")
    for line in text.splitlines():
        upper = line.upper()
        if "BUCKLING" in upper and "EIGENVALUE" in upper:
            in_table = True
            continue
        if in_table and "PAGE" in upper:
            in_table = False
        if not in_table:
            continue
        match = pattern.match(line)
        if match:
            rows.append({"mode": int(match.group(1)), "load_factor": _f(match.group(2))})
    return rows


def parse_grid_displacements(text: str) -> list[dict]:
    """Parse standard six-component displacement rows inside a displacement table."""
    rows: list[dict] = []
    pattern = re.compile(
        rf"^\s*(\d+)\s+([GS])\s+({_FLOAT})\s+({_FLOAT})\s+({_FLOAT})\s+({_FLOAT})\s+({_FLOAT})\s+({_FLOAT})\s*$"
    )
    in_table = False
    for line in text.splitlines():
        upper = line.upper()
        if "D I S P L A C E M E N T" in upper or "DISPLACEMENT VECTOR" in upper:
            in_table = True
            continue
        if in_table and "PAGE" in upper:
            in_table = False
        if not in_table:
            continue
        match = pattern.match(line)
        if match:
            rows.append({
                "grid": int(match.group(1)), "type": match.group(2),
                "t1": _f(match.group(3)), "t2": _f(match.group(4)), "t3": _f(match.group(5)),
                "r1": _f(match.group(6)), "r2": _f(match.group(7)), "r3": _f(match.group(8)),
            })
    return rows
