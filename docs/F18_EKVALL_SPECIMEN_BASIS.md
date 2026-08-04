# F18 — Ekvall Specimen Basis and Method Scatter — AF-DT-1000

**Closes the longest-standing open item in this project.** `MARGIN_SUMMARY.md` has carried a
double-counting question since the thick-lug correction was applied: does the Ekvall correlation
band already contain the thick-lug effect, such that applying both penalises the same physics
twice? It was recorded as unresolvable without the source paper.

**The paper was obtained and read in full on 2026-08-04. The question is resolved.**

**Source:** Ekvall, J.C., "Static Strength Analysis of Pin-Loaded Lugs," *Journal of Aircraft*,
Vol. 23, No. 5, May 1986, pp. 438–443. Referred to as R4 in the stress report.

**Claim boundary:** educational / representative / portfolio only. Non-OEM, non-certified.

---

## 1. Answer

**The double-counting is real, but it cannot be quantified.**

| Question | Answer |
|---|---|
| Does the specimen set include lugs as thick as ours? | **Yes** |
| Does the method contain any thickness-dependent term? | **No** |
| Can the overlap be quantified? | **No** — the `t/D` distribution is not reported |

**Consequence: the negative worst case is a conservative bound, not a best estimate.** That is a
weaker statement than "the worst case is positive," and it is the strongest statement the source
supports.

## 2. Specimen range — the fitting is inside it

The correlation section states the parameter ranges covered by the tests:

| Parameter | Range |
|---|---|
| Lug hole diameter | 0.25 – 2.85 in |
| Material thickness | 0.049 – 2.125 in |
| **`D/t`** | **0.76 – 10.2** |
| `W/D` | 1.33 – 4.5 |
| `2a/W` | 0.73 – 2.0 |

Inverting the third row:

    t/D  =  0.098  to  1.316

**AF-DT-1000 sits at `t/D = 1.250`, i.e. `D/t = 0.800`.** That is inside the range, at **95% of the
way to the thickest specimen in the set**. Our `W/D = 2.00` and `2a/W = 1.0` are also comfortably
inside their ranges.

**This is printed in the paper's prose, not read from a figure**, so it carries no digitisation
uncertainty.

## 3. The method has no thickness term

The predicted failure load is

    P = D * t * K_BR * F_tu

with the bearing efficiency factor defined by inverting that same expression against test data,
`K_BR = P/(D t F_tu)`. `K_BR` is obtained from the elastic stress concentration factor `K_tb`, which
is a function of `W/D` and lug eccentricity only — the axially loaded straight-lug relation is
`K_tb = 2.75 (W/D − 1)^−0.675`, with taper and load-angle variants of the same form.

**Thickness enters only as the gross `t` in the denominator, linearly, and nowhere else.**

That is the crux. `K_BR` was **fitted to physical test results using the full lug thickness**. If
the specimens carried real through-thickness bearing non-uniformity, that effect had nowhere to go
except into the fitted `K_BR` values and the scatter about the fitted curve.

**Applying our own `t_eff/t` correction to an allowable derived from `K_BR` therefore applies the
same physical effect a second time. This follows from the construction of the method, not from a
coincidence of specimen selection.**

### 3.1 The pins were elastic and of the same stiffness class as ours

All evaluated tests used **solid steel pins**. One reference (R4's Ref. 10) tested pins across
Rockwell C 18–46.5, and **only the maximum-strength pins from that reference were retained** in the
correlation; the low-hardness pins deformed severely and those results were excluded.

**A hardness range is a yield-strength range, not a modulus range.** All solid steel pins have
`E ≈ 200 GPa` regardless of heat treatment. So the retained specimens used pins that bent
**elastically**, exactly as the 4340 pin in our F7 and F16 models does.

The paper reports that varying pin bending deformation reduced ultimate strength by at most 14%
across seven lug-test groups, concluding pin deflection is not a large effect for ductile materials.

> **That 14% is not comparable to our 37%, and an earlier reading of this project treated it as
> though it were.** The 14% is the *additional* penalty from a pin going plastic and deforming
> severely, measured against hard pins that stayed elastic. Our `1/0.730 = 1.370` is the effect of
> an elastic steel pin measured against a **rigid** reference. Different baselines, different
> quantities. The correction is recorded here so the error does not propagate.

The paper separately notes twice that differences in modulus between pin and lug have only a small
effect on the elastic stress concentration factor.

## 4. Why the overlap cannot be quantified

Table 2 of the source summarises the 263 tests by **lug type (`2a/W` band) and loading angle**.
It does not break the set down by thickness, `t/D`, or `D/t`. No other table or figure does either.

**The range is reported; the distribution is not.** Without knowing how many of the 243 correlated
tests sat at high `t/D`, and how their residuals were distributed, no defensible fraction of the
scatter band can be attributed to thick-lug effects.

**So no numerical double-count credit is taken.** The full thick-lug correction and the full
method-scatter band both continue to be applied. What changes is that this is now known to be
**conservative**, with a stated reason, rather than of unknown direction.

## 5. Method scatter, restated on a proper statistical basis

This is the second finding, and it was not expected.

The project has been quoting the correlation band as "predicted/test 0.85 to 1.19", the observed
extremes. The source gives a full statistical characterisation:

| | |
|---|---|
| Distribution | approximately normal |
| Mean, test/predicted | **1.003** |
| Standard deviation | **0.065** |
| Predictions | 224, covering 243 tests |

and two one-sided tolerance limit factors on predicted load:

| Multiplying factor | Statement |
|---|---|
| **0.910** | at least 90% of test values exceed the predicted value, 95% confidence |
| **0.837** | at least 99% of test values exceed the predicted value, 95% confidence |

Inverting to the predicted/test convention this project uses:

| Basis | factor | pred/test | **MS** |
|---|---|---|---|
| Mean | 1.003 | 1.003 | +0.153 |
| 90% probability, 95% confidence | 0.910 | ≤ 1.099 | **+0.052** |
| **99% probability, 95% confidence** | **0.837** | **≤ 1.195** | **−0.032** |
| Observed extreme (previously used) | — | 1.19 | −0.028 |

### 5.1 Why this matters more than the numbers moving

**99% probability with 95% confidence is the definition of A-basis.** This project uses A-basis
allowables. **The statistically consistent method-scatter pairing is therefore 1.195** — which is
essentially the 1.19 the project has been carrying.

The negative worst case was never an arbitrary extreme. It is the A-basis-consistent tolerance
limit, and it should be quoted as such. The figure moves marginally, from −0.028 to **−0.032**,
because the tolerance limit is slightly more severe than the worst observed ratio.

It also produces a clean B-basis-consistent statement that did not exist before: **at 90%
probability and 95% confidence the margin is +0.052, positive.** If a redundant load path is ever
demonstrated, B-basis allowables and the 90%/95% scatter limit pair correctly and the margin is
positive under both.

## 6. Two caveats that cut against us

Recorded here rather than left for a reviewer to find.

**Localized bearing failures were excluded from the correlation.** The source states that bearing
failures occurred in two of the referenced test programmes and that those results were not included
in the evaluation; Table 1's footnote confirms the counts cover only tension and shear-bearing
failures. **Our governing mode is combined bearing / transverse at the bore.** The 0.85–1.19 band
was therefore fitted on a dataset that deliberately excluded a failure mode adjacent to ours. This
does not invalidate using the band, but it limits how well it characterises scatter for our case,
and the method is explicitly stated not to account for localized bearing failure.

**Our lug is thicker in absolute terms than any specimen in the set.** `t = 2.500 in` against a
maximum specimen thickness of 2.125 in. `t/D` is inside range because our hole is large, but no
specimen was this thick. Absolute thickness governs quench rate and through-thickness property
gradients in 7xxx plate, which is why MIL-HDBK-5J tabulates allowables by thickness band at all.
**The `t/D` similarity is real; the absolute-thickness similarity is not.**

## 7. What changes in the released documents

| Document | Change |
|---|---|
| `MARGIN_SUMMARY.md` §5 | Ekvall band restated on tolerance limits; worst case −0.028 → **−0.032**; double-counting item closed as resolved-directional |
| `STRESS_REPORT_AF-DT-1000.md` §6.4 | same, and the open item removed from §13 |
| Open items | "Establish the t/D range of Ekvall's specimens" — **CLOSED** |

**The governing margin `MS = +0.156` is unchanged.** Nothing in this document alters the nominal
result; it changes what can be said about the scatter around it.

## 8. Limitations

1. **No quantified credit is taken**, because the `t/D` distribution is unavailable — §4.
2. **The tolerance limits are the source's own**, computed on its 224-prediction set. They are
   applied here to a different method (Melcon-Hoblit) as a proxy for method scatter, which is the
   same approximation this project has always made in using the band at all.
3. **The excluded bearing-failure mode** limits applicability to our governing mode — §6.
4. **Absolute thickness exceeds the specimen set** — §6.
5. **Eccentricity correction scatter is a component, not additional.** The source reports about
   ±12% scatter about its eccentricity correction curves; that is already inside the overall band
   and is not stacked separately here.
