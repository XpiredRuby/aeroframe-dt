# STRESS REPORT — AF-DT-1000
## Forward Pylon-to-Wingbox Attachment Fitting

| | |
|---|---|
| **Document** | AF-DT-1000-SR-001 |
| **Revision** | E |
| **Geometry revision** | D (frozen) |
| **Part** | AF-DT-1000, forward pylon-to-wingbox attachment fitting |
| **Aircraft** | MD-11 class, representative |
| **Material** | 7075-T7351 plate, AMS 4078 / AMS-QQ-A-250/12 |
| **Status** | **PASS**, `MS = +0.156` governing |

> ### CLAIM BOUNDARY
> **Educational / representative / portfolio only. Non-OEM, non-certified.**
> Geometry and load case are `SYNTHETIC_TEST_ONLY`. The damage-tolerance spectrum is
> `SYNTHETIC_SPECTRUM`. **Material allowables are real**, from MIL-HDBK-5J.
> This document has not been checked or approved by a licensed stress engineer. It demonstrates
> method and traceability; it does not substantiate a flight article.

**Revision E supersedes D.** The elastic-plastic contact measurement (§6.2), the FE verification
benchmarks (§10), and the modal and buckling FE (§9) were all executed after Rev D was issued.
The governing margin moves from `+0.078` to `+0.156`.

---

## 1. Summary of Results

| Check | Method | Margin | Ref |
|---|---|---|---|
| **Lug, combined oblique** | Melcon-Hoblit, elastic-plastic thick-lug corrected | **+0.156** | §6 |
| Lug, worst-case tolerance stack | released GD&T at adverse limits | +0.133 | §6.5 |
| Pin, bending | Simple beam, balanced clevis | +1.39 | §7 |
| Pin, double shear | Direct | +3.90 | §7 |
| Buckling | Eigenvalue FE, prestressed | no mode under applied load | §9 |
| Damage tolerance | Crack growth to `a_c` | 4,500 flt interval | §8 |

**Governing failure mode: combined bearing / transverse at the lug bore.**

### Margin history — why the number moved

| Stage | MS | Cause |
|---|---|---|
| Initial, thin-lug method, assumed Ftu = 71 ksi | +0.710 | — |
| Thick-lug correction applied, elastic | +0.165 | `t/D = 1.25` invalidates the uniform-bearing assumption |
| Real A-basis allowables substituted | +0.078 | assumed Ftu was 9% optimistic |
| **Elastic-plastic contact measurement** | **+0.156** | yielding redistributes the bearing peak |

**The initial figure was overstated by a factor of 4.6.** The first two corrections removed
assumptions that did not hold; neither was a refinement of the arithmetic. The third replaced a
deliberately conservative bound with a measurement, and is the only one that moved the margin
favourably.

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

**`t/D = 1.25` is the single most consequential geometric parameter in this report.** See §6.

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
B-basis becomes defensible only if a redundant path is demonstrated.

**Plasticity model** (§6.2, elastic-plastic run): bilinear isotropic hardening,
`Fty = 358.5 MPa` (52 ksi, A-basis L), tangent modulus `1631 MPa` derived from `Ftu`, `Fty` and 6%
elongation. **The elongation is S-basis and tabulated for LT**, not L — R1 does not give L
elongation on this page. The hardening curve is therefore mixed-basis and is not quoted as a
single-basis material definition.

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

The Melcon-Hoblit method (R2, R3) is a **thin-lug** method assuming bearing pressure is **uniform
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

**Elastic convergence study:**

| Bore mesh | Nodes | p real (MPa) | p stiff (MPa) | t_eff/t |
|---|---|---|---|---|
| 3.00 mm | 21,744 | 1265.1 | 938.6 | 0.7419 |
| 1.50 mm | 58,780 | 2146.8 | 1432.0 | 0.6670 |
| **0.75 mm** | **203,472** | **2955.9** | **2012.7** | **0.6809** |

**Absolute pressure diverged 134% across the study. The ratio moved 8.2% and converged.** This
validates the ratio method by evidence rather than argument.

**Elastic-plastic measurement**, same mesh, bilinear isotropic hardening on the lug in both runs:

| | p real (MPa) | p stiff (MPa) | **t_eff/t** |
|---|---|---|---|
| Elastic | 2955.9 | 2012.7 | 0.6809 |
| **Elastic-plastic** | **2236.9** | **1633.0** | **0.7300** |

Both peaks fall as yielding requires; the real-pin peak falls further (−24.3% against −18.9%),
because its higher peak had more plasticity available to relieve. Peak equivalent plastic strain
**6.46%** confirms the material genuinely yielded.

**Result: `t_eff/t = 0.730`.** The elastic value of 0.681 was a conservative lower bound, as Rev D
stated it to be.

**The plastic strain exceeds the 6% tabulated elongation.** Bilinear hardening carries no failure
criterion, so the model continues past the point where real material would fracture. This does not
affect the ratio — both runs share the material model — but **the 6.46% figure is not a rupture
prediction**, and none should be inferred from it. It occurs at a mesh-refined contact edge in the
same singular region that makes absolute pressure meaningless.

### 6.3 Margin calculation

Allowable loads from R2 with `Kt = 0.950`, `Ktru = 0.7875`, `Kbr = 1.240`:

    P'tu  = Kt   * Atn * Ftu  = 0.950  * 5.00 * 65,000 = 308,750 lb
    P'tru = Ktru * Abr * Ftux = 0.7875 * 5.00 * 66,000 = 259,875 lb
    P'bru = Kbr  * Abr * Ftux = 1.240  * 5.00 * 66,000 = 409,200 lb

Nominal stresses on the reduced effective area, with the 1.15 fitting factor:

    Elastic, t_eff/t = 0.6809:         Ra = 0.3909,   Rtr = 0.7740   ->  MS = +0.078
    Elastic-plastic, t_eff/t = 0.7300: Ra = 0.36463,  Rtr = 0.72198  ->  MS = +0.156

    MS = 1 / (Ra^1.6 + Rtr^1.6)^0.625 - 1

Lug areas are linear in effective thickness, so both load ratios scale directly with `t_eff`.

### 6.4 Sensitivities

| Case | MS |
|---|---|
| **Governing** | **+0.156** |
| Elastic contact bound (Rev D) | +0.078 |
| Thin-lug (uncorrected) | +0.584 |
| Ekvall mean, r = 1.003 | +0.153 |
| **Ekvall worst, r = 1.19** | **−0.028** |

**At Ekvall's worst-case method scatter the margin is still negative**, though far less so than at
Rev D's −0.094. R4 correlates the method against 243 lug tests with predicted/test ratios 0.85–1.19.

**The breakeven is `t_eff/t = 0.7513`** — the value at which the Ekvall worst case reaches zero. The
measurement came in at **0.7300, just short of clearing the band.**

**Possible double-counting:** if R4's specimen set included thick lugs, the thick-lug effect is
partly inside the measured scatter already, and applying both penalises the same physics twice.
**The elastic-plastic run did not resolve this** — it measured `t_eff/t`, whereas the question is
about the composition of R4's specimen set and requires the paper. **Best estimate +0.156;
worst-case stack −0.028, possibly conservative.**

### 6.5 Manufacturing tolerance stack

The released GD&T scheme (`PMI_GDT_DEFINITION.md`) derives every tolerance from margin sensitivity.
Stacking all of them back onto the margin at their adverse limits, evaluated on the interaction
equation rather than by linearisation:

| Term | ΔMS | Basis |
|---|---|---|
| Lug thickness at low material limit | −0.00925 | exact |
| **Bore position at LMC with MMC bonus** | **−0.01281** | extrapolated |
| Bore size at LMC | −0.00116 | bounded |
| **Worst case (arithmetic sum)** | **−0.02322** | |
| RSS | −0.01585 | context only |

    MS worst case = +0.133
    MS RSS        = +0.140

**The tolerance scheme consumes 14.9% of the margin and leaves it positive.** Tolerances would have
to be **6.7× wider** to reach zero — up from 3.6× at the Rev D margin.

The bore-position sensitivity is re-anchored on the F15 nonconformance case at the new operating
point, giving `dMS/de = 0.801/in` against Rev D's 0.747. **It remains an extrapolation from a single
distant anchor and remains the dominant term at 55% of the worst-case loss.**

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

**A high-strength steel pin is required.** Aluminium is not viable. Bending rises 49% if ears are as
thick as the lug, so **the clevis must be defined before a pin is selected.**

---

## 8. Damage Tolerance

**Safe-life fatigue is not supportable.** R1 §3.7.6.2 provides **no S-N curves** for the T73/T7351
temper. Damage tolerance is used instead, consistent with R5 (25.571).

**Critical crack size**, from `K_Ic = 25 ksi-sqrt(in)`, the governing transverse stress, and the
finite-width edge-crack geometry factor:

    a_c = **3.07 mm**    (0.1208 in)

Ligament bore-to-edge is 38.1 mm, so **`a_c` is 8.1% of the available ligament**. This depends only
on tabulated toughness, computed stress and geometry — the most defensible result in this section.

**`a_c` is itself a consequence of the thick-lug correction.** Uncorrected, transverse stress would
be 164.2 MPa and `a_c` about 6.6 mm — more than double. **`a_c` is quoted at the elastic
`t_eff/t = 0.681`, which is conservative**; re-deriving at 0.730 would give a slightly larger
critical flaw and a slightly longer interval. That re-derivation is an open item and is not claimed
here.

**Crack growth** uses Paris constants read from R1 Figure 3.7.6.2.9(b) at R = 0.10:
`m = 4.00`, `C = 3.7e-9` (in/cycle, ksi-sqrt-in). Graph-read, so factor-3 uncertainty on C.

**Spectrum is constructed** (`SYNTHETIC_SPECTRUM`): 1 GAG cycle/flight at 0.30 of limit,
10 manoeuvre at 0.15, 100 gust at 0.05. Equivalent `dS = 11.99 ksi/flight`.

    Flights, rogue flaw (1.27 mm) to critical:  9.42e3
    **Repeat inspection interval, life/2:        4,500 flights**

**By NDI at a 1.27 mm detection threshold. Visual inspection is inadequate** — `a_c = 3.07 mm` is
below reliable visual detection regardless of interval.

**The GAG cycle contributes 59% of damage from 0.9% of cycles.** Under a fourth-power law the
largest cycle dominates.

**The interval is assumption-limited.** Varying the GAG fraction 0.20–0.50 spans 8,912 to 952
flights — **a factor of 9.4, exceeding every other uncertainty combined.**

---

## 9. Dynamics and Stability

Free-vibration modal and prestressed eigenvalue buckling on the Rev D model, 119,408 nodes.

### 9.1 Modal

| Mode | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|
| Hz | **1197.2** | 1672.7 | 3130.0 | 5002.1 | 5887.4 | 6037.3 |

An analytical cantilever idealisation gave 2133 Hz and **predicted, before the run, that the true
first mode would be lower** because it ignores lug-head tip mass and flange compliance. It is lower
by 44%. The prediction held.

**Shaft-order excitation is comfortably clear** — turbofan N1 at 50–100 Hz and N2 at 200–300 Hz sit
four to twenty times below the first mode.

**Blade passing is not clear, and is now a live concern rather than an open question.** Blade-passing
frequency is `N1 × blade count`, roughly **1000–2500 Hz** for a large fan. **Modes 1 and 2 both fall
inside that band.** Resolving this requires a forced-response analysis against a defined engine;
neither the engine nor its blade count exists in this synthetic project. **This is recorded as a
finding, not a closure.**

### 9.2 Buckling

Three eigenvalue buckling modes, prestressed by the linear static solution:

| Mode | 1 | 2 | 3 |
|---|---|---|---|
| Load multiplier | −51.814 | −51.620 | **−25.068** |

**All three are negative** — buckling occurs only with the applied load **reversed**. Under the
design load direction **no buckling mode exists within the three extracted.** The governing case is
the smallest magnitude, `|λ| = 25.07`.

An analytical Euler column estimate gave `MS = +43.4` under compression. **That and the FE result
are different quantities** — a forward-load 1D column estimate against a reversed-load 3D
eigenvalue — and are not reported as agreeing. Both reach the same conclusion independently: at
`L/r = 6.9` this member is far too stocky for buckling to compete with yielding and bearing.

Linear eigenvalue buckling is an upper bound; real structures buckle below it. Irrelevant at a
factor of 25 in the wrong direction, but stated.

---

## 10. Verification Evidence

| Check | Result |
|---|---|
| Hand method reconstructed independently on a stress basis | agrees to **0.06%** |
| FE equilibrium, Rev D linear elastic | reaction error **0.006%** after refinement |
| FE equilibrium, both elastic-plastic contact runs | **10 ppm** |
| FE critical location | **bore**, confirming the lug method applies where it is used |
| Secondary critical location (blade root) | none — checked and ruled out |
| Mesh convergence, Rev D | 3-point, singularity ruled out |
| Mesh convergence, F7 ratio | 3-point, 8.2% total movement, converged |
| Geometry mass vs FE | **0.01%** |
| F12 correlation allowables vs R1 | Fsu matches to **0.1%** |
| **Damage tolerance, two independent implementations** | **agree to 7% on `a_c`, 10% on life** |

### 10.1 Analytical FE benchmarks

Acceptance criteria frozen before execution. Full detail in `reports/FE_VERIFICATION_REPORT.md`.

| Benchmark | Criterion | Result | Verdict |
|---|---|---|---|
| Constant-strain patch test, distorted mesh | exact | error **4.34e-19 m**, strains exact | PASS |
| Cantilever, BEAM188 | ≤0.5% | +0.57% | pass with exceedance |
| Cantilever, SOLID186 | ≤2%, converged | +0.20%, converged 0.09% | PASS |
| Simply supported plate vs Navier | ≤2% | +0.62% | pass |

Three caveats are carried in that report rather than smoothed over: a 1e-8 relative force residual
against a "machine precision" criterion, the beam's 0.57% against a 0.5% limit (transverse shear —
BEAM188 is Timoshenko, the oracle is Euler-Bernoulli, and the rotation was exact), and the plate
sequence drifting upward rather than converging.

**These verify the tool, not this analysis.** They are generic problems on simple geometry with no
contact, plasticity or stress concentration.

### 10.2 What the FE is and is not used for

**Linear elastic FE peak stress is NOT used to validate the margin.** Empirical lug allowables
already contain the stress concentration and local plasticity; comparing a peak elastic stress
against an allowable-based margin is a category error. The FE validates the method's *assumptions* —
load path, critical location, absence of a secondary failure site — not the margin itself.

**The damage tolerance cross-check** compared a hand calculation using a constant `F = 1.12` against
`src/aeroframe_dt/fatigue.py`, which applies the full finite-width edge-crack polynomial. The hand
calculation's stated limitation — that it would be non-conservative — **was recorded before the
comparison was run**, and the comparison confirmed both its direction and its magnitude. Module
values are adopted.

---

## 11. Limitations

1. **The elastic-plastic ratio is not independently mesh-converged.** It was run at the finest of
   F7's three meshes and inherits F7's convergence study rather than repeating it.
2. **The 20× stiff pin still bends.** Both the elastic and elastic-plastic ratios share that bias,
   so the **change** from 0.681 to 0.730 is more robust than either absolute value.
3. **Worst-case method scatter is negative** (−0.028), with an unresolved double-counting question.
4. **A-basis assumed.** B-basis becomes defensible if a redundant load path is demonstrated.
5. **Clevis undefined.** Pin bending and therefore `t_eff` both depend on it.
6. **Spectrum constructed, not derived.** The interval is conditional on §8's assumptions.
7. **Paris constants graph-read.** Order-of-magnitude life uncertainty.
8. **Edge-crack K solution.** A lug has a *loaded* hole; Bowie or Newman-Raju would be correct and
   would give a smaller `a_c` still.
9. **Bore-position tolerance sensitivity is extrapolated**, not derived, and dominates the
   tolerance stack.
10. **Blade-passing separation is not established**, with two modes inside a plausible band.
11. **No professional review.** Not checked or approved by a licensed stress engineer.

---

## 12. Conclusions

1. **The fitting passes at `MS = +0.156`** under A-basis allowables with the elastic-plastic
   thick-lug correction and the 1.15 fitting factor.
2. **The margin survives manufacturing variation** — the full tolerance stack at adverse limits
   leaves +0.133, and tolerances would need to be 6.7× wider to exhaust it.
3. **It does not survive worst-case method scatter** (−0.028), and whether that case is real depends
   on the double-counting question in §6.4, which needs R4.
4. **A high-strength steel pin is mandatory.** Aluminium is not viable.
5. **NDI at 4,500-flight intervals**, conditional on the constructed spectrum. Visual inspection is
   inadequate at any interval.
6. **Buckling is not a credible failure mode.** No mode exists under the applied load direction.
7. **Blade-passing separation is the most significant unresolved dynamic question**, and the FE
   modal made it more pressing rather than less.
8. **`t/D = 1.25` is the root of most of the above.** It invalidated the thin-lug method, drove the
   pin bending requirement, and halved the tolerable flaw size. **A thinner lug at larger diameter
   would relieve all three simultaneously** — the natural next design iteration.
9. **The corrections applied here account for a 4.6× movement in the original margin.** Two removed
   assumptions that did not hold; one replaced a conservative bound with a measurement.

---

## 13. Open Items

| Item | Effect if resolved |
|---|---|
| Load spectrum for the pylon attachment | replaces the largest uncertainty in §8 |
| R4 specimen `t/D` range | resolves the double-counting question on the worst case |
| Blade-passing frequency for a defined engine | resolves §9.1, the most pressing dynamic question |
| Clevis definition (AF-DT-2000) | fixes pin bending and `t_eff` |
| Single vs redundant load path | fixes A-basis vs B-basis |
| Mesh convergence of the elastic-plastic ratio | removes the inherited convergence argument |
| AFFDL K-factor curves digitised | replaces the extrapolated bore-position sensitivity |
| Exact Melcon-Hoblit rerun at e = 1.900 in | exact F15 nonconformance margin |
| Re-derive `a_c` at `t_eff/t = 0.730` | slightly larger critical flaw, longer interval |
| Bowie / Newman-Raju K solution for a loaded hole | corrects the remaining `a_c` approximation |
