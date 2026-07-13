# Load Assumptions and Provenance

## Provenance classes

- `PUBLISHED`: copied from a cited primary source without alteration.
- `DERIVED`: calculated from published inputs using a documented equation.
- `REPRESENTATIVE_ESTIMATE`: educational assumption selected for a sensitivity study.
- `TUNED`: adjusted during correlation; pre- and post-tune values must both be preserved.
- `SYNTHETIC_TEST_ONLY`: arithmetic/software test input; prohibited for design claims.

## Current load state

No aircraft design load is frozen. `examples/synthetic_load_case.json` exists only to verify force/moment assembly and load-sharing arithmetic.

## Required load families

1. axial thrust and drag;
2. vertical maneuver/inertia;
3. lateral maneuver/gust/engine-side load;
4. combined axial/vertical/lateral cases;
5. torsional and roll-couple cases;
6. thermal mismatch where a defensible temperature range is established;
7. fatigue spectrum bins;
8. fail-safe or redistributed-load screening cases.

## Load-factor policy

Limit, ultimate, and fatigue-spectrum values will be stored separately. No safety factor is silently embedded in a load vector. Every margin row will identify whether the applied load is limit or ultimate and the factor used in the denominator.
