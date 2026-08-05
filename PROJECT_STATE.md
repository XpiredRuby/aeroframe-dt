# AeroFrame-DT — Project State

**Last updated: 2026-08-05**
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
allowables are real** — but see F21, the cited handbook is cancelled.

---

## 2. Headline results

| | |
|---|---|
| **Governing margin** | **`MS = +0.156`** — passes |
| Worst-case manufacturing tolerance stack | **+0.133** |
| A-basis-consistent method scatter (99%/95%) | **−0.032** — conservative, see F18 |
| Independent method cross-check (Ekvall closed form) | +0.053 |
| Governing failure mode | combined bearing / transverse at the lug bore |
| Pin | high-strength steel mandatory, bending governs at 780 MPa |
| Damage tolerance | critical crack 3.07 mm, NDI at 4,500-flight intervals |
| First natural frequency | 1197.2 Hz — **inside the plausible blade-passing band** |
| **OPEN finding (F20)** | **the allowables band cited is not a band this part can be cut from** |
| **OPEN finding (F21)** | **the allowables are cited from a cancelled handbook** |

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

**REQ-012 (safe-life fatigue) is open and its status is under review.** It was closed as
permanently blocked because MIL-HDBK-5J §3.7.6.2 has no S-N curves for the T7351 temper — **but
that is a statement about a 2003 document.** See §5.

**Project completion: ~92%.**

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
bending requirement, halved the tolerable flaw size, and is the reason F22 rejects composite.

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
| F10 / F17 | Dynamics and buckling, analytical then FE |
| F11 | Geometric optimization |
| F12 / F18 / F19 | Correlation against 243 lug tests, specimen basis, independent method cross-check |
| F13 | Manufacturing, inspection plan, tolerance stack |
| F14 | Digital thread — **62 artifacts, 103 links, 0 audit issues** |
| F15 | Nonconformance RCCA, mis-drilled bore, REWORK |
| F16 | Elastic-plastic contact, `t_eff/t = 0.7300` |
| F20 | Recurring cost trade — buy-to-fly 5.36, raises the material-band finding |
| **F21** | **Allowables governance — the cited handbook is cancelled** |
| **F22** | **Composite trade — retain 7075-T7351** |
| FE verification | `reports/FE_VERIFICATION_REPORT.md` + NASTRAN cross-check decks (not yet run) |

### Recent findings worth knowing

**F21 — the one to know.** Every allowable is cited from **MIL-HDBK-5J, cancelled and superseded by
MMPDS**, and the FAA removed MIL-HDBK-5 from the 14 CFR 25.613 compliance path. 51 substantive
citations across 18 files. **The values are not in question** — 5J and MMPDS-01 were technically
equivalent in 2003 — but the currency of the citation is, and equivalence *today* has not been
checked. It also reopened REQ-012.

**F22.** Retain 7075-T7351. The argument is the project's own: F16 measured the margin nearly
doubling **because the aluminium yielded and redistributed the bearing peak**. A laminate has no
such mechanism, and at `t/D = 1.25` the pin flexure drives load through the thickness into the
matrix-dominated direction. Composite wins on buy-to-fly, mass and corrosion — and still loses.

**F20.** The envelope requires ≥6.000 in stock; the allowables come from the 2.001–2.500 in band.
Expected direction non-conservative, magnitude unread. Buy-to-fly 5.36, utilisation 18.6%.
Pocketing mass out at fixed envelope costs **+0.2%**; shrinking the envelope 10% costs **−6.8%** —
F11 optimised the wrong variable.

**F16.** `t_eff/t` 0.6809 → 0.7300. Peak plastic strain 6.46%, **exceeding tabulated elongation** —
recorded as *not* a rupture prediction, since it occurs at a mesh-singular contact edge. Breakeven
for clearing the Ekvall band is 0.7513; **we came in at 0.7300, just short.**

**F17.** First mode 1197.2 Hz against an analytical 2133 Hz — the prediction that it would come out
*lower* was recorded in advance and held. **But 1197 Hz and 1673 Hz both fall inside the plausible
blade-passing band**, so that concern is sharper, not resolved.

---

## 5. Open items

| Item | Blocker | Effect if resolved |
|---|---|---|
| **MMPDS lookup (NOT blocked)** | **one library session** | **closes F20, confirms or moves the margin, and decides REQ-012** |
| **REQ-012 safe-life fatigue** | **unknown — depends on the MMPDS lookup** | **17/18 → 18/18 if the data exists** |
| Mesh-converge the elastic-plastic ratio | needs ~40 min Ansys | removes the inherited convergence argument |
| Run the NASTRAN cross-check decks | needs a NASTRAN licence | tests four frozen predictions; single-solver risk remains until then |
| AFFDL / TM-X-73305 K-factor curves | needs digitising from figures | exact F15 margin at `e = 1.900 in` |
| Ekvall Figs 3 and 6 digitised | graphs, no equations | would make F19 a full second independent margin |
| Blade-passing frequency | needs a defined engine + blade count | resolves the most pressing dynamic question |
| Load spectrum with thrust content | no public source exists | replaces the largest uncertainty in damage tolerance |
| Clevis definition (AF-DT-2000) | undefined mating part | fixes pin bending and `t_eff` |

**The MMPDS session — four things:**

1. **7075-T7351 plate, the band containing 6.000 in** — `F_tu` (L/LT/ST), `F_ty`, `F_bru` at
   `e/D = 2.0`, A basis. *Closes F20.*
2. **7075-T7351 plate, 2.001–2.500 in band**, current edition. *Confirms or moves `+0.156`.*
   Also note **whether that band still exists with the same boundaries** — if it was resplit, F20's
   finding changes shape.
3. **Does MMPDS contain S-N curves for 7075-T7351?** Yes or no, section number either way.
   *Decides REQ-012.*
4. **MMPDS edition number and date**, for the citation itself.

---

## 6. Working preferences (important)

- **Short, plain words. No yapping.** Low on credits.
- **Claude does all GitHub and software work autonomously.** Never present options — decide using
  good engineering and job-market reasoning, then act.
- **Only ask Ruby for:** Ansys/FEA runs, browser logins, library access, physical file moves.
- **Be honest.** Never guess numbers or citations — verify or say you can't.
- **After each milestone, give % complete of the whole project.**
- **Scope cuts unwelcome.** Don't shrink the project.
- **Any filename Ruby types must be lowercase alphanumeric only** — the Ansys VDI cannot produce
  Shift-modified characters.
- **Binaries cannot be pushed** (.png, .step, .xlsx, .wbpz) — the tool is text-only. SVG works.
- **Do not run two agents against this repo at once.** Parallel writers produced stale-SHA
  collisions and duplicated work on 2026-08-05.

### GitHub mechanics

- Use `create_or_update_file` only. **`push_files` returns 403.**
- Overwrites need the **git blob SHA** (`git rev-parse HEAD:path`), not the file's SHA-256.
- Clone to the compute node and work locally; it is far cheaper than repeated API reads.
- Large regenerated exports (the 36 KB thread JSON) cost real tokens to commit. Batch them.

---

## 7. Tools and sources

| | |
|---|---|
| **FEA** | Ansys Mechanical 2025 R2 + APDL, via TAMU VDI |
| **Critical** | Work on **`C:\Users\vin`**, never `H:` — a 5 GB quota that caused a disk-full crash |
| **Ansys warning** | This project lineage has been corrupted **four times**: 7/29 bad write, 8/02 disk-full crash, 8/04 and 8/05 persisted solve-state locks that greyed out Solve and blocked Clear Generated Data. If it recurs: kill `AnsysWBU.exe`, delete `.lock`, and if that fails restore from a clean parent rather than repairing |
| **Hand calcs** | Abbott Aerospace AA-SM-009-002 / -005 (Melcon-Hoblit per NASA TM-X-73305) |
| **CAD** | Onshape; CadQuery (parametric, pip-installable on the Claude compute node) |
| **References** | **MMPDS (current, needed)**; MIL-HDBK-5J (cancelled, currently cited); Ekvall 1986 |

---

## 8. Lessons the project has already paid for

- **Accuracy over speed.** Claude has made documented errors: mis-diagnosing a stress singularity
  twice, mis-assigning load components, building unnecessary geometry revisions, and claiming the
  elastic-plastic run would settle the double-counting question when it could not. **Ruby caught
  several. All are recorded rather than erased.**
- **Failures stay visible.** Four of eight blind predictions failed and are still committed.
- **Three deck-level defects were found by inspection, not by result** — `NMODIF`, `SECDATA`, and
  `PBEAM` writing `J` into the `I12` field. **All three produce believable numbers**, which is
  exactly why review cannot be skipped after a passing test.
- **A document can invalidate its own count by existing.** F21 reported 58 citations; publishing it
  made the true figure 65. Self-referential measurement needs to be designed out, not patched.
- **The axis-mapping error invalidated everything downstream of the load basis** — 24 by hand then,
  30 in the current graph. Lock the load axis before anything downstream.
- **A back-edge in the evidence graph is not a free way to express a finding.** It closed a cycle
  and hung `audit()`. Fixed, tested, written up.
- **Cost is set by the envelope, not the finished mass.**
- **Sequencing matters.** The thread's forward query correctly predicted that the elastic-plastic
  run would invalidate the tolerance scheme — which is why it was run first.

---

## 9. PROMPT TO PASTE INTO THE NEW CHAT

Copy everything below the line, and attach this file.

---

I'm Ruby (GitHub: XpiredRuby), Texas A&M aerospace senior. I'm continuing a portfolio project
called AeroFrame-DT. I've attached PROJECT_STATE.md — read it first, it's the full project state.

Quick version: AeroFrame-DT is a rigorous stress substantiation of ONE aircraft part, a forward
pylon-to-wingbox attachment fitting (AF-DT-1000) on an MD-11-class aircraft. Repo is
github.com/XpiredRuby/aeroframe-dt on branch main. The project is ~92% complete: 17 of 18
requirements verified, governing margin MS = +0.156, 22 analysis documents, 41 verification rows,
and a hash-verified digital thread of 62 artifacts. Two open findings about the allowables (F20,
F21) and one requirement whose status depends on a library lookup I have not done yet.

HOW TO WORK WITH ME

Short, plain words. No yapping. I'm low on credits.

If it's GitHub or software, YOU do it — you have write access via the GitHub connector. Commit with
create_or_update_file (needs the git blob SHA when overwriting; look it up with
`git rev-parse HEAD:path`). push_files returns 403. Clone the repo to your compute node and work
locally — much cheaper than repeated API reads.

Only ask me for: Ansys/FEA runs, browser logins, library access, physical file moves.

Don't ask me to pick between options. Decide yourself using good engineering and job-market
reasoning.

Be honest. Never guess numbers or citations — verify or say you can't. If you get something wrong,
say so plainly and correct it in the repo rather than quietly fixing it.

After each milestone, give % complete of the whole project.

Scope cuts unwelcome. Don't shrink the project.

Any filename you ask me to type must be lowercase alphanumeric only — my Ansys VDI cannot produce
Shift-modified characters. You cannot push binaries (.png, .step, .xlsx, .wbpz). SVG works.

When giving me Ansys instructions, go one step at a time. Be warned: this project's Ansys files have
been corrupted four separate times, most recently by a persisted solve-state lock that greys out
Solve and blocks Clear Generated Data. If that happens, don't try to repair it — rebuild from a
clean parent.

WHAT I WANT NEXT

Read PROJECT_STATE.md, check the repo, then tell me the highest-value remaining work and start on
whatever doesn't need me.

The one thing gating everything: I need to sit down with MMPDS and pull four things — see §5. Until
I do, REQ-012's status is genuinely unknown and two allowables findings stay open.
