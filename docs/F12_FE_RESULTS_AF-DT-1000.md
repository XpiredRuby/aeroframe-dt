# F12 Piece 2 — FE Results Log (Ekvall correlation specimen)

**Status:** IN PROGRESS — e/D = 1.5 solved, mesh convergence closed, sweep outstanding
**Claim boundary:** educational / representative / portfolio only. Non-OEM, non-certified.
All numbers `SYNTHETIC_TEST_ONLY`.

---

## 0. CORRECTION — geometry record, superseding first commit

The first version of this file recorded the specimen bounding box as
`Y = -160.8 .. 0.0, span 160.8 mm`. **That was wrong.**

It came from parsing `CARTESIAN_POINT` entities out of the STEP text. Circular arc extremes are
defined by centre plus radius and carry **no explicit control point at the crown**, so the crown of
the head was invisible to that parse. The reported span was the shank only.

Corrected by importing the file into the CAD kernel and asking for the real bounding box:

| Axis | Min | Max | Span |
|---|---|---|---|
| X | -40.200 | 40.200 | 80.400 mm (width w) |
| Y | **-160.800** | **+40.200** | **201.000 mm** |
| Z | 0.000 | 25.000 | 25.000 mm (thickness t) |

Kernel volume **372,567.1 mm^3**, matching the value recorded in `HANDOFF.md` §11 to
7 parts in 10^6. Closed-form check of the same profile
(`w*shank + 0.5*pi*r_head^2 - pi*(D/2)^2, times t`) returns 372,564.5 mm^3, agreeing to
0.0007%. Geometry is confirmed correct as built.

**Corrected layout:** hole centre at **Y = 0**. Head crown at **Y = +40.2**. Straight shank runs
**Y = 0 down to Y = -160.8**. Edge distance `e` is measured from hole centre to crown = 40.2 mm,
giving `e/D = 40.2 / 26.8 = 1.5` as intended.

**Impact on the solved runs: none.** Both boundary conditions were placed on features the bad
parse still identified correctly —

- Fixed support face at `Y = -160.8`, area 2010 mm^2 = 80.4 x 25. Still the correct tail face.
- Bearing load direction `+Y`, head pulled away from tail. Still correct; the head is at
  greater Y, which the error did not change.

Logged because a geometry record that is wrong in the repo is a latent trap for every later phase,
and because this is the third instance of the failure class named in `HANDOFF.md` §14 — a
reference derived from geometry without verifying what it actually measured.
**Rule going forward: bounding boxes and volumes come from the kernel, never from text-parsing
a STEP.**

---

## 1. Model definition

| Quantity | Value |
|---|---|
| Bore diameter D | 26.8 mm |
| Thickness t | 25.0 mm |
| Applied axial load P | 284,686 N (64,000 lbf) |
| Straight shank length below hole centre | 160.8 mm (held constant across the sweep) |

## 2. Material card — 7075-T651

| Property | Value |
|---|---|
| Density | 2810 kg/m^3 |
| Young's modulus E | 71,000 MPa |
| Poisson's ratio | 0.33 |
| Bilinear isotropic hardening — yield | 469 MPa |
| Bilinear isotropic hardening — tangent modulus | 760 MPa |

**Note on E:** the source paper prints 1.03e6 psi = 7.1 GPa. That is a typo — aluminium is
10.3e6 psi = 71 GPa. 71,000 MPa used. Recorded so the deviation from the printed source is
explicit and auditable.

Hand-check allowables (not used in the FE run): Ftu 517 MPa, Fty/Fcy 469 MPa, Fsu 303 MPa.

## 3. Boundary conditions

**Bearing Load** — scoped to bore inner cylindrical face (1 Face, r = 1.34e-2 m, continuous, not a
split half-bore). Define By Components, Global CS. `Fx = 0, Fy = 284,686 N, Fz = 0`.

**Fixed Support** — flat tail end face at Y = -160.8. Face area 2.01e-3 m^2 = 80.4 x 25 mm.

**Global mesh** — 6 mm throughout. Bore face sizing varied for the convergence study below.

### Method note — direction picking

First attempt used the Direction geometry picker on the bore. That selection returned the
**cylindrical face** (status bar: "1 Cylinder Selected, Radius = 1.34e-002 m"), which supplies a
radial reference, not an axial direction. Abandoned in favour of explicit Components entry with
the load axis confirmed independently from measured geometry.

---

## 4. Mesh convergence study — e/D = 1.5

Three points, bore-face element size varied 4x. Global size, material, load and support held
identical across all three.

| Bore face size | Peak von Mises (MPa) | Max deformation (mm) | Reaction Y (N) |
|---|---|---|---|
| 4 mm | 510.13 | 0.63167 | -284,690 |
| 2 mm | 490.45 | 0.63186 | -284,690 |
| 1 mm | 494.76 | 0.63242 | -284,690 |

### Interpretation

**Deformation is converged.** Spread across the full 4x refinement is 0.12%, monotonically
increasing (0.63167 -> 0.63186 -> 0.63242). This is the primary convergence metric and it is
settled.

**Reaction force is mesh-independent.** Identical to all displayed digits at every refinement,
and equal to the applied 284,686 N. Equilibrium does not depend on discretisation, as it should
not.

**Peak von Mises does not converge monotonically — and that is the useful result.**
The sequence is 510.13 -> 490.45 -> 494.76: non-monotonic, contained in a +/-2.0% band about a
498.45 MPa mean, total range 19.68 MPa.

The purpose of this three-point study was to test for a stress singularity at the loaded bore edge
(`HANDOFF.md` §14: two-point studies misdiagnosed a singularity twice previously). A true
singularity produces peak stress that **climbs without bound** under refinement. This sequence does
not climb at all — it oscillates inside a narrow band and shows no refinement trend.
**Singularity ruled out.**

The oscillation is attributable to plastic redistribution combined with mesh-dependent integration
point sampling near the contact edge, not to a divergent field. All three values sit 4.6% to 8.8%
above the 469 MPa yield, consistent with a nearly perfectly plastic card (tangent modulus
760 MPa) capping the concentration just above yield.

**Consequence for the sweep:** peak von Mises is a plasticity-limited quantity here and must not
be reported as a converged elastic peak or used alone for correlation. Deformation and reaction are
the reliable per-run outputs. The 2 mm bore size is adopted for the remaining e/D runs — it sits
within the converged band and costs a fraction of the 1 mm solve.

---

## 5. Results — e/D = 1.5, 2 mm bore mesh (reference run)

| Output | Value | Location |
|---|---|---|
| Peak von Mises | **490.45 MPa** | bore edge, loaded side |
| Min von Mises | 7.83 MPa | lower shank |
| Max total deformation | **0.632 mm** | bore |
| Force reaction, Y | **-284,690 N** | fixed support |
| Force reaction, X | -2.33e-7 N (numerical zero) | fixed support |
| Force reaction, Z | -4.95e-8 N (numerical zero) | fixed support |

Solver: MAPDL, status Done, 14 s elapsed, 4 substeps (nonlinear material engaged).

### Independent cross-checks

**Equilibrium.** Reaction Y 284,690 N vs applied 284,686 N; off-axis reactions at 1e-7 N.
Load and support correctly scoped; load purely axial as intended.

**Nominal bearing stress.**
`Sbr = P / (D*t) = 284,686 / (26.8*25) = 425.0 MPa`
Peak von Mises exceeds nominal bearing by 1.15x — the expected order for a bore-edge
concentration after plastic redistribution.

**Nominal net-section stress.**
`Anet = (w-D)*t = (80.4-26.8)*25 = 1340 mm^2`
`Snet = 284,686 / 1340 = 212.5 MPa` — well below yield; net section is not the driver.

**Nominal shear-out stress.**
`Ashear = 2*(e - D/2)*t = 2*(40.2-13.4)*25 = 1340 mm^2`
`Ssh = 284,686 / 1340 = 212.5 MPa` vs Fsu 303 MPa.

Bearing governs at e/D = 1.5, consistent with expectation for this geometry.

**Deformation is length-dependent.** The 0.632 mm figure is specific to the 160.8 mm shank and is
not a transferable lug property. Retained as a convergence and equilibrium metric, not as a
correlation quantity.

---

## 6. Sweep geometry — generated set

Built parametrically: `e = (e/D)*D`, `w = 2*(e/D)*D`, head radius `= w/2`, shank held at
160.8 mm so only head geometry varies across the sweep.

| e/D | e (mm) | w (mm) | Volume (mm^3) | Mass at 2810 kg/m^3 |
|---|---|---|---|---|
| 1.0 | 26.80 | 53.60 | 229,574.6 | 0.645 kg |
| 1.2 | 32.16 | 64.32 | 285,079.3 | 0.801 kg |
| 1.5 | 40.20 | 80.40 | **372,567.1** | **1.047 kg** |
| 1.8 | 48.24 | 96.48 | 465,131.9 | 1.307 kg |
| 2.0 | 53.60 | 107.20 | 529,662.3 | 1.488 kg |

Every kernel volume agrees with the closed-form profile area times thickness to within
floating-point noise. The e/D = 1.5 rebuild reproduces the volume of the already-solved file
(372,567.1 mm^3) identically — this is what validates the generator against a known-good part.

Mass figures are the import verification check. If Ansys reports a different mass, the wrong file
was imported.

Generator: `cad/build_lug_sweep.py`.

---

## 7. Open — required before this piece can be called done

- [x] Mesh convergence at e/D = 1.5 (4 / 2 / 1 mm) — singularity ruled out
- [ ] e/D = 1.0 run
- [ ] e/D = 1.2 run
- [ ] e/D = 1.8 run
- [ ] e/D = 2.0 run
- [ ] Margin-vs-e/D comparison against the published curves
- [ ] Confirm the published shear-out and bearing curves cross at e/D = 1.5
