# F27 — REQ-012 Safe-Life Fatigue — AF-DT-1000

**Claim boundary:** educational / representative / portfolio only. Non-OEM, non-certified.
The spectrum is `SYNTHETIC_SPECTRUM`. **The S/N data is real**, from MMPDS-2026.

**AFDT-REQ-012 has been open since the project began**, closed as *permanently blocked* on the
grounds that no S-N curves exist for the 7075-T7351 temper. That was true, and remains true.
**It stopped applying when F23 changed the material for unrelated reasons.**

**Source: MMPDS-2026, Volume I, Figure 3.7.4.2.8(f)** — best-fit S/N curves for notched, `Kt = 3.0`,
7050-T7451 plate, longitudinal and long transverse, t/4 specimen location.

---

## 1. Why this was blocked, and why it no longer is

MMPDS-2026 §3.7.9.2 covers the T73/T7351 tempers and provides stress-strain, tangent-modulus,
crack-growth and residual-strength data — **and no S/N curves**. 7075 S/N exists only in the **T6**
temper. Two decades of MMPDS submissions did not change that; F21 §3.3 reopened the question and the
answer came back the same.

**The blocker was never "fatigue data does not exist". It was "fatigue data does not exist for this
specific temper".** 7050-T7451 has a full S/N suite, including a notched curve, and the material was
changed to 7050 because 7075 plate is not tabulated thick enough to make the part — a reason with
nothing to do with fatigue.

## 2. The curve

**Figure 3.7.4.2.8(f)**, correlative information:

| | |
|---|---|
| Product form | **Plate, 1.0 to 6.0 in thick** — contains this part's 6.000 in stock |
| Specimen | circumferentially notched, `Kt = 3.0`, 0.253 in net diameter, 0.013 in notch-tip radius |
| Loading | axial, room temperature, air |
| Properties of test material | TUS 75–81 ksi, TYS 65–72 ksi |
| **Equivalent stress equation** | **`log Nf = 10.0 − 3.96 log(Seq)`** |
| | **`Seq = Smax (1−R)^0.64`**, stresses in ksi |
| Heats / lots | 11 |
| Sample size | 79 |
| Std. error of estimate, log(life) | 0.248 |
| **Standard deviation, log(life)** | **0.728** |
| R² | 88% |

The handbook attaches a caution that the equivalent-stress model may give unrealistic predictions
for stress ratios beyond those tested. **That caution is load-bearing here** — see §6.

## 3. Spectrum

Taken unchanged from `F9b_SPECTRUM_AND_INTERVAL.md`, so the safe-life and damage-tolerance
assessments rest on the same loading rather than two different ones:

| Block | Cycles/flight | dS, ksi |
|---|---|---|
| GAG | 1 | 10.49 |
| Manoeuvre | 10 | 5.25 |
| Gust / thrust trim | 100 | 1.75 |

**All three blocks are assumed fully-released, `R = 0`**, so `Smax = dS` and `Seq = dS`. For the GAG
cycle — engine off to takeoff thrust and back — that is close to physical. **For the manoeuvre and
gust blocks it is not**: those oscillate about a non-zero steady thrust level, so their true `R` is
positive. Sensitivity in §5.

## 4. Miner damage

    log Nf = 10.0 - 3.96 log(Seq)

| Block | n | Seq, ksi | N_f | damage/flight | share |
|---|---|---|---|---|---|
| GAG | 1 | 10.49 | 9.07e5 | 1.102e−6 | **57.9%** |
| Manoeuvre | 10 | 5.25 | 1.407e7 | 7.109e−7 | 37.3% |
| Gust | 100 | 1.75 | 1.090e9 | 9.171e−8 | 4.8% |
| **Total** | 111 | | | **1.905e−6** | 100% |

    Damage per flight = 1.905e-6
    Mean life to Miner D = 1  ->  5.25e5 flights

### 4.1 An independent cross-check that fell out for free

**The GAG cycle contributes 57.9% of fatigue damage from 0.9% of the cycles.** `F9b` §3, using a
completely different mechanism — Paris crack growth under a fourth-power law — found the GAG block
contributed **59%**.

Two unrelated damage models, one empirical S/N fit and one fracture-mechanics integration, **agree
to about 1 percentage point on which part of the spectrum matters.** Neither was tuned to the other.

## 5. Safe life

Mean life is not a safe life. Applying the conventional scatter factors:

| Basis | Flights |
|---|---|
| Mean life, Miner D = 1 | 5.25e5 |
| **Scatter factor 4** | **1.31e5** |
| Scatter factor 8 | 6.56e4 |
| −3σ on log life, using the handbook σ of 0.728 (factor 153) | 3.44e3 |

**The −3σ figure is the honest one to look at, and it is brutal.** A log-life standard deviation of
0.728 means the 99.9% survival life is **153 times** below the mean — far more severe than any
conventional scatter factor. That is not a defect in this analysis; it is what the handbook's own
scatter says about notched aluminium fatigue.

**Stress-ratio sensitivity**, varying `R` on all blocks:

| R | Mean life, flights |
|---|---|
| 0.0 | 5.25e5 |
| 0.1 | 4.52e5 |
| 0.2 | 3.82e5 |

**A 27% life reduction across a plausible `R` range** — significant but not order-of-magnitude, and
much smaller than the scatter term.

## 6. What this does and does not establish

**Establishes:** a spectrum-based, mean-stress-corrected, Miner-summed fatigue life on real published
S/N data for the released material, cross-checked against an independent damage mechanism on the
damage distribution. **REQ-012 is satisfied as written** — "fatigue screening shall include a
spectrum mean-stress method and Miner damage."

**Does not establish that this fitting has an adequate fatigue life.** Three reasons, in order of
severity:

1. **The `Kt = 3.0` notched curve is applied to a lug bore whose actual stress concentration under
   transverse loading was never derived.** A circumferentially notched round bar with a 0.013 in
   notch radius is not a 2.000 in bore in a lug. The nominal stress used is the F9b transverse
   nominal. **If the true concentration is higher than 3.0, the life is overstated, and by the
   fourth power of the discrepancy.** This is the dominant uncertainty.
2. **The spectrum is synthetic.** Three block fractions and three counts, assumed at preliminary
   design. F9b §5 already showed the answer is sensitive to the GAG fraction, and §4.1 above shows
   the GAG block dominates in this model too.
3. **Scatter is enormous.** §5.

**Damage tolerance remains the governing route for this fitting**, as F9 and F9b argue and as is
standard for a single-load-path fitting. This analysis supplements it; it does not replace it.

## 7. Limitations

1. **`R = 0` assumed for all blocks.** §3, §5.
2. **`Kt` mismatch between specimen and part.** §6.1 — the largest limitation.
3. **No notch-root plasticity, no local-strain method.** A `Kt = 3.0` bore at these nominal stresses
   would yield locally; nominal-stress S/N does not model that.
4. **No surface-condition correction.** The handbook records the specimen surface as "not
   specified"; the part is machined to Ra 32 µin with no shot peen and no cold expansion, per
   F13 §3.2 and F26.
5. **No size effect.** Specimens are 0.253 in net diameter; the part is 2.500 in thick.
6. **Miner's rule assumes linear damage accumulation and no sequence effect.**
7. **Test material TUS 75–81 ksi** against the A-basis 70 ksi used for static margins — the fatigue
   population is stronger than the design allowable, as is normal for best-fit S/N data, and no
   knock-down for that has been applied.
