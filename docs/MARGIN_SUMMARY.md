# AF-DT-1000 — Margin Summary (single source of truth)

**This document supersedes the margin figure quoted anywhere else in the repository.**

**Governing margin: `MS = +0.156`**
(A-basis allowables, elastic-plastic thick-lug correction, 1.15 fitting factor)

**Superseded 2026-08-03.** The previous figure of `+0.078` was an elastic-only lower bound.
`F16_ELASTIC_PLASTIC_CONTACT.md` measured `t_eff/t = 0.7300` against the elastic 0.6809, raising
the margin to `+0.156`. The `+0.078` value remains valid as a conservative floor and appears
throughout the F13 and F15 documents, which were built on it.

**Claim boundary:** educational / representative / portfolio only. Non-OEM, non-certified.
Load case and geometry are `SYNTHETIC_TEST_ONLY`. **Material allowables are now real**, taken from
MIL-HDBK-5J.

---

## 1. The chain

| Stage | MS | What changed |
|---|---|---|
| Melcon-Hoblit, thin-lug, assumed Ftu = 71 ksi | +0.710 | original |
| Reconstructed on a stress basis | +0.7104 | verification only, 0.06% agreement |
| Corrected for thick-lug bearing distribution | +0.165 | F7 contact measurement, elastic |
| Real A-basis allowables from MIL-HDBK-5J | +0.078 | Ftu was 9% optimistic |
| **Elastic-plastic contact measurement** | **+0.156** | F16, `t_eff/t` 0.6809 -> 0.7300 |

**The originally reported margin was overstated by a factor of 4.6.** The first two corrections
were not refinements — each removed an assumption that did not hold. The third, F16, is the only
one that moved the margin favourably, and it did so by replacing a conservative bound with a
measurement rather than by relaxing anything.

## 2. Correction 1 — the thin-lug assumption

The Melcon-Hoblit method assumes bearing pressure is uniform through the lug thickness. **This lug
is at t/D = 1.25**, roughly double the t/D ~ 0.6 above which pin bending normally warrants
assessment.

F7 measured the real distribution by contact FE, using a stiff-pin ratio that cancels the
clearance-induced circumferential concentration and the contact-edge singularity:

    t_eff / t = p_max(stiff pin) / p_max(real pin) = 0.681   (elastic)
                                                   = 0.730   (elastic-plastic, F16)

Converged over three mesh densities (21.7k / 58.8k / 203.5k nodes). The ratio moved 8.2% while the
underlying absolute pressures diverged 134%. Full detail in `F7_CONTACT_THICK_LUG.md` and
`F16_ELASTIC_PLASTIC_CONTACT.md`.

## 3. Correction 2 — real material allowables

The project previously carried `Ftu = 71 ksi (representative)` and `Ftux = Ftu` as an admitted
placeholder. Both are now replaced.

**Source: MIL-HDBK-5J, 31 January 2003, Table 3.7.6.0(b3), page 3-373.**
7075-T7351 plate, AMS 4078 and AMS-QQ-A-250/12, **thickness band 2.001-2.500 in**, which contains
the `t_lug = 2.500 in` of this part.

| Property | A-basis | B-basis | Previously assumed |
|---|---|---|---|
| Ftu, L | **65** | 67 | 71 (both directions) |
| Ftu, LT | **66** | 68 | 71 |
| Ftu, ST | 62 | 64 | — |
| Fty, L | 52 | 55 | — |
| Fty, LT | 52 | 55 | — |
| Fty, ST | 49 | 52 | — |
| Fcy, L | 50 | 53 | — |
| Fsu | 39 | 40 | — |
| Fbru, e/D = 1.5 | 102 | 105 | — |
| Fbru, e/D = 2.0 | 131 | 135 | — |
| Fbry, e/D = 1.5 | 79 | 83 | — |
| Fbry, e/D = 2.0 | 93 | 99 | — |

All values in ksi. Bearing values are "dry pin" per Section 1.4.7.1.
`E = 10.3e3 ksi`, `Ec = 10.6e3 ksi`, `G = 3.9e3 ksi`, `mu = 0.33`, `density = 0.101 lb/in^3`.

**The assumed 71 ksi was 9% optimistic** against the A-basis L value of 65 ksi.

### Grain orientation — a stated design decision

The part is taken from plate with the **lug axis along L** and the **transverse load direction
along LT**. The short-transverse direction is therefore the bore axis, carrying no primary load.

This is deliberate. ST is always the weakest direction in thick 7xxx plate — 62 ksi here against 65
and 66 — and MIL-HDBK-5J Table 3.1.2.3.1(b) additionally flags 7075-T7351 for
**stress-corrosion susceptibility in the ST direction**, with a threshold of 39 ksi at this
thickness. Keeping ST out of the load path avoids both.

Consequently `Ftu = 65 ksi (L)` for net tension and `Ftux = 66 ksi (LT)` for the transverse and
bearing terms. LT being marginally stronger than L is why the transverse-dominant load is oriented
this way rather than the reverse.

### A-basis, not B-basis

**A-basis is used**, appropriate for a single-load-path fitting where failure would be
catastrophic. B-basis applies to redundant structure and would give MS = +0.111 on the elastic
basis. If the design is later shown to have a redundant load path, B-basis becomes defensible and
the margin improves accordingly.

## 4. Result

    Elastic (F7, t_eff/t = 0.6809):
    Ra  = 0.3909,  Rtr = 0.7740
    MS  = 1/(Ra^1.6 + Rtr^1.6)^0.625 - 1 = +0.078

    Elastic-plastic (F16, t_eff/t = 0.7300):
    Ra  = 0.36463, Rtr = 0.72198
    MS  = +0.156

| Basis | Thin-lug | Thick-lug, elastic | **Thick-lug, elastic-plastic** |
|---|---|---|---|
| Assumed 71 ksi | +0.710 | +0.165 | — |
| **MIL-HDBK-5J A-basis** | +0.584 | +0.078 | **+0.156** |
| MIL-HDBK-5J B-basis | +0.632 | +0.111 | — |

**The fitting passes by 15.6%.**

## 5. Ekvall correlation band, re-propagated

Ekvall's 243 lug tests give predicted/test ratios of 0.85 to 1.19, mean 1.003. Allowable scales as
`1/r`, so `(1 + MS)` scales as `1/r`.

| Ekvall ratio | On +0.710 (original) | On +0.078 (elastic) | **On +0.156 (current)** |
|---|---|---|---|
| Best, r = 0.85 | +1.012 | +0.269 | **+0.360** |
| Mean, r = 1.003 | +0.705 | +0.075 | **+0.153** |
| **Worst, r = 1.19** | +0.437 | -0.094 | **-0.028** |

**At Ekvall's worst-case method scatter the margin is still negative**, but far less so than the
elastic case suggested. The breakeven is `t_eff/t = 0.7513`; the elastic-plastic run measured
**0.7300, just short of clearing the band.**

### Caveat — possible double-counting

Ekvall's band came from 243 physical lug tests. If any specimens were thick lugs, the thick-lug
effect is **already partly inside the measured scatter**, and applying the full correction plus the
full worst-case scatter penalises the same physical effect twice. Resolving this needs the Ekvall
paper to establish the t/D range of his specimen set.

**The elastic-plastic run did not resolve this.** F16 measured `t_eff/t`; the double-counting
question is about the composition of a 1986 test dataset and no FE run on this fitting can answer
it. See `F16_ELASTIC_PLASTIC_CONTACT.md` §6, which corrects an overstatement made during execution.

**Best estimate +0.156. Worst-case stack -0.028, possibly conservative.**

## 6. Effect on the F15 nonconformance case

`F15_NONCONFORMANCE_RCCA_AF-DT-1000.md` assesses a mis-drilled bore, edge distance 2.500 -> 1.900
in, originally recorded as +0.710 -> +0.220.

Scaling by the same `(1 + MS)` factor gives approximately **-0.370** on the elastic basis, or
approximately **-0.32** on the elastic-plastic basis.

**REWORK disposition stands and is now unambiguous** on either basis. The original justification —
"only +0.025 at worst-case scatter" — substantially understated the severity. The figure is
approximate, scaled rather than re-derived at e = 1.900 in; exact recomputation is an open item.

## 7. What did not change

- **Equilibrium verified** to 0.006% in the Rev D linear elastic run, and to 10 ppm in both F16 runs
- **Bore is the critical location**, confirmed by FE — where the lug method applies
- **Pin bending governs the pin** at ~780 MPa, requiring a high-strength steel pin
- **The hand method is internally consistent**, reconstructible from first principles to 0.06%
- **Nominal stresses remain modest** — bearing 191.5 MPa, net section 98.5 MPa

The part is not grossly undersized. The methods used to substantiate it were optimistic, and
correcting them consumed most of the reported margin; a better contact measurement returned some.

## 8. F12 correlation allowables — independently verified

The F12 lug sweep used a different alloy, 7075-T651 at t = 0.984 in. Checked against
MIL-HDBK-5J Table 3.7.6.0(b1), thickness band 0.500-1.000 in:

| Property | Used in F12 | MIL-HDBK-5J A-basis |
|---|---|---|
| Fsu | 303 MPa | **44 ksi = 303.4 MPa** |
| Ftu | 517 MPa (75.0 ksi) | 77 ksi |

**Fsu matches to 0.1%.** Ftu was 2.6% conservative. The F12 correlation therefore rests on verified
allowables and requires no revision.

## 9. Fracture toughness — now available

MIL-HDBK-5J Table 3.1.2.1.6, 7075-T7351 plate, `K_Ic` in ksi-sqrt(in):

| Orientation | Max | Avg | Min | Samples |
|---|---|---|---|---|
| L-T | 36 | 30 | 25 | 65 |
| T-L | 47 | 27 | 21 | 56 |
| S-L | 38 | 22 | 17 | 20 |

Marked "for information only" in the handbook and must be cited as such. Sufficient to support a
damage tolerance assessment.

## 10. Bottom line

**The fitting passes at MS = +0.156**, with four qualifications a reviewer should see stated rather
than discover:

1. **The contact measurement is now elastic-plastic** (F16), so the elastic lower bound of +0.078
   has been replaced by a measured +0.156. The remaining bias is that the 20x stiff-pin reference
   still bends slightly; the *change* from 0.6809 to 0.7300 is more robust than either absolute.
   F16 ran one mesh and inherits F7's convergence study rather than repeating it.
2. **Worst-case method scatter is still negative** (-0.028), with the double-counting question
   unresolved.
3. **A-basis assumed.** If a redundant load path is demonstrated, B-basis applies.
4. **The margin remains thin enough that the fitting factor matters.** Removing the 1.15 factor
   would raise it substantially; it is retained because FAR 25.625 requires it.

## 11. Open

- [ ] Re-run Melcon-Hoblit at e = 1.900 in for an exact F15 margin
- [ ] Establish the t/D range of Ekvall's specimens to resolve double-counting
- [x] ~~Elastic-plastic contact run to tighten the lower bound~~ — **CLOSED**, F16, `t_eff/t = 0.7300`
- [ ] Re-propagate the F13 tolerance stack exactly at the new +0.156 operating point
- [ ] Mesh-converge the elastic-plastic ratio; F16 ran one mesh and inherits F7's convergence study
- [ ] Confirm whether the installation is single or redundant load path, fixing A vs B basis
- [ ] **F8 safe-life fatigue is not supportable from MIL-HDBK-5J** — Section 3.7.6.2 provides no
      S-N curves for the T73/T7351 temper. Damage tolerance is the appropriate route and the data
      exists: crack-propagation Figures 3.7.6.2.9(a) through (c), plus the K_Ic above.
