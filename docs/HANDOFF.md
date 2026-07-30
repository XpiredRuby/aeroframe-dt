# AeroFrame-DT — Handoff (analysis phase complete, Ansys work finished)

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
  Shift-modified characters.

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
- **Binaries (.xlsx, .step, .png, .wbpz) CANNOT be pushed** by Claude. I upload those.
  **SVG is text and CAN be pushed.**

## 3. Environment
- **Ansys Mechanical 2025 R2** on **TAMU VDI**. **No further Ansys work is required.**
- Files: my PC -> Google Drive **AeroFrame-DT** -> VDI. Also H: drive (persists across logout).
- Hand calcs: **Abbott Aerospace** AA-SM-009-002/-005, digitizing USAF AFFDL-TR-69-42 /
  NASA TM X-73305 (Melcon-Hoblit lug method).

## 4. GEOMETRY — Rev D (frozen)
| Param | Rev A | **Rev D** |
|---|---|---|
| d_pin | 2.000 | 2.000 |
| t_lug | 1.500 | **2.500** |
| w_lug | 4.000 | 4.000 |
| e_center | 2.500 | 2.500 |
| t_flange | 1.000 | 1.000 |
| t_web | 0.750 | **2.500** |
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
STEP files are not in the repo (binary). Rebuild with:

    python cad/build_revD.py          # inch numbers
    python cad/build_revD_to_mm.py    # rescales x25.4 -> use this one
    python cad/build_f7.py            # two-body lug + pin, already in mm

**Always use the `_mm` file.** cadquery declares millimetres regardless of the numbers fed to it.

Verified: **1 continuous bore face at r = 25.40 mm**, 8 fastener holes r = 3.175 mm, 8 blends
r = 12.70 mm. Bore area **1.0134e-2 m²**. Flange underside **6.1682e-2 m²**.

## 5. LOADS — Rev C
- 6000 kg propulsion, 9g fwd. LC-02 governs.
- F_x = 529,740 N fwd; CG offset → couple → R_z = 317,840 N vertical.
- **Resultant 617,776 N at 59.04° off the lug axis. TRANSVERSE-DOMINANT.**
- In lb: P_axial = 71,453 lb (Z), P_transverse = 119,090 lb (X).

## 6. MARGIN — see `docs/MARGIN_SUMMARY.md` for the authoritative figure

**Governing margin: `MS = +0.165`** (thick-lug corrected, converged).

| Stage | MS |
|---|---|
| Melcon-Hoblit thin-lug method | +0.710 |
| Reconstructed on a stress basis (0.06% agreement) | +0.7104 |
| **Corrected for thick-lug bearing distribution** | **+0.165** |

**Any document quoting +0.710 without qualification is quoting the uncorrected thin-lug value.**
The thin-lug method was **optimistic by a factor of 4.3 on margin** at t/D = 1.25.

Sensitivities on the corrected value:

| Case | MS |
|---|---|
| Baseline | +0.165 |
| Ftux -10% | +0.074 |
| Ekvall mean, r = 1.003 | +0.161 |
| **Ekvall worst, r = 1.19** | **-0.021** |
| Zero-margin threshold | at t_eff/t = 0.585 |

**The worst-case Ekvall stack is marginally negative**, with a possible double-counting caveat —
if Ekvall's 243 test specimens included thick lugs, the effect is partly inside his scatter band
already. Unresolvable without the paper.

## 7. F7 CONTACT — COMPLETE (`docs/F7_CONTACT_THICK_LUG.md`)
Two-body lug + steel pin, Frictional contact mu = 0.1, 0.0127 mm radial clearance.

**Ratio method:** `t_eff/t = p_max(stiff pin) / p_max(real pin)`. A 20x-stiffness pin cannot bend,
so through-thickness concentration vanishes while clearance effects and the contact-edge
singularity remain identical and cancel.

| Bore mesh | Nodes | p real | p stiff | t_eff/t | MS |
|---|---|---|---|---|---|
| 3.00 mm | 21,744 | 1265.1 | 938.6 | 0.7419 | +0.269 |
| 1.50 mm | 58,780 | 2146.8 | 1432.0 | 0.6670 | +0.141 |
| **0.75 mm** | **203,472** | **2955.9** | **2012.7** | **0.6809** | **+0.165** |

**Absolute contact pressure diverges 134% and never converges** — a genuine contact-edge
singularity. **The ratio moves 8.2% and converges.** This validates the method by evidence rather
than argument.

**Two points would have given the wrong answer.** The 3.0 -> 1.5 mm trend extrapolated to
t_eff/t ~ 0.60 and MS ~ +0.03. The third point showed it rebounding. Third instance in this project
where a two-point study misled, and the first where it would have changed the engineering answer.

## 8. F6 PIN BENDING — COMPLETE (`docs/F6_PIN_BENDING_THICK_LUG.md`)
- **Pin bending governs the pin at ~780 MPa**, 5.1x the 152 MPa double-shear stress.
- **High-strength steel pin required.** 155-200 ksi steels give MS +1.05 to +1.72.
  7075-T6 gives only +0.10 and goes negative for thicker clevis ears. **Aluminium not viable.**
- Bending stress is **49% higher** if clevis ears are as thick as the lug. **The clevis is undefined.**

## 9. F5 FE — Rev D linear elastic — COMPLETE (`docs/F5_FE_REVD_LINEAR_ELASTIC.md`)
Converged 8 mm global / 1 mm bore, 152,951 nodes: peak **1194.1 MPa** at the bore edge,
deformation **3.5686 mm**, reaction **-529,770 / ~0 / -317,860 N**.
Reaction error fell 0.074% -> 0.022% -> **0.006%** under refinement, confirming faceting as
predicted before the study.

**Does NOT validate the margin and cannot** — peak elastic stress is not comparable to an
allowable-based margin. What it established: the load reaches the assumed path, **the bore is
critical** (not the blade root), and no secondary critical location exists.

## 10. F12 CORRELATION — COMPLETE
Anchor: **Ekvall, J.C., J. Aircraft 23(5), 1986, pp. 438-443.** 243 lug tests, 24 materials,
predicted/test 0.85–1.19, mean 1.003.

The IAF paper (Shiroky et al.) has a unit error in its headline test and an inconsistent e/D.
**NOT the anchor.**

FE sweep, straight 7075-T651 lug, D=26.8, t=25, P=284,686 N:

| e/D | Peak vM (MPa) | Deformation (mm) | Plastic strain |
|---|---|---|---|
| 1.0 | 750.23 (discarded) | 7.655 | 0.37211 |
| 1.2 | 521.47 | 0.896 | 0.03107 |
| 1.5 | 490.45 | 0.632 | not captured |
| 1.8 | 506.34 | 0.526 | 0.00888 |
| 2.0 | 503.49 | 0.4817 | 0.00795 |

- **Shear-out governs below e/D = 1.353, bearing above.** Bearing margin flat at +0.216.
- **Zero margin at e/D = 1.201**, confirmed by measurement (-0.002).
- **e/D = 1.0 fails by shear-out.** Its 750 MPa peak needs 37% plastic strain — discarded.
- **Elastic scaling law** holds to 1.7% at e/D >= 1.5.
- `w = 2e` makes net-section and shear-out areas **algebraically identical** in that sweep.

Peak stress not quoted for e/D >= 1.2 — see `docs/F12_STRESS_STRAIN_CONSISTENCY.md`.

## 11. F15 RCCA — DISPOSITION UNCHANGED, SEVERITY WORSE
Mis-drilled bore, edge distance 2.500 -> 1.900 in. Originally recorded as +0.710 -> +0.220.
**Under the thick-lug correction this becomes approximately -0.169** — clearly negative before any
Ekvall scatter is applied.

**REWORK disposition stands and is strengthened.** It is no longer a marginal call.
The figure is approximate — scaled rather than re-derived. Exact recomputation at e = 1.900 in is
an open item.

## 12. Committed files
- `cad/PARAMETER_SCHEMA.csv`, `build_revD.py`, `build_revD_to_mm.py`, `build_lug_sweep.py`, `build_f7.py`
- **`docs/MARGIN_SUMMARY.md`** <- authoritative margin figure, read this first
- `docs/F5_F6_STATIC_RESULTS_AF-DT-1000_revA/B/D.md`
- `docs/F5_FE_REVD_LINEAR_ELASTIC.md`, `docs/F5_MARGIN_CROSSCHECK.md`
- `docs/F6_PIN_BENDING_THICK_LUG.md`, **`docs/F7_CONTACT_THICK_LUG.md`**
- `docs/F12_CORRELATION_AF-DT-1000.md`, `F12_FE_RESULTS_AF-DT-1000.md`,
  `F12_STRESS_STRAIN_CONSISTENCY.md`
- `docs/F15_NONCONFORMANCE_RCCA_AF-DT-1000.md`
- `figures/make_figures.py`, `README.md`, `fig1_margin_vs_eD.svg`, `fig3_plastic_strain_check.svg`
- `loads/LOAD_BASIS_AF-DT-1000_revA/B/C.md`, `loads/AA-SM-009-005_AF-DT-1000_revD.xlsx`

**Pending manual upload (binaries):** figure PNGs, `fig2_fe_response.svg`, Ansys result images.

## 13. Ansys archives on H:
| File | Size | Contents |
|---|---|---|
| `ed2p0.wbpz` | 9.21 MB | F12 lug e/D = 2.0, solved |
| `revdconverged.wbpz` | 45.5 MB | Rev D linear elastic, 1 mm converged |
| `f7contact.wbpz` | 20.3 MB | F7 contact, 3 mm bore mesh |
| **`f7converged.wbpz`** | **335 MB** | **F7 contact, 0.75 mm converged — the good copy** |

## 14. WHERE WE ARE
**All Ansys work is complete.** No further VDI sessions are required for the phases below.

**Remaining, all off-VDI:**
1. **MIL-HDBK-5J** — freely available, Distribution Statement A, public release. Hosted on the
   Internet Archive and by Abbott Aerospace. Fixes **Ftux** and **A/B-basis allowables**, both
   currently placeholders. Also supplies S-N and da/dN data for F8/F9. **Highest value per hour.**
2. **F8 fatigue** — hand calculation from FE stresses plus MIL-HDBK-5J S-N curves. An aircraft
   fitting with no fatigue analysis is the most conspicuous gap a reviewer would find.
3. **F9 crack growth** — hand da/dN integration with a published K solution.
4. **F11 optimization** — the closed-form margins are already parametric; sweep analytically.
5. **F13 manufacturing/inspection, F14 digital thread** — documentation.
6. **F16/F17 formal stress report** — the artifact a stress engineer recognises on sight.

**Not done and not required:** F10 modal and eigenvalue buckling. Would be ~45 min VDI if wanted.

## 15. PORTFOLIO TARGET
- **Now: ~90.** **Realistic ceiling: ~92.**
- **95+ is NOT achievable** without a professional sign-off or a physical test. Both ruled out by
  constraint. Don't promise 95.

## 16. Still-open
- [ ] Ftux proper basis; A/B-basis allowables (MIL-HDBK-5J)
- [ ] Re-run Melcon-Hoblit at e = 1.900 in for an exact F15 margin
- [ ] Establish t/D range of Ekvall's specimens to resolve the double-counting question
- [ ] Ekvall paper — our margin curves cross at **e/D = 1.353**, an earlier note claimed 1.5.
      A crossing at 1.5 implies Fbru ≈ 606 MPa (1.17 × Ftu). **Do not assume it.**
- [ ] Elastic-plastic contact run to tighten the +0.165 lower bound
- [ ] Define the AF-DT-2000 clevis; pin material and size selection
- [ ] Resolve over-constrained contact nodes and the 1e8 coefficient ratio in F7
- [ ] Onshape drawing out of date; delete broken "Drawing 1"
- [ ] Plastic strain at e/D = 1.5 not captured; F12 colocation test

## 17. Lessons — don't repeat

### Analysis
- **Convergence needs 3+ points.** Two-point studies misdiagnosed a singularity three times in this
  project. The third instance (F7) would have changed the engineering conclusion.
- **Check whether a method's assumptions hold for the actual geometry.** The thin-lug method was
  used at t/D = 1.25 for months before anyone asked what that did to the margin. Correcting it
  consumed 77% of the reported margin.
- **Never compare a linear elastic peak stress against an allowable-based margin.** Convert both
  sides to the same basis first.
- **Bilinear hardening has no failure criterion.** Compute
  `required plastic strain = (peak vM - yield)/tangent modulus` before quoting any peak stress.
- **Near yield, comparing in strain space is ill-conditioned.** Compare in stress space.
- **Verify colocation before comparing two field maxima.**
- **Beam theory does not apply below about L/h = 3.** A cantilever estimate on the Rev D blade
  (L/h = 1.4) predicted the wrong critical location and understated deflection 3x.
- **When an absolute FE quantity diverges, look for a ratio that cancels the divergence.** F7's
  contact pressure diverged 134%; the stiff-pin ratio converged to 8%.
- **A pin joint carries no moment about its own axis.** Loading a lug at the flange while fixing the
  pin makes a free hinge — 87 kN.m applied against 1.6 kN.m of friction. Diverged immediately.

### Geometry / CAD
- **Build STEP externally and import — don't fight Discovery's GUI/scripting.**
- **Never text-parse a STEP for bounding boxes or volumes.** Arc crowns have no `CARTESIAN_POINT`.
  **Use the CAD kernel.**
- **Check the unit declaration on every generated STEP.** cadquery writes millimetres regardless.
- **Re-derive every geometry gate when a parameter changes.** A stale gate rejects correct work.

### Ansys operation
- **After changing any unit dropdown, re-read the numeric field.** Ansys *converts* rather than
  relabels. Caused a 0.071 MPa modulus, a 6 µm element size, and a 175 lb/ft³ density.
- **Scope by Named Selection worksheet rule, not by clicking.** Rules survive geometry swaps.
  Rev D bore: `Radius / Equal / 0.0254`. Flange: `Location Z / Smallest`. Pin ends:
  `Location Y / Equal / +-0.048387`. **Worksheet compares in the CAD unit system — read the note.**
- **Settings silently revert.** Contact Type reverted from Frictional to Bonded, and material
  assignments were wiped, both by an automatic geometry refresh. **Re-verify every setting
  immediately before solving, not just when you set it.**
- **Verify every typed field by zooming in.** Single-click selects the row, not the edit box.
- **Mass/volume gate every import.**
- A **Bonded** contact will solve cleanly and measure nothing. Check the type before trusting a
  contact result.

### Session management
- **The VDI wipes local disk at logout.** Two sessions were lost.
- `File > Archive` gives a single `.wbpz`. **Distinct name each time.**
- **Copy to H: immediately.** An archive far smaller than its mesh warrants means results were not
  included. Check you are reading the `.wbpz`, not the `.wbpj`.
- Confirm only **one Workbench instance** is running.
