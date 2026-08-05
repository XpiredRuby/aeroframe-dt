# Digital Thread

**Delivered:** `docs/F14_DIGITAL_THREAD.md`. Engine in `src/aeroframe_dt/digital_thread.py`,
populated by `tools/build_f14_thread.py`.

    requirement -> source -> load case -> geometry -> CAD script -> PMI characteristic
    -> analysis -> margin -> inspection plan -> nonconformance -> report

**59 artifacts, 95 links, 0 audit issues.** Every file-backed artifact carries the SHA-256 of that
file computed at build time, so the graph cannot drift from the repository.

| File | Content |
|---|---|
| `thread_AF-DT-1000_revD.json` | full graph export |
| `thread_AF-DT-1000_revD.dot` | Graphviz source |
| `impact_analysis.json` | both impact analyses |

Two impact analyses are recorded:

- **Historical replay** — revising the load basis B to C marks **29 artifacts stale**, reproducing
  the blast radius of a rework cycle that was found by hand.
- **Forward query** — a further revision of the contact measurement would mark **21 stale**,
  including the entire PMI tolerance scheme. That prediction is why the elastic-plastic run was
  executed before any downstream work was treated as final.

**Rebuild after any document change:** `python tools/build_f14_thread.py`

The export is a snapshot taken at build time. Editing a registered document changes its hash, and
the graph will report the drift on the next build — that is the mechanism working, not a fault.

**Cycle safety.** `audit()` reports dependency cycles rather than hanging on them; the recursive
walk is bounded by `UNION`. This was found by registering F20 with a back-edge to the margin, which
closed `MARGIN -> F13 -> F20 -> MARGIN`. Regression test in `tests/test_advanced.py`.
