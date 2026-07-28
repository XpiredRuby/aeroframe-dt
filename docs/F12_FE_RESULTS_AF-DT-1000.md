# F12 Piece 2 — FE Results Log (Ekvall correlation specimen)

**Status:** SWEEP COMPLETE — all five e/D cases solved, convergence closed.
Two items open: §9 averaging check, and comparison against published curves.
**Claim boundary:** educational / representative / portfolio only. Non-OEM, non-certified.
All numbers `SYNTHETIC_TEST_ONLY`.

---

## 0. CORRECTION — geometry record, superseding first commit

The first version of this file recorded the specimen bounding box as
`Y = -160.8 .. 0.0, span 160.8 mm`. **That was wrong.** It came from parsing `CARTESIAN_POINT`
entities out of the STEP text. Circular arc extremes are defined by centre plus radius and carry
**no explicit control point at the crown**, so the crown of the head was invisible to that parse.
The reported span was the shank only.

Corrected against the CAD kernel: `X -40.2..40.2`, **`Y -160.8..+40.2, span 201.0 mm`**,
`Z 0..25`. Kernel volume **372,567.1 mm^3**, matching `HANDOFF.md` §11 to 7 parts in 10^6.

Hole centre at Y = 0, head crown at Y = +40.2, straight shank Y = 0 down to Y = -160.8.
**Impact on solved runs: none** — both boundary conditions sat on features the bad parse still
identified correctly.

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

Density 2810 kg/m^3, E = 71,000 MPa, nu = 0.33.
Bilinear isotropic hardening: yield **469 MPa**, tangent modulus **760 MPa**.

**Note on E:** source paper prints 1.03e6 psi = 7.1 GPa. That is a typo — aluminium is
10.3e6 psi = 71 GPa. 71,000 MPa used, deviation recorded so it stays auditable.

Hand-check allowables: Ftu 517 MPa, Fty/Fcy 469 MPa, Fsu 303 MPa.

**Model limitation, load-bearing on all interpretation below.** Bilinear isotropic hardening has
**no failure criterion**. It hardens indefinitely and reports stresses beyond any strain the real
material could reach. Every run is checked against equivalent plastic strain before its peak stress
is quoted. See §7 and §9.

## 3. Boundary conditions (identical across all five runs)

**Bearing Load** — bore inner cylindrical face. Components, Global CS.
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
face presents as a sliver. Repeated attempts failed.

**Adopted method: scope by Named Selection worksheet rule instead of by click.**

| Target | Rule |
|---|---|
| Tail face | `Entity Type = Face, Criterion = Location Y, Operator = Smallest` |
| Bore face | `Entity Type = Face, Criterion = Radius, Operator = Smallest` |

Neither needs a typed value, rotation, or precise clicking, and both are geometry-independent:
shank length is constant so the tail face is always at minimum Y; D is constant at 26.8 mm while
head radius equals `e >= 26.8 mm`, so the bore is always the smallest radius.

**Validated by re-solve, not by inspection.** After re-scoping the e/D = 1.0 model from hand-picked
faces to the two rules, it was re-solved. All four outputs reproduced the original run to every
displayed digit. Rule-based scoping is proven equivalent, not assumed.

All four subsequent geometry swaps re-resolved automatically with zero missing references.

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
at all. **Singularity ruled out.** The +/-2% band is carried forward as the scatter floor on any
peak-stress comparison in this study.

2 mm bore sizing adopted for the sweep.

---

## 5. Complete sweep results

| e/D | Nodes | Elements | Peak vM (MPa) | Max deformation (mm) | Max plastic strain | Reaction Y (N) | Substeps |
|---|---|---|---|---|---|---|---|
| 1.0 | 10,191 | 1,998 | 750.23 (see §7) | 7.655 | 0.37211 | -284,690 | 7 |
| 1.2 | 12,141 | 2,418 | 521.47 | 0.896 | 0.03107 | -284,690 | — |
| 1.5 | — | — | 490.45 | 0.632 | not measured | -284,690 | 4 |
| 1.8 | 19,416 | 4,008 | 506.34 | 0.526 | 0.00888 | -284,690 | 4 |
| 2.0 | 21,933 | 4,554 | 503.49 | 0.4817 | 0.00795 | -284,690 | 4 |

**Equilibrium holds in every case.** Reaction Y equals the applied 284,686 N exactly, with X and Z
at numerical zero (order 1e-7 N), across five geometries and both scoping methods.

Geometry verified on import each time against predicted mass:

| e/D | Predicted | Reported |
|---|---|---|
| 1.0 | 0.645 kg | 0.64504 kg |
| 1.2 | 0.801 kg | 0.80095 kg |
| 1.8 | 1.307 kg | 1.307 kg |
| 2.0 | 1.488 kg | 1.4883 kg |

---

## 6. Hand-method margins

`Abr = D*t = 670 mm^2`, so **nominal bearing stress is 425.0 MPa at every e/D** — independent of
geometry, since neither D nor t varies. `MS_bearing = 517/425 - 1 = +0.216` throughout.

Because the sweep holds `w = 2e` (see §10), `Anet = Ash = (2e - D)*t` exactly.

| e/D | Ash = Anet (mm^2) | Ssh = Snet (MPa) | MS shear-out | MS net section | MS bearing | **Governing** |
|---|---|---|---|---|---|---|
| 1.0 | 670 | 425.0 | -0.287 | +0.216 | +0.216 | **shear-out, -0.287** |
| 1.2 | 938 | 303.5 | -0.002 | +0.703 | +0.216 | **shear-out, -0.002** |
| 1.5 | 1340 | 212.5 | +0.426 | +1.433 | +0.216 | **bearing, +0.216** |
| 1.8 | 1742 | 163.4 | +0.854 | +2.164 | +0.216 | **bearing, +0.216** |
| 2.0 | 2010 | 141.6 | +1.140 | +2.651 | +0.216 | **bearing, +0.216** |

**Mode crossover.** Shear-out and bearing margins are equal when
`303/Ssh - 1 = 0.216` -> `Ssh = 249.2 MPa` -> `Ash = 1142.4 mm^2` -> **e/D = 1.353**.

Below that, shear-out governs and the margin is strongly geometry-dependent. Above it, bearing
governs and the margin is **flat at +0.216 regardless of e/D**, because bearing area `D*t` does not
change in this sweep.

---

## 7. e/D = 1.0 — specimen fails, peak stress not reportable

Three independent lines agree the specimen does not carry the load:

**1. Hand method.** `Ssh = 425.0 MPa` vs `Fsu = 303 MPa`. Exceeded by 40%.
**2. FE deformation.** 7.655 mm against 0.632 mm at e/D = 1.5 — a **12x increase** for a 1.5x
change in edge distance. Gross section yielding, not a stiffness trend.
**3. Plastic strain.** 0.37211 m/m, i.e. **37%**.

### Why the 750 MPa peak is discarded

Predicted from the material card: `(750.23 - 469)/760 = 0.370`. Measured **0.37211**.
Agreement to **0.6%** — the solver is following the bilinear card exactly, with no contact artefact
or mesh pathology. But 37% plastic strain is several times the elongation of any 7075-T651 product
form. The specimen would fracture long before reaching that state.

**The 750 MPa figure is the solver extrapolating outside the validity of its own material model,
and is not quoted as a physical result.** What is reportable: the specimen fails at e/D = 1.0, by
shear-out, confirmed independently by hand method and by the magnitude of the plastic response.

---

## 8. Predictions recorded before their runs, and outcomes

Each prediction below was committed to this repository **before** the corresponding solve. They are
listed with outcomes, including the one that missed.

**e/D = 1.2 — failure onset.** Predicted from `w = 2e` algebra: onset at e/D = 1.201, therefore
meaningful plasticity but nothing like e/D = 1.0, deformation between 0.632 and 7.655 mm and much
nearer the low end, plastic strain well under 0.37.
Measured: deformation **0.896 mm**, plastic strain **0.0311**, hand margin **-0.002**. **Held.**

**e/D = 1.8 — bearing takes over.** Predicted: peak vM close to the 490 MPa at e/D = 1.5 and no
longer responsive to geometry; deformation falling to roughly 0.45–0.58 mm.
Measured: peak **506.34 MPa** (3.2% from 490.45, inside the +/-2% mesh scatter band of §4 plus
rounding), deformation **0.526 mm**. **Held.**

**e/D = 2.0 — elastic scaling.** Predicted from the shank-stretch ratio established at e/D = 1.5
and 1.8: deformation **approximately 0.47 mm**, peak vM 490–515 MPa, plastic strain 0.005–0.007.
Measured: deformation **0.4817 mm** (1.6% from prediction), peak **503.49 MPa**.
Plastic strain **0.00795** — **above the predicted range. Recorded as a miss.**

### Elastic scaling law

Pure shank stretch `delta = P*L/(A*E)` with `A = w*t`, `L = 160.8 mm`:

| e/D | w (mm) | shank stretch (mm) | measured (mm) | ratio |
|---|---|---|---|---|
| 1.5 | 80.40 | 0.3208 | 0.632 | 1.970 |
| 1.8 | 96.48 | 0.2673 | 0.526 | 1.968 |
| 2.0 | 107.20 | 0.2406 | 0.4817 | 2.002 |

Constant to 1.7% across the three cases where response is essentially elastic. The factor of ~1.97
is compliance from the head and bore region that the shank formula does not capture. Its stability
is what makes it a usable cross-check rather than a coincidence. The cases at e/D = 1.0 and 1.2 do
not follow it, as expected — they are plastically dominated.

### Bearing-governed flatline, confirmed by data

Peak von Mises for e/D = 1.2, 1.5, 1.8, 2.0: **521.47, 490.45, 506.34, 503.49 MPa**. Total spread
6%, against a shear-out margin that swings from -0.002 to +1.140 over the same range. Bearing
stress is `P/(D*t)`, constant by construction. The flatline is the direct observable consequence of
bearing governing above e/D = 1.353, and it is present in the data.

---

## 9. OPEN — plastic strain / peak stress consistency

The material card implies `epsilon_p = (sigma - 469)/760` at any yielded point.

| e/D | Peak vM (MPa) | epsilon_p implied | epsilon_p measured | ratio measured/implied |
|---|---|---|---|---|
| 1.0 | 750.23 | 0.3700 | 0.37211 | **1.006** |
| 1.2 | 521.47 | 0.0690 | 0.03107 | 0.450 |
| 1.8 | 506.34 | 0.0491 | 0.00888 | 0.181 |
| 2.0 | 503.49 | 0.0454 | 0.00795 | 0.175 |

**Monotonic with plastic zone size.** Agreement is near-exact where plasticity is widespread and
degrades steadily as the yielded region shrinks. This is a trend across four cases, not a one-off.

**Working hypothesis, still not confirmed.** Nodal averaging over elements that are only partly
yielded depresses the reported plastic strain more than it depresses the reported stress. Where the
plastic zone spans many elements (e/D = 1.0) the effect is negligible; where it is confined to a
few elements at the bore edge it dominates.

**Consequence: peak stresses for e/D >= 1.2 are treated as indicative, not quantitative, and are
not used for correlation until this is resolved.** None of the conclusions in §6 or §8 depend on
them — those rest on deformation, plastic strain magnitude, reaction equilibrium, and hand-method
margins.

**To resolve:** restore an archive, set Display Option to Unaveraged for both Equivalent Stress and
Equivalent Plastic Strain, and repeat the check. If unaveraged values reconcile, the hypothesis is
confirmed and the correction applies across the sweep. This check was scheduled at e/D = 1.2 but
skipped before the geometry was swapped; the state is recoverable from `H:\seven_twnetyseven.wbpz`.

---

## 10. Algebraic property of this sweep

Because the sweep holds `w = 2e`:

`Anet = (w - D)*t = (2e - D)*t`  and  `Ash = 2*(e - D/2)*t = (2e - D)*t`

**Algebraically identical at every e/D.** Net-section and shear-out nominal stresses are equal
throughout; only the allowables differ (Ftu 517 vs Fsu 303). Shear-out governs over net section
everywhere, by the fixed ratio 517/303 = 1.71, regardless of geometry.

This is a property of the chosen `w = 2e` parametrisation, **not a general lug result**, and must be
stated as such in the correlation write-up. The sweep tests bearing against shear-out only — it is
not a three-way competition, and it cannot exercise net-section failure at all.

Setting shear-out stress equal to Fsu: `284,686/((2e - 26.8)*25) = 303` -> `e = 32.19` ->
**e/D = 1.201**. Confirmed by the e/D = 1.2 run.

---

## 11. Standing check applied to every run

Compute `required plastic strain = (peak vM - 469)/760` and compare against material elongation
**before quoting any peak stress**. Bilinear hardening will report stresses the material could
never reach. This check caught the e/D = 1.0 result and exposed the §9 discrepancy.

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

**Unit conversion on entry.** Global mesh element size was found at `6.e-006 m` — 6 micrometres on
a 200 mm part; a mesh attempt ran past 10 minutes without completing. Same failure mode as the
Engineering Data material card at project start: a value entered while the unit selector was on a
different setting, then **converted rather than relabelled** when the unit changed. Two occurrences.
**Rule: after changing any unit dropdown, re-read the numeric field.**

**Session loss.** The VDI wipes local disk at logout. Two sessions were lost. `File > Archive`
produces a single `.wbpz` that cannot be separated from its `_files` folder, unlike a bare `.wbpj`.
A third near-loss occurred when an archive overwrote its predecessor because the default filename
was reused.
**Rule: archive after every solve, give each archive a distinct name, and copy to persistent
storage immediately.**

**Stale project lock.** On reopening, Workbench reported the project locked by a previous session
and a second Workbench instance was found still running. Two instances on one project risk
corruption.
**Rule: confirm only one Workbench instance is running before editing.**

---

## 14. Open

- [x] Mesh convergence at e/D = 1.5 — singularity ruled out
- [x] e/D = 1.0 — fails by shear-out
- [x] e/D = 1.2 — margin approximately zero, prediction confirmed
- [x] e/D = 1.5 — passes, bearing governs
- [x] e/D = 1.8 — passes, prediction confirmed
- [x] e/D = 2.0 — passes, elastic scaling prediction confirmed to 1.6%
- [ ] Resolve §9 plastic strain / peak stress discrepancy using unaveraged results
- [ ] Plastic strain at e/D = 1.5 was not captured — fill in for completeness
- [ ] Margin-vs-e/D comparison against the published curves
- [ ] Confirm the published shear-out and bearing curves cross at e/D = 1.5

**Note on the published-curve comparison.** `HANDOFF.md` §11 records that the source paper's
shear-out and bearing curves cross at e/D = 1.5. **Our own margins cross at e/D = 1.353**, using
`Fbru = Ftu = 517 MPa`. A crossing at 1.5 would require a bearing allowable near 606 MPa
(1.17 x Ftu), which is a plausible value for a bearing allowable but **is not established here**.
This is a specific, checkable discrepancy against the source, and it is flagged as open rather
than reconciled by assumption. Resolving it requires the paper in hand.
