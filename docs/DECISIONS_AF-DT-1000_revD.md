# Decision Record — AF-DT-1000 Design Envelope, Rev D

**Decision ID:** DEC-AFDT-1000-revD
**Supersedes:** DEC-AFDT-1000-revA (geometry only; the e/D rationale in rev A §3 remains valid)
**Component:** AF-DT-1000, forward pylon-to-wingbox attachment fitting
**Status:** Approved — freezes the rev D geometry and the CAD-to-aircraft installation orientation
**Claim boundary:** educational / representative / portfolio only. Non-OEM, non-certified. All values are `SYNTHETIC_TEST_ONLY` and must never be presented as aircraft design data.

---

## 1. Why this revision exists

`loads/LOAD_BASIS_AF-DT-1000_revB.md` resolved the propulsion-CG pitching couple through an
explicit free body and raised the forward-fitting ultimate load from 264.9 kN to **617.8 kN**,
a factor of 2.33, and changed its direction from axial to oblique.

Re-run against that load, the rev A geometry gives **MS = −0.32**. The fitting fails. Rev A
geometry is therefore not a viable envelope and must be resized.

This record freezes the resized geometry (rev D) and, because the margin proved to be strongly
orientation-dependent, also freezes the previously undeclared mapping between the CAD coordinate
frame and the aircraft frame.

---

## 2. Frozen dimensions

Authored in inches; SI is the internal calculation unit per `PROJECT_STATE.md`.

| ID | Symbol | Meaning | Rev A (in) | **Rev D (in)** | Rev D (m) |
|---|---|---|---|---|---|
| GEO-001 | d_pin | Pin / hole nominal diameter | 2.000 | 2.000 | 0.050800 |
| GEO-002 | t_lug | Lug thickness (projected bearing) | 1.500 | **2.500** | 0.063500 |
| GEO-003 | w_lug | Lug width (net section) | 4.000 | 4.000 | 0.101600 |
| GEO-004 | e_center | Hole centre to free edge | 2.500 | 2.500 | 0.063500 |
| GEO-005 | t_flange | Wingbox-interface flange thickness | 1.000 | 1.000 | 0.025400 |
| GEO-006 | t_web | Transition web thickness | 0.750 | **2.500** | 0.063500 |
| GEO-007 | r_blend | Minimum structural blend radius | 0.500 | 0.500 | 0.012700 |
| GEO-008 | g_y | Fastener gauge (transverse) | 2.000 | **4.000** | 0.101600 |
| GEO-009 | p_x | Fastener pitch (longitudinal) | 1.500 | 1.500 | 0.038100 |
| GEO-010 | L_station | Flange plate length | 16.000 | 16.000 | 0.406400 |

Fastener pattern: 4 x 2 holes, nominal 0.250 in. Material 7075-T7351 (representative; no design
allowable is frozen by this record). Finish: sulfuric anodise per MIL-A-8625 Type II.

Derived ratios: **e/D = 1.25**, **W/D = 2.00**, **t/D = 1.25** (rev A t/D was 0.75).

Section areas at the frozen geometry:

- bearing area, `A_br = d_pin * t_lug` = **5.000 in²**
- net section, `(w_lug - d_pin) * t_lug` = **5.000 in²**
- two-plane shear-out, `2 (e_center - d_pin/2) t_lug` = **7.500 in²**

Mass and volume, from `cad/build_revD.py` at ρ = 2810 kg/m³:

| | Rev A | Rev D | Change |
|---|---|---|---|
| Volume | 130.11 in³ | 166.19 in³ | +27.7 % |
| Mass | 5.99 kg | **7.65 kg** | +1.66 kg |

The 7.65 kg figure is a **verification target** for the Ansys rev D model. A mass property
mismatch against this value indicates the wrong STEP file has been imported.

---

## 3. Decision 1 — lug thickness increased to 2.500 in

### 3.1 Issue

Rev A geometry under rev B loading gives MS = −0.32. The deficit must be recovered by geometry,
by orientation, or by relaxing the load basis. The load basis is not relaxed.

### 3.2 Analysis

Every lug capacity term in the Air Force / Melcon-Hoblit method scales linearly with `t_lug`:
bearing, net section and shear-out areas are all proportional to it. Increasing `t_lug` is
therefore the most direct available lever, and unlike increasing `w_lug` or `e_center` it does not
invalidate the e/D = 1.25 regime argument approved in rev A §3.

`t_lug` = 2.500 in raises t/D from 0.75 to 1.25. This is within the range covered by the method
and does not push the lug into the thick-lug regime where pin bending would need separate
treatment (pin bending is nonetheless carried as an open item, see §7).

### 3.3 Decision

**`t_lug` is increased from 1.500 in to 2.500 in.** `w_lug` and `e_center` are unchanged, so the
rev A edge-distance rationale is preserved intact.

---

## 4. Decision 2 — constant-thickness blade, and fastener gauge opened

### 4.1 Web thickness

Rev A carried `t_web` = 0.750 in against a 1.500 in lug, giving a thickness step at the web/lug
junction. Two problems follow from thickening the lug alone:

1. The step becomes 2.500 → 0.750 in, a stress-concentrating discontinuity directly in the
   primary load path.
2. `cad/build_revD.py` asserts `2 * r_blend < t_web`. At `r_blend` = 0.500 and `t_web` = 0.750 this
   is violated (1.000 > 0.750). This is the geometric reason the rev A fillets could not all be
   built, which the `NearestToPointSelector` defect then masked.

**`t_web` is set equal to `t_lug` = 2.500 in.** Lug and web become a single constant-thickness
blade. The web/lug junction ceases to exist as a discontinuity, and only the blade/flange junction
requires a blend. `build_revD.py` asserts `abs(t_web - t_lug) < 1e-9` to enforce this.

### 4.2 Fastener gauge

The rev A gauge `g_y` = 2.000 in places the fastener rows 1.000 in either side of the flange
centreline. A 2.500 in thick blade occupies ±1.250 in. The rev A pattern would put fastener holes
**inside the blade footprint**.

**`g_y` is increased from 2.000 in to 4.000 in.** `build_revD.py` asserts
`g_y/2 > t_lug/2 + 2*d_fast` and `(w_lug + 2)/2 - g_y/2 > 2*d_fast`, so both the blade clearance
and the flange edge distance are checked at build time.

---

## 5. Decision 3 — CAD-to-aircraft axis mapping declared

### 5.1 Issue

This mapping was never declared. Its absence produced a direct contradiction in the released
evidence:

- `loads/LOAD_BASIS_AF-DT-1000_revB.md` §3.2 states the resultant is **30.96°** off the lug axis,
  computed as `atan(R_z / R_x)`. That expression treats **aircraft X (forward) as the lug axis**.
- The subsequent geometry review of `cad/build_revD.py` established the lug axis as **CAD Z**,
  giving `atan(R_x / R_z)` = **59.04°**.

The two angles are complementary. They are not a numerical error; they are two different,
undeclared installations of the same fitting. Per the F5 orientation sensitivity study the choice
is worth approximately **1.1 in margin** — more than the thickness change itself. It cannot be
left implicit.

### 5.2 CAD frame, established from `cad/build_revD.py`

| Feature | Construction | CAD direction |
|---|---|---|
| Flange plate | `Workplane("XY").box(L_station, w_lug+2, t_flange)` | plane = XY, normal = Z |
| Web / blade | rises from the flange | height along **+Z** |
| Lug tab | `box(w_lug, t_lug, 2*e_center)` | w_lug along X, t_lug along Y |
| Pin bore | `Workplane("XZ")` extruded `t_lug + 2.0` | bore axis along **Y** |

Therefore, in the CAD frame: **lug axis = Z**, **pin/bore axis = Y**, **net-section width = X**.
For the lug method this gives **Z = axial** and **X = transverse**.

### 5.3 The mapping is constrained, not free

The installation is fixed by the flange, not chosen for convenience:

1. Datum A is the wingbox mounting plane (flange underside). The flange must lie flat on the
   wingbox, whose surface normal is substantially vertical. This forces **CAD Z → aircraft Z (up)**.
2. The flange is 16.000 in in X and 6.000 in in Y. Its long axis runs fore-and-aft along the
   wingbox. This forces **CAD X → aircraft X (forward)**.
3. The remaining axis follows: **CAD Y → aircraft Y (spanwise)**, so the pin axis is lateral. This
   is the correct arrangement for a pylon mount that articulates in pitch relative to the wing.

The more favourable 30.96° orientation would require the lug axis to point forward, which would
stand the flange on edge and destroy the wingbox interface. It is not available.

### 5.4 Decision

**The mapping CAD X → aircraft X, CAD Y → aircraft Y, CAD Z → aircraft Z (identity) is frozen.**

Consequently, for LC-02:

| Component | Magnitude | Aircraft direction | Lug sense |
|---|---|---|---|
| R_x | 529 740 N | forward | **transverse** |
| R_z | 317 840 N | vertical | **axial** |
| Resultant | 617 776 N | — | **59.04° off the lug axis** |

`loads/LOAD_BASIS_AF-DT-1000_revB.md` §3.2 and §5.1 are superseded on this point by
`loads/LOAD_BASIS_AF-DT-1000_revC.md`.

---

## 6. Margin status — PROVISIONAL

Rev D closes the margin at every orientation examined:

| Orientation off lug axis | M.S. |
|---|---|
| 0° (pure axial) | +1.11 |
| 30° | +0.44 |
| 45° | +0.23 |
| **59° (LC-02, frozen orientation)** | **+0.11** |
| 90° (pure transverse, bounding) | +0.03 |

**These values are PROVISIONAL and must not be quoted as substantiated.** They depend on three
inputs that are not yet verified:

1. `A₁` and `A₄` in the transverse allowable are currently taken as **1.5 in² by assumption**.
   They have not been read off USAF Fig. 9-7 for this section. This input can change the sign of
   the margin.
2. The axial and transverse curve numbers for 7075-T7351 (curve 5 and curve 8) are **defaults**,
   not confirmed for this alloy and temper.
3. Spreadsheets AA-SM-009-002 and AA-SM-009-005 disagree on the axial allowable for identical
   inputs — 191 700 lb (Kt = 0.90) against 202 350 lb (Kt = 0.95). The discrepancy is unresolved.

The geometry freeze does **not** depend on resolving these. Rev D is strictly stronger than rev A
in every mode at equal orientation, and rev A is known to fail at −0.32. The freeze is justified
on that basis alone. Only the numerical margin is held provisional.

---

## 7. Open items carried forward

| Item | Phase | Priority | Note |
|---|---|---|---|
| Verify A₁–A₄ against USAF Fig. 9-7 for this section | F5 | **Highest** | Can flip the margin sign |
| Confirm axial/transverse curve numbers for 7075-T7351 | F5 | High | Currently defaults |
| Reconcile the AA-SM-009-002 vs -005 Kt disagreement | F5 | High | 191 700 vs 202 350 lb |
| Re-run Ansys on the rev D STEP: 317 840 N in Z **and** 529 740 N in X | F5/F6 | High | Verify mass = 7.65 kg first |
| Establish A/B-basis material allowable | F5 | High | Ftu = 71 ksi is representative only |
| Pin bending check at t/D = 1.25 | F5 | Medium | Not covered by the thin-lug method |
| Re-issue Onshape drawing (g_y and t_lug both changed) | F13 | Medium | "Drawing 2" is now out of date |
| Delete the broken Onshape "Drawing 1" | F13 | Low | Housekeeping |
| Rename GEO-010 from `station_spacing` to `flange_length` | F13 | Low | Description corrected at rev D; field name retained for compatibility |
| Correct the stale `t_web -> 1.250` comment in `build_revD.py` | F13 | Low | Actual value is 2.500 |

**Note on the mounting-face fasteners.** Opening `g_y` to 4.000 in moves the fastener rows outboard.
The rev A flange bending check and the fastener load distribution both assumed the 2.000 in gauge
and are void. Both must be redone in F5 against the frozen pattern.
