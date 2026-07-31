# Resolution of Three Open Items

Addresses the three items blocking closure of `STRESS_REPORT_AF-DT-1000.md` §12:
the Ekvall double-counting question, the clevis definition, and the load spectrum.

**Two are resolved. One is bounded and its resolution path identified. One remains genuinely open,
with the correct reference now named.**

**Claim boundary:** educational / representative / portfolio only. Non-OEM, non-certified.

---

## 1. Ekvall double-counting — RESOLVED AS BOUNDED, with a decisive test identified

### The question

`MARGIN_SUMMARY.md` §5 reports the margin under Ekvall's worst-case method scatter as **-0.094**,
with the caveat that this may double-count: if Ekvall's 243 test specimens included thick lugs, the
thick-lug effect is already inside his measured scatter, and applying our separately measured
correction on top penalises the same physics twice.

The paper itself could not be obtained. **The question is resolvable without it.**

### The argument

Our measured thick-lug knockdown on allowable load is

    t_eff / t = 0.681

If a lug at `t/D = 1.25` had been in Ekvall's specimen set, the thin-lug method would have
over-predicted its strength by

    1 / 0.681 = 1.47

and that specimen would appear in his data at `predicted/test ~ 1.47`.

**Ekvall's reported maximum is 1.19**, corresponding to a knockdown of `1/1.19 = 0.840`.

**Our measured knockdown of 0.681 is 23% more severe than his entire worst observed case.**

### Therefore, exactly one of two things is true

**(a) His specimens were thinner than ours.** No lug in his set experienced a knockdown as severe as
0.681, so the thick-lug effect at `t/D = 1.25` is **not** represented in his band. The two effects are
independent, **stacking is legitimate, and the worst case of -0.094 stands.**

**(b) Our elastic knockdown overstates the real effect.** `F7_CONTACT_THICK_LUG.md` already records
0.681 as a **lower bound** — both contact runs are linear elastic, and yielding at the bore would
flatten the pressure peak and raise `t_eff`. If the true elastic-plastic value is milder than 0.840,
his band could contain it, **the effects overlap, and no stack should be applied.**

### The threshold is sharp and testable

    t_eff / t  <  0.840   ->  effects independent, stacking legitimate, worst case -0.094
    t_eff / t  >= 0.840   ->  effects overlap, stacking double-counts, worst case +0.078

**The elastic-plastic contact run already listed as an open item is the decisive test.** It was
previously justified only as "tightening the lower bound"; it now also settles this question. That
raises its priority.

### Reported position

**Worst case is bounded in `[-0.094, +0.078]`.** The best estimate of **+0.078** is unaffected —
this concerns only how the method-scatter band should be applied on top of it.

This is a materially better answer than the previous "unresolvable without the paper", and it was
obtained from the published abstract figures alone.

---

## 2. Clevis definition — DECIDED

The mating fitting AF-DT-2000 was undefined, leaving pin bending and `t_eff` resting on an
unjustified assumption. **Now defined by design decision:**

| Parameter | Value | Basis |
|---|---|---|
| Clevis ear thickness `t2` | **1.250 in** (`= t1/2`) | balanced bearing, see below |
| Gap each side `g` | **0.030 in** | representative clearance |
| Configuration | symmetric double-shear clevis | standard lug-clevis joint |

### Why `t2 = t1/2` and not something else

Each clevis ear carries `P/2`. Equal bearing stress in the lug and in each ear requires

    (P/2) / (D * t2)  =  P / (D * t1)      ->      t2 = t1 / 2

So `t2 = t1/2` is the **minimum ear thickness that does not make the clevis more highly loaded in
bearing than the lug**. Anything thinner makes the clevis critical; anything thicker is wasted
material that also **increases pin bending**, because the pin moment arm is

    arm = t1/4 + g + t2/2

`F6_PIN_BENDING_THICK_LUG.md` quantifies this: ears as thick as the lug raise pin bending stress by
**49%**. So `t2 = t1/2` simultaneously balances bearing and minimises the pin moment arm. It is the
correct choice, not merely a convenient one.

**This is what F6 and F7 already assumed.** The decision does not change any number in the project —
it converts a floating assumption into a stated, justified design choice.

### Consequence

The pin bending result of **780 MPa** and the requirement for a **high-strength steel pin** are now
resting on a defined clevis rather than an assumed one. The `t_eff/t = 0.681` measurement likewise
used this geometry.

---

## 3. Load spectrum — STILL OPEN, correct reference identified

### What was searched for

A standardised, citable load sequence applicable to a pylon-to-wingbox attachment fitting, to
replace the constructed GAG fractions in `F9b_SPECTRUM_AND_INTERVAL.md`.

### What exists

**TWIST** (Transport WIng STandard load programme) is the recognised reference for transport
aircraft fatigue spectra at preliminary design. It comprises 4,000 flights and 4,000 landings,
characterised by a mean flight stress `Smf`, with gust loading at ten amplitude levels, Level I
highest at `+/-1.6 Smf`. **MINITWIST** is a shortened form that omits high-frequency low-amplitude
cycles and consequently **overestimates fatigue life**.

### Why it does not solve the problem

**TWIST describes wing-root bending moment.** A pylon attachment fitting is not loaded that way:

1. **The vertical component does track `nz`**, which is what a gust and manoeuvre spectrum
   describes, so TWIST's gust content is relevant to that part of the load.
2. **The longitudinal component is thrust-driven** — takeoff, climb, cruise, reverse. **TWIST
   contains no thrust content at all.** For this fitting the transverse term governs the margin, so
   the missing part is the important one.
3. **The full amplitude-versus-occurrence table is required** to build a spectrum, and only the
   Level I anchor (`+/-1.6 Smf`) is available from secondary sources.

### Position

**The constructed spectrum in `F9b_SPECTRUM_AND_INTERVAL.md` stands**, clearly labelled
`SYNTHETIC_SPECTRUM`, with its factor-9.4 sensitivity documented.

**What has improved:** the correct reference is now named, its structure understood, and the reason
it is insufficient stated precisely. A future spectrum should take gust and manoeuvre content from a
TWIST-type source and add a separate thrust-cycle block, which TWIST cannot supply.

### To close this item

1. Obtain the full TWIST level table (ten amplitude levels with occurrence counts), or
2. Obtain an engine-mount or pylon load survey, which would supply the thrust content directly

Item 2 is what actually governs here.

---

## 4. Summary

| Item | Status |
|---|---|
| Ekvall double-counting | **Bounded** to `[-0.094, +0.078]`; elastic-plastic run is the decisive test |
| Clevis definition | **Decided** — `t2 = t1/2 = 1.250 in`, gap 0.030 in, justified by balanced bearing |
| Load spectrum | **Open** — TWIST identified but not applicable; thrust content is the gap |

**No margin changes.** The governing result remains **`MS = +0.078`**.

The elastic-plastic contact run is now the single highest-value remaining analysis: it would tighten
the lower bound on the margin **and** settle the double-counting question in §1.
