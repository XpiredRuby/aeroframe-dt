"""Independent closed-form benchmark oracles."""
from __future__ import annotations
from math import pi

def cantilever_tip_deflection(force_N: float, length_m: float, elastic_modulus_Pa: float, second_moment_m4: float) -> float:
    if min(length_m,elastic_modulus_Pa,second_moment_m4)<=0: raise ValueError('positive geometry/properties required')
    return force_N*length_m**3/(3*elastic_modulus_Pa*second_moment_m4)

def cantilever_root_stress(force_N: float, length_m: float, outer_fiber_m: float, second_moment_m4: float) -> float:
    return abs(force_N)*length_m*outer_fiber_m/second_moment_m4

def simply_supported_square_plate_center_deflection(uniform_pressure_Pa: float, side_m: float, thickness_m: float, elastic_modulus_Pa: float, poisson: float, terms: int=41) -> float:
    if min(side_m,thickness_m,elastic_modulus_Pa)<=0 or not -1 < poisson < .5: raise ValueError('invalid input')
    D=elastic_modulus_Pa*thickness_m**3/(12*(1-poisson**2)); total=0.0
    odds=range(1,terms+1,2)
    for m in odds:
        for n in odds:
            total += ((-1)**((m-1)//2+(n-1)//2))/(m*n*(m*m+n*n)**2)
    return 16*uniform_pressure_Pa*side_m**4*total/(pi**6*D)

def hertz_line_contact_half_width(load_per_length_N_per_m: float, radius_m: float, effective_modulus_Pa: float) -> float:
    if min(load_per_length_N_per_m,radius_m,effective_modulus_Pa)<=0: raise ValueError('inputs must be positive')
    return (4*load_per_length_N_per_m*radius_m/(pi*effective_modulus_Pa))**0.5
