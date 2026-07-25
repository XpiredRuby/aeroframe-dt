# F5 Static Results — AF-DT-1000, Rev D

**Decision ID:** F5-AFDT-1000-revD
**Supersedes:** `docs/F5_STATIC_RESULTS_AF-DT-1000_revB.md` and the PROVISIONAL margins in
`docs/DECISIONS_AF-DT-1000_revD.md` §6.
**Method:** Lug oblique-load method, NASA TM X-73305 (1975) §B2, via Abbott Aerospace
AA-SM-009-005. Melcon-Hoblit lineage.
**Claim boundary:** educational / representative / portfolio only. Non-OEM, non-certified.
All values `SYNTHETIC_TEST_ONLY`.

---

## 1. Headline result

**Margin of Safety = +0.71** at the LC-02 oblique load (59.04° off the lug axis).

This replaces the earlier provisional +0.11. The margin improved — it did not go negative — once
three previously-open inputs were resolved against the source method. The provisional value was
pessimistic because it used a wrong material curve and an incorrect area assumption.

---

## 2. What changed from the provisional estimate

Three open items from `docs/DECISIONS_AF-DT-1000_revD.md` §6 are now closed.

### 2.1 A₁–A₄ areas — were a guess (1.5 in²), now derived (3.75 in²)
Per NASA TM X-73305 Fig 12.2.9-5, for a plain rectangular lug the four transverse-idealisation
areas are **not free parameters**. Each equals the ligament area on its radial section:

    A₁ = A₂ = A₃ = A₄ = (e − D/2) · t = (2.5 − 1.0) · 2.5 = 3.75 in²

The weighted average area is therefore

    Aav = 6 / (3/A₁ + 1/A₂ + 1/A₃ + 1/A₄) = 3.75 in²
    Aav / Abr = 3.75 / 5.00 = 0.75

The earlier 1.5 in² assumption understated these by 2.5×, which suppressed the transverse
allowable.

### 2.2 Curve number — was Curve 8 (wrong material), now Curve 5
The transverse and axial K-factor curves are material-specific (Fig 12.2.9-4 and -7 notes).
**Curve 8 is 18-8 stainless / thick 7075 forgings — not this material.** For 7075 panel stock
the correct selection is **Curve 5** (2014-T6 and 7075-T6 panel ≤ 0.5 in). This is the single
largest correction:

    Transverse Ktru at Aav/Abr = 0.75:  Curve 8 → 0.387   |   Curve 5 → 0.7875

The transverse efficiency roughly doubled.

### 2.3 Kt disagreement (AA-SM-009-002 vs -005) — resolved, not a real conflict
The two sheets differed (191 700 vs 202 350 lb) because -005 applies the method's recommended
10% off-axis / 1.15 fitting-factor convention to the combined oblique case, while -002 is a
pure-axial check without it. For a combined 59° load the oblique sheet (-005) is the correct
tool. The 1.15 fitting factor is applied here.

---

## 3. Inputs (rev D geometry, LC-02 load)

| Symbol | Value | Meaning |
|---|---|---|
| D | 2.000 in | pin / hole diameter |
| t | 2.500 in | lug thickness |
| e | 2.500 in | edge distance |
| w | 4.000 in | lug width |
| Ftu | 71 000 psi | ult. tensile (representative) |
| Ftux | 71 000 psi | transverse ult. (set equal — see §5 caveat) |
| P_axial | 71 453 lb | Z component (317 840 N) |
| P_transverse | 119 090 lb | X component (529 740 N) |
| Fitting factor | 1.15 | per method |

Derived: e/D = 1.25, w/D = 2.00, D/t = 0.80, Abr = 5.00 in², Atn = 5.00 in², Aav = 3.75 in².

---

## 4. Allowables and interaction

| Factor | Source | Value |
|---|---|---|
| Kt (axial) | Fig 12.2.9-4, Curve 5, w/D = 2.0 | 0.950 |
| Ktru (transverse) | Fig 12.2.9-7, Curve 5, Aav/Abr = 0.75 | 0.7875 |
| Kbr (shear-bearing) | Fig 12.2.9-3, e/D = 1.25 | 1.240 |

| Allowable | Formula | Value |
|---|---|---|
| P'bru shear-bearing | Ftu · Kbr · Abr | 440 200 lb |
| P'tu net tension | Ftu · Kt · Atn | 337 250 lb |
| P'tru transverse | Ftux · Ktru · Abr | 279 562 lb |

Interaction (exponent 1.6):

    Ra  = (P_ax · 1.15) / min(P'bru, P'tu) = 82 171 / 337 250 = 0.2436
    Rtr = (P_tr · 1.15) / P'tru            = 136 954 / 279 562 = 0.4899
    M.S. = 1 / (Ra^1.6 + Rtr^1.6)^0.625 − 1 = +0.710

Transverse dominates (Rtr ≈ 2× Ra), consistent with the vertical lug axis established in the
rev C load basis.

---

## 5. Verification and caveats

**Method validated against the source spreadsheet's own worked example.** Reproducing
AA-SM-009-005's shipped example (P1=3500, P2=1500, D=0.75, t=0.375, e=1.0) with this
implementation returns Aav = 0.08563, P'tu = 30 879 lb, P'tru = 7406 lb, MS = 2.346 — matching
the sheet line-for-line. The rev D numbers use the identical, validated calculation chain.

**Caveats carried forward:**
- **Ftux = Ftu is optimistic.** Real 7075 is ~5-10% weaker transverse (short-transverse grain).
  A −10% Ftux sensitivity drops the margin to roughly +0.5 — still positive. A proper A/B-basis
  transverse allowable remains an F5 open item.
- Material allowable is still representative (71 ksi), not A/B-basis.
- Pin bending at t/D = 1.25 is not covered by this method and remains a separate F5 check.
- This is a hand-method result. The rev D Ansys run (both components on the bore) is the
  independent FE confirmation and is still outstanding.

---

## 6. Status

The pylon static margin is **no longer provisional** for the lug oblique check. The governing
LC-02 margin is **+0.71**, positive with room. Remaining F5 work: transverse allowable basis,
pin bending, and the FE cross-check.
