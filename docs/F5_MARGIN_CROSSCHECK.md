# F5 — Margin Cross-Check, Like for Like

**Companion to** `F5_FE_REVD_LINEAR_ELASTIC.md` §6, which identified that a linear elastic peak
stress cannot be compared against an allowable-based margin, and recommended this comparison
instead. This document closes that item.

**Claim boundary:** educational / representative / portfolio only. Non-OEM, non-certified.
All numbers `SYNTHETIC_TEST_ONLY`.

---

## 1. The problem being solved

The hand margin of **+0.710** comes from the Melcon-Hoblit method, which works in **loads**:
applied load `P` against empirical allowable load `P'`. The FE run produces **stresses**. The
converged FE peak of 1194 MPa is 2.44x Ftu, which reads alarming but is meaningless as a comparison
— empirical lug allowables already incorporate the stress concentration and local plastic
redistribution that the linear elastic peak is measuring.

Comparing them directly is a category error. The valid comparison converts both sides to the same
basis.

## 2. Method — convert allowable loads to allowable stresses

Nominal areas, from `HANDOFF.md` §4:

    Abr = D * t     = 2.000 * 2.500 = 5.00 in^2      (bearing)
    Atn = (w - D)*t = (4.000-2.000)*2.500 = 5.00 in^2 (net tension)

Empirical allowable loads, from `HANDOFF.md` §6, divided by their respective areas:

| Allowable | Load (lb) | Area (in^2) | Stress (MPa) | After 1.15 fitting factor |
|---|---|---|---|---|
| Bearing, P'bru | 440,200 | 5.00 | 607.0 | 527.8 |
| Net tension, P'tu | 337,250 | 5.00 | 465.1 | 404.4 |
| Transverse, P'tru | 279,562 | 5.00 | 385.5 | 335.2 |

The 1.15 fitting factor is applied per AA-SM-009-005 for the combined oblique case, as recorded in
`HANDOFF.md` §6.

Applied nominal stresses, using the same load components as the FE model
(`Fx = 529,740 N` transverse, `Fz = 317,840 N` axial) over `Abr = 3225.8 mm^2`:

    axial      = 317,840 / 3225.8 =  98.53 MPa
    transverse = 529,740 / 3225.8 = 164.22 MPa

## 3. Result — the hand margin reproduces exactly

    Ra  = 98.53  / 404.4 = 0.2437
    Rtr = 164.22 / 335.2 = 0.4899

    MS = 1 / (Ra^1.6 + Rtr^1.6)^0.625 - 1 = +0.7104

| Quantity | Reconstructed here | Recorded in HANDOFF §6 | Agreement |
|---|---|---|---|
| Ra | 0.2437 | 0.2436 | 0.04% |
| Rtr | 0.4899 | 0.4899 | exact |
| **MS** | **+0.7104** | **+0.710** | **0.06%** |

The +0.710 margin is **internally consistent and reconstructible from first principles**, including
the placement of the 1.15 fitting factor and the 1.6 / 0.625 oblique interaction exponents.

## 4. What this does and does not prove

**Be precise about the FE's role.** The nominal stresses in §2 are applied load divided by nominal
area. **The FE does not influence them.** This section is therefore a re-derivation of the hand
method on a different basis — a check of its internal consistency and of the arithmetic — not an
independent confirmation of the margin.

**What the FE independently established, and the hand method could not:**

1. **The full applied load actually reaches the assumed load path.** FE reaction resultant
   617,812 N against 617,776 N applied — **0.006%**, after mesh convergence. The hand method
   *assumes* the bore reacts the entire load into the flange; the FE demonstrates it.
2. **The bore is the critical location**, which is where the lug method applies. Had the peak
   appeared at the blade-to-flange fillet, the hand method would have been substantiating the wrong
   feature.
3. **No secondary critical location exists.** The blade root does not govern, contrary to the
   pre-run prediction recorded in `F5_FE_REVD_LINEAR_ELASTIC.md` §7.
4. **Mesh convergence and equilibrium** hold, so the model is a sound basis for the later phases.

**Division of labour:** the FE validates the *assumptions* of the hand method. The empirical
allowables supply the *margin*. Neither substitutes for the other, and a linear elastic FE cannot
produce an allowable-based margin no matter how well converged it is.

## 5. What would genuinely challenge the +0.710

Only two things, neither currently available:

- **An elastic-plastic FE run with verified 7075-T7351 yield and hardening data.** This project has
  no such data and must not invent it. Even then, the comparison would need a failure criterion the
  bilinear model does not supply — the limitation documented at length in
  `F12_STRESS_STRAIN_CONSISTENCY.md`.
- **A physical test.** Ruled out by project constraint.

The correlation route already taken — Ekvall's 243 lug tests, predicted/test 0.85 to 1.19 — remains
the strongest available check on the allowables themselves, and it places the margin in the band
**+0.44 to +1.01** with a mean of +0.70.

## 6. Status

**The F5 FE cross-check is closed.** The margin is reproducible, the load path is verified, the
critical location is confirmed, and the limits of what FE can say about an allowable-based margin
are documented rather than papered over.
