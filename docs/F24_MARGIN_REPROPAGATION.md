# F24 — Margin Re-propagation at 7050-T7451 — AF-DT-1000

**Claim boundary:** educational / representative / portfolio only. Non-OEM, non-certified.

**This document supersedes the governing margin in `MARGIN_SUMMARY.md`.** That document still states
`MS = +0.156` on 7075-T7351; it has not yet been re-issued.

F23 recommended changing to 7050-T7451 and flagged that the elastic-plastic contact ratio had been
measured on 7075 properties and must be re-measured. **It has been.**

---

## 1. The measurement

Ansys Mechanical 2025 R2, project `f7plastic7050`, restored from the clean `f7plastic` parent.
Bilinear isotropic hardening, **yield 413.7 MPa** (7050-T7451 A-basis `Fty` = 60 ksi), **tangent
modulus 2018 MPa**, derived by the same `(Ftu − Fty)/(e_f − e_y)` route F16 used. Elastic constants
unchanged — 7050 and 7075 are identical to tabulated precision. Pin remains `steel4340`.

| | 7075 elastic (F7) | 7075 elastic-plastic (F16) | **7050 elastic-plastic (F24)** |
|---|---|---|---|
| p_real, MPa | 2955.9 | 2236.9 | **2316.6** |
| p_stiff, MPa | 2012.7 | 1633.0 | **1581.8** |
| **t_eff/t** | 0.6809 | 0.7300 | **0.6828** |

**`t_eff/t = 0.6828` — within 0.3% of the elastic value.**

### 1.1 The prediction held

F23 §4.1 predicted this, before the run: 7050 yields at 60 ksi against 7075's 52, so less material
plasticises at the bearing edge, so less load redistributes, so the ratio falls back **toward** the
elastic bound rather than holding at 0.730.

It did. **The +7.2% recovery that plasticity bought the 7075 design does not exist for 7050.** This
fitting now earns its margin from material strength alone.

Both runs completed cleanly. The stiff-pin case produced the usual weak-springs warning, as it did
in F7 and F16 — expected, and not an error.

## 2. Governing margin

Load ratios scale as `1/t_eff` from the elastic reference, then with the allowables. Validating the
method against the published F16 result before applying it:

    model check, 7075 e-p:  Ra = 0.36461  Rtr = 0.72194  ->  MS = +0.1562
    published F16:          Ra = 0.36463  Rtr = 0.72198  ->  MS = +0.156

Reproduces to four decimals. Applying it at the measured ratio and MMPDS-2026 7050-T7451 A-basis
allowables (`Ftu` L 70 ksi, LT 70 ksi, against 7075's 65 / 66):

    7050-T7451, t_eff/t = 0.6828
      on 7075 allowables:  Ra = 0.38981  Rtr = 0.77183  ->  MS = +0.0815
      on 7050 allowables:  Ra = 0.36196  Rtr = 0.72773  ->  MS = +0.151

**`MS = +0.151`.**

### 2.1 Where the margin comes from

| Contribution | MS |
|---|---|
| 7075 allowables, elastic ratio | +0.078 |
| 7075 allowables, 7050's measured ratio | +0.082 |
| **7050 allowables, 7050's measured ratio** | **+0.151** |

**Essentially all of the gain is the material; almost none is plasticity.** Under 7075 the split ran
the other way — the elastic-plastic measurement was worth +0.078 and the allowables were fixed.

### 2.2 Against the released number

**`+0.156` → `+0.151`.** Marginally lower.

The material change was never about raising the margin. It was forced by F23's finding that
7075-T7351 plate is not tabulated above 4.000 in while this part needs 6.000 in stock. **The margin
is preserved almost exactly while moving onto a material the part can actually be made from**, cited
from the current handbook, with fatigue and crack-growth data available.

## 3. Ekvall method scatter

| Pairing | 7075-T7351 (F16) | **7050-T7451 (F24)** |
|---|---|---|
| A-basis consistent, 99%/95%, ×1.195 | −0.032 | **−0.037** |
| B-basis consistent, 90%/95%, ×1.099 | +0.052 | **+0.048** |

**The A-basis worst case still does not clear, and is marginally worse than before** — the plasticity
gain that had lifted it from −0.094 to −0.032 is gone.

This project uses A-basis allowables, so **−0.037 is the statistically consistent worst case and it
is negative.** No claim is made that the fitting clears A-basis method scatter. The position is
unchanged in kind from F16 and F18: negative at the A-basis pairing, positive at the B-basis
pairing, and a demonstrated redundant load path would resolve it.

## 4. Tolerance stack — partially re-propagated

`tools/run_f13_inspection_plan.py` re-run at `t_eff/t = 0.6828`:

| | 7075 e-p (F13 as released) | at measured ratio |
|---|---|---|
| Worst-case delta | −0.0232 | **−0.0217** |
| Sensitivity `dMS/de` | 0.8013 /in | 0.7495 /in |

**But the tool hardcodes the 7075 allowables**, so its `ms_nominal` of +0.0814 is the 7075 number,
not +0.151. The **delta** is usable and the **nominal is not**.

Taking the delta against the correct nominal gives an indicative worst case of roughly **+0.130**,
consuming about 14% of the margin. **That figure is indicative only.** The sensitivity itself depends
on the allowables, so the stack has to be recomputed with 7050 values in the tool before any stack
number is quoted. That is a code change, not an analysis change, and it belongs to the next phase.

## 5. What this changes

| Document | Status |
|---|---|
| `MARGIN_SUMMARY.md` | **stale** — still states +0.156 on 7075 |
| `STRESS_REPORT_AF-DT-1000.md` | **stale** — §6.3 states the F16 basis |
| `F13_MANUFACTURING_INSPECTION.md` | **stale** — stack at the 7075 operating point |
| `tools/run_f13_inspection_plan.py` | needs 7050 allowables |
| F16 | **not superseded** — it remains the correct 7075 measurement, and the comparison in §1 depends on it standing |

## 6. Limitations

1. **One mesh only.** The 1.50 mm bore mesh was not re-converged for 7050. The ratio construction is
   the same one F7 converged over three meshes at 8.2%, and the two alloys are elastically
   identical, so the convergence argument is inherited rather than re-demonstrated — the same
   limitation F16 carried.
2. **Peak plastic strain was not recorded** for these runs. 7050's tabulated LT elongation at this
   band is **4%**, against 7075's 6%, so the strain-versus-elongation caveat in F16 §5 is *more*
   acute here, not less. It has not been quantified.
3. **The stack nominal in §4 is indicative.** See the paragraph there.
4. **Ekvall applicability to 7050 remains unverified**, per F23 §8.3.
5. The margin rescaling assumes the governing failure mode is unchanged. Net tension still governs
   the axial term at 7050's allowables, but the interaction was not recomputed from first
   principles.
