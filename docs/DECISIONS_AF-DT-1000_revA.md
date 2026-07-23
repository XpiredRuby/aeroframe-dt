# Decision Record — AF-DT-1000 Design Envelope, Rev A

**Decision ID:** DEC-AFDT-1000-revA
**Component:** AF-DT-1000, forward pylon-to-wingbox attachment fitting
**Status:** Approved — closes the CAD gate defined in `cad/GEOMETRY_CONCEPT.md`
**Claim boundary:** educational / representative / portfolio only. Non-OEM, non-certified. All values are `SYNTHETIC_TEST_ONLY` and must never be presented as aircraft design data.

---

## 1. Purpose

`cad/GEOMETRY_CONCEPT.md` lists hole diameter, lug width/thickness, edge distance, flange
thickness, fastener pattern and blend radii as "not frozen", and states that these remain
blank until a representative design envelope is formally approved in a decision record.
This record provides that approval and moves `cad/PARAMETER_SCHEMA.csv` from `TBD` to `SET`.

---

## 2. Frozen dimensions

Authored in inches; SI is the internal calculation unit per `PROJECT_STATE.md`.

| ID | Symbol | Meaning | Value (in) | Value (m) |
|---|---|---|---|---|
| GEO-001 | d_pin | Pin / hole nominal diameter | 2.000 | 0.050800 |
| GEO-002 | t_lug | Lug thickness (projected bearing) | 1.500 | 0.038100 |
| GEO-003 | w_lug | Lug width (net section) | 4.000 | 0.101600 |
| GEO-004 | e_center | Hole centre to free edge | 2.500 | 0.063500 |
| GEO-005 | t_flange | Wingbox-interface flange thickness | 1.000 | 0.025400 |
| GEO-006 | t_web | Transition web thickness | 0.750 | 0.019050 |
| GEO-007 | r_blend | Minimum structural blend radius | 0.500 | 0.012700 |
| GEO-008 | g_y | Fastener gauge (transverse) | 2.000 | 0.050800 |
| GEO-009 | p_x | Fastener pitch (longitudinal) | 1.500 | 0.038100 |
| GEO-010 | L_station | Flange / station length | 16.000 | 0.406400 |

Fastener pattern: 4 x 2 holes, nominal 0.250 in.
Material: 7075-T7351 aluminium (representative; no design allowable is frozen by this record).
Finish: sulfuric anodise per MIL-A-8625 Type II.

Derived ratios: **e/D = 1.25**, **W/D = 2.00**, **t/D = 0.75**.

---

## 3. Principal decision — edge distance retained at e/D = 1.25

### 3.1 Issue

`src/aeroframe_dt/cad_automation.py::validate_functional_constraints` rejects any geometry
where `edge_distance_m < 1.5 * hole_diameter_m`, reporting it as below "the provisional 1.5D
screening floor". The frozen envelope gives e/D = 1.25 and would be flagged by that rule.

### 3.2 Analysis

In the Melcon & Hoblit / U.S. Air Force Stress Analysis Manual lug method, e/D = 1.5 is **not a
minimum permissible value**. It is the approximate boundary between failure regimes: below
e/D = 1.5 lug failure tends to involve shear-out and hoop tension, and above it bearing tends to
govern. The method explicitly covers both regimes through the allowable load coefficient K, which
also absorbs the interaction between modes. A lug at e/D = 1.25 is therefore an ordinary,
analysable configuration, not an out-of-bounds one.

A load-path area comparison supports retaining the current geometry:

- net-section area = (w_lug - d_pin) * t_lug = (4.000 - 2.000) * 1.500 = **3.000 in^2**
- two-plane shear-out area = 2 * (e_center - d_pin/2) * t_lug = 2 * 1.500 * 1.500 = **4.500 in^2**

The shear-out path already carries 50 percent more area than the net section. Increasing
e_center enlarges the non-governing path only; it adds mass to an engine-attachment fitting
without improving the limiting margin. Capacity in this configuration is more sensitive to w_lug
than to e_center.

Secondary consideration: the CAD package, the fully toleranced drawing and the PMI set are
complete and mutually consistent. A geometry change would invalidate the released drawing, and
a previous geometry update has already broken a drawing in this project. That rework risk is not
justified to correct a condition that is not a defect.

### 3.3 Decision

**e_center is retained at 2.500 in (0.063500 m), e/D = 1.25. No CAD change is made.**

### 3.4 Binding consequences

1. `validate_functional_constraints` must be revised so that the 1.5D test is reported as a
   **regime flag**, not a failure. A physical-validity floor (positive ligament, e_center > d_pin/2)
   remains a genuine error condition.
2. Because the lug sits below e/D = 1.5, the simplified two-plane shear-out expression
   `P/[2(e - d/2)t]` implemented in `hand_calcs.two_plane_shear_out` **may be unconservative**:
   as e/D falls, the ligament transitions from shear-critical toward bending-critical behaviour.
   That expression is retained for screening only and **must not govern** the substantiation.
3. F5/F6 must establish the governing static margin using the K-coefficient lug method together
   with solid FEA, and must report shear-out, hoop tension, bearing and net section explicitly.
4. F8/F9 must treat the pin bore as the fatigue-critical location; the reduced edge distance
   raises local stress at the bore relative to a wider-edge lug.

---

## 4. PMI / GD&T frozen by this record

Matches drawing **AF-DT-1000_fitting Drawing 2** (ANSI B, inch, 1:5) and satisfies the categories
required by `cad/PMI_REQUIREMENTS.md`.

- Datum A: wingbox mounting plane (flange underside).
- Datum B: pin-hole axis.
- Datum C: lug side face (clocking).
- Pin hole: size 2.000; position ⊕ Ø0.010 A B C; perpendicularity ⊥ Ø0.005 A; texture 63 microinch.
- Mounting face A: flatness 0.005; texture 63 microinch.
- Fastener pattern: 8X Ø0.250; position ⊕ Ø0.015 A B C.
- Notes: interpret per ASME Y14.5-2018; inch units; material and anodise callouts; break sharp
  edges; **REPRESENTATIVE / EDUCATIONAL — NOT CERTIFIED DESIGN DATA**.

Numerical tolerance values are representative and remain subject to the tolerance stack and
process-capability work in F13.

---

## 5. Open items carried forward

| Item | Phase | Note |
|---|---|---|
| Revise the 1.5D constraint to a regime flag | F5 | See 3.4.1 |
| Governing static margin by K-method + FEA | F5/F6 | See 3.4.2, 3.4.3 |
| Correct unsupported source citation in legacy `pylon_fitting.py` header and its `0.15*d_pin` assertion, which is not a Melcon-Hoblit criterion | F5 | Legacy script also retains a superseded axial pin bore and must not be treated as current geometry |
| Material allowable basis for 7075-T7351 | F5 | No allowable is frozen here |
| Fatigue assessment at the pin bore | F8/F9 | See 3.4.4 |
