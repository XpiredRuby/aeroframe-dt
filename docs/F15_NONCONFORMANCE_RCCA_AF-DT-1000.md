# F15 Nonconformance & RCCA — AF-DT-1000

**Record ID:** NCR-AFDT-1000-0001 / RCCA-AFDT-1000-0001
**Component:** AF-DT-1000, forward pylon-to-wingbox attachment fitting
**Method basis:** lug oblique-load analysis, NASA TM X-73305 §B2, via AA-SM-009-005 (validated
in F5). Failure-load correlation per Ekvall 1986 (F12).
**Claim boundary:** educational / representative / portfolio only. Non-OEM, non-certified. All
values `SYNTHETIC_TEST_ONLY`. This is a *representative* nonconformance exercise; no real part,
supplier, or program is involved.

---

## 1. Purpose

This record works one realistic manufacturing nonconformance end-to-end the way a Material Review
Board (MRB) and a Root Cause Corrective Action (RCCA) process would: raise it, disposition it with
analysis, find the true root cause, and put in corrective and preventive action. It demonstrates
the liaison / MRB / RCCA workflow that entry-level structural roles name explicitly, on top of the
clean-design substantiation in F5-F12.

---

## 2. Nonconformance description (the NCR)

| Field | Entry |
|---|---|
| NCR number | NCR-AFDT-1000-0001 |
| Part | AF-DT-1000, rev D |
| Discovered at | First-article dimensional inspection (CMM), post-machining |
| Nonconforming feature | Primary pin bore location |
| Drawing requirement | Hole-centre to top free edge, e = 2.500 in (edge distance basic) |
| As-measured | e = 1.900 in |
| Deviation | Bore mis-located 0.600 in toward the loaded edge |
| Drawing tolerance on hole position | ±0.010 in (typical) |
| Magnitude | ~60× the position tolerance — unambiguously a rejectable nonconformance |
| Immediate action | Part quarantined, tagged, routed to MRB. Lot held pending disposition. |

The defect is not marginal against tolerance — it is a gross mis-drill. The engineering question
is therefore not "is it in tolerance" (clearly no) but "is the as-built part still structurally
adequate, or must it be scrapped or reworked."

---

## 3. Engineering disposition (the analysis)

The mis-drill shortens the edge distance, which directly attacks the shear-out / transverse path —
the governing mode for this fitting. The F5 lug method is re-run with e = 1.900 in, all else at
rev D nominal and the LC-02 oblique load unchanged.

### 3.1 Effect on the driving parameters

| Parameter | Nominal (e=2.500) | As-built (e=1.900) | Effect |
|---|---|---|---|
| e/D | 1.250 | 0.950 | drops below the 1.0 shear-out threshold |
| Aav/Abr | 0.750 | 0.450 | transverse area idealisation shrinks |
| Kbr (shear-bearing) | 1.240 | 1.160 | lower |
| Ktru (transverse eff.) | 0.7875 | 0.517 | **sharply lower — the dominant effect** |
| P'tru (transverse allow.) | 279 562 lb | 183 713 lb | −34 % |
| Ra (axial/bearing ratio) | 0.244 | 0.244 | unchanged (net section not moved) |
| Rtr (transverse ratio) | 0.490 | 0.745 | **rises sharply** |
| **M.S.** | **+0.71** | **+0.22** | **−0.49** |

### 3.2 Result

The as-built part retains **M.S. = +0.22** at ultimate under the full LC-02 oblique load. It does
**not** fail. But the margin has lost roughly 70 % of its reserve, and the loss is concentrated
entirely in the transverse/shear-out path that the edge distance protects.

### 3.3 Confidence check against real scatter (F12 link)

The +0.22 as-built margin must be judged against the method's known accuracy, not in isolation.
Per Ekvall (1986), the method's predicted/test ratio reaches 1.19 at its worst over-prediction in
243 tests. Propagating that worst case:

    true M.S._worst = 1.22 / 1.19 − 1 = +0.025

At the method's single most optimistic historical case, the as-built part is **barely positive
(+0.025)** — it has effectively consumed its entire statistical confidence band. The nominal part,
by contrast, held +0.44 even at that worst case. This is the crux of the disposition: the defect
does not cause predicted failure, but it erases the safety the edge distance existed to provide.

---

## 4. Disposition decision (the MRB call)

**Disposition: REWORK — do not use-as-is, do not scrap outright.**

Reasoning:

- **Not use-as-is.** Although the deterministic margin is +0.22, §3.3 shows the as-built part
  sits at the very edge of the method's confidence band (+0.025 worst case). Dispositioning a
  primary flight-critical propulsion attachment "use-as-is" with essentially no statistical
  reserve is not defensible. Edge distance is a protection against exactly the scatter that
  hand methods cannot fully capture (fastener hole quality, local yielding, load redistribution);
  spending all of it on a shop error is the wrong call.
- **Not scrap.** The part is expensive (7075-T7351 forging, 166 in³) and the defect is
  recoverable. Scrapping without exploring rework is wasteful.
- **Rework path:** the shortfall is edge distance. It can be restored by rework only if the part
  has stock to give. Two options are evaluated:
  1. **Trim-and-re-datum:** if the head has machining stock above the hole, the outer profile can
     be re-cut to restore e ≥ 2.500 in relative to the mis-located hole. Requires the as-forged
     head to have ≥ 0.600 in excess stock over the finished profile. **This is the preferred
     rework if stock exists.**
  2. **Weld-repair + re-drill:** not permitted. 7075 is not weldable to structural allowables;
     this path is explicitly excluded.
- If neither rework restores full edge distance, the part is scrapped. Rework is contingent on the
  stock check, which is a producibility question routed back to manufacturing.

**Conditions on the disposition:** reworked part must re-pass full CMM dimensional inspection and
show restored e ≥ 2.500 in before release. The reworked margin returns to the nominal +0.71 only
if full edge distance is recovered; any residual shortfall requires re-analysis.

---

## 5. Root cause (the RCCA)

The disposition handles *this* part. RCCA prevents the *next* one. Structured as a condensed 8D.

**D1 Problem statement:** primary bore on AF-DT-1000 mis-located 0.600 in toward the loaded edge,
60× position tolerance, reducing ultimate margin from +0.71 to +0.22.

**D2 Containment:** lot quarantined; all AF-DT-1000 parts from the same setup held for CMM before
release.

**D3 Root cause investigation (5-Why):**
1. Why did the bore fail position? — It was drilled 0.600 in off the datum.
2. Why 0.600 in off? — The drilling fixture located off the wrong reference edge.
3. Why the wrong edge? — The setup sheet did not call out which edge is the position datum, and
   the two candidate edges are only 0.600 in apart on this profile.
4. Why no datum call-out? — The drawing declares Datum A (mount face) but the machining planning
   never propagated a *hole-position* datum to the shop traveller.
5. Why not propagated? — There is no check in the planning release that verifies every
   tolerance-critical feature has an unambiguous datum on the shop-floor document.

**Root cause:** a datum-reference gap between the engineering drawing and the manufacturing
traveller — the same class of "undeclared reference" error that caused the CAD-to-aircraft axis
ambiguity resolved in DEC-AFDT-1000-revD §5. The failure mode is organisational (reference not
propagated), not a machinist error.

**D4/D5 Corrective action (this part / this process):**
- Add the hole-position datum explicitly to the AF-DT-1000 traveller.
- Re-issue the drawing with a GD&T position callout (true position relative to Datum A) on the
  primary bore, removing edge ambiguity.

**D6 Preventive action (systemic):**
- Add a planning-release gate: every tolerance-critical feature must have an unambiguous datum on
  the shop document before the traveller is released. This closes the whole class of defect, not
  just the bore.
- Add a first-article CMM hold point on hole position for all lug-type parts.

**D7 Verification:** first reworked/re-made part must pass CMM on bore position and be re-analysed
to confirm margin restoration to +0.71.

**D8 Lessons:** this is the second "undeclared reference" defect in the project (axis mapping was
the first). The systemic preventive action is therefore raised to a project-level principle:
**no reference — geometric, coordinate, or datum — is left implicit between one artefact and the
next.**

---

## 6. Traceability

| Links to | ID |
|---|---|
| Governing margin method | F5-AFDT-1000-revD (+0.71 nominal) |
| Load basis | LOAD-AFDT-1000-revC (LC-02, 59.04°) |
| Geometry / datum baseline | DEC-AFDT-1000-revD |
| Failure-load confidence | F12-AFDT-1000-revA (Ekvall 1986) |
| Recurring root-cause class | DEC-AFDT-1000-revD §5 (undeclared reference) |

---

## 7. Status

F15 nonconformance and RCCA **complete** as a representative exercise. It exercises the full MRB /
liaison / RCCA loop — NCR, analytical disposition, structured root cause, corrective and
preventive action, verification, and traceability back to the substantiation. The margin
arithmetic in §3 reuses the F5-validated method chain; no new allowable is introduced.
