# F17 — Modal and Buckling FE — AF-DT-1000 Rev D

**Closes AFDT-REQ-014.** Completes the FE half of `F10_DYNAMICS_BUCKLING.md`, whose analytical half
was recorded as `VERIFIED_ANALYTICAL_ONLY`. Executed 2026-08-03.

**Claim boundary:** educational / representative / portfolio only. Non-OEM, non-certified.

---

## 1. Headline

**The F10 prediction held, and the consequence is worse than F10 estimated.**

    F10 analytical first mode:  2133 Hz
    F17 FE first mode:          1197.2 Hz   (44% lower)

F10 predicted the analytical value would be **high**, because the cantilever idealisation ignores
lug-head tip mass and treats the flange as rigid. It was, by 44%. The prediction is confirmed in
direction and now quantified in magnitude.

But F10 also flagged blade-passing separation as unresolved at 2133 Hz. **At 1197 Hz that concern
is sharper, not resolved** — see §2.2.

**Buckling is not a credible failure mode**, and the FE result is stronger than the hand
calculation: all three extracted load multipliers are **negative**, meaning no buckling mode exists
under the applied load direction at all.

## 2. Modal analysis

**Setup.** Free vibration, no prestress. Rev D geometry, 119,408 nodes / 69,551 elements,
7075-T7351, fixed support on the flange underside — the same named selection the F5 static run uses.

| Mode | Frequency (Hz) |
|---|---|
| **1** | **1197.2** |
| 2 | 1672.7 |
| 3 | 3130.0 |
| 4 | 5002.1 |
| 5 | 5887.4 |
| 6 | 6037.3 |

### 2.1 Against the analytical estimate

    f1 analytical (cantilever idealisation)  = 2133 Hz
    f1 FE                                    = 1197.2 Hz
    ratio                                    = 0.561

F10 §57 stated: *"The true first mode is below 2133 Hz."* It is. The 44% shortfall is the combined
cost of two idealisations F10 named in advance — neglected tip mass at the lug head, and an assumed
rigid flange. Neither was quantified at the time; together they are worth a factor of 1.78 in
frequency.

**This is a recorded prediction that held**, in the same register as the F12 blind predictions and
the B-002 `SECDATA` prediction in the FE verification report.

### 2.2 Shaft-order and blade-passing separation

**Shaft order remains comfortably clear.** Turbofan N1 runs roughly 50–100 Hz, N2 roughly
200–300 Hz. At 1197 Hz the first mode is still four to twenty times above both.

**Blade passing is now a live concern rather than an open question.** Blade-passing frequency is
`N1 × blade count`; for a large fan at 50–100 Hz N1 with 20–25 blades that is roughly
**1000–2500 Hz**.

> At 2133 Hz F10 wrote that separation was "not established". At **1197.2 Hz the first mode sits
> inside the lower part of that band**, and the second mode at 1672.7 Hz sits inside it as well.

**This is a finding, not a closure.** The correct response is not to declare it acceptable but to
record that a forced-response or harmonic analysis against an actual engine's BPF is required, and
that neither the engine nor its blade count is defined in this synthetic project. Two modes falling
inside a plausible excitation band is exactly the result that should not be rounded off.

`F10_DYNAMICS_BUCKLING.md` open item 2 — blade-passing separation — **stays open, and is now better
characterised and more concerning than when it was written.**

### 2.3 What the mode shapes are

Not recorded. The six frequencies were extracted; individual mode shapes were not classified as
bending, torsion or lug-head modes. That classification would be needed for any forced-response
work and is a stated gap.

## 3. Eigenvalue buckling

**Setup.** Prestressed by the F5 linear static solution — `Fx = 529,740 N`, `Fz = 317,840 N` on the
bore, flange fixed. Three modes extracted.

| Mode | Load multiplier |
|---|---|
| 1 | −51.814 |
| 2 | −51.620 |
| 3 | **−25.068** |

### 3.1 All three are negative — what that means

A negative load multiplier means the structure buckles only when the applied load is **reversed**.
Under the design load direction, **no buckling mode was found within the three extracted.**

The governing case is the one of smallest magnitude, **|λ| = 25.068** — that is, buckling would
require reversing the applied load and multiplying it by 25.

Ansys sorts these algebraically, so mode 3 rather than mode 1 is the critical one. Modes 1 and 2 at
−51.814 and −51.620 are a near-degenerate pair, consistent with a symmetric blade geometry having
two closely spaced buckling shapes.

### 3.2 Against the analytical estimate — not directly comparable

F10 computed an Euler column result:

    P_cr = 23.5e6 N,  MS_buckling = 23.5e6/529,740 - 1 = +43.4   (lambda = 44.4)

**This and the FE value are different quantities.** F10 treated the blade as a column in
compression under the axial component. The FE run applies the real combined bearing load, and finds
the structure is not in a compression state that buckles at all — the critical eigenvalue is in
reversal.

Comparing 25.07 against 44.4 would be comparing a reversed-load 3D eigenvalue against a
forward-load 1D column estimate. **They are not the same number and are not reported as agreeing.**

What both establish, independently, is the same engineering conclusion: at `L/r = 6.9` this member
is far too stocky for buckling to compete with yielding and bearing. F10's conclusion stands; the
FE result reaches it by a different and more complete route.

### 3.3 Linear eigenvalue buckling is an upper bound

Eigenvalue buckling assumes perfect geometry, no imperfections, and linear pre-buckling behaviour.
Real structures buckle below the eigenvalue. That caveat is irrelevant at a factor of 25 in the
wrong direction, but it should not be dropped from the record.

## 4. Limitations

1. **Mode shapes not classified** — §2.3.
2. **Blade-passing separation not resolved**, and now shows two modes inside a plausible excitation
   band — §2.2. No forced-response analysis was performed.
3. **No damping** in the modal analysis. Undamped natural frequencies only.
4. **Buckling is linear eigenvalue**, not nonlinear collapse — §3.3.
5. **Only three buckling modes** extracted. A forward-direction mode could exist beyond mode 3;
   what is established is that none appears among the first three.
6. **The modal mesh is the F5 mesh** (119,408 nodes), not independently converged for frequency.
   Modal convergence generally requires less refinement than stress, but no mesh study was run.

## 5. Provenance

| | |
|---|---|
| Solver | Ansys Mechanical 2025 R2 |
| Project | `modalbuckling`, restored from the Rev D linear elastic archive |
| Mesh | 119,408 nodes / 69,551 elements |
| Modal | 6 modes, no prestress, flange fixed, 11 s elapsed |
| Buckling | 3 modes, prestressed by the F5 static solution, 44 s elapsed |
| Executed | 2026-08-03 |
| Errors | 0 |

**Setup note.** The modal system was created by dropping onto the static system's `Model` cell,
which Workbench links as a **pre-stressed** modal by default. That link was removed so the modal is
free-vibration, matching what F10's analytical estimate describes. The buckling system's prestress
link was retained, because eigenvalue buckling requires it. A `Fixed Support` was added to the
modal environment explicitly — boundary conditions do not inherit from the static environment, and
without it the analysis would have returned six rigid-body modes near 0 Hz.
