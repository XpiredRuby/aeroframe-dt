# F12 Piece 2 — FE Results Log (Ekvall correlation specimen)

**Status:** IN PROGRESS — e/D = 1.5 and 1.0 solved, mesh convergence closed
**Claim boundary:** educational / representative / portfolio only. Non-OEM, non-certified.
All numbers `SYNTHETIC_TEST_ONLY`.

---

## 0. CORRECTION — geometry record, superseding first commit

The first version of this file recorded the specimen bounding box as
`Y = -160.8 .. 0.0, span 160.8 mm`. **That was wrong.**

It came from parsing `CARTESIAN_POINT` entities out of the STEP text. Circular arc extremes are
defined by centre plus radius and carry **no explicit control point at the crown**, so the crown of
the head was invisible to that parse. The reported span was the shank only.

Corrected by importing the file into the CAD kernel:

| Axis | Min | Max | Span |
|---|---|---|---|
| X | -40.200 | 40.200 | 80.400 mm |
| Y | **-160.800** | **+40.200** | **201.000 mm** |
| Z | 0.000 | 25.000 | 25.000 mm |

Kernel volume **372,567.1 mm^3**, matching `HANDOFF.md` §11 to 7 parts in 10^6. Closed-form check
of the same profile returns 372,564.5 mm^3, agreeing to 0.0007%.

**Corrected layout:** hole centre at Y = 0, head crown at Y = +40.2, straight shank Y = 0 down to
Y = -160.8. Edge distance `e` measured hole centre to crown.

**Impact on solved runs: none.** Both boundary conditions sat on features the bad parse still
identified correctly. Logged because a wrong geometry record in the repo is a latent trap, and
because this is the third instance of the failure class in `HANDOFF.md` §14.
**Rule: bounding boxes and volumes come from the kernel, never from text-parsing a STEP.**

---

## 1. Model definition

| Quantity | Value |
|---|---|
| Bore diameter D | 26.8 mm |
| Thickness t | 25.0 mm |
| Applied axial load P | 284,686 N (64,000 lbf) |
| Straight shank length below hole centre | 160.8 mm (held constant across sweep) |

## 2. Material card — 7075-T651

| Property | Value |
|---|---|
| Density | 2810 kg/m^3 |
| Young's modulus E | 71,000 MPa |
| Poisson's ratio | 0.33 |
| Bilinear isotropic hardening — yield | 469 MPa |
| Bilinear isotropic hardening — tangent modulus | 760 MPa |

**Note on E:** source paper prints 1.03e6 psi = 7.1 GPa. That is a typo — aluminium is
10.3e6 psi = 71 GPa. 71,000 MPa used, deviation recorded so it stays auditable.

Hand-check allowables: Ftu 517 MPa, Fty/Fcy 469 MPa, Fsu 303 MPa.

**Model limitation, load-bearing on interpretation below.** Bilinear isotropic hardening has
**no failure criterion**. It will harden indefinitely and report stresses far beyond any strain the
real material could reach. Every run must therefore be checked against equivalent plastic strain
before its peak stress is quoted. See §7.

## 3. Boundary conditions (identical across all runs)

**Bearing Load** — bore inner cylindrical face, 1 Face, r = 1.34e-2 m, continuous.
Define By Components, Global CS. `Fx = 0, Fy = 284,686 N, Fz = 0`.

**Fixed Support** — flat tail end face at minimum Y.

**Mesh** — 6 mm global, 2 mm bore face sizing.

### Method note 1 — direction picking

The Direction geometry picker on the bore returns the **cylindrical face** ("1 Cylinder Selected,
Radius = 1.34e-002 m"), a radial reference, not an axial direction. Abandoned for explicit
Components entry with the load axis confirmed from measured geometry.

### Method note 2 — scoping after a geometry swap

Replacing the geometry invalidates every scoped selection. Ansys keeps displaying the stale
attachment, so Details can still read "1 Face" when nothing is actually attached. **Reliable
tells:** a magenta "Old Geometry Tessellation" overlay in the viewport, and Number of Matched
Entities = 0 in the scoping worksheet.

On narrow end faces, manual re-picking proved impractical under a streamed desktop (no drag, face
presents as a sliver). **Adopted method: scope by Named Selection worksheet rule instead of by
click.** For the tail face: `Entity Type = Face, Criterion = Location Y, Operator = Smallest`.
Selects uniquely, needs no typed value, no rotation, and is geometry-independent — the shank
length is held constant so this rule holds for every e/D in the sweep.

---

## 4. Mesh convergence study — e/D = 1.5

| Bore face size | Peak von Mises (MPa) | Max deformation (mm) | Reaction Y (N) |
|---|---|---|---|
| 4 mm | 510.13 | 0.63167 | -284,690 |
| 2 mm | 490.45 | 0.63186 | -284,690 |
| 1 mm | 494.76 | 0.63242 | -284,690 |

**Deformation converged** — 0.12% spread across a 4x refinement, monotonic.
**Reaction mesh-independent** — identical at every refinement, equal to applied load.

**Peak von Mises does not converge monotonically, and that is the useful result.**
510.13 -> 490.45 -> 494.76: non-monotonic, within +/-2.0% of a 498.45 MPa mean.

The study existed to test for a bore-edge singularity (`HANDOFF.md` §14: two-point studies
misdiagnosed one twice). A singularity climbs without bound under refinement. This does not climb
at all. **Singularity ruled out.** The oscillation is plastic redistribution plus mesh-dependent
integration point sampling.

2 mm bore sizing adopted for the sweep — inside the converged band, fraction of the 1 mm cost.

---

## 5. Results — e/D = 1.5

| Output | Value |
|---|---|
| Peak von Mises | 490.45 MPa |
| Max total deformation | 0.632 mm |
| Force reaction Y | -284,690 N |
| Force reaction X, Z | -2.33e-7, -4.95e-8 N (numerical zero) |

Solver: 14 s, 4 substeps.

**Nominal bearing** `Sbr = P/(D*t) = 284,686/670 = 425.0 MPa`
**Nominal net section** `Anet = (w-D)*t = 1340 mm^2`, `Snet = 212.5 MPa` vs Ftu 517
**Nominal shear-out** `Ash = 2*(e-D/2)*t = 1340 mm^2`, `Ssh = 212.5 MPa` vs Fsu 303

All below allowable. Specimen passes at e/D = 1.5.

---

## 6. Results — e/D = 1.0

Geometry verified on import: mass 0.64504 kg against 0.645 kg predicted, volume 229,550 mm^3
against 229,575 mm^3. Correct file confirmed.

| Output | Value |
|---|---|
| Peak von Mises | 750.23 MPa |
| Max total deformation | **7.655 mm** |
| Max equivalent plastic strain | **0.37211 m/m** |
| Force reaction Y | -284,690 N |
| Force reaction X, Z | 6.67e-8, 5.34e-9 N (numerical zero) |

Solver: ~14 s, 7 substeps (auto time stepping subdivided to reach convergence — itself an
indicator of strong nonlinearity).

Max plastic strain located at the bore edge on the loaded side, toward the head crown.

### Mesh-setting fault found and corrected before this run

Global element size read **6.e-006 m** — 6 micrometres on a 200 mm part. An earlier mesh attempt
ran past 10 minutes without completing. Corrected to 6.e-003 m; mesh then completed in seconds at
10,191 nodes / 1,998 elements.

Same failure mode as the Engineering Data material card at project start: a value entered while
the unit selector was on a different setting, then **converted rather than relabelled** when the
unit was changed. Third occurrence of this class in the project.
**Rule: after changing any unit dropdown, re-read the numeric field before proceeding.**

---

## 7. Interpretation of e/D = 1.0 — specimen fails, and the peak stress is not reportable

**The specimen does not carry the applied load.** Three independent lines agree:

**1. Hand method.** `Ash = 2*(e - D/2)*t = 2*(26.8-13.4)*25 = 670 mm^2`
`Ssh = 284,686 / 670 = 425.0 MPa` against **Fsu = 303 MPa**. Shear-out allowable exceeded by 40%.

**2. FE deformation.** 7.655 mm against 0.632 mm at e/D = 1.5 — a **12x increase** for a 1.5x
change in edge distance. That is not a stiffness trend. It is gross section yielding.

**3. Plastic strain.** 0.37211 m/m, i.e. **37%**.

### Why the 750 MPa peak stress is discarded

Predicted plastic strain from the material card, given the reported peak:
`(750.23 - 469) / 760 = 0.370 m/m`
Measured: **0.37211 m/m**. Agreement to **0.6%**.

The solver is following the bilinear card exactly — no contact artefact, no mesh pathology. But
37% plastic strain is several times the elongation of any 7075-T651 product form. The specimen
would fracture long before reaching that state.

Bilinear isotropic hardening carries no failure criterion, so the model hardened straight through
fracture and kept reporting stress. **The 750 MPa figure is the solver extrapolating outside the
validity of its own material model, and is not quoted as a physical result.**

What is reportable from this run: the specimen fails at e/D = 1.0, by shear-out, confirmed
independently by hand method and by the magnitude of the plastic response.

**Generalised check, applied to every run from here:** compute
`required plastic strain = (peak vM - 469) / 760` and compare against material elongation before
quoting any peak stress. This is what the plastic strain probe is for.

---

## 8. Sweep geometry — generated set

`e = (e/D)*D`, `w = 2*(e/D)*D`, head radius `= w/2`, shank held at 160.8 mm.

| e/D | e (mm) | w (mm) | Volume (mm^3) | Mass at 2810 kg/m^3 |
|---|---|---|---|---|
| 1.0 | 26.80 | 53.60 | 229,574.6 | 0.645 kg |
| 1.2 | 32.16 | 64.32 | 285,079.3 | 0.801 kg |
| 1.5 | 40.20 | 80.40 | 372,567.1 | 1.047 kg |
| 1.8 | 48.24 | 96.48 | 465,131.9 | 1.307 kg |
| 2.0 | 53.60 | 107.20 | 529,662.3 | 1.488 kg |

Kernel volumes agree with closed-form to floating-point noise. The e/D = 1.5 rebuild reproduces
the hand-built part's volume identically, validating the generator against a known-good part.
Mass column is the import verification check.

Generator: `cad/build_lug_sweep.py`.

---

## 9. Algebraic property of this sweep — net section and shear-out are not independent

Because the sweep holds `w = 2e`:

`Anet = (w - D)*t = (2e - D)*t`
`Ash  = 2*(e - D/2)*t = (2e - D)*t`

**These are algebraically identical at every e/D.** Net-section and shear-out nominal stresses are
therefore equal throughout the sweep, and only the allowables differ (Ftu 517 vs Fsu 303). Shear-out
governs over net section everywhere, by the ratio 517/303 = 1.71, regardless of geometry.

This is a property of the chosen `w = 2e` parametrisation, not a general lug result, and must be
stated as such in the correlation write-up. It also means the sweep tests **bearing against
shear-out**, not a three-way competition.

Setting shear-out stress equal to Fsu:
`284,686 / ((2e - 26.8) * 25) = 303`  ->  `e = 32.19 mm`  ->  **e/D = 1.201**

**Prediction: failure onset lands essentially exactly on e/D = 1.2.** That run should return a
near-zero margin, with plastic strain intermediate between the e/D = 1.0 and 1.5 cases. Recorded
here before the run so it stands as a falsifiable check on the method rather than a
post-hoc rationalisation.

Nominal bearing stress is `P/(D*t) = 425.0 MPa`, **independent of e/D** — constant across the whole
sweep, since neither D nor t varies.

---

## 10. Open

- [x] Mesh convergence at e/D = 1.5 — singularity ruled out
- [x] e/D = 1.0 run — specimen fails by shear-out
- [ ] e/D = 1.2 run — predicted near-zero margin, see §9
- [ ] e/D = 1.8 run
- [ ] e/D = 2.0 run
- [ ] Margin-vs-e/D comparison against the published curves
- [ ] Confirm the published shear-out and bearing curves cross at e/D = 1.5

**Note on the published-curve comparison.** `HANDOFF.md` §11 records that the source paper's
shear-out and bearing curves cross at e/D = 1.5. Our own nominal stresses cross at e/D = 1.0
(`Ash = Abr` when `2e - D = D`, i.e. `e = D`). A crossing at e/D = 1.5 in *margin* terms would
imply a bearing allowable near 606 MPa rather than Ftu. This is not resolvable without the paper
in hand and **must not be assumed** — it is flagged here as a specific quantity to check against
the source, not as a finding.
