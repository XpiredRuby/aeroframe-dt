# Predeclared Structural Extraction Rules

1. **Equilibrium:** sum all interface reactions and applied loads in the same coordinate system. Report six residual components and normalized residuals.
2. **Fastener load:** use integrated connector/contact resultant, not a single nodal force.
3. **Bearing:** report integrated contact resultant divided by projected diameter-thickness area; separately report pressure distribution and its mesh sensitivity.
4. **Net-section:** use path-averaged membrane stress across the ligament at a predeclared section. Do not compare a singular local peak with nominal hand stress.
5. **Shear-out:** use average shear traction/resultant across the two physical ligaments.
6. **Plate bending:** compare linearized membrane-plus-bending stress at a predeclared section away from contact edges.
7. **Convergence:** track displacement, integrated resultants, fastener loads, averaged structural stresses, and strain energy. Local contact peaks are diagnostic only.
8. **Nonlinear convergence:** retain load-step, force, displacement, contact-status, penetration, and energy histories.
