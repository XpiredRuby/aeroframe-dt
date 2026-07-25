# F12 Public-Data Correlation — AF-DT-1000

**Decision ID:** F12-AFDT-1000-revA
**Purpose:** Anchor the AF-DT-1000 hand-calc margin to published experimental lug data, so the
predicted margin carries a quantified, literature-backed confidence — not just an internal number.
**Claim boundary:** educational / representative / portfolio only. Non-OEM, non-certified.
All AF-DT-1000 values `SYNTHETIC_TEST_ONLY`. Cited experimental values are from public literature
and belong to their authors.

---

## 1. Why F12 exists

Every margin in this project so far is *self-consistent* — the hand calc agrees with the source
spreadsheet, and (pending) will agree with FE. But self-consistency is not the same as being
*right about the real world*. F12 closes that gap: it ties the method used here to a body of
**real lug tests that were loaded to failure**, and asks a single question —

> When this class of method predicts a lug's failure load, how close is it to the load the lug
> actually broke at?

If the method has a known, tight accuracy band against hundreds of real failures, then the
AF-DT-1000 margin inherits that same accuracy band. That is the correlation.

---

## 2. Primary correlation source — Ekvall (1986)

**Ekvall, J. C., "Static Strength Analysis of Pin-Loaded Lugs," Journal of Aircraft, Vol. 23,
No. 5, May 1986, pp. 438-443. Lockheed-California Company.**

This is the canonical validation of the pin-loaded-lug static strength method. It is the same
method lineage used in this project: the axial analysis originates in Cozzone-Melcon-Hoblit
(1950), the oblique/transverse analysis in Melcon-Hoblit (1953), and both feed the Air Force
manual (AFFDL-TR-69-42) and NASA TM X-73305 that the AA-SM-009 spreadsheets digitize.

Key published result:

| Quantity | Value |
|---|---|
| Number of lug tests | 243 |
| Number of materials | 24 |
| Predicted load / test load — range | 0.85 to 1.19 |
| Predicted load / test load — **mean** | **1.003** |

In words: across 243 real lugs loaded to destruction in 24 different materials, this method's
predicted failure load landed on average within **0.3%** of the actual break load, and never
worse than about ±19%. That is the accuracy envelope the AF-DT-1000 prediction sits inside.

The method is directly applicable here: the paper covers straight and tapered lugs, tension and
shear-bearing failure, and accounts for lug eccentricity and loading angle — matching the
AF-DT-1000 case (straight lug, oblique 59° load, shear-out/bearing regime at e/D = 1.25).

---

## 3. Correlation result — margin confidence band

The AF-DT-1000 governing margin is **M.S. = +0.71** (F5 rev D), i.e. predicted capacity /
applied ultimate load = 1.71.

Applying the Ekvall accuracy envelope to that prediction — treating the predicted/test ratio as
the uncertainty on the predicted capacity — gives the band of *true* margins consistent with the
method's historical performance:

| Method performance | Pred/test ratio | Implied true AF-DT-1000 M.S. |
|---|---|---|
| Worst historical over-prediction | 1.19 | **+0.44** |
| Mean (best estimate) | 1.003 | **+0.70** |
| Best historical under-prediction | 0.85 | **+1.01** |

**The margin stays positive across the entire validated band.** Even if the method were as
optimistic for this lug as the single most optimistic case in 243 tests, the fitting still holds
a +0.44 margin. This is the substantive F12 outcome: the AF-DT-1000 static substantiation is not
merely internally consistent, it is robust against the documented real-world scatter of the
method itself.

---

## 4. What is proven, and what is not

**Proven (software, this document):**
- The method used for AF-DT-1000 has a peer-reviewed accuracy of mean 1.003 against 243 real
  failures.
- Propagated through the AF-DT-1000 prediction, that accuracy leaves the margin positive
  (+0.44 worst case, +0.70 expected).

**Not proven here — requires the FE step (F12 Piece 2, needs Ansys):**
- A *modeled* predicted-vs-published break-load comparison for a single specimen.
- For this, rebuild the Ekvall-class nominal parametric lug used in the IAF study
  (Shiroky et al., IAF): straight 7075-T651 lug, D = 26.8 mm, t = 25 mm, e/D swept 1-2,
  axial load 64 000 lbf, with published margin-vs-e/D curves (their Figs 9-11, which are
  internally self-consistent). Running that model and matching its published margin curve gives
  the predicted-vs-published plot.
- Material card for that model: Ftu 75 000 psi, Fty = Fcy 68 000 psi, Fsu 44 000 psi,
  E 1.03e6 psi, nu 0.33, bilinear stress-strain, yield strain 0.07.

---

## 5. Source-quality note (honesty record)

The IAF paper (Shiroky et al., "An Innovative Method for Lug Strength Analysis," Israel Air
Force) was reviewed as a candidate single-specimen target. Its headline nominal experiment
reports "predicted 3850 lbf, actual 3900 kgf, within 1%." These two figures are a factor of ~2.2
apart (3900 kgf = 8598 lbf); the ~1% agreement only holds if both are the same unit, so the
paper contains a unit-labelling error in that line. Its stated e/D = 1.26 also does not follow
from its quoted D = 15.88, e = 40 mm (that gives e/D = 2.5), indicating an `e` vs edge-distance
definition mismatch. Because of these internal inconsistencies, that specific experiment is
**not** used as the correlation anchor. The paper's *nominal parametric case* (Figs 9-11) is
self-consistent and is retained only as the geometry basis for the optional FE cross-check in §4.
The statistical correlation in §3 rests entirely on Ekvall (1986), which has no such issues.

---

## 6. Status

F12 Piece 1 (statistical correlation to published test data) is **complete**. The AF-DT-1000
margin is correlated to 243 real lug failures via Ekvall (1986) and remains positive across the
method's full documented accuracy band. F12 Piece 2 (single-specimen FE break-load match) is
set up and waiting on the Ansys run.
