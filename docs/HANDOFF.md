# AeroFrame-DT — Handoff (current as of this session)

## 0. Who I am / how to work with me
- I'm **Ruby** (GitHub: **XpiredRuby**). Texas A&M aerospace senior. Portfolio project, not a pro dev.
- **Talk in short, plain words. Caveman-brief. No yapping.** I'm low on credits.
- **Only tell me what *I* need to do.** If it's GitHub or software, YOU do it — you have write access.
- Only ask me for: Ansys/FEA runs, browser logins, physical file moves.
- **Don't ask me to pick options.** Decide yourself using good engineering + job-market reasoning.
- **Be honest. Never guess numbers or citations.** Verify or say you can't. Past chats lost hours to confident wrong guesses.
- After each milestone, give **% complete of whole project**.
- **Scope cuts unwelcome.** Don't shrink the project.

## 1. What the project IS
**AeroFrame-DT** = rigorous engineering **substantiation** of ONE small critical aircraft part —
a **forward pylon-to-wingbox attachment fitting (AF-DT-1000)** on an MD-11-class aircraft — done
like a real aerospace stress engineer, with a full digital-thread evidence trail.

- **Thesis: depth over breadth on ONE fitting. Do NOT add more parts.**
  (I asked about breaking up an MD-11 CAD into many parts. Answer: no — job postings reward
  substantiation depth, test correlation, and documentation, NOT part count.)
- Claim boundary: **educational / representative / portfolio only. Non-OEM, non-certified.
  All numbers `SYNTHETIC_TEST_ONLY`.**

## 2. Repo
- **github.com/XpiredRuby/aeroframe-dt**, owner `XpiredRuby`, repo `aeroframe-dt`, branch `main`.
- **GitHub connector HAS WRITE ACCESS.** Claude commits directly via `create_or_update_file`
  (needs correct blob SHA when overwriting). `push_files` returns 403 — use single-file calls.
- **Binary files (.xlsx, .step) CANNOT be pushed** by Claude (tool base64-encodes text only).
  Those I upload by hand.

## 3. Environment
- **Ansys Discovery / Mechanical 2025 R2** on **TAMU virtual desktop (VDI)** — full license, no node cap.
- Files move: my PC → Google Drive folder **AeroFrame-DT** (xpiredruby@gmail.com) → VDI browser.
- Hand calcs: **Abbott Aerospace** sheets (AA-SM-009-002/-005), digitizing USAF AFFDL-TR-69-42 /
  NASA TM X-73305 (Melcon-Hoblit lug method).
- I also drive Ansys via **Claude for Chrome extension** (use Sonnet there to save credits).

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
Lug axis = CAD Z. Bore axis = CAD Y. Forced by the flange lying on the wingbox — not a free choice.

## 5. LOADS — Rev C
- 6000 kg propulsion, 9g fwd. LC-02 governs.
- F_x = 529,740 N fwd; CG offset → couple → R_z = 317,840 N vertical.
- **Resultant 617,776 N at 59.04° off the lug axis. TRANSVERSE-DOMINANT.**
- (Rev B said 30.96° — that measured from aircraft X, wrong reference. Rev C corrected it.)
- In lb: P_axial = 71,453 lb (Z), P_transverse = 119,090 lb (X).

## 6. RESULT — margin CLOSED
**M.S. = +0.71** (was provisional +0.11). Three open items resolved:
1. **A₁–A₄ were a guess (1.5 in²).** Real value = `(e−D/2)·t` = **3.75 in²** each for a
   rectangular lug. Aav = 3.75, Aav/Abr = 0.75.
2. **Curve 8 was WRONG material** (stainless/thick forging). **Curve 5** is 7075 panel.
   Transverse Ktru: 0.387 → **0.7875**. Biggest correction.
3. **AA-SM-009-002 vs -005 Kt conflict wasn't real** — -005 applies the 1.15 fitting factor for
   the combined oblique case; -002 is pure axial.

Factors: Kt=0.950, Ktru=0.7875, Kbr=1.240.
Allowables: P'bru=440,200 lb; P'tu=337,250 lb; P'tru=279,562 lb.
Ra=0.2436, Rtr=0.4899 → **MS=+0.710**.
**Method validated line-for-line against AA-SM-009-005's own worked example** before use.
Caveat: Ftux set = Ftu (no separate transverse allowable). At −10% Ftux, MS ≈ +0.5. Still passes.

## 7. F12 CORRELATION — Piece 1 DONE
Anchor: **Ekvall, J.C., "Static Strength Analysis of Pin-Loaded Lugs," J. Aircraft 23(5), 1986,
pp. 438-443** (Lockheed). **243 lug tests, 24 materials, predicted/test 0.85–1.19, mean 1.003.**
Propagated through our +0.71: worst case **+0.44**, mean +0.70, best +1.01. **Positive across the
whole validated band.**

**Honesty note recorded:** the IAF paper (Shiroky et al., "An Innovative Method for Lug Strength
Analysis") has a unit error in its headline test ("3850 lbf" vs "3900 kgf" — factor 2.2 apart;
the ~1% claim only holds if same unit) and its stated e/D=1.26 doesn't follow from D=15.88/e=40mm.
So it is NOT the anchor. Only its self-consistent nominal parametric case is used as FE geometry.

## 8. F15 RCCA — DONE
Representative MRB/nonconformance: **mis-drilled bore, edge distance 2.500 → 1.900 in** (60×
position tolerance). Margin **+0.71 → +0.22**. At Ekvall's worst ratio (1.19) it's only **+0.025**
— so disposition = **REWORK**, not use-as-is. Full 8D/5-Why: root cause = datum not propagated
from drawing to shop traveller (same "undeclared reference" class as the axis-mapping bug).

## 9. Committed files (all on `main`)
- `cad/PARAMETER_SCHEMA.csv` (rev D)
- `cad/build_revD.py`
- `docs/DECISIONS_AF-DT-1000_revA.md`, `docs/DECISIONS_AF-DT-1000_revD.md`
- `docs/F5_F6_STATIC_RESULTS_AF-DT-1000_revA.md`, `docs/F5_STATIC_RESULTS_AF-DT-1000_revB.md`
- `docs/F5_STATIC_RESULTS_AF-DT-1000_revD.md`  ← the +0.71 result
- `docs/F12_CORRELATION_AF-DT-1000.md`
- `docs/F15_NONCONFORMANCE_RCCA_AF-DT-1000.md`
- `docs/ANSYS_GUIDE_F12_and_revD.md`
- `docs/ROADMAP_portfolio_quality.md`
- `loads/LOAD_BASIS_AF-DT-1000_revA/revB/revC.md`
- `loads/AA-SM-009-005_AF-DT-1000_revD.xlsx` (I uploaded by hand)

## 10. PORTFOLIO TARGET
Assessed vs full-time entry structural/stress roles incl. interns converting:
- **Now: ~72–89.** **Realistic ceiling: ~90.**
- **95+ is NOT achievable** without (a) a real stress engineer signing off, or (b) our own hardware
  test. Both ruled out by constraint. Don't promise 95.
- Path to ~90: close margin (DONE) → F12 (Piece 1 DONE) → F15 (DONE) → formal stress report +
  A/B-basis allowables → visible self-checking (hand vs FEA vs 2nd method, convergence, uncertainty).

## 11. WHERE WE ARE RIGHT NOW — the active blocker
**F12 Piece 2 = the Ansys run.** Everything software-side is done. Only the FEA remains.

### The lug to model (published correlation specimen)
Straight 7075-T651 lug, **D = 26.8 mm, t = 25 mm**, e/D swept 1.0→2.0,
`e = (e/D)·D`, `w = 2·(e/D)·D`. Axial load **64,000 lbf = 284,686 N**.
| e/D | D | w | e |
|---|---|---|---|
| 1.0 | 26.8 | 53.6 | 26.8 |
| 1.2 | 26.8 | 64.3 | 32.2 |
| **1.5** | 26.8 | **80.4** | **40.2** |
| 1.8 | 26.8 | 96.5 | 48.2 |
| 2.0 | 26.8 | 107.2 | 53.6 |

**Material card:** E = **71000 MPa** (the paper prints 1.03e6 psi = 7.1 GPa — that's a TYPO,
aluminum is 10.3e6 psi = 71 GPa; use 71 GPa), ν 0.33, Bilinear Isotropic Hardening:
yield **469 MPa**, tangent modulus **760 MPa**. Allowables for hand check: Ftu 517 MPa,
Fty/Fcy 469 MPa, Fsu 303 MPa.

### CAD lesson learned (do not repeat)
Tried to script the lug in Discovery. **Three script versions all failed at the hole cut**
(`CreatedFaces` attribute error, then a silent hang in the face-area loop, then no hole).
Discovery quirks found: click-drag does NOT survive the VDI stream; Shift/capitals/parens can't
be typed by the extension; the circle field takes DIAMETER and eats the first character;
Pull "Up To" works, dragging doesn't.
**SOLUTION ADOPTED: skip CAD entirely — import a ready-made STEP.**
Claude built `lug_eD_1p5.step` with cadquery (volume 372,567 mm³). I import that.

### Immediate next action
1. Put `lug_eD_1p5.step` in Google Drive → open on VDI.
2. Import into Workbench Static Structural.
3. Material 7075-T651 as above.
4. Mesh 2 mm on hole face, 6 mm global.
5. **Bearing Load 284,686 N** on hole inner face, along shank axis, pulling head away from tail.
6. **Fixed Support** on the flat bottom end face of the shank.
7. Solve. Results: von Mises, Total Deformation, Force Reaction probe on the support.
8. Report: **peak von Mises (MPa) + location, reaction force (~284,686 N), max deformation (mm).**
9. Then repeat for other e/D values, and do a **3-point mesh convergence** at e/D=1.5
   (4 mm / 2 mm / 1 mm hole-face element size).
10. Compare margin-vs-e/D to the paper's published curves. Sanity check: their shear-out and
    bearing curves **cross at e/D = 1.5**.

### Also queued (separate model, same VDI session)
**Rev D pylon FE run** to close the F5 FE cross-check:
- Import `AF-DT-1000_fitting_revD.step`. **Verify mass = 7.65 kg first** (wrong mass = wrong file).
- Apply **BOTH** components on the bore: **317,840 N along Z** and **529,740 N along X**.
- Confirm bore scoping covers **BOTH half-cylinder faces** (area ≈ 6.078e-3 m², not 3.039e-3) —
  a prior run grabbed one face only and gave wild results.
- Fixed support on flange underside. Capture von Mises, true-scale deformation, bearing stress,
  reaction (must balance 617,776 N).

## 12. Remaining phases after F12
F7 contact → F8/F9 fatigue & crack growth → F10 dynamics/buckling → F11 optimization →
F13 manufacturing/inspection → F14 digital thread → F16/F17 final package (formal stress report).

## 13. Still-open items
- [ ] Transverse allowable Ftux — currently = Ftu, needs proper basis
- [ ] A/B-basis material allowables (Ftu 71 ksi is representative only)
- [ ] Pin bending check at t/D = 1.25 (not covered by thin-lug method)
- [ ] FE cross-check of the +0.71 hand margin
- [ ] Onshape drawing out of date (g_y and t_lug changed); delete broken "Drawing 1"
- [ ] `build_revD.py` docstring says `t_web -> 1.250`; actual 2.500

## 14. Lessons — don't repeat
- Convergence needs **3+ points**. Two points misdiagnosed a singularity twice.
- **Check scoping before blaming the mesher** (the half-bore-face bug).
- **Declare axis mapping before resolving loads.** Cost a full rework cycle.
- `NearestToPointSelector` returns ONE edge — silently under-applied fillets.
- Don't patch fillets onto an imported STEP — rebuild parametrically.
- **Don't fight Discovery's GUI/scripting for geometry — build STEP externally and import.**
- Verify curve/material selection in lug methods; wrong curve nearly doubled an allowable.
