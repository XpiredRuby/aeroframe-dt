# AeroFrame-DT Software Verification Report

**Document:** `AFDT-RPT-SW-001`  
**Revision:** `A`  
**Claim:** Representative, non-OEM, educational structural-engineering evidence.  

## Document control

This report is generated from source-controlled inputs and compact result manifests. It is not a certification report and does not establish OEM accuracy.

## Scope

All outputs in this report are synthetic software-verification evidence. No OEM dimensions, aircraft loads, or certification claims are included.

## Implemented workflows

Load assembly, integrated hand substantiation, solver-deck generation, convergence assessment, CAD parameter macros, fatigue/AFGROW packaging, inspection statistics, NCR packages, digital-thread export, and deterministic reporting are automated.

## Execution boundary

Licensed solver execution and CAD export remain human-tool execution gates. The software needed to prepare, run, parse, compare, trace, and report those future files is present.

## Limitations

- Synthetic values are not design data.
- Solver decks require vendor execution and review.
- The QIF-style XML is an open sidecar, not schema-valid QIF.

## Evidence index

| artifact | status | purpose |
| --- | --- | --- |
| results/software_verification/afgrow_package/AFGROW_IMPORT_INSTRUCTIONS.md | GENERATED | Synthetic software verification |
| results/software_verification/afgrow_package/case.json | GENERATED | Synthetic software verification |
| results/software_verification/afgrow_package/spectrum.csv | GENERATED | Synthetic software verification |
| results/software_verification/cad_macros/freecad_parameter_sheet.py | GENERATED | Synthetic software verification |
| results/software_verification/cad_macros/set_global_variables.bas | GENERATED | Synthetic software verification |
| results/software_verification/digital_thread.dot | GENERATED | Synthetic software verification |
| results/software_verification/digital_thread.json | GENERATED | Synthetic software verification |
| results/software_verification/ncr/NCR-SYNTH-001.md | GENERATED | Synthetic software verification |
| results/software_verification/ncr/NCR-SYNTH-002.md | GENERATED | Synthetic software verification |
| results/software_verification/ncr/NCR-SYNTH-003.md | GENERATED | Synthetic software verification |
| results/software_verification/release_audit.json | GENERATED | Synthetic software verification |
| results/software_verification/solver_decks/cantilever_buckling_ansys.dat | GENERATED | Synthetic software verification |
| results/software_verification/solver_decks/cantilever_modal_ansys.dat | GENERATED | Synthetic software verification |
| results/software_verification/solver_decks/cantilever_modal_nastran.bdf | GENERATED | Synthetic software verification |
| results/software_verification/solver_decks/cantilever_static_ansys.dat | GENERATED | Synthetic software verification |
| results/software_verification/solver_decks/cantilever_static_nastran.bdf | GENERATED | Synthetic software verification |
| results/software_verification/solver_decks/constant_strain_patch_nastran.bdf | GENERATED | Synthetic software verification |
| results/software_verification/solver_decks/square_plate_ansys.dat | GENERATED | Synthetic software verification |
| results/software_verification/synthetic_convergence.json | GENERATED | Synthetic software verification |
| results/software_verification/synthetic_inspection.json | GENERATED | Synthetic software verification |
| results/software_verification/synthetic_load_envelope.csv | GENERATED | Synthetic software verification |
| results/software_verification/synthetic_qif_sidecar.xml | GENERATED | Synthetic software verification |
| results/software_verification/synthetic_substantiation.json | GENERATED | Synthetic software verification |
| results/software_verification/unit_test_log.txt | GENERATED | Synthetic software verification |
