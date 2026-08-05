# Changelog

## 0.7.0 — 2026-08-05

**A market review of the project turned into a defect report on its own sources.**

### Added
- **F21 allowables governance** (`docs/F21_ALLOWABLES_GOVERNANCE.md`,
  `tools/check_allowables_citations.py`): every material allowable in this project is cited from
  **MIL-HDBK-5J, a cancelled document**, superseded by MMPDS and removed from the 14 CFR 23.613 /
  25.613 compliance path. **51 substantive citations across 18 files**, six distinct locators, all
  `TO_VERIFY`. The values are not in question — MMPDS-01 and MIL-HDBK-5J were issued technically
  equivalent for the 2003 transition year — but the currency of the citation is.
- **REQ-012 reopened as a question.** "No S-N curves exist for the T7351 temper" is a statement
  about a 2003 document. Whether the current handbook contains them is **unknown and must not be
  assumed in either direction**. If it does, the project goes 17/18 → 18/18; if it does not, the
  blocker is restated against the current handbook, which is stronger. Status changed from
  *permanently blocked* to *open, under review*.
- **F22 composite trade** (`docs/F22_COMPOSITE_TRADE.md`): retain 7075-T7351. The argument comes
  from the project's own measurement — F16 recorded the margin nearly doubling **because the
  aluminium yielded and redistributed the bearing peak**, and a laminate has no such mechanism. At
  `t/D = 1.25` the pin flexure drives load through the thickness into the matrix-dominated
  direction, and the 59.04° off-axis load forces quasi-isotropic. Composite wins on buy-to-fly,
  mass and corrosion, and still loses. **Screening trade, not a sizing** — no laminate allowables
  were available.
- **NASTRAN cross-solver verification** (`benchmarks/NASTRAN_CROSSCHECK.md`, three `.bdf` decks):
  every FE result in this project comes from one solver family. Four predictions frozen before
  execution, including that `PBEAM` without shear factors will land within 0.05% of the
  Euler-Bernoulli oracle and thereby **demonstrate** the shear-flexibility explanation previously
  offered for the BEAM188 +0.57% exceedance. **Not yet run** — no licence confirmed.
- `docs/README.md`: an index of all 36 documents grouped by purpose, with reading paths and every
  superseded document labelled.

### Fixed
- **`PBEAM` wrote the torsional constant into the `I12` product-of-inertia field**, leaving `J`
  blank. `I12` must be zero for a symmetric rectangular section; non-zero rotates the principal
  axes and couples the bending planes. **The static tip-load case would still have returned a
  plausible deflection and passed the 0.5% criterion.** Third deck-level defect found by inspection
  rather than by result, after `NMODIF` and `SECDATA` — all three produce believable numbers.
- **The F21 citation inventory counted itself.** The first published version reported 58 citations
  across 19 files, a figure taken before the document existed; publishing it moved the total to 65.
  Files that are *about* the citation problem are now counted separately from files that are
  *instances* of it. Recorded in F21 §4 rather than silently corrected.
- Cancellation date softened from an asserted "March 2006" to what the notices support — issued
  2004, restated 2006, with sources differing on the operative date.

### Changed
- Digital thread rebuilt to **62 artifacts, 103 links, 0 audit issues**; replay marks 30 stale,
  forward query 22. **F21 is deliberately outside the load-basis blast radius** — a finding about a
  document's currency cannot be invalidated by a load revision — while F22 is inside it. Verified
  against the generated impact analysis rather than asserted.
- README rewritten as a front door: F21 and F22 surfaced, counts corrected, docs index linked.
- Repository cleanup: internal instruction sheets, superseded planning documents and a
  typo-duplicated parameter schema removed, each with zero remaining references. **Superseded
  analysis records were deliberately retained** and are labelled as such in the docs index.

## 0.6.0 — 2026-08-04

**First cost analysis in the project — and it found a material-allowables problem, not a price
problem.**

### Added
- **F20 recurring cost trade** (`docs/F20_COST_TRADE.md`, `tools/run_f20_cost_model.py`):
  buy-to-fly **5.36**, material utilisation **18.6%**. Cost rates are declared
  `ASSUMED_COST_BASIS` low/nominal/high, never quoted as sourced; only conclusions that survive the
  full range are drawn.
- **OPEN finding, material band.** The Rev D envelope is 16.000 x 6.000 x 9.000 in, so the part
  cannot be cut from stock thinner than **6.000 in**, but every allowable in the project comes from
  the **2.001–2.500 in** band of MIL-HDBK-5J Table 3.7.6.0(b3). The band was selected on `t_lug`
  rather than on stock thickness. Expected direction is **non-conservative**; magnitude is not
  stated because the table has not been read. Registered in the thread as `ANL-F20-COST`, state
  OPEN.
- **F20 answers the question F11 never asked.** Pocketing 10% of finished mass out at fixed envelope
  costs **+0.2%**; removing the same mass by shrinking the envelope 10% costs **−6.8%**. Envelope,
  not mass, is what is purchased — which makes the orientation lever free and the Rev D thickness
  growth paid for in plate.
- Regression test `test_digital_thread_cycle_is_reported_not_hung` in `tests/test_advanced.py`.

### Fixed
- **`EvidenceGraph.audit()` did not terminate on a cycle reached from outside that cycle.** The
  recursive walk used `UNION ALL` and only guarded re-entry to its own start node. Changed to
  `UNION`, which bounds the walk and reports the cycle instead of hanging. Found by registering
  F20 with a back-edge to the margin, which closed the loop `MARGIN -> F13 -> F20 -> MARGIN`.
  The back-edge was then removed on its merits: F20 sits downstream of the margin, and the finding
  it raises is carried in artifact metadata. Written up in `docs/F14_DIGITAL_THREAD.md` §5.2.

### Changed
- **F19 registered in the digital thread** as `ANL-F19-CROSSCHECK`, linked to the margin as
  `cross_checks` — a finding, not a correction. The released margin remains unamended.
- Digital thread rebuilt to **59 artifacts, 95 links, 0 audit issues**. Historical replay marks
  29 stale, forward query 21. Counts updated in `README.md`, `digital_thread/README.md` and
  `docs/F14_DIGITAL_THREAD.md`, which had drifted (56/79 and 57/84 were both still quoted).
- `README.md` status corrected from 38 to **41 verification rows**, matching
  `tools/check_traceability.py`.

## 0.5.0 — 2026-08-03

**Governing margin moves from `+0.078` to `+0.156`.** Three Ansys sessions closed every
solver-dependent open item. **17 of 18 requirements verified — the honest ceiling.**

### Added
- **F16 elastic-plastic contact** (`docs/F16_ELASTIC_PLASTIC_CONTACT.md`): `t_eff/t = 0.7300`
  measured against the elastic 0.6809. Bilinear isotropic hardening, yield 358.5 MPa, tangent
  modulus 1631 MPa. Equilibrium verified to 10 ppm on both the real-pin and stiff-pin solves.
  Peak plastic strain 6.46% confirms the material yielded.
- **F17 modal and buckling FE** (`docs/F17_MODAL_BUCKLING_FE.md`): six modes, first at 1197.2 Hz;
  three eigenvalue buckling modes, all negative.
- **FE verification report** (`reports/FE_VERIFICATION_REPORT.md`): patch test, cantilever in two
  element formulations, and simply supported plate, against criteria frozen before execution.
- Four Mechanical APDL verification decks in `benchmarks/`.
- `docs/ansysworkorder.md`, the step-by-step execution record for the three sessions.
- Verification rows AFDT-V-034 through AFDT-V-039.

### Changed
- **Stress report to Rev E.** New §6.5 manufacturing tolerance stack and §9 dynamics and stability;
  §10 gains the analytical benchmarks. Margin history now shows a 4.6x movement, not 9.1x.
- **`MARGIN_SUMMARY.md`** re-propagated throughout. Ekvall worst case improves from −0.094 to
  −0.028. The breakeven is `t_eff/t = 0.7513`; the measurement came in at 0.7300, **just short of
  clearing the scatter band.**
- **F13 tolerance stack re-propagated** at the new operating point: worst case +0.133, consuming
  14.9% of the margin against 27.6% before. Tolerances would need to be 6.7x wider to reach zero.
- `tools/run_f13_inspection_plan.py` now computes the stack at both contact ratios and re-anchors
  the bore-position sensitivity on the F15 case.
- Digital thread rebuilt to **56 artifacts, 79 links, 0 audit issues**. F7 is linked to F16 by
  `superseded_by` rather than being overwritten.
- REQ-009 and REQ-014 status OPEN/IN_PROGRESS to VERIFIED.

### Fixed
- **`patch.inp`**: `NMODIF` cannot move nodes still attached to a meshed area. Without
  `MODMSH,DETACH` the mesh stayed a regular grid — which passes a patch test trivially, and would
  have been recorded as a pass on a test that was not testing anything.
- **`cant.inp` and `cantsolid.inp`**: for `SECTYPE RECT` the first `SECDATA` argument lies along
  element local Z, so the 0.05 dimension landed in the load plane and returned **exactly 4x** the
  correct deflection. The same error in the solid model's `BLOCK` made the continuum companion a
  different beam from the beam-element model. **The 4x symptom and its fix were written into the
  deck's comments before execution**, and are recorded as a prediction that held.

### Corrected
- **F16 §6 retracts a claim made during execution.** The elastic-plastic run was described in
  progress as settling whether the thick-lug correction and the Ekvall scatter band double-count.
  It does not. That question concerns the composition of a 1986 test dataset and requires the paper.
  The open item stays open and the conservative default is retained.

### Verification
- `tools/check_traceability.py`: 18 requirements, 39 verification rows, passing.
- Re-anchored bore-position sensitivity reproduces the independently derived 0.747/in at the
  elastic nominal to four significant figures.
- Three benchmark caveats recorded rather than smoothed over: a 1e-8 relative force residual
  against a "machine precision" criterion, the beam element's 0.57% against a 0.5% limit, and the
  plate sequence drifting upward rather than converging.
- **AFDT-REQ-012 remains open permanently.** MIL-HDBK-5J provides no S-N curves for the T7351
  temper; damage tolerance is the appropriate route and is complete.

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
- **F14 populated digital thread** (`docs/F14_DIGITAL_THREAD.md`): 53 artifacts, 68 links, zero
  audit issues, every file-backed artifact carrying its build-time SHA-256.
- Two recorded impact analyses: a historical replay of the load revision B to C axis-mapping
  correction, and a forward query on the pending elastic-plastic contact run.
- Verification rows AFDT-V-030 through AFDT-V-033.

### Changed
- `PMI_GDT_DEFINITION.md` limitation 2 closed — the statistical tolerance stack now exists.
- README surfaces F13 and F14 and states the three remaining solver-dependent open items.
- Both `inspection_quality/` and `digital_thread/` READMEs now describe delivered work rather than
  plans.

### Verification
- `tools/check_traceability.py` passes: 18 requirements, 33 verification rows.
- Exact tolerance stack agrees with the independent linearised thickness sensitivity to 0.1%.
- Historical replay reproduces the rework blast radius previously established by hand; the single
  over-flag is identified and explained rather than suppressed.
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
