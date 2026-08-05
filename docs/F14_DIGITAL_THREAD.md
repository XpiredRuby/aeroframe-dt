# F14 — Digital Thread — AF-DT-1000 Rev D

**Supports AFDT-REQ-016.** A populated, hash-verified evidence graph over the actual repository,
plus two impact analyses run on it.

**Claim boundary:** educational / representative / portfolio only. Non-OEM, non-certified.

**Build:** `python tools/build_f14_thread.py`
**Outputs:** `digital_thread/thread_AF-DT-1000_revD.json`, `.dot`, `digital_thread/impact_analysis.json`
**Engine:** `src/aeroframe_dt/digital_thread.py` (SQLite, recursive descendant query)

---

## 1. What exists now that did not before

`AFDT-REQ-016` was already closed by the engine and a generic synthetic graph. **The engine was
never pointed at this project.** F14 populates it with the real thing:

    59 artifacts, 95 links, 0 audit issues

Every artifact backed by a file carries the **SHA-256 of that file computed at build time**, not a
recorded string. Re-running the build after any edit changes the hash. The graph is regenerable
from the repository and cannot silently drift from it.

Artifact kinds: `source`, `requirement`, `load_case`, `geometry`, `parameter_set`, `cad_script`,
`pmi_definition`, `pmi_characteristic`, `analysis`, `margin`, `inspection_plan`, `nonconformance`,
`report`.

The 18 requirement nodes are read from `requirements/requirements.csv` and the 10 PMI
characteristics from `inspection_quality/inspection_plan_AF-DT-1000_revD.csv`, so the graph cannot
disagree with those files — it is generated from them.

## 2. Modelling decision: one node per artifact, not per revision

The load basis is a **single node `LOAD-AF-DT-1000` carrying a revision**, not three nodes A/B/C.
Same for geometry.

This is not cosmetic. `revise_artifact()` only means something if the identity of the thing being
revised persists across the revision. Modelling each revision as its own node would make the
history a chain of unrelated objects and would make "what did this change break" unanswerable —
which is the only question the graph exists to answer.

The same principle handles supersession. When F16 replaced F7's elastic contact measurement, F7 was
**not** deleted or overwritten — it remains a node, linked to F16 by a `superseded_by` relation.
The elastic result is still evidence; it is just no longer the governing one. F18 is linked to the
same F7 node by `double_count_assessed_by`, because it assesses that correction against the source
test data rather than replacing it.

## 3. Impact analysis A — historical replay

**The test:** register the graph as it stood when the load basis was at revision B, then apply the
real correction — the lug-axis mapping error, where 30.96° had been measured from aircraft X rather
than from the lug axis, and the correct 59.04° is transverse-dominant. Compare what the graph
flags against the rework that actually happened.

**Result: 29 artifacts marked STALE.**

| Group | Flagged |
|---|---|
| The load basis itself | LOAD-AF-DT-1000 |
| Analyses | F5 FE, F6 pin, F7 contact, F9 DT, F9b spectrum, F10 dynamics, F11 optimisation, F13 stack, F16 elastic-plastic, F17 modal/buckling, F18 Ekvall basis, F19 method cross-check, F20 cost trade |
| Released | MARGIN-AF-DT-1000, PMI-AF-DT-1000, INSP-PLAN, NCR-F15-001, RPT-STRESS |
| PMI characteristics | all 10 |

**This matches what actually happened.** Every rev B margin was voided by that correction. The
graph, given only the dependency structure, reproduces the blast radius of a rework cycle that was
discovered by hand.

*The count has grown with the project — 24 when the rework was worked out by hand, 29 now — because
the graph has more nodes downstream of the load basis than it had then. The set, not the number, is
what reproduces.*

### 3.1 Where it over-flags — stated, not hidden

**`ANL-F10-DYNAMICS` should not be fully stale.** F10 covers two things: a modal analysis, which
does not take an applied load and is therefore unaffected by a load revision, and an eigenvalue
buckling assessment, which does. The graph flags the whole document because the document is one
node.

**F17 inherits the same problem and demonstrates it more sharply.** Its modal half is genuinely
load-independent — F17 solved it with the prestress link deliberately removed — while its buckling
half is prestressed by the static solution and would genuinely go stale. One node, two answers.

This is a real limitation and it generalises: **invalidation here is transitive and unconditional.
The graph over-flags rather than under-flags.** For a configuration-control tool that is the right
direction to be wrong in, but a reviewer should know that a STALE flag means "re-examine", not
"re-run".

## 4. Impact analysis B — forward query on a contact revision

**The question:** if the contact measurement changes again, what does it invalidate?

**Result: 21 artifacts, including all 10 PMI characteristics, the inspection plan, the F13
tolerance stack, the NCR assessment and the stress report.**

**This is a sequencing finding, not a bookkeeping one**, and it was acted on. Before F16 was run,
this query showed that a new contact result would move the **tolerance scheme** as well as the
margin — because `PMI_GDT_DEFINITION.md` derives every tolerance from margin sensitivity and `F13`
stacks those tolerances back onto the margin.

**That is why the elastic-plastic run was executed before any further downstream work was treated
as final.** The prediction held: F16 moved the margin from +0.078 to +0.156, and the F13 stack was
re-propagated at the new operating point.

## 5. Audit

`EvidenceGraph.audit()` checks for dangling link endpoints and dependency cycles. **Zero issues on
the released graph.** The build script exits non-zero on any audit issue, or if any artifact
declares a file that does not exist — so a deleted or renamed file breaks the build rather than
producing a graph with a hole in it.

### 5.1 The mechanism has been exercised on real drift

On 2026-08-03 the stress report was reissued at Rev E **after** a graph build. The next build
flagged exactly one node, `RPT-STRESS-AF-DT-1000`, with a changed hash — one node predicted, one
node found. The same happened again when Rev F and the F18 update landed, flagging the stress
report and the margin summary.

**That is the tool doing its job on live changes rather than on a demonstration case.** The export
is a snapshot at build time; editing a registered document is expected to make it drift, and the
correct response is to rebuild.

### 5.2 The cycle check was itself defective, and the graph found it

Registering F20 with a back-edge to the margin closed the loop `MARGIN -> F13 -> F20 -> MARGIN`.
`audit()` did not report the cycle — **it hung.** The recursive walk used `UNION ALL` and guarded
only re-entry to its own start node, so a cycle reached from outside that cycle never terminated.
Changed to `UNION`, which bounds the walk; the cycle is now reported. Regression test in
`tests/test_advanced.py`. **The back-edge was removed rather than kept:** F20 sits downstream of the
margin, and the finding it raises against the margin is carried in its metadata instead.

## 6. Limitations

1. **Hashes detect change, not significance.** A typo fix and a corrected number produce the same
   result. The graph tells you what to look at; it does not tell you whether it mattered.
2. **Invalidation is unconditional and transitive** — see §3.1. Conservative by design.
3. **Node granularity is document granularity.** Where a document contains load-dependent and
   load-independent content, the graph cannot distinguish them. F10 and F17 both show this.
4. **Link relations are labels, not semantics.** `corrects`, `superseded_by`,
   `double_count_assessed_by` and `load_input` are recorded and displayed but the engine treats
   every link identically when propagating staleness.
5. **The graph is rebuilt, not maintained.** There is no persistent database under version control
   and no history across builds beyond what the revision events record within a single run.
6. **Requirement-to-evidence links come from a single `evidence_path` column**, so a requirement
   with several pieces of evidence shows only one.
