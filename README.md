# AeroFrame-DT

Representative transport-aircraft forward pylon-to-wingbox attachment fitting substantiation and digital-thread program.

> **Claim boundary:** educational and portfolio-focused; non-OEM; non-certified. No example load, dimension, allowable, spectrum, or result may be represented as aircraft design data.

## Software status

The software side is complete to the boundary of external engineering inputs and licensed-tool execution. The repository contains tested implementations for:

- load provenance, free-body assembly, and two-station load sharing;
- classical lug, bearing, shear-out, pin, flange, fastener, prying, fitting-factor, and slip checks;
- integrated traceable margin generation;
- material and fastener trades;
- static, patch, plate, modal, buckling, and contact solver-deck preparation;
- solver batch contracts and compact result parsing;
- mesh convergence, solver comparison, stress linearization, and integrated contact resultants;
- fatigue, Miner damage, Paris crack growth, critical flaw size, and AFGROW packaging;
- Monte Carlo, Latin hypercube, DOE, Pareto, and robust optimization;
- blind public-data correlation records;
- SolidWorks/FreeCAD parameter macros;
- STEP AP242 inventory screening and QIF-style inspection linkage;
- capability, gage R&R, three synthetic NCR/RCCA packages;
- revision-aware SQLite/JSON/DOT digital thread;
- automated Markdown/HTML reports, evidence manifests, CI, and reproducible source releases.

See [`docs/SOFTWARE_COMPLETION_MATRIX.md`](docs/SOFTWARE_COMPLETION_MATRIX.md) for the exact boundary between implemented software and future CAD/solver/data execution.

## Quick verification

```bash
python -m pip install -e .
python -m unittest discover -s tests -v
python tools/check_traceability.py
python tools/generate_all_software_evidence.py
aeroframe-dt audit .
```

## Unified CLI

```bash
aeroframe-dt --help
aeroframe-dt substantiation examples/synthetic_substantiation_case.json result.json
aeroframe-dt generate-decks examples/synthetic_benchmarks.json generated_decks/
aeroframe-dt convergence examples/synthetic_convergence.csv convergence.json
aeroframe-dt cad-macro examples/synthetic_cad_parameters.json set_globals.bas
aeroframe-dt inspection examples/synthetic_inspection.json inspection.json
aeroframe-dt qif-sidecar examples/synthetic_qif_sidecar.json inspection.xml
aeroframe-dt afgrow-package examples/synthetic_afgrow_case.json afgrow_case/
aeroframe-dt report examples/synthetic_report.json report.md report.html
```

## Repository policy

Commit source, solver inputs, compact outputs, plots, reports, hashes, and manifests. Do not indiscriminately commit native solver databases or large binary result files. The release audit rejects common ANSYS/NASTRAN/OptiStruct database formats.

## Remaining execution gates

No physical hardware is needed to finish software. Future progress requires one or more of:

1. representative CAD geometry or the existing context CAD;
2. source-backed loads, material allowables, and fatigue data;
3. licensed SolidWorks/ANSYS/Altair/AFGROW execution;
4. returned solver/CAD/AP242/QIF artifacts;
5. an appropriate public metallic joint/lug dataset for correlation.

Follow [`docs/HUMAN_TOOL_EXECUTION_RUNBOOK.md`](docs/HUMAN_TOOL_EXECUTION_RUNBOOK.md) when those inputs are available.
