#!/usr/bin/env python3

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

import argparse,csv
from aeroframe_dt.digital_thread import EvidenceGraph
p=argparse.ArgumentParser(); p.add_argument('csv'); p.add_argument('database'); a=p.parse_args(); g=EvidenceGraph(a.database)
with open(a.csv,newline='') as f:
    for r in csv.DictReader(f):
        g.add_artifact(r['id'],r['kind'],r['revision'],r.get('uri') or None,r.get('sha256') or None)
with open(a.csv,newline='') as f:
    for r in csv.DictReader(f):
        if r.get('parent_id'): g.link(r['parent_id'],r['id'],r.get('relation') or 'depends_on')
g.close()
