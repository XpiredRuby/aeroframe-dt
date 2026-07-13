"""Unified command-line interface for AeroFrame-DT software workflows."""
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
import sys

from .afgrow import AFGROWCase, parse_growth_csv, write_neutral_package
from .batch import ansys_batch_run, nastran_batch_run, write_run_contract
from .cad_automation import CADParameter, freecad_parameter_macro, solidworks_global_variables_macro
from .convergence import ConvergencePoint, assess_convergence
from .digital_exchange import qif_style_inspection_xml, validate_qif_sidecar
from .inspection import Nonconformance, capability, crossed_gage_rr
from .load_cases import load_cases_from_json, write_resultant_csv
from .release import audit_repository, create_source_release
from .reporting import ReportSection, engineering_report, write_report
from .solver_decks import BeamBenchmark, PlateBenchmark, ansys_cantilever_apdl, ansys_plate_apdl, nastran_cantilever_bdf, write_text
from .solver_results import read_long_csv
from .substantiation import run_substantiation_file


def _json(path: str | Path):
    return json.loads(Path(path).read_text(encoding="utf-8"))



def cmd_substantiation(args: argparse.Namespace) -> int:
    result = run_substantiation_file(args.input, args.output)
    print(json.dumps(result.to_dict(), indent=2))
    return 0 if result.status != "FAIL" else 2


def cmd_load_envelope(args: argparse.Namespace) -> int:
    cases = load_cases_from_json(args.input)
    write_resultant_csv(cases.values(), args.output)
    print(f"wrote {len(cases)} load cases to {args.output}")
    return 0


def cmd_decks(args: argparse.Namespace) -> int:
    data = _json(args.input)
    out = Path(args.output); out.mkdir(parents=True, exist_ok=True)
    beam = BeamBenchmark(**data["beam"])
    plate = PlateBenchmark(**data["plate"])
    write_text(out / "cantilever_nastran.bdf", nastran_cantilever_bdf(beam))
    write_text(out / "cantilever_ansys.dat", ansys_cantilever_apdl(beam))
    write_text(out / "plate_ansys.dat", ansys_plate_apdl(plate))
    print(f"wrote solver decks to {out}")
    return 0


def cmd_convergence(args: argparse.Namespace) -> int:
    points: list[ConvergencePoint] = []
    with Path(args.input).open(newline="", encoding="utf-8") as stream:
        for row in csv.DictReader(stream):
            points.append(ConvergencePoint(float(row["characteristic_size"]), float(row["value"]), int(row["dof"]) if row.get("dof") else None, row.get("run_id", "")))
    result = assess_convergence(points, args.tolerance)
    Path(args.output).write_text(json.dumps(result.to_dict(), indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result.to_dict(), indent=2))
    return 0 if result.passed else 2


def cmd_cad_macro(args: argparse.Namespace) -> int:
    data = _json(args.input)
    parameters = [CADParameter(**item) for item in data["parameters"]]
    text = solidworks_global_variables_macro(parameters) if args.format == "solidworks" else freecad_parameter_macro(parameters)
    Path(args.output).write_text(text, encoding="utf-8")
    print(f"wrote {args.format} macro to {args.output}")
    return 0


def cmd_inspection(args: argparse.Namespace) -> int:
    data = _json(args.input)
    cap = capability(data["capability"]["values"], data["capability"]["lower_limit"], data["capability"]["upper_limit"])
    rr = crossed_gage_rr(data["gage_rr"])
    ncrs = [Nonconformance(**row) for row in data["nonconformances"]]
    for row in ncrs: row.validate()
    payload = {"capability": cap.to_dict(), "gage_rr": rr.to_dict(), "nonconformances": [row.__dict__ for row in ncrs]}
    Path(args.output).write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"wrote inspection analysis to {args.output}")
    return 0


def cmd_qif_sidecar(args: argparse.Namespace) -> int:
    data = _json(args.input)
    xml = qif_style_inspection_xml(data["part_id"], data["revision"], data["characteristics"])
    issues = validate_qif_sidecar(xml)
    if issues:
        print("\n".join(issues), file=sys.stderr); return 2
    Path(args.output).write_text(xml, encoding="utf-8")
    print(f"wrote open QIF-style sidecar to {args.output}")
    return 0


def cmd_afgrow_package(args: argparse.Namespace) -> int:
    data = _json(args.input)
    case = AFGROWCase(**data["case"])
    write_neutral_package(case, data["spectrum"], args.output)
    print(f"wrote AFGROW neutral package to {args.output}")
    return 0


def cmd_batch_contract(args: argparse.Namespace) -> int:
    if args.solver == "ansys":
        run = ansys_batch_run(args.run_id, args.executable, args.input, args.output_file, args.working_directory, args.processors)
    else:
        run = nastran_batch_run(args.run_id, args.executable, args.input, args.working_directory, args.scratch)
    write_run_contract(run, args.contract)
    print(run.shell_preview())
    return 0


def cmd_audit(args: argparse.Namespace) -> int:
    issues = audit_repository(args.root)
    for issue in issues: print(f"{issue.severity}: {issue.path}: {issue.message}")
    errors = [item for item in issues if item.severity == "ERROR"]
    print(f"release audit: {len(errors)} errors, {len(issues)-len(errors)} warnings")
    return 2 if errors else 0


def cmd_release(args: argparse.Namespace) -> int:
    manifest = create_source_release(args.root, args.output)
    print(json.dumps(manifest, indent=2))
    return 0


def cmd_report(args: argparse.Namespace) -> int:
    data = _json(args.input)
    sections = [ReportSection(item["title"], item["body_markdown"]) for item in data["sections"]]
    text = engineering_report(data["title"], data["document_id"], data["revision"], sections, data["limitations"], data["evidence"])
    write_report(text, args.markdown, args.html, data["title"])
    print(f"wrote report to {args.markdown} and {args.html}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="aeroframe-dt")
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("substantiation"); p.add_argument("input"); p.add_argument("output"); p.set_defaults(func=cmd_substantiation)
    p = sub.add_parser("load-envelope"); p.add_argument("input"); p.add_argument("output"); p.set_defaults(func=cmd_load_envelope)
    p = sub.add_parser("generate-decks"); p.add_argument("input"); p.add_argument("output"); p.set_defaults(func=cmd_decks)
    p = sub.add_parser("convergence"); p.add_argument("input"); p.add_argument("output"); p.add_argument("--tolerance", type=float, default=0.02); p.set_defaults(func=cmd_convergence)
    p = sub.add_parser("cad-macro"); p.add_argument("input"); p.add_argument("output"); p.add_argument("--format", choices=("solidworks", "freecad"), default="solidworks"); p.set_defaults(func=cmd_cad_macro)
    p = sub.add_parser("inspection"); p.add_argument("input"); p.add_argument("output"); p.set_defaults(func=cmd_inspection)
    p = sub.add_parser("qif-sidecar"); p.add_argument("input"); p.add_argument("output"); p.set_defaults(func=cmd_qif_sidecar)
    p = sub.add_parser("afgrow-package"); p.add_argument("input"); p.add_argument("output"); p.set_defaults(func=cmd_afgrow_package)
    p = sub.add_parser("batch-contract"); p.add_argument("solver", choices=("ansys", "nastran")); p.add_argument("run_id"); p.add_argument("executable"); p.add_argument("input"); p.add_argument("working_directory"); p.add_argument("contract"); p.add_argument("--output-file", default="solver.out"); p.add_argument("--processors", type=int, default=2); p.add_argument("--scratch"); p.set_defaults(func=cmd_batch_contract)
    p = sub.add_parser("audit"); p.add_argument("root", nargs="?", default="."); p.set_defaults(func=cmd_audit)
    p = sub.add_parser("release"); p.add_argument("root"); p.add_argument("output"); p.set_defaults(func=cmd_release)
    p = sub.add_parser("report"); p.add_argument("input"); p.add_argument("markdown"); p.add_argument("html"); p.set_defaults(func=cmd_report)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    return int(args.func(args))


if __name__ == "__main__":
    raise SystemExit(main())
