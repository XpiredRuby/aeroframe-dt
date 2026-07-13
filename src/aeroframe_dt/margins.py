"""Traceable margin-table construction and governing-check selection."""
from __future__ import annotations
import csv, json
from pathlib import Path
from typing import Iterable

def build_margin_rows(checks: Iterable[dict], context: dict) -> list[dict]:
    required=['load_case_id','geometry_revision','source_id','extraction_rule_id','allowable_source_id','safety_factor_source_id']
    missing=[k for k in required if not context.get(k)]
    if missing: raise ValueError(f'missing traceability context: {missing}')
    rows=[]
    for check in checks:
        row={**context,**check}
        row['status']='UNASSESSED' if check.get('margin') is None else ('PASS' if check['margin']>=0 else 'FAIL')
        rows.append(row)
    return rows

def governing_row(rows: Iterable[dict]) -> dict|None:
    assessed=[r for r in rows if r.get('margin') is not None]
    return min(assessed,key=lambda r:r['margin']) if assessed else None

def write_margin_csv(rows: list[dict], path: str|Path) -> None:
    if not rows: raise ValueError('rows cannot be empty')
    path=Path(path); path.parent.mkdir(parents=True,exist_ok=True)
    fields=list(dict.fromkeys(k for row in rows for k in row))
    with path.open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields); w.writeheader(); w.writerows(rows)

def write_manifest(rows: list[dict], path: str|Path) -> None:
    gov=governing_row(rows)
    payload={'schema_version':'1.0','row_count':len(rows),'governing_check':gov,'rows':rows}
    Path(path).write_text(json.dumps(payload,indent=2,sort_keys=True))
