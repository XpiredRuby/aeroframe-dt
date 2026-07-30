# F7 — Pin/Lug Contact Analysis: Thick-Lug Bearing Distribution

**Closes the critical open item from `F6_PIN_BENDING_THICK_LUG.md`** — whether the +0.710 hand
margin survives the thick-lug effect at t/D = 1.25.

**Result: it survives, at roughly a third of its stated value.**
`MS = +0.710` becomes **`MS ≈ +0.25`**.

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

Two bodies, imported as a single STEP built by `cad/build_f7.py`:

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

**Mesh:** 8 mm global, 3 mm on the bore.

**Solve:** converged, 22 s, 5 substeps.

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

## 3. Method — why the raw pressure cannot be used directly

The obvious extraction is `t_eff/t = p_uniform / p_max`, where
`p_uniform = 4P/(pi*D*t) = 243.8 MPa` is the peak of a cosine distribution with uniform
through-thickness bearing. Applied to the measured 1265.1 MPa this gives 0.19 and a badly negative
margin.

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

## 4. Result

| Run | Pin E (MPa) | Peak contact pressure |
|---|---|---|
| Real pin | 200,000 | **1265.1 MPa** |
| Stiff reference | 4,000,000 (20x) | **938.6 MPa** |

    t_eff / t = 938.6 / 1265.1 = 0.742

Both peaks occur on `lug\lug`, at the bore.

The stiff-pin run was reverted to E = 200,000 MPa afterwards and re-solved, returning 1265.1 MPa
exactly — confirming the model was restored and that the difference was caused by the modulus
change alone and nothing else.

### Corrected margin

    Ra  = 0.3284      (was 0.2437)
    Rtr = 0.6603      (was 0.4899)
    MS  = +0.269      (was +0.710)

**Pin bending costs 62% of the margin.** The thin-lug method was materially optimistic at
t/D = 1.25, exactly as F6 predicted. But bearing concentrates to 74% of the thickness, not the
58.5% that would have driven the margin to zero.

## 5. Bounds and caveats

**0.742 is an upper bound on t_eff/t.** A 20x pin still bends, at roughly 1/20 the deflection.
Extrapolating the residual to a truly rigid pin gives `t_eff/t ~ 0.729` and **MS ~ +0.247**. The
correction is small and does not change the conclusion.

**+0.25 is conservative in the other direction.** Both runs are linear elastic. Real yielding at
the bore edge would flatten the pressure peak and raise `t_eff`, moving the margin back toward
+0.710. **The true margin lies between +0.25 and +0.71**, and +0.25 is the defensible lower bound.

**Single mesh.** This is one mesh density, not a convergence study. `HANDOFF.md` §16 records that
convergence needs three points and that two-point studies misdiagnosed a singularity twice in this
project. The ratio is more robust than either absolute value, since mesh-dependent peak effects
appear in numerator and denominator alike — but it is reported as a **bounded estimate**, not a
converged value.

**Clevis geometry is assumed.** `t2 = 0.5 t1`, gap 0.030 in. F6 showed pin bending stress rises 49%
if the ears are as thick as the lug, so a different clevis would shift `t_eff`. The mating fitting
(AF-DT-2000) remains undefined.

## 6. Conclusions

1. **The +0.710 margin survives, at MS ~ +0.25.** The fitting passes.
2. **The thin-lug method was optimistic by a factor of ~2.8 on margin** at t/D = 1.25. This is a
   real, quantified methodological limitation, not a modelling artefact.
3. **`t_eff/t = 0.742`**, comfortably above the 0.585 failure threshold but far below the 1.0 the
   hand method assumed.
4. **Any future lug work in this project at t/D above ~0.6 must carry this correction** or repeat
   this measurement.
5. The stated margin in all summary documents should be **+0.25 (thick-lug corrected)** with
   +0.710 shown as the uncorrected thin-lug value, not the other way round.

## 7. Open

- [ ] Mesh convergence on the pressure ratio — 3 points at 3 / 1.5 / 0.75 mm bore sizing
- [ ] Elastic-plastic rerun to recover the yielding benefit, needs verified 7075-T7351 hardening data
- [ ] Define the AF-DT-2000 clevis and repeat if `t2` differs materially from 0.5 t1
- [ ] Ekvall correlation band should be re-propagated through +0.25 rather than +0.710

## 8. Archive

`f7contact.wbpz`, 20.3 MB, on both `C:\Users\vin` and the `H:` drive. Size confirms solution data
is included.

Result images on `H:`: `f7pressure`, `f7stress`, `f7deform`, `f7status`, `f7mesh`.
