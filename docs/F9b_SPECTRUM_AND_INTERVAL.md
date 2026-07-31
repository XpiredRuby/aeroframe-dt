# F9b — Representative Spectrum and Inspection Interval

**Extends `F9_DAMAGE_TOLERANCE.md`**, which produced a parametric life table but stopped short of an
inspection interval because no load spectrum exists for this project.

**This document supplies a representative spectrum so the method runs end to end.**

> ## `SYNTHETIC_SPECTRUM`
> **The spectrum below is constructed, not derived from flight data or a load survey.**
> The interval it produces is a demonstration of method, not a certifiable result. Every assumption
> is stated in §2 and its effect quantified in §5. **Do not quote the interval without the spectrum
> that produced it.**

**Claim boundary:** educational / representative / portfolio only. Non-OEM, non-certified.

---

## 1. Why a spectrum had to be constructed

The Rev C load basis defines **one** case: 9g forward, LC-02. That is an **emergency-landing static
condition** per FAR 25.561 — the aircraft does not experience it repeatedly. It cannot serve as a
fatigue cycle.

A damage tolerance interval requires a flight-by-flight spectrum: cycle types, stress ranges, and
occurrence counts. None exists here.

Three options were considered:

| Option | Assessment |
|---|---|
| Leave parametric | Honest, but the chapter never reaches its purpose |
| Invent a spectrum silently | Unacceptable — the project's value rests on traceable numbers |
| **Construct one, label it, quantify its influence** | **Chosen** |

The third is what a stress engineer does at preliminary design when spectrum data is not yet
available: assume, state, and carry the assumption visibly forward.

## 2. The constructed spectrum

Stress ranges are expressed as **fractions of the limit transverse nominal stress**,
`sigma_limit = 34.98 ksi` (241.2 MPa, thick-lug corrected, from `MARGIN_SUMMARY.md`).

| Block | Cycles per flight | Fraction of limit | dS (ksi) | Rationale |
|---|---|---|---|---|
| **GAG** | 1 | 0.30 | 10.49 | engine off to takeoff thrust and back, once per flight |
| **Manoeuvre** | 10 | 0.15 | 5.25 | normal manoeuvre and thrust changes |
| **Gust / thrust trim** | 100 | 0.05 | 1.75 | small-amplitude, high-count |

**These three fractions and three counts are the assumption.** They are typical of transport
primary structure at preliminary design but are not derived from anything in this project.

## 3. Equivalent-cycle reduction

Under a Paris law, crack growth per cycle scales as `dS^m`. Damage per flight is therefore
proportional to `sum(n_i * dS_i^m)`, and an equivalent single cycle per flight follows from

    dS_eq = ( sum( n_i * dS_i^m ) )^(1/m)

| Block | n | dS | n * dS^4 |
|---|---|---|---|
| GAG | 1 | 10.49 | 1.213e4 |
| Manoeuvre | 10 | 5.25 | 7.580e3 |
| Gust | 100 | 1.75 | 9.357e2 |
| **Equivalent** | **1 / flight** | **11.99** | **2.064e4** |

**`dS_eq = 11.99 ksi` per flight.**

Note the GAG block contributes 59% of the damage despite being one cycle in 111. Under a fourth-
power law, the largest cycle dominates — the 100 gust cycles contribute under 5%.

## 4. Result

Integrating from the rogue flaw `a0 = 0.05 in` to `a_c = 0.1296 in` at `dS_eq`:

    Flights from rogue flaw to critical crack:   1.04e4

| Interval basis | Flights |
|---|---|
| Life / 2 (two inspections in the window) | **5,178** |
| Life / 3 (more conservative) | 3,452 |

**Recommended repeat inspection interval: 5,000 flights**, rounded down, by NDI capable of
reliably detecting a **1.27 mm** flaw at the bore.

The detection threshold is not incidental — it *is* `a0`. If the chosen NDI method cannot reliably
find 1.27 mm, `a0` rises, the window shortens, and the interval must shorten with it.

## 5. Sensitivity — how much the assumption matters

Varying only the GAG fraction, holding the manoeuvre and gust blocks fixed:

| GAG fraction | dS_eq (ksi) | Flights to critical | Interval, life/2 |
|---|---|---|---|
| 0.20 | 10.22 | 1.96e4 | 9,800 |
| 0.25 | 10.95 | 1.49e4 | 7,400 |
| **0.30 (assumed)** | **11.99** | **1.04e4** | **5,200** |
| 0.35 | 13.27 | 6.90e3 | 3,450 |
| 0.40 | 14.71 | 4.56e3 | 2,280 |
| 0.50 | 17.87 | 2.09e3 | 1,050 |

**A GAG fraction between 0.20 and 0.50 spans intervals from 9,800 to 1,050 flights — a factor of
9.3.** The interval is dominated by a single assumed number.

This is the honest headline of the document: **the method is sound, the arithmetic is checkable, and
the answer is only as good as the spectrum.** Obtaining a real spectrum would narrow this more than
any refinement of the crack growth model.

## 6. Uncertainty stack

Ranked by influence on the final interval:

| Source | Effect on interval |
|---|---|
| **GAG fraction** (0.20-0.50) | factor 9.3 |
| **Paris C** (graph-read, factor ~3) | factor 3 |
| **Paris m** (+/-0.5) | factor ~2-4 depending on dS |
| **`F = 1.12`** (simplified K solution) | `a_c` non-conservative; true value smaller |
| **`K_Ic`** min 25 vs avg 30 ksi-sqrt-in | `a_c` varies 3.3 to 4.7 mm |
| Retardation neglected | conservative |

**These do not multiply into a meaningful confidence band.** The result is order-of-magnitude, and
is presented as such.

## 7. What would make this real

1. **A load spectrum** for the pylon attachment. Single largest improvement, by a wide margin.
2. **Paris constants from a digital source** rather than a scanned figure.
3. **A proper K solution** — Bowie or Newman-Raju for a corner crack at a loaded hole, replacing
   `F = 1.12`.
4. **A defined NDI method** with a demonstrated 90/95 detection threshold, fixing `a0` on evidence
   rather than convention.

## 8. Conclusions

1. **Representative interval: 5,000 flights** by NDI at a 1.27 mm threshold, conditional entirely on
   the §2 spectrum.
2. **The GAG cycle dominates.** 59% of damage from 0.9% of cycles. Any spectrum refinement should
   start there.
3. **The interval is assumption-limited, not method-limited.** A factor-of-9 spread from one
   assumed fraction exceeds every other uncertainty in the analysis combined.
4. **Visual inspection remains inadequate.** `a_c = 3.3 mm` is below reliable visual detection
   regardless of interval.
