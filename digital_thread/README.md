# Digital Thread

**Delivered:** `docs/F14_DIGITAL_THREAD.md`. Engine in `src/aeroframe_dt/digital_thread.py`,
populated by `tools/build_f14_thread.py`.

    requirement -> source -> load case -> geometry -> CAD script -> PMI characteristic
    -> analysis -> margin -> inspection plan -> nonconformance -> report

**53 artifacts, 68 links, 0 audit issues.** Every file-backed artifact carries the SHA-256 of that
file computed at build time, so the graph cannot drift from the repository.

| File | Content |
|---|---|
| `thread_AF-DT-1000_revD.json` | full graph export |
| `thread_AF-DT-1000_revD.dot` | Graphviz source |
| `impact_analysis.json` | both impact analyses |

Two impact analyses are recorded:

- **Historical replay** — revising the load basis B to C marks **24 artifacts stale**, reproducing
  the blast radius of a rework cycle that was found by hand.
- **Forward query** — the pending elastic-plastic contact run would mark **17 stale**, including
  the entire PMI tolerance scheme. It should therefore be run before anything downstream of the
  margin is treated as final.

Rebuild: `python tools/build_f14_thread.py`
