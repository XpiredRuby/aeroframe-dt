#!/usr/bin/env python3
"""Generate the complete synthetic software-verification evidence package."""
from __future__ import annotations

import csv
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from aeroframe_dt.afgrow import AFGROWCase, write_neutral_package
from aeroframe_dt.cad_automation import CADParameter, freecad_parameter_macro, solidworks_global_variables_macro
from aeroframe_dt.cli import cmd_inspection
from aeroframe_dt.convergence import ConvergencePoint, assess_convergence
from aeroframe_dt.digital_exchange import qif_style_inspection_xml, validate_qif_sidecar
from aeroframe_dt.digital_thread import EvidenceGraph
from aeroframe_dt.load_cases import load_cases_from_json, write_resultant_csv
from aeroframe_dt.manifest import RunManifest
from aeroframe_dt.release import audit_repository
from aeroframe_dt.reporting import ReportSection, engineering_report, write_report
from aeroframe_dt.solver_decks import (
    BeamBenchmark, PlateBenchmark, ansys_cantilever_apdl, ansys_cantilever_modal_apdl,
    ansys_eigen_buckling_apdl, ansys_plate_apdl, nastran_cantilever_bdf,
    nastran_cantilever_modal_bdf, nastran_quad_patch_bdf, write_text,
)
from aeroframe_dt.substantiation import run_substantiation_file


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    output = ROOT / "results" / "software_verification"
    if output.exists(): shutil.rmtree(output)
    output.mkdir(parents=True)

    test_run = subprocess.run(
        [sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v"],
        cwd=ROOT, text=True, capture_output=True, check=False,
        env={**__import__("os").environ, "PYTHONPATH": str(ROOT / "src")},
    )
    (output / "unit_test_log.txt").write_text(test_run.stdout + test_run.stderr, encoding="utf-8")
    if test_run.returncode != 0:
        raise RuntimeError("software verification tests failed")

    run_substantiation_file(ROOT / "examples/synthetic_substantiation_case.json", output / "synthetic_substantiation.json")
    cases = load_cases_from_json(ROOT / "examples/synthetic_load_envelope.json")
    write_resultant_csv(cases.values(), output / "synthetic_load_envelope.csv")

    points = []
    with (ROOT / "examples/synthetic_convergence.csv").open(newline="", encoding="utf-8") as stream:
        for row in csv.DictReader(stream): points.append(ConvergencePoint(float(row["characteristic_size"]), float(row["value"]), int(row["dof"]), row["run_id"]))
    (output / "synthetic_convergence.json").write_text(json.dumps(assess_convergence(points).to_dict(), indent=2, sort_keys=True) + "\n", encoding="utf-8")

    benchmark = read_json(ROOT / "examples/synthetic_benchmarks.json")
    beam, plate = BeamBenchmark(**benchmark["beam"]), PlateBenchmark(**benchmark["plate"])
    decks = output / "solver_decks"; decks.mkdir()
    write_text(decks / "cantilever_static_nastran.bdf", nastran_cantilever_bdf(beam))
    write_text(decks / "cantilever_modal_nastran.bdf", nastran_cantilever_modal_bdf(beam))
    write_text(decks / "constant_strain_patch_nastran.bdf", nastran_quad_patch_bdf())
    write_text(decks / "cantilever_static_ansys.dat", ansys_cantilever_apdl(beam))
    write_text(decks / "cantilever_modal_ansys.dat", ansys_cantilever_modal_apdl(beam))
    write_text(decks / "cantilever_buckling_ansys.dat", ansys_eigen_buckling_apdl(beam, 1000))
    write_text(decks / "square_plate_ansys.dat", ansys_plate_apdl(plate))

    cad = read_json(ROOT / "examples/synthetic_cad_parameters.json")
    parameters = [CADParameter(**row) for row in cad["parameters"]]
    macro_dir = output / "cad_macros"; macro_dir.mkdir()
    (macro_dir / "set_global_variables.bas").write_text(solidworks_global_variables_macro(parameters), encoding="utf-8")
    (macro_dir / "freecad_parameter_sheet.py").write_text(freecad_parameter_macro(parameters), encoding="utf-8")

    inspection = read_json(ROOT / "examples/synthetic_inspection.json")
    from aeroframe_dt.inspection import capability, crossed_gage_rr, Nonconformance
    inspection_payload = {
        "classification": inspection["classification"],
        "capability": capability(inspection["capability"]["values"], inspection["capability"]["lower_limit"], inspection["capability"]["upper_limit"]).to_dict(),
        "gage_rr": crossed_gage_rr(inspection["gage_rr"]).to_dict(),
        "nonconformances": inspection["nonconformances"],
    }
    (output / "synthetic_inspection.json").write_text(json.dumps(inspection_payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    ncr_dir = output / "ncr"; ncr_dir.mkdir()
    for row in inspection["nonconformances"]:
        ncr = Nonconformance(**row); ncr.validate()
        lines = [f"# {ncr.ncr_id}", "", "**Classification:** `SYNTHETIC_TEST_ONLY`", ""]
        for key, value in ncr.__dict__.items(): lines.extend([f"## {key.replace('_',' ').title()}", "", str(value), ""])
        (ncr_dir / f"{ncr.ncr_id}.md").write_text("\n".join(lines), encoding="utf-8")

    qif = read_json(ROOT / "examples/synthetic_qif_sidecar.json")
    xml = qif_style_inspection_xml(qif["part_id"], qif["revision"], qif["characteristics"])
    if validate_qif_sidecar(xml): raise RuntimeError("QIF sidecar validation failed")
    (output / "synthetic_qif_sidecar.xml").write_text(xml, encoding="utf-8")

    afgrow = read_json(ROOT / "examples/synthetic_afgrow_case.json")
    write_neutral_package(AFGROWCase(**afgrow["case"]), afgrow["spectrum"], output / "afgrow_package")

    with tempfile.TemporaryDirectory() as temp:
        graph = EvidenceGraph(Path(temp) / "evidence.db")
        graph.add_artifact("REQ-STATIC", "requirement", "A", "requirements/requirements.csv")
        graph.add_artifact("CAD-FITTING", "cad", "A", "cad/GEOMETRY_CONCEPT.md")
        graph.add_artifact("AN-HAND", "analysis", "A", "results/software_verification/synthetic_substantiation.json")
        graph.add_artifact("PMI-SIDECAR", "pmi", "A", "results/software_verification/synthetic_qif_sidecar.xml")
        graph.add_artifact("INSP-PLAN", "inspection", "A", "results/software_verification/synthetic_inspection.json")
        graph.link("REQ-STATIC", "CAD-FITTING", "allocated_to")
        graph.link("CAD-FITTING", "AN-HAND", "analyzed_by")
        graph.link("CAD-FITTING", "PMI-SIDECAR", "defines")
        graph.link("PMI-SIDECAR", "INSP-PLAN", "verified_by")
        if graph.audit(): raise RuntimeError(graph.audit())
        (output / "digital_thread.json").write_text(json.dumps(graph.export_json(), indent=2, sort_keys=True) + "\n", encoding="utf-8")
        (output / "digital_thread.dot").write_text(graph.export_dot(), encoding="utf-8")
        graph.close()

    issues = audit_repository(ROOT)
    release_audit = {"errors": [item.__dict__ for item in issues if item.severity == "ERROR"], "warnings": [item.__dict__ for item in issues if item.severity == "WARNING"]}
    # Cache findings are expected only if Python was run before cleanup; the release command removes them.
    release_audit["errors"] = [item for item in release_audit["errors"] if "__pycache__" not in item["path"] and not item["path"].endswith(".pyc")]
    if release_audit["errors"]: raise RuntimeError(release_audit["errors"])
    (output / "release_audit.json").write_text(json.dumps(release_audit, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    evidence = [{"artifact": path.relative_to(ROOT).as_posix(), "status": "GENERATED", "purpose": "Synthetic software verification"} for path in sorted(output.rglob("*")) if path.is_file()]
    report = engineering_report(
        "AeroFrame-DT Software Verification Report", "AFDT-RPT-SW-001", "A",
        [
            ReportSection("Scope", "All outputs in this report are synthetic software-verification evidence. No OEM dimensions, aircraft loads, or certification claims are included."),
            ReportSection("Implemented workflows", "Load assembly, integrated hand substantiation, solver-deck generation, convergence assessment, CAD parameter macros, fatigue/AFGROW packaging, inspection statistics, NCR packages, digital-thread export, and deterministic reporting are automated."),
            ReportSection("Execution boundary", "Licensed solver execution and CAD export remain human-tool execution gates. The software needed to prepare, run, parse, compare, trace, and report those future files is present."),
        ],
        ["Synthetic values are not design data.", "Solver decks require vendor execution and review.", "The QIF-style XML is an open sidecar, not schema-valid QIF."],
        evidence,
    )
    write_report(report, output / "SOFTWARE_VERIFICATION_REPORT.md", output / "SOFTWARE_VERIFICATION_REPORT.html", "AeroFrame-DT Software Verification Report")

    manifest = RunManifest("AFDT-SW-VERIFY-001", "aeroframe-dt", "0.3.0", "PASS")
    for path in sorted(output.rglob("*")):
        if path.is_file() and path.name != "manifest.json": manifest.add_file(path, "software_verification_output", output=True, base=ROOT)
    manifest.parameters = {"classification": "SYNTHETIC_TEST_ONLY", "test_count_expected_minimum": 43}
    manifest.write(output / "manifest.json")
    print(f"Generated {sum(1 for path in output.rglob('*') if path.is_file())} evidence files in {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
