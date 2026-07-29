# AeroFrame-DT — Handoff (analysis phase complete)

## 0. Who I am / how to work with me
- I'm **Ruby** (GitHub: **XpiredRuby**). Texas A&M aerospace senior. Portfolio project, not a pro dev.
- **Talk in short, plain words. Caveman-brief. No yapping.** I'm low on credits.
- **Only tell me what *I* need to do.** If it's GitHub or software, YOU do it — you have write access.
- Only ask me for: Ansys/FEA runs, browser logins, physical file moves.
- **Don't ask me to pick options.** Decide yourself using good engineering + job-market reasoning.
- **Be honest. Never guess numbers or citations.** Verify or say you can't.
- After each milestone, give **% complete of whole project**.
- **Scope cuts unwelcome.** Don't shrink the project.
- **Any name you ask me to type must be lowercase alphanumeric only.** The VDI cannot produce
  Shift-modified characters. This has cost time three times.

## 1. What the project IS
**AeroFrame-DT** = rigorous engineering **substantiation** of ONE small critical aircraft part —
a **forward pylon-to-wingbox attachment fitting (AF-DT-1000)** on an MD-11-class aircraft — done
like a real aerospace stress engineer, with a full digital-thread evidence trail.

- **Thesis: depth over breadth on ONE fitting. Do NOT add more parts.**
- Claim boundary: **educational / representative / portfolio only. Non-OEM, non-certified.
  All numbers `SYNTHETIC_TEST_ONLY`.**

## 2. Repo
- **github.com/XpiredRuby/aeroframe-dt**, branch `main`.
- **GitHub connector HAS WRITE ACCESS.** Claude commits via `create_or_update_file`
  (needs the blob SHA when overwriting). `push_files` returns 403 — use single-file calls.
- **Binaries (.xlsx, .step, .png) CANNOT be pushed** by Claude. I upload those.
  **SVG is text and CAN be pushed.**

## 3. Environment
- **Ansys Mechanical 2025 R2** on **TAMU VDI** — full license.
- Files: my PC → Google Drive **AeroFrame-DT** → VDI. Also H: drive (persists across logout).
- Hand calcs: **Abbott Aerospace** AA-SM-009-002/-005, digitizing USAF AFFDL-TR-69-42 /
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

Volume 166.19 in³, **mass 7.65 kg**. Material 7075-T7351
(E=71.7 GPa, ν=0.33, ρ=2810, Ftu≈71 ksi representative).
Ratios: **e/D=1.25, W/D=2.00, t/D=1.25**. Abr=5.00 in², Atn=5.00 in², Aav=3.75 in².

**Axis mapping FROZEN (identity):** CAD X→aircraft X (fwd), Y→Y (span), Z→Z (up).
Lug axis = CAD Z. Bore axis = CAD Y.

### STEP build chain and unit trap
The Rev D STEP is not in the repo (binary). Rebuild with:

    python cad/build_revD.py          # writes ..._revD.step, in INCH numbers
    python cad/build_revD_to_mm.py    # rescales x25.4, writes ..._revD_mm.step

**Always use the `_mm` file.** cadquery declares millimetres regardless of the numbers fed to it,
so the raw export is a part 25.4x too small and imports silently wrong.

Verified: **1 continuous bore face at r = 25.40 mm**, 8 fastener holes r = 3.175 mm, 8 blends
r = 12.70 mm. Bore area **1.0134e-2 m²**. Flange underside **6.1682e-2 m²**.

## 5. LOADS — Rev C
- 6000 kg propulsion, 9g fwd. LC-02 governs.
- F_x = 529,740 N fwd; CG offset → couple → R_z = 317,840 N vertical.
- **Resultant 617,776 N at 59.04° off the lug axis. TRANSVERSE-DOMINANT.**
- In lb: P_axial = 71,453 lb (Z), P_transverse = 119,090 lb (X).

## 6. RESULT — margin, and its two live caveats
**M.S. = +0.710.** Kt=0.950, Ktru=0.7875, Kbr=1.240.
Allowables: P'bru=440,200 lb; P'tu=337,250 lb; P'tru=279,562 lb. Ra=0.2436, Rtr=0.4899.
**Method validated line-for-line against AA-SM-009-005's worked example** before use.

**Reconstructed independently on a stress basis** (`docs/F5_MARGIN_CROSSCHECK.md`): converting
allowable loads to allowable stresses on Abr and Atn with the 1.15 fitting factor gives
Ra = 0.2437, Rtr = 0.4899, **MS = +0.7104** — agreement to 0.06%.

### Caveat 1 — Ftux basis (moderate)
Ftux set = Ftu, no separate transverse allowable. At −10% Ftux, MS ≈ +0.5. Still passes.

### Caveat 2 — thick-lug / pin bending (LARGE, see `docs/F6_PIN_BENDING_THICK_LUG.md`)
The Melcon-Hoblit method is a **thin-lug** method assuming uniform bearing through thickness.
**This lug is at t/D = 1.25**, more than double the ~0.6 threshold where pin bending normally
warrants assessment.

| t_eff / t | MS |
|---|---|
| 1.00 | +0.710 |
| 0.80 | +0.368 |
| 0.70 | +0.197 |
| **0.585** | **0.000** |
| 0.50 | −0.145 |

**The margin reaches zero if bearing concentrates into 58.5% of the thickness.** This is a steeper
sensitivity than Ftux. No claim is made about the actual `t_eff` — establishing it needs a traceable
thick-lug correction or F7 contact FE. **This makes F7 critical path, not polish.**

## 7. F12 CORRELATION — COMPLETE
Anchor: **Ekvall, J.C., J. Aircraft 23(5), 1986, pp. 438-443.** 243 lug tests, 24 materials,
predicted/test 0.85–1.19, mean 1.003. Propagated through +0.71: **+0.44 worst, +0.70 mean, +1.01 best**.

The IAF paper (Shiroky et al.) has a unit error in its headline test and an inconsistent e/D.
**NOT the anchor** — only its self-consistent nominal case used as FE geometry.

FE sweep, straight 7075-T651 lug, D=26.8, t=25, P=284,686 N. Record: `docs/F12_FE_RESULTS_AF-DT-1000.md`.

| e/D | Peak vM (MPa) | Deformation (mm) | Plastic strain | Reaction Y (N) |
|---|---|---|---|---|
| 1.0 | 750.23 (discarded) | 7.655 | 0.37211 | -284,690 |
| 1.2 | 521.47 | 0.896 | 0.03107 | -284,690 |
| 1.5 | 490.45 | 0.632 | not captured | -284,690 |
| 1.8 | 506.34 | 0.526 | 0.00888 | -284,690 |
| 2.0 | 503.49 | 0.4817 | 0.00795 | -284,690 |

- **Shear-out governs below e/D = 1.353, bearing above.** Bearing margin flat at +0.216.
- **Zero margin at e/D = 1.201**, confirmed by the e/D = 1.2 run (measured −0.002).
- **e/D = 1.0 fails by shear-out.** Its 750 MPa peak needs 37% plastic strain — discarded.
- **Elastic scaling law** holds to 1.7% at e/D ≥ 1.5.
- **Singularity ruled out** by 3-point convergence.
- `w = 2e` makes net-section and shear-out areas **algebraically identical**. Net section can never
  govern in that sweep — a property of the parametrisation, not a general lug result.

**Peak stress not quoted for e/D ≥ 1.2.** See `docs/F12_STRESS_STRAIN_CONSISTENCY.md` — one
hypothesis rejected, one half-supported, and a flaw in the check itself found afterwards.
Closed as bounded: true peak at e/D=2.0 between 469 and 503 MPa.

## 8. F5 FE — Rev D pylon run — COMPLETE
`docs/F5_FE_REVD_LINEAR_ELASTIC.md`. **Linear elastic by design** — no verified yield or hardening
data for 7075-T7351 exists and must not be invented.

Converged, 8 mm global / 1 mm bore, 152,951 nodes: peak **1194.1 MPa** at the bore edge,
deformation **3.5686 mm**, reaction **−529,770 / ~0 / −317,860 N**.

Convergence 4/2/1 mm: 1209.4 → 1187.1 → 1194.1 MPa, non-monotonic within ±0.95%, **singularity
ruled out**. Reaction error fell 0.074% → 0.022% → **0.006%**, confirming faceting as predicted.

**This run does NOT validate the +0.710 and cannot.** Empirical allowables already absorb the
concentration and local plasticity; peak elastic stress is a different quantity. What it did
establish: the load reaches the assumed path, **the bore is critical** (not the blade root), no
secondary critical location, and a verified elastic baseline for F7.

Nominal: bearing 191.5 MPa, net section 98.5 MPa — both well inside Ftu ≈ 489 MPa.

## 9. F6 PIN BENDING — COMPLETE (`docs/F6_PIN_BENDING_THICK_LUG.md`)
- **Pin bending governs the pin at ~780 MPa**, 5.1x the 152 MPa double-shear stress.
- **High-strength steel pin required.** 155–200 ksi steels give MS +1.05 to +1.72.
  7075-T6 gives only +0.10 and goes negative for thicker clevis ears. **Aluminium not viable.**
- Bending stress is **49% higher** if clevis ears are as thick as the lug. **The clevis is undefined.**
- Drives Caveat 2 in §6.

## 10. F15 RCCA — DONE
Mis-drilled bore, edge distance 2.500 → 1.900 in. Margin **+0.71 → +0.22**. At Ekvall's worst ratio
it is only **+0.025** — disposition **REWORK**, not use-as-is. Root cause: datum not propagated from
drawing to shop traveller.

## 11. Committed files
- `cad/PARAMETER_SCHEMA.csv`, `cad/build_revD.py`, `cad/build_revD_to_mm.py`, `cad/build_lug_sweep.py`
- `docs/F5_F6_STATIC_RESULTS_AF-DT-1000_revA/B/D.md` ← the +0.71 result
- `docs/F5_FE_REVD_LINEAR_ELASTIC.md`, `docs/F5_MARGIN_CROSSCHECK.md`
- **`docs/F6_PIN_BENDING_THICK_LUG.md`**
- `docs/F12_CORRELATION_AF-DT-1000.md`, `docs/F12_FE_RESULTS_AF-DT-1000.md`,
  `docs/F12_STRESS_STRAIN_CONSISTENCY.md`
- `docs/F15_NONCONFORMANCE_RCCA_AF-DT-1000.md`
- `docs/DECISIONS_*`, `docs/ANSYS_GUIDE_F12_and_revD.md`, `docs/ROADMAP_portfolio_quality.md`
- `figures/make_figures.py`, `figures/README.md`, `fig1_margin_vs_eD.svg`, `fig3_plastic_strain_check.svg`
- `loads/LOAD_BASIS_AF-DT-1000_revA/B/C.md`, `loads/AA-SM-009-005_AF-DT-1000_revD.xlsx`

**Pending manual upload (binaries):** `fig1/2/3 .png`, `fig2_fe_response.svg`, Ansys result images
on H: (`vonmises2p0`, `deform2p0`, `plastic2p0`, `mesh2p0`, `report2p0`).

## 12. Ansys archives on H:
| File | Contents |
|---|---|
| `ed1p8.wbpz` (8.29 MB) | F12 lug e/D = 1.8, solved |
| `ed2p0.wbpz` (9.21 MB) | F12 lug e/D = 2.0, solved |
| `ed2p0final.wbpz` (1.62 MB) | **no solution data** — size gives it away |
| `revdrun.wbpz` (8.85 MB) | Rev D pylon, 4 mm bore mesh |
| **`revdconverged.wbpz` (45.5 MB)** | **Rev D pylon, 1 mm converged — the good copy, F7 starts here** |

## 13. PORTFOLIO TARGET
- **Now: ~90.** **Realistic ceiling: ~90-92.**
- **95+ is NOT achievable** without a real stress engineer signing off or our own hardware test.
  Both ruled out by constraint. Don't promise 95.

## 14. WHERE WE ARE
**The analysis phase is complete.** Hand margin closed and independently reconstructed, correlated
to 243 published tests, FE model verified and converged, pin bending checked, RCCA done.

**F7 contact is now critical path, not polish.** §6 Caveat 2 means the headline +0.710 is not
substantiated against the thick-lug effect. F7 answers it, starting from `revdconverged.wbpz` with
the pin modelled as a separate body in contact.

**Then:** F8/F9 fatigue & crack growth → F10 dynamics/buckling → F11 optimization →
F13 manufacturing/inspection → F14 digital thread → F16/F17 final package.

## 15. Still-open
**Needs F7 contact FE**
- [ ] `t_eff / t` — determines whether +0.710 survives. Highest priority.
- [ ] Chamfer at the Rev D bore mouth (none modelled; a real part has one)

**Needs external sources**
- [ ] Ekvall paper — our margin curves cross at **e/D = 1.353**, an earlier note claimed the paper
      says 1.5. A crossing at 1.5 implies Fbru ≈ 606 MPa (1.17 × Ftu). **Do not assume it.**
- [ ] Ftux proper basis; A/B-basis allowables (MMPDS)
- [ ] Verify the 1.5 plastic bending factor against a citable source

**Needs a decision**
- [ ] Clevis geometry of the mating fitting (AF-DT-2000) — undefined, drives pin bending
- [ ] Pin material and size selection

**Housekeeping**
- [ ] Onshape drawing out of date (g_y and t_lug changed); delete broken "Drawing 1"
- [ ] Plastic strain at e/D = 1.5 not captured
- [ ] F12 colocation test — probe stress and plastic strain at one common node

## 16. Lessons — don't repeat

### Analysis
- Convergence needs **3+ points**. Two points misdiagnosed a singularity twice.
- **Check scoping before blaming the mesher.**
- **Declare axis mapping before resolving loads.**
- Verify curve/material selection in lug methods; a wrong curve nearly doubled an allowable.
- **Bilinear hardening has no failure criterion.** Compute
  `required plastic strain = (peak vM − yield)/tangent modulus` and compare against elongation
  **before** quoting any peak stress.
- **Near yield, comparing in strain space is ill-conditioned.** Compare in stress space.
- **Verify colocation before comparing two field maxima.**
- **Never compare a linear elastic peak stress against an allowable-based margin.** Convert both
  sides to the same basis. This was set up wrongly once and corrected after the run.
- **Beam theory does not apply below about L/h = 3.** A cantilever estimate on the Rev D blade
  (L/h = 1.4) predicted the wrong critical location and understated deflection 3x.
- **Check whether a method's assumptions hold for the actual geometry.** The thin-lug method was
  used at t/D = 1.25 for months before anyone asked what that did to the margin. It is the largest
  caveat on the headline result.

### Geometry / CAD
- **Build STEP externally and import — don't fight Discovery's GUI/scripting.**
- Rebuild parametrically rather than patching fillets onto an imported STEP.
- `NearestToPointSelector` returns ONE edge — silently under-applied fillets.
- **Never text-parse a STEP for bounding boxes or volumes.** Arc crowns have no `CARTESIAN_POINT`.
  This gave a wrong 160.8 mm span for a part that is 201.0 mm. **Use the CAD kernel.**
- **Check the unit declaration on every generated STEP.** cadquery writes millimetres regardless.
- **Re-derive every geometry gate when a parameter changes.** The bore-area gate sat at the Rev A
  value long after t_lug changed. A stale gate rejects correct work.

### Ansys operation
- **After changing any unit dropdown, re-read the numeric field.** Ansys *converts* rather than
  relabels. Caused a 0.071 MPa modulus, a 6 µm element size, and a 175 lb/ft³ density. Three times.
- **Scope by Named Selection worksheet rule, not by clicking.**
  F12 lug: tail `Location Y / Smallest`, bore `Radius / Smallest`.
  Rev D pylon: bore `Radius / Equal / 0.0254`, flange `Location Z / Smallest`.
  **Do not use Smallest for the Rev D bore** — blends and fastener holes are smaller.
- Stale scoping still displays "1 Face". **Tells:** magenta "Old Geometry Tessellation", and
  Matched Entities = 0.
- **Verify every typed field by zooming in.** Single-click selects the row, not the edit box.
- Material assignment does **not** carry across a geometry swap.
- **Mass/volume gate every import.**
- Kernel-to-kernel translation gives ~0.01% differences. Judge by the gap to the next candidate.

### Session management
- **The VDI wipes local disk at logout.** Two sessions lost.
- `File > Archive` gives a single `.wbpz`. **Distinct name each time** — one overwrote another.
- **Copy to H: immediately.** A small archive means results were not included.
- Confirm only **one Workbench instance** is running.
