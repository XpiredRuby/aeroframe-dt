# F5/F6 — Static Substantiation Results, AF-DT-1000 Rev A

**Record ID:** F56-AFDT-1000-revA
**Component:** AF-DT-1000, forward pylon-to-wingbox attachment fitting
**Load case:** LC-02 per `loads/LOAD_BASIS_AF-DT-1000_revA.md`
**Claim boundary:** educational / representative / portfolio only. Non-OEM, non-certified.
All magnitudes `SYNTHETIC_TEST_ONLY`. Not a compliance finding.

---

## 1. Headline result

| Quantity | Value |
|---|---|
| Applied ultimate load, P | 264.9 kN (59 552 lb) |
| Fitting factor applied | 1.15 |
| Required ultimate | 68 485 lb |
| Shear-bearing allowable | 250 966 lb |
| **Net-section allowable** | **191 700 lb** |
| **Governing mode** | **Net-section tension** |
| **Margin of safety** | **MS = +1.80** |

The fitting is substantially over-strength for the rev A load case. See Section 6 before
treating this as a strength statement.

---

## 2. Geometry and material

Per `DEC-AFDT-1000-revA`. D = 2.000 in, t = 1.500 in, w = 4.000 in, e = 2.500 in.
Derived: e/D = 1.25, w/D = 2.00, D/t = 1.33, a/D = 0.75.
Material 7075-T7351, Ftu = 71 ksi (representative; no allowable basis established).

---

## 3. Hand analysis — Air Force / Melcon-Hoblit lug method

Tooling: Abbott Aerospace spreadsheets AA-SM-009-001 (shear-bearing) and AA-SM-009-002
(axial/net-section), which digitise the curves of the US Air Force Stress Manual
AFFDL-TR-69-42. Both cite NASA TM X-73305 (1975).

### 3.1 Shear-bearing

Because e/D = 1.25 < 1.5, the sub-1.5 branch applies: `F_bru.L = K (a/D) F_tux`.
Result: allowable 250 966 lb, MS = +2.66.

### 3.2 Net-section tension

Allowable = Ftu * Kt * At, with At = (w - D) t = 3.000 in^2.
Kt = 0.90 read from the net-tension efficiency curve at w/D = 2.00.
Result: allowable 191 700 lb, MS = +1.80. **Governs.**

### 3.3 Documented deviation

AA-SM-009-002 computes lug width internally as `w = 2e`, which models a round-ended
concentric lug. AF-DT-1000 is a rectangular tab where w = 4.000 in and e = 2.500 in, so
w != 2e. Cell G20 was therefore overwritten with the true width of 4.000 in, replacing the
sheet's formula. Verified after override: w/D = 2.00 and At = 3.000 in^2, both consistent with
the actual geometry. This deviation is deliberate and is recorded here rather than left silent.

---

## 4. Finite element model

Ansys Mechanical 2025 R2 (academic licence), linear static.

| Item | Setting |
|---|---|
| Geometry | AF-DT-1000 extracted from AF-DT-2000 assembly; 12 other bodies suppressed |
| Verification | volume 2.1325e-3 m^3 (130.110 in^3), mass 5.9923 kg |
| Material | 7075-T7351, E = 71.7 GPa, nu = 0.33, rho = 2810 kg/m^3 |
| Constraint | Fixed Support on DATUM_A_MOUNT_FACE (area 6.1688e-2 m^2) |
| Load | Bearing Load on PIN_BORE, 264 900 N in +X |
| PIN_BORE scope | 2 faces, area 6.078e-3 m^2 = pi*D*t (full bore) |
| Element type | tetrahedral, program-controlled order |

### 4.1 Mesh independence

| Element size | Peak von Mises (MPa) | Surface average (MPa) |
|---|---|---|
| 4 mm | 690.5 | 284.1 |
| 2 mm | 691.2 | 288.9 |

Peak varies 0.1 percent and average 1.7 percent across a halving of element size. The solution
is mesh-independent at the applied load. No singular behaviour is present.

### 4.2 Interpretation

Peak von Mises of 691 MPa exceeds the representative yield strength of 7075-T7351
(approximately 434 MPa), indicating local yielding at the bore. This is expected for a
pin-loaded lug and is not a failure indication: linear-elastic FE reports elastic stress
without redistribution, and the empirical K coefficients of the lug method already account for
local plasticity. **FE peak stress is not used as the margin basis.** The FE result is used as
corroboration of load path and of the failure location, which is at the bore as predicted.

### 4.3 Superseded runs

Earlier runs in this phase produced peaks between 183 and 762 MPa with apparently divergent
mesh refinement. The cause was traced to `PIN_BORE` being scoped to only one of the two
half-cylinder faces forming the bore (area 3.039e-3 m^2 instead of 6.078e-3 m^2), which
concentrated the full bearing load into a quarter of the hole. Once the scoping was corrected
the solution became mesh-independent immediately. Those runs are void and are recorded only so
the error is not repeated. Geometry revisions B and C, which added a bore-mouth radius to
address a singularity that did not exist, are also withdrawn.

---

## 5. Modelling assumptions

1. Fixed Support applies to the entire mounting face rather than the eight fastener locations.
   This over-stiffens the flange. Lug results are unaffected; **flange-local stresses from this
   model are not valid** and require a fastener-modelled boundary condition.
2. Bearing Load applies a cosine pressure distribution over the loaded half of the bore. It
   does not represent pin contact, clearance, or friction. F7 supersedes it.
3. The pin, bushing, clevis, interface plate and bolts are suppressed. Only AF-DT-1000 is
   modelled.
4. The bore edge is geometrically sharp. Since FE peak stress is not the margin basis, this
   does not affect the reported result.

---

## 6. Limitations on the reported margin

**MS = +1.80 must not be quoted as a strength substantiation.** Four items constrain it:

1. **The applied load is a lower bound.** Per `LOAD_BASIS` 5.1, the 50/50 forward-aft split
   omits the pitching couple produced by the propulsion CG offset. The true forward-fitting load
   is higher, possibly substantially. This is the largest single source of optimism.
2. **Kt = 0.90 was taken from Curve 5**, the spreadsheet default. The correct curve for
   7075-T7351 in the relevant grain direction has not been confirmed. The margin scales
   directly with Kt.
3. **No material allowable basis is established.** Ftu = 71 ksi is representative. A-basis or
   B-basis values with product form, thickness and grain direction are required.
4. Transverse and oblique load cases have not been analysed. Only LC-02 axial is covered.

---

## 7. Open items

| Item | Phase | Priority |
|---|---|---|
| Replace the 50/50 split with a real free-body including the CG-offset couple | F3/F5 | Highest |
| Confirm the correct net-tension curve for 7075-T7351 | F5 | High |
| Establish material allowable basis | F5 | High |
| Apply missing web-to-flange and web-to-lug fillets in a parametric rebuild | before F8/F9 | High |
| Fastener-modelled boundary condition for flange-local stress | F5/F13 | Medium |
| Pin contact analysis | F7 | Scheduled |
| Transverse and oblique cases | F5 | Medium |

### 7.1 Note on the CAD fillet defect

`pylon_fitting.py` applies its blend using `NearestToPointSelector`, which returns a single
edge. Only one fillet of the intended set exists in the geometry; the remaining web transitions
are sharp. The `try/except` around it did not fire, so the partial application was silent.
This does not affect the static result above but **must be corrected before F8/F9**, since
sharp re-entrant corners dominate fatigue initiation. The correction belongs in a parametric
rebuild, not as an operation patched onto an exported STEP.
