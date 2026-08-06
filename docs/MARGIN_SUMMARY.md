# AF-DT-1000 — Margin Summary (single source of truth)

**This document supersedes the margin figure quoted anywhere else in the repository.**

**Governing margin: `MS = +0.151`**
(7050-T7451, A-basis allowables, elastic-plastic thick-lug correction, 1.15 fitting factor)

**Superseded 2026-08-06.** The previous figure of `+0.156` was on 7075-T7351. F23 established that
**7075-T7351 plate is not tabulated above 4.000 in** while this part requires 6.000 in stock, so the
material was re-selected to **7050-T7451**. F24 re-measured the elastic-plastic contact ratio on the
new material — `t_eff/t = 0.6828`, against 0.7300 for 7075 — and re-derived the margin at `+0.151`.

**Claim boundary:** educational / representative / portfolio only. Non-OEM, non-certified.
Load case and geometry are `SYNTHETIC_TEST_ONLY`. **Material allowables are real**, taken from
**MMPDS-2026, Volume I, 1 July 2026**, Table 3.7.4.0(b1).

---

## 1. The chain

| Stage | MS | What changed |
|---|---|---|
| Melcon-Hoblit, thin-lug, assumed Ftu = 71 ksi | +0.710 | original |
| Reconstructed on a stress basis | +0.7104 | verification only, 0.06% agreement |
| Corrected for thick-lug bearing distribution | +0.165 | F7 contact measurement, elastic |
| Real A-basis allowables from MIL-HDBK-5J | +0.078 | Ftu was 9% optimistic |
| Elastic-plastic contact measurement, 7075 | +0.156 | F16, `t_eff/t` 0.6809 -> 0.7300 |
| **Material re-selected to 7050-T7451** | **+0.151** | F23/F24 — 7075 plate does not exist at 6.000 in |

**The originally reported margin was overstated by a factor of 4.7.** The first two corrections were
not refinements — each removed an assumption that did not hold. F16 was the only stage that moved
the margin favourably, and the final stage gave most of that back: **7050 does not yield as readily
as 7075, so it earns its margin from strength rather than from plastic redistribution.**

## 2. Correction 1 — the thin-lug assumption

The Melcon-Hoblit method assumes bearing pressure is uniform through the lug thickness. **This lug
is at t/D = 1.25**, roughly double the t/D ~ 0.6 above which pin bending normally warrants
assessment.

F7 measured the real distribution by contact FE, using a stiff-pin ratio that cancels the
clearance-induced circumferential concentration and the contact-edge singularity:

    t_eff / t = p_max(stiff pin) / p_max(real pin) = 0.6809   (elastic, 7075 and 7050)
                                                   = 0.7300   (elastic-plastic, 7075, F16)
                                                   = 0.6828   (elastic-plastic, 7050, F24)

Converged over three mesh densities (21.7k / 58.8k / 203.5k nodes) in the elastic case. The ratio
moved 8.2% while the underlying absolute pressures diverged 134%. Full detail in
`F7_CONTACT_THICK_LUG.md`, `F16_ELASTIC_PLASTIC_CONTACT.md` and `F24_MARGIN_REPROPAGATION.md`.

## 3. Correction 2 — real material allowables

**Source: MMPDS-2026, Volume I, Table 3.7.4.0(b1).** 7050-T7451 plate, AMS 4050,
**thickness band 5.001-6.000 in**, which contains the 6.000 in minimum stock thickness this part's
envelope requires.

| Property | A-basis, L | A-basis, LT | A-basis, ST |
|---|---|---|---|
| Ftu, ksi | **70** | **70** | 66 |
| Fty, ksi | 60 | 60 | 57 |
| Fcy, ksi | 57 | 63 | 62 |
| Fsu, ksi | 43 (L-S) | 43 (T-S) | 35 (S-L) |
| Fbru, e/D = 2.0 | 137 | **138** | — |
| Fbry, e/D = 2.0 | 105 | 106 | — |

`E = 10.3e3 ksi`, `Ec = 10.6e3 ksi`, `G = 3.9e3 ksi`, `mu = 0.33`, `density = 0.102 lb/in^3`.
Bearing values are "dry pin" per Section 1.4.7.1.

**The elastic constants are identical to 7075-T7351 to tabulated precision**, which is why the FE
stiffness model carried over without re-running.

### 3.1 What was superseded

The project previously used **MIL-HDBK-5J Table 3.7.6.0(b3)**, 7075-T7351, band 2.001-2.500 in:
`Ftu` 65 (L) / 66 (LT), `Fbru` at e/D 2.0 of 131. Two independent problems retired that basis:

- **F21** — MIL-HDBK-5J was cancelled and superseded by MMPDS, and removed from the 14 CFR 25.613
  compliance path. The MMPDS locator is **3.7.9.0(b2)**, not 3.7.6.0(b3); §3.7.6 in MMPDS is alloy
  7056. Re-reading it also showed the values had moved: `Ftu` L 65 -> 66, `Fbru` 131 -> 132.
- **F23** — 7075-T7351 plate is tabulated only to 4.000 in. **There is no band containing 6.000 in.**

### Grain orientation — a stated design decision

The part is taken from plate with the **lug axis along L** and the **transverse load direction along
LT**. The short-transverse direction is the bore axis, carrying no primary load.

For 7050-T7451 the L and LT ultimate strengths are equal at 70 ksi, so the orientation no longer
buys strength as it did with 7075. It is retained because **ST remains the weakest direction** (66
ksi) and because 7050-T7451 carries a **stress-corrosion threshold of 35 ksi in ST** over
0.750-6.000 in. Keeping ST out of the load path avoids both.

### A-basis, not B-basis

**A-basis is used**, appropriate for a single-load-path fitting where failure would be catastrophic.
If the design is later shown to have a redundant load path, B-basis becomes defensible and the
margin improves.

## 4. Result

    Allowable loads, Kt = 0.950, Ktru = 0.7875, Kbr = 1.240, Ftu = Ftux = 70 ksi:
      P'tu  = 0.950  * 5.00 * 70,000 = 332,500 lb
      P'tru = 0.7875 * 5.00 * 70,000 = 275,625 lb
      P'bru = 1.240  * 5.00 * 70,000 = 434,000 lb

    Elastic-plastic, 7050, t_eff/t = 0.6828:
      Ra = 0.36196,  Rtr = 0.72773
      MS = 1/(Ra^1.6 + Rtr^1.6)^0.625 - 1 = +0.151

| Basis | Thick-lug, elastic | **Thick-lug, elastic-plastic** |
|---|---|---|
| 7075-T7351, MIL-HDBK-5J A-basis | +0.078 | +0.156 |
| **7050-T7451, MMPDS-2026 A-basis** | +0.148 | **+0.151** |

**The fitting passes by 15.1%.**

Note that for 7050 the elastic and elastic-plastic values nearly coincide — 0.148 against 0.151 —
because the measured contact ratio barely moved off the elastic bound. **Under 7050 the margin is
essentially insensitive to the plasticity assumption**, which is a more robust position than 7075's
was, even though the headline number is marginally lower.

## 5. Ekvall method scatter — on tolerance limits, not observed extremes

Ekvall's 243 correlated lug tests give a mean test/predicted ratio of **1.003** with a standard
deviation of **0.065** over 224 predictions, approximately normally distributed. See
`F18_EKVALL_SPECIMEN_BASIS.md`.

| Basis | factor | pred/test | **MS** |
|---|---|---|---|
| Mean | 1.003 | 1.003 | +0.148 |
| 90% probability, 95% confidence | 0.910 | <= 1.099 | **+0.048** |
| **99% probability, 95% confidence** | **0.837** | **<= 1.195** | **-0.037** |

**99% probability at 95% confidence is the definition of A-basis.** This project uses A-basis
allowables, so **-0.037 is the statistically consistent worst case** and it is negative. It was
-0.032 under 7075; the small worsening is the loss of the plasticity gain.

**At the B-basis-consistent pairing the margin is positive at +0.048.**

### Double-counting — RESOLVED, directionally

If Ekvall's specimens included thick lugs, the thick-lug effect is already inside the measured
scatter and applying both penalises the same physics twice.

**The source confirms it does.** Specimen `t/D` ranges **0.098 to 1.316**. This fitting is at
**1.250, inside that range at 95% of the thickest specimen.** The method contains **no
thickness-dependent term** — `P = D t K_BR F_tu` with `K_BR` a function of `W/D` and eccentricity
only — so any real through-thickness bearing effect in those tests was absorbed into the empirically
fitted `K_BR` and its scatter.

**The overlap cannot be quantified.** The source reports the `t/D` range but never its distribution.
**No numerical credit is taken** — both the full thick-lug correction and the full scatter band
continue to be applied.

**A new limitation applies since F23.** Ekvall's population is a 1986 dataset whose **alloy
coverage this project has not verified for 7050**. The correlation, the specimen basis and the
method cross-check all now rest on an unverified assumption of applicability.

**Best estimate +0.151. A-basis-consistent worst case -0.037, established as conservative.**

## 6. Manufacturing tolerance stack

`tools/run_f13_inspection_plan.py`, evaluated on the real Melcon-Hoblit interaction at the released
7050 operating point:

| | Value |
|---|---|
| Nominal | **+0.151** |
| Worst case, all tolerances adverse | **+0.128** |
| RSS | +0.136 |
| Margin consumed, worst case | **15.3%** |
| Tolerance scale factor to zero margin | **6.54x** |

Bore position dominates at −0.0128 of the −0.0231 worst-case delta. **The bore-position sensitivity
is extrapolated from the F15 anchor rather than independently derived** — see PMI §4.2.

## 7. Effect on the F15 nonconformance case

`F15_NONCONFORMANCE_RCCA_AF-DT-1000.md` assesses a mis-drilled bore, edge distance 2.500 -> 1.900
in, originally recorded as +0.710 -> +0.220.

Scaling by the same `(1 + MS)` factor gives approximately **-0.370** on the elastic 7075 basis.
**REWORK disposition stands and is unambiguous on every basis evaluated.** The figure is
approximate, scaled rather than re-derived at e = 1.900 in; exact recomputation is an open item and
has not been redone on 7050.

## 8. What did not change

- **Equilibrium verified** to 0.006% in the Rev D linear elastic run, and to 10 ppm in the F16 runs
- **Bore is the critical location**, confirmed by FE — where the lug method applies
- **Pin bending governs the pin** at ~780 MPa, requiring a high-strength steel pin
- **The hand method is internally consistent**, reconstructible from first principles to 0.06%
- **Geometry is unchanged** — Rev D stands, no Rev E was required by the material change

## 9. F12 correlation allowables — independently verified

The F12 lug sweep used a different alloy, 7075-T651 at t = 0.984 in. Checked against
MIL-HDBK-5J Table 3.7.6.0(b1), thickness band 0.500-1.000 in:

| Property | Used in F12 | MIL-HDBK-5J A-basis |
|---|---|---|
| Fsu | 303 MPa | **44 ksi = 303.4 MPa** |
| Ftu | 517 MPa (75.0 ksi) | 77 ksi |

**Fsu matches to 0.1%.** Ftu was 2.6% conservative. **This check has not been repeated against
MMPDS**, and the MIL-HDBK-5J locator used here is subject to the same cancellation finding as §3.1.

## 10. Fracture toughness

The `K_Ic` values previously quoted here are **MIL-HDBK-5J Table 3.1.2.1.6 for 7075-T7351** and no
longer apply to the released material. MMPDS-2026 provides fatigue crack growth data for 7050-T7451
plate at Figures **3.7.4.2.9(a) through (c)**, and the stress-corrosion threshold in ST is **35 ksi**
over 0.750-6.000 in.

**The 7050 fracture toughness values have not yet been read**, so `F9_DAMAGE_TOLERANCE.md` still
rests on 7075 data and is stale pending re-derivation.

## 11. Bottom line

**The fitting passes at MS = +0.151**, with four qualifications a reviewer should see stated rather
than discover:

1. **The contact measurement was re-made on the released material** (F24). One mesh was run; it
   inherits F7's three-mesh convergence study rather than repeating it. The two alloys are
   elastically identical, so that inheritance is stronger than it would otherwise be.
2. **The A-basis-consistent method scatter is negative** (-0.037), established as conservative
   because the correlation set included lugs as thick as this one and the method has no thickness
   term. The overlap cannot be quantified. **Ekvall's applicability to 7050 is unverified.**
3. **A-basis assumed.** If a redundant load path is demonstrated, B-basis applies and the
   B-basis-consistent scatter limit gives +0.048 — positive on both counts.
4. **The margin remains thin enough that the fitting factor matters.** It is retained because
   FAR 25.625 requires it.

## 12. Open

- [x] ~~Establish the t/D range of Ekvall's specimens~~ — **CLOSED**, F18
- [x] ~~Elastic-plastic contact run to tighten the lower bound~~ — **CLOSED**, F16
- [x] ~~Re-propagate the F13 tolerance stack at the new operating point~~ — **CLOSED**, §6
- [x] ~~Resolve the plate thickness band the part can be cut from~~ — **CLOSED**, F23
- [ ] Re-derive `F9_DAMAGE_TOLERANCE.md` on 7050 `K_Ic` and `da/dN`
- [ ] Verify Ekvall's alloy coverage includes 7050
- [ ] Re-run Melcon-Hoblit at e = 1.900 in for an exact F15 margin, on 7050
- [ ] Mesh-converge the elastic-plastic ratio
- [ ] Confirm whether the installation is single or redundant load path, fixing A vs B basis
- [ ] **REQ-012 safe-life fatigue is now supportable and has not been built.** MMPDS-2026
      §3.7.4.2.8 provides best-fit S/N curves for 7050-T7451 plate including **notched Kt = 3.0**.
      The blocker was never the absence of fatigue data — it was 7075-T7351 specifically, which has
      no S/N curves in any temper but T6.
