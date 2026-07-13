# Decisions

## D-001 — Component selection

The project component is a **representative forward pylon-to-wingbox attachment fitting**. The fitting is treated as one member of a symmetric left/right pair at the forward pylon station. The pylon is supported by forward and aft stations.

Reason: this component exposes realistic combined axial, lateral, vertical, bending, roll-couple, lug, fastener, contact, fatigue, manufacturing, and inspection problems while keeping the engineering decision bounded.

## D-002 — Geometry concept

Use a machined fitting with:

- a primary pin-loaded lug or clevis interface toward the pylon;
- a transition web/body;
- a wingbox-side flange with a discrete close-tolerance fastener pattern;
- generous, parameterized blend radii;
- explicit datum and inspection surfaces.

No MD-11/OEM dimensions are implied.

## D-003 — Units and coordinates

All authoritative calculations use SI. `+X` forward, `+Y` right, `+Z` upward. Forces are external loads acting on the isolated pylon; support reactions oppose them.

## D-004 — Verification before production FEA

No production contour is decision-authoritative until constant-strain, cantilever, plate, equilibrium, fastener-group, and Hertz-contact checks pass their predeclared tolerances.

## D-005 — Evidence language

Permitted language includes “representative,” “certification-inspired,” “public-data correlated,” and “damage-tolerance screening.” Prohibited language includes “OEM-accurate,” “certified,” “FAA compliant,” and “validated” when evidence is only code-to-code.
