# Software Completion Matrix

**Status definition:** `IMPLEMENTED` means source code, deterministic inputs, tests, and a documented interface exist. It does not mean a licensed solver or physical test has been executed.

| Capability | Status | Implementation | External execution still required? |
|---|---|---|---|
| Requirements and V&V traceability | IMPLEMENTED | CSV registers, traceability audit, evidence graph | No |
| Load-case/provenance generation | IMPLEMENTED | `load_cases.py`, load-envelope CLI | Authoritative load source still required |
| Free-body and load sharing | IMPLEMENTED | `loads.py`, equilibrium tests | No |
| Classical fitting calculations | IMPLEMENTED | `hand_calcs.py`, integrated substantiation | Source-backed allowables required for design use |
| Fastener distribution and interaction | IMPLEMENTED | shear/tension group solvers and prying interface | Final pattern and allowable method required |
| Material and fastener trades | IMPLEMENTED | `materials.py` | Legal allowable sources required |
| CAD parameter control | IMPLEMENTED | SolidWorks VBA and FreeCAD macros | CAD application execution required |
| FE benchmark input generation | IMPLEMENTED | patch, cantilever, plate, modal, buckling decks | Solver execution required |
| Nonlinear contact preparation | IMPLEMENTED | topology-gated APDL template and extraction contract | Meshed geometry/named components and solver required |
| Solver batch contracts | IMPLEMENTED | argv-based run manifests | Licensed executable required |
| F06 and compact result parsing | IMPLEMENTED | force, displacement, modal, buckling parsers | Result files required |
| Stress/contact extraction | IMPLEMENTED | weighted averages, linearization, integrated resultants | Solver field exports required |
| Mesh convergence and solver comparison | IMPLEMENTED | monotonicity, apparent order, extrapolation, GCI | Mesh-series results required |
| Static margin tables | IMPLEMENTED | mandatory source/load/geometry/extraction/allowable/factor trace | Design inputs required |
| Modal/buckling analytical checks | IMPLEMENTED | beam frequencies, Euler buckling, comparison utilities | Numerical results required |
| Fatigue and Miner screening | IMPLEMENTED | Goodman/Basquin/Miner | Source-backed spectrum and properties required |
| Damage tolerance and AFGROW workflow | IMPLEMENTED | Paris integration, critical crack size, neutral package/parser | AFGROW execution and material data required |
| Uncertainty propagation | IMPLEMENTED | Monte Carlo and Latin hypercube | Distribution basis required |
| Robust optimization | IMPLEMENTED | DOE, constraints, Pareto and robust ranking | Frozen geometry/manufacturing constraints required |
| Public-data correlation | IMPLEMENTED | frozen dataset hash, blind/post metrics, parameter audit | Suitable public dataset required |
| AP242 continuity screening | IMPLEMENTED | STEP schema/entity/PMI inventory | AP242 export required |
| QIF/inspection linkage | IMPLEMENTED | open XML sidecar and validation | Standards-compliant QIF tool required for formal exchange |
| Inspection statistics | IMPLEMENTED | capability and crossed gage R&R | Measurements required for non-synthetic use |
| NCR/RCCA packages | IMPLEMENTED | three synthetic cases and disposition schema | Real NCRs only if manufacturing occurs |
| Revision-aware digital thread | IMPLEMENTED | SQLite graph, invalidation, JSON/DOT export | No |
| Automated reports and release packages | IMPLEMENTED | Markdown/HTML reports, manifests, deterministic archive | No |

## Software completion boundary

No further source-code capability is blocked by physical hardware. Remaining work is **execution and data population**: authoritative geometry, loads, allowables, licensed solver/CAD runs, AP242/QIF exports, and optional physical measurements.
