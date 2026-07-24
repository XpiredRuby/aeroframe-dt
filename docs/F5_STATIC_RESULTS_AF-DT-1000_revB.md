# F5 — Static Substantiation Results, AF-DT-1000 Rev B

**Record ID:** F5-AFDT-1000-revB
**Supersedes:** F56-AFDT-1000-revA
**Load basis:** LOAD-AFDT-1000-revB (617.8 kN at 30.96 deg)
**Claim boundary:** educational / representative / portfolio only. Non-OEM, non-certified.
All magnitudes `SYNTHETIC_TEST_ONLY`.

---

## 1. Result

**M.S. = -0.32. The fitting does not meet the rev B load case.**

| Quantity | Value |
|---|---|
| Axial component on lug (Z) | 317.8 kN / 71 453 lb |
| Transverse component on lug (X) | 529.7 kN / 119 090 lb |
| Fitting factor | 1.15 |
| Shear-bearing allowable, P'bru | 250 966 lb |
| Axial-tension allowable, P'tu | 202 350 lb |
| **Transverse allowable, P'tru** | **101 042 lb** |
| Ra = axial factored / min(P'bru, P'tu) | 0.406 |
| Rtr = transverse factored / P'tru | 1.355 |
| **M.S.** | **-0.32** |

Method: Air Force Stress Manual oblique interaction, `(P/Pu.L)^1.6 + (Ptr/Ptru.L)^1.6 = 1`,
via Abbott Aerospace AA-SM-009-005.

**Rtr exceeds 1.0 on its own.** The transverse demand exceeds the transverse allowable before
any interaction is considered. The lug is loaded predominantly across its weak axis.

---

## 2. Progression of the result

| Stage | M.S. | What changed |
|---|---|---|
| Rev A | +1.80 | 50/50 load split, axial method |
| Rev B, first pass | -0.13 | CG-offset couple added; axial/transverse mis-assigned |
| **Rev B, corrected** | **-0.32** | Axial/transverse assigned to the correct lug axes |

The rev A result was optimistic by a factor of roughly six on load-carrying adequacy. The
dominant cause was the screening load split, not the analysis method.

---

## 3. Lug axis orientation

Established from the delivered geometry, not from documentation:

- the lug tab rises in **+Z**; lug axis is Z
- the pin bore runs through **Y** (bore circles at Y = +/-19.05 mm, half of t_lug = 1.500 in)
- `e_center` is measured in **Z**
- `w_lug` = 4.000 in lies in **X**

Therefore for lug analysis the **Z** component is axial and the **X** component is transverse.

### 3.1 Open gap: CAD-to-aircraft axis mapping is undeclared

**No document in this repository states how CAD axes map to aircraft axes.** The rev B load
resolution assumes CAD X = aircraft forward and CAD Z = aircraft vertical. That assumption is
reasonable but was never declared, and the result is sensitive to it.

The first-pass rev B calculation applied the components to the opposite axes and produced
-0.13. Both orientations give a negative margin, so the conclusion that the fitting fails LC-02
is robust to this gap. The **magnitude** is not. A declared orientation is required before any
margin is quoted.

---

## 4. Provisional inputs

These affect the number and are not yet verified:

1. **A1 = A4 = 1.5 in^2**, taken as the side-ligament area (w - D)/2 * t. The manual defines
   A1..A4 as the areas of sections at h1..h4 per Figure 9-7, with h1 most critical and h3 the
   smallest hole-to-edge distance. The mapping for a rectangular lug has not been confirmed
   against that figure.
2. **Transverse curve 8** and **axial curve 5** are spreadsheet defaults. The correct curves for
   7075-T7351 have not been confirmed.
3. **Kt disagreement between sheets.** AA-SM-009-002 gives an axial allowable of 191 700 lb
   (Kt = 0.90); AA-SM-009-005 gives 202 350 lb (Kt = 0.95) for identical geometry and the same
   curve. A 5 percent inconsistency between two sheets from the same source, unresolved.
4. **Ftu = 71 000 psi both directions.** Representative. No allowable basis established, and
   cross-grain strength is not distinguished from longitudinal.
5. Both spreadsheets compute `w = 2e` internally, appropriate to a concentric round-ended lug.
   AF-DT-1000 is rectangular, so the width cell was overwritten with the true 4.000 in in each
   case. Verified after override: w/D = 2.00, At = 3.000 in^2.

---

## 5. Status of the FE model

The Ansys model applies 264 900 N in +X, which is the rev A load. It is **superseded** and its
results are void. It must be re-run with 317.8 kN in Z and 529.7 kN in X, or with the 617.8 kN
resultant applied at the correct orientation.

Note that the rev A FE also applied the load along CAD X, which is transverse to the lug axis.
The rev A FE and the rev A hand calc were therefore not analysing the same load direction. This
was not detected at the time.

---

## 6. Consequence

The design does not close. The available responses, in order of preference:

1. **Re-examine the load path.** The transverse component arises from the CG-offset couple. If
   the fitting is oriented so that the forward inertia is axial to the lug rather than
   transverse, the demand falls substantially. This is a pylon-architecture question, not a
   fitting question, and is the cheapest fix if available.
2. **Increase w_lug.** Net section and transverse capacity both scale with width.
3. **Increase t_lug.** Bearing and transverse capacity scale with thickness.
4. **Reduce the couple** by shortening the CG offset or lengthening the attachment spacing.

Option 1 must be resolved before options 2-4 are sized, since it changes the target.

---

## 7. Open items

| Item | Phase | Priority |
|---|---|---|
| Declare CAD-to-aircraft axis mapping | F5 | Highest |
| Confirm A1..A4 against Figure 9-7 for a rectangular lug | F5 | Highest |
| Resolve the Kt disagreement between AA-SM-009-002 and -005 | F5 | High |
| Confirm axial and transverse curve numbers for 7075-T7351 | F5 | High |
| Establish material allowable basis, including cross-grain | F5 | High |
| Re-run FE at the corrected load and orientation | F5/F6 | High |
| Resize the fitting once the load path is settled | F11 | Scheduled |
