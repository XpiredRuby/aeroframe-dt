# AeroFrame-DT — Handoff

**Analysis phase complete. All Ansys work finished. Material allowables now real.**

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
Rigorous engineering **substantiation** of ONE small critical aircraft part — a **forward
pylon-to-wingbox attachment fitting (AF-DT-1000)** on an MD-11-class aircraft — done like a real
aerospace stress engineer, with a full digital-thread evidence trail.

- **Thesis: depth over breadth on ONE fitting. Do NOT add more parts.**
- Claim boundary: **educational / representative / portfolio only. Non-OEM, non-certified.**
  Geometry and load case are `SYNTHETIC_TEST_ONLY`. **Material allowables are real** (MIL-HDBK-5J).

## 2. Repo
- **github.com/XpiredRuby/aeroframe-dt**, branch `main`.
- Claude commits via `create_or_update_file` (needs blob SHA when overwriting). `push_files` = 403.
- **Binaries (.xlsx, .step, .png, .wbpz) CANNOT be pushed.** I upload those. **SVG is text, can be pushed.**

## 3. Environment
- **Ansys Mechanical 2025 R2** on **TAMU VDI**. **No further Ansys work is required.**
- Files: my PC -> Google Drive -> VDI. Also H: drive (persists).
- Hand calcs: **Abbott Aerospace** AA-SM-009-002/-005, digitizing USAF AFFDL-TR-69-42 /
  NASA TM X-73305 (Melcon-Hoblit lug method).
- **MIL-HDBK-5J** (31 Jan 2003) downloaded, 69 MB. Public release, Distribution Statement A.

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

Volume 166.19 in³, **mass 7.65 kg**. Ratios **e/D=1.25, W/D=2.00, t/D=1.25**.
Abr=5.00 in², Atn=5.00 in², Aav=3.75 in².

**Axis mapping FROZEN (identity):** CAD X→aircraft X (fwd), Y→Y (span), Z→Z (up).
Lug axis = CAD Z. Bore axis = CAD Y.

**Grain orientation (design decision):** lug axis along **L**, transverse load along **LT**,
bore axis (thickness) along **ST**. Keeps the weakest direction and the SCC-susceptible direction
out of the primary load path.

### STEP build chain and unit trap
    python cad/build_revD.py          # inch numbers
    python cad/build_revD_to_mm.py    # rescales x25.4 -> USE THIS ONE
    python cad/build_f7.py            # two-body lug + pin, already mm

cadquery declares millimetres regardless of the numbers fed to it. Always use `_mm`.

## 5. LOADS — Rev C
- 6000 kg propulsion, 9g fwd. LC-02 governs.
- F_x = 529,740 N fwd; CG offset -> couple -> R_z = 317,840 N vertical.
- **Resultant 617,776 N at 59.04° off the lug axis. TRANSVERSE-DOMINANT.**
- In lb: P_axial = 71,453 lb (Z), P_transverse = 119,090 lb (X).

## 6. MARGIN — read `docs/MARGIN_SUMMARY.md`, it is authoritative

**Governing: `MS = +0.078`** — A-basis allowables, thick-lug corrected, 1.15 fitting factor.

| Stage | MS | What changed |
|---|---|---|
| Melcon-Hoblit thin-lug, assumed Ftu = 71 ksi | +0.710 | original |
| Thick-lug corrected (F7) | +0.165 | t_eff/t = 0.681 measured |
| **Real A-basis allowables (MIL-HDBK-5J)** | **+0.078** | Ftu was 9% optimistic |

**The original figure was overstated by a factor of 9.1.** Any document quoting +0.710 is quoting
the uncorrected, unverified value.

| Case | MS |
|---|---|
| **A-basis, corrected** | **+0.078** |
| B-basis, corrected | +0.111 |
| Ekvall mean, r = 1.003 | +0.075 |
| **Ekvall worst, r = 1.19** | **-0.094** |

Worst-case stack is negative, with a possible **double-counting** caveat — if Ekvall's 243 test
specimens included thick lugs, the effect is partly inside his scatter already. Needs the paper.

## 7. MATERIAL ALLOWABLES — real, from MIL-HDBK-5J
**Table 3.7.6.0(b3), page 3-373.** 7075-T7351 plate, **2.001-2.500 in** band (contains t_lug = 2.500).

| | A | B |
|---|---|---|
| Ftu L / LT / ST | 65 / 66 / 62 | 67 / 68 / 64 |
| Fty L / LT / ST | 52 / 52 / 49 | 55 / 55 / 52 |
| Fcy L / LT | 50 / 54 | 53 / 57 |
| Fsu | 39 | 40 |
| Fbru e/D 1.5 / 2.0 | 102 / 131 | 105 / 135 |
| Fbry e/D 1.5 / 2.0 | 79 / 93 | 83 / 99 |

ksi. `E = 10.3e3 ksi`, `Ec = 10.6e3`, `G = 3.9e3`, `mu = 0.33`, `density = 0.101 lb/in^3`.
Used: **Ftu = 65 (L)** for net tension, **Ftux = 66 (LT)** for transverse and bearing.

**K_Ic** (Table 3.1.2.1.6, "information only"): L-T 30 avg / 25 min, T-L 27 / 21, S-L 22 / 17 ksi-sqrt(in).

**SCC caution:** Table 3.1.2.3.1(b) flags 7075-T7351 ST direction, 39 ksi threshold at this
thickness. Grain orientation choice avoids it.

**F12 sweep allowables verified** against Table 3.7.6.0(b1), 0.500-1.000 in band:
Fsu 303 MPa used vs **44 ksi = 303.4 MPa A-basis** — matches to 0.1%. Ftu 75 ksi used vs 77 ksi
A-basis, 2.6% conservative. **F12 needs no revision.**

## 8. F7 CONTACT — COMPLETE (`docs/F7_CONTACT_THICK_LUG.md`)
Two-body lug + steel pin, Frictional mu = 0.1, 0.0127 mm radial clearance.
**Ratio method:** `t_eff/t = p_max(stiff pin) / p_max(real pin)`.

| Bore mesh | Nodes | p real | p stiff | t_eff/t | MS |
|---|---|---|---|---|---|
| 3.00 mm | 21,744 | 1265.1 | 938.6 | 0.7419 | — |
| 1.50 mm | 58,780 | 2146.8 | 1432.0 | 0.6670 | — |
| **0.75 mm** | **203,472** | **2955.9** | **2012.7** | **0.6809** | converged |

**Absolute pressure diverges 134%** — contact-edge singularity. **The ratio moves 8.2% and
converges.** Validates the method by evidence, not argument.

**Two points would have given the wrong answer** — the 3.0 -> 1.5 mm trend extrapolated to
t_eff/t ~ 0.60. The third point showed it rebounding.

## 9. F6 PIN BENDING — COMPLETE
Pin bending governs at ~780 MPa, 5.1x the 152 MPa double-shear stress. **High-strength steel pin
required**; aluminium not viable. Bending is 49% higher if clevis ears are as thick as the lug —
**the clevis is undefined.**

## 10. F5 FE — Rev D linear elastic — COMPLETE
Converged 152,951 nodes: peak 1194.1 MPa at bore edge, deformation 3.5686 mm.
Reaction error fell 0.074% -> 0.022% -> **0.006%**, confirming faceting as predicted.
**Does NOT validate the margin and cannot** — peak elastic stress is not comparable to an
allowable-based margin. Established: load reaches the assumed path, **bore is critical**, no
secondary critical location.

## 11. F12 CORRELATION — COMPLETE
Anchor: **Ekvall, J. Aircraft 23(5), 1986, pp. 438-443.** 243 tests, predicted/test 0.85-1.19,
mean 1.003. The IAF paper (Shiroky et al.) has a unit error — **NOT the anchor**.

Sweep, 7075-T651 lug, D=26.8, t=25, P=284,686 N:
- **Shear-out governs below e/D = 1.353, bearing above.** Bearing margin flat at +0.216.
- **Zero margin at e/D = 1.201**, confirmed by measurement (-0.002).
- **e/D = 1.0 fails by shear-out.** 750 MPa peak needs 37% plastic strain — discarded.
- Elastic scaling law holds to 1.7%. `w = 2e` makes net-section and shear-out areas identical.

## 12. F15 RCCA — DISPOSITION UNCHANGED, SEVERITY WORSE
Mis-drilled bore, e 2.500 -> 1.900 in. Originally +0.710 -> +0.220.
**Under both corrections this is approximately -0.370.** REWORK stands and is now unambiguous.
Approximate — scaled, not re-derived. Exact recomputation is open.

## 13. Ansys archives on H:
| File | Size | Contents |
|---|---|---|
| `revdconverged.wbpz` | 45.5 MB | Rev D linear elastic, converged |
| **`f7converged.wbpz`** | **335 MB** | **F7 contact, 0.75 mm converged — the good copy** |
| `f7contact.wbpz` | 20.3 MB | F7 contact, 3 mm mesh |
| `ed2p0.wbpz` | 9.21 MB | F12 lug e/D = 2.0 |

## 14. WHERE WE ARE — remaining work, none needs the VDI

1. **F9 damage tolerance.** **F8 safe-life fatigue is NOT supportable** — MIL-HDBK-5J Section
   3.7.6.2 has **no S-N curves** for the T73/T7351 temper. It does have crack-propagation data
   (Figures 3.7.6.2.9 a-c, graphs) and K_Ic. Damage tolerance is also what FAR 25.571 requires for
   primary structure. **Needs: da/dN values read off those figures, or published Paris constants.**
2. **F11 optimization** — margins are parametric; sweep analytically. Blocked on the Melcon-Hoblit
   K-factor curves, which are not digitised.
3. **F13 manufacturing/inspection, F14 digital thread** — documentation, unblocked.
4. **F16/F17 formal stress report** — the artifact a stress engineer recognises.

**Not done, not required:** F10 modal and buckling. ~45 min VDI if wanted.

## 15. PORTFOLIO TARGET
**Now ~90. Ceiling ~92.** 95+ needs professional sign-off or a physical test. Both ruled out.

## 16. Still-open
- [ ] Re-run Melcon-Hoblit at e = 1.900 in for exact F15 margin
- [ ] Ekvall specimen t/D range, to resolve double-counting
- [ ] Ekvall paper — our curves cross at **e/D = 1.353**, an earlier note claimed 1.5.
      A crossing at 1.5 implies Fbru ≈ 606 MPa. **Do not assume it.**
- [ ] Single vs redundant load path, fixing A-basis vs B-basis
- [ ] Elastic-plastic contact run to tighten the +0.078 lower bound
- [ ] Define AF-DT-2000 clevis; pin material and size selection
- [ ] Over-constrained contact nodes and 1e8 coefficient ratio in F7
- [ ] Onshape drawing out of date; plastic strain at e/D = 1.5; F12 colocation test

## 17. Lessons — don't repeat

### Analysis
- **Convergence needs 3+ points.** Two-point studies misled three times. The F7 instance would have
  changed the engineering conclusion.
- **Check whether a method's assumptions hold for the actual geometry.** The thin-lug method was
  used at t/D = 1.25 for months. Correcting it consumed 77% of the margin.
- **Verify allowables before trusting a margin.** "Representative Ftu = 71 ksi" was 9% optimistic
  against A-basis. Combined with the thick-lug error the headline was overstated 9.1x.
- **Never compare a linear elastic peak stress against an allowable-based margin.**
- **Bilinear hardening has no failure criterion.** Check required plastic strain against elongation
  before quoting any peak stress.
- **Near yield, comparing in strain space is ill-conditioned.** Compare in stress space.
- **Beam theory does not apply below about L/h = 3.**
- **When an absolute FE quantity diverges, look for a ratio that cancels it.**
- **A pin joint carries no moment about its own axis.** Loading the lug at the flange while fixing
  the pin makes a free hinge — 87 kN.m against 1.6 kN.m of friction.

### Geometry / CAD
- **Build STEP externally and import.** Don't fight Discovery's scripting.
- **Never text-parse a STEP for bounding boxes.** Arc crowns have no `CARTESIAN_POINT`.
- **Check the unit declaration on every generated STEP.**
- **Re-derive every geometry gate when a parameter changes.**

### Ansys operation
- **After changing any unit dropdown, re-read the numeric field.** Ansys converts rather than
  relabels. Caused a 0.071 MPa modulus, a 6 µm element size, a 175 lb/ft³ density.
- **Scope by Named Selection worksheet rule, not by clicking.** Rules survive geometry swaps.
  **The worksheet compares in the CAD unit system — read the note above the grid.**
- **Settings silently revert.** Contact Type went Frictional -> Bonded and materials were wiped,
  both by an automatic geometry refresh. **Re-verify immediately before solving.**
- A **Bonded** contact solves cleanly and measures nothing.
- **Verify every typed field by zooming.** Single-click selects the row, not the edit box.
- **Mass/volume gate every import.**

### Session management
- **The VDI wipes local disk at logout.** Two sessions lost.
- `File > Archive` gives one `.wbpz`. **Distinct name each time. Copy to H: immediately.**
- An archive far smaller than its mesh warrants means results were not included. Check you are
  reading the `.wbpz`, not the `.wbpj`.
