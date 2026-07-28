# F12 Piece 2 — FE Results Log (Ekvall correlation specimen)

**Status:** IN PROGRESS — e/D = 1.0, 1.2 and 1.5 solved; convergence closed
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

Kernel volume **372,567.1 mm^3**, matching `HANDOFF.md` §11 to 7 parts in 10^6.

**Corrected layout:** hole centre at Y = 0, head crown at Y = +40.2, straight shank Y = 0 down to
Y = -160.8. **Impact on solved runs: none** — both boundary conditions sat on features the bad
parse still identified correctly.

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

**Model limitation, load-bearing on all interpretation below.** Bilinear isotropic hardening has
**no failure criterion**. It hardens indefinitely and reports stresses beyond any strain the real
material could reach. Every run is therefore checked against equivalent plastic strain before its
peak stress is quoted. See §7 and §11.

## 3. Boundary conditions (identical across all runs)

**Bearing Load** — bore inner cylindrical face. Define By Components, Global CS.
`Fx = 0, Fy = 284,686 N, Fz = 0`.
**Fixed Support** — flat tail end face at minimum Y.
**Mesh** — 6 mm global, 2 mm bore face sizing.

### Method note 1 — direction picking

The Direction geometry picker on the bore returns the **cylindrical face** ("1 Cylinder Selected,
Radius = 1.34e-002 m"), a radial reference, not an axial direction. Abandoned for explicit
Components entry with the load axis confirmed from measured geometry.

### Method note 2 — rule-based scoping, adopted after manual picking failed

Replacing geometry invalidates every scoped selection. Ansys keeps displaying the stale
attachment, so Details can read "1 Face" when nothing is attached. **Tells:** magenta "Old Geometry
Tessellation" overlay, and Number of Matched Entities = 0 in the scoping worksheet.

Manual re-picking of the tail face proved impractical on a streamed desktop — no drag available,
and the face presents as a sliver at most orientations. Repeated attempts failed.

**Adopted method: scope by Named Selection worksheet rule instead of by click.**

| Target | Rule |
|---|---|
| Tail face | `Entity Type = Face, Criterion = Location Y, Operator = Smallest` |
| Bore face | `Entity Type = Face, Criterion = Radius, Operator = Smallest` |

Both need no typed value, no rotation and no precise clicking, and both are geometry-independent
across the sweep: shank length is held constant so the tail face is always at minimum Y, and D is
held constant at 26.8 mm while the head radius equals `e >= 26.8 mm`, so the bore is always the
smallest radius.

**Validated by re-solve, not by inspection.** After re-scoping the e/D = 1.0 model from
hand-picked faces to the two rules, it was re-solved. All four outputs reproduced the original run
to every displayed digit (750.23 MPa, 7.655 mm, 0.37211, -284,690 N). Rule-based scoping is
therefore proven equivalent, not merely assumed to be.

Subsequent geometry swaps re-resolved automatically with no missing references.

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
at all. **Singularity ruled out.**

2 mm bore sizing adopted for the sweep.

---

## 5. Results summary — three cases solved

| e/D | Nodes | Peak vM (MPa) | Max deformation (mm) | Max plastic strain | Reaction Y (N) |
|---|---|---|---|---|---|
| 1.0 | 10,191 | 750.23 | 7.655 | 0.37211 | -284,690 |
| 1.2 | 12,141 | 521.47 | 0.896 | 0.03107 | -284,690 |
| 1.5 | — | 490.45 | 0.632 | not measured | -284,690 |

Reaction Y equals the applied load in every case, with X and Z at numerical zero (order 1e-7 N).
Equilibrium holds across all geometries and both scoping methods.

Geometry verified on import each time against the predicted mass:

| e/D | Predicted mass | Reported mass |
|---|---|---|
| 1.0 | 0.645 kg | 0.64504 kg |
| 1.2 | 0.801 kg | 0.80095 kg |

---

## 6. Hand-method margins

`Abr = D*t = 670 mm^2`, so **nominal bearing stress is 425.0 MPa at every e/D** — independent of
geometry, since neither D nor t varies.

| e/D | e (mm) | Ash = Anet (mm^2) | Ssh = Snet (MPa) | Ssh / Fsu | MS shear-out |
|---|---|---|---|---|---|
| 1.0 | 26.80 | 670 | 425.0 | 1.403 | **-0.287** |
| 1.2 | 32.16 | 938 | 303.5 | 1.002 | **-0.002** |
| 1.5 | 40.20 | 1340 | 212.5 | 0.701 | **+0.426** |

---

## 7. e/D = 1.0 — specimen fails, peak stress not reportable

Three independent lines agree the specimen does not carry the load:

**1. Hand method.** `Ssh = 425.0 MPa` vs `Fsu = 303 MPa`. Exceeded by 40%.

**2. FE deformation.** 7.655 mm against 0.632 mm at e/D = 1.5 — a **12x increase** for a 1.5x
change in edge distance. Gross section yielding, not a stiffness trend.

**3. Plastic strain.** 0.37211 m/m, i.e. **37%**.

### Why the 750 MPa peak is discarded

Predicted from the material card: `(750.23 - 469) / 760 = 0.370 m/m`.
Measured: **0.37211**. Agreement to **0.6%**.

The solver is following the bilinear card exactly — no contact artefact, no mesh pathology. But
37% plastic strain is several times the elongation of any 7075-T651 product form. The specimen
would fracture long before reaching that state.

**The 750 MPa figure is the solver extrapolating outside the validity of its own material model,
and is not quoted as a physical result.** What is reportable: the specimen fails at e/D = 1.0,
by shear-out, confirmed independently by hand method and by the magnitude of the plastic response.

---

## 8. e/D = 1.2 — prediction tested and held

**The prediction was recorded before this run was made.** From the `w = 2e` algebra in §10, setting
shear-out stress equal to Fsu gives failure onset at `e/D = 1.201`. The stated expectation was:
meaningful plasticity but nothing like e/D = 1.0, deformation between 0.632 and 7.655 mm and much
nearer the low end, plastic strain well under 0.37.

| Quantity | Predicted | Measured |
|---|---|---|
| Deformation | 0.632–7.655 mm, near low end | **0.896 mm** |
| Plastic strain | well under 0.37 | **0.0311** |
| Shear-out margin | approximately zero | **-0.002** |

Held. Deformation is only 1.4x the fully-elastic e/D = 1.5 case, and plastic strain of 3.1% is
localised yielding rather than collapse. This is what incipient failure should look like at a
stress-based allowable, and it lands where the algebra placed it.

---

## 9. OPEN DISCREPANCY — plastic strain / peak stress consistency at e/D = 1.2

The material card implies `epsilon_p = (sigma - 469) / 760` at any yielded point.

| e/D | Peak vM | epsilon_p implied | epsilon_p measured | Agreement |
|---|---|---|---|---|
| 1.0 | 750.23 MPa | 0.3700 | 0.37211 | 0.6% |
| 1.2 | 521.47 MPa | 0.0690 | 0.03107 | **factor 2.2 low** |

**The e/D = 1.2 pair does not reconcile.** Working backwards from the measured plastic strain gives
`469 + 760*0.03107 = 492.6 MPa`, not the reported 521.47 MPa.

**Working hypothesis, not a finding.** At e/D = 1.0 the plastic zone is large and well resolved, so
nodal averaging has little effect relative to the magnitude. At e/D = 1.2 the plastic zone is
confined to a few elements at the bore edge, and averaging against still-elastic neighbours may
depress the nodal plastic strain more than it depresses the nodal stress.

**Consequence: the 521.47 MPa peak at e/D = 1.2 is less trustworthy than the e/D = 1.0 peak and is
not used quantitatively until this is resolved.** The conclusions of §8 do not depend on it — they
rest on deformation, on the plastic strain magnitude, and on the hand-method margin, all three of
which are consistent with each other.

**To resolve:** re-read both fields as unaveraged (element-nodal) results at e/D = 1.2 and repeat
the consistency check. If unaveraged values reconcile, the averaging hypothesis is confirmed and
the same check should be re-run on every case in the sweep.

---

## 10. Algebraic property of this sweep — net section and shear-out are not independent

Because the sweep holds `w = 2e`:

`Anet = (w - D)*t = (2e - D)*t`
`Ash  = 2*(e - D/2)*t = (2e - D)*t`

**Algebraically identical at every e/D.** Net-section and shear-out nominal stresses are equal
throughout, and only the allowables differ (Ftu 517 vs Fsu 303). Shear-out governs over net section
everywhere, by the ratio 517/303 = 1.71, regardless of geometry.

This is a property of the chosen `w = 2e` parametrisation, **not a general lug result**, and must be
stated as such in the correlation write-up. The sweep tests bearing against shear-out, not a
three-way competition.

Setting shear-out stress equal to Fsu:
`284,686 / ((2e - 26.8) * 25) = 303` -> `e = 32.19 mm` -> **e/D = 1.201**

Confirmed by the e/D = 1.2 run, §8.

---

## 11. Standing check applied to every run

Compute `required plastic strain = (peak vM - 469) / 760` and compare against material elongation
**before quoting any peak stress**. Bilinear hardening will report stresses the material could
never reach. This check is what caught the e/D = 1.0 result and what exposed the e/D = 1.2
discrepancy in §9.

---

## 12. Sweep geometry — generated set

`e = (e/D)*D`, `w = 2*(e/D)*D`, head radius `= w/2`, shank held at 160.8 mm.

| e/D | e (mm) | w (mm) | Volume (mm^3) | Mass at 2810 kg/m^3 |
|---|---|---|---|---|
| 1.0 | 26.80 | 53.60 | 229,574.6 | 0.645 kg |
| 1.2 | 32.16 | 64.32 | 285,079.3 | 0.801 kg |
| 1.5 | 40.20 | 80.40 | 372,567.1 | 1.047 kg |
| 1.8 | 48.24 | 96.48 | 465,131.9 | 1.307 kg |
| 2.0 | 53.60 | 107.20 | 529,662.3 | 1.488 kg |

Kernel volumes agree with closed-form to floating-point noise. The e/D = 1.5 rebuild reproduces the
hand-built part's volume identically, validating the generator against a known-good part.

Generator: `cad/build_lug_sweep.py`.

---

## 13. Session-management faults encountered

Recorded because they cost real time and are avoidable.

**Unit conversion on entry.** Global mesh element size was found at `6.e-006 m` — 6 micrometres on
a 200 mm part. A mesh attempt ran past 10 minutes without completing. Same failure mode as the
Engineering Data material card at project start: a value entered while the unit selector was on a
different setting, then **converted rather than relabelled** when the unit changed. Two occurrences.
**Rule: after changing any unit dropdown, re-read the numeric field.**

**Session loss.** The VDI wipes local disk at logout. A project was lost once, and a second session
was lost after that. `File > Archive` produces a single `.wbpz` that cannot be separated from its
`_files` folder, unlike a bare `.wbpj`.
**Rule: archive after every solve and copy the .wbpz to persistent storage immediately.**

**Stale project lock.** On reopening, Workbench reported the project locked by a previous session
and a second Workbench instance was found still running. Two instances on one project risk
corruption.
**Rule: confirm only one Workbench instance is running before editing.**

---

## 14. Open

- [x] Mesh convergence at e/D = 1.5 — singularity ruled out
- [x] e/D = 1.0 run — fails by shear-out
- [x] e/D = 1.2 run — margin approximately zero, prediction confirmed
- [ ] e/D = 1.8 run
- [ ] e/D = 2.0 run
- [ ] Resolve the §9 plastic strain / peak stress discrepancy using unaveraged results
- [ ] Margin-vs-e/D comparison against the published curves
- [ ] Confirm the published shear-out and bearing curves cross at e/D = 1.5

**Note on the published-curve comparison.** `HANDOFF.md` §11 records that the source paper's
shear-out and bearing curves cross at e/D = 1.5. Our own nominal stresses cross at e/D = 1.0
(`Ash = Abr` when `2e - D = D`). A crossing at e/D = 1.5 in *margin* terms would imply a bearing
allowable near 606 MPa rather than Ftu. Not resolvable without the paper in hand and
**must not be assumed** — flagged as a quantity to check against the source, not as a finding.
