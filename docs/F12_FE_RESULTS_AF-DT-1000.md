# F12 Piece 2 — FE Results Log (Ekvall correlation specimen)

**Status:** IN PROGRESS — first datapoint captured
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

**Impact on the solved run: none.** Both boundary conditions were placed on features the bad
parse still identified correctly —

- Fixed support face at `Y = -160.8`, area 2010 mm^2 = 80.4 x 25. Still the correct tail face.
- Bearing load direction `+Y`, head pulled away from tail. Still correct; the head is at
  greater Y, which the error did not change.

So §6 results stand. No rework. Logged because a geometry record that is wrong in the repo is a
latent trap for every later phase, and because this is the third instance of the same failure class
already named in `HANDOFF.md` §14 — a reference derived from geometry without verifying what it
actually measured. **Rule going forward: bounding boxes and volumes come from the kernel, never
from text-parsing a STEP.**

---

## 1. Model definition

**Specimen:** straight lug, published correlation geometry.

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

## 3. Mesh

| Control | Setting |
|---|---|
| Face Sizing — bore inner cylindrical face | 2 mm |
| Global element size | 6 mm |

Bore face scoping confirmed as 1 Face, radius 1.34e-2 m — a single continuous cylindrical face,
not a split half-bore.

## 4. Boundary conditions

**Bearing Load**
- Scoped to bore inner cylindrical face (1 Face)
- Define By: Components, Global Coordinate System
- Fx = 0, **Fy = 284,686 N**, Fz = 0
- Direction +Y, head pulled away from tail

**Fixed Support**
- Flat end face at Y = -160.8 (tail, farthest from bore)
- Face area 2.01e-3 m^2 = 80.4 x 25 mm

## 5. Method note — direction picking

First attempt used the Direction geometry picker on the bore. That selection returned the
**cylindrical face** (status bar: "1 Cylinder Selected, Radius = 1.34e-002 m"), which supplies a
radial reference, not an axial direction. Abandoned in favour of explicit Components entry with
the load axis confirmed independently from measured geometry.

## 6. Results — e/D = 1.5, 2 mm bore mesh

| Output | Value | Location |
|---|---|---|
| Peak von Mises | **490.45 MPa** (4.9045e8 Pa) | bore edge, loaded side |
| Min von Mises | 7.83 MPa | lower shank |
| Max total deformation | **0.632 mm** (6.3186e-4 m) | bore |
| Force reaction, Y | **-284,690 N** | fixed support |
| Force reaction, X | -2.33e-7 N (numerical zero) | fixed support |
| Force reaction, Z | -4.95e-8 N (numerical zero) | fixed support |

Solver: MAPDL, status Done, 14 s elapsed, 4 substeps (nonlinear material engaged).

## 7. Verification of this datapoint

**Equilibrium.** Reaction Y magnitude 284,690 N vs applied 284,686 N. Off-axis reactions at
1e-7 N, i.e. numerical zero. Load and support correctly scoped; load is purely axial as intended.

**Plasticity consistency.** Peak von Mises 490.45 MPa against 469 MPa yield. With a tangent
modulus of 760 MPa the material is very nearly perfectly plastic, so the bore-edge concentration
is capped just above yield rather than growing elastically. Peak/yield = 1.046.

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
not a transferable lug property. It is retained as a convergence metric and an equilibrium sanity
check, not as a correlation quantity.

## 8. Sweep geometry — generated set

Built parametrically, `e = (e/D)*D`, `w = 2*(e/D)*D`, head radius `= w/2`, shank held at
160.8 mm so that only head geometry varies across the sweep.

| e/D | e (mm) | w (mm) | Volume (mm^3) | Closed-form check |
|---|---|---|---|---|
| 1.0 | 26.80 | 53.60 | 229,574.6 | exact |
| 1.2 | 32.16 | 64.32 | 285,079.3 | exact |
| 1.5 | 40.20 | 80.40 | **372,567.1** | exact |
| 1.8 | 48.24 | 96.48 | 465,131.9 | exact |
| 2.0 | 53.60 | 107.20 | 529,662.3 | exact |

Every kernel volume agrees with the closed-form profile area times thickness to within
floating-point noise. The e/D = 1.5 rebuild reproduces the volume of the already-solved file
(372,567.1 mm^3) identically, which is what validates the generator against a known-good part.

**Mass check for import verification** (density 2810 kg/m^3): e/D = 1.5 part should read
**1.047 kg**. If Ansys reports something else, the wrong file was imported.

## 9. Open — required before this piece can be called done

- [ ] Mesh convergence at e/D = 1.5: bore-face element size 4 mm / 2 mm / 1 mm.
      Three points minimum (`HANDOFF.md` §14 — two points misdiagnosed a singularity twice).
- [ ] e/D = 1.0 run
- [ ] e/D = 1.2 run
- [ ] e/D = 1.8 run
- [ ] e/D = 2.0 run
- [ ] Margin-vs-e/D comparison against the published curves
- [ ] Confirm the published shear-out and bearing curves cross at e/D = 1.5

**Caution on the convergence study.** Peak von Mises at a loaded bore edge under a nearly
perfectly plastic material card is a plasticity-limited quantity, not a free elastic peak. It will
converge much flatter than an elastic stress concentration would. That flatness must not be read
as proof of a converged elastic field. Reaction force and total deformation are the better
convergence metrics here and are to be tracked alongside peak stress.
