# AeroFrame-DT — Handoff (current as of end of F12)

## 0. Who I am / how to work with me
- I'm **Ruby** (GitHub: **XpiredRuby**). Texas A&M aerospace senior. Portfolio project, not a pro dev.
- **Talk in short, plain words. Caveman-brief. No yapping.** I'm low on credits.
- **Only tell me what *I* need to do.** If it's GitHub or software, YOU do it — you have write access.
- Only ask me for: Ansys/FEA runs, browser logins, physical file moves.
- **Don't ask me to pick options.** Decide yourself using good engineering + job-market reasoning.
- **Be honest. Never guess numbers or citations.** Verify or say you can't.
- After each milestone, give **% complete of whole project**.
- **Scope cuts unwelcome.** Don't shrink the project.

## 1. What the project IS
**AeroFrame-DT** = rigorous engineering **substantiation** of ONE small critical aircraft part —
a **forward pylon-to-wingbox attachment fitting (AF-DT-1000)** on an MD-11-class aircraft — done
like a real aerospace stress engineer, with a full digital-thread evidence trail.

- **Thesis: depth over breadth on ONE fitting. Do NOT add more parts.**
- Claim boundary: **educational / representative / portfolio only. Non-OEM, non-certified.
  All numbers `SYNTHETIC_TEST_ONLY`.**

## 2. Repo
- **github.com/XpiredRuby/aeroframe-dt**, owner `XpiredRuby`, repo `aeroframe-dt`, branch `main`.
- **GitHub connector HAS WRITE ACCESS.** Claude commits directly via `create_or_update_file`
  (needs correct blob SHA when overwriting). `push_files` returns 403 — use single-file calls.
- **Binary files (.xlsx, .step, .png) CANNOT be pushed** by Claude — the tool handles text only.
  I upload those by hand. **SVG is text and CAN be pushed.**

## 3. Environment
- **Ansys Discovery / Mechanical 2025 R2** on **TAMU virtual desktop (VDI)** — full license.
- Files: my PC → Google Drive **AeroFrame-DT** (xpiredruby@gmail.com) → VDI. Also H: drive (persists).
- Hand calcs: **Abbott Aerospace** sheets (AA-SM-009-002/-005), digitizing USAF AFFDL-TR-69-42 /
  NASA TM X-73305 (Melcon-Hoblit lug method).
- I drive Ansys via **Claude for Chrome extension** (use Sonnet there to save credits).

## 4. GEOMETRY — Rev D (frozen)
| Param | Rev A | **Rev D** |
|---|---|---|
| d_pin | 2.000 | 2.000 |
| t_lug | 1.500 | **2.500** |
| w_lug | 4.000 | 4.000 |
| e_center | 2.500 | 2.500 |
| t_flange | 1.000 | 1.000 |
| t_web | 0.750 | **2.500** (constant-thickness blade) |
| r_blend | 0.500 | 0.500 |
| g_y | 2.000 | **4.000** |
| p_x | 1.500 | 1.500 |
| L_station | 16.000 | 16.000 |

Volume 166.19 in³, **mass 7.65 kg** (FE verification target). Material 7075-T7351
(E=71.7 GPa, ν=0.33, ρ=2810, Ftu≈71 ksi representative).
Ratios: e/D=1.25, W/D=2.00, t/D=1.25. Abr=5.00 in², Atn=5.00 in², Aav=3.75 in².

**Axis mapping FROZEN (identity):** CAD X→aircraft X (fwd), Y→Y (span), Z→Z (up).
Lug axis = CAD Z. Bore axis = CAD Y.

## 5. LOADS — Rev C
- 6000 kg propulsion, 9g fwd. LC-02 governs.
- F_x = 529,740 N fwd; CG offset → couple → R_z = 317,840 N vertical.
- **Resultant 617,776 N at 59.04° off the lug axis. TRANSVERSE-DOMINANT.**
- In lb: P_axial = 71,453 lb (Z), P_transverse = 119,090 lb (X).

## 6. RESULT — margin CLOSED
**M.S. = +0.71.** Factors: Kt=0.950, Ktru=0.7875, Kbr=1.240.
Allowables: P'bru=440,200 lb; P'tu=337,250 lb; P'tru=279,562 lb.
Ra=0.2436, Rtr=0.4899 → **MS=+0.710**.
**Method validated line-for-line against AA-SM-009-005's own worked example** before use.
Caveat: Ftux set = Ftu. At −10% Ftux, MS ≈ +0.5. Still passes.

## 7. F12 CORRELATION — **COMPLETE**

### Piece 1 — literature anchor (done)
**Ekvall, J.C., "Static Strength Analysis of Pin-Loaded Lugs," J. Aircraft 23(5), 1986,
pp. 438-443** (Lockheed). **243 lug tests, 24 materials, predicted/test 0.85–1.19, mean 1.003.**
Propagated through our +0.71: worst case **+0.44**, mean +0.70, best +1.01.

**Honesty note:** the IAF paper (Shiroky et al.) has a unit error in its headline test
("3850 lbf" vs "3900 kgf") and its stated e/D=1.26 doesn't follow from D=15.88/e=40mm.
NOT the anchor. Only its self-consistent nominal parametric case used as FE geometry.

### Piece 2 — FE sweep (done)
Straight 7075-T651 lug, D=26.8 mm, t=25 mm, shank 160.8 mm, P=284,686 N axial.
Five e/D cases solved. Full record: `docs/F12_FE_RESULTS_AF-DT-1000.md`.

| e/D | Peak vM (MPa) | Deformation (mm) | Plastic strain | Reaction Y (N) |
|---|---|---|---|---|
| 1.0 | 750.23 (discarded) | 7.655 | 0.37211 | -284,690 |
| 1.2 | 521.47 | 0.896 | 0.03107 | -284,690 |
| 1.5 | 490.45 | 0.632 | not captured | -284,690 |
| 1.8 | 506.34 | 0.526 | 0.00888 | -284,690 |
| 2.0 | 503.49 | 0.4817 | 0.00795 | -284,690 |

**Key findings:**
- **Shear-out governs below e/D = 1.353, bearing above it.** Bearing margin is flat at **+0.216**
  because bearing area is `D*t` and neither varies in this sweep.
- **Zero margin at e/D = 1.201.** Confirmed by the e/D = 1.2 run (measured MS -0.002).
- **e/D = 1.0 fails by shear-out.** Its 750 MPa peak requires 37% plastic strain, far beyond
  7075-T651 ductility — discarded as unphysical, not reported.
- **Elastic scaling law:** measured deformation / shank stretch `PL/(AE)` = 1.970, 1.968, 2.002 at
  e/D = 1.5, 1.8, 2.0. Constant to 1.7%.
- **Mesh convergence (4/2/1 mm at e/D=1.5): singularity ruled out.** Peak stress oscillates within
  ±2% rather than climbing. Deformation converged to 0.12%; reaction exact.
- Because the sweep holds `w = 2e`, **net-section and shear-out areas are algebraically identical**.
  Net section can never govern here. Property of the parametrisation, not a general lug result.

**Three predictions were recorded in git BEFORE their runs.** Two held (e/D=1.2 failure onset,
e/D=1.8 bearing takeover). One missed (e/D=2.0 plastic strain came in above the stated range).
The miss is retained in the record.

**Peak stress is NOT quoted quantitatively for e/D >= 1.2.** See `docs/F12_STRESS_STRAIN_CONSISTENCY.md`:
reported peak stress and measured plastic strain disagree by ~29 MPa wherever plasticity is
confined. One hypothesis (nodal averaging) was tested and rejected. A second (integration-point
extrapolation) was supported by Elemental Mean but not by mesh refinement. A flaw in the check
itself — comparing global maxima that may not be colocated — was found afterwards.
**Closed as bounded: true peak at e/D=2.0 lies between 469 and 503 MPa, i.e. barely yielding.**
No sweep conclusion depends on it.

## 8. F15 RCCA — DONE
Representative MRB/nonconformance: **mis-drilled bore, edge distance 2.500 → 1.900 in**.
Margin **+0.71 → +0.22**. At Ekvall's worst ratio (1.19) it's only **+0.025** — so disposition =
**REWORK**, not use-as-is. Full 8D/5-Why: root cause = datum not propagated from drawing to shop
traveller.

## 9. Committed files (all on `main`)
- `cad/PARAMETER_SCHEMA.csv`, `cad/build_revD.py`, `cad/build_lug_sweep.py`
- `docs/DECISIONS_AF-DT-1000_revA.md`, `_revD.md`
- `docs/F5_F6_STATIC_RESULTS_AF-DT-1000_revA.md`, `F5_..._revB.md`, `F5_..._revD.md` ← the +0.71 result
- `docs/F12_CORRELATION_AF-DT-1000.md`
- **`docs/F12_FE_RESULTS_AF-DT-1000.md`** ← full sweep record
- **`docs/F12_STRESS_STRAIN_CONSISTENCY.md`** ← the consistency investigation
- `docs/F15_NONCONFORMANCE_RCCA_AF-DT-1000.md`
- `docs/ANSYS_GUIDE_F12_and_revD.md`, `docs/ROADMAP_portfolio_quality.md`
- `figures/make_figures.py`, `figures/README.md`, `figures/fig1_margin_vs_eD.svg`,
  `figures/fig3_plastic_strain_check.svg`
- `loads/LOAD_BASIS_AF-DT-1000_revA/revB/revC.md`
- `loads/AA-SM-009-005_AF-DT-1000_revD.xlsx` (uploaded by hand)

**Pending manual upload (binaries Claude cannot push):** `fig1/2/3 .png`, `fig2_fe_response.svg`,
and the Ansys result images on H: (`vonmises2p0`, `deform2p0`, `plastic2p0`, `mesh2p0`, `report2p0`).

## 10. Ansys archives on H: drive
| File | Contents |
|---|---|
| `seven_twnetyseven.wbpz` | e/D = 1.2 state |
| `ed1p8.wbpz` (8.29 MB) | e/D = 1.8, solved |
| `ed2p0.wbpz` (9.21 MB) | e/D = 2.0, solved — **the good copy** |
| `ed2p0final.wbpz` (1.62 MB) | e/D = 2.0 but almost certainly **no solution data** — the small size gives it away. Don't rely on it. |

Working project currently at `H:\Downloads\FinalNight.wbpj`.

## 11. PORTFOLIO TARGET
- **Now: ~90.** **Realistic ceiling: ~90-92.**
- **95+ is NOT achievable** without (a) a real stress engineer signing off, or (b) our own hardware
  test. Both ruled out by constraint. Don't promise 95.

## 12. WHERE WE ARE — next actions
**Project ~98% of F12-and-earlier scope.**

**The one remaining F12 item needs the paper, not more FEA.**
This handoff previously recorded that the source paper's shear-out and bearing curves cross at
**e/D = 1.5**. **Ours cross at e/D = 1.353**, using `Fbru = Ftu = 517 MPa`. A crossing at 1.5 would
require a bearing allowable near **606 MPa (1.17 × Ftu)** — plausible for a bearing allowable but
**not established**. Resolving this requires the Ekvall paper in hand. Do not assume it.

**Then:** F7 contact → F8/F9 fatigue & crack growth → F10 dynamics/buckling → F11 optimization →
F13 manufacturing/inspection → F14 digital thread → F16/F17 final package (formal stress report).

## 13. Still-open items
- [ ] Transverse allowable Ftux — currently = Ftu, needs proper basis
- [ ] A/B-basis material allowables (Ftu 71 ksi is representative only)
- [ ] Pin bending check at t/D = 1.25 (not covered by thin-lug method)
- [ ] FE cross-check of the +0.71 hand margin (Rev D pylon run — still not done)
- [ ] Onshape drawing out of date (g_y and t_lug changed); delete broken "Drawing 1"
- [ ] `build_revD.py` docstring says `t_web -> 1.250`; actual 2.500
- [ ] Plastic strain at e/D = 1.5 not captured
- [ ] Probe stress and plastic strain at a single common node (the colocation test)

## 14. Rev D pylon FE run — still queued
- Import `AF-DT-1000_fitting_revD.step`. **Verify mass = 7.65 kg first** (wrong mass = wrong file).
- Apply **BOTH** bore components: **317,840 N along Z** and **529,740 N along X**.
- Confirm bore scoping covers **BOTH half-cylinder faces** (area ≈ 6.078e-3 m², not 3.039e-3).
- Fixed support on flange underside. Capture von Mises, deformation, bearing stress,
  reaction (must balance 617,776 N).

## 15. Lessons — don't repeat

### Analysis
- Convergence needs **3+ points**. Two points misdiagnosed a singularity twice.
- **Check scoping before blaming the mesher.**
- **Declare axis mapping before resolving loads.**
- Verify curve/material selection in lug methods; wrong curve nearly doubled an allowable.
- **Bilinear hardening has no failure criterion.** It reports stresses the material could never
  reach. Always compute `required plastic strain = (peak vM - yield)/tangent modulus` and compare
  against elongation **before** quoting any peak stress. This is what caught the e/D = 1.0 result.
- **Near yield, comparing in strain space is ill-conditioned.** `(sigma - yield)/E_tan` is a small
  difference of large numbers; a 5 MPa stress error becomes a large apparent strain ratio. Compare
  in stress space.
- **Verify colocation before comparing two field maxima.** A relation that holds pointwise says
  nothing about global maxima of two separately post-processed fields.

### Geometry / CAD
- **Don't fight Discovery's GUI/scripting for geometry — build STEP externally and import.**
- Don't patch fillets onto an imported STEP — rebuild parametrically.
- `NearestToPointSelector` returns ONE edge — silently under-applied fillets.
- **Never text-parse a STEP for bounding boxes or volumes.** Circular arc crowns have no
  `CARTESIAN_POINT`, so the extremes are invisible. This produced a wrong 160.8 mm span for a part
  that is actually 201.0 mm. **Use the CAD kernel.**

### Ansys operation
- **After changing any unit dropdown, re-read the numeric field.** Ansys *converts* the stored
  value rather than relabelling it. Caused a 0.071 MPa modulus and a 6 µm global element size
  (which hung a mesh past 10 minutes). Two occurrences.
- **Scope by Named Selection worksheet rule, not by clicking.** Tail face:
  `Face / Location Y / Smallest`. Bore face: `Face / Radius / Smallest`. Both are
  geometry-independent across the sweep and survive geometry swaps with zero re-picking.
  **Validated by re-solve** — reproduced hand-picked results to every digit.
- After a geometry swap, stale scoping still displays as "1 Face". **Real tells:** magenta
  "Old Geometry Tessellation" overlay, and Matched Entities = 0 in the scoping worksheet.
- **Verify every typed field by zooming in before proceeding.** Single-click selects the row, not
  the edit box — edits silently fail to commit. This invalidated a full mesh/solve cycle once.
- Material assignment does **not** carry across a geometry swap. Re-assign, then check mass.
- **Mass/volume gate every import.** Wrong mass = wrong file.

### Session management
- **The VDI wipes local disk at logout.** Two sessions were lost.
- `File > Archive` gives a single `.wbpz`; a bare `.wbpj` can be separated from its `_files` folder.
- **Give every archive a distinct name** — one overwrote its predecessor.
- **Copy the archive to H: or Drive immediately**, not just C:.
- A small archive (1-2 MB vs 8-9 MB) means **the results were not included**.
- Confirm only **one Workbench instance** is running. A stale lock and a second instance were found
  open simultaneously; two instances on one project risk corruption.
