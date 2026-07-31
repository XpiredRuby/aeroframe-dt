# F9 — Damage Tolerance Assessment, AF-DT-1000

**Why damage tolerance and not safe-life fatigue.** MIL-HDBK-5J Section 3.7.6.2 provides **no S-N
curves** for the 7075-T73/T7351 temper — only stress-strain, fatigue-crack-propagation, and
residual-strength data. Safe-life analysis is therefore not supportable for this material from this
source. Damage tolerance is also what FAR 25.571 requires for transport-category primary structure,
and the necessary data exists.

**Adopted results (see §5 for the reconciliation that fixed them):**

    critical crack size   a_c = 3.07 mm
    growth life           9.41e3 flights at the F9b spectrum

**Claim boundary:** educational / representative / portfolio only. Non-OEM, non-certified.
**A load spectrum does not exist for this project.** See `F9b_SPECTRUM_AND_INTERVAL.md`.

---

## 1. Inputs

### Fracture toughness — MIL-HDBK-5J Table 3.1.2.1.6

7075-T7351 plate, `K_Ic` in ksi-sqrt(in):

| Orientation | Max | Avg | **Min** | Samples |
|---|---|---|---|---|
| L-T | 36 | 30 | **25** | 65 |
| T-L | 47 | 27 | 21 | 56 |
| S-L | 38 | 22 | 17 | 20 |

**`K_Ic = 25 ksi-sqrt(in)` used** — the L-T minimum, matching the chosen grain orientation
(lug axis L, transverse load LT, so a crack across the ligament is L-T).

The handbook marks these **"for information only"**. Used on that basis; they are not design
allowables.

### Crack growth rate — MIL-HDBK-5J Figure 3.7.6.2.9(b), page 3-424

0.500-inch 7075-T7351 plate, L-T, M(T) specimens, RT, 50-95% RH, **R = 0.10-0.11** band
(5 specimens, 316 data points). Two points read off the fitted line: `(3, 3e-7)` and `(30, 3e-3)`.

    da/dN = C (dK)^m       m = 4.00       C = 3.7e-9      (in/cycle, ksi-sqrt-in)
    SI equivalent:         C_SI = 6.447e-35              (m/cycle, Pa-sqrt-m)

| dK (ksi-sqrt-in) | da/dN from fit (in/cyc) |
|---|---|
| 5 | 2.3e-6 |
| 10 | 3.7e-5 |
| 20 | 5.9e-4 |
| 40 | 9.5e-3 |

**Read off a scanned log-log figure with a scattered band.** Realistic uncertainty **+/-0.5 on m,
factor ~3 on C**. Life scales as `1/C` and `dS^-m`, so **predicted lives are order-of-magnitude**.

### Stresses

From `MARGIN_SUMMARY.md`, with the thick-lug correction `t_eff/t = 0.681`:

    axial       144.7 MPa = 20.99 ksi
    transverse  241.2 MPa = 34.98 ksi   <- governs

### Geometry

Crack modelled as growing from the bore radially into the ligament.
**Ligament bore-to-free-edge = 38.1 mm**, taken as the effective width `W`.

## 2. Critical crack size — the robust result

    a_c = 3.07 mm       (0.1208 in)

**`a_c` is 8.1% of the available ligament.**

Solved from `K = Y(a/W) * sigma * sqrt(pi*a) = K_Ic` using the finite-width edge-crack geometry
factor (§5). Depends only on tabulated toughness, computed stress and geometry — **not** on the
graph-read Paris constants. This is the most defensible number in the document.

**Engineering significance:** the fitting reaches unstable fracture at a crack far smaller than the
geometry suggests. A 3 mm crack at a bore is at or below the practical limit of routine visual
inspection and requires eddy-current or equivalent NDI. **This drives the inspection method, not
just the interval.**

**`a_c` is itself a consequence of the thick-lug correction.** Uncorrected, the transverse stress
would be 164.2 MPa and `a_c` about 6.6 mm — more than double. The correction more than halves the
tolerable flaw.

## 3. Crack growth life — parametric

Rogue-flaw initial size `a0 = 0.05 in = 1.27 mm`, standard damage-tolerance practice for a flaw at
a pin or fastener hole. Integrated numerically to `a_c`.

| Cyclic stress range dS (ksi) | Cycles to failure |
|---|---|
| 34.98 (full limit range) | ~1.3e2 |
| 20 | ~1.2e3 |
| 11.99 (F9b spectrum equivalent) | **9.41e3** |
| 10 | ~1.9e4 |
| 5 | ~3.1e5 |
| 3 | ~2.4e6 |

**Life scales as `dS^-4`.** Halving the cyclic stress range multiplies life by 16.

### The 130-cycle figure is not a fatigue result

That row cycles the part over its **full limit-load range** — a 9g emergency-landing condition,
a **static** case. Aircraft do not see it repeatedly. Included only to bound the table.

## 4. The blocking limitation — no load spectrum

This project defines **one** load case: 9g forward, LC-02. A damage tolerance life requires a
flight-by-flight spectrum with occurrence counts. None exists.

A representative spectrum is constructed in `F9b_SPECTRUM_AND_INTERVAL.md`, clearly labelled
`SYNTHETIC_SPECTRUM`, so the method runs end to end.

## 5. Independent implementation cross-check

The first version of this analysis used a **constant geometry factor `F = 1.12`** — the
`a/W -> 0` limit for an edge crack. Its §5 limitations recorded:

> *"F near the bore is higher than 1.12, so the quoted `a_c` is non-conservative and a proper
> solution would give a smaller critical crack."*

That was then tested against `src/aeroframe_dt/fatigue.py`, an implementation already present in
this repository and written independently of this analysis. It uses the full finite-width
edge-crack polynomial:

    Y(a/W) = 1.12 - 0.231x + 10.55x^2 - 21.72x^3 + 30.39x^4        x = a/W

| a/W | a (mm) | Y |
|---|---|---|
| 0.010 | 0.38 | 1.119 |
| 0.050 | 1.91 | 1.132 |
| **0.081** | **3.07** | **1.164** |
| 0.100 | 3.81 | 1.184 |
| 0.200 | 7.62 | 1.371 |

### Result of the comparison

| Quantity | Hand calc, F = 1.12 | Repo, finite-width Y | Difference |
|---|---|---|---|
| Critical crack `a_c` | 3.29 mm | **3.07 mm** | 7% |
| Life at `dS_eq = 11.99 ksi` | 1.04e4 | **9.41e3** | 10% |

**Two independent implementations agree to within 10%**, and **the discrepancy went in the
direction predicted before the comparison was made.** The stated non-conservatism was real and its
magnitude is now quantified.

**The repo values are adopted** throughout this document and in the stress report. They are the more
rigorous of the two — the finite-width correction is physically real and grows as the crack extends.

**No conclusion changes.** Critical crack remains ~3 mm, NDI remains mandatory, and the interval
shifts by less than the spectrum uncertainty already documented in F9b.

## 6. Limitations

- **Paris constants are graph-read.** Factor-3 uncertainty on C, +/-0.5 on m. Lives are
  order-of-magnitude indicative.
- **`K_Ic` is "information only"** per MIL-HDBK-5J, not a design allowable.
- **Edge-crack model.** The finite-width polynomial in §5 is for a single edge crack in a plate. A
  lug has a **loaded** hole, and the real solution would be Bowie or Newman-Raju, accounting for
  pin bearing pressure on the crack faces. That remains an approximation, though a better one than
  the constant `F` it replaced.
- **Through crack assumed.** A corner crack at the bore — the more likely initiation geometry —
  has a different K solution and different early growth.
- **R-ratio fixed at 0.10.** The figure also gives R = 0.25-0.31 and 0.44-0.50. Higher R grows
  faster; a real spectrum needs the right band or a Walker correction.
- **No retardation.** Overloads retard growth, so constant-amplitude integration is conservative
  in that respect.

## 7. Conclusions

1. **Critical crack size is 3.07 mm** under the governing transverse stress — 8.1% of the ligament.
   Independent of the graph-read constants.
2. **NDI is required.** A 3 mm critical crack at a bore is not reliably detectable visually.
3. **Life scales as the fourth power of stress range**, so the interval is dominated by the
   spectrum — which does not exist for this project.
4. **F8 safe-life fatigue is not supportable** for 7075-T7351 from MIL-HDBK-5J. This document
   replaces it rather than supplementing it.
5. **Two independent implementations agree within 10%**, with the difference explained and its
   direction predicted in advance.

## 8. Open

- [ ] Load spectrum for the pylon attachment — the single blocking item
- [ ] Bowie or Newman-Raju K solution for a corner crack at a **loaded** hole
- [ ] Read the R = 0.25-0.31 and 0.44-0.50 bands, apply a Walker correction
- [ ] Confirm Paris constants against a digital source rather than a graph read
- [ ] Establish the NDI method and its 90/95 detection threshold, fixing `a0` on evidence
