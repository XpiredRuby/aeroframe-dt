# F12 — Stress / plastic strain consistency investigation

**Companion to** `F12_FE_RESULTS_AF-DT-1000.md` §9. **This document supersedes the working
hypothesis stated there.**

**Outcome: closed as bounded, not fully resolved.** One hypothesis was tested and rejected. A
second was tested twice and the two tests disagree. A flaw in the consistency check itself was
identified after the fact. The practical answer is a bracketed stress range, and no sweep
conclusion depends on narrowing it further.

**Claim boundary:** educational / representative / portfolio only. Non-OEM, non-certified.
All numbers `SYNTHETIC_TEST_ONLY`.

---

## 1. The observation

The bilinear isotropic hardening card defines, at any yielded point,

    sigma_vm = 469 + 760 * epsilon_p          (MPa)

Under J2 plasticity with isotropic hardening this is the yield surface itself, so a point
reporting `sigma_vm > 469` must carry exactly the plastic strain that relation implies. The two are
not independent outputs.

Across the sweep they did not agree:

| e/D | epsilon_p measured | epsilon_p implied by peak stress | ratio |
|---|---|---|---|
| 1.0 | 0.37211 | 0.3700 | 1.006 |
| 1.2 | 0.03107 | 0.0690 | 0.450 |
| 1.8 | 0.00888 | 0.0491 | 0.181 |
| 2.0 | 0.00795 | 0.0454 | 0.175 |

## 2. Hypothesis 1 — nodal averaging. REJECTED.

**Stated before the test:** averaging over partly-yielded elements depresses reported plastic
strain more than reported stress. If true, unaveraged results should bring them into line — stress
falling toward ~475 MPa or plastic strain rising toward ~0.045.

**Test:** e/D = 2.0, Display Option switched to Unaveraged for both fields, no re-solve, then
reverted and re-read to confirm the model was unchanged.

| Quantity | Averaged | Unaveraged | Change |
|---|---|---|---|
| Peak von Mises | 503.49 MPa | **551.35 MPa** | +9.5% |
| Peak equivalent plastic strain | 0.0079481 | **0.008013** | +0.8% |

**Rejected.** Stress moved the wrong way and plastic strain barely moved. Unaveraged makes the
inconsistency worse (ratio 0.175 -> 0.074). Averaging was partially *masking* the problem, not
causing it.

## 3. What the failed test revealed

The informative result was the **asymmetry in sensitivity**: peak stress changed 9.5% between
display modes, peak plastic strain changed 0.8%. Plastic strain is nearly invariant to
post-processing; peak stress is not.

Running the yield surface backwards gives a stress estimate from the robust quantity:

    sigma_derived = 469 + 760 * epsilon_p_measured

| e/D | epsilon_p | sigma derived | sigma reported | absolute gap |
|---|---|---|---|---|
| 1.0 | 0.37211 | 751.80 | 750.23 | -1.6 MPa |
| 1.2 | 0.03107 | 492.61 | 521.47 | +28.9 MPa |
| 1.8 | 0.00888 | 475.75 | 506.34 | +30.6 MPa |
| 2.0 | 0.0079481 | 475.04 | 503.49 | +28.5 MPa |

**Restating in stress space corrects a misleading impression.** Near yield,
`epsilon_p = (sigma - 469)/760` is a small difference of large numbers: a 5 MPa error in sigma
shifts epsilon_p by 0.0066, which at e/D = 2.0 is comparable to epsilon_p itself. Comparing in
strain space is ill-conditioned and inflated a modest ~29 MPa stress error into an apparent
"factor of 5.7". The absolute gap is in fact **nearly constant at 28-31 MPa** wherever plasticity
is confined, and near zero where it is widespread.

## 4. Hypothesis 2 — integration point to node extrapolation. TESTS DISAGREE.

Element results are computed at integration points and extrapolated to nodes for display. Where
the plastic zone spans many elements the gradient per element is gentle and extrapolation error is
small; where it is a few elements at the bore edge the gradient is steep and extrapolation to the
surface node overshoots.

### Test A — Elemental Mean. SUPPORTS.

Elemental Mean reports element-averaged values, removing node extrapolation.
Prediction stated before the test: approximately 475 MPa.

| Display mode | sigma reported | sigma derived from its own epsilon_p | gap |
|---|---|---|---|
| Unaveraged | 551.35 | 475.09 | +76.3 MPa |
| Averaged | 503.49 | 475.04 | +28.5 MPa |
| **Elemental Mean** | **469.24** | 473.19 | **-3.9 MPa** |

Removing extrapolation cuts the gap by 86%. Consistent with the hypothesis.

### Test B — mesh refinement. DOES NOT SUPPORT.

Extrapolation error scales with the stress gradient across a single element, so halving element
size should substantially close the gap. Bore face sizing 2 mm -> 1 mm, e/D = 2.0.

| Bore mesh | Nodes | Elements | sigma reported | sigma derived | gap |
|---|---|---|---|---|---|
| 2 mm | 21,933 | 4,554 | 503.49 | 475.04 | 28.45 MPa |
| 1 mm | 35,848 | 7,677 | 501.03 | 475.25 | **25.78 MPa** |

A 2x refinement closed the gap by **9%**. Fitting `gap ~ h^p` gives **p = 0.14** — effectively no
convergence. Extrapolation error would be expected to fall roughly linearly or quadratically with
element size. **This does not support the hypothesis.**

Both quantities did move slightly toward each other, and nothing diverged, but the effect is far
too weak to be the mechanism.

## 5. Flaw identified in the consistency check itself

The check compares **global maximum** stress against **global maximum** plastic strain.

The yield surface locks the two together **at a point**. It does not require the two global maxima
to lie at the same node once extrapolation and averaging have smoothed each field differently. That
colocation was assumed and never verified.

If the maxima are not colocated, part of the apparent discrepancy is an artefact of the check
rather than a property of the solution. This should have been established before either hypothesis
was tested. Resolving it requires probing both quantities at a single common location rather than
comparing field maxima.

## 6. Conclusion — bounded, not resolved

**True peak von Mises at e/D = 2.0 is bracketed:**

- **Lower bound 469.24 MPa** (Elemental Mean) — under-reports, because elements straddling the
  elastic-plastic boundary average unyielded integration points into the result
- **Upper bound 503.49 MPa** (averaged nodal) — over-reports, by extrapolation overshoot

The material is therefore **barely yielding, roughly 1 to 7 percent above the 469 MPa yield**.
This is consistent with the hand-method bearing margin of +0.216, a comfortable pass, and with the
small deformation of 0.4817 mm.

**Reported peak von Mises is not used quantitatively for e/D >= 1.2 anywhere in this study.**

### What is solid

Refinement confirmed the quantities the sweep actually relies on:

| Quantity | 2 mm | 1 mm | Change |
|---|---|---|---|
| Max total deformation | 0.4817 mm | 0.48147 mm | **0.05%** |
| Force reaction Y | -284,690 N | -284,690 N | **exact** |

**No sweep conclusion changes.** The failure mode map, the crossover at e/D = 1.353, the
zero-margin point at e/D = 1.201, and the elastic scaling law all rest on deformation, plastic
strain magnitude, reaction equilibrium, and closed-form margins. None rests on reported peak
stress.

The mesh convergence study at e/D = 1.5 is retroactively better explained: peak von Mises
oscillated within +/-2% and would not converge monotonically while deformation converged to 0.12%
and reaction was exact. That was the same fragility, observed before its cause was investigated.

## 7. Open, if ever revisited

- [ ] Probe stress and plastic strain at a **single common node** to eliminate the §5 colocation
      confound. This is the test that should have come first.
- [ ] Plastic strain at e/D = 1.5, not captured during the sweep.

Further refinement is not recommended. Test B showed the gap is insensitive to mesh size, so more
elements will not settle it, and the practical answer is already bounded tightly enough that no
conclusion depends on it.

## 8. Method note

The rejected hypothesis in §2 and the unsupported half of §4 are retained in full rather than
deleted. Each was recorded before its test, each test was chosen because it could falsify, and the
outcomes are reported as they came — including the disagreement between Test A and Test B, and
including a flaw in the check that was found only afterwards. Removing any of that would
misrepresent how the bounded conclusion in §6 was reached and would imply more certainty than the
evidence supports.
