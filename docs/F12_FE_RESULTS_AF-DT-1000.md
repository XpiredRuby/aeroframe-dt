# F12 Piece 2 — FE Results Log (Ekvall correlation specimen)

**Status:** IN PROGRESS — first datapoint captured
**Claim boundary:** educational / representative / portfolio only. Non-OEM, non-certified.
All numbers `SYNTHETIC_TEST_ONLY`.

---

## 1. Model definition

**Specimen:** straight lug, published correlation geometry.
Source geometry parameters carried from `HANDOFF.md` §11.

| Quantity | Value |
|---|---|
| Bore diameter D | 26.8 mm |
| Thickness t | 25.0 mm |
| Applied axial load P | 284,686 N (64,000 lbf) |

**STEP bounding box verified before meshing** (parsed from `lug_eD_1p5.step`):

| Axis | Min | Max | Span |
|---|---|---|---|
| X | -40.2 | 40.2 | 80.4 mm (width w) |
| Y | -160.8 | 0.0 | 160.8 mm (length) |
| Z | 0.0 | 25.0 | 25.0 mm (thickness t) |

Long axis = **Y**. Hole end at Y = 0, tail end at Y = -160.8.
This bounding-box check is what fixed the load direction — see §5.

## 2. Material card — 7075-T651

| Property | Value |
|---|---|
| Density | 2810 kg/m^3 |
| Young's modulus E | 71,000 MPa |
| Poisson's ratio | 0.33 |
| Bilinear isotropic hardening — yield | 469 MPa |
| Bilinear isotropic hardening — tangent modulus | 760 MPa |

**Note on E:** the source paper prints 1.03e6 psi = 7.1 GPa. That is a typo — aluminium is
10.3e6 psi = 71 GPa. 71,000 MPa used. Recorded here so the deviation from the printed
source is explicit and auditable.

Hand-check allowables (not used in the FE run): Ftu 517 MPa, Fty/Fcy 469 MPa, Fsu 303 MPa.

## 3. Mesh

| Control | Setting |
|---|---|
| Face Sizing — bore inner cylindrical face | 2 mm |
| Global element size | 6 mm |

Bore face scoping confirmed as **1 Face**, radius 1.34e-2 m — a single continuous
cylindrical face, not a split half-bore. Full wrap confirmed.

## 4. Boundary conditions

**Bearing Load**
- Scoped to bore inner cylindrical face (1 Face)
- Define By: Components, Global Coordinate System
- Fx = 0, **Fy = 284,686 N**, Fz = 0
- Direction: +Y, head pulled away from tail

**Fixed Support**
- Flat end face at Y = -160.8 (farthest from bore)
- Face area 2.01e-3 m^2 = 80.4 x 25 mm — matches the bounding box, confirming the
  correct face was picked

## 5. Method note — direction picking

First attempt used the Direction geometry picker on the bore. That selection returned the
**cylindrical face** (status bar: "1 Cylinder Selected, Radius = 1.34e-002 m"), which supplies a
radial reference, not the axial load direction. Abandoned in favour of explicit Components entry
with the axis confirmed independently from the STEP bounding box.

Same failure class as the axis-mapping bug in `HANDOFF.md` §14: a reference taken from geometry
without declaring what it referenced. Resolution: declare the axis from measured geometry first,
then enter components.

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

**Equilibrium.** Reaction Y magnitude 284,690 N vs applied 284,686 N. Off-axis reactions are
1e-7 N, i.e. numerical zero. Load and support are both correctly scoped, and the load is purely
axial as intended.

**Plasticity consistency.** Peak von Mises 490.45 MPa against a 469 MPa yield. With a tangent
modulus of 760 MPa the material is very nearly perfectly plastic, so the hole-edge concentration
is capped just above yield rather than growing elastically. Peak/yield = 1.046.

**Nominal bearing stress cross-check.**
`Sbr = P / (D * t) = 284,686 / (26.8 * 25) = 425.0 MPa`
Peak von Mises of 490 MPa sits above nominal bearing by a factor of 1.15 — the expected order
for a bore-edge concentration once plasticity has redistributed.

**Nominal net-section stress cross-check.**
`Anet = (w - D) * t = (80.4 - 26.8) * 25 = 1340 mm^2`
`Snet = 284,686 / 1340 = 212.5 MPa` — well below yield, so net section is not the driver here.

**Nominal shear-out cross-check.**
`Ashear = 2 * (e - D/2) * t = 2 * (40.2 - 13.4) * 25 = 1340 mm^2`
`Ssh = 284,686 / 1340 = 212.5 MPa` vs Fsu 303 MPa.

Bearing governs at e/D = 1.5, consistent with expectation for this geometry.

## 8. Open — required before this piece can be called done

- [ ] Mesh convergence at e/D = 1.5: bore-face element size 4 mm / 2 mm / 1 mm.
      Three points minimum (see `HANDOFF.md` §14 — two points misdiagnosed a singularity twice).
- [ ] e/D = 1.0 run
- [ ] e/D = 1.2 run
- [ ] e/D = 1.8 run
- [ ] e/D = 2.0 run
- [ ] Margin-vs-e/D comparison against the published curves
- [ ] Confirm the published shear-out and bearing curves cross at e/D = 1.5

**Caution on the convergence study.** Peak von Mises at a loaded bore edge under a nearly
perfectly plastic material card is a plasticity-limited quantity, not a free elastic peak. It will
converge much flatter than an elastic stress concentration would. Do not read that flatness as
proof of a converged elastic field. Reaction force and total deformation are the better
convergence metrics here and should be tracked alongside peak stress.
