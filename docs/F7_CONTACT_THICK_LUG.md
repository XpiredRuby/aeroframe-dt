# F7 — Pin/Lug Contact Analysis: Thick-Lug Bearing Distribution

**Closes the critical open item from `F6_PIN_BENDING_THICK_LUG.md`** — whether the +0.710 hand
margin survives the thick-lug effect at t/D = 1.25.

**Result: it survives, at about a quarter of its stated value.**
`MS = +0.710` becomes **`MS = +0.165`**, converged over three mesh densities.

**Claim boundary:** educational / representative / portfolio only. Non-OEM, non-certified.
All numbers `SYNTHETIC_TEST_ONLY`.

---

## 1. The question

The Melcon-Hoblit method behind the +0.710 margin is a **thin-lug** method: it assumes bearing
pressure is uniform through the lug thickness. At **t/D = 1.25** the pin bends and bearing
concentrates toward the lug faces.

F6 established the sensitivity by defining an effective bearing thickness `t_eff`:

| t_eff / t | MS |
|---|---|
| 1.00 | +0.710 |
| 0.80 | +0.368 |
| 0.70 | +0.197 |
| **0.585** | **0.000** |
| 0.50 | -0.145 |

The margin needed only 58.5% concentration to vanish. **This analysis measures `t_eff`.**

## 2. Model

Two bodies, from a single STEP built by `cad/build_f7.py`:

| Body | Material | E (MPa) | Mass |
|---|---|---|---|
| lug | 7075-T7351 | 71,700 | 7.6527 kg |
| pin | 4340 steel | 200,000 | 1.5367 kg |

Pin diameter 1.998 in in a 2.000 in bore, giving **0.0127 mm radial clearance**.
Pin length 3.810 in = `t1 + 2g + t2`, placing each flat end at the centroid of a balanced-shear
clevis ear (`t2 = 0.5 t1`, gap 0.030 in) so the moment arm matches the F6 hand calculation exactly.

**Contact:** one region, Frictional, mu = 0.1, Interface Treatment `Adjust to Touch`,
Update Stiffness `Each Iteration`.

**Boundary conditions:** Fixed Support on the flange underside (6.1688e-2 m2).
Force on the two pin end faces, Components, `Fx = 529,740 N`, `Fy = 0`, `Fz = 317,840 N`.
Weak Springs On to suppress the pin's axial float and spin about its own axis, neither of which
carries load.

### Setup error corrected mid-analysis

The first attempt **inverted the boundary conditions** — flange loaded, pin fixed. It diverged on
displacement DOF UY with "internal solution magnitude limit exceeded".

The diagnosis is quantitative. The load applied at the flange (Z = 0) against a bore at
Z = 0.1651 m produces a moment about the pin axis:

    M_y = 529,740 * 0.1651 = 87,460 N.m

A pin joint is a hinge and carries no moment about its own axis. The only resistance was friction:

    M_friction = mu * N * r = 0.1 * 617,776 * 0.0254 = 1,569 N.m

**Driven 56x harder than friction could hold.** The lug rotated off the pin. In the real fitting
the flange is bolted flat to the wingbox over 6.17e-2 m2; replacing that restraint with a force
deleted the thing holding the part. Reversing the boundary conditions fixed it.

## 3. Method — why the raw pressure cannot be used

The obvious extraction is `t_eff/t = p_uniform / p_max`, where
`p_uniform = 4P/(pi*D*t) = 243.8 MPa` is the peak of a cosine distribution with uniform
through-thickness bearing. Applied to the coarsest measured peak this gives 0.19 and a badly
negative margin.

**That would be wrong.** The measured peak contains three superimposed effects:

1. **Through-thickness concentration from pin bending** — the quantity we want
2. **Circumferential concentration from the 0.0127 mm radial clearance** — contact subtends a
   narrow arc rather than a full cosine. Nothing to do with pin bending.
3. **Elastic idealisation** — no yielding to flatten the peak

Only the first belongs in `t_eff`.

### The ratio method

Run the identical model twice, changing **only** the pin's Young's modulus. A stiff pin cannot
bend, so the through-thickness concentration disappears while clearance and elastic idealisation
remain **exactly identical**. Everything that is not pin bending cancels:

    t_eff / t = p_max(stiff pin) / p_max(real pin)

## 4. Mesh convergence — three points

Six solves: three bore mesh densities, each with a real pin (E = 200 GPa) and a stiff reference
(E = 4000 GPa, 20x). Global mesh held at 8 mm throughout.

| Bore mesh | Nodes | Elements | p_max real (MPa) | p_max stiff (MPa) | **t_eff/t** | **MS** | change |
|---|---|---|---|---|---|---|---|
| 3.00 mm | 21,744 | 15,204 | 1265.1 | 938.6 | 0.7419 | +0.269 | — |
| 1.50 mm | 58,780 | 34,209 | 2146.8 | 1432.0 | 0.6670 | +0.141 | -10.1% |
| **0.75 mm** | **203,472** | **118,379** | **2955.9** | **2012.7** | **0.6809** | **+0.165** | **+2.1%** |

### The absolute pressure does not converge

1265.1 -> 2146.8 -> 2955.9 MPa. A **134% rise** across a 9.4x increase in node count, still
climbing at the finest mesh. This is a **contact-edge singularity**: with a clearance-fit pin the
contact patch has a sharp edge, and the elastic pressure there grows without bound under
refinement.

**Any absolute contact pressure from this model is meaningless.** Reporting 1265 MPa, or 2956 MPa,
as a physical bearing pressure would be wrong.

### The ratio does converge

0.7419 -> 0.6670 -> 0.6809. Total movement **8.2%**, and the third step is **5x smaller** than the
second, in the opposite direction. Non-monotonic and settling around **0.67 to 0.68**.

**Both runs share the singularity, and it cancels.** This was the design intent of the ratio
method, stated as a hypothesis before the study. The study confirms it: the underlying quantity
diverges by 134% while the ratio moves 8% and converges.

### Two points would have given the wrong answer

At two points the sequence read 0.7419 -> 0.6670, a 10% fall. Extrapolating that trend
geometrically predicts `t_eff/t ~ 0.60` at 0.75 mm and **MS ~ +0.03** — effectively zero, and a
conclusion that the fitting only barely passes. The third point shows the ratio rebounding and
stabilising at 0.68.

`HANDOFF.md` records that convergence needs three or more points, and that two-point studies
misdiagnosed a singularity twice earlier in this project. **This is the third instance, and the
first where the two-point answer would have materially changed the engineering conclusion.**

## 5. Result

    t_eff / t = 0.681

    Ra  = 0.3578      (was 0.2437 under the thin-lug assumption)
    Rtr = 0.7194      (was 0.4899)
    MS  = +0.165      (was +0.710)

**Pin bending costs 77% of the margin.** The thin-lug method was optimistic by a factor of 4.3 on
margin at t/D = 1.25 — substantially worse than the factor of 2.8 suggested by the unconverged
first estimate. Bearing concentrates into 68% of the thickness, above the 58.5% that would drive
the margin to zero, but not by a wide band.

## 6. Model verification, from the solved archive

Read directly out of the solved files rather than taken on trust from the GUI.

**Material assignments as intended:**

    MP,EX,1,71700000000    Pa      lug, 71.7 GPa
    MP,EX,2,200000000000   Pa      pin, 200 GPa   <- real pin, not the stiff reference
    MP,DENS,1,2810 / MP,DENS,2,7850
    mp,mu,cid,0.1

**Bore resolution at the 3 mm mesh** (the coarsest of the three, so a lower bound on all of them):

| Quantity | Value |
|---|---|
| Nodes on the bore surface | 8,037 |
| Effective bore nodal spacing | 1.12 mm |
| Node layers through the 63.5 mm thickness | 111 |
| Median layer spacing | 0.54 mm |

Surface renders of this model look coarse because the far-field flange is coarse. That is
irrelevant — the measurement happens at the bore, which is finely resolved even at the coarsest
mesh used.

**Solver health:** 0 errors. Converged in 2 to 3 equilibrium iterations per substep, 5 substeps.
"Initial penetration is excluded" confirms `Adjust to Touch` took effect.

## 7. Caveats

**Elastic only, so +0.165 is conservative.** Real yielding at the bore edge would flatten the
pressure peak and raise `t_eff`, moving the margin back toward +0.710. **The true margin lies
between +0.165 and +0.710**, and +0.165 is the defensible lower bound.

**0.681 is an upper bound on t_eff/t from the stiffness side.** A 20x pin still bends, at roughly
1/20 the deflection, so a truly rigid reference would give a slightly lower ratio. The correction
is small relative to the 8% convergence band and does not change the conclusion.

**Contact status shows some over-constrained nodes**, and the solver logged
*"Coefficient ratio exceeds 1.0e8 - Check results"*. Both follow from holding the pin with weak
springs plus contact rather than a kinematic constraint. All six solves converged with zero errors,
so neither is treated as invalidating — but neither is dismissed.

**Mesh quality at 0.75 mm.** Ansys reported that some elements could not meet target metrics at the
finest density. The ratio at that mesh agrees with the 1.5 mm value to 2.1%, so the effect appears
small, but it is recorded.

**Clevis geometry is assumed.** `t2 = 0.5 t1`, gap 0.030 in. F6 showed pin bending stress rises 49%
if the ears are as thick as the lug, so a different clevis would shift `t_eff`. The mating fitting
(AF-DT-2000) remains undefined.

## 8. Conclusions

1. **The +0.710 margin survives, at MS = +0.165.** The fitting passes, with less margin than
   previously believed.
2. **The thin-lug method was optimistic by a factor of 4.3 on margin** at t/D = 1.25. A real,
   quantified methodological limitation, not a modelling artefact.
3. **`t_eff/t = 0.681`**, above the 0.585 failure threshold but without a wide band.
4. **Absolute contact pressure from this model is not usable** — it diverges under refinement. Only
   the ratio is meaningful.
5. **Any future lug work in this project at t/D above ~0.6 must carry this correction** or repeat
   this measurement.
6. All summary documents should state **+0.165 (thick-lug corrected, converged)** with +0.710 shown
   as the uncorrected thin-lug value.

## 9. Open

- [ ] Resolve the over-constrained contact nodes and the 1e8 coefficient ratio
- [ ] Elastic-plastic rerun to recover the yielding benefit, needs verified 7075-T7351 hardening data
- [ ] Define the AF-DT-2000 clevis and repeat if `t2` differs materially from 0.5 t1
- [ ] Re-propagate the Ekvall correlation band through +0.165 rather than +0.710
- [ ] F10 modal and eigenvalue buckling were planned in the same session and not run

## 10. Archive

| File | Size | Contents |
|---|---|---|
| `f7contact.wbpz` | 20.3 MB | 3 mm bore mesh, first solve |
| **`f7converged.wbpz`** | **335 MB** | **0.75 mm bore mesh, converged, real pin restored** |

Both on `C:\Users\vin` and the `H:` drive. Sizes confirm solution data is included.

Result images from the 3 mm run: `f7pressure`, `f7stress`, `f7deform`, `f7status`, `f7mesh`.
Note that the pressure and stress values in those images are from the unconverged coarse mesh and
are superseded by the table in section 4.
