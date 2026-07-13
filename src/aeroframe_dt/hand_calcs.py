"""Classical structural screening calculations.

These equations are deliberately explicit and local. They do not replace a
product-form allowable basis, a validated lug method, or detailed joint FEA.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from math import pi, sqrt
from typing import Iterable, Sequence


@dataclass(frozen=True)
class CheckResult:
    check_id: str
    demand: float
    allowable: float | None
    safety_factor: float
    margin: float | None
    units: str
    method: str
    notes: str = ""

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


def _positive(name: str, value: float) -> float:
    value = float(value)
    if value <= 0.0:
        raise ValueError(f"{name} must be positive")
    return value


def margin_of_safety(allowable: float, demand: float, safety_factor: float = 1.0) -> float:
    allowable = _positive("allowable", allowable)
    safety_factor = _positive("safety_factor", safety_factor)
    if demand < 0.0:
        raise ValueError("demand must be nonnegative")
    if demand == 0.0:
        return float("inf")
    return allowable / (demand * safety_factor) - 1.0


def lug_net_section(
    load_N: float,
    width_m: float,
    hole_diameter_m: float,
    thickness_m: float,
    allowable_Pa: float | None = None,
    safety_factor: float = 1.0,
    check_id: str = "lug_net_section",
) -> CheckResult:
    width_m = _positive("width_m", width_m)
    hole_diameter_m = _positive("hole_diameter_m", hole_diameter_m)
    thickness_m = _positive("thickness_m", thickness_m)
    if width_m <= hole_diameter_m:
        raise ValueError("width_m must exceed hole_diameter_m")
    stress = abs(load_N) / ((width_m - hole_diameter_m) * thickness_m)
    margin = None if allowable_Pa is None else margin_of_safety(allowable_Pa, stress, safety_factor)
    return CheckResult(check_id, stress, allowable_Pa, safety_factor, margin, "Pa", "P/[(w-d)t]")


def projected_bearing(
    load_N: float,
    diameter_m: float,
    thickness_m: float,
    allowable_Pa: float | None = None,
    safety_factor: float = 1.0,
    check_id: str = "projected_bearing",
) -> CheckResult:
    diameter_m = _positive("diameter_m", diameter_m)
    thickness_m = _positive("thickness_m", thickness_m)
    stress = abs(load_N) / (diameter_m * thickness_m)
    margin = None if allowable_Pa is None else margin_of_safety(allowable_Pa, stress, safety_factor)
    return CheckResult(check_id, stress, allowable_Pa, safety_factor, margin, "Pa", "P/(dt)")


def two_plane_shear_out(
    load_N: float,
    edge_distance_center_m: float,
    hole_diameter_m: float,
    thickness_m: float,
    allowable_Pa: float | None = None,
    safety_factor: float = 1.0,
    check_id: str = "two_plane_shear_out",
) -> CheckResult:
    edge_distance_center_m = _positive("edge_distance_center_m", edge_distance_center_m)
    hole_diameter_m = _positive("hole_diameter_m", hole_diameter_m)
    thickness_m = _positive("thickness_m", thickness_m)
    ligament = edge_distance_center_m - 0.5 * hole_diameter_m
    if ligament <= 0.0:
        raise ValueError("edge distance must leave a positive physical ligament")
    stress = abs(load_N) / (2.0 * ligament * thickness_m)
    margin = None if allowable_Pa is None else margin_of_safety(allowable_Pa, stress, safety_factor)
    return CheckResult(check_id, stress, allowable_Pa, safety_factor, margin, "Pa", "P/[2(e-d/2)t]")


def pin_shear(
    load_N: float,
    diameter_m: float,
    shear_planes: int = 1,
    allowable_Pa: float | None = None,
    safety_factor: float = 1.0,
    check_id: str = "pin_shear",
) -> CheckResult:
    diameter_m = _positive("diameter_m", diameter_m)
    if shear_planes <= 0:
        raise ValueError("shear_planes must be positive")
    area = pi * diameter_m**2 / 4.0
    stress = abs(load_N) / (shear_planes * area)
    margin = None if allowable_Pa is None else margin_of_safety(allowable_Pa, stress, safety_factor)
    return CheckResult(check_id, stress, allowable_Pa, safety_factor, margin, "Pa", "P/(n*pi*d^2/4)")


def rectangular_plate_bending(
    moment_Nm: float,
    section_width_m: float,
    thickness_m: float,
    allowable_Pa: float | None = None,
    safety_factor: float = 1.0,
    check_id: str = "rectangular_plate_bending",
) -> CheckResult:
    section_width_m = _positive("section_width_m", section_width_m)
    thickness_m = _positive("thickness_m", thickness_m)
    stress = 6.0 * abs(moment_Nm) / (section_width_m * thickness_m**2)
    margin = None if allowable_Pa is None else margin_of_safety(allowable_Pa, stress, safety_factor)
    return CheckResult(check_id, stress, allowable_Pa, safety_factor, margin, "Pa", "6M/(bt^2)")


def fastener_group_shear(
    positions_m: Sequence[tuple[float, float]],
    force_xy_N: tuple[float, float],
    moment_z_Nm: float,
) -> list[tuple[float, float]]:
    """Elastic direct-plus-torsional shear distribution for equal fasteners."""

    if not positions_m:
        raise ValueError("At least one fastener is required")
    n = len(positions_m)
    cx = sum(p[0] for p in positions_m) / n
    cy = sum(p[1] for p in positions_m) / n
    centered = [(x - cx, y - cy) for x, y in positions_m]
    polar = sum(x * x + y * y for x, y in centered)
    if abs(moment_z_Nm) > 0.0 and polar <= 0.0:
        raise ValueError("Nonzero moment requires a non-degenerate fastener pattern")
    direct_x = force_xy_N[0] / n
    direct_y = force_xy_N[1] / n
    loads: list[tuple[float, float]] = []
    for x, y in centered:
        torsion_x = -moment_z_Nm * y / polar if polar else 0.0
        torsion_y = moment_z_Nm * x / polar if polar else 0.0
        loads.append((direct_x + torsion_x, direct_y + torsion_y))
    return loads


def _solve_3x3(a: list[list[float]], b: list[float]) -> list[float]:
    aug = [row[:] + [rhs] for row, rhs in zip(a, b)]
    for col in range(3):
        pivot = max(range(col, 3), key=lambda r: abs(aug[r][col]))
        if abs(aug[pivot][col]) < 1e-15:
            raise ValueError("Fastener pattern is singular for the requested tension distribution")
        aug[col], aug[pivot] = aug[pivot], aug[col]
        scale = aug[col][col]
        aug[col] = [v / scale for v in aug[col]]
        for row in range(3):
            if row == col:
                continue
            factor = aug[row][col]
            aug[row] = [v - factor * w for v, w in zip(aug[row], aug[col])]
    return [aug[i][3] for i in range(3)]


def fastener_group_tension(
    positions_m: Sequence[tuple[float, float]],
    direct_tension_N: float,
    moment_x_Nm: float,
    moment_y_Nm: float,
    tension_only: bool = False,
) -> list[float]:
    """Linear elastic tension distribution satisfying force and two moments.

    The fitted field is q(x,y)=a+b*x+c*y after centering. It satisfies:
    Σq=T, Σ(y*q)=Mx, and Σ(-x*q)=My. If `tension_only` clips negative
    values, the clipped result no longer exactly satisfies equilibrium and is a
    screening approximation only.
    """

    if len(positions_m) < 3:
        raise ValueError("At least three non-collinear fasteners are required")
    n = len(positions_m)
    cx = sum(p[0] for p in positions_m) / n
    cy = sum(p[1] for p in positions_m) / n
    pts = [(x - cx, y - cy) for x, y in positions_m]
    sx = sum(x for x, _ in pts)
    sy = sum(y for _, y in pts)
    sxx = sum(x * x for x, _ in pts)
    syy = sum(y * y for _, y in pts)
    sxy = sum(x * y for x, y in pts)
    # Unknowns [a,b,c], with q=a+b*x+c*y.
    matrix = [
        [float(n), sx, sy],
        [sy, sxy, syy],
        [-sx, -sxx, -sxy],
    ]
    coeff = _solve_3x3(matrix, [direct_tension_N, moment_x_Nm, moment_y_Nm])
    loads = [coeff[0] + coeff[1] * x + coeff[2] * y for x, y in pts]
    if tension_only:
        return [max(0.0, value) for value in loads]
    return loads


def shear_tension_interaction(
    shear_load_N: float,
    shear_allowable_N: float,
    tension_load_N: float,
    tension_allowable_N: float,
    exponent: float = 1.0,
    check_id: str = "fastener_shear_tension_interaction",
) -> CheckResult:
    shear_allowable_N = _positive("shear_allowable_N", shear_allowable_N)
    tension_allowable_N = _positive("tension_allowable_N", tension_allowable_N)
    exponent = _positive("exponent", exponent)
    rs = abs(shear_load_N) / shear_allowable_N
    rt = max(0.0, tension_load_N) / tension_allowable_N
    index = rs**exponent + rt**exponent
    margin = float("inf") if index == 0.0 else 1.0 / index - 1.0
    return CheckResult(
        check_id,
        index,
        1.0,
        1.0,
        margin,
        "ratio",
        f"(V/V_allow)^{exponent:g} + (T/T_allow)^{exponent:g}",
        "Exponent must be tied to the selected fastener allowable method.",
    )


def tension_with_explicit_prying(
    direct_tension_N: float,
    prying_increment_N: float | None = None,
    prying_factor: float | None = None,
) -> float:
    """Return augmented tension without inventing a prying model.

    Supply exactly one of an independently calculated prying increment or a
    source-backed factor Q/T. Detailed T-stub/contact FEA will replace this
    screening interface when geometry and joint stiffness are frozen.
    """

    if (prying_increment_N is None) == (prying_factor is None):
        raise ValueError("Supply exactly one of prying_increment_N or prying_factor")
    if direct_tension_N < 0.0:
        raise ValueError("direct_tension_N must be nonnegative")
    if prying_increment_N is not None:
        if prying_increment_N < 0.0:
            raise ValueError("prying_increment_N must be nonnegative")
        return direct_tension_N + prying_increment_N
    assert prying_factor is not None
    if prying_factor < 0.0:
        raise ValueError("prying_factor must be nonnegative")
    return direct_tension_N * (1.0 + prying_factor)


def resultant_2d(vector: tuple[float, float]) -> float:
    return sqrt(vector[0] ** 2 + vector[1] ** 2)


def factored_stress(
    nominal_stress_Pa: float,
    fitting_factor: float,
    allowable_Pa: float | None = None,
    safety_factor: float = 1.0,
    check_id: str = "factored_stress",
    factor_source: str = "SOURCE_REQUIRED",
) -> CheckResult:
    """Apply an explicit, source-identified fitting/stress factor."""
    if nominal_stress_Pa < 0:
        raise ValueError("nominal_stress_Pa must be nonnegative")
    fitting_factor = _positive("fitting_factor", fitting_factor)
    if not factor_source.strip() or factor_source == "SOURCE_REQUIRED":
        raise ValueError("a non-placeholder factor_source is required")
    demand = nominal_stress_Pa * fitting_factor
    margin = None if allowable_Pa is None else margin_of_safety(allowable_Pa, demand, safety_factor)
    return CheckResult(check_id, demand, allowable_Pa, safety_factor, margin, "Pa", "K * sigma_nominal", f"factor={fitting_factor:g}; source={factor_source}")


def friction_slip_capacity(
    friction_coefficient: float,
    preload_per_fastener_N: float,
    fastener_count: int,
    slip_planes: int = 1,
    preload_loss_factor: float = 1.0,
) -> float:
    """Return source-gated Coulomb slip capacity for a preloaded joint."""
    if friction_coefficient < 0:
        raise ValueError("friction_coefficient must be nonnegative")
    preload_per_fastener_N = _positive("preload_per_fastener_N", preload_per_fastener_N)
    if fastener_count <= 0 or slip_planes <= 0:
        raise ValueError("fastener_count and slip_planes must be positive")
    if not 0 < preload_loss_factor <= 1:
        raise ValueError("preload_loss_factor must be in (0,1]")
    return friction_coefficient * preload_per_fastener_N * fastener_count * slip_planes * preload_loss_factor


def joint_slip_check(
    applied_shear_N: float,
    friction_coefficient: float,
    preload_per_fastener_N: float,
    fastener_count: int,
    slip_planes: int = 1,
    preload_loss_factor: float = 1.0,
    safety_factor: float = 1.0,
    check_id: str = "joint_slip",
) -> CheckResult:
    capacity = friction_slip_capacity(friction_coefficient, preload_per_fastener_N, fastener_count, slip_planes, preload_loss_factor)
    demand = abs(applied_shear_N)
    margin = margin_of_safety(capacity, demand, safety_factor)
    return CheckResult(check_id, demand, capacity, safety_factor, margin, "N", "mu * preload * n * slip_planes * loss_factor", "Friction/preload inputs require source and installation provenance.")
