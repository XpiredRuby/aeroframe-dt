# Documentation Index

36 documents. This page is the map. **If you are reading this repository for the first time, start
with the three documents in bold.**

---

## Start here

| Document | What it is |
|---|---|
| **[STRESS_REPORT_AF-DT-1000.md](STRESS_REPORT_AF-DT-1000.md)** | **The released substantiation report.** The whole project in one document. |
| **[MARGIN_SUMMARY.md](MARGIN_SUMMARY.md)** | **The authoritative margin**, its basis, and every open item against it. |
| **[RISKS_AND_LIMITATIONS.md](RISKS_AND_LIMITATIONS.md)** | **What this project does not claim.** Read before citing any number. |

---

## Definition — what is being analysed and why

| Document | Content |
|---|---|
| [DECISIONS.md](DECISIONS.md) | Scope, claim boundary, and the decision log format |
| [DECISIONS_AF-DT-1000_revD.md](DECISIONS_AF-DT-1000_revD.md) | **Frozen Rev D geometry** and the rationale for every dimension |
| [DECISIONS_AF-DT-1000_revA.md](DECISIONS_AF-DT-1000_revA.md) | Original Rev A geometry — superseded, retained as history |
| [LOAD_PATH_AND_FBD.md](LOAD_PATH_AND_FBD.md) | Free bodies and load path from airframe to fitting |
| [PMI_GDT_DEFINITION.md](PMI_GDT_DEFINITION.md) | GD&T scheme, every callout traced to the analysis that sizes it |

## Analysis — the substantiation chain

| Document | Content |
|---|---|
| [F5_FE_REVD_LINEAR_ELASTIC.md](F5_FE_REVD_LINEAR_ELASTIC.md) | Rev D linear elastic FE, equilibrium to 0.006% |
| [F5_MARGIN_CROSSCHECK.md](F5_MARGIN_CROSSCHECK.md) | **A methodological error, caught and documented** — FE peak stress is not a check on an allowable-based margin |
| [F6_PIN_BENDING_THICK_LUG.md](F6_PIN_BENDING_THICK_LUG.md) | Pin bending governs at 780 MPa; steel pin is mandatory |
| [F7_CONTACT_THICK_LUG.md](F7_CONTACT_THICK_LUG.md) | Contact FE; a **measurement designed around a mesh-divergent quantity** |
| [F16_ELASTIC_PLASTIC_CONTACT.md](F16_ELASTIC_PLASTIC_CONTACT.md) | Elastic-plastic contact — the correction that moved the margin `+0.078 → +0.156` |
| [F9_DAMAGE_TOLERANCE.md](F9_DAMAGE_TOLERANCE.md) | Critical crack size 3.07 mm |
| [F9b_SPECTRUM_AND_INTERVAL.md](F9b_SPECTRUM_AND_INTERVAL.md) | Inspection interval, 4,500 flights |
| [F10_DYNAMICS_BUCKLING.md](F10_DYNAMICS_BUCKLING.md) | Analytical dynamics and stability |
| [F17_MODAL_BUCKLING_FE.md](F17_MODAL_BUCKLING_FE.md) | Modal + eigenvalue buckling FE; first mode 1197 Hz |
| [F11_OPTIMIZATION.md](F11_OPTIMIZATION.md) | Geometric optimisation on mass and margin |

## Validation — checking the analysis against something external

| Document | Content |
|---|---|
| [F12_CORRELATION_AF-DT-1000.md](F12_CORRELATION_AF-DT-1000.md) | Correlation against **243 published lug tests** |
| [F18_EKVALL_SPECIMEN_BASIS.md](F18_EKVALL_SPECIMEN_BASIS.md) | What the test population actually contains, and the double-counting question |
| [F19_METHOD_CROSSCHECK.md](F19_METHOD_CROSSCHECK.md) | A second independent method — raised as a finding, **not silently folded into the margin** |
| [F12_STRESS_STRAIN_CONSISTENCY.md](F12_STRESS_STRAIN_CONSISTENCY.md) | **An unresolved problem, published rather than buried.** Closed as *bounded*, not solved |
| [F12_FE_RESULTS_AF-DT-1000.md](F12_FE_RESULTS_AF-DT-1000.md) | Recorded FE results supporting F12 |

## Production — making it, inspecting it, and what happens when it goes wrong

| Document | Content |
|---|---|
| [F13_MANUFACTURING_INSPECTION.md](F13_MANUFACTURING_INSPECTION.md) | Process plan, 10 inspection characteristics, **tolerance stack back onto the margin** |
| [F15_NONCONFORMANCE_RCCA_AF-DT-1000.md](F15_NONCONFORMANCE_RCCA_AF-DT-1000.md) | **Mis-drilled bore: margin re-run, REWORK disposition, root cause.** MRB/liaison work |
| [F20_COST_TRADE.md](F20_COST_TRADE.md) | Recurring cost, buy-to-fly 5.36 — **and an open finding about the plate the part can be cut from** |

## Governance — the sources themselves

| Document | Content |
|---|---|
| [F21_ALLOWABLES_GOVERNANCE.md](F21_ALLOWABLES_GOVERNANCE.md) | **Every allowable is cited from a cancelled handbook.** MMPDS transition, and REQ-012 reopened |
| [F22_COMPOSITE_TRADE.md](F22_COMPOSITE_TRADE.md) | Should this be composite? **No — and the reason comes from F16's own measurement** |

## Infrastructure

| Document | Content |
|---|---|
| [F14_DIGITAL_THREAD.md](F14_DIGITAL_THREAD.md) | Evidence graph, hash-verified, **tested against a rework cycle that actually happened** |
| [SOFTWARE_COMPLETION_MATRIX.md](SOFTWARE_COMPLETION_MATRIX.md) | The boundary between implemented software and external solver/data execution |
| [HANDOFF.md](HANDOFF.md) | Long-form project handoff |
| [ansysworkorder.md](ansysworkorder.md) | Step-by-step execution record for the Ansys sessions |

## Superseded — retained deliberately

**This project does not delete work that turned out to be wrong or was overtaken.** Where a document
has been superseded, it carries a banner saying so and points at what replaced it. The history is
part of the evidence.

| Document | Status |
|---|---|
| [STRESS_REPORT.md](STRESS_REPORT.md) | Framework placeholder; its §5 gate list is the record of what had to be closed first |
| [F5_F6_STATIC_RESULTS_AF-DT-1000_revA.md](F5_F6_STATIC_RESULTS_AF-DT-1000_revA.md) | Rev A results |
| [F5_STATIC_RESULTS_AF-DT-1000_revB.md](F5_STATIC_RESULTS_AF-DT-1000_revB.md) | Rev B results — the load-axis mapping error was found here |
| [F5_STATIC_RESULTS_AF-DT-1000_revD.md](F5_STATIC_RESULTS_AF-DT-1000_revD.md) | Rev D static results, superseded by the FE record |

---

## Reading paths

**If you have ten minutes** — `STRESS_REPORT_AF-DT-1000.md`, then `MARGIN_SUMMARY.md` §11 for the
open items.

**If you want to know whether the work is honest** — `F5_MARGIN_CROSSCHECK.md` (an error, admitted),
`F12_STRESS_STRAIN_CONSISTENCY.md` (a problem, unsolved and published), `F19_METHOD_CROSSCHECK.md`
(a finding raised against the released number rather than absorbed into it), and `F21` (a defect in
the project's own sourcing, found late and written up rather than quietly patched).

**If you are hiring for stress or MRB work** — `F13`, `F15`, `F20`.

**If you are hiring for FE or methods work** — `F7`, `F16`, `../reports/FE_VERIFICATION_REPORT.md`,
and `../benchmarks/NASTRAN_CROSSCHECK.md`.
