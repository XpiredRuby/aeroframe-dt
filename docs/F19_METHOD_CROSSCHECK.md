# F19 — Independent Method Cross-Check — AF-DT-1000

**The governing lug check has only ever been evaluated by one method.** Every margin in this project
traces to Melcon-Hoblit (R2/R3). The Ekvall paper obtained for F18 contains **explicit closed-form
equations**, not merely a correlation band, which makes a second independent evaluation possible for
the first time.

**Claim boundary:** educational / representative / portfolio only. Non-OEM, non-certified.

**Source:** Ekvall, J.C., *J. Aircraft* 23(5), 1986, pp. 438–443 — Fig. 4 relation for straight lugs
loaded at 90° to the lug axis, and Eq. (2) defining the bearing efficiency factor.

---

## 1. Result

    Melcon-Hoblit transverse allowable:  259,875 lb
    Ekvall transverse allowable:         230,010 lb
    ratio Ekvall / Melcon-Hoblit = 0.885

**Two independent published methods disagree by 11.5% on the governing allowable, with Ekvall the
more conservative.**

| | MS |
|---|---|
| Melcon-Hoblit transverse allowable (released) | **+0.156** |
| Ekvall transverse allowable substituted | **+0.053** |

**Both are positive.** The disagreement does not change the pass/fail conclusion, but it is large
relative to the margin and belongs on the record.

## 2. Why the comparison is possible and what exactly is compared

Ekvall defines the bearing efficiency factor as `K_BR = P/(D t F_tu)`, so the predicted failure load
is `P = D · t · K_BR · F_tu`. For **straight lugs loaded at 90° to the lug axis** — the transverse
case — his Fig. 4 gives `K_BR` directly as a printed linear relation in `W/D`:

    K_BR = -0.463 + 0.580 (W/D)

At `W/D = 2.000` this gives `K_BR = 0.6970`, and with `D = 2.000 in`, `t = 2.500 in`,
`F_tu = 66 ksi` (LT, the transverse load direction):

    P = 2.000 * 2.500 * 0.6970 * 66,000 = 230,010 lb

Melcon-Hoblit gives the same quantity as `P'tru = Ktru · Abr · Ftux = 0.7875 × 5.00 × 66,000 =
259,875 lb`.

**This is a like-for-like comparison of the transverse allowable only.** Both use the same geometry,
the same `F_tu`, and the same gross bearing area basis. The 1.15 fitting factor is applied inside the
load ratios in this project, not inside the allowables, so substituting one allowable for the other
is a clean swap.

### 2.1 Effect on the margin

The transverse load ratio scales inversely with the allowable:

    Rtr = 0.72198  ->  0.72198 x (259,875 / 230,010) = 0.81570
    Ra  = 0.36463  (unchanged, axial allowable not affected)

    MS = 1/(Ra^1.6 + Rtr^1.6)^0.625 - 1 = +0.053

## 3. Is this a problem?

**No, and the reason is quantitative.** The ratio 0.885 sits **inside Ekvall's own measured
predicted/test band of 0.85 to 1.19.** Two methods differing by an amount smaller than the
demonstrated scatter of either is exactly what should be expected. It is evidence that both are
working, not that one is wrong.

**But it does put a number on something previously unquantified.** Before this, "method uncertainty"
was represented only by Ekvall's statistical band applied to a Melcon-Hoblit result. Now there is a
direct method-to-method comparison on this specific geometry.

### 3.1 An unforced agreement worth noting

Two entirely different routes land in the same place:

| Route | MS |
|---|---|
| Melcon-Hoblit at the B-basis-consistent scatter limit (90%/95%, F18 §5) | +0.052 |
| Ekvall closed-form transverse allowable substituted (this document) | +0.053 |

These share no arithmetic — one is a statistical tolerance limit applied to a Melcon-Hoblit
allowable, the other is a different method's closed-form equation. **They agree to within 0.001.**

That is a coincidence and is presented as one. It is not independent confirmation of anything, and
no weight is placed on it. It is recorded because a reviewer will notice it and should be told it
was noticed.

## 4. Caveats — and the largest one first

**Fig. 4's relation is fitted to *symmetric* straight lugs, where `2a/W = 1.0`. This fitting is
eccentric at `2a/W = 1.250`.** Ekvall handles eccentricity through a separate correction factor
(his Fig. 6), applied to the stress concentration factor and then carried into `K_BR` through his
Fig. 3. **Neither Fig. 3 nor Fig. 6 is available as an equation** — both are graphs, and digitising
them from the source would introduce error of the same order as the effect being measured.

The correction is therefore **not applied**. Fig. 6 shows the 90° eccentricity curve is comparatively
flat above `2a/W = 1.0`, so the omission is expected to be small — but "expected to be small" is an
assertion, not a measurement, and the 11.5% figure should be read with that attached.

**Other caveats:**

1. **Pure 90° versus 59.04°.** The comparison is of the transverse allowable term in isolation, which
   is the correct like-for-like, but the actual load is oblique and both methods combine terms
   differently. Only the transverse term is compared here; the axial term and the interaction
   equation are Melcon-Hoblit's in both cases.
2. **`F_tu` selection.** LT (66 ksi) is used, matching the transverse load direction. Ekvall
   recommends minimum strength with respect to grain direction; using ST (62 ksi) would give
   216,070 lb and a further reduction. That case is not adopted, because ST carries no primary load
   in this design (see `MARGIN_SUMMARY.md` §3).
3. **Ekvall excluded localized bearing failures** from the data behind these relations, as recorded
   in `F18_EKVALL_SPECIMEN_BASIS.md` §6.
4. **Range check passes.** `W/D = 2.000` sits inside the span of the Fig. 4 data points (roughly
   1.3 to 3.6), so this is interpolation, not extrapolation.

## 5. What this does not do

**It does not change the governing margin.** `MS = +0.156` stands, on Melcon-Hoblit, which remains
the released method for this project.

This is a **cross-check raised as a finding**, not an amendment. A released stress report is not
silently edited because a cross-check produced a different number; the finding is recorded, and it is
incorporated at the next revision if review concludes it should be. The proposed change is a single
additional row in the §6.4 sensitivities table of the stress report and `MARGIN_SUMMARY.md` §5:

    Ekvall closed-form transverse allowable substituted    +0.053

## 6. What would make this decisive

Digitising **Fig. 3** (`K_BR` versus `K_tb`) and **Fig. 6** (eccentricity correction) would allow
Ekvall's full procedure to be executed for the actual `2a/W = 1.250` geometry and the actual 59.04°
load angle, rather than the symmetric 90° special case. That would convert this from an approximate
cross-check into a genuine second independent margin.

It is the same digitisation task already listed as an open item for the AFFDL K-factor curves, and
would close both.

## 7. Limitations

1. **Eccentricity correction omitted** — §4. The single largest source of uncertainty here.
2. **Transverse term only.** Not a full second margin; the interaction equation and axial term remain
   Melcon-Hoblit's.
3. **One geometry.** No sweep was performed, so nothing is established about how the two methods
   compare elsewhere.
4. **The agreement in §3.1 is coincidental** and is given no weight.
