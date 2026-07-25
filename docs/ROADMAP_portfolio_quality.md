# AeroFrame-DT — Roadmap to Best-in-Class Portfolio Quality

**Status of this document:** planning / target-setting. Not a substantiation record.
**Claim boundary:** educational / representative / portfolio only. Non-OEM, non-certified.
All numbers `SYNTHETIC_TEST_ONLY`.

---

## 1. Target and honest ceiling

The goal is the strongest version of this project achievable under two fixed constraints:

- **no physical hardware / test of our own**, and
- **no external stress-engineer review**.

Under those constraints the realistic ceiling is **~90 / 100** measured against full-time
entry-level structural / stress roles, including candidates converting from internships. The
final ~5–10 points that reach 95+ are earned by things this project cannot manufacture by
constraint — an independent professional sign-off, or correlation against hardware we tested
ourselves. We are not chasing those points; we are maximising everything below them.

**Breadth is explicitly rejected as a path to score.** Adding more parts (e.g. an MD-11 part
breakdown) does not raise the score against these roles — no scanned job posting rewards part
count. It rewards substantiation depth, hand-calc / FEA agreement, test correlation, and
documentation. Effort goes into depth on AF-DT-1000, not more parts. The MD-11 CAD, if used at
all, appears as a single context render showing where the fitting lives on the airframe.

---

## 2. Ordered work to reach ~90

Each item lists the approximate score movement it is responsible for. Do them in this order.

### 2.1 Close the pylon margin — verify A₁–A₄  (gate, ~72 → ~77)
The rev D margin is PROVISIONAL (see `docs/DECISIONS_AF-DT-1000_revD.md` §6). It hinges on the
transverse lug areas A₁–A₄, currently taken as 1.5 in² by assumption. These must be read off
USAF Fig. 9-7 for the actual section. This is the single input that can still flip the margin
sign, and at 59.04° the transverse allowable governs the interaction. Nothing downstream is
"substantiated" until this is closed.

### 2.2 F12 — correlate to a published lug test  (~77 → ~83, highest single lever)
Model a lug test that is **already published** (no hardware needed on our side), predict its
failure load, and compare to the printed measured value. This is the closest a software-only
project gets to "verified against reality" and is the strongest single visual and credibility
item in the whole project. The predicted-vs-measured plot is the best figure we will produce.

### 2.3 F15 — RCCA / nonconformance package  (~83 → ~86, key differentiator)
Build a realistic nonconformance and run it as a Material Review Board would. A good candidate
defect is drawn from our own history: an under-applied fillet (the `NearestToPointSelector`
defect) or an edge-distance / mis-drill scenario. The package contains:
- defect description and how it was found,
- disposition (use-as-is / rework / scrap) with rationale,
- structured root-cause writeup (8D or DMAIC),
- corrective and preventive action,
- re-analysis showing the margin **with** the defect present.
RCCA / MRB experience is named explicitly in entry-level postings and is rare in student
portfolios. Interns often never own one.

### 2.4 Formal stress report + material allowables basis  (~86 → ~89)
- Package everything in real stress-report format (the deliverable postings name explicitly:
  stress reports, margin-of-safety calculations, supporting compliance documentation).
- Replace the representative Ftu = 71 ksi with a proper A/B-basis allowable and state the
  statistical basis. Allowables rigor is graded.

### 2.5 Visible independent self-checking  (~89 → ~90)
Because there is no external checker, the checking is built in and shown on paper:
- independent-method check on the driving margin (hand calc vs FEA vs a second closed-form
  method — three ways agreeing),
- documented mesh convergence study (3+ points; two points is insufficient),
- uncertainty / sensitivity analysis identifying which inputs actually drive the margin.

---

## 3. Evidence & plot capture checklist

Plots are **evidence that points back to proof, not proof by themselves**. Each plot earns its
place by sitting next to the calculation it confirms, with a stated percent difference. Capture
everything below in a **single Ansys session per configuration** so no re-run is needed later.

Ratio target: a handful of plots, each nailed to a number — not dozens that only look busy.

| # | Plot | What it proves | Pairs with |
|---|---|---|---|
| 1 | Von Mises contour — full part | Overall stress field is sane | Load path narrative |
| 2 | Von Mises contour — zoomed at pin bore | Critical location is where the hand calc predicted | Net-section / bearing hand calc |
| 3 | Bearing stress at pin bore | The margin-driving number | Hand-calc bearing stress (money plot) |
| 4 | Deformation — exaggerated scale | Deflection shape / BCs behave correctly | Expected mode shape |
| 5 | Deformation — TRUE scale | Real magnitude is physical (not a student tell) | Stiffness sanity check |
| 6 | Reaction forces at supports | Load out equals load in | Applied load: 317 840 N (Z) + 529 740 N (X) |
| 7 | Mesh convergence — stress vs element count | Result is not mesh-dependent (reviewers look for this) | Convergence study, 3+ points |
| 8 | Fatigue / life contour (F8/F9) | Analysis went beyond static | Fatigue hand calc / spectrum |
| 9 | Predicted vs measured (F12) | Method predicts reality | Published test value |

Also capture, for the digital thread:
- Abbott / Excel spreadsheet screenshots showing **input → source reference (USAF Fig / NASA TM)
  → output → where the output flows next** — traceability is the proof, not the raw sheet.
- A single results-summary table: location | hand calc | FEA | % diff | margin. One such table
  outweighs ten contour images.

**Mass verification reminder:** the rev D FE model must return mass = 7.65 kg. A mismatch means
the wrong STEP was imported (see `docs/DECISIONS_AF-DT-1000_revD.md` §2).

---

## 4. Immediate next action

When work resumes on the pylon, execute §2 in order: **A₁–A₄ → re-run Ansys on rev D (capture
all §3 plots in one pass) → F12 → F15.** Do not begin F12 before the A₁–A₄ margin is closed;
a provisional margin caps the whole package.
