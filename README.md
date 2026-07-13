# AeroFrame-DT

AeroFrame-DT is an educational, portfolio-focused structural substantiation and digital-thread program for a **representative forward pylon-to-wingbox attachment fitting**.

It is not an OEM reconstruction, certification analysis, or claim of compliance. Geometry and loads are representative unless a source record explicitly marks a value as published. Solver agreement is verification evidence, not physical validation.

## Current execution state

The program has started with the scope and interfaces frozen, analytical load-path infrastructure implemented, requirements and verification traceability established, and the benchmark set locked. See [`PROJECT_STATE.md`](PROJECT_STATE.md).

## Core workflow

```text
requirements and assumptions
→ pylon free body and load sharing
→ classical sizing and margins
→ parametric CAD / GD&T / PMI
→ verified FE hierarchy
→ nonlinear contact model
→ fatigue and damage-tolerance screening
→ uncertainty and robust optimization
→ AP242/QIF-style inspection and nonconformance thread
```

## Run the analytical smoke tests

```bash
python -m unittest discover -s tests -v
python tools/run_load_model.py examples/synthetic_load_case.json
python tools/run_hand_calcs.py examples/synthetic_hand_calc_case.json
python tools/check_traceability.py
```

The files under `examples/` contain synthetic arithmetic smoke-test data only. They are not aircraft loads or material allowables.
