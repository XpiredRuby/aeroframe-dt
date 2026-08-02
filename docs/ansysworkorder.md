# Ansys Work Order — one session, three jobs

Everything outstanding on AeroFrame-DT that needs a solver. Do the sessions **in this order**.
Session A must come first: the digital thread shows it invalidates 17 downstream artifacts, so
anything finalised before it would have to be redone.

**Budget:** A ≈ 45 min, B ≈ 45 min, C ≈ 50 min.

**Before you start — one thing to look up.** Open MIL-HDBK-5J Table 3.7.6.0(b3), the 7075-T7351
plate page, band 2.001–2.500 in. **Read the elongation column, `e`, for the L direction.** You need
it in Session A step 5. Write it down as a percentage.

**Names to type are all lowercase letters and digits, no capitals and no underscores.**

---

# SESSION A — Elastic-plastic contact

**What it settles.** F7 measured `t_eff/t = 0.681` on a fully elastic model. Real 7075 yields at the
contact edge, which spreads the load and raises `t_eff`. This run replaces a lower bound with a
measurement, and the number decides an open question:

| Result | Meaning | Worst-case margin |
|---|---|---|
| `t_eff/t` **above 0.840** | the thick-lug correction and the Ekvall scatter band are measuring the same physics — they double-count | **+0.078** |
| `t_eff/t` **below 0.840** | they are independent effects and both apply | **−0.094** |

You run the model **twice**: real pin, then stiff pin. The ratio of the two peak pressures is the
answer. Only the pin's Young's modulus changes between them.

## A1 — Restore the model

1. Open **Workbench 2025 R2**.
2. `File` → `Restore Archive…`
3. Pick `f7converged.wbpz`.
4. When it asks where to save, make a new folder and name the project **`f7plastic`**.
5. It opens the restored project. `File` → `Save`.

## A2 — Add plasticity to the lug

6. In the Project Schematic, double-click **`Engineering Data`**.
7. Click the **7075-T7351** row to select it.
8. In the **Toolbox** panel on the left, expand **`Plasticity`**.
9. Drag **`Bilinear Isotropic Hardening`** onto the properties table on the right.
10. Fill in the two boxes that appear:

    - **Yield Strength = `358.5` MPa** — this is A-basis `Fty` (L) = 52 ksi, from
      `docs/MARGIN_SUMMARY.md` §3.
    - **Tangent Modulus** — pick from the elongation you looked up:

      | Elongation from the handbook | Tangent Modulus to enter |
      |---|---|
      | 5% | `1993` MPa |
      | 6% | `1631` MPa |
      | 7% | `1380` MPa |

      **Write down which one you used.** It is an assumption and it goes in the write-up.

11. Click **`Return to Project`**. Save.

## A3 — Solve the real pin

12. Double-click **`Model`** (or `Setup`) to open Mechanical.
13. **Do not touch the mesh.** It should be the converged 0.75 mm bore sizing, about 203,000 nodes.
    Confirm that number in the `Mesh` → `Statistics` panel before going on.
14. Click **`Analysis Settings`** in the tree. Set:

    - `Large Deflection` = **On**
    - `Auto Time Stepping` = **On**
    - `Initial Substeps` = **10**
    - `Minimum Substeps` = **5**
    - `Maximum Substeps` = **100**

15. Confirm the pin material is still at **E = 200,000 MPa** (the real 4340 steel value). This is
    the real-pin run.
16. Click **`Solve`**. Expect **15–25 minutes**.

### What to record from the real-pin run

17. Click the existing **Contact Pressure** result. **Record the Maximum.** Call it
    **`p real`**.
18. Right-click `Solution` → `Insert` → `Strain` → **`Equivalent Plastic Strain`**. Scope it to the
    **lug body only**. Right-click → `Evaluate All Results`. **Record the Maximum.**

    **This is your proof the run did anything.** If plastic strain is essentially zero, the material
    never yielded, and `t_eff/t` will come back at 0.681 — which is a valid result, but say so
    explicitly rather than reporting it as a plastic run.

19. Right-click `Solution` → `Insert` → `Probe` → **`Force Reaction`**, scope it to the **contact
    region**. **Record all three components.** They should sum to the applied
    `Fx = 529,740 N`, `Fz = 317,840 N`. This is the contact-resultant check REQ-009 also asks for,
    and you get it free here.

20. Save.

## A4 — Solve the stiff pin

21. Back in the Project Schematic, **right-click the analysis system** → **`Duplicate`**.
22. In the duplicate, open `Engineering Data` and change **only the pin material's Young's Modulus**
    to **`4e6` MPa** (4,000 GPa, 20× steel). Leave the lug plasticity exactly as it is.
23. `Return to Project`, open the duplicate's Mechanical, **`Solve`**.
24. **Record the Contact Pressure Maximum.** Call it **`p stiff`**.
25. Save. `File` → `Archive…` → name it **`f7plastic`**.

## A5 — The answer

    t eff / t  =  p stiff  /  p real

**Send me those two pressures and I will do the rest.** Also send: the tangent modulus you used, the
max plastic strain, and the contact force components.

### If it will not converge

Plasticity plus frictional contact can fail to converge. In order, try:

- `Analysis Settings` → `Maximum Substeps` = **500**
- Contact region → `Normal Stiffness` = **Manual**, `Factor` = **0.1**
- Last resort: change the bore mesh sizing from 0.75 mm to **1.5 mm** and run both pins at that
  size. The ratio still works because both runs share the mesh — **just tell me you did it**, so the
  write-up says so.

---

# SESSION B — REQ-009 FE benchmarks

**Not in Workbench.** These run in **Mechanical APDL**, which is faster and gives text output you
can read straight off the screen. Three ready-made input files are in the repo.

## B1 — Get the files

1. In the VDI, open Chrome and go to **`github.com/XpiredRuby/aeroframe-dt`**, folder
   **`benchmarks`**.
2. Download these four files into a working folder (click the file, then the **Download raw file**
   button):

   - `patch.inp`
   - `cant.inp`
   - `cantsolid.inp`
   - `plate.inp`

## B2 — Start Mechanical APDL

3. Start menu → **Ansys 2025 R2** → **Mechanical APDL Product Launcher**.
4. Set **Working Directory** to the folder with the `.inp` files.
5. Set **Job Name** to **`bench`**.
6. Click **Run**.

## B3 — B-001, the patch test

7. In Mechanical APDL: `File` → **`Read Input from…`** → pick **`patch.inp`**.
8. It solves in a few seconds. Read the output window and record:

   - **max absolute displacement error** — must be **1e-10 m or smaller**
   - **element strains** from the printed table — must be `epsx = 1e-3`, `epsy = 5e-4`,
     `gamxy = -1e-4` for **every** element
   - **FSUM reactions** — FX and FY must be zero to machine precision

   This is a pass/fail test with no tolerance to argue about. Distorted elements that reproduce a
   linear field exactly are the whole point.

## B4 — B-002, the cantilever

9. `File` → `Read Input from…` → **`cant.inp`**.
10. Record tip **UY** and **ROTZ**. Expect **−1.142857e-3 m** and **−1.714286e-3 rad**.
    Acceptance is **0.5%**.

    **If UY comes out near −4.571e-3** the section is rotated 90°. Open `cant.inp` in Notepad,
    change `secdata,0.05,0.10` to `secdata,0.10,0.05`, save, and read it in again.

11. Record the root bending stress from the printed table. Expect **12.0 MPa**.
12. Now the continuum companion. `File` → `Read Input from…` → **`cantsolid.inp`**.
13. Record the tip UY. Then open `cantsolid.inp` in Notepad, change the line **`es=0.025`** to
    **`es=0.0125`**, save, and read it in again. Then once more at **`es=0.00625`**.
14. **Record all three tip deflections.** Acceptance is 2% against beam theory plus a visible
    convergence trend.

## B5 — B-003, the plate

15. `File` → `Read Input from…` → **`plate.inp`**.
16. Record the centre UZ. Oracle is **6.33727e-4 m**. Acceptance is **2%**.
17. Edit `es=0.025` to **`es=0.05`**, run again. Then **`es=0.0125`**, run again.
18. **Record all three centre deflections and the centre moments.**

## B6 — Save

19. `File` → `Save as Jobname.db`.
20. Keep the output text. Easiest: `File` → `Save Output to…`, or just screenshot the numbers.

**Send me every number above.** If any script throws an error, **send me the exact error text** —
these are text files in the repo, so a fix is one commit.

---

# SESSION C — REQ-014 modal and buckling

## C1 — Open the Rev D linear model

1. In Workbench, open the **F5 Rev D linear elastic project** (the linear static structural on the
   Rev D geometry — *not* the F7 contact model).
2. `File` → `Save As…` → **`modalbuckling`**.

**Why the linear model:** eigenvalue buckling has to sit on a linear static solution. The F7 contact
model is nonlinear and cannot feed it.

## C2 — Modal, 6 modes

3. From the Toolbox, drag a **`Modal`** system and drop it **onto the `Model` cell** of the existing
   Static Structural. This shares the geometry, material and mesh — do not build a new one.
4. Open Mechanical. Under the new **Modal** branch, click **`Analysis Settings`** and set
   **`Max Modes to Find` = 6**.
5. Apply a **`Fixed Support`** to the **flange underside face** — the same face F5 uses, area
   6.1688e-2 m².
6. **`Solve`**. Expect 10–20 minutes.
7. **Record all 6 frequencies in Hz.**
8. Click each mode and **note what it is doing** — blade bending, blade torsion, lug head, and which
   direction. One line each is enough.

**What to compare against.** `docs/F10_DYNAMICS_BUCKLING.md` predicts a first mode near **2133 Hz**
from a cantilever idealisation, and states explicitly that the real first mode should come out
**lower**, because the idealisation ignores the lug head mass at the tip and the flange's finite
compliance. **If the FE first mode is below 2133 Hz, the prediction was right.** If it is above,
that is the more interesting result and we write up why.

## C3 — Eigenvalue buckling, 3 modes

9. Back in the Project Schematic, drag an **`Eigenvalue Buckling`** system onto the **`Solution`
   cell** of the Static Structural.
10. Confirm the Static Structural still carries the F5 load — **`Fx = 529,740 N`,
    `Fz = 317,840 N`** on the bore — and the fixed support on the flange.
11. In Mechanical, under **Eigenvalue Buckling** → `Analysis Settings`, set
    **`Max Modes to Find` = 3**.
12. **`Solve`**.
13. **Record the three Load Multipliers.**

    `MS_buckling = Load Multiplier − 1`

    Analytical Euler gives **+43.4**. Anything in the tens confirms it. Buckling is not going to
    become critical at `L/r = 6.9`; this run exists to close the requirement honestly, not because
    the answer is in doubt.

## C4 — Save

14. `File` → `Archive…` → name it **`modalbuckling`**.

---

# What to send me

One message with all of it:

**Session A** — `p real`, `p stiff`, tangent modulus used, max plastic strain, contact force
components, and whether you had to drop to the 1.5 mm mesh.

**Session B** — patch max error and strain table, cantilever UY / ROTZ / root stress, three solid
tip deflections, three plate centre deflections and moments.

**Session C** — six modal frequencies with a one-line mode description each, three buckling load
multipliers.

Then I write F16 (elastic-plastic), the FE verification report (REQ-009), and the F10 FE closure
(REQ-014), update the margin summary and the verification matrix, and rebuild the digital thread so
the 17 stale artifacts come back current.

**That closes 17 of 18 requirements** — the ceiling, since REQ-012 has no S-N data behind it and
cannot close honestly.
