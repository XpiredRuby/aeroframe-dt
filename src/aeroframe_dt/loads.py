"""Pylon free-body assembly and representative two-station load sharing.

Inputs are external loads on the isolated pylon. Reactions are returned with the
opposing sign. Statics cannot determine every internal share, so axial and roll
shares are explicit assumptions rather than hidden defaults.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from .vector import Vector3, add, cross, norm, scale, sub


@dataclass(frozen=True)
class AppliedLoad:
    load_id: str
    point_m: Vector3
    force_N: Vector3
    free_moment_Nm: Vector3 = (0.0, 0.0, 0.0)
    provenance: str = "UNSPECIFIED"


@dataclass(frozen=True)
class Resultant:
    force_N: Vector3
    moment_Nm: Vector3
    reference_m: Vector3


@dataclass(frozen=True)
class SupportModel:
    station_spacing_m: float
    axial_forward_share: float
    roll_forward_share: float
    forward_fitting_count: int = 2
    aft_fitting_count: int = 2
    fitting_gauge_m: float = 1.0
    selected_side_sign: int = 1

    def validate(self) -> None:
        if self.station_spacing_m <= 0.0:
            raise ValueError("station_spacing_m must be positive")
        if not 0.0 <= self.axial_forward_share <= 1.0:
            raise ValueError("axial_forward_share must be in [0, 1]")
        if not 0.0 <= self.roll_forward_share <= 1.0:
            raise ValueError("roll_forward_share must be in [0, 1]")
        if self.forward_fitting_count <= 0 or self.aft_fitting_count <= 0:
            raise ValueError("fitting counts must be positive")
        if self.fitting_gauge_m <= 0.0:
            raise ValueError("fitting_gauge_m must be positive")
        if self.selected_side_sign not in (-1, 1):
            raise ValueError("selected_side_sign must be -1 or +1")


@dataclass(frozen=True)
class SupportSolution:
    forward_station_reaction_N: Vector3
    aft_station_reaction_N: Vector3
    selected_forward_fitting_reaction_N: Vector3
    forward_roll_couple_force_N: float
    residual_force_N: Vector3
    residual_moment_Nm: Vector3

    @property
    def residual_force_norm_N(self) -> float:
        return norm(self.residual_force_N)

    @property
    def residual_moment_norm_Nm(self) -> float:
        return norm(self.residual_moment_Nm)


def assemble_resultant(loads: Iterable[AppliedLoad], reference_m: Vector3 = (0.0, 0.0, 0.0)) -> Resultant:
    force = (0.0, 0.0, 0.0)
    moment = (0.0, 0.0, 0.0)
    for load in loads:
        force = add(force, load.force_N)
        arm = sub(load.point_m, reference_m)
        moment = add(moment, add(load.free_moment_Nm, cross(arm, load.force_N)))
    return Resultant(force_N=force, moment_Nm=moment, reference_m=reference_m)


def solve_two_station_supports(resultant: Resultant, model: SupportModel) -> SupportSolution:
    """Solve the statically determinate portions of a two-station support model.

    Forward station is x=0 and aft station is x=L. Pitch and yaw moments set the
    aft vertical/lateral reactions. Axial and roll distribution require explicit
    share assumptions.
    """

    model.validate()
    fx, fy, fz = resultant.force_N
    mx, my, mz = resultant.moment_Nm
    L = model.station_spacing_m

    # Equilibrium about forward station:
    # My - L*Raz = 0; Mz + L*Ray = 0.
    raz = my / L
    rfz = -fz - raz
    ray = -mz / L
    rfy = -fy - ray

    rfx = -model.axial_forward_share * fx
    rax = -(1.0 - model.axial_forward_share) * fx

    forward_station = (rfx, rfy, rfz)
    aft_station = (rax, ray, raz)

    # Forward share of the roll reaction is an equal/opposite vertical-force
    # couple across the left/right fitting gauge. Q*g = -eta_roll*Mx.
    q_roll = -model.roll_forward_share * mx / model.fitting_gauge_m
    selected = (
        rfx / model.forward_fitting_count,
        rfy / model.forward_fitting_count,
        rfz / model.forward_fitting_count + model.selected_side_sign * q_roll,
    )

    total_reaction_force = add(forward_station, aft_station)
    residual_force = add(resultant.force_N, total_reaction_force)

    aft_arm = (L, 0.0, 0.0)
    station_moment = cross(aft_arm, aft_station)
    reacted_roll = -model.roll_forward_share * mx - (1.0 - model.roll_forward_share) * mx
    reaction_moment = add(station_moment, (reacted_roll, 0.0, 0.0))
    residual_moment = add(resultant.moment_Nm, reaction_moment)

    return SupportSolution(
        forward_station_reaction_N=forward_station,
        aft_station_reaction_N=aft_station,
        selected_forward_fitting_reaction_N=selected,
        forward_roll_couple_force_N=q_roll,
        residual_force_N=residual_force,
        residual_moment_Nm=residual_moment,
    )
