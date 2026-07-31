# F11 — Geometric Optimization

**Headline: the Rev D decision to thicken the lug was counterproductive.**
Once the thick-lug bearing penalty is accounted for, a **thinner, larger-diameter** lug delivers the
same margin for **19% less material**, or three times the margin for the same material.

**Claim boundary:** educational / representative / portfolio only. Non-OEM, non-certified.

---

## 1. Parametrisation, and why it is valid

The Melcon-Hoblit factors `Kt`, `Ktru` and `Kbr` are read from curves against `e/D` and `W/D`.
Those curves are not digitised in this project, so **any design change that alters `e/D` or `W/D`
cannot be evaluated** without re-reading them.

**The study therefore holds both ratios fixed** at the Rev D values:

    e/D = 1.25        W/D = 2.00

Under those ratios the K factors are unchanged and the areas simplify exactly:

    Abr = D * t
    Atn = (w - D) * t = (2D - D) * t = D * t

**So `Abr = Atn = D*t`, and the entire margin depends on the single product `D*t` and on the
thick-lug factor `k = t_eff/t`.** That makes the trade clean and the result exact rather than
interpolated.

**Free variables:** `D` (pin diameter) and `t` (lug thickness), with `e` and `w` following.

## 2. The competing effects

**Bearing capacity** scales with `A = D*t`. Increasing either helps.

**The thick-lug penalty** depends on `t/D`. From `F7_CONTACT_THICK_LUG.md`:

| t/D | k = t_eff/t | Basis |
|---|---|---|
| 1.25 | **0.681** | measured, three-mesh converged contact FE |
| <= 0.60 | **1.000** | thin-lug method valid, no correction required |
| between | **unknown** | not measured — only two anchor points exist |

**Lug volume**, taking a half-disc head of radius `w/2 = D` plus a body `w x e`, less the bore:

    V = (pi*D^2/2 + 2.5*D^2 - pi*D^2/4) * t = 3.285 * D^2 * t

**This is the crux.** For fixed bearing area `A = D*t`, volume is `3.285 * D * A` — so volume grows
with `D`. A **thick, small-diameter** lug is lighter for a given bearing area. **That is presumably
why Rev D thickened the lug rather than enlarging it.**

But that reasoning ignores `k`. The thick lug does not get the full `A` it appears to have.

## 3. Results

Current design and three alternatives at `t/D = 0.60`, the thickest geometry for which the thin-lug
method needs no correction:

| Configuration | D | t | t/D | k | A = D*t | MS | Lug volume |
|---|---|---|---|---|---|---|---|
| **Current (Rev D)** | 2.000 | 2.500 | 1.25 | 0.681 | 5.00 | **+0.078** | **32.9 in³** |
| Same bearing area | 2.887 | 1.732 | 0.60 | 1.000 | 5.00 | +0.584 | 47.4 in³ |
| **Same volume** | 2.554 | 1.533 | 0.60 | 1.000 | 3.91 | **+0.240** | 32.9 in³ |
| **Same margin** | 2.382 | 1.429 | 0.60 | 1.000 | 3.40 | +0.078 | **26.6 in³** |

### Two ways to read it

**At equal margin:** `D = 2.382 in`, `t = 1.429 in` gives the same `MS = +0.078` using
**26.6 in³ instead of 32.9 in³ — 19% less lug material.**

**At equal volume:** `D = 2.554 in`, `t = 1.533 in` gives **`MS = +0.240` instead of +0.078 —
3.1 times the margin for no mass penalty at all.**

## 4. Why the Rev D thickening backfired

`HANDOFF.md` §4 records the Rev D change as `t_lug 1.500 -> 2.500 in`, justified as *"F5 rev B
sizing: closes MS at all orientations."*

Thickening does raise `A = D*t` and the margin did improve. **But it simultaneously raised `t/D`
from 0.75 to 1.25**, deepening a penalty that had not yet been identified. The gain was real but
substantially smaller than believed at the time — and the same margin was available at lower mass by
increasing diameter instead.

**This is not hindsight criticism of the Rev D decision.** The thick-lug penalty was unknown until
F7 measured it, and the decision was correct given what was known. It is an illustration of the
point the whole project turns on: **a design decision is only as good as the validity of the method
used to justify it.**

## 5. Constraints and limitations

**`t/D = 0.60` is a cliff edge, not a smooth optimum.** `k` is known at only two points — 0.681
measured at `t/D = 1.25`, and 1.000 assumed valid at `t/D <= 0.60`. **The behaviour between is not
measured.** The alternatives above sit exactly at 0.60 to stay in the region where no correction is
needed. A genuine continuous optimum requires `k(t/D)`, which would take three or four more contact
runs at intermediate `t/D`.

**Lug volume is not fitting mass.** Only the lug head is parametrised here. The flange
(4.42 kg of the 7.65 kg total) and blade are unchanged, so the whole-fitting mass saving is smaller
than 19% in absolute terms.

**Envelope is unchecked.** A larger `D` means a larger head, and the installation envelope at the
wingbox is not defined in this project. **A 27% diameter increase may not fit.**

**Pin size follows diameter.** A larger bore needs a larger pin. That is favourable — pin bending
stress falls as `1/D^3` for a given load — but the clevis and mating fitting would need rework.

**Manufacturability is not assessed.** REQ-015 calls for manufacturability constraints; none are
applied here beyond noting that all candidates remain machinable from plate in the same thickness
bands.

## 6. Recommendation

**Do not re-cut Rev D on this basis.** The current design passes at `MS = +0.078` and the geometry
is frozen with FE and correlation evidence behind it.

**Do carry this into any Rev E.** The finding is that **diameter buys margin more efficiently than
thickness once `t/D` exceeds about 0.6**, and the Rev D geometry sits well past that point.

**Ranked next steps if a Rev E is opened:**

1. Measure `k(t/D)` at three or four intermediate points. Turns the cliff edge into a real optimum.
2. Confirm the installation envelope permits a larger head.
3. Re-read `Kt`, `Ktru`, `Kbr` at any new `e/D` and `W/D` if the ratios are allowed to vary — this
   study deliberately did not.

## 7. Verification

Areas and margins recomputed from the closed-form expressions in `MARGIN_SUMMARY.md`. The current
configuration reproduces `A = 5.00 in²`, `Ra = 0.3909`, `Rtr = 0.7740`, `MS = +0.078` exactly,
confirming the parametrisation is consistent with the released margin.
