# Load Basis — AF-DT-1000, Revision C

**Supersedes Revision B.** Rev B resolved the design load at **30.96°**, measured from the wrong
reference. Rev C corrects it to **59.04°** and reclassifies the case as **transverse-dominant**.

**This is the governing load basis for every margin in the project.**

> **Provenance classification** per `ASSUMPTIONS_AND_PROVENANCE.md`:
> the 9g factor is `PUBLISHED`; the 6000 kg propulsion mass and the CG offsets are
> `REPRESENTATIVE_ESTIMATE`; the resolved components are `DERIVED`.
> **No value here may be represented as aircraft design data.**

---

## 1. Why this revision exists

Rev B computed the resultant correctly in magnitude but reported its direction as **30.96°
measured from the aircraft X axis**.

**The Melcon-Hoblit oblique lug method requires the angle measured from the lug axis**, not from an
aircraft axis. The lug axis is CAD Z (see `DECISIONS_AF-DT-1000_revD.md` — the axis mapping is
frozen as identity, forced by the flange lying on the wingbox).

    angle from aircraft X   = atan(317,840 / 529,740) = 30.96 deg
    angle from lug axis (Z) = atan(529,740 / 317,840) = **59.04 deg**

The two are complementary: `30.96 + 59.04 = 90.00`.

**Consequence of the error.** At 30.96° from the lug axis the case would be **axial-dominant** and
the axial term would govern. At the correct 59.04° it is **transverse-dominant**, and the transverse
term governs. Since `Ktru = 0.7875` is substantially lower than `Kt = 0.950`, the correct
orientation is the more severe one. **Rev B was non-conservative.**

This is the same class of fault recorded in `HANDOFF.md` §17 — *a reference derived from geometry
without declaring what it referenced* — and it is why the axis mapping is now frozen and stated
explicitly before any load is resolved.

## 2. Load level and coordinate frame

| Attribute | Value |
|---|---|
| **Load level** | **LIMIT** |
| **Coordinate frame** | Aircraft axes. X forward, Y starboard, Z up. Identity mapping to CAD. |
| **Revision** | C |
| **Supersedes** | Revision B (30.96°, non-conservative) |
| **Governing case** | LC-02 |

**No safety factor is embedded in this load vector**, per the load-factor policy in
`ASSUMPTIONS_AND_PROVENANCE.md`. The 1.15 fitting factor is applied separately in the margin
calculation and is identified there.

## 3. Inputs

| Input | Value | Provenance |
|---|---|---|
| Propulsion system mass | 6000 kg | `REPRESENTATIVE_ESTIMATE` |
| Forward load factor | 9g | `PUBLISHED` — FAR 25.561 emergency landing |
| CG offset producing the couple | see Rev B §2 | `REPRESENTATIVE_ESTIMATE` |

**The 9g case is an emergency-landing static condition.** It is not a fatigue cycle and must not be
used as one — see `F9b_SPECTRUM_AND_INTERVAL.md` §1.

## 4. Resolved design load

    F_x = 6000 kg * 9 * 9.81 m/s^2 = 529,740 N   forward
    R_z = 317,840 N                              vertical, from the CG-offset couple

    Resultant = sqrt(529,740^2 + 317,840^2) = **617,776 N**
    Direction = **59.04 deg from the lug axis**   -> TRANSVERSE-DOMINANT

In pound units, as used by the Melcon-Hoblit sheets:

| Component | Value |
|---|---|
| `P_axial` (along lug axis, CAD Z) | **71,453 lb** |
| `P_transverse` (perpendicular, CAD X) | **119,090 lb** |

## 5. Verification

**Equilibrium check by FE.** The Rev D linear elastic model applied this load at the bore and
reacted it at the flange. After mesh refinement the reaction resultant was **617,811 N against
617,776 N applied — 0.006%**. See `F5_FE_REVD_LINEAR_ELASTIC.md` §3.

**Trigonometric self-check.** `sqrt(529740^2 + 317840^2) = 617,776` and
`atan(529740/317840) = 59.04 deg`, consistent with the complementary 30.96° from aircraft X.

**Independent reconstruction.** The margin was rebuilt from these components on a stress basis and
reproduced the hand-calculated value to **0.06%**. See `F5_MARGIN_CROSSCHECK.md`.

## 6. Limitations carried forward from Rev B

1. The attachment geometry is **declared, not derived**. The design load is directly sensitive to
   `L_fa`, `x_cg` and `z_cg`.
2. The axial distribution assumption is an idealisation; a thrust-link arrangement would
   redistribute the X component.
3. **Only LC-02 has been resolved through the free body.** LC-01 and LC-03 still use Rev A screening
   distribution.
4. Engine gyroscopic and torque reactions are not represented.
5. LC-04 engine-failure transient remains deferred.
6. **No fatigue spectrum exists.** One load case cannot supply one. See
   `F9b_SPECTRUM_AND_INTERVAL.md`.

## 7. Status of Rev B open items

| Rev B open item | Status |
|---|---|
| Recompute the margin using the oblique interaction method | **CLOSED** — `MARGIN_SUMMARY.md` |
| Re-run FE with 617.8 kN at the corrected angle | **CLOSED** — `F5_FE_REVD_LINEAR_ELASTIC.md` |
| Resolve LC-01 and LC-03 through the same free body | **OPEN** |
| Confirm the net-tension curve for 7075-T7351 | **CLOSED** — MIL-HDBK-5J Table 3.7.6.0(b3) |
| Establish material allowable basis | **CLOSED** — A-basis, 2.001-2.500 in band |
| Reconcile the `L_station` naming inconsistency | **OPEN** |
| Sensitivity of design load to `L_fa`, `x_cg`, `z_cg` | **OPEN** |

Rev A and Rev B remain in the repository as history and are not deleted.
