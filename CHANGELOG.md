# Changelog

## 0.4.0 — 2026-08-01

### Added
- **F13 manufacturing, inspection and quality package** (`docs/F13_MANUFACTURING_INSPECTION.md`):
  12-operation process plan with the structural reason for each step, ten measurable inspection
  characteristics tied to the PMI callouts, measurement-system analysis, and process capability.
- Machine-readable inspection plan `inspection_quality/inspection_plan_AF-DT-1000_revD.csv` and its
  validator `tools/run_f13_inspection_plan.py`, which also screens gauge resolution against the
  10:1 rule.
- **Worst-case tolerance stack onto the governing margin**, evaluated on the real Melcon-Hoblit
  interaction rather than a linearisation: `MS +0.0784 -> +0.0568`, consuming 27.6% of the margin.
  Tolerances would have to be 3.62x wider to reach zero.
- **F14 populated digital thread** (`docs/F14_DIGITAL_THREAD.md`): 53 artifacts, 68 links, zero
  audit issues, every file-backed artifact carrying its build-time SHA-256. Built by
  `tools/build_f14_thread.py` from the repository itself.
- Two recorded impact analyses: a historical replay of the load revision B to C axis-mapping
  correction, and a forward query on the pending elastic-plastic contact run.
- Verification rows AFDT-V-030 through AFDT-V-033.

### Changed
- `PMI_GDT_DEFINITION.md` limitation 2 closed — the statistical tolerance stack now exists. Bore
  position remains the dominant and least-certain term, and is now the binding limitation.
- README surfaces F13 and F14 and states the three remaining solver-dependent open items.
- Both `inspection_quality/` and `digital_thread/` READMEs now describe delivered work rather than
  plans.

### Verification
- `tools/check_traceability.py` passes: 18 requirements, 33 verification rows.
- Exact tolerance stack agrees with the independent linearised thickness sensitivity to 0.1%.
- Historical replay reproduces the 24-artifact rework blast radius previously established by hand;
  the single over-flag is identified and explained rather than suppressed.
- All measurement data in F13 sections 5 and 6 remains `SYNTHETIC_TEST_ONLY`.

## 0.3.0 — 2026-07-12

### Added
- Unified `aeroframe-dt` command-line interface.
- Load-envelope and integrated fitting-substantiation pipelines.
- Explicit unit conversions and source-gated material/fastener trades.
- Patch, cantilever, plate, modal, buckling, and contact deck generators.
- Solver batch contracts, extended F06 parsers, compact result records, and equilibrium validation.
- Structural extraction, mesh-convergence/GCI, solver comparison, and dynamics checks.
- AFGROW-neutral package and crack-growth result processing.
- Latin-hypercube uncertainty, DOE, Pareto, and robust optimization.
- Blind public-data correlation records and frozen-dataset hashing.
- SolidWorks and FreeCAD parameter macros.
- STEP AP242 inventory screen and QIF-style inspection XML.
- Capability, gage R&R, NCR/RCCA workflows, and three synthetic NCRs.
- Expanded revision-aware evidence graph and deterministic report/release tooling.
- End-to-end synthetic evidence generator and expanded CI.

### Changed
- Margin rows now require explicit allowable and safety-factor provenance.
- Project state now distinguishes complete software from external execution/data gates.

### Verification
- 43 automated tests passing before final evidence generation.
- All numerical examples remain `SYNTHETIC_TEST_ONLY`.

## 0.2.0 — 2026-07-12

- Added analytical benchmark, fatigue, uncertainty, F06, margin, and evidence-graph foundations.

## 0.1.0 — 2026-07-12

- Initial scope, load model, hand calculations, requirements, benchmarks, and traceability foundation.
