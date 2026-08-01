# Inspection, Quality, and Nonconformance

**Delivered:** `docs/F13_MANUFACTURING_INSPECTION.md` — process plan, inspection plan, measurement
system analysis, and a tolerance stack onto the governing margin.

| File | Content |
|---|---|
| `inspection_plan_AF-DT-1000_revD.csv` | 10 measurable characteristics, machine-readable |
| `../tools/run_f13_inspection_plan.py` | validates the plan, screens gauge resolution, runs MSA and capability, computes the tolerance stack |
| `../results/software_verification/f13_inspection_plan.json` | generated results |

**Headline:** the released tolerance scheme takes MS from **+0.0784 to +0.0568** at worst case —
27.6% of the margin, still positive. Tolerances would have to be 3.62x wider to reach zero.

Nonconformance cases are in `docs/F15_NONCONFORMANCE_RCCA_AF-DT-1000.md` and
`examples/synthetic_inspection.json`. All measurement data is `SYNTHETIC_TEST_ONLY`.
