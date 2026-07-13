# Benchmark Lock

**Lock date:** 2026-07-12. Benchmark definitions may only change through a recorded decision; results may not be used to tune acceptance tolerances after the fact.

## B-001 — Constant-strain patch

- Domain: 1 m × 1 m plane-stress patch, arbitrary conforming triangle/quad subdivision.
- Material: `E = 70 GPa`, `ν = 0.30`.
- Prescribed linear field: `u = 1e-3 x + 2e-4 y`; `v = -3e-4 x + 5e-4 y`.
- Exact strains: `εx=1e-3`, `εy=5e-4`, `γxy=-1e-4`.
- Acceptance: displacement max absolute error `<=1e-10 m`; element strain max absolute error `<=1e-10`; reaction equilibrium relative error `<=1e-10`.

## B-002 — Euler-Bernoulli cantilever

- Beam: `L=1 m`, rectangular `b=0.05 m`, `h=0.10 m`, `E=70 GPa`, tip load `P=1000 N`.
- Exact: `I=bh^3/12`, `δ=PL^3/(3EI)`, `θ=PL^2/(2EI)`, root extreme-fiber stress `6PL/(bh^2)`.
- Acceptance: beam model `<=0.5%` displacement error; continuum model demonstrates convergence and `<=2%` displacement error away from the clamp singular region.

## B-003 — Simply-supported square plate under uniform pressure

- Plate: `a=b=1 m`, `t=0.01 m`, `E=70 GPa`, `ν=0.30`, `q=1000 Pa`.
- Oracle: Navier double-sine series for Kirchhoff-Love plate theory, evaluated to a documented truncation error below `0.05%`.
- Acceptance: thin-shell center deflection `<=2%` from oracle and convergent moments at the center; transverse shear and corner singular quantities are excluded.

## B-004 — Hertz line contact

- Geometry: elastic cylinder against elastic half-space, unit axial length.
- Inputs: `R=0.05 m`, load per length `W'=100000 N/m`; both bodies `E=210 GPa`, `ν=0.30`.
- Effective modulus: `1/E'=(1-ν1^2)/E1+(1-ν2^2)/E2`.
- Exact half-width: `b=sqrt(4 W' R/(π E'))`; peak pressure `p0=2W'/(πb)`.
- Acceptance: integrated contact resultant `<=0.2%` error; contact half-width `<=3%`; peak pressure is reported but is not the sole pass/fail quantity.

## B-005 — Eccentric fastener group

- Method source: NASA RP-1228, *Fastener Design Manual*, design-criteria section on direct plus moment-induced fastener loads.
- Pattern: eight equal fasteners at `(x,y) = (±0.15, ±0.05)` and `(±0.05, ±0.05)` m.
- Load: `Fx=80 kN`, `Fy=40 kN`, `Mz=12 kN·m` about group centroid.
- Oracle: direct load divided by `n` plus tangential moment load `M r_i / Σr_n²`, combined vectorially.
- Acceptance: each component and resultant agrees with the independent oracle to `1e-10` relative arithmetic tolerance; vector sum and moment reproduce the applied load.

## B-006 — Constant-amplitude Paris-law crack growth

- Geometry factor: constant `β=1.12`.
- Inputs: `a0=0.5 mm`, `af=5 mm`, `Δσ=80 MPa`, `C=1.0e-12 m/cycle/(MPa√m)^m`, `m=3.0`.
- Oracle: closed-form integration of `da/dN=C(βΔσ√(πa))^m`.
- Acceptance: numerical integrator life `<=0.2%` from closed form. AFGROW screening must archive the exact model/spectrum and explain any difference; AFGROW agreement is not physical validation.

## B-007 — NIST STEP AP242 semantic-PMI transfer

- Test case: NIST Simplified Test Case 08 (STC-08), STEP AP242 edition supplied by NIST.
- Acceptance: file imports without repair; semantic dimensions/tolerances and datum references are inventoried before and after translation; missing/altered semantic entities are zero for the selected authoritative path or are explicitly dispositioned.
- Source: NIST MBE PMI Validation and Conformance Testing Project.

## B-008 — NIST QIF PMI report

- Tool: NIST QIF PMI Report (QPR) version 2.01.
- Input: a QIF 3.0 example containing semantic PMI and measurement/QPid relationships.
- Acceptance: generated spreadsheet completes without schema errors; every selected critical characteristic has a stable identifier linking design requirement, PMI, inspection plan, and result.

## External-correlation benchmark still to freeze

A public metallic lug/bearing-bypass experimental dataset is required before F12. Selection is intentionally not fabricated here. The dataset must provide specimen geometry, material state, boundary/loading definition, and measured stiffness/strain/failure data. It will be locked before any production-model tuning.

## Primary sources

- NASA RP-1228 Fastener Design Manual: https://ntrs.nasa.gov/citations/19900009424
- NIST MBE PMI test cases: https://www.nist.gov/ctl/smart-connected-systems-division/smart-connected-manufacturing-systems-group/mbe-pmi-0
- NIST QIF PMI Report: https://www.nist.gov/services-resources/software/qif-pmi-report-software
