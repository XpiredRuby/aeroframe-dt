# AeroFrame-DT — Project State

**Last updated: 2026-08-04**
**Repo:** `github.com/XpiredRuby/aeroframe-dt`, branch `main`
**Owner:** Ruby, Texas A&M aerospace senior (GitHub: XpiredRuby)

---

## 1. What this project is

A rigorous static stress substantiation of **one** aircraft part: a forward pylon-to-wingbox
attachment fitting (**AF-DT-1000**) on an MD-11-class aircraft.

The thesis is **depth over breadth on a single fitting**. Scope expansion to more parts was
evaluated twice and rejected both times. The project replicates a full V-model engineering
lifecycle — requirements, load basis, CAD/GD&T, hand analysis, multi-fidelity FEA, damage
tolerance, manufacturing and inspection, digital thread, nonconformance/RCCA — to compensate for
limited internship experience in the aerospace job market.

**Claim boundary, stated in every document:** educational / representative / portfolio only.
Non-OEM, non-certified. Geometry and load case are `SYNTHETIC_TEST_ONLY`; the damage-tolerance
spectrum is `SYNTHETIC_SPECTRUM`; the F20 cost rates are `ASSUMED_COST_BASIS`. **Material
allowables are real**, from MIL-HDBK-5J with page-level citation.

---

## 2. Headline results

| | |
|---|---|
| **Governing margin** | **`MS = +0.156`** — passes |
| Worst-case manufacturing tolerance stack | **+0.133** |
| A-basis-consistent method scatter (99%/95%) | **−0.032** — conservative, see F18 |
| B-basis-consistent method scatter (90%/95%) | +0.052 |
| Independent method cross-check (Ekvall closed form) | +0.053 |
| Governing failure mode | combined bearing / transverse at the lug bore |
| Pin | high-strength steel mandatory, bending governs at 780 MPa |
| Damage tolerance | critical crack 3.07 mm, NDI at 4,500-flight intervals |
| First natural frequency | 1197.2 Hz — **inside the plausible blade-passing band** |
| Buckling | all three eigenvalues negative — no mode under applied load |
| **OPEN finding (F20)** | **allowables are cited from the 2.001–2.500 in plate band, but the part envelope requires ≥6.000 in stock** |

**Margin history — the most important story in the project:**

| Stage | MS | Cause |
|---|---|---|
| Initial hand analysis, thin-lug, assumed Ftu = 71 ksi | +0.710 | — |
| Thick-lug correction, elastic (F7) | +0.165 | `t/D = 1.25` invalidates uniform bearing |
| Real A-basis allowables (MIL-HDBK-5J) | +0.078 | assumed Ftu was 9% optimistic |
| **Elastic-plastic contact measurement (F16)** | **+0.156** | yielding redistributes the bearing peak |

The original number was overstated by **4.6×**. Two corrections removed assumptions that did not
hold; the third replaced a conservative bound with a measurement.

---

## 3. Status

**17 of 18 formal requirements VERIFIED.** `tools/check_traceability.py` passes at
**18 requirements, 41 verification rows**.

**REQ-012 (safe-life fatigue) cannot close and never will** — MIL-HDBK-5J §3.7.6.2 provides no S-N
curves for the T73/T7351 temper. Damage tolerance is the correct route and is complete.
**17/18 is the honest ceiling, not a gap.**

**Project completion: ~98%.** Everything obtainable was done — then F20 opened one new item that
is neither blocked nor solver-dependent: see §5.

### Key geometry (Rev D, frozen)

| Parameter | Value |
|---|---|
| Pin bore diameter `D` | 2.000 in |
| Lug thickness `t` | 2.500 in |
| Lug width `W` | 4.000 in |
| Edge distance `e` | 2.500 in |
| **Derived** | `e/D = 1.25`, `W/D = 2.00`, **`t/D = 1.25`** |
| Overall envelope | 16.000 × 6.000 × 9.000 in — **minimum stock thickness 6.000 in** |
| Mass | 7.65 kg |

**`t/D = 1.25` is the root of most findings** — it invalidated the thin-lug method, drove the pin
bending requirement, and halved the tolerable flaw size.

### Load basis (Rev C)

`Fx = 529,740 N`, `Fz = 317,840 N`, **resultant 617,776 N at 59.04° off the lug axis**,
transverse-dominant. 9g emergency landing per FAR 25.561. Fitting factor 1.15 per FAR 25.625.

---

## 4. Completed work

| Phase | Content |
|---|---|
| Loads | Rev C, axis-mapping error corrected (was 30.96°, actually 59.04°) |
| F5 | Melcon-Hoblit lug analysis + Rev D linear elastic FE, equilibrium 0.006% |
| F6 | Pin bending, thick-lug sensitivity, 780 MPa |
| F7 | Two-body contact FE, elastic `t_eff/t = 0.681`, converged over 3 meshes |
| F9 / F9b | Damage tolerance, `a_c = 3.07 mm`, 4,500-flight interval |
| F10 | Dynamics and buckling, analytical |
| F11 | Geometric optimization |
| F12 | Correlation against 243 published lug tests |
| F13 | Manufacturing, inspection plan, tolerance stack |
| F14 | Digital thread — 59 artifacts, 95 links, 0 audit issues |
| F15 | Nonconformance RCCA, mis-drilled bore, REWORK |
| **F16** | **Elastic-plastic contact, `t_eff/t = 0.7300`** |
| **F17** | **Modal + eigenvalue buckling FE** |
| **F18** | **Ekvall specimen basis — resolves double-counting** |
| **F19** | **Independent method cross-check** |
| **F20** | **Recurring cost trade — buy-to-fly 5.36, raises the material-band finding** |
| FE verification | `reports/FE_VERIFICATION_REPORT.md` — patch, cantilever, plate |

### Recent findings worth knowing

**F16:** `t_eff/t` elastic 0.6809 → elastic-plastic 0.7300. Peak plastic strain 6.46%, which
**exceeds the 6% tabulated elongation** — recorded as *not* a rupture prediction, since it occurs at
a mesh-singular contact edge. Breakeven for clearing the Ekvall band is 0.7513; **we came in at
0.7300, just short.**

**F17:** first mode 1197.2 Hz against an analytical prediction of 2133 Hz — the prediction that it
would come out *lower* was recorded in advance and held. **But 1197 Hz and 1673 Hz both fall inside
the plausible blade-passing band (~1000–2500 Hz)**, so that concern is now sharper, not resolved.
All buckling multipliers negative — no buckling mode under the applied load direction.

**F18:** Ekvall's specimens span `t/D` 0.098–1.316; **our lug at 1.250 is inside**, at 95% of his
thickest. His method has **no thickness term** (`P = D·t·K_BR·F_tu`, `K_BR = f(W/D)`), so the
thick-lug effect is inside his fitted factor and its scatter — **double-counting is real but not
quantifiable** (he reports the range, never the distribution). Also: the 1.19 worst case turned out
to be his **99%/95% one-sided tolerance limit**, which is the definition of A-basis — so it was
always the statistically correct pairing.

**F20 — the one to know:** the first cost analysis in the project found a materials problem, not a
price problem. The Rev D envelope is 16.000 × 6.000 × 9.000 in, so the part cannot be cut from stock
thinner than **6.000 in** — but every allowable comes from the **2.001–2.500 in** band, selected on
`t_lug` rather than on stock thickness. Expected direction **non-conservative**; magnitude unread.
Also: buy-to-fly **5.36**, utilisation **18.6%**, and pocketing 10% of finished mass out at fixed
envelope costs **+0.2%** while shrinking the envelope 10% costs **−6.8%** — F11 optimised the wrong
variable. Cost rates are `ASSUMED_COST_BASIS`, never quoted as sourced.

**F19:** Ekvall's closed-form transverse allowable is **11.5% below** Melcon-Hoblit (230,010 vs
259,875 lb), giving MS +0.053. The ratio 0.885 sits **inside his own 0.85–1.19 band**, so the two
methods agree within the demonstrated scatter of either. **Raised as a finding, not incorporated** —
the released stress report was not silently amended.

---

## 5. Open items

| Item | Blocker | Effect if resolved |
|---|---|---|
| **F20 material band (NOT blocked)** | **needs MIL-HDBK-5J Table 3.7.6.0(b3) read for the band containing 6.000 in** | **fixes or falsifies the released +0.156** |
| Mesh-converge the elastic-plastic ratio | **needs ~40 min Ansys** — the only solver item left | removes the inherited convergence argument |
| AFFDL / TM-X-73305 K-factor curves | needs digitising from figures | replaces the extrapolated bore-position sensitivity; gives exact F15 margin at `e = 1.900` |
| Ekvall Figs 3 and 6 digitised | graphs, no equations | would make F19 a full second independent margin |
| Blade-passing frequency | needs a defined engine + blade count | resolves the most pressing dynamic question |
| Load spectrum with thrust content | no public source exists | replaces the largest uncertainty in damage tolerance |
| Clevis definition (AF-DT-2000) | undefined mating part | fixes pin bending and `t_eff` |
| Single vs redundant load path | design decision | fixes A-basis vs B-basis |
| **REQ-012 safe-life fatigue** | **no S-N data exists for T7351** | **permanently blocked** |

**Bookkeeping: done.** F19 and F20 are both registered in the digital thread (`ANL-F19-CROSSCHECK`,
`ANL-F20-COST`); the counts in `README.md`, `digital_thread/README.md` and
`docs/F14_DIGITAL_THREAD.md` had drifted and were corrected. Cost analysis: **done, F20.**

---

## 6. Working preferences (important)

- **Short, plain words. No yapping.** Low on credits.
- **Claude does all GitHub and software work autonomously.** Never present options — decide using
  good engineering and job-market reasoning, then act.
- **Only ask Ruby for:** Ansys/FEA runs, browser logins, physical file moves.
- **Be honest.** Never guess numbers or citations — verify or say you can't.
- **After each milestone, give % complete of the whole project.**
- **Scope cuts unwelcome.** Don't shrink the project.
- **Any filename Ruby types must be lowercase alphanumeric only** — the Ansys VDI cannot produce
  Shift-modified characters.
- **Binaries cannot be pushed** (.png, .step, .xlsx, .wbpz) — the tool is text-only. SVG works.
  Ruby uploads binaries by hand.
- **When giving Ansys instructions:** one step at a time unless she asks for a block. She often
  routes work through a Claude browser/desktop extension, so self-contained prompts are useful.

### GitHub mechanics

- Use `create_or_update_file` only. **`push_files` returns 403 — never use it.**
- Overwrites need the **git blob SHA** (`git rev-parse HEAD:path`), not the file's SHA-256.
  Getting this wrong wastes a round trip.
- Cloning the repo to the compute node and working locally is far cheaper than repeated API reads.

---

## 7. Tools and sources

| | |
|---|---|
| **FEA** | Ansys Mechanical 2025 R2 + Mechanical APDL, via TAMU VDI (full academic licence) |
| **Critical** | Work on **`C:\Users\vin`**, never `H:` — H: is a 5 GB network quota that caused a mid-solve disk-full crash |
| **Hand calcs** | Abbott Aerospace AA-SM-009-002 / -005 (Melcon-Hoblit per NASA TM-X-73305) |
| **CAD** | Onshape (drawings); CadQuery (parametric, pip-installable on the Claude compute node) |
| **File transport** | Google Drive folder AeroFrame-DT (xpiredruby@gmail.com) → VDI via browser |
| **References** | MIL-HDBK-5J; Ekvall 1986 *J. Aircraft* 23(5) 438–443 (**obtained, read in full**) |

---

## 8. Lessons the project has already paid for

- **Accuracy over speed.** Claude has made documented errors: mis-diagnosing a stress singularity
  twice, mis-assigning load components, building unnecessary geometry revisions B and C, sending
  Ruby into the wrong Workbench restore dialog, mis-diagnosing a mislabeled archive as corrupt, and
  claiming the elastic-plastic run would settle the double-counting question when it could not.
  **Ruby caught several of these. All are recorded in the repo rather than erased.**
- **Failures stay visible.** Four of eight blind predictions failed and are still committed. Two
  benchmark deck bugs are documented with the wrong answers they produced.
- **The axis-mapping error invalidated everything downstream of the load basis** — 24 found by hand
  at the time, 29 in the current graph as the graph has grown. Lock the load axis before anything
  downstream.
- **A back-edge in the evidence graph is not a free way to express a finding.** Linking F20 back to
  the margin closed the loop `MARGIN -> F13 -> F20 -> MARGIN` and hung `audit()`. The engine's cycle
  walk used `UNION ALL`; it now uses `UNION`, reports the cycle, and has a regression test. The
  finding is carried in artifact metadata instead.
- **Cost is set by the envelope, not by the finished mass.** Mass optimisation that leaves the
  bounding box alone buys nothing.
- **Sequencing matters.** The digital thread's forward query correctly predicted that the
  elastic-plastic run would invalidate the whole tolerance scheme — which is why it was run first.
- **Orientation is a stronger design lever than thickness** (~1.1 in margin gain vs ~0.45 in) — and
  on cost it is free, which thickness is not.

---

## 9. PROMPT TO PASTE INTO THE NEW CHAT

Copy everything below the line, and attach this file.

---

I'm Ruby (GitHub: XpiredRuby), Texas A&M aerospace senior. I'm continuing a portfolio project
called AeroFrame-DT. I've attached PROJECT_STATE.md — read it first, it's the full project state.

Quick version: AeroFrame-DT is a rigorous stress substantiation of ONE aircraft part, a forward
pylon-to-wingbox attachment fitting (AF-DT-1000) on an MD-11-class aircraft. Repo is
github.com/XpiredRuby/aeroframe-dt on branch main. The project is ~98% complete: 17 of 18
requirements verified, governing margin MS = +0.156, 20 analysis documents, 41 verification rows.
One OPEN finding (F20): the allowables band cited does not match the plate the part must be cut from.

HOW TO WORK WITH ME

Short, plain words. No yapping. I'm low on credits.

If it's GitHub or software, YOU do it — you have write access via the GitHub connector. Commit with
create_or_update_file (needs the git blob SHA when overwriting; look it up with
`git rev-parse HEAD:path`, don't guess and don't use the SHA-256). push_files returns 403, so use
single-file calls. Cloning the repo to your compute node and working locally is much cheaper than
repeated API reads.

Only ask me for: Ansys/FEA runs, browser logins, physical file moves.

Don't ask me to pick between options. Decide yourself using good engineering and job-market
reasoning.

Be honest. Never guess numbers or citations — verify or say you can't. If you get something wrong,
say so plainly and correct it in the repo rather than quietly fixing it.

After each milestone, give % complete of the whole project.

Scope cuts unwelcome. Don't shrink the project.

Any filename you ask me to type must be lowercase alphanumeric only — my Ansys VDI cannot produce
Shift-modified characters. You cannot push binaries (.png, .step, .xlsx, .wbpz) — the tool is
text-only. SVG works. I upload binaries by hand.

When giving me Ansys instructions, go one step at a time unless I ask for a block.

WHAT I WANT NEXT

Read PROJECT_STATE.md, check the repo to see the current state, then tell me what the
highest-value remaining work is and start on whatever doesn't need me. Stop only when you actually
need something from me.

For reference, what I know is still open:
- One reading task for me: MIL-HDBK-5J Table 3.7.6.0(b3), the 7075-T7351 plate band containing
  6.000 in — F_tu (L/LT/ST), F_ty, F_bru at e/D = 2.0, A basis. This closes the F20 finding.
- One Ansys item: mesh-converge the elastic-plastic contact ratio at the 1.50 mm bore mesh (~40
  min). Removes the last stated limitation in the stress report.
- Everything else is blocked on sources: the AFFDL K-factor curves, Ekvall's Figs 3 and 6, a
  defined engine for blade-passing, a thrust load spectrum, and S-N data for 7075-T7351 that does
  not exist.
- Bookkeeping and cost analysis are done (F19 registered, F20 delivered).
