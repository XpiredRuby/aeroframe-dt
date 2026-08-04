# F20 — Recurring Cost Trade and Raw Stock Envelope — AF-DT-1000

**Claim boundary:** educational / representative / portfolio only. Non-OEM, non-certified.

Every trade in this project so far has been decided on **mass and margin**. F11 optimised the
geometry on exactly those two. Nothing has ever been costed. This document closes that gap — and
the first thing the cost model needed, the size of the raw billet, turned out to raise a question
about the **material allowables**, not about the price.

**Tool:** `tools/run_f20_cost_model.py` → `results/f20_cost_model.json`,
`results/f20_cost_breakdown.csv`

---

## 0. Two classes of number in this document

| Class | What it covers | Trust |
|---|---|---|
| **DERIVED** | envelope, part volume, buy-to-fly, removed volume, machined area | follows from frozen Rev D parameters; checkable by re-running the script |
| **ASSUMED_COST_BASIS** | every currency rate, cutting rate and inspection time | **no public source was available.** Declared as low/nominal/high and reported as a range |

No rate below is a quotation and none should be cited as one. **Every conclusion drawn in §3 and §4
is one that survives the full assumed range**, because it depends on a ratio rather than on an
absolute rate. The dollar figures in §2 are illustrative only.

---

## 1. The finding that matters — DERIVED

The Rev D solid has a bounding envelope of

    16.000 (X) x 6.000 (Y) x 9.000 (Z) in

so the **smallest dimension of the part is 6.000 in**. A monolithic machined part cannot be cut
from stock thinner than its own smallest bounding dimension. The minimum plate thickness this part
can be made from is therefore **6.000 in**.

**Every allowable in this project is taken from the 2.001–2.500 in plate thickness band.**

> MIL-HDBK-5J Table 3.7.6.0(b3) p.3-373, 7075-T7351 plate, band **2.001–2.500 in** — cited in
> `docs/STRESS_REPORT_AF-DT-1000.md` §5, `docs/MARGIN_SUMMARY.md` §3, `docs/PMI_GDT_DEFINITION.md`,
> and enforced as an incoming-inspection attribute (`AFDT-ATTR-002`) by
> `docs/F13_MANUFACTURING_INSPECTION.md` operation 010.

The band was selected because `t_lug = 2.500 in` sits at the top of it. **That is the wrong
selection rule.** The handbook tabulates by the thickness of the *mill product the part is cut
from*, not by the local thickness of the feature being checked. F13 operation 010 states the
consequence itself: a plate outside the band has different A-basis values and voids the margin.
The routing calls up a plate the part cannot physically be made from.

### 1.1 Which way the error goes

MIL-HDBK-5J bands 7xxx plate by thickness because quench rate falls as section thickness rises, so
strength falls with it — the same mechanism `docs/F18_EKVALL_SPECIMEN_BASIS.md` §6 already invokes.
**The expected direction is that the allowables for 6.000 in plate are lower than those used**,
which makes the released margin **non-conservative**.

**The magnitude is not stated here because it has not been read.** `F_tu`, `F_ty` and `F_bru` for
the band containing 6.000 in have to come off the table. Guessing them would be worse than leaving
the gap open. **This is an action for Ruby — see §5.**

### 1.2 Three ways out, and which to check first

| Option | Effect | Cost effect |
|---|---|---|
| **A. Re-select the allowables for the 6.000 in band** and re-run the margin | keeps geometry; margin drops by an unknown amount from +0.156 | none |
| **B. Split the flange from the blade** so no piece exceeds 2.500 in min dimension | keeps the allowables; introduces a joint, fasteners, and a new failure mode in the primary load path | higher |
| **C. Change product form to a hand or die forging** | realistic for a pylon fitting; grain flow follows the load path | different allowables table entirely, high non-recurring tooling |

**A is the check to run first**, because it is the only one that costs nothing and it determines
whether B or C is even needed. If the margin stays positive under the correct band, the finding is
closed by a citation change. If it does not, the geometry is not sized.

---

## 2. Cost model — ASSUMED_COST_BASIS

Recurring cost per part, lot of 25, across the full assumed rate range:

| Rate case | Total | Material | Machining | Inspection |
|---|---|---|---|---|
| low | $831 | 44% | 53% | 6% |
| **nominal** | **$1,066** | **60%** | **31%** | **13%** |
| high | $1,748 | 62% | 19% | 22% |

Cost elements: plate purchase, scrap credit on chips, rough removal at a volumetric removal rate,
finish machining on the finished surface area, per-lot setup amortised, and inspection built from
the **10 characteristics of the F13 Rev D inspection plan** plus penetrant and the 100% bore check.

**Material dominates at nominal and high rates.** That is a direct consequence of §3.

---

## 3. Buy-to-fly — DERIVED

| | |
|---|---|
| Billet (envelope + 0.060 in rough stock per face, per F13 op 030) | 899.8 in³ |
| Finished part | 167.75 in³ |
| **Buy-to-fly** | **5.36** |
| **Material utilisation** | **18.6%** |

**Over 80% of the purchased plate becomes chips.** The part is a thin blade standing on a long flat
flange, so its bounding box is mostly air.

*Consistency check:* the prismatic decomposition gives 7.69 kg against the 7.65 kg reported by the
CadQuery solid — 0.5% high, the difference being the blend fillets, which the decomposition ignores.
The CAD value governs; the cost model uses the prismatic volume only for material accounting, where
0.5% is far inside the assumed rate spread.

---

## 4. What F11 optimised, and what it should have optimised

F11 minimised **finished mass**. The cost model answers the question F11 never asked: does removing
finished mass remove cost? Both cases below remove the same 10% of finished mass, at nominal rates,
lot of 25.

| Change | Cost |
|---|---|
| Pocket 10% of the finished mass out of the part, envelope unchanged | **+0.2%** |
| Reduce the envelope height 10%, removing the same mass | **−6.8%** |

**Pocketing mass out is cost-neutral to slightly cost-negative** — the billet is unchanged, so the
same plate is bought and more of it is machined away. **Only shrinking the envelope removes cost**,
because the envelope is what is purchased.

This sharpens a lesson the project already recorded. **Orientation was found to be the stronger
design lever (~1.1 in of margin) against a thickness increase (~0.45 in).** On cost the gap is
wider still: reorienting the lug changes no dimension of the billet and is therefore **free**, while
the Rev D thickness increases — `t_lug` 1.500 → 2.500 in and `g_y` 2.000 → 4.000 in — grew the
envelope and were paid for in plate. **Orientation wins on margin and on cost simultaneously.**

### 4.1 The inspection burden is real but not the driver

Inspection is 6–22% of unit cost depending on rates. The 100% bore check is not free, but it is not
what makes this part expensive. Material is. **The F13 conclusion that bore position dominates the
tolerance stack stands; it simply is not the cost driver, and those are different questions.**

---

## 5. Open — needs Ruby

**Read MIL-HDBK-5J Table 3.7.6.0(b3) for the 7075-T7351 plate thickness band containing 6.000 in**
and record `F_tu` (L, LT, ST), `F_ty` and `F_bru` at `e/D = 2.0`, A basis. That is the one input
needed to close §1. Everything else in this document is already computed.

Until it is read, the correct status of the released margin is: **+0.156 on a stated plate band the
part cannot be made from.** The number is not withdrawn, and it is not defended either.

---

## 6. Limitations

- Every rate is an assumption, not a quotation. Absolute dollars are illustrative.
- Non-recurring cost — tooling, fixtures, programming, first-article — is not modelled. At a lot of
  25 it would not be small.
- The machining model is volumetric. It has no toolpath, no tool changes, no fixturing plan and no
  allowance for the deep, narrow pocket either side of the blade, which is the hardest feature to
  cut and is under-costed here.
- Scrap credit assumes segregated, uncontaminated aluminium chips.
- No yield or rework loss is included, although `docs/F15_NONCONFORMANCE_RCCA_AF-DT-1000.md`
  documents exactly the kind of bore-position escape that would drive one.
- §1 identifies the inconsistency and its expected direction. **It does not quantify it.**
