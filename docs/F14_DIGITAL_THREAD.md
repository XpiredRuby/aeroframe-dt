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

    53 artifacts, 68 links, 0 audit issues

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

## 3. Impact analysis A — historical replay

**The test:** register the graph as it stood when the load basis was at revision B, then apply the
real correction — the lug-axis mapping error, where 30.96° had been measured from aircraft X rather
than from the lug axis, and the correct 59.04° is transverse-dominant. Compare what the graph
flags against the rework that actually happened.

**Result: 24 artifacts marked STALE.**

| Group | Flagged |
|---|---|
| The load basis itself | LOAD-AF-DT-1000 |
| Analyses | F5 FE, F6 pin, F7 contact, F9 DT, F9b spectrum, F10 dynamics, F11 optimisation, F13 stack |
| Released | MARGIN-AF-DT-1000, PMI-AF-DT-1000, INSP-PLAN, NCR-F15-001, RPT-STRESS |
| PMI characteristics | all 10 |

**This matches what actually happened.** Every rev B margin was voided by that correction. The
graph, given only the dependency structure, reproduces the blast radius of a rework cycle that was
discovered by hand.

### 3.1 Where it over-flags — stated, not hidden

**`ANL-F10-DYNAMICS` should not be fully stale.** F10 covers two things: a modal analysis, which
does not take an applied load and is therefore unaffected by a load revision, and an eigenvalue
buckling assessment, which does. The graph flags the whole document because the document is one
node.

This is a real limitation and it generalises: **invalidation here is transitive and unconditional.
The graph over-flags rather than under-flags.** For a configuration-control tool that is the right
direction to be wrong in, but a reviewer should know that a STALE flag means "re-examine", not
"re-run".

Splitting F10 into separate modal and buckling nodes would fix this instance. The general problem —
that document granularity and dependency granularity are not the same — does not go away.

## 4. Impact analysis B — forward query on the pending elastic-plastic run

**The question:** the elastic-plastic contact run is the highest-value open item
(`MARGIN_SUMMARY.md` §11). What does it invalidate when it lands?

**Result: 17 artifacts, including all 10 PMI characteristics, the inspection plan, the F13
tolerance stack, the NCR assessment and the stress report.**

**This is a sequencing finding, not a bookkeeping one.** The obvious expectation is that a better
contact measurement moves a margin number. What the graph shows is that it moves the **tolerance
scheme** too — because `PMI_GDT_DEFINITION.md` derives every tolerance from margin sensitivity
rather than from convention, and `F13` stacks those tolerances back onto the margin. The
dependency is real and it is one this project created deliberately.

**Consequence: the elastic-plastic run should be executed before any further work downstream of
the margin is treated as final.** Anything built on `MS = +0.078` between now and then is built on
a value the run is expected to change.

## 5. Audit

`EvidenceGraph.audit()` checks for dangling link endpoints and dependency cycles. **Zero issues on
the released graph.** The build script exits non-zero on any audit issue, or if any artifact
declares a file that does not exist — so a deleted or renamed file breaks the build rather than
producing a graph with a hole in it.

## 6. Limitations

1. **Hashes detect change, not significance.** A typo fix and a corrected number produce the same
   result. The graph tells you what to look at; it does not tell you whether it mattered.
2. **Invalidation is unconditional and transitive** — see §3.1. Conservative by design.
3. **Node granularity is document granularity.** Where a document contains load-dependent and
   load-independent content, the graph cannot distinguish them.
4. **Link relations are labels, not semantics.** `corrects` and `load_input` are recorded and
   displayed but the engine treats every link identically when propagating staleness.
5. **The graph is rebuilt, not maintained.** There is no persistent database under version control
   and no history across builds beyond what the revision events record within a single run.
6. **Requirement-to-evidence links come from a single `evidence_path` column**, so a requirement
   with several pieces of evidence shows only one.
