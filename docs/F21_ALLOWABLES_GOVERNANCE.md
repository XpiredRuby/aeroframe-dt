# F21 — Allowables Governance and the MMPDS Transition — AF-DT-1000

**Claim boundary:** educational / representative / portfolio only. Non-OEM, non-certified.

**Every material allowable in this project is cited from a document that was cancelled in 2006.**

This document records that finding, establishes what does and does not follow from it, and defines
what has to be done to close it.

**Tool:** `tools/check_allowables_citations.py` → `results/f21_citation_inventory.csv`

---

## 1. The finding

`MIL-HDBK-5J`, dated 31 January 2003, was the last edition of a handbook lineage that began as
ANC-5 in 1937. It was **cancelled** — by a notice issued in 2004 and restated in 2006; sources
differ on which date to treat as the operative one, and this document does not need to resolve
that — and superseded by the **MMPDS Handbook** — *Metallic Materials Properties Development and
Standardization* — which is maintained by Battelle under FAA oversight and reissued periodically.

The regulatory consequence matters more than the bibliographic one. **The specific reference to
MIL-HDBK-5 was removed from 14 CFR 23.613 and 25.613** as a means of showing compliance. The FAA
accepts MMPDS as the source for metallic design allowables and **encourages the latest revision for
the certification of new products**.

This project cites MIL-HDBK-5J **51 times across 18 files**, invoking six distinct locators:

| Locator | Citations | What it supplies |
|---|---|---|
| Table 3.7.6.0(b3) | 15 | **the governing allowables** — 7075-T7351 plate, 2.001–2.500 in band |
| Section 3.7.6.2 | 4 | the S-N fatigue section — **the REQ-012 blocker** |
| Table 3.1.2.1.6 | 3 | `K_Ic`, information only |
| Table 3.7.6.0(b1) | 1 | 7075-T7351 plate, 0.500–1.000 in band — F12 correlation basis |
| Table 3.1.2.3.1(b) | 1 | short-transverse property and SCC guidance |
| Figure 3.7.6.2.9(b) | 1 | `da/dN` crack growth data for F9 |

## 2. What does *not* follow from this

**The margin does not move.** MMPDS-01 and MIL-HDBK-5J were published as **technically equivalent
documents** for the 2003 transition year — the handover was a change of custodian and name, not of
data. Every value this project took from 5J was, on the day it was published, also an MMPDS value.

So this is **not** a finding in the same class as F20. F20 identified a physical mismatch between the
plate the part must be cut from and the band the allowables were taken from, and that one can move
the number. This one is about **currency of source**, and its consequence is to the credibility of
the report rather than to its arithmetic.

Both are real, and they are independent. It is possible for the values to be right, the band to be
wrong, and the document to be cancelled, all at once — which is the current state.

## 3. What does follow

**Three things.**

**3.1 The citations must be restated.** A substantiation report that presents itself as certification
work cannot rest its allowables on a document the regulator has removed from the compliance path.
The fix is a restatement, not a re-analysis: each locator is mapped to its MMPDS equivalent and the
values re-read from the current edition to confirm they have not been revised in twenty years of
subsequent coordination meetings.

**3.2 The values must be re-confirmed, not assumed.** Equivalence held in 2003. It does not
automatically hold now. MMPDS has been revised annually since, and revisions exist precisely because
values change as data accumulates. **The 2003 equivalence licenses the claim that the numbers were
right when taken; it does not license the claim that they are current.** Anyone reading `+0.156`
is entitled to know which edition it rests on.

**3.3 REQ-012 has to be reopened as a question.** The safe-life fatigue requirement is closed as
*permanently blocked* on the grounds that MIL-HDBK-5J Section 3.7.6.2 contains no S-N curves for the
T7351 temper. **That statement is about a 2003 document.** MMPDS has accumulated two decades of
submissions since. Whether it now contains S-N data for 7075-T7351 is unknown to this project and
**must not be assumed in either direction**.

Both outcomes are worth having:

- **If MMPDS has the data** — REQ-012 unblocks, safe-life fatigue can be built against the F9b
  spectrum, and the verified count goes from 17/18 to **18/18**.
- **If it does not** — the blocker is restated against the *current* handbook rather than a cancelled
  one, which is a considerably stronger statement of the same limitation.

The present wording claims more than the evidence supports. Until the current handbook has been
checked, the honest form is: *no S-N curves for this temper were found in MIL-HDBK-5J; the current
handbook has not been searched.*

## 4. Status of the mapping

| | |
|---|---|
| Substantive citations inventoried | **51** across 18 files |
| Self-referential (this document and the tool) | 14, counted separately |
| Tied to a specific locator | **25** |
| MMPDS equivalent confirmed | **0** |
| MMPDS equivalent to verify | **51** |

**The first published version of this document got this count wrong, and got it wrong by existing.**
It reported 58 citations across 19 files — a figure taken before the document itself was committed.
Publishing it added seven more citations, and the inventory tool added seven of its own, so the
total moved to 65 the moment the finding was written down. The tool now separates files that are
*about* the citation problem from files that are *instances* of it. Counting a governance document
as evidence of the defect it documents is a small error, but it is the same class of error as
citing a cancelled handbook: **a number that looks sourced and is not.**

**No MMPDS locator appears anywhere in this document or in the inventory tool, and none will until
the handbook has been opened.** MMPDS largely preserves the MIL-HDBK-5 numbering conventions, which
makes it tempting to write the mapping by inference. That temptation is the reason for the rule:
an inferred citation is indistinguishable in print from a verified one, and this project's entire
value rests on that distinction holding.

`tools/check_allowables_citations.py` reports every entry as `TO_VERIFY` and is written so that the
status can only advance by editing the locator registry — that is, by someone having looked.

## 5. Open — needs Ruby

One library session. MMPDS is available through university and AIAA subscriptions.

1. **7075-T7351 plate, the band containing 6.000 in** — `F_tu` (L, LT, ST), `F_ty`, `F_bru` at
   `e/D = 2.0`, A basis. *Closes F20.*
2. **7075-T7351 plate, 2.001–2.500 in band** — the same properties at the current edition.
   *Confirms or moves the released margin.*
3. **Does MMPDS contain S-N curves for 7075-T7351?** Yes or no, with the section number recorded
   either way. *Decides REQ-012.*
4. **The MMPDS edition number and date**, for the citation itself.

Items 1 and 3 are the ones that can change the project's results. Item 2 is the one that confirms
they have not already changed underneath it.

## 6. Limitations

- The 2003 equivalence is documented in the transition notices themselves. **Equivalence at any
  later date is not claimed and has not been checked.**
- This document establishes that the citations are to a cancelled source. It does **not** establish
  that any specific value is wrong. No value is withdrawn.
- The inventory tool is a text scan. It finds citations that name the handbook; it cannot find a
  value that was taken from the handbook and then quoted without attribution.
- MMPDS is a fee-based document. If access cannot be obtained, the correct disposition is to state
  the limitation explicitly rather than to continue citing a cancelled handbook silently.
