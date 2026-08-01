#!/usr/bin/env python3
"""F14 — build the AF-DT-1000 evidence graph and run impact analysis on it.

Unlike ``tools/build_evidence_graph.py``, which loads whatever CSV it is handed, this
script populates the graph from the **actual repository**: requirement IDs are read from
`requirements/requirements.csv`, PMI characteristics from the Rev D inspection plan, and
every artifact backed by a file carries the **real SHA-256 of that file at build time**.
A stale hash is therefore detectable, not merely asserted.

Two impact analyses are run and recorded:

  A. HISTORICAL REPLAY — the load basis is registered at revision B and then revised to C
     with the real rationale (the lug-axis mapping error). The descendant set the graph
     marks STALE is compared against the rework that actually happened.

  B. FORWARD QUERY — what would go stale if the pending elastic-plastic contact run
     changes t_eff/t.

Outputs:
    digital_thread/thread_AF-DT-1000_revD.json
    digital_thread/thread_AF-DT-1000_revD.dot
    digital_thread/impact_analysis.json

Run:  python tools/build_f14_thread.py
"""

from __future__ import annotations

import csv
import hashlib
import json
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from aeroframe_dt.digital_thread import EvidenceGraph  # noqa: E402

OUT_DIR = ROOT / "digital_thread"


def sha256_of(relative: str) -> str | None:
    path = ROOT / relative
    if not path.is_file():
        return None
    return hashlib.sha256(path.read_bytes()).hexdigest()


# --- artifact declarations ----------------------------------------------------
# (id, kind, revision, uri, metadata)
SOURCES = [
    ("SRC-MILHDBK5J-3.7.6.0b3", "source", "5J",
     None, {"citation": "MIL-HDBK-5J 31 Jan 2003 Table 3.7.6.0(b3) p.3-373",
            "scope": "7075-T7351 plate allowables, 2.001-2.500 in band", "class": "REAL"}),
    ("SRC-MILHDBK5J-3.1.2.1.6", "source", "5J",
     None, {"citation": "MIL-HDBK-5J Table 3.1.2.1.6",
            "scope": "K_Ic, information only", "class": "REAL"}),
    ("SRC-MELCON-HOBLIT", "source", "TM-X-73305",
     None, {"citation": "NASA TM-X-73305 Astronautics Structures Manual Vol I Sec B2",
            "scope": "lug analysis method", "class": "REAL"}),
    ("SRC-EKVALL-1986", "source", "1986",
     None, {"citation": "Ekvall, J. Aircraft 23(5) 1986 pp.438-443",
            "scope": "243 lug tests, correlation band", "class": "REAL"}),
    ("SRC-FAR-25", "source", "current",
     None, {"citation": "14 CFR 25.561 emergency landing, 25.625 fitting factor",
            "class": "REAL"}),
]

# The load basis is ONE artifact that carries a revision, not one node per revision.
# That is what makes revise_artifact() meaningful: revising it is the same operation the
# project actually performed when the axis-mapping error was found.
LOAD_URI = {"A": "loads/LOAD_BASIS_AF-DT-1000_revA.md",
            "B": "loads/LOAD_BASIS_AF-DT-1000_revB.md",
            "C": "loads/LOAD_BASIS_AF-DT-1000_revC.md"}

LOAD_METADATA = {
    "B": {"class": "SYNTHETIC_TEST_ONLY", "state": "superseded",
          "angle_deg": 30.96,
          "defect": "angle measured from aircraft X, not the lug axis; non-conservative"},
    "C": {"class": "SYNTHETIC_TEST_ONLY", "state": "released",
          "resultant_N": 617776, "angle_deg_off_lug_axis": 59.04, "level": "LIMIT"},
}

GEOMETRY = [
    ("GEO-AF-DT-1000", "geometry", "D", "docs/DECISIONS_AF-DT-1000_revD.md",
     {"state": "frozen", "t_lug_in": 2.500, "e_over_D": 1.25, "W_over_D": 2.00,
      "t_over_D": 1.25, "mass_kg": 7.65}),
    ("CAD-BUILD-REVD", "cad_script", "D", "cad/build_revD.py", {"units": "inch valued"}),
    ("CAD-BUILD-REVD-MM", "cad_script", "D", "cad/build_revD_to_mm.py",
     {"units": "mm", "note": "this is the export used for FE"}),
    ("CAD-BUILD-F7", "cad_script", "D", "cad/build_f7.py", {"units": "mm"}),
    ("CAD-PARAMS", "parameter_set", "D", "cad/PARAMETER_SCHEMA.csv", {}),
]

ANALYSES = [
    ("ANL-F5-FE", "analysis", "D", "docs/F5_FE_REVD_LINEAR_ELASTIC.md",
     {"type": "linear elastic FE", "nodes": 152951, "equilibrium_error_pct": 0.006}),
    ("ANL-F6-PIN", "analysis", "D", "docs/F6_PIN_BENDING_THICK_LUG.md",
     {"pin_bending_MPa": 780}),
    ("ANL-F7-CONTACT", "analysis", "D", "docs/F7_CONTACT_THICK_LUG.md",
     {"t_eff_over_t": 0.681, "basis": "elastic only", "mesh_points": 3,
      "note": "makes MS a lower bound"}),
    ("ANL-F9-DT", "analysis", "D", "docs/F9_DAMAGE_TOLERANCE.md", {"a_c_mm": 3.07}),
    ("ANL-F9B-SPECTRUM", "analysis", "D", "docs/F9b_SPECTRUM_AND_INTERVAL.md",
     {"class": "SYNTHETIC_SPECTRUM", "interval_flights": 4500, "ndi_threshold_mm": 1.27}),
    ("ANL-F10-DYNAMICS", "analysis", "D", "docs/F10_DYNAMICS_BUCKLING.md",
     {"f1_Hz": 2133, "state": "analytical only"}),
    ("ANL-F11-OPT", "analysis", "D", "docs/F11_OPTIMIZATION.md", {}),
    ("ANL-F12-CORR", "analysis", "D", "docs/F12_CORRELATION_AF-DT-1000.md",
     {"tests": 243, "ratio_range": "0.85-1.19"}),
    ("ANL-F13-STACK", "analysis", "D", "docs/F13_MANUFACTURING_INSPECTION.md",
     {"ms_worst_case": 0.0568, "consumption_pct": 27.6}),
]

RELEASED = [
    ("MARGIN-AF-DT-1000", "margin", "D", "docs/MARGIN_SUMMARY.md",
     {"MS": 0.078, "basis": "A-basis, thick-lug corrected, fitting factor 1.15",
      "authoritative": True}),
    ("PMI-AF-DT-1000", "pmi_definition", "D", "docs/PMI_GDT_DEFINITION.md", {}),
    ("INSP-PLAN-AF-DT-1000", "inspection_plan", "D",
     "inspection_quality/inspection_plan_AF-DT-1000_revD.csv", {}),
    ("NCR-F15-001", "nonconformance", "D",
     "docs/F15_NONCONFORMANCE_RCCA_AF-DT-1000.md",
     {"deviation": "edge distance 2.500 -> 1.900 in", "MS_after": -0.370,
      "disposition": "REWORK"}),
    ("RPT-STRESS-AF-DT-1000", "report", "D", "docs/STRESS_REPORT_AF-DT-1000.md", {}),
]

LINKS = [
    # sources into the things that consume them
    ("SRC-FAR-25", "LOAD-AF-DT-1000", "governs"),
    ("SRC-MELCON-HOBLIT", "MARGIN-AF-DT-1000", "method_source"),
    ("SRC-MILHDBK5J-3.7.6.0b3", "MARGIN-AF-DT-1000", "allowable_source"),
    ("SRC-MILHDBK5J-3.1.2.1.6", "ANL-F9-DT", "allowable_source"),
    ("SRC-EKVALL-1986", "ANL-F12-CORR", "correlation_source"),
    # geometry chain
    ("CAD-PARAMS", "CAD-BUILD-REVD", "parameterises"),
    ("CAD-BUILD-REVD", "CAD-BUILD-REVD-MM", "rescaled_by"),
    ("CAD-BUILD-REVD-MM", "GEO-AF-DT-1000", "produces"),
    ("CAD-BUILD-F7", "ANL-F7-CONTACT", "produces_model_for"),
    # load and geometry into analysis
    ("LOAD-AF-DT-1000", "ANL-F5-FE", "load_input"),
    ("LOAD-AF-DT-1000", "ANL-F6-PIN", "load_input"),
    ("LOAD-AF-DT-1000", "ANL-F7-CONTACT", "load_input"),
    ("LOAD-AF-DT-1000", "ANL-F9-DT", "load_input"),
    ("LOAD-AF-DT-1000", "ANL-F10-DYNAMICS", "load_input"),
    ("LOAD-AF-DT-1000", "ANL-F11-OPT", "load_input"),
    ("LOAD-AF-DT-1000", "MARGIN-AF-DT-1000", "load_input"),
    ("GEO-AF-DT-1000", "ANL-F5-FE", "geometry_input"),
    ("GEO-AF-DT-1000", "ANL-F6-PIN", "geometry_input"),
    ("GEO-AF-DT-1000", "ANL-F7-CONTACT", "geometry_input"),
    ("GEO-AF-DT-1000", "ANL-F9-DT", "geometry_input"),
    ("GEO-AF-DT-1000", "ANL-F10-DYNAMICS", "geometry_input"),
    ("GEO-AF-DT-1000", "ANL-F11-OPT", "geometry_input"),
    ("GEO-AF-DT-1000", "PMI-AF-DT-1000", "geometry_input"),
    # analysis into the released margin
    ("ANL-F5-FE", "MARGIN-AF-DT-1000", "validates_assumptions_of"),
    ("ANL-F7-CONTACT", "MARGIN-AF-DT-1000", "corrects"),
    ("ANL-F12-CORR", "MARGIN-AF-DT-1000", "bounds_scatter_of"),
    ("ANL-F9-DT", "ANL-F9B-SPECTRUM", "feeds"),
    # margin into everything downstream of it
    ("MARGIN-AF-DT-1000", "PMI-AF-DT-1000", "sizes_tolerances_of"),
    ("MARGIN-AF-DT-1000", "ANL-F13-STACK", "baseline_for"),
    ("MARGIN-AF-DT-1000", "NCR-F15-001", "assesses"),
    ("MARGIN-AF-DT-1000", "RPT-STRESS-AF-DT-1000", "released_in"),
    ("PMI-AF-DT-1000", "INSP-PLAN-AF-DT-1000", "defines"),
    ("PMI-AF-DT-1000", "ANL-F13-STACK", "tolerances_stacked_by"),
    ("ANL-F9B-SPECTRUM", "INSP-PLAN-AF-DT-1000", "sets_ndi_threshold_of"),
    ("INSP-PLAN-AF-DT-1000", "NCR-F15-001", "detects"),
    ("ANL-F13-STACK", "RPT-STRESS-AF-DT-1000", "reported_in"),
    ("ANL-F6-PIN", "RPT-STRESS-AF-DT-1000", "reported_in"),
    ("ANL-F10-DYNAMICS", "RPT-STRESS-AF-DT-1000", "reported_in"),
    ("ANL-F11-OPT", "RPT-STRESS-AF-DT-1000", "reported_in"),
    ("ANL-F9B-SPECTRUM", "RPT-STRESS-AF-DT-1000", "reported_in"),
]


def read_requirements() -> list[tuple]:
    rows = []
    with (ROOT / "requirements" / "requirements.csv").open(newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            rows.append((row["requirement_id"], "requirement", "1",
                         row["evidence_path"] or None,
                         {"category": row["category"], "status": row["status"],
                          "method": row["verification_method"]}))
    return rows


def read_characteristics() -> list[tuple]:
    rows = []
    path = ROOT / "inspection_quality" / "inspection_plan_AF-DT-1000_revD.csv"
    with path.open(newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            rows.append((row["characteristic_id"], "pmi_characteristic", "D", None,
                         {"feature": row["feature_id"], "method": row["method"],
                          "upper_limit": row["upper_limit"], "units": row["units"],
                          "criticality": row["criticality"]}))
    return rows


def load_node(revision: str) -> tuple:
    return ("LOAD-AF-DT-1000", "load_case", revision, LOAD_URI[revision],
            LOAD_METADATA[revision])


def populate(graph: EvidenceGraph, load_revision: str) -> None:
    """Register every artifact. ``load_revision`` selects which load basis is current."""
    declared = (SOURCES + [load_node(load_revision)] + GEOMETRY + ANALYSES + RELEASED
                + read_requirements() + read_characteristics())
    for artifact_id, kind, revision, uri, metadata in declared:
        graph.add_artifact(artifact_id, kind, revision, uri,
                           sha256_of(uri) if uri else None, metadata)

    for parent, child, relation in LINKS:
        graph.link(parent, child, relation)

    # requirement -> evidence, taken straight from requirements.csv.
    # The load basis is matched on any of its revisions so the replay keeps its links.
    evidence_map = {node[3]: node[0]
                    for node in (SOURCES + GEOMETRY + ANALYSES + RELEASED) if node[3]}
    for uri in LOAD_URI.values():
        evidence_map[uri] = "LOAD-AF-DT-1000"
    for requirement_id, _, _, evidence, _ in read_requirements():
        target = evidence_map.get(evidence)
        if target:
            graph.link(requirement_id, target, "verified_by")
    # PMI definition -> its characteristics
    for characteristic_id, *_ in read_characteristics():
        graph.link("PMI-AF-DT-1000", characteristic_id, "specifies")
        graph.link(characteristic_id, "INSP-PLAN-AF-DT-1000", "inspected_by")


def new_graph(load_revision: str = "C") -> tuple[EvidenceGraph, Path]:
    handle = Path(tempfile.mkdtemp()) / "thread.sqlite"
    graph = EvidenceGraph(handle)
    populate(graph, load_revision)
    return graph, handle


def historical_replay() -> dict:
    """Register the graph as it stood at load rev B, then apply the real correction."""
    graph, _ = new_graph(load_revision="B")
    stale = graph.revise_artifact(
        "LOAD-AF-DT-1000", "C",
        "lug-axis mapping error: 30.96 deg was measured from aircraft X, not the lug "
        "axis; the correct 59.04 deg is transverse-dominant and Ktru governs",
    )
    audit = graph.audit()
    graph.close()
    return {
        "trigger": "LOAD-AF-DT-1000 revised B -> C",
        "artifacts_marked_stale": sorted(stale),
        "count": len(stale),
        "audit_issues": audit,
    }


def forward_query() -> dict:
    """What the pending elastic-plastic contact run would invalidate."""
    graph, _ = new_graph()
    stale = graph.revise_artifact(
        "ANL-F7-CONTACT", "E",
        "elastic-plastic contact run supersedes the elastic t_eff/t = 0.681 lower bound",
    )
    graph.close()
    return {
        "trigger": "ANL-F7-CONTACT revised D -> E (planned)",
        "artifacts_marked_stale": sorted(stale),
        "count": len(stale),
    }


def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    graph, _ = new_graph()
    export = graph.export_json()
    dot = graph.export_dot()
    audit = export["audit_issues"]

    unhashed = [a["id"] for a in export["artifacts"] if a["uri"] and not a["sha256"]]

    (OUT_DIR / "thread_AF-DT-1000_revD.json").write_text(
        json.dumps(export, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (OUT_DIR / "thread_AF-DT-1000_revD.dot").write_text(dot, encoding="utf-8")
    graph.close()

    impact = {
        "component": "AF-DT-1000",
        "geometry_revision": "D",
        "historical_replay": historical_replay(),
        "forward_query": forward_query(),
    }
    (OUT_DIR / "impact_analysis.json").write_text(
        json.dumps(impact, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    print(f"Artifacts: {len(export['artifacts'])}   Links: {len(export['links'])}")
    print(f"Audit issues: {len(audit)}")
    for issue in audit:
        print(f"  ERROR: {issue}")
    if unhashed:
        print(f"  WARNING: {len(unhashed)} artifacts declare a uri with no file present: "
              f"{', '.join(unhashed)}")
    print(f"Historical replay (load rev B -> C) marks "
          f"{impact['historical_replay']['count']} artifacts stale")
    print(f"Forward query (elastic-plastic F7) marks "
          f"{impact['forward_query']['count']} artifacts stale")
    print(f"Written: {OUT_DIR.relative_to(ROOT)}/")
    return 1 if audit or unhashed else 0


if __name__ == "__main__":
    raise SystemExit(main())
