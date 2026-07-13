# Project State

**Program:** AeroFrame-DT  
**State date:** 2026-07-12  
**Authoritative component:** representative forward pylon-to-wingbox attachment fitting  
**Claim level:** educational and portfolio-focused; non-OEM; non-certified  
**Software release state:** implementation complete through external-tool/data boundary

## Frozen decisions

- Component: one forward pylon-to-wingbox attachment fitting within a two-station pylon support idealization.
- Coordinate system: right-handed; `+X` forward, `+Y` aircraft right, `+Z` upward.
- Internal calculation units: SI (`N`, `m`, `Pa`, `kg`, `s`).
- Baseline architecture: lug/clevis load introduction into a machined fitting body with a wingbox-interface flange and discrete fastener pattern.
- Interfaces: pylon lug/pin, fitting body, wingbox-side flange/fasteners, and local wingbox idealization.
- Candidate materials: 7050-T7451 aluminum, Ti-6Al-4V, and 15-5PH stainless. No design allowable is frozen.
- Candidate fasteners: source-gated close-tolerance titanium or alloy-steel pins/bolts.
- Loads/dimensions: no OEM values assumed. All repository examples are `SYNTHETIC_TEST_ONLY`.

## Software phase state

| Capability | State | Evidence |
|---|---|---|
| Scope, requirements, caveats | COMPLETE | project-control documents and traceability tests |
| Loads/free-body/hand sizing | COMPLETE SOFTWARE | analytical modules and integrated substantiation |
| CAD/PMI preparation | COMPLETE SOFTWARE | schemas, macros, runbook, exchange checks |
| FE verification/production preparation | COMPLETE SOFTWARE | decks, templates, parsers, extraction and convergence tools |
| Fatigue/damage tolerance | COMPLETE SOFTWARE | screening calculations and AFGROW package/parser |
| Dynamics/buckling | COMPLETE SOFTWARE | analytical checks and deck/result support |
| Uncertainty/optimization | COMPLETE SOFTWARE | sampling, DOE, constraints, Pareto and robust ranking |
| Public-data validation | COMPLETE SOFTWARE | blind-correlation and dataset-freeze tools; dataset not yet selected |
| Manufacturing/inspection/quality | COMPLETE SOFTWARE | capability, gage R&R, NCR/RCCA and sidecars |
| Digital thread/reports/releases | COMPLETE SOFTWARE | evidence graph, AP242/QIF screening, reports, manifests and release audit |

## Verification state

- Automated tests: **43 passing** before final evidence regeneration.
- End-to-end synthetic evidence generator: implemented.
- Traceability audit: implemented and passing.
- Repository release audit: implemented.
- CI: installs the package, compiles source, runs tests, generates evidence, and audits the release.

## Remaining non-software gates

1. Existing MD-11/context CAD or representative dimensions.
2. Source-backed loads, spectra, materials, fasteners, allowables, and safety-factor basis.
3. Licensed SolidWorks/ANSYS/Altair/AFGROW execution and returned files.
4. Suitable public metallic lug/joint experimental data.
5. Optional physical inspection or test evidence.

## Next program action

Begin geometry/data intake and external-tool execution using `docs/HUMAN_TOOL_EXECUTION_RUNBOOK.md`. Software development resumes only if returned files expose a missing adapter or verified defect.
