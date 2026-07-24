# Load Basis — AF-DT-1000, Rev B

**Decision ID:** LOAD-AFDT-1000-revB
**Supersedes:** LOAD-AFDT-1000-revA
**Component:** AF-DT-1000, forward pylon-to-wingbox attachment fitting
**Claim boundary:** educational / representative / portfolio only. Non-OEM, non-certified.
All magnitudes `SYNTHETIC_TEST_ONLY`.

---

## 1. Why this revision exists

Rev A distributed the applied inertia resultant to the forward fitting using a 50/50
forward-aft split, and recorded in its Section 5.1 that this omitted the pitching couple
produced by the propulsion centre-of-gravity offset. That omission was identified as the
highest-priority open item in the load path.

This revision closes it by resolving an explicit free body. The result changes the forward
fitting design load by a factor of **2.33** and changes its **direction**, so every downstream
result derived from rev A is superseded.

---

## 2. Declared attachment geometry

These values are **representative and declared**, not derived from any aircraft. They define
the structural context of AF-DT-1000 and are frozen by this record.

| Symbol | Meaning | Value |
|---|---|---|
| L_fa | Forward-to-aft attachment station spacing | 2.000 m |
| x_cg | Propulsion CG forward of the forward attachment | 1.500 m |
| z_cg | Propulsion CG below the attachment plane | 1.200 m |
| m | Propulsion system mass (engine + nacelle + QEC) | 6 000 kg |

Axis convention: X positive forward, Z positive up, attachment plane at Z = 0. Forward
attachment at X = 0; aft attachment at X = -L_fa.

**Note on `L_station`.** The parameter `GEO-010 L_station` in `cad/PARAMETER_SCHEMA.csv` is
described as forward-to-aft support-station spacing but is used in the CAD as the flange plate
length (0.4064 m). It is **not** the attachment spacing and must not be confused with `L_fa`.
That naming inconsistency remains an open item.

---

## 3. Free-body resolution, LC-02

Applied: 9.0 g forward at the propulsion CG.

    W    = m g            = 58.86 kN
    F_x  = 9.0 W          = 529.74 kN, acting at (x_cg, z_cg)

Moment about the forward attachment, taken as M_y = z F_x:

    M_y  = (-1.200)(529.74) = -635.69 kN.m

This moment is reacted as a vertical couple across the attachment spacing:

    R_z(aft) = +317.84 kN
    R_z(fwd) = -317.84 kN

### 3.1 Axial distribution assumption

The forward fitting is assumed to react **100 percent** of the axial (X) component. This
represents a forward mount that carries thrust and axial inertia, with the aft mount reacting
vertical and lateral load only.

This is a declared idealisation. Real pylon mount systems distribute axial load through thrust
links and the split depends on the mount arrangement. An alternative 50/50 axial split would
give a forward resultant of 413.7 kN at 50.2 degrees. The chosen assumption is the more severe
in magnitude and is retained on that basis.

### 3.2 Forward fitting design load

    R_x = 529.74 kN
    R_z = 317.84 kN
    P   = sqrt(R_x^2 + R_z^2) = 617.78 kN
    alpha = atan(R_z / R_x)   = 30.96 degrees off the lug axis

---

## 4. Frozen design load

| Quantity | Rev A | **Rev B** |
|---|---|---|
| Forward fitting ultimate load | 264.9 kN | **617.8 kN** |
| Direction | axial | **30.96 deg oblique** |
| Ratio | — | **2.33x** |

---

## 5. Consequences for the substantiation

### 5.1 Static margin

Against the rev A net-section allowable of 191 700 lb (852.7 kN) and the 1.15 fitting factor:

    required = 617.78 x 1.15 = 710.4 kN
    MS (axial method) = 852.7 / 710.4 - 1 = +0.20

compared with +1.80 in rev A.

### 5.2 The axial method no longer applies

At alpha = 30.96 degrees the load is **oblique**, not axial. The Air Force method requires the
oblique interaction relationship

    (P / P_u.L)^1.6 + (P_tr / P_tru.L)^1.6 = 1

with the transverse allowable obtained separately. The oblique allowable is lower than the
axial allowable, therefore **MS = +0.20 is itself optimistic**. The true margin may approach or
fall below zero. It must be recomputed with the oblique method before any margin is quoted.

### 5.3 Superseded work

The following are void against rev B loading and must be re-run:

- `docs/F5_F6_STATIC_RESULTS_AF-DT-1000_revA.md` in its entirety
- the Ansys model, which applies 264 900 N in +X only
- both hand-calc spreadsheet results

The rev A record remains in the repository as history. It is not deleted.

---

## 6. Remaining limitations

1. The attachment geometry in Section 2 is declared, not derived. Changing L_fa, x_cg or z_cg
   changes the couple proportionally; the design load is directly sensitive to all three.
2. The axial distribution assumption in 3.1 is an idealisation. A thrust-link arrangement would
   redistribute the X component.
3. Only LC-02 has been resolved through the free body. LC-01 and LC-03 still use rev A
   screening distribution and require the same treatment.
4. Engine gyroscopic and torque reactions are not represented.
5. LC-04 engine-failure transient remains deferred to F10.

---

## 7. Open items

| Item | Phase | Priority |
|---|---|---|
| Recompute the margin using the oblique interaction method | F5 | Highest |
| Re-run the FE model with 617.8 kN at 30.96 degrees | F5/F6 | Highest |
| Resolve LC-01 and LC-03 through the same free body | F5 | High |
| Confirm the net-tension curve for 7075-T7351 | F5 | High |
| Establish material allowable basis | F5 | High |
| Reconcile the `L_station` naming inconsistency | F5 | Medium |
| Sensitivity of the design load to L_fa, x_cg, z_cg | F11 | Medium |
