# F5 FE — Rev D Pylon Fitting, Linear Elastic Run

**Status:** model verified. **This run does NOT validate the +0.71 hand margin.** See §6.
**Claim boundary:** educational / representative / portfolio only. Non-OEM, non-certified.
All numbers `SYNTHETIC_TEST_ONLY`.

---

## 1. Geometry

The Rev D STEP did not exist on the VDI when this run was attempted — only revB and revC were
present, and both predate the Rev D changes (`t_lug` 1.500 -> 2.500, `g_y` 2.000 -> 4.000).
Using revC would have analysed a different part from the one the +0.71 margin covers.

Rebuilt from `cad/build_revD.py`, then rescaled by `cad/build_revD_to_mm.py`.

**Unit fault found in the generator chain.** `build_revD.py` works in inches, but cadquery's STEP
exporter declares `SI_UNIT(.MILLI.,.METRE.)`. The raw export therefore describes a part 25.4x too
small — 16 mm long instead of 16 in, mass about 0.47 grams instead of 7.65 kg. Importing it
directly would have produced a silently wrong model. The rescale script applies a uniform 25.4
factor and gates on mass before writing.

| Check | Built | Published Rev D | Ansys reported |
|---|---|---|---|
| Volume | 2,723,301 mm^3 | 166.19 in^3 | 2.7231e-3 m^3 |
| Mass at 2810 kg/m^3 | 7.6525 kg | 7.65 kg | 7.6519 kg |
| Bounding box | 406.40 x 152.40 x 228.60 mm | 16 x 6 x 9 in | — |
| Bore | 1 face, r = 25.40 mm | d_pin 2.000 in | 1 face, 1.013e-2 m^2 |
| Fastener holes | 8 at r = 3.175 mm | d_fast 0.250 in | — |
| Blend faces | 8 at r = 12.70 mm | r_blend 0.500 in | — |

Volume agreement 0.007%, mass agreement 0.008% — translation noise between CAD kernels.

**Correction to a stale gate.** `HANDOFF.md` previously instructed verifying bore area against
**6.078e-3 m^2**. That figure derives from `t_lug = 1.500 in`, i.e. **Rev A thickness**, and was
never updated when Rev D thickened the lug. The correct Rev D bore area is
`pi * d_pin * t_lug = pi * 50.8 * 63.5 = 10,134 mm^2 = 1.0134e-2 m^2`. Using the old number as a
gate would have rejected a correctly scoped bore.

The handoff also warned to confirm scoping covered **both half-cylinder faces**. In this
parametrically rebuilt geometry **the bore is a single continuous cylindrical face**, not two
halves. Face count of 1 is correct here; the earlier warning applied to a differently built file.

## 2. Model setup

**Material — linear elastic only.** 7075-T7351, density 2810 kg/m^3, E = 71,700 MPa, nu = 0.33.
**No plasticity model was defined.** There is no verified yield strength or tangent modulus for
7075-T7351 in this project, and inventing one would introduce exactly the kind of unverified number
this project refuses to carry. Linear elastic is also the correct basis for comparison against a
stress-allowable hand method, and it avoids the plasticity-interpretation problems documented in
`F12_STRESS_STRAIN_CONSISTENCY.md`.

**Scoping by Named Selection worksheet rule**, per the method established in F12.

| Target | Rule | Result |
|---|---|---|
| Bore | `Face / Radius / Equal / 0.0254 m` | 1 face, 1.013e-2 m^2 |
| Flange underside | `Face / Location Z / Smallest` | 1 face, 6.1688e-2 m^2 |

The `Smallest` operator was deliberately **not** used for the bore: this part also carries blend
radii of 0.0127 m and fastener holes of 0.003175 m, so `Smallest` would have selected a fastener
hole. Computed flange underside area for confirmation: 61,682 mm^2 = 6.1682e-2 m^2, against 6.1688e-2
reported — 0.01%. The next-nearest plane by Z is 20x smaller in area, so misidentification is not
plausible.

**Loads — Rev C basis.** Bearing Load on the bore, Components, Global CS:
`Fx = 529,740 N`, `Fy = 0`, `Fz = 317,840 N`. Ansys computed the resultant as **617,780 N**;
`sqrt(529740^2 + 317840^2) = 617,776 N`.

**Fixed Support** on the flange underside.

## 3. Mesh convergence study

Global element size held at 8 mm. Only the bore face sizing varied.

| Bore sizing | Nodes | Elements | Peak vM (MPa) | Deformation (mm) | Reaction X (N) | Reaction Z (N) |
|---|---|---|---|---|---|---|
| 4 mm | 30,764 | 17,689 | 1209.4 | 3.5695 | -530,130 | -318,080 |
| 2 mm | 55,335 | 32,474 | 1187.1 | 3.5696 | -529,860 | -317,910 |
| 1 mm | 152,951 | 91,672 | **1194.1** | **3.5686** | -529,770 | -317,860 |

### Peak stress — converged, singularity ruled out

Sequence 1209.4 -> 1187.1 -> 1194.1, **non-monotonic, within +/-0.95% of a 1196.9 MPa mean** across
a 16x increase in element count. A singularity climbs without bound under refinement; this does not
climb at all.

This is geometrically expected. The maximum sits where the bore breaks through the top face of the
lug — an edge where two **free surfaces meet at 90 degrees**. A convex free-surface corner of that
kind does not produce an elastic singularity, unlike a re-entrant corner. A finite converged peak is
the correct behaviour.

### Deformation — converged

3.5695 -> 3.5696 -> 3.5686 mm. **0.03% spread.** This is the most trustworthy quantity in the run.

### Reaction — faceting error, prediction confirmed

Before the study it was predicted that the reaction overshoot was **mesh faceting of the curved
bore**, and therefore that it would shrink under refinement. Recorded before the runs.

| Bore sizing | Reaction resultant (N) | Error vs applied 617,776 N |
|---|---|---|
| 4 mm | 618,234 | +0.074% |
| 2 mm | 617,914 | +0.022% |
| 1 mm | **617,811** | **+0.006%** |

Monotonic, roughly 3.5x reduction per 2x refinement. **Confirmed.** This also rules out a scoping or
load-definition fault, which would produce a fixed offset rather than a converging one.

## 4. Results — converged run, 1 mm bore mesh

| Output | Value | Location |
|---|---|---|
| Peak von Mises | **1194.1 MPa** | bore edge, where the hole breaks the top face |
| Max total deformation | **3.5686 mm** | boss / bore region, far from the fixed flange |
| Reaction X | -529,770 N | flange underside |
| Reaction Y | ~0 (4.7e-4 N) | flange underside |
| Reaction Z | -317,860 N | flange underside |

Solve time 18 s, 152,951 nodes.

## 5. Nominal stress cross-checks

    Bearing:      617,776 / (50.8 * 63.5)    = 191.5 MPa
    Net section:  317,840 / ((101.6-50.8)*63.5) = 98.5 MPa

Both are far below Ftu of approximately 489 MPa (71 ksi representative). **The part is not grossly
overstressed in nominal terms.**

Implied elastic concentration factor at the bore edge:

    Kt = 1194.1 / 191.5 = 6.24

## 6. CRITICAL — what this run does and does not establish

**It does NOT validate the +0.71 hand margin. It cannot, as configured.**

The +0.71 comes from empirical lug allowables (P'bru, P'tu, P'tru) derived from the
Melcon-Hoblit method. **Those allowables already incorporate the stress concentration and local
plastic redistribution at the bore.** A linear elastic peak stress is a different physical quantity.
Comparing 1194 MPa against an allowable-based margin is a category error.

The converged peak of 1194 MPa is **2.44x Ftu**. In a linear elastic model this does not indicate
failure — it indicates that the real material would yield locally at the bore edge, which is
precisely the behaviour the empirical allowables are built to absorb. Reporting it as an overstress
finding would be wrong.

**What this run DOES establish:**

1. **The Rev D model is sound.** Equilibrium closes to 0.006%, all three boundary conditions scope
   correctly, and geometry matches the published mass to 0.008%.
2. **Mesh convergence is demonstrated** on three points, with a singularity ruled out by the
   non-monotonic behaviour and by the convex free-surface geometry of the peak location.
3. **The critical location is the bore**, not the blade-to-flange fillet. This matters: it confirms
   the lug method is being applied at the location that actually governs.
4. **Nominal stresses are well within allowables**, so the part is not grossly undersized.
5. **A verified elastic baseline** now exists for the later phases — F7 contact, F8/F9 fatigue,
   F10 dynamics, F11 optimisation — all of which need a trustworthy elastic model first.

**To actually cross-check the +0.71 would require either:**
- an elastic-plastic run with a **verified** yield and hardening curve for 7075-T7351, which this
  project does not currently have and must not invent, or
- computing the FE bearing and net-section stresses on the same nominal areas the hand method uses,
  and comparing those against the same empirical allowables — comparing like with like rather than
  peak stress against allowable.

The second is the cheaper and more defensible route and is recommended.

## 7. Predictions recorded before the run, and outcomes

Two of three were wrong. Retained as recorded.

**Location — WRONG.** Predicted the peak would fall at the blade-to-flange fillet, based on a
cantilever estimate giving roughly 680 MPa root bending stress. **It fell at the bore instead.**
The cantilever model was inapplicable: at L/h = 1.4 the blade is far too stubby for beam theory and
behaves closer to a shear panel, and the estimate also ignored the 12.7 mm fillet and the restraint
from the flange.

**Deformation — WRONG.** Bracketed at 0.3 to 1.2 mm, deliberately loose. **Measured 3.5686 mm**,
about 3x the upper bound. Same root cause: beam-theory intuition applied to a geometry it does not
suit.

**Reaction convergence — CORRECT.** Predicted the reaction overshoot was faceting of the curved bore
and would shrink under refinement. It fell 0.074% -> 0.022% -> 0.006%, monotonically. See §3.

## 8. Open

- [ ] Compare FE nominal bearing and net-section stresses against the empirical lug allowables,
      like for like. This is the real cross-check of the +0.71.
- [ ] Verified yield and hardening data for 7075-T7351, if an elastic-plastic run is ever wanted
- [ ] `build_revD.py` docstring still says `t_web -> 1.250`; actual value is 2.500
- [ ] Peak stress location has no chamfer modelled at the bore mouth; a real part would have one,
      and it would reduce the local concentration

## 9. Archive

`revdrun.wbpz`, 8.85 MB, on both `C:\Users\vin` and the `H:` drive. Size confirms solution data is
included — a 1-2 MB archive would indicate results were dropped.
