# F16 — Elastic-Plastic Contact — AF-DT-1000 Rev D

**Replaces the elastic lower bound on `t_eff/t` with a measurement that includes yielding.**
Executed 2026-08-02/03 on the converged F7 model.

**Claim boundary:** educational / representative / portfolio only. Non-OEM, non-certified.

---

## 1. Result

    t_eff / t = 0.7300      (elastic value was 0.6809, +7.2%)

| | MS |
|---|---|
| Released, elastic `t_eff/t = 0.6809` | +0.078 |
| **Elastic-plastic, `t_eff/t = 0.7300`** | **+0.156** |

**The margin roughly doubles.** This is the first correction in the project that moved the margin
in the favourable direction — the thick-lug correction cost a factor of 4.3, the A-basis allowables
another 2.1, and this recovers part of the first.

**It does not resolve the Ekvall double-counting question.** See §6. That was overstated in the
live session and is corrected here.

## 2. Why the elastic run was a bound and not an answer

F7 measured contact pressure on a fully elastic model. Real 7075-T7351 yields at the contact edge
well before limit load, and yielding redistributes bearing pressure away from the peak — which
raises `t_eff` and therefore the margin. An elastic model cannot see that. `MS = +0.078` was
correct as a conservative floor, not as a prediction.

## 3. Method

Identical to F7's ratio method, with plasticity added to the lug in **both** runs:

    t_eff / t = p_max(stiff pin) / p_max(real pin)

Contact pressure at a clearance-fit bore is mesh-singular — F7 documented a 134% rise across a
9.4x node increase with no sign of settling. Both runs share that singularity and it cancels in the
ratio. Adding plasticity does not change that argument, because the material model is identical
between the two runs; only the pin modulus differs.

### 3.1 Material model

| Property | Value | Source |
|---|---|---|
| Constitutive model | Bilinear isotropic hardening | — |
| Yield strength | **358.5 MPa** | A-basis `Fty` (L) = 52 ksi, `MARGIN_SUMMARY.md` §3 |
| Tangent modulus | **1631 MPa** | derived, §3.2 |
| Elongation used | 6% | MIL-HDBK-5J Table 3.7.6.0(b3), **LT direction, S-basis** |

### 3.2 Tangent modulus derivation, and a stated inconsistency

    E_t = (Ftu - Fty) / (e_f - e_y)
        = (448.2 - 358.5) / (0.06 - 0.005)
        = 1631 MPa

**Two bases are mixed here and it should be visible rather than buried.** `Fty` and `Ftu` are
A-basis; the elongation is S-basis, and it is tabulated for **LT** while the lug axis is **L** —
MIL-HDBK-5J does not give elongation for L on this page. For a hardening slope this is acceptable,
but the resulting curve is not a single-basis material definition and should not be quoted as one.

### 3.3 Model and settings

| | |
|---|---|
| Mesh | 203,472 nodes / 118,379 elements — the converged 0.75 mm bore sizing, unchanged from F7 |
| Large deflection | On |
| Auto time stepping | On, 10 initial / 5 min / 100 max substeps |
| Output | Last time point only |
| Pin, run 1 | Steel 4340, E = 200,000 MPa |
| Pin, run 2 | E = 4,000,000 MPa (20x steel, numerical reference) |
| Lug, both runs | 7075-T7351 with bilinear hardening |

## 4. Results

| | Elastic (F7) | **Elastic-plastic (F16)** | Change |
|---|---|---|---|
| `p_max` real pin | 2955.9 MPa | **2236.9 MPa** | −24.3% |
| `p_max` stiff pin | 2012.7 MPa | **1633.0 MPa** | −18.9% |
| **`t_eff/t`** | 0.6809 | **0.7300** | **+7.2%** |

Both peaks fall, as yielding requires. The real-pin peak falls further than the stiff-pin peak,
which is what raises the ratio: the real pin's higher peak had more plasticity available to relieve.

### 4.1 Equilibrium

| | Applied | Run 1 (real pin) | Run 2 (stiff pin) |
|---|---|---|---|
| Fx | 529,740 N | −529,740 | −529,740 |
| Fy | 0 | 0.0196 | −0.305 |
| Fz | 317,840 N | −317,840 | −317,840 |
| Total | 617,776 N | 617,780 | 617,770 |

**Agreement to ~10 ppm on both runs.** Fy is numerical noise at 1e-5 of the resultant. This also
satisfies the contact-resultant element of AFDT-REQ-009.

### 4.2 Confirmation that the material actually yielded

Peak plastic strain increments by substep: **0.62%, 1.48%, 1.84%, 2.88%, 3.76%, 2.33%, 2.21%**
across seven substeps to `TIME = 1.0`. Maximum equivalent plastic strain **6.456%**, scoped to the
lug body (volume 2.7234e-3 m³, confirming the correct body).

This is a genuine elastic-plastic run, not an elastic run wearing a plasticity card.

### 4.3 The plastic strain exceeds tabulated elongation

**6.456% against 6% elongation.** Bilinear isotropic hardening has no failure criterion, so the
material model simply continues hardening past the point where real 7075-T7351 would have fractured.

**This does not invalidate the ratio** — both runs share the material model, and the ratio cancels
effects common to both. But it does mean:

> **The 6.456% figure is not a rupture prediction.** It occurs at a mesh-refined contact edge where
> strain concentrates without bound, in the same singular region that makes absolute contact
> pressure meaningless. F16 gives pressure redistribution. It does not give a fracture assessment,
> and none should be inferred from it.

A ductile-failure assessment would need a damage model, a mesh-objective formulation at the contact
edge, and elongation data in the L direction — none of which exist in this project.

## 5. Margin re-propagation

Lug areas are linear in effective thickness, so both load ratios scale by `t_eff`:

    Ra, Rtr  x  (0.6809 / 0.7300) = 0.93274
    Ra = 0.36463,  Rtr = 0.72198
    MS = 1/(Ra^1.6 + Rtr^1.6)^0.625 - 1 = +0.1562

Same scaling argument as `F13_MANUFACTURING_INSPECTION.md` §7.1.

### 5.1 Effect on the F13 tolerance stack

The stack terms scale with the nominal. Worst-case consumption stays at 27.6% of nominal, so:

    MS worst-case tolerance stack: +0.156 -> approximately +0.113

Recomputing the stack exactly at the new operating point is a small open item; the bore-position
term remains extrapolated and remains dominant, so the precision of that re-propagation is limited
by the same thing it was before.

## 6. What this does NOT settle — correcting a live-session overstatement

During execution this run was described as settling whether the thick-lug correction and the Ekvall
scatter band double-count. **It does not, and that framing was wrong.**

The double-counting question is: *did Ekvall's 243 test specimens include thick lugs, such that the
thick-lug effect is already inside his measured scatter band?* That is a question about the
**composition of a 1986 test dataset**. No FE run on this fitting can answer it. It needs the
paper, to establish the specimen `t/D` range.

A decision threshold of `t_eff/t = 0.840` was carried in the project state as the trigger for that
call. The measured 0.7300 falls below it, so no double-counting credit is taken and both
corrections continue to apply — but that is the conservative default, not a resolution.

**`MARGIN_SUMMARY.md` open item "establish the t/D range of Ekvall's specimens" stays open.**

### 6.1 Ekvall band re-propagated at the new nominal

`(1 + MS)` scales as `1/r`:

| Ekvall ratio | On +0.078 (elastic) | **On +0.156 (elastic-plastic)** |
|---|---|---|
| Best, r = 0.85 | +0.269 | **+0.360** |
| Mean, r = 1.003 | +0.075 | **+0.153** |
| **Worst, r = 1.19** | **−0.094** | **−0.028** |

**The worst case is still negative, but far less so** — from −0.094 to −0.028.

The breakeven is `t_eff/t = 0.7513`: at that value the Ekvall worst case reaches exactly zero. The
measurement came in at **0.7300, just short of it.** That is an uncomfortably close miss and it is
the honest headline of this analysis: a better contact measurement nearly, but did not quite,
clear the worst-case scatter band.

## 7. Limitations

1. **The 20x pin still bends.** F7 established that a 20x-stiffness pin is not perfectly rigid, so
   the stiff-pin reference retains some through-thickness concentration and `t_eff/t` is biased.
   Both F7 and F16 use the same reference, so the **change** from 0.6809 to 0.7300 is more robust
   than either absolute value.
2. **One mesh only.** F7 converged the ratio across three bore meshes (0.7419 → 0.6670 → 0.6809,
   8.2% total movement). F16 ran only at the finest of those. The plastic ratio is **not
   independently mesh-converged**, and inherits F7's convergence argument rather than repeating it.
3. **Bilinear hardening is a two-parameter idealisation** of a real stress-strain curve, built on
   mixed-basis inputs (§3.2). A multilinear curve from measured data would be better.
4. **No failure criterion** — §4.3.
5. **Isotropic hardening** ignores the Bauschinger effect. Irrelevant for a monotonic run; it would
   matter for any cyclic extension of this work.
6. **The double-counting question is unresolved** — §6.

## 8. Provenance

| | |
|---|---|
| Solver | Ansys Mechanical 2025 R2, distributed, 4 cores |
| Model | restored from `f7converged.wbpz`, project `f7plastic` |
| Run 1 | real pin, converged 7 substeps, 0 errors |
| Run 2 | stiff pin, converged, 0 errors, weak springs added (expected, as in F7) |
| Executed | 2026-08-02 and 2026-08-03 |

A first attempt on 2026-08-02 solved to completion but was lost writing results to a network drive
with 1.08 GB free (`I/O status error 28`). The project was relocated to local disk and re-run. No
solver setting was changed as a result — only the storage location and `Store Results At`, which
was set to `Last Time Point` because the ratio method uses only the final converged state.
