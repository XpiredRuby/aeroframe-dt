# AeroFrame-DT
## Transport-Aircraft Structural Substantiation, Manufacturing, Quality, and Digital Thread

**Full-depth ceiling:** 96/100  
**Estimated effort:** 550–850 focused hours  
**No-purchase path:** Existing MD-11 CAD, SolidWorks, ANSYS, Altair, public joint/structural test data, NIST PMI/QIF benchmarks  
**Primary roles:** Structures, stress, mechanical design, loads, fatigue, manufacturing support, quality, liaison, test

---

## 1. Engineering mission

Substantiate one representative transport-aircraft pylon attachment, lug, or load-critical fitting from load definition through:

- classical sizing;
- CAD and GD&T;
- nonlinear joint FEA;
- fatigue and damage-tolerance screening;
- modal and vibration response;
- design optimization;
- manufacturing/inspection planning;
- public-data correlation;
- nonconformance and root-cause disposition;
- revision-aware digital evidence.

A full aircraft CAD model provides context; the engineering decision remains focused on one critical assembly.

---

## 2. No-purchase validation strategy

Primary validation shall use:
- classical mechanics;
- two independent FE formulations or solvers;
- public lug, fastener, bearing-bypass, joint, or coupon test datasets;
- NASA/FAA/AGARD/NIST benchmark data;
- NIST AP242 and QIF PMI benchmarks;
- campus test or inspection facilities only if free and available.

No personal purchase of metal, fasteners, strain gauges, or test equipment is required.

---

## 3. Step-by-step execution

### Phase F0 — Part selection and scope
1. Select one load-critical fitting.
2. Define representative geometry and aircraft context.
3. Define interfaces and load path.
4. Define exclusions and non-proprietary assumptions.
5. Define certification-inspired but non-certified claim language.
6. Create assumptions register.

**Exit:** The project is narrow enough for deep substantiation.

### Phase F1 — Requirements and loads
1. Define limit and ultimate loads.
2. Draw free-body diagrams.
3. Define axial, shear, bending, torsion, and combined cases.
4. Define pressure, inertia, thermal, and dynamic contributions where relevant.
5. Define mass, stiffness, envelope, fatigue, and inspection requirements.
6. Define material and fastener allowables sources.
7. Build V&V matrix.

**Exit:** Every numerical load traces to a documented basis.

### Phase F2 — Classical analysis
Calculate:
- net-section stress;
- bearing;
- shear-out;
- lug failure;
- fastener shear/tension interaction;
- bending;
- bypass load;
- joint slip;
- eccentricity;
- margin of safety.

1. Implement independent spreadsheet and Python calculations.
2. Check units and limiting cases.
3. Size initial geometry.
4. Document uncertainty in allowables and loads.

**Exit:** Initial design is defensible without FEA.

### Phase F3 — Parametric CAD
1. Build parameterized part and assembly.
2. Preserve design intent.
3. Define interface geometry.
4. Model appropriate fastener/detail fidelity.
5. Generate mass properties.
6. Establish revision naming.
7. Create configuration table.

**Exit:** Design variants update predictably.

### Phase F4 — Drawing, PMI, and GD&T
1. Select functional datums.
2. Define hole pattern and position.
3. Define profile, perpendicularity, flatness, and surface finish where needed.
4. Define material, heat treatment, coating, and notes.
5. Perform critical tolerance stack.
6. Create model-based definition/PMI where supported.
7. Review every tolerance for functional necessity.

**Exit:** Drawing supports assembly and inspection.

### Phase F5 — FE model hierarchy
Create:
1. beam/plate reduced-order model;
2. shell model;
3. detailed solid/contact model.

For each:
- element choice;
- constraints;
- load introduction;
- contact;
- fastener representation;
- output quantities;
- intended decision.

**Exit:** Fidelity increases only where required.

### Phase F6 — Verification
1. Reaction-force equilibrium.
2. Displacement comparison to analytical model.
3. Mesh convergence.
4. Contact sensitivity.
5. Fastener stiffness sensitivity.
6. Boundary-condition sensitivity.
7. Solver comparison using ANSYS and Altair/OptiStruct where possible.
8. Identify singularities and nonphysical peak stresses.

**Exit:** Conclusions do not depend on a single mesh or boundary choice.

### Phase F7 — Nonlinear joint behavior
Analyze:
- bolt preload;
- friction;
- gap;
- slip;
- bearing;
- fastener load redistribution;
- material plasticity for limit exploration;
- contact opening/closing.

**Exit:** Critical joint behavior is physically interpreted.

### Phase F8 — Fatigue
1. Define representative spectrum.
2. Identify critical locations.
3. Perform stress-life or strain-life screening.
4. Apply mean-stress correction.
5. Calculate Miner damage.
6. Conduct sensitivity to spectrum and notch.
7. Define limitations of public allowables.

**Exit:** Fatigue claims are clearly bounded.

### Phase F9 — Damage tolerance
1. Select initial flaw assumptions.
2. Calculate stress-intensity range.
3. Use Paris-law or AFGROW-style crack growth.
4. Estimate residual strength.
5. Develop conceptual inspection interval.
6. Sensitivity to flaw size and spectrum.
7. State why this is screening, not certification.

**Exit:** Crack-growth conclusions are supported by public material data.

### Phase F10 — Dynamics
1. Modal analysis.
2. Boundary sensitivity.
3. Analytical frequency check.
4. Harmonic or random vibration.
5. Fastener/joint damping sensitivity.
6. Identify resonance and interface implications.
7. Optional shock-response spectrum.

**Exit:** Modes are physically interpreted and connected to design.

### Phase F11 — Optimization
1. Define mass, margin, stiffness, and manufacturability objectives.
2. Select design variables.
3. Run DOE.
4. Build response surfaces.
5. Evaluate robust design under uncertainty.
6. Select final configuration.
7. Preserve rejected designs and rationale.

**Exit:** Optimization respects real drawing and inspection constraints.

### Phase F12 — Public-data validation
1. Select published joint/lug/coupon experiments.
2. Reproduce specimen geometry and loads.
3. Predict stiffness, strain, contact, or failure.
4. Compare pre-correlation model.
5. Update only justified uncertain parameters.
6. Preserve pre- and post-correlation results.
7. Quantify residuals.

**Exit:** The FE method is validated against evidence outside the project.

### Phase F13 — Manufacturing and inspection
1. Process plan.
2. Critical characteristics.
3. Tooling/fixture assumptions.
4. Inspection methods.
5. Measurement uncertainty.
6. Sampling plan.
7. AS9102-style first-article package using synthetic/public measurement data.
8. Gage R&R and capability study using physically grounded simulated process data.

**Exit:** Design intent connects to measurable characteristics.

### Phase F14 — Digital thread
Create trace:

```text
structural requirement
→ CAD feature
→ PMI characteristic
→ analysis margin
→ inspection plan
→ measurement
→ nonconformance
→ disposition
→ corrective action
→ revised configuration
```

Use:
- STEP AP242;
- QIF-style data;
- SQLite or graph store;
- revision history;
- automated impact analysis.

**Exit:** A design revision invalidates affected downstream evidence.

### Phase F15 — Nonconformance and RCCA
Create at least three cases:
- hole-position error;
- thickness undersize;
- surface/edge defect;
- material lot deviation.

For each:
1. detect;
2. contain;
3. assess structural impact;
4. determine root cause;
5. disposition;
6. corrective action;
7. re-evaluate evidence.

**Exit:** Dispositions are engineering-based.

### Phase F16 — Final package
Produce:
- requirements and loads report;
- classical calculation book;
- CAD/drawing/PMI release;
- FE verification report;
- nonlinear joint report;
- fatigue/damage-tolerance report;
- dynamics report;
- optimization report;
- public-data validation report;
- manufacturing/inspection plan;
- digital-thread database;
- nonconformance/RCCA package;
- PDR/CDR-style reviews;
- evidence index.

---

## 4. Mandatory acceptance criteria

- Documented load path
- Independent classical calculations
- Parametric CAD and professional drawing
- Functional GD&T/PMI
- Multi-fidelity FE hierarchy
- Mesh/contact/boundary sensitivity
- Static, fatigue, crack-growth, and dynamics analysis
- Second solver or independent implementation
- Public experimental correlation
- Robust design trade
- Inspection/measurement uncertainty
- Revision-aware digital thread
- At least three nonconformance dispositions
- Requirements-to-evidence traceability

---

## 5. Rating conditions

- **Below 88:** CAD and one FEA contour
- **92:** solid static analysis but weak fatigue/validation
- **95:** full substantiation with public-data correlation and drawings
- **96:** manufacturing, quality, revision-aware digital thread, and RCCA
- **98+:** free university full-scale test, strain measurement, or external stress-team review

---

## 6. Final portfolio evidence

> Substantiated a representative transport-aircraft pylon attachment using classical sizing, nonlinear joint FEA, fatigue and damage-tolerance screening, modal/vibration analysis, parametric CAD/GD&T, public experimental correlation, inspection planning, nonconformance disposition, and a revision-aware AP242/QIF-style digital thread.
