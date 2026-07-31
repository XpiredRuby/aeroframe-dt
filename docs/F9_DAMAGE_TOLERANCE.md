# F9 — Damage Tolerance Assessment, AF-DT-1000

**Why damage tolerance and not safe-life fatigue.** MIL-HDBK-5J Section 3.7.6.2 provides **no S-N
curves** for the 7075-T73/T7351 temper — only stress-strain, fatigue-crack-propagation, and
residual-strength data. Safe-life analysis is therefore not supportable for this material from this
source. Damage tolerance is also what FAR 25.571 requires for transport-category primary structure,
and the necessary data does exist.

**Claim boundary:** educational / representative / portfolio only. Non-OEM, non-certified.
**A load spectrum does not exist for this project.** Life results below are therefore **parametric**,
not a certified life.

---

## 1. Inputs

### Fracture toughness — from MIL-HDBK-5J Table 3.1.2.1.6

7075-T7351 plate, `K_Ic` in ksi-sqrt(in):

| Orientation | Max | Avg | **Min** | Samples |
|---|---|---|---|---|
| L-T | 36 | 30 | **25** | 65 |
| T-L | 47 | 27 | 21 | 56 |
| S-L | 38 | 22 | 17 | 20 |

**`K_Ic = 25 ksi-sqrt(in)` used** — the L-T minimum, matching the chosen grain orientation
(lug axis L, transverse load LT, so a crack growing across the ligament is L-T).

The handbook marks these **"for information only"**. They are used here on that basis and must be
cited as such — they are not design allowables.

### Crack growth rate — read from MIL-HDBK-5J Figure 3.7.6.2.9(b), page 3-424

0.500-inch 7075-T7351 plate, L-T, M(T) specimens, room temperature, 50-95% RH,
**R = 0.10-0.11** band (5 specimens, 316 data points).

Two points read off the fitted line: `(3, 3e-7)` and `(30, 3e-3)`.

    da/dN = C (dK)^m       m = 4.00       C = 3.7e-9      (in/cycle, ksi-sqrt-in)

Spot checks against the plotted band:

| dK | da/dN from fit |
|---|---|
| 5 | 2.3e-6 |
| 10 | 3.7e-5 |
| 20 | 5.9e-4 |
| 40 | 9.5e-3 |

**These constants are read off a scanned log-log figure with a scattered data band.** Realistic
uncertainty is roughly **+/-0.5 on m and a factor of ~3 on C**. Because life scales as `1/C` and as
`dS^-m`, **predicted lives carry order-of-magnitude uncertainty** and are indicative only.

### Stresses

From `MARGIN_SUMMARY.md`, nominal stresses with the thick-lug correction `t_eff/t = 0.681`:

    axial       144.7 MPa = 20.99 ksi
    transverse  241.2 MPa = 34.98 ksi   <- governs

## 2. Critical crack size — the robust result

    a_c = (1/pi) * (K_Ic / (F * sigma))^2      with F = 1.12

| Driving stress | sigma | **a_c** |
|---|---|---|
| **Transverse (governs)** | 34.98 ksi | **0.1296 in = 3.29 mm** |
| Axial | 20.99 ksi | 0.3601 in = 9.15 mm |

**Ligament from bore to free edge: 38.1 mm.**

**The critical crack is 3.3 mm — only 8.6% of the available ligament.**

This result depends only on the tabulated `K_Ic` and the computed stress. It does **not** depend on
the graph-read Paris constants, so it is the most defensible number in this document.

**Engineering significance:** the fitting reaches unstable fracture at a crack far smaller than the
geometry might suggest. A 3.3 mm crack at a bore is near the practical limit of routine visual
inspection and would normally require eddy-current or equivalent NDI. **This drives the inspection
method, not just the interval.**

## 3. Crack growth life — parametric

Rogue-flaw initial size `a0 = 0.05 in = 1.27 mm`, standard damage-tolerance practice for a flaw at
a fastener or pin hole. Grown to `a_c = 0.1296 in`.

    N = (1 / (C * F^m * pi^(m/2) * dS^m)) * integral[a0..ac] a^(-m/2) da

| Cyclic stress range dS (ksi) | Cycles to failure |
|---|---|
| 34.98 (full limit range) | 1.4e2 |
| 20 | 1.3e3 |
| 10 | 2.1e4 |
| 5 | 3.4e5 |
| 3 | 2.6e6 |
| 2 | 1.3e7 |

**Life scales as `dS^-4`.** Halving the cyclic stress range multiplies life by 16.

### The 143-cycle figure is not a fatigue result

The 34.98 ksi row cycles the part over its **full limit-load range**. That load case is a 9g
emergency-landing condition per the Rev C load basis — a **static** case, not a repeated one. An
aircraft does not see it cyclically. The row is included only to bound the table.

**Realistic ground-air-ground stress ranges for a pylon fitting would be a few ksi**, placing the
life in the 10^5 to 10^7 range. But that is an inference, not a calculation, because:

## 4. The blocking limitation — no load spectrum

This project defines **one** load case: 9g forward, LC-02. A damage tolerance life requires a
**flight-by-flight load spectrum** — GAG cycles, manoeuvre, gust, thrust cycling, with occurrence
counts. None of that exists here.

**No single life number is therefore quoted.** The parametric table above is the honest output.
Producing a certified inspection interval would require:

1. A load spectrum for the pylon attachment
2. Cycle counting (rainflow) to a stress-range histogram
3. Crack growth integration under that spectrum, with retardation modelling
4. An inspection interval set at a fraction of the resulting life

Items 2 through 4 are mechanical once item 1 exists.

## 5. Limitations, stated plainly

- **Paris constants are graph-read.** Factor-of-3 uncertainty on C, +/-0.5 on m. Lives are
  order-of-magnitude indicative.
- **`K_Ic` is "information only"** per MIL-HDBK-5J, not a design allowable.
- **Simplified K solution.** `K = F*sigma*sqrt(pi*a)` with `F = 1.12` — a free-surface factor for a
  through crack. A real lug analysis would use a Bowie or Newman-Raju solution accounting for the
  hole and finite ligament, and for a corner rather than through crack. `F` near the bore is higher
  than 1.12, so **the quoted `a_c` is non-conservative** and a proper solution would give a smaller
  critical crack.
- **Through crack assumed.** A corner crack at the bore, the more likely initiation geometry, has a
  different K solution and a different early growth rate.
- **R-ratio fixed at 0.10.** The figure also provides R = 0.25-0.31 and R = 0.44-0.50 bands. Higher
  R gives faster growth; a real spectrum would need the appropriate band or a Walker correction.
- **No retardation.** Overloads in a real spectrum retard growth, so a constant-amplitude
  integration is conservative in that respect.

## 6. Conclusions

1. **Critical crack size is 3.3 mm** under the governing transverse stress — 8.6% of the ligament.
   This is the solid result and does not depend on the graph-read constants.
2. **NDI is required, not visual inspection.** A 3.3 mm critical crack at a bore is too small for
   reliable visual detection.
3. **Life scales as the fourth power of stress range**, so the inspection interval is extremely
   sensitive to the spectrum — which does not exist for this project.
4. **F8 safe-life fatigue is not supportable** for 7075-T7351 from MIL-HDBK-5J. This document
   replaces it rather than supplementing it.
5. **The critical crack size is another consequence of the thick-lug correction.** Without it, the
   transverse stress would be 164.2 MPa rather than 241.2 MPa and `a_c` would be 7.1 mm — more than
   double. The correction more than halves the tolerable flaw.

## 7. Open

- [ ] Load spectrum for the pylon attachment — the single blocking item
- [ ] Bowie or Newman-Raju K solution for a corner crack at the bore, replacing `F = 1.12`
- [ ] Read the R = 0.25-0.31 and R = 0.44-0.50 bands and apply a Walker correction
- [ ] Confirm Paris constants against an independent source rather than a single graph read
- [ ] Establish the NDI method and its reliable detection threshold, then set the interval
