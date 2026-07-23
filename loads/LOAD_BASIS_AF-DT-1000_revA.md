# Load Basis — AF-DT-1000, Rev A

**Decision ID:** LOAD-AFDT-1000-revA
**Component:** AF-DT-1000, forward pylon-to-wingbox attachment fitting
**Status:** Approved for F5/F6 screening and FE model definition
**Claim boundary:** educational / representative / portfolio only. Non-OEM, non-certified.
All magnitudes in this document are `SYNTHETIC_TEST_ONLY`. Nothing here is a compliance
finding, a certification basis, or aircraft design data.

---

## 1. Purpose

`PROJECT_STATE.md` lists source-backed loads as an open non-software gate. This record closes
that gate at **screening level** by freezing a small, explicitly synthetic load envelope so that
F5/F6 can produce margins. It does not claim regulatory compliance.

---

## 2. Regulatory conditions used as rationale

The magnitudes below are synthetic. The *conditions* are modelled on 14 CFR Part 25 so that the
envelope has an engineering rationale rather than an arbitrary one.

| Ref | Condition | Role here |
|---|---|---|
| 25.337 | Positive limit manoeuvring load factor, n_z = 2.5 for transport category | Basis for LC-01 |
| 25.561 | Emergency-landing ultimate inertia forces, including 9.0 g forward | Basis for LC-02 |
| 25.363 | Side load on engine mount and supporting structure | Basis for LC-03 |
| 25.362 | Engine-failure transient loads; factor 1.0 on mounts and pylons, 1.25 on adjacent airframe | Basis for LC-04, deferred |
| 25.303 | Factor of safety 1.5 between limit and ultimate | Applied to LC-01 and LC-03 |

**Applicability caveat.** The applicability of 25.561 to wing-mounted engine pylons is not
settled among practitioners; the competing view is that engine-mount strength requirements are
governed from 25.901 onward. LC-02 is therefore used as a *representative severe forward
inertia case*, not as a compliance condition. This ambiguity is deliberately recorded rather
than resolved.

---

## 3. Representative propulsion system

| Quantity | Value | Note |
|---|---|---|
| Propulsion system mass (engine + nacelle + QEC) | 6 000 kg | SYNTHETIC, representative high-bypass turbofan installation |
| Reference gravity | 9.81 m/s^2 | |
| Installed weight, W | 58.86 kN | m * g |

---

## 4. Frozen load envelope

Loads are the inertia reactions carried by the pylon-to-wingbox attachment set as a whole.

| Case | Direction | Factor | Limit (kN) | Ultimate (kN) | Basis |
|---|---|---|---|---|---|
| LC-01 | Vertical (+Z) | n_z = 2.5 | 147.2 | 220.7 | 25.337, x1.5 |
| LC-02 | Forward (+X) | 9.0 g | n/a | **529.7** | 25.561, ultimate by definition |
| LC-03 | Lateral (+Y) | 3.0 g | 176.6 | 264.9 | 25.363, x1.5 |
| LC-04 | Combined transient | n/a | deferred | deferred | 25.362, requires dynamic analysis |

**Governing case for rev A: LC-02.**

---

## 5. Distribution to the forward fitting

The pylon is idealised with two support stations, forward and aft, consistent with
`docs/LOAD_PATH_AND_FBD.md`.

**Screening assumption (rev A):** the forward station reacts **50 percent** of the applied
resultant.

Forward fitting design ultimate pin load, LC-02:

    P_ult = 0.50 * 529.7 kN = 264.9 kN

### 5.1 Known limitation of this assumption

In a forward inertia event the propulsion system centre of gravity lies forward of and below the
attachment plane. The offset inertia force therefore produces a pitching couple that is reacted
as opposing axial loads at the forward and aft stations. That couple is not represented by a
50/50 direct-load split and can exceed the direct component.

The couple cannot be evaluated until pylon station geometry, attachment plane location and
propulsion CG offset are defined. Until then:

- the loads in Section 4 are **lower bounds** at the forward fitting;
- resulting margins are correspondingly optimistic;
- **no margin from rev A may be quoted as a strength substantiation.**

This is the highest-priority open item in the load path.

---

## 6. Screening stresses at the frozen envelope

Geometry per `DEC-AFDT-1000-revA`: d_pin = 0.050800 m, t_lug = 0.038100 m,
w_lug = 0.101600 m, e_center = 0.063500 m. Load P_ult = 264.9 kN.

| Mode | Expression | Area (m^2) | Stress (MPa) |
|---|---|---|---|
| Projected bearing | P / (d t) | 0.0019355 | 136.9 |
| Net section | P / [(w - d) t] | 0.0019355 | 136.9 |
| Two-plane shear-out | P / [2 (e - d/2) t] | 0.0029032 | 91.2 |

Bearing and net-section areas are numerically equal here because w - d = d at W/D = 2.00.

Indicative margins against representative 7075-T7351 properties (Ftu ~ 490 MPa,
Fsu ~ 290 MPa, no allowable frozen, no basis claimed):

- net section: MS ~ +2.6
- shear-out: MS ~ +2.2

These are large. Section 5.1 explains why. They are screening indications only.

---

## 7. Constraints carried into F5/F6

1. Per `DEC-AFDT-1000-revA` 3.4.2, the simplified two-plane shear-out expression may be
   unconservative at e/D = 1.25 and **must not govern**. The K-coefficient lug method plus solid
   FEA establishes the governing static margin.
2. The FE model must apply LC-02 as a pin-bearing load through the bore, not as a point load.
3. Mesh convergence must be demonstrated at the bore before any margin is quoted.
4. The pitching-couple limitation in 5.1 must be closed before any margin is presented as a
   result rather than a screening indication.
5. No design allowable is frozen by this record. Allowables require a stated product form,
   thickness, grain direction and basis before use.

---

## 8. Open items

| Item | Phase | Priority |
|---|---|---|
| Define pylon station geometry and propulsion CG offset; replace the 50/50 split with a real free-body | F3 / F5 | Highest |
| LC-04 engine-failure transient by dynamic analysis | F10 | Deferred |
| 7075-T7351 allowable basis with product form and grain direction | F5 | High |
| Reconcile `L_station` naming: the parameter schema describes it as forward-to-aft station spacing, the CAD script uses it as flange plate length | F5 | Medium |
