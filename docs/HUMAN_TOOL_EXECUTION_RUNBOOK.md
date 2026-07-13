# Human Tool Execution Runbook

This runbook is the only remaining human interface after software completion. Do not make engineering choices during execution unless the prepared inputs are invalid; return the requested artifact instead.

## SolidWorks

1. Open or create the representative fitting part.
2. Run `set_global_variables.bas` generated from the frozen parameter JSON.
3. Build/rebuild the feature tree using the named datum and feature scheme in `cad/PMI_REQUIREMENTS.md`.
4. Export:
   - native part/assembly;
   - STEP AP242 with semantic PMI if available;
   - Parasolid geometry-only backup;
   - drawing PDF;
   - mass-properties text;
   - screenshots of the feature tree, datums, and PMI tree.
5. Return the files without renaming their revision identifiers.

## ANSYS Mechanical/APDL

1. Execute the generated benchmark decks first.
2. Return every text result CSV, solver output log, error/warning file, and exact software version.
3. For the production model, preserve named selections used by the contact template.
4. Run the predeclared mesh sequence without changing extraction rules between meshes.
5. Export compact field tables for the paths/interfaces listed in `fe/solid_contact/EXTRACTION_RULES.md`.

## Altair OptiStruct/NASTRAN

1. Execute the `.bdf` verification decks.
2. Return `.f06` plus compact CSV exports. Do not commit `.op2` or `.h3d` unless a separate storage decision is made.
3. Record the executable, version, command line, and warnings.

## AFGROW

1. Use the generated neutral package.
2. Enter only source-backed material and spectrum data.
3. Export `cycles,crack_length_m` CSV, run summary, native project, and version information.

## Required return convention

Place returned files under a folder named:

```text
AFDT_RETURN_<tool>_<run-id>_<YYYYMMDD>/
```

Include `RETURN_MANIFEST.md` stating the tool/version, operator actions, any deviations, and all filenames.
