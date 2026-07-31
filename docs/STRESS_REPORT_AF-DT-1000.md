# STRESS REPORT — AF-DT-1000
## Forward Pylon-to-Wingbox Attachment Fitting

| | |
|---|---|
| **Document** | AF-DT-1000-SR-001 |
| **Revision** | D |
| **Part** | AF-DT-1000, forward pylon-to-wingbox attachment fitting |
| **Aircraft** | MD-11 class, representative |
| **Material** | 7075-T7351 plate, AMS 4078 / AMS-QQ-A-250/12 |
| **Status** | **PASS**, `MS = +0.078` governing |

> ### CLAIM BOUNDARY
> **Educational / representative / portfolio only. Non-OEM, non-certified.**
> Geometry and load case are `SYNTHETIC_TEST_ONLY`. The damage-tolerance spectrum is
> `SYNTHETIC_SPECTRUM`. **Material allowables are real**, from MIL-HDBK-5J.
> This document has not been checked or approved by a licensed stress engineer. It demonstrates
> method and traceability; it does not substantiate a flight article.

---

## 1. Summary of Results

| Check | Method | Margin | Ref |
|---|---|---|---|
| **Lug, combined oblique** | Melcon-Hoblit, thick-lug corrected | **+0.078** | §6 |
| Pin, bending | Simple beam, balanced clevis | +1.39 | §7 |
| Pin, double shear | Direct | +3.90 | §7 |
| Damage tolerance | Crack growth to `a_c` | 5,000 flt interval | §8 |

**Governing failure mode: combined bearing / transverse at the lug bore.**

### Margin history — why the number moved

| Stage | MS | Cause |
|---|---|---|
| Initial, thin-lug method, assumed Ftu = 71 ksi | +0.710 | — |
| Thick-lug correction applied | +0.165 | `t/D = 1.25` invalidates the uniform-bearing assumption |
| Real A-basis allowables substituted | **+0.078** | assumed Ftu was 9% optimistic |

**The initial figure was overstated by a factor of 9.1.** Both corrections removed assumptions that
did not hold; neither was a refinement of the arithmetic.

---

## 2. References

| Ref | Document |
|---|---|
| R1 | MIL-HDBK-5J, *Metallic Materials and Elements for Aerospace Vehicle Structures*, 31 Jan 2003 |
| R2 | Melcon & Hoblit lug method, via Abbott Aerospace AA-SM-009-002 and AA-SM-009-005 |
| R3 | USAF AFFDL-TR-69-42 / NASA TM X-73305 (lug allowable curves) |
| R4 | Ekvall, J.C., "Static Strength Analysis of Pin-Loaded Lugs," *J. Aircraft* 23(5), 1986, pp. 438-443 |
| R5 | FAR 25.561 (emergency landing), 25.571 (damage tolerance), 25.625 (fitting factor) |

---

## 3. Geometry

Rev D, frozen. All dimensions inches.

| Parameter | Value |
|---|---|
| Pin bore diameter, `d_pin` | 2.000 |
| Lug thickness, `t_lug` | 2.500 |
| Lug width, `w_lug` | 4.000 |
| Edge distance, `e_center` | 2.500 |
| Flange thickness | 1.000 |
| Web thickness | 2.500 (constant-thickness blade) |
| Blend radius | 0.500 |
| Station length | 16.000 |

**Derived:** `e/D = 1.25`, `W/D = 2.00`, **`t/D = 1.25`**
**Areas:** `Abr = 5.00 in²`, `Atn = 5.00 in²`, `Aav = 3.75 in²`
**Mass:** 7.65 kg (verified against FE model to 0.01%)

**`t/D = 1.25` is the single most consequential geometric parameter in this report.** See §5.

### Grain orientation — design decision

Part taken from plate with the **lug axis along L**, **transverse load along LT**, and the **bore
axis (thickness) along ST**.

Deliberate. ST is the weakest direction in thick 7xxx plate (62 ksi vs 65 and 66), and R1 Table
3.1.2.3.1(b) flags 7075-T7351 as **stress-corrosion susceptible in ST**, threshold 39 ksi at this
thickness. The orientation keeps ST out of the primary load path entirely.

---

## 4. Material and Allowables

**Source: R1, Table 3.7.6.0(b3), page 3-373.** 7075-T7351 plate, thickness band **2.001–2.500 in**,
containing `t_lug = 2.500 in`.

| Property | A-basis | B-basis |
|---|---|---|
| Ftu — L / LT / ST | **65** / **66** / 62 | 67 / 68 / 64 |
| Fty — L / LT / ST | 52 / 52 / 49 | 55 / 55 / 52 |
| Fcy — L / LT | 50 / 54 | 53 / 57 |
| Fsu | 39 | 40 |
| Fbru — e/D 1.5 / 2.0 | 102 / 131 | 105 / 135 |
| Fbry — e/D 1.5 / 2.0 | 79 / 93 | 83 / 99 |

ksi. Bearing values are "dry pin" per R1 §1.4.7.1.
`E = 10.3e3 ksi`, `Ec = 10.6e3`, `G = 3.9e3`, `mu = 0.33`, `rho = 0.101 lb/in³`.

**Used: `Ftu = 65 ksi (L)` for net tension, `Ftux = 66 ksi (LT)` for transverse and bearing.**

**A-basis is applied**, appropriate to a single-load-path fitting where failure is catastrophic.
B-basis would give `MS = +0.111` and becomes defensible only if a redundant path is demonstrated.

**Fracture toughness** (R1 Table 3.1.2.1.6, marked *information only*): `K_Ic` L-T = 30 avg,
**25 min** ksi-sqrt(in).

---

## 5. Loads

| Component | Value |
|---|---|
| Longitudinal, `F_x` | 529,740 N (119,090 lb) |
| Vertical, `R_z` | 317,840 N (71,453 lb) |
| **Resultant** | **617,776 N at 59.04° off the lug axis** |

Basis: 6000 kg propulsion mass at 9g forward per R5 (25.561 emergency landing), with a CG offset
producing the vertical couple. **Transverse-dominant** — the transverse term drives the margin.

**Fitting factor 1.15** applied per R5 (25.625), consistent with R2 for the combined oblique case.

---

## 6. Lug Analysis — Governing Check

### 6.1 Method and its limitation

The Melcon-Hoblit method (R2, R3) is a **thin-lug** method. It assumes bearing pressure is **uniform
through the lug thickness**. That assumption degrades as `t/D` rises; `t/D > 0.6` normally warrants
a pin-bending assessment.

**This lug is at `t/D = 1.25`.**

### 6.2 Thick-lug correction

A two-body contact FE model (lug + steel pin, frictional, 0.0127 mm radial clearance) measured the
real through-thickness distribution. Absolute contact pressure at a clearance-fit bore is
mesh-divergent, so a **ratio method** was used:

    t_eff / t = p_max(stiff pin) / p_max(real pin)

The stiff reference pin (20× modulus) cannot bend, so through-thickness concentration vanishes while
clearance effects and the contact-edge singularity remain identical and cancel.

| Bore mesh | Nodes | p real (MPa) | p stiff (MPa) | t_eff/t |
|---|---|---|---|---|
| 3.00 mm | 21,744 | 1265.1 | 938.6 | 0.7419 |
| 1.50 mm | 58,780 | 2146.8 | 1432.0 | 0.6670 |
| **0.75 mm** | **203,472** | **2955.9** | **2012.7** | **0.6809** |

**Absolute pressure diverged 134% across the study. The ratio moved 8.2% and converged.** This
validates the ratio method by evidence rather than argument.

**Result: `t_eff/t = 0.681`.** Bearing concentrates into 68% of the thickness. Nominal stresses rise
by `1/0.681`.

### 6.3 Margin calculation

Allowable loads from R2 with `Kt = 0.950`, `Ktru = 0.7875`, `Kbr = 1.240`:

    P'tu  = Kt   * Atn * Ftu  = 0.950 * 5.00 * 65,000 = 308,750 lb
    P'tru = Ktru * Abr * Ftux = 0.7875 * 5.00 * 66,000 = 259,875 lb
    P'bru = Kbr  * Abr * Ftux = 1.240 * 5.00 * 66,000 = 409,200 lb

Nominal stresses on the reduced effective area, with the 1.15 fitting factor:

    Ra  = 0.3909
    Rtr = 0.7740

    MS = 1 / (Ra^1.6 + Rtr^1.6)^0.625 - 1 = **+0.078**

### 6.4 Sensitivities

| Case | MS |
|---|---|
| **Governing** | **+0.078** |
| B-basis allowables | +0.111 |
| Thin-lug (uncorrected) | +0.584 |
| Ekvall mean, r = 1.003 | +0.075 |
| **Ekvall worst, r = 1.19** | **−0.094** |

**At Ekvall's worst-case method scatter the margin is negative.** R4 correlates the method against
243 lug tests with predicted/test ratios 0.85–1.19.

**Possible double-counting:** if R4's specimen set included thick lugs, the thick-lug effect is
partly inside the measured scatter already, and applying both penalises the same physics twice.
Unresolvable without the specimen `t/D` range from R4. **Best estimate +0.078; worst-case stack
−0.094, possibly conservative.**

---

## 7. Pin

Balanced clevis assumed (`t2 = 0.5 t1`, gap 0.030 in). **The mating fitting AF-DT-2000 is
undefined**; this is an assumption.

    Double shear:  tau = P / (2A) = 152.4 MPa
    Bending:       M = (P/2)(t1/4 + g + t2/2),  sigma = M/S = 780.3 MPa

**Bending exceeds shear by 5.1×.** Pin bending governs.

| Candidate pin material | Fb = 1.5 Ftu | MS |
|---|---|---|
| 15-5PH H1025 | 1603 MPa | +1.05 |
| 4340 at 180 ksi | 1862 | +1.39 |
| PH13-8Mo H1000 | 2120 | +1.72 |
| *7075-T6 (for contrast)* | *858* | *+0.10* |

**A high-strength steel pin is required.** Aluminium is not viable — 7075-T6 gives +0.10 at the
reference clevis and goes negative for thicker ears. Bending rises 49% if ears are as thick as the
lug, so **the clevis must be defined before a pin is selected.**

---

## 8. Damage Tolerance

**Safe-life fatigue is not supportable.** R1 §3.7.6.2 provides **no S-N curves** for the T73/T7351
temper. Damage tolerance is used instead, consistent with R5 (25.571).

**Critical crack size**, from `K_Ic = 25 ksi-sqrt(in)` and the governing transverse stress:

    a_c = (1/pi)(K_Ic / (F*sigma))^2 = 0.1296 in = **3.29 mm**

Ligament bore-to-edge is 38.1 mm, so **`a_c` is 8.6% of the available ligament**. This depends only
on tabulated toughness and computed stress — the most defensible result in this section.

**`a_c` is itself a consequence of the thick-lug correction.** Uncorrected, transverse stress would
be 164.2 MPa and `a_c` would be 7.1 mm — more than double.

**Crack growth** uses Paris constants read from R1 Figure 3.7.6.2.9(b) at R = 0.10:
`m = 4.00`, `C = 3.7e-9` (in/cycle, ksi-sqrt-in). Graph-read, so factor-3 uncertainty on C.

**Spectrum is constructed** (`SYNTHETIC_SPECTRUM`): 1 GAG cycle/flight at 0.30 of limit,
10 manoeuvre at 0.15, 100 gust at 0.05. Equivalent `dS = 11.99 ksi/flight`.

    Flights, rogue flaw (1.27 mm) to critical:  1.04e4
    **Repeat inspection interval, life/2:       5,000 flights**

**By NDI at a 1.27 mm detection threshold. Visual inspection is inadequate** — `a_c = 3.3 mm` is
below reliable visual detection regardless of interval.

**The GAG cycle contributes 59% of damage from 0.9% of cycles.** Under a fourth-power law the
largest cycle dominates.

**The interval is assumption-limited.** Varying the GAG fraction 0.20–0.50 spans 9,800 to 1,050
flights — **a factor of 9.3, exceeding every other uncertainty combined.**

---

## 9. Verification Evidence

| Check | Result |
|---|---|
| Hand method reconstructed independently on a stress basis | agrees to **0.06%** |
| FE equilibrium, Rev D linear elastic | reaction error **0.006%** after refinement |
| FE critical location | **bore**, confirming the lug method applies where it is used |
| Secondary critical location (blade root) | none — checked and ruled out |
| Mesh convergence, Rev D | 3-point, singularity ruled out |
| Mesh convergence, F7 ratio | 3-point, 8.2% total movement, converged |
| Geometry mass vs FE | **0.01%** |
| F12 correlation allowables vs R1 | Fsu matches to **0.1%** |

**Linear elastic FE peak stress is NOT used to validate the margin.** Empirical lug allowables
already contain the stress concentration and local plasticity; comparing a peak elastic stress
against an allowable-based margin is a category error. The FE validates the method's *assumptions* —
load path, critical location, absence of a secondary failure site — not the margin itself.

---

## 10. Limitations

1. **Elastic-only contact measurement.** Real yielding would flatten the pressure peak and raise
   `t_eff`. **`+0.078` is a lower bound**; the true margin lies between +0.078 and +0.584.
2. **Worst-case method scatter is negative** (−0.094), with an unresolved double-counting question.
3. **A-basis assumed.** B-basis gives +0.111 if a redundant load path is demonstrated.
4. **Clevis undefined.** Pin bending and therefore `t_eff` both depend on it.
5. **Spectrum constructed, not derived.** The interval is conditional on §8's assumptions.
6. **Paris constants graph-read.** Order-of-magnitude life uncertainty.
7. **Simplified K solution** (`F = 1.12`). A Bowie or Newman-Raju solution would give a **smaller**
   `a_c`, so the quoted value is non-conservative.
8. **No professional review.** Not checked or approved by a licensed stress engineer.

---

## 11. Conclusions

1. **The fitting passes at `MS = +0.078`** under A-basis allowables with the thick-lug correction
   and the 1.15 fitting factor.
2. **The margin is thin.** It survives worst-case method scatter only if the double-counting concern
   in §6.4 resolves favourably.
3. **A high-strength steel pin is mandatory.** Aluminium is not viable.
4. **NDI at 5,000-flight intervals**, conditional on the constructed spectrum. Visual inspection is
   inadequate at any interval.
5. **`t/D = 1.25` is the root of most of the above.** It invalidated the thin-lug method, drove the
   pin bending requirement, and halved the tolerable flaw size. **A thinner lug at larger diameter
   would relieve all three simultaneously** — the natural next design iteration.
6. **The two corrections applied here account for a 9.1× overstatement in the original margin.**
   Neither was a modelling refinement; both removed assumptions that did not hold for this geometry.

---

## 12. Open Items

| Item | Effect if resolved |
|---|---|
| Load spectrum for the pylon attachment | replaces the largest uncertainty in §8 |
| R4 specimen `t/D` range | resolves the double-counting question on the worst case |
| Clevis definition (AF-DT-2000) | fixes pin bending and `t_eff` |
| Single vs redundant load path | fixes A-basis vs B-basis, worth +0.033 |
| Elastic-plastic contact run | tightens the +0.078 lower bound |
| Exact Melcon-Hoblit rerun at e = 1.900 in | exact F15 nonconformance margin |
| Bowie / Newman-Raju K solution | corrects the non-conservative `a_c` |
