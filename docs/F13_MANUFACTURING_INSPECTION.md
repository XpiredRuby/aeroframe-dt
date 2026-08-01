# F13 — Manufacturing, Inspection and Quality Package — AF-DT-1000 Rev D

**Supports AFDT-REQ-008 and AFDT-REQ-013.** Turns the tolerances defined in
`PMI_GDT_DEFINITION.md` into a producible process plan, a measurable inspection plan, and — the
part that is actual engineering rather than paperwork — **a tolerance stack showing what the
released tolerance scheme does to the governing margin.**

**Claim boundary:** educational / representative / portfolio only. Non-OEM, non-certified.
Geometry and load case are `SYNTHETIC_TEST_ONLY`. All measurement data in §5 and §6 is
`SYNTHETIC_TEST_ONLY`. Material allowables and the tolerance-stack arithmetic are real.

**Executable evidence:** `tools/run_f13_inspection_plan.py` →
`results/software_verification/f13_inspection_plan.json`.
The plan itself is machine-readable at
`inspection_quality/inspection_plan_AF-DT-1000_revD.csv`.

---

## 1. Headline result

| | MS |
|---|---|
| Nominal Rev D | **+0.0784** |
| **Worst case, all released tolerances at their adverse limit** | **+0.0568** |
| RSS of the same three terms | +0.0636 |

**The tolerance scheme consumes 27.6% of the margin and leaves it positive.**
Tolerances would have to be **3.62x wider** to reach MS = 0.

This closes limitation 2 of `PMI_GDT_DEFINITION.md` §7 ("no statistical tolerance stack has been
performed"). Derivation in §7.

---

## 2. Manufacturing process plan

Single-piece machining from plate. No forging, no welding, no assembly operations on the fitting
itself.

| Op | Operation | Structural reason it is written this way |
|---|---|---|
| 010 | Receive 7075-T7351 plate, AMS 4078 or AMS-QQ-A-250/12, thickness band 2.001–2.500 in. Verify certificate and **rolling direction marking**. | The allowables in `MARGIN_SUMMARY.md` §3 are band-specific. A plate outside 2.001–2.500 in has different A-basis values and voids the margin. |
| 020 | Lay out and mark the blank with the L direction identified. **Blank orientation is a hold point.** | §3 below. An incorrectly oriented blank is a structural nonconformance. |
| 030 | Rough mill the external envelope, 0.060 in stock on all finished surfaces. | Stock allowance keeps rough-cut residual stress out of the finished skin. |
| 040 | Stress-relieve by natural stabilisation between rough and finish. No thermal treatment. | T7351 is **already stress-relieved by stretching** as part of the temper. Any post-machining thermal cycle would alter the temper and invalidate the allowables. |
| 050 | Finish mill Datum A flange underside. **A is cut first and becomes the fixture reference for everything after.** | Datum A is the analysis reaction plane (F5 fixed support, area 6.1688e-2 m²). Cutting it first means every later feature is located from the same surface the analysis assumes. |
| 060 | Finish mill lug blade and flange to size, including the R0.500 blends. | Constant-thickness blade, `t_web = t_lug = 2.500`. |
| 070 | Drill the 8x ⌀0.250 fastener pattern from Datum A. | Establishes Datum B. |
| 080 | Semi-finish bore ⌀1.990, then finish bore ⌀2.000 +0.002/−0.000 in a single setup from A and B. | Bore last, one setup. Position, cylindricity and perpendicularity are all held against the same reference; re-fixturing is the dominant source of the position error that F15 documents. |
| 090 | Finish the bore to Ra 32 µin. **No cold expansion, no shot peen.** | §3.2. |
| 100 | Deburr all edges. **Blend radii are controlled features (profile 0.015) — do not hand-blend them.** | The F15-family NCR "deburr tool contact at the lug blend" is exactly this failure. |
| 110 | Final inspection per §4. | |
| 120 | Eddy-current inspection of the bore. | AFDT-CHAR-010. Structural, not QA boilerplate — see §4.2. |

## 3. Orientation and special-process control

### 3.1 Grain orientation — a hold point, not a note

    lug axis        -> L   (rolling direction)
    transverse load -> LT
    bore axis       -> ST

MIL-HDBK-5J Table 3.7.6.0(b3) gives `Ftu(ST) = 62 ksi` against 65 (L) and 66 (LT), and
Table 3.1.2.3.1(b) flags 7075-T7351 as stress-corrosion susceptible in ST with a 39 ksi threshold
at this thickness. **A 90° blank rotation costs 6% of Ftu and puts the SCC-susceptible direction
into the primary load path.** It is not detectable by dimensional inspection after machining, which
is why it is controlled at op 020 as a hold point and re-verified by certificate review at op 110.

### 3.2 Cold expansion and peening — deliberately excluded

Split-sleeve cold expansion of the bore is standard practice for fatigue-critical holes and would
plausibly improve the damage-tolerance life established in F9. **It is excluded here**, for two
reasons that are worth stating rather than leaving implicit:

1. The compressive residual field it produces is **not in the F9 model**. Taking credit for it
   without modelling it would be exactly the kind of unsupported optimism that cost this project a
   factor of 9.1 in margin.
2. Cold expansion changes bore size and cylindricity after the finish bore, and both are controlled
   features tied to the F7 contact basis (`PMI_GDT_DEFINITION.md` §4.3).

If cold expansion were later introduced it would be a **design change requiring re-analysis of F7
and F9**, not a process improvement.

## 4. Inspection plan

Ten measurable characteristics, machine-readable in
`inspection_quality/inspection_plan_AF-DT-1000_revD.csv` and validated by
`tools/run_f13_inspection_plan.py`.

| ID | Feature | Characteristic | Tolerance | Instrument | Sampling | Class |
|---|---|---|---|---|---|---|
| AFDT-CHAR-001 | Datum A face | Flatness | 0.008 | CMM | 100% | critical |
| AFDT-CHAR-002 | Pin bore | Position to A, B at MMC | ⌀0.030 | CMM | 100% | critical |
| AFDT-CHAR-003 | Pin bore | Diameter | ⌀2.000 +0.002/−0.000 | air gauge | 100% | critical |
| AFDT-CHAR-004 | Pin bore | Cylindricity | 0.002 | CMM | 100% | critical |
| AFDT-CHAR-005 | Pin bore | Perpendicularity to A | 0.005 | CMM | 100% | critical |
| AFDT-CHAR-006 | Lug blade | Thickness | 2.500 ±0.020 | micrometer | 100% | critical |
| AFDT-CHAR-007 | Fastener pattern | Position to A at MMC | ⌀0.014 | CMM | FAI + 10% | major |
| AFDT-CHAR-008 | R0.500 blends | Profile of a surface | 0.015 | CMM | FAI + 10% | major |
| AFDT-CHAR-009 | Pin bore | Roughness Ra | 32 µin max | profilometer | 100% | critical |
| AFDT-CHAR-010 | Pin bore | Subsurface indication | none ≥ 1.27 mm | eddy current | 100% | critical |

Plus two attribute characteristics with no numeric limit:

| ID | Characteristic | Method | Accept |
|---|---|---|---|
| AFDT-ATTR-001 | Grain orientation per §3.1 | mill certificate + op 020 hold-point record | L/LT/ST as specified |
| AFDT-ATTR-002 | Material band 2.001–2.500 in | certificate review | in band |

### 4.1 Why every bore characteristic is 100% inspected

The bore is simultaneously the load-introduction feature, the critical stress location confirmed by
F5 FE, and the crack-initiation site identified in F9. **Every failure mode in this project passes
through the bore.** Sampling a feature that carries all of them is not defensible at MS = +0.078.

The two non-bore, non-critical characteristics — the fastener pattern and the blend profile — are
sampled, because neither is in the governing load path and the fastener group is not the critical
feature (`PMI_GDT_DEFINITION.md` §7.4).

### 4.2 The eddy-current requirement

`F9_DAMAGE_TOLERANCE.md` gives `a_c = 3.07 mm`, and `F9b` sets a 4,500-flight repeat interval
predicated on reliably detecting a 1.27 mm flaw. **Visual inspection cannot find 1.27 mm.** If the
available NDI method cannot demonstrate that threshold, the interval must shorten — this
characteristic and the inspection interval are one decision, not two.

### 4.3 Gauge resolution screen

Every characteristic passes the 10:1 rule (instrument resolution ≤ 10% of the tolerance band). The
tightest ratio is **AFDT-CHAR-004 cylindricity at 5.0%** (0.0001 in resolution on a 0.002 band) —
acceptable, but it is the first characteristic that would fail if the tolerance tightened. Screen
implemented in `tools/run_f13_inspection_plan.py`.

## 5. Measurement system analysis — SYNTHETIC data

Balanced crossed gauge R&R, 3 parts x 2 operators x 2 repeats, through
`aeroframe_dt.inspection.crossed_gage_rr`. Run on the two characteristics the margin is actually
sensitive to.

| Characteristic | % gauge R&R of total variation | Precision-to-tolerance | Verdict |
|---|---|---|---|
| AFDT-CHAR-006 lug thickness | 5.05% | 3.03% | acceptable |
| AFDT-CHAR-002 bore position | 2.86% | 4.24% | acceptable |

**Both are reported** because they answer different questions. % gauge R&R compares the gauge to
the observed part scatter and depends on which parts you happened to pick; precision-to-tolerance
compares the gauge to the specification and does not. **P/T is the one that matters for an
acceptance decision** — it is the fraction of the tolerance band the measurement itself consumes.

**Reproducibility came out identically zero in both studies.** That is the variance-component
estimator clamping a negative operator-variance estimate to zero, which happens when the true
operator effect is small relative to repeatability. It means "no detectable operator effect in this
dataset", not "operators are identical". With 2 operators and 2 repeats the study has very little
power to see one.

## 6. Process capability — SYNTHETIC data

Ten parts on AFDT-CHAR-006, the thickness characteristic:

    mean 2.5011 in, sample sigma 0.002979 in
    Cp = 2.24, Cpk = 2.12  -> capable (>= 1.33)

Consistent with `PMI_GDT_DEFINITION.md` §4.1, which notes thickness is easy to hold. **The
capability is high because the tolerance is loose relative to the process, not because the margin
is comfortable** — §7 shows the thickness tolerance still costs 0.0086 of margin at its limit.

## 7. Tolerance stack onto the governing margin

This is the part of F13 that is engineering rather than documentation, and it closes
`PMI_GDT_DEFINITION.md` §7 limitation 2.

**Method.** Rather than linearising, each geometric term is pushed back through the real
Melcon-Hoblit interaction from `MARGIN_SUMMARY.md` §4:

    MS = 1/(Ra^1.6 + Rtr^1.6)^0.625 - 1,   Ra = 0.3909, Rtr = 0.7740  ->  MS = +0.07843

### 7.1 Thickness — exact

Every lug area (`Abr = D·t`, `Atn = (w−D)·t`, `Aav`) is linear in `t`, so at reduced thickness both
load ratios scale by `t_nom/t`. At the low material limit `t = 2.480`:

    Ra, Rtr x 1.008065  ->  MS = +0.06980,  dMS = -0.00863

**Cross-check:** the linear sensitivity in `PMI_GDT_DEFINITION.md` §4.1 (`dMS/dt = 0.431/in`)
predicts −0.00862. **Agreement to 0.1%** — the exact and linearised routes are independent and
they land on the same number.

### 7.2 Bore position — extrapolated, and the dominant term

Radial offset is taken at the **LMC condition including the full MMC bonus**:

    radial = (0.030 + 0.002)/2 = 0.016 in
    dMS = -0.016 x 0.747 = -0.01195

`dMS/de = 0.747/in` is the F15-anchored extrapolation from `PMI_GDT_DEFINITION.md` §4.2. It is
**not derived** — the K-factor curves are not digitised in this project, and the relationship is
nonlinear. Because the anchor sits far from the operating point, this term is the **least
trustworthy number in the stack, and it is also the largest.** Both facts should be read together.

### 7.3 Bore size — bounded, not resolved

At LMC (`D = 2.002`) the bearing area `D·t` rises 0.1% while the net-section area `(w−D)·t` falls
0.1%. The two effects act in opposition, and which one governs depends on whether bearing or net
section controls the axial term — not established in this project. **The adverse 0.1% is therefore
applied to both ratios, which bounds the term rather than resolving it:**

    dMS <= -0.00108

Any true value lies between roughly zero and this bound.

### 7.4 Combined

| Term | ΔMS | Basis |
|---|---|---|
| Thickness at LML | −0.00863 | exact |
| **Bore position at LMC with MMC bonus** | **−0.01195** | extrapolated |
| Bore size at LMC | −0.00108 | bounded |
| **Worst case (arithmetic sum)** | **−0.02166** | |
| RSS | −0.01478 | |

    MS worst case = +0.0568
    MS RSS        = +0.0636

**Worst case is the acceptance basis.** RSS is reported for context only and should not be leaned
on here: it assumes independent, centred, normally distributed contributors, and the position term
is none of those — it is a radial zone whose adverse direction is a matter of orientation, not a
symmetric two-sided variation. Three contributors is also far too few for the central-limit
argument that makes RSS respectable.

### 7.5 What this says about the design

- **The tolerance scheme is not the binding constraint.** It costs 27.6% of the margin; the
  thick-lug correction cost 77%.
- **Bore position dominates the stack** at 55% of the worst-case loss, despite being toleranced at
  only 14% of the offset that would exhaust the margin. Tightening thickness would buy little;
  tightening position, or digitising the K-factor curves so the term stops being an extrapolation,
  is where the effort belongs.
- **This stack is on top of an already-thin margin.** At the Ekvall worst-case scatter of −0.094
  the stack is irrelevant, because the part is already negative. The stack answers "does
  manufacturing variation break it", not "is the margin adequate".

## 8. First article and acceptance

- **First article:** all 10 numeric characteristics plus both attribute characteristics, full
  dimensional report, AS9102-style format. Required on the first part and after any change to the
  fixture, the CAM program, or the plate lot.
- **Production:** 100% on the eight critical characteristics; FAI plus 10% on the two major ones.
- **Acceptance:** a part is accepted only when every critical characteristic is within limits
  **and** the material certificate confirms both the thickness band and the grain orientation. No
  material review board disposition is available for out-of-band material or wrong orientation —
  the allowables would not apply.

## 9. Nonconformance routing

Any out-of-tolerance critical characteristic routes to the F15 process
(`F15_NONCONFORMANCE_RCCA_AF-DT-1000.md`): containment, measurement-uncertainty assessment,
structural re-assessment against `MARGIN_SUMMARY.md`, disposition, root cause, corrective action,
re-verification.

**The measurement-uncertainty step is not optional.** With P/T at 3–4% the gauge is not the
question for a gross deviation, but for a borderline reading — a thickness of 2.4795 against a
2.480 limit — the measurement uncertainty is comparable to the exceedance, and the disposition has
to say so.

The F15 case (bore position 2.500 → 1.900 in edge distance) is **roughly 20x the position
tolerance** and sits far outside anything this stack covers. It remains a REWORK.

## 10. Limitations

1. **All measurement data in §5 and §6 is synthetic.** No parts were made or measured. The
   analysis methods are real; the numbers they consume are not.
2. **The bore-position sensitivity is extrapolated**, and it is the dominant stack term. Digitising
   the AFFDL K-factor curves would replace it with a derived value and is the single highest-value
   improvement to this document.
3. **The bore-size term is bounded, not resolved.** Establishing whether bearing or net section
   governs the axial term would collapse it.
4. **No thermal, fixture-induced or residual-stress distortion** is in the stack. Op 040 argues
   these are small for this temper and process, but that argument is qualitative.
5. **Datum A flatness is not in the stack.** Its effect is on the fixed-support idealisation rather
   than on a lug area, and quantifying it needs a flange contact-pressure study that does not
   exist.
6. **Two operators and two repeats** is a weak gauge study. It is enough to screen, not enough to
   qualify a measurement system.
