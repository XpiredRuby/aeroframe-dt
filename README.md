# AeroFrame-DT

**Full stress substantiation of one critical aircraft part, carried from load basis to inspection
interval — with every assumption tested.**

A forward pylon-to-wingbox attachment fitting (AF-DT-1000) on an MD-11-class aircraft, analysed the
way a stress engineer would: hand methods first, FE to verify the assumptions behind them, published
test data to correlate, and a formal stress report at the end — supported by a reproducible Python
toolchain and a revision-aware digital thread.

> **Claim boundary:** educational and portfolio-focused; non-OEM; non-certified. Geometry and load
> case are `SYNTHETIC_TEST_ONLY`; the damage-tolerance spectrum is `SYNTHETIC_SPECTRUM`.
> **Material allowables are real**, from MIL-HDBK-5J with page-level citation. No example load,
> dimension, allowable, spectrum, or result may be represented as aircraft design data.

**Start here: [`docs/STRESS_REPORT_AF-DT-1000.md`](docs/STRESS_REPORT_AF-DT-1000.md)**

---

## Result

| | |
|---|---|
| **Governing margin** | **`MS = +0.078`** — passes |
| Failure mode | combined bearing / transverse at the lug bore |
| Pin | high-strength steel mandatory, bending governs at 780 MPa |
| Damage tolerance | critical crack **3.07 mm**, NDI at 4,500-flight intervals |

### The margin moved by a factor of 9

| Stage | MS | What was wrong |
|---|---|---|
| Initial hand analysis | +0.710 | — |
| Thick-lug correction | +0.165 | the method assumes uniform bearing; at `t/D = 1.25` it isn't |
| Real A-basis allowables | **+0.078** | the assumed `Ftu` was 9% optimistic |

Neither correction refined the arithmetic. Each removed an assumption that did not hold. **The most
useful thing this project produced was finding out its own headline number was wrong.**

---

## What's distinctive

**Predictions were committed to git before the runs that tested them.** Eight in total. Four held,
four failed — including a bracketed deflection that came in 3× high, and a hypothesis about nodal
averaging that a targeted test falsified outright. **The failures are still in the repository**,
because removing them would misrepresent how the conclusions were reached.

**A measurement designed around a divergent quantity.** Contact pressure at a clearance-fit bore is
mesh-singular — it rose 134% across a three-point convergence study and never settled. The needed
quantity was extracted as a *ratio* of two runs sharing that singularity, which converged to 8.2%.
Predicted to work, then demonstrated to work.
[`docs/F7_CONTACT_THICK_LUG.md`](docs/F7_CONTACT_THICK_LUG.md)

**A methodological error caught after the fact and documented.** A linear elastic FE peak stress was
initially set up as a check on an allowable-based margin. It isn't one — empirical allowables already
contain the concentration and local plasticity. The setup was wrong, and the write-up says so.
[`docs/F5_MARGIN_CROSSCHECK.md`](docs/F5_MARGIN_CROSSCHECK.md)

**Three separate two-point convergence studies gave misleading answers.** The third would have
changed the engineering conclusion: a two-point trend extrapolated to a margin of +0.03, and the
third point showed it rebounding to +0.165.

---

## Analysis chain

| Phase | Content | Status |
|---|---|---|
| Loads | 9g emergency landing, 617,776 N at 59.04° | complete |
| F5 | Melcon-Hoblit lug analysis + Rev D linear elastic FE | complete |
| F6 | Pin bending, thick-lug sensitivity | complete |
| F7 | Two-body contact FE, `t_eff/t = 0.681` measured | complete, converged |
| F9 | Damage tolerance, critical crack + inspection interval | complete |
| F12 | Correlation against 243 published lug tests | complete |
| F15 | Nonconformance RCCA, mis-drilled bore | complete |
| F8 | Safe-life fatigue | **not supportable** — no S-N data exists for 7075-T7351 |

### Verification

| Check | Result |
|---|---|
| Hand method reconstructed independently on a stress basis | agrees to **0.06%** |
| FE equilibrium after mesh refinement | **0.006%** |
| Geometry mass vs FE model | **0.01%** |
| Correlation allowables vs MIL-HDBK-5J | Fsu matches to **0.1%** |
| Mesh convergence | 3-point, repeated, singularities ruled out |
| Damage tolerance, two independent implementations | agree to **7%** on critical crack, **10%** on life |

The damage-tolerance cross-check compared a hand calculation against `src/aeroframe_dt/fatigue.py`,
written independently of the analysis. The hand calculation's own stated limitation — that its
constant geometry factor would prove non-conservative — was recorded *before* the comparison and
confirmed by it, in both direction and magnitude.

---

## Figures

![Margin of safety vs edge distance ratio](figures/fig1_margin_vs_eD.svg)

Failure-mode map from the F12 correlation sweep. Shear-out governs below `e/D = 1.353`, bearing
above. Zero margin at `e/D = 1.201` — predicted from algebra before the run, then measured at −0.002.

![Plastic strain consistency check](figures/fig3_plastic_strain_check.svg)

**An unresolved problem, plotted deliberately.** Reported plastic strain and reported peak stress
disagree by a factor that grows as the plastic zone shrinks. One hypothesis was tested and rejected,
a second half-supported, and a flaw in the check itself found afterwards. Closed as *bounded*, not
solved. [`docs/F12_STRESS_STRAIN_CONSISTENCY.md`](docs/F12_STRESS_STRAIN_CONSISTENCY.md)

---

## Software framework

Alongside the analysis records, the repository contains tested implementations for:

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

See [`docs/SOFTWARE_COMPLETION_MATRIX.md`](docs/SOFTWARE_COMPLETION_MATRIX.md) for the boundary
between implemented software and CAD/solver/data execution.

### Quick verification

```bash
python -m pip install -e .
python -m unittest discover -s tests -v
python tools/check_traceability.py
python tools/generate_all_software_evidence.py
aeroframe-dt audit .
```

### Unified CLI

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

---

## Tools and sources

**Ansys Mechanical 2025 R2** — linear elastic and nonlinear frictional contact
**cadquery** — parametric geometry; all models rebuildable from `cad/`
**MIL-HDBK-5J** — material allowables, fracture toughness, crack growth data
**Abbott Aerospace AA-SM-009** — Melcon-Hoblit lug method, validated line-for-line against the
source's own worked example before use
**Ekvall (1986)**, *J. Aircraft* 23(5) — 243 lug tests, correlation anchor

---

## Repository

```
docs/    STRESS_REPORT_AF-DT-1000.md   <- start here
         MARGIN_SUMMARY.md             <- authoritative margin figure
         HANDOFF.md                    <- full project state
         F5/F6/F7/F9/F12/F15 analysis records
         SOFTWARE_COMPLETION_MATRIX.md
cad/     parametric generators (cadquery)
figures/ generated from recorded data by make_figures.py
loads/   load basis revisions
src/     aeroframe_dt package
tests/   unit tests for the analysis toolchain
tools/   traceability and evidence generation
```

## Repository policy

Commit source, solver inputs, compact outputs, plots, reports, hashes, and manifests. Do not
indiscriminately commit native solver databases or large binary result files. The release audit
rejects common ANSYS/NASTRAN/OptiStruct database formats.

## Status

The analysis chain is complete through the formal stress report. Remaining open items are listed in
[`docs/STRESS_REPORT_AF-DT-1000.md`](docs/STRESS_REPORT_AF-DT-1000.md) §12 — chiefly a real load
spectrum, the Ekvall specimen `t/D` range, and definition of the mating clevis.

Not checked or approved by a licensed stress engineer. This demonstrates method, traceability and
self-verification — it does not substantiate a flight article.
