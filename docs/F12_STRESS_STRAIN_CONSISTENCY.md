# F12 — Stress / plastic strain consistency investigation

**Companion to** `F12_FE_RESULTS_AF-DT-1000.md` §9. **This document supersedes the working
hypothesis stated there.**

**Claim boundary:** educational / representative / portfolio only. Non-OEM, non-certified.
All numbers `SYNTHETIC_TEST_ONLY`.

---

## 1. The observation

The bilinear isotropic hardening card defines, at any yielded point,

    sigma_vm = 469 + 760 * epsilon_p          (MPa)

This is not an approximation. Under J2 plasticity with isotropic hardening it is the yield
surface itself, so any point reporting `sigma_vm > 469` must carry exactly the plastic strain that
relation implies. The two quantities are not independent outputs — one determines the other.

Across the solved sweep they do not agree:

| e/D | epsilon_p measured | epsilon_p implied by peak stress | ratio |
|---|---|---|---|
| 1.0 | 0.37211 | 0.3700 | 1.006 |
| 1.2 | 0.03107 | 0.0690 | 0.450 |
| 1.8 | 0.00888 | 0.0491 | 0.181 |
| 2.0 | 0.00795 | 0.0454 | 0.175 |

Agreement is near-exact at e/D = 1.0 and degrades monotonically as the yielded region shrinks.

## 2. Hypothesis tested — nodal averaging. REJECTED.

**Stated before the test** (recorded in the results document): nodal averaging over elements that
are only partly yielded depresses reported plastic strain more than reported stress. If true,
switching to unaveraged results should bring the two into line — stress falling toward roughly
475 MPa, or plastic strain rising toward roughly 0.045.

**Test:** e/D = 2.0 model, Display Option switched to Unaveraged for both fields. No re-solve.
Both then reverted to Averaged and re-read to confirm the model was left unchanged.

| Quantity | Averaged | Unaveraged | Change |
|---|---|---|---|
| Peak von Mises | 503.49 MPa | **551.35 MPa** | +9.5% |
| Peak equivalent plastic strain | 0.0079481 | **0.008013** | +0.8% |

**The hypothesis is wrong.** Stress moved in the wrong direction — up, not down — and plastic
strain barely moved at all. Unaveraged results make the inconsistency worse:

    implied epsilon_p = (551.35 - 469) / 760 = 0.10836
    measured           = 0.008013
    ratio              = 0.074      (was 0.175 averaged)

Averaging is not the cause. It was partially *masking* the problem.

## 3. What the failed test revealed

The informative result is the **asymmetry in sensitivity**:

- Peak von Mises changed by **9.5%** between display modes
- Peak plastic strain changed by **0.8%**

Plastic strain is nearly invariant to how results are post-processed. Peak stress is not. This
inverts the usual assumption — here the **plastic strain is the robust quantity and the peak
stress is the fragile one**.

### Running the relation backwards

Because the yield surface fixes the relationship, measured plastic strain can be used to derive
the stress at the most-yielded integration point:

    sigma_derived = 469 + 760 * epsilon_p_measured

| e/D | epsilon_p | sigma derived (MPa) | sigma reported (MPa) | reported error |
|---|---|---|---|---|
| 1.0 | 0.37211 | 751.80 | 750.23 | -0.21% |
| 1.2 | 0.03107 | 492.61 | 521.47 | +5.86% |
| 1.8 | 0.00888 | 475.75 | 506.34 | +6.43% |
| 2.0 (avg) | 0.0079481 | 475.04 | 503.49 | +5.99% |
| 2.0 (unavg) | 0.008013 | 475.09 | 551.35 | **+16.05%** |

A consistent, one-sided pattern: where plasticity is widespread the reported peak is essentially
exact; where it is confined, the reported peak runs about 6% high on averaged results and 16% high
on unaveraged.

## 4. Revised mechanism — integration point to node extrapolation

Element results are computed at integration points and extrapolated to nodes for display.
Averaging then blends the extrapolated values from adjacent elements.

Where the plastic zone spans many elements (e/D = 1.0), stress gradients through each element are
gentle, extrapolation error is small, and the reported peak matches the yield surface to 0.2%.

Where the plastic zone is a few elements at the bore edge (e/D >= 1.2), the gradient across a
single element is steep, and extrapolating from integration points to the surface node overshoots.
Averaging against neighbouring elements partially cancels that overshoot, which is why the
**averaged** result is closer to correct and the **unaveraged** result is worse — the exact
opposite of what the rejected hypothesis predicted.

Plastic strain does not suffer the same overshoot because it is bounded below by zero and is
near-zero in the surrounding elastic material, so extrapolation cannot inflate it the same way.

**This mechanism is consistent with all the data in hand but has not itself been confirmed.**
It is recorded as the current best explanation, not as a finding. See §6 for the tests that would
confirm or reject it.

## 5. Consequence for the sweep

**Peak von Mises as reported by Ansys is not used quantitatively for e/D >= 1.2.**
Where a stress value is needed, `sigma_derived = 469 + 760 * epsilon_p` is used instead, because
the plastic strain it derives from is post-processing invariant to 0.8%.

**Revised physical picture at e/D = 2.0:** the material is barely yielding —
about **475 MPa, 1.3% above the 469 MPa yield**. The 503 MPa and 551 MPa figures are
post-processing artefacts. This is consistent with the hand-method bearing margin of +0.216, a
comfortable pass, and with the very small deformation of 0.4817 mm.

**Nothing in the sweep's conclusions changes.** Every conclusion in the results document rests on
deformation, plastic strain magnitude, reaction equilibrium, and closed-form margins — none on
reported peak stress. The failure mode map, the crossover at e/D = 1.353, the zero-margin point at
e/D = 1.201, and the elastic scaling law are all unaffected.

The mesh convergence study is also unaffected but is now better explained: peak von Mises there
oscillated within +/-2% and refused to converge monotonically, while deformation converged to
0.12% and reaction was exact. That is the same fragility, observed before its cause was
identified.

## 6. Open — tests that would confirm or reject the revised mechanism

- [ ] **Elemental Mean display option** at e/D = 2.0. This reports element-averaged values rather
      than node-extrapolated ones, so it should sit much closer to `sigma_derived = 475 MPa`. If it
      does not, the extrapolation mechanism is wrong too.
- [ ] **Mesh refinement at e/D = 2.0**, bore face 2 mm -> 1 mm. Extrapolation error scales with the
      stress gradient across a single element, so refinement should shrink the gap between
      reported and derived stress. If the gap is insensitive to mesh size, the mechanism is wrong.
- [ ] **Plastic strain at e/D = 1.5**, not captured during the sweep. Fills the one gap in the
      table in §1 and §3.

## 7. Method note

The rejected hypothesis is retained in full above rather than deleted. It was recorded before the
test, the test was chosen specifically because it could falsify it, and it was falsified. Removing
it would misrepresent how the conclusion in §4 was reached, and would hide that the currently
stated mechanism is itself unconfirmed and arrived at the same way.
