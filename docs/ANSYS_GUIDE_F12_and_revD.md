# Ansys Guide — F12 Lug Correlation Run (and rev D pylon run)

**For:** Ruby, on the TAMU VDI, Ansys Mechanical 2025 R2.
**Goal:** rebuild the Ekvall-class nominal lug, run it, and match the published margin-vs-e/D
curve so you get a predicted-vs-published plot.
**Claim boundary:** educational / representative / portfolio. `SYNTHETIC_TEST_ONLY` for AF-DT-1000;
the lug in this guide is a published-geometry correlation specimen, cited to its authors.

---

## 0. Read this first — one number the paper got wrong

The IAF paper's material table prints **E = 1.03·10⁶ psi**. That is a typo. 7075-T651 aluminum
has **E = 10.3·10⁶ psi ≈ 71 GPa** (1.03e6 psi would be 7.1 GPa, which is not aluminium — it's
about a tenth of the real value). **Enter the correct 71 GPa / 71 000 MPa / 10.3e6 psi.** If you
type the paper's number your deflections come out 10× too big. Everything else in the paper's
table is fine.

**Work in metric (mm, N, MPa) the whole way** — the geometry is given in mm, so this avoids
unit-mixing.

---

## 1. Geometry — build ONE lug, then just change two numbers per run

You are sweeping e/D from 1.0 to 2.0. All dimensions come from the paper's relations:
`e = (e/D)·D`, `w = 2·(e/D)·D`, fixed `D = 26.8 mm`, `t = 25 mm`.

| e/D | hole dia D (mm) | width w (mm) | height to top edge e (mm) |
|---|---|---|---|
| 1.0 | 26.8 | 53.6 | 26.8 |
| 1.2 | 26.8 | 64.3 | 32.2 |
| 1.5 | 26.8 | 80.4 | 40.2 |
| 1.8 | 26.8 | 96.5 | 48.2 |
| 2.0 | 26.8 | 107.2 | 53.6 |

Thickness `t = 25 mm` for every run. Start with **e/D = 1.5** (the bifurcation point — best first
check), then do the others.

### 1a. Make the shape (SpaceClaim / DesignModeler)
1. Open Ansys **Workbench** (desktop icon on the VDI).
2. Left panel "Toolbox" → drag **Static Structural** onto the empty "Project Schematic" canvas on
   the right. A box with rows (Engineering Data, Geometry, Model…) appears.
3. Double-click the **Geometry** row → SpaceClaim opens.
4. Draw the lug as a flat plate, hole in it:
   - **Sketch** tab (top ribbon) → **Rectangle**. Draw a rectangle width `w`, tall enough to hold
     the pin plus the top edge distance plus a straight shank below (make the shank ~2·w long so
     the load end is far from the hole).
   - Round the **top** end into a half-circle of radius `w/2` (that's the classic lug head). Use
     **Pull** → tangent, or sketch a semicircle on top.
   - **Sketch** → **Circle** at the centre of the head, diameter `D = 26.8`. Position its centre so
     the distance from hole-centre to the top edge = `e` from the table.
   - Exit sketch. **Pull** the face to thickness `t = 25 mm` (this makes it 3D).
5. Save. File name like `lug_eD_1p5.scdoc`.

Tip: because only `w` and `e` change between runs, "Save As" a new file and edit those two
dimensions in the sketch — don't rebuild from scratch.

---

## 2. Material — 7075-T651 bilinear

1. Back in Workbench, double-click **Engineering Data** (top row of the Static Structural box).
2. Click into an empty "Click here to add a new material" row, name it `7075-T651`.
3. From the left "Toolbox" drag in these properties and set values (metric):
   - **Isotropic Elasticity**: Young's Modulus **71000 MPa** (the corrected value — NOT 7100),
     Poisson's Ratio **0.33**.
   - **Bilinear Isotropic Hardening**: Yield Strength **469 MPa** (68 000 psi),
     Tangent Modulus — compute from the paper's bilinear curve: it rises from yield (68 ksi at
     strain ≈ 0.0066) to ultimate (75 ksi at strain 0.07). Tangent modulus ≈ (75000−68000) psi /
     (0.07−0.0066) = **110 000 psi ≈ 760 MPa**. Enter **760 MPa**.
4. Note allowables for later hand comparison (not entered in Ansys): Ftu 517 MPa (75 ksi),
   Fty/Fcy 469 MPa (68 ksi), Fsu 303 MPa (44 ksi).
5. Return to Project (tab top-left).

---

## 3. Mesh, pin load, boundary conditions

1. Double-click the **Model** row → Mechanical opens.
2. **Assign material:** click the body in the tree → Details → Material → Assignment → `7075-T651`.
3. **Mesh:**
   - Right-click **Mesh** → Insert → **Sizing**. Pick the hole's inner cylindrical face. Element
     size ~**2 mm** on that face (fine where stress concentrates).
   - Global element size ~**6 mm** (Mesh → Details → Element Size).
   - Right-click **Mesh** → **Generate Mesh**.
   - You will do a convergence check later (Section 5) — for now this is the baseline.
4. **Pin load (bearing) — this is the important part:**
   - The pin pushes on the hole. Simplest valid approach: **Bearing Load** on the hole face.
   - Right-click **Static Structural** → Insert → **Bearing Load**.
   - Scope it to the **hole inner cylindrical face**.
   - Magnitude **284686 N** (= 64 000 lbf), direction **along the shank, pulling the head away
     from the fixed end** (axial). Use the "Direction" selector and pick the shank axis.
   - A Bearing Load automatically puts a cosine pressure on half the hole — correct for a pin.
5. **Fix the far end:**
   - Right-click **Static Structural** → Insert → **Fixed Support**.
   - Scope to the **bottom face of the shank** (the end far from the hole).

---

## 4. Solve and capture plots

1. Right-click **Solution** → Insert → **Equivalent (von-Mises) Stress**.
2. Also insert: **Total Deformation**, and a **Shear Stress** (Solution → Insert → Stress → Shear,
   pick the plane aligned with the ~40° shear-out planes).
3. Right-click **Solution** → **Solve** (or the yellow lightning "Solve" button on the top ribbon).
4. When it finishes, click each result in the tree to view the contour.
5. **Capture for the portfolio** (one screenshot each — right-click plot → Image → Save, or PrtScn):
   - von Mises full lug
   - von Mises zoomed at the hole
   - Total Deformation, **true scale** (set "Auto Scale" → 1.0, NOT exaggerated)
   - Shear stress on the shear-out plane
   - Reaction at the fixed support: click **Solution → Insert → Probe → Force Reaction**, scope to
     the Fixed Support. It should read ≈ 284 686 N. **If it doesn't, the load didn't apply
     right — stop and check before trusting anything.**
6. **Read the failure indicator:** note the peak von Mises and where it is. For each e/D, the
   margin vs the material allowable is what you compare to the paper.

---

## 5. Mesh convergence (do NOT skip — reviewers look for this)

Run the **e/D = 1.5** case **three** times, changing only the hole-face element size:
- coarse ~4 mm, medium ~2 mm, fine ~1 mm.
Record peak stress each time. Plot peak stress vs element count. When the last two points are
within a few %, you've converged — report that number. Two points is not enough; you need three.

---

## 6. Make the correlation plot

For each e/D (1.0, 1.2, 1.5, 1.8, 2.0):
- get your FE-based margin,
- put it next to the paper's published margin (their Figs 9-11).

Plot both series (yours vs published) against e/D on one chart. **If they track, F12 Piece 2 is
done** — that chart is the headline visual of the whole project. Send me the numbers and I'll
build the comparison chart and the write-up, and push them.

Sanity target: the paper's own curves cross at **e/D = 1.5** (shear-out = bearing). If your
shear-out and bearing margins also cross near 1.5, your model is behaving correctly.

---

## 7. While you're in there — the rev D PYLON run (separate model)

Different part, same tool. This closes the F5 FE cross-check.
1. Import the STEP: `AF-DT-1000_fitting_revD.step` (from your Google Drive → VDI).
2. Material: same 7075 elastic is fine (E 71 000 MPa, ν 0.33). ρ 2810 kg/m³.
3. **Verify mass first:** Model → click body → Details → Properties → Mass. Must read **7.65 kg**.
   Wrong mass = wrong STEP imported. Stop if so.
4. **Load — BOTH components on the pin bore** (this is the thing that was wrong before):
   - Force on bore face, **317 840 N along Z** (axial) **and** **529 740 N along X** (transverse),
     or one combined 617 776 N force vector with those components.
   - Confirm the bore scoping covers **both half-cylinder faces** (area ≈ 6.078e-3 m², not
     3.039e-3). A prior run grabbed one face only.
5. Fixed support: the flange underside (the wingbox interface).
6. Solve → capture von Mises (full + at bore), true-scale deformation, bearing stress at bore,
   reaction at the flange (must balance the applied 617 776 N).
7. Send me the peak numbers; I'll compare FE vs the +0.71 hand margin and push the F5/F6 FE doc.

---

## 8. What to send me after the VDI session

Just the numbers (screenshots optional, but grab them for the portfolio):
- Lug: peak stress and margin for each e/D, plus the 3 convergence points.
- Pylon: mass reading, peak von Mises at bore, reaction force.
I turn those into the correlation chart, the FE-vs-hand comparison, and the committed docs.
