# AeroFrame-DT

**Full stress substantiation of one critical aircraft part, carried from load basis to inspection
interval — with every assumption tested.**

A forward pylon-to-wingbox attachment fitting (AF-DT-1000) on an MD-11-class aircraft, analysed the
way a stress engineer would: hand methods first, FE to verify the assumptions behind them, published
test data to correlate, and a formal stress report at the end — supported by a reproducible Python
toolchain and a revision-aware digital thread.

> **Claim boundary:** educational and portfolio-focused; non-OEM; non-certified. Geometry and load
> case are `SYNTHETIC_TEST_ONLY`; the fatigue and damage-tolerance spectrum is `SYNTHETIC_SPECTRUM`;
> the cost rates are `ASSUMED_COST_BASIS`. **Material allowables, S/N curves and fracture data are
> real**, from MMPDS-2026 with table-level citation. No example load, dimension, allowable,
> spectrum, or result may be represented as aircraft design data.

**Start here: [`docs/STRESS_REPORT_AF-DT-1000.md`](docs/STRESS_REPORT_AF-DT-1000.md)**
**Authoritative margin: [`docs/MARGIN_SUMMARY.md`](docs/MARGIN_SUMMARY.md)**
**Lost? [`docs/README.md`](docs/README.md) indexes every document with reading paths.**

---

## Result

| | |
|---|---|
| **Governing margin** | **`MS = +0.151`** — passes |
| **Material** | **7050-T7451 plate**, MMPDS-2026 Table 3.7.4.0(b1), A-basis |
| Worst-case manufacturing tolerance stack | +0.128, 15.3% of margin consumed |
| At A-basis-consistent method scatter | −0.037 — negative, and stated rather than buried |
| Failure mode | combined bearing / transverse at the lug bore |
| Pin | high-strength steel mandatory, bending governs at 780 MPa |
| Damage tolerance | critical crack **3.51 mm** |
| **Safe life** | **5.25e5 flights mean, 1.31e5 at scatter factor 4** |
| First natural frequency | 1197 Hz — inside the plausible blade-passing band |
| **Requirements verified** | **18 of 18** |

### The margin moved by a factor of 4.7, and the material changed underneath it

| Stage | MS | What changed |
|---|---|---|
| Initial hand analysis | +0.710 | — |
| Thick-lug correction, elastic | +0.165 | the method assumes uniform bearing; at `t/D = 1.25` it isn't |
| Real A-basis allowables | +0.078 | the assumed `Ftu` was 9% optimistic |
| Elastic-plastic contact measurement | +0.156 | yielding redistributes the bearing peak |
| **Material re-selected to 7050-T7451** | **+0.151** | **7075-T7351 plate is not tabulated thick enough to make this part** |

The first two corrections refined nothing — each removed an assumption that did not hold. **The most
useful thing this project produced was finding out its own headline number, and then its own
material, were wrong.**

---

## What's distinctive

**The project audited its own sources and found the part could not be made.** Every allowable was
cited from MIL-HDBK-5J — cancelled in 2006, superseded by MMPDS, and removed from the 14 CFR 25.613
compliance path. Reading the current handbook to fix the citation revealed something worse:
**MMPDS tabulates 7075-T7351 plate only to 4.000 in, while this part's envelope requires 6.000 in
stock.** Not the wrong band — no band. The fix was a material change to 7050-T7451, which exists
precisely because 7075 runs out in thick section.
[`F21`](docs/F21_ALLOWABLES_GOVERNANCE.md) · [`F23`](docs/F23_MATERIAL_RESELECTION.md)

**A requirement written off as permanently blocked turned out not to be.** REQ-012 safe-life fatigue
was closed for the life of the project because no S-N curves exist for the T7351 temper. That was
true and still is. **It stopped applying when the material changed for unrelated reasons** — 7050-T7451
has a full S/N suite including a notched `Kt = 3.0` curve. 17/18 became 18/18 as a side effect of a
materials finding. [`F27`](docs/F27_REQ012_SAFE_LIFE.md)

**Two unrelated damage models agree on which cycles matter.** The safe-life Miner summation puts
57.9% of fatigue damage in the once-per-flight ground-air-ground cycle. The damage-tolerance Paris
integration, a completely different mechanism, put it at 59%. Neither was tuned to the other.

**Predictions were committed to git before the runs that tested them.** Eight in the FE correlation
work, plus: that the analytical 2133 Hz first mode would prove **high** (it did, by 44%); that a
beam section entered 90° out would read **exactly 4× the correct deflection** (it did); and that
7050's higher yield would collapse the plasticity gain and push `t_eff/t` back toward the elastic
bound (it did — 0.730 → 0.6828). **The failures are still in the repository.**

**A measurement designed around a divergent quantity.** Contact pressure at a clearance-fit bore is
mesh-singular — it rose 134% across a three-point convergence study and never settled. The needed
quantity was extracted as a *ratio* of two runs sharing that singularity, which converged to 8.2%.
[`F7`](docs/F7_CONTACT_THICK_LUG.md) · [`F16`](docs/F16_ELASTIC_PLASTIC_CONTACT.md) ·
[`F24`](docs/F24_MARGIN_REPROPAGATION.md)

**A cost analysis that found a materials problem instead of a price.** Buy-to-fly is **5.36** — over
80% of the plate becomes chips — and removing finished mass without shrinking the envelope costs
nothing to make. It was this analysis that first derived the 6.000 in stock requirement.
[`F20`](docs/F20_COST_TRADE.md)

**A composite trade answered from the project's own measurements.** Should this be carbon? No — and
not for generic reasons. F16 measured the margin nearly doubling *because the aluminium yielded and
redistributed the bearing peak*. A laminate has no such mechanism.
[`F22`](docs/F22_COMPOSITE_TRADE.md)

**A configuration-management tool tested against a rework cycle that actually happened**, which then
exposed a defect in its own cycle check — it hung instead of reporting. Fixed, tested, written up.
[`F14`](docs/F14_DIGITAL_THREAD.md)

**A released routing amended by change notice, not edited in place.** When the material changed, the
F13 process plan was left intact and PCN-001 issued against it, so the superseded instruction stays
legible. [`F26`](docs/F26_PROCESS_CHANGE_NOTICE.md)

**A methodological error caught after the fact and documented.** A linear elastic FE peak stress was
initially set up as a check on an allowable-based margin. It isn't one. The write-up says so.
[`F5`](docs/F5_MARGIN_CROSSCHECK.md)

**A claim retracted after the run that was supposed to prove it.** F16 was described in progress as
settling the Ekvall double-counting question. It does not — that question is about the composition
of a 1986 test dataset, and no FE run on this fitting can answer it.

---

## Analysis chain

| Phase | Content | Status |
|---|---|---|
| Loads | 9g emergency landing, 617,776 N at 59.04° | complete |
| F5–F7 | Lug analysis, linear elastic FE, contact FE | complete |
| F9 / F9b | Damage tolerance, inspection interval | complete |
| F10 / F17 | Dynamics and buckling, analytical then FE | complete |
| F11 | Geometric optimization | complete |
| F12 / F18 / F19 | Correlation against 243 lug tests, specimen basis, method cross-check | complete |
| F13 | Manufacturing, inspection, tolerance stack | complete |
| F14 | Digital thread | complete |
| F15 | Nonconformance RCCA, mis-drilled bore | complete |
| F16 | Elastic-plastic contact, 7075 | complete |
| F20 | Recurring cost trade and raw stock envelope | complete |
| F21 | Allowables governance, MMPDS transition | complete |
| F22 | Composite material trade | complete |
| **F23** | **Material re-selection to 7050-T7451** | **complete** |
| **F24** | **Margin re-propagation, `t_eff/t` = 0.6828** | **complete** |
| **F25** | **Damage tolerance re-derived on 7050** | **complete** |
| **F26** | **PCN-001 against the routing** | **complete** |
| **F27** | **REQ-012 safe-life fatigue** | **complete — 18/18** |

### Verification

| Check | Result |
|---|---|
| Hand method reconstructed independently on a stress basis | agrees to **0.06%** |
| FE equilibrium after mesh refinement | **0.006%** |
| Contact-model equilibrium, elastic-plastic runs | **10 ppm** |
| Constant-strain patch test on a distorted mesh | error **4.3e-19 m** |
| Cantilever, continuum model | **0.20%** |
| Plate bending vs Navier series | **0.62%** |
| Damage tolerance, two independent implementations | agree to **7%** on critical crack |
| **Safe-life vs damage-tolerance damage distribution** | **57.9% vs 59% on the GAG cycle** |
| Tolerance stack, exact vs linearised sensitivity | agree to **0.1%** |
| Critical crack routine reproduces the published F9 value | **3.068 vs 3.07 mm** |
| Margin rescaling reproduces the published F16 case | **4 decimal places** |
| Cross-solver NASTRAN check | decks generated, **predictions frozen, not yet run** |

---

## Software framework

Tested implementations for load provenance and free-body assembly; classical lug, bearing,
shear-out, pin, fastener and prying checks; traceable margin generation; solver-deck preparation for
**both Ansys APDL and NASTRAN**; mesh convergence and stress linearization; fatigue, Miner damage,
Paris crack growth and critical flaw size; Monte Carlo, DOE and robust optimization; recurring cost
modelling; allowables citation auditing; STEP AP242 and QIF-style inspection linkage; capability and
gage R&R; a revision-aware SQLite/JSON/DOT digital thread; and automated reports, manifests and CI.

See [`docs/SOFTWARE_COMPLETION_MATRIX.md`](docs/SOFTWARE_COMPLETION_MATRIX.md) for the boundary
between implemented software and CAD/solver/data execution.

### Quick verification

```bash
python -m pip install -e .
python -m unittest discover -s tests -v
python tools/check_traceability.py
python tools/check_allowables_citations.py
python tools/run_f13_inspection_plan.py
python tools/build_f14_thread.py
python tools/run_f20_cost_model.py
aeroframe-dt audit .
```

---

## Tools and sources

**Ansys Mechanical 2025 R2** — linear elastic, nonlinear frictional contact, elastic-plastic, modal
and eigenvalue buckling
**Ansys Mechanical APDL 2025 R2** — analytical verification benchmarks
**cadquery** — parametric geometry; all models rebuildable from `cad/`
**MMPDS-2026, Volume I** — allowables, S/N curves, fracture toughness, crack growth. Accessed via
Knovel. **Supersedes MIL-HDBK-5J**, which this project cited until F21 and F23 —
see [`F21`](docs/F21_ALLOWABLES_GOVERNANCE.md)
**Abbott Aerospace AA-SM-009** — Melcon-Hoblit lug method, validated against the source's own
worked example before use
**Ekvall (1986)**, *J. Aircraft* 23(5) — 243 lug tests, correlation anchor

---

## Repository

```
docs/               README.md                     <- index of every document
                    STRESS_REPORT_AF-DT-1000.md   <- start here
                    MARGIN_SUMMARY.md             <- authoritative margin figure
                    F5..F27 analysis records
benchmarks/         locked acceptance criteria, APDL decks, NASTRAN decks + frozen predictions
cad/                parametric generators (cadquery)
digital_thread/     populated evidence graph, JSON/DOT, impact analyses
figures/            generated from recorded data by make_figures.py
inspection_quality/ inspection plan for Rev D
loads/              load basis revisions
reports/            FE_VERIFICATION_REPORT.md
requirements/       requirements and verification matrix
results/            recorded numerical outputs, cost model, citation inventory
src/                aeroframe_dt package
tests/              unit tests for the analysis toolchain
tools/              traceability, inspection, digital thread, cost, citations, evidence generation
```

## Status

**18 of 18 formal requirements verified.** `tools/check_traceability.py` passes at 18 requirements
and 45 verification rows.

REQ-012 safe-life fatigue closed on 2026-08-06 against MMPDS-2026 §3.7.4.2.8(f). **It is satisfied
as written; it does not demonstrate that the fitting has adequate fatigue life** — the `Kt = 3.0`
specimen curve is applied to a bore whose true concentration was never derived, and F27 §6 says so.
**Damage tolerance remains the governing route.**

Open items are stated in `MARGIN_SUMMARY.md` §12 rather than left implicit — the 7050 inspection
interval (crack-growth curves not digitised), Ekvall's alloy coverage for 7050, three unmapped
MMPDS locators, mesh convergence of the elastic-plastic ratio, and single-vs-redundant load path.

Not checked or approved by a licensed stress engineer. This demonstrates method, traceability and
self-verification — it does not substantiate a flight article.
