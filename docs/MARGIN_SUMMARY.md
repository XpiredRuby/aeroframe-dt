# AF-DT-1000 — Margin Summary (single source of truth)

**This document supersedes the margin figure quoted anywhere else in the repository.**
Where an older document states +0.710 without qualification, it is stating the **uncorrected
thin-lug value**, which is now known to be optimistic.

**Governing margin: `MS = +0.165`**

**Claim boundary:** educational / representative / portfolio only. Non-OEM, non-certified.
All numbers `SYNTHETIC_TEST_ONLY`.

---

## 1. The chain

| Stage | MS | Source |
|---|---|---|
| Melcon-Hoblit, thin-lug method | +0.710 | `F5_..._revD.md` |
| Reconstructed independently on a stress basis | +0.7104 | `F5_MARGIN_CROSSCHECK.md` |
| **Corrected for thick-lug bearing distribution** | **+0.165** | `F7_CONTACT_THICK_LUG.md` |

The correction is not a refinement. It is the removal of an assumption that does not hold for this
part.

## 2. Why the thin-lug value was wrong

The Melcon-Hoblit method assumes bearing pressure is **uniform through the lug thickness**. That is
reasonable for a thin lug. **This lug is at t/D = 1.25**, roughly double the t/D ~ 0.6 above which
pin bending normally warrants assessment.

F7 measured the actual distribution by contact FE, using a ratio method that cancels the
clearance-induced circumferential concentration and the contact-edge singularity:

    t_eff / t = p_max(stiff pin) / p_max(real pin) = 0.681

Converged over three mesh densities (21.7k / 58.8k / 203.5k nodes), ratio moving 8.2% total while
the underlying absolute pressures diverged 134%.

Bearing concentrates into **68% of the thickness**. The nominal stresses rise by `1/0.681`, and:

    Ra  = 0.3578    (thin-lug value 0.2437)
    Rtr = 0.7195    (thin-lug value 0.4899)
    MS  = +0.165    (thin-lug value +0.710)

**The thin-lug method was optimistic by a factor of 4.3 on margin.**

## 3. Sensitivities on the corrected margin

| Case | MS | Note |
|---|---|---|
| **Baseline, corrected** | **+0.165** | governing |
| Ftux = Ftu (as assumed) | +0.165 | Ftux has never had a proper basis |
| **Ftux -10%** | **+0.074** | still positive, thin |
| Zero-margin threshold | 0.000 | occurs at t_eff/t = 0.585 |

`t_eff/t = 0.681` sits above the 0.585 failure threshold, but the band is **0.096 wide**, not the
comfortable margin the thin-lug value implied.

## 4. Ekvall correlation band, re-propagated

Ekvall's 243 lug tests give predicted/test ratios of 0.85 to 1.19, mean 1.003
(`F12_CORRELATION_AF-DT-1000.md`). Allowable scales as `1/r`, so `(1 + MS)` scales as `1/r`.

| Ekvall ratio | On +0.710 (old) | **On +0.165 (corrected)** |
|---|---|---|
| Best, r = 0.85 | +1.012 | **+0.370** |
| Mean, r = 1.003 | +0.705 | **+0.161** |
| **Worst, r = 1.19** | **+0.437** | **-0.021** |

**At Ekvall's worst-case method scatter the corrected margin is marginally negative.**

Under the thin-lug value the margin stayed positive across the entire validated band. It no longer
does.

### Important caveat on this stack

**This may be double-counting, and should not be quoted without the qualification.**

Ekvall's scatter band was derived from 243 physical lug tests across 24 materials. If any of those
specimens were thick lugs, **the thick-lug effect is already partly inside the measured scatter**.
Applying the full thick-lug correction and then the full worst-case scatter on top may penalise the
same physical effect twice.

Resolving this requires the Ekvall paper to establish the t/D range of his specimen set. Until
then, the honest statement is:

- **Best estimate: MS = +0.165.** The part passes.
- **Worst-case stack: MS = -0.021.** Possibly conservative by double-counting, but not dismissible.

## 5. Effect on the F15 nonconformance case

`F15_NONCONFORMANCE_RCCA_AF-DT-1000.md` assesses a mis-drilled bore with edge distance reduced
2.500 -> 1.900 in, and recorded the margin falling +0.710 -> +0.220, with disposition **REWORK**
justified because at Ekvall's worst ratio it fell to only +0.025.

Scaling by the same `(1 + MS)` factor:

    corrected mis-drilled margin ~ -0.169

**The nonconformance case is negative under the thick-lug correction**, before any Ekvall scatter is
applied at all.

**This strengthens the REWORK disposition** — it is no longer a marginal call, it is a clear
failure. But it also means the original justification understated the severity.

**This figure is approximate.** It scales the corrected baseline by the ratio the original analysis
found, rather than re-running the Melcon-Hoblit method at e = 1.900 in. The `Kt`, `Ktru` and `Kbr`
factors all depend on e/D and would need re-reading from the curves. `t_eff/t = 0.681` should carry
over unchanged, since it depends on pin bending — a function of t and D, not e — but the
interaction is not exactly linear. **A proper recomputation is an open item.**

## 6. What is still true

The corrected margin does not change these:

- **Equilibrium verified** to 0.006% in the Rev D linear elastic run
- **Bore is the critical location**, confirmed by FE, which is where the lug method applies
- **Pin bending governs the pin** at ~780 MPa, requiring a high-strength steel pin
  (`F6_PIN_BENDING_THICK_LUG.md`)
- **The hand method is internally consistent** and reconstructible from first principles to 0.06%
  (`F5_MARGIN_CROSSCHECK.md`)
- **Nominal stresses are modest** — bearing 191.5 MPa, net section 98.5 MPa, against Ftu ~ 489 MPa

The part is not grossly undersized. The issue is that the **method** used to substantiate it did
not hold for this geometry, and correcting that consumes most of the reported margin.

## 7. Bottom line

**The fitting passes at MS = +0.165**, with three qualifications that a reviewer should see stated
rather than discovered:

1. That figure depends on a **linear elastic** contact measurement. Real yielding would flatten the
   pressure peak and raise `t_eff`, so **+0.165 is a lower bound**; the true value lies between
   +0.165 and +0.710.
2. **Worst-case method scatter takes it marginally negative** (-0.021), with a possible
   double-counting caveat that cannot be resolved without the Ekvall paper.
3. **Ftux has no proper basis.** A 10% reduction leaves +0.074. MIL-HDBK-5J would fix this and is
   freely available.

## 8. Open

- [ ] Re-run Melcon-Hoblit at e = 1.900 in for an exact F15 nonconformance margin
- [ ] Establish the t/D range of Ekvall's specimen set to resolve the double-counting question
- [ ] Ftux from MIL-HDBK-5J transverse allowables, replacing the Ftux = Ftu placeholder
- [ ] A/B-basis allowables from MIL-HDBK-5J, replacing the representative Ftu ~ 71 ksi
- [ ] Elastic-plastic contact run to recover the yielding benefit and tighten the lower bound
