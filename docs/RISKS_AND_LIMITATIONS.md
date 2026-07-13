# Risks and Limitations

| ID | Risk or limitation | Control |
|---|---|---|
| R-001 | Public information cannot establish OEM geometry or loads. | Keep all design inputs provenance-tagged; use representative values only. |
| R-002 | Local FE peaks at constraints/contact edges may be singular or mesh-sensitive. | Use integrated resultants, path/area averages, structural stress, and convergence trends. |
| R-003 | Material values found in handbooks may not be valid design allowables for the selected product form. | Separate typical properties from statistically based allowables; freeze product form and source before margin release. |
| R-004 | Two solvers can share modeling errors. | Require analytical checks and public experimental correlation in addition to code-to-code comparison. |
| R-005 | Prying is geometry- and stiffness-dependent. | Current code accepts only an explicitly sourced prying force or factor; no default is invented. |
| R-006 | Miner and Paris-law models omit sequence, closure, and scatter effects. | Label results screening and run sensitivity/uncertainty studies. |
| R-007 | CAD/PMI translation can preserve graphics while losing semantics. | Verify semantic entity mapping using NIST AP242 cases and QIF reporting. |
| R-008 | GUI solver exports are not yet available. | Prepare exact templates and acceptance criteria before requesting manual interaction. |
