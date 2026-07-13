# Project State

**Program:** AeroFrame-DT  
**State date:** 2026-07-12  
**Authoritative component:** representative forward pylon-to-wingbox attachment fitting  
**Claim level:** educational and portfolio-focused; non-OEM; non-certified

## Frozen decisions

- Component: one forward pylon-to-wingbox attachment fitting within a two-station pylon support idealization.
- Coordinate system: right-handed; `+X` forward, `+Y` aircraft right, `+Z` upward.
- Internal calculation units: SI (`N`, `m`, `Pa`, `kg`, `s`). Display conversions are secondary only.
- Baseline architecture: lug/clevis load introduction into a machined fitting body with a wingbox-interface flange and a discrete fastener pattern.
- Interfaces: pylon lug/pin, fitting body, wingbox-side flange/fasteners, and local wingbox idealization.
- Material candidates: 7050-T7451 aluminum, Ti-6Al-4V, and 15-5PH stainless steel. No design allowable is frozen yet.
- Fastener candidates: aerospace close-tolerance titanium or alloy-steel pins/bolts. Exact specification and allowables remain source-gated.
- Loads and dimensions: no OEM values are assumed. Numerical values in examples are synthetic test values only.

## Phase state

| Phase | State | Evidence |
|---|---|---|
| F0 scope | Complete for project start | `docs/DECISIONS.md`, `cad/GEOMETRY_CONCEPT.md` |
| F1 requirements/loads | In progress | requirements CSVs, load model, FBD document |
| F2 classical analysis | In progress | `src/aeroframe_dt/hand_calcs.py`, unit tests |
| F3-F4 CAD/PMI | Prepared | parameter schema and PMI requirements |
| F5-F7 FE/contact | Benchmark-locked, production model not run | `benchmarks/BENCHMARK_LOCK.md` |
| F8-F9 fatigue/DT | Benchmark-locked, material data pending | benchmark lock and limitations |
| F10-F16 | Planned | requirements and verification matrix |

## Completed digital work

- Repository structure and state-management files created.
- Scope, units, interfaces, caveats, and candidate materials frozen.
- Requirements and verification matrix initialized.
- Pylon resultant and two-station load-sharing implementation completed.
- Classical checks implemented for net section, bearing, shear-out, pin shear, plate bending, fastener-group loading, combined shear/tension interaction, and explicit-source prying augmentation.
- Exact numerical-verification benchmarks locked.
- Unit tests and traceability checks implemented.

## Blocking inputs

1. Existing MD-11 context CAD exports/drawings, when available, to establish envelope context without copying OEM geometry.
2. A new private GitHub repository named `aeroframe-dt`, because the connected GitHub tool can write to repositories but does not expose repository creation.
3. Licensed-GUI interaction later for SolidWorks/ANSYS/Altair/AFGROW exports.

## Next execution block

- Finalize a source-backed representative load envelope and load-case taxonomy.
- Add fastener-pattern elastic distribution and fitting margin-table generation to the load-model pipeline.
- Implement independent Navier plate and Paris-law benchmark oracles.
- Prepare CAD global variables/equations and solver input templates.
