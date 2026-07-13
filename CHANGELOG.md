# Changelog

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
