"""Text-deck generators for open, reviewable solver inputs.

The generators intentionally create transparent templates. They do not claim to
replace vendor preprocessors or validate a production finite-element model.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Mapping


def _positive(name: str, value: float) -> float:
    value = float(value)
    if value <= 0:
        raise ValueError(f"{name} must be positive")
    return value


@dataclass(frozen=True)
class BeamBenchmark:
    length_m: float
    width_m: float
    height_m: float
    elastic_modulus_Pa: float
    poisson: float
    density_kg_m3: float
    tip_force_N: float
    elements: int = 20

    def validate(self) -> None:
        for name in ("length_m", "width_m", "height_m", "elastic_modulus_Pa", "density_kg_m3"):
            _positive(name, getattr(self, name))
        if not -1 < self.poisson < 0.5:
            raise ValueError("invalid Poisson ratio")
        if self.elements < 1:
            raise ValueError("elements must be positive")


@dataclass(frozen=True)
class PlateBenchmark:
    side_m: float
    thickness_m: float
    elastic_modulus_Pa: float
    poisson: float
    pressure_Pa: float
    divisions: int = 20

    def validate(self) -> None:
        for name in ("side_m", "thickness_m", "elastic_modulus_Pa"):
            _positive(name, getattr(self, name))
        if not -1 < self.poisson < 0.5:
            raise ValueError("invalid Poisson ratio")
        if self.divisions < 2:
            raise ValueError("divisions must be at least 2")


def nastran_cantilever_bdf(model: BeamBenchmark, solution: int = 101) -> str:
    """Generate a small-field NASTRAN/OptiStruct CBEAM cantilever benchmark."""
    model.validate()
    area = model.width_m * model.height_m
    iy = model.width_m * model.height_m**3 / 12
    iz = model.height_m * model.width_m**3 / 12
    j = iy + iz
    lines = [
        "$ AeroFrame-DT cantilever verification deck",
        "$ SI units: N, m, Pa, kg",
        f"SOL {solution}",
        "CEND",
        "TITLE = AFDT CANTILEVER BENCHMARK",
        "SUBCASE 1",
        "  SPC = 1",
        "  LOAD = 1",
        "  DISPLACEMENT(PLOT,PRINT) = ALL",
        "  SPCFORCES(PRINT) = ALL",
        "  FORCE(PRINT) = ALL",
        "BEGIN BULK",
        "PARAM,POST,-1",
        f"MAT1,1,{model.elastic_modulus_Pa:.9E},,{model.poisson:.8f},{model.density_kg_m3:.9E}",
        f"PBEAM,1,1,{area:.9E},{iz:.9E},{iy:.9E},{j:.9E}",
    ]
    dx = model.length_m / model.elements
    for index in range(model.elements + 1):
        lines.append(f"GRID,{index + 1},,{index * dx:.9E},0.,0.")
    for index in range(model.elements):
        lines.append(f"CBEAM,{index + 1},1,{index + 1},{index + 2},0.,1.,0.")
    lines.extend([
        "SPC1,1,123456,1",
        f"FORCE,1,{model.elements + 1},0,{model.tip_force_N:.9E},0.,0.,-1.",
        "ENDDATA",
        "",
    ])
    return "\n".join(lines)


def ansys_cantilever_apdl(model: BeamBenchmark) -> str:
    """Generate a Mechanical APDL BEAM188 cantilever benchmark."""
    model.validate()
    area = model.width_m * model.height_m
    iy = model.width_m * model.height_m**3 / 12
    iz = model.height_m * model.width_m**3 / 12
    lines = [
        "! AeroFrame-DT cantilever verification deck",
        "! SI units: N, m, Pa, kg",
        "/CLEAR",
        "/PREP7",
        "ET,1,BEAM188",
        f"MP,EX,1,{model.elastic_modulus_Pa:.12E}",
        f"MP,PRXY,1,{model.poisson:.12E}",
        f"MP,DENS,1,{model.density_kg_m3:.12E}",
        "SECTYPE,1,BEAM,RECT,AFDT_RECT",
        f"SECDATA,{model.width_m:.12E},{model.height_m:.12E}",
    ]
    dx = model.length_m / model.elements
    for index in range(model.elements + 1):
        lines.append(f"N,{index + 1},{index * dx:.12E},0,0")
    for index in range(model.elements):
        lines.append(f"E,{index + 1},{index + 2}")
    lines.extend([
        "D,1,ALL,0",
        f"F,{model.elements + 1},FZ,{-abs(model.tip_force_N):.12E}",
        "/SOLU",
        "ANTYPE,STATIC",
        "SOLVE",
        "FINISH",
        "/POST1",
        "SET,LAST",
        f"*GET,AFDT_TIP_UZ,NODE,{model.elements + 1},U,Z",
        "*GET,AFDT_REACT_FZ,NODE,1,RF,FZ",
        "*CFOPEN,afdt_cantilever_results,csv",
        "*VWRITE,'metric,value'",
        "(A)",
        "*VWRITE,'tip_uz_m',AFDT_TIP_UZ",
        "(A,',',E24.16)",
        "*VWRITE,'root_reaction_fz_N',AFDT_REACT_FZ",
        "(A,',',E24.16)",
        "*CFCLOSE",
        "FINISH",
        "",
    ])
    return "\n".join(lines)


def ansys_plate_apdl(model: PlateBenchmark) -> str:
    """Generate a quarter-symmetry SHELL181 simply supported plate deck."""
    model.validate()
    half = model.side_m / 2
    element_size = half / model.divisions
    return f"""! AeroFrame-DT simply-supported square plate verification deck
! Quarter symmetry model, SI units
/CLEAR
/PREP7
ET,1,SHELL181
SECTYPE,1,SHELL
SECDATA,{model.thickness_m:.12E},1
MP,EX,1,{model.elastic_modulus_Pa:.12E}
MP,PRXY,1,{model.poisson:.12E}
BLC4,0,0,{half:.12E},{half:.12E}
ESIZE,{element_size:.12E}
AMESH,ALL
! Symmetry x=0: UX=0 and ROTY=0
NSEL,S,LOC,X,0
D,ALL,UX,0
D,ALL,ROTY,0
! Symmetry y=0: UY=0 and ROTX=0
NSEL,S,LOC,Y,0
D,ALL,UY,0
D,ALL,ROTX,0
! Simply supported outer edges: UZ=0
NSEL,S,LOC,X,{half:.12E}
D,ALL,UZ,0
NSEL,S,LOC,Y,{half:.12E}
D,ALL,UZ,0
ALLSEL,ALL
SFE,ALL,1,PRES,,{model.pressure_Pa:.12E}
/SOLU
ANTYPE,STATIC
SOLVE
FINISH
/POST1
SET,LAST
NSEL,S,LOC,X,0
NSEL,R,LOC,Y,0
*GET,AFDT_CENTER_NODE,NODE,0,NUM,MIN
*GET,AFDT_CENTER_UZ,NODE,AFDT_CENTER_NODE,U,Z
ALLSEL,ALL
*CFOPEN,afdt_plate_results,csv
*VWRITE,'metric,value'
(A)
*VWRITE,'center_uz_m',AFDT_CENTER_UZ
(A,',',E24.16)
*CFCLOSE
FINISH
"""


def production_solver_contract(parameters: Mapping[str, float | str]) -> str:
    """Create a solver-neutral production model input contract."""
    required = {
        "geometry_revision", "load_case_id", "material_id", "mesh_revision",
        "contact_friction", "bolt_preload_N", "solver", "solver_version",
    }
    missing = sorted(required - set(parameters))
    if missing:
        raise KeyError(f"missing production parameters: {', '.join(missing)}")
    rows = ["# AeroFrame-DT Production Solver Contract", "", "```yaml"]
    for key in sorted(parameters):
        rows.append(f"{key}: {parameters[key]}")
    rows.extend([
        "```", "", "## Required outputs", "",
        "- reaction force and moment equilibrium",
        "- integrated contact resultants by interface",
        "- fastener shear/tension resultants",
        "- predeclared averaged structural stresses",
        "- mesh and nonlinear convergence histories",
        "- model mass, modal frequencies, and buckling factors when applicable",
        "- solver warning/error log and exact command line",
        "",
        "Local contact-pressure maxima and unconverged singular stress peaks are not margin quantities.",
    ])
    return "\n".join(rows) + "\n"


def write_text(path: str | Path, text: str) -> None:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(text, encoding="utf-8")


def nastran_quad_patch_bdf(
    elastic_modulus_Pa: float = 70e9,
    poisson: float = 0.33,
    thickness_m: float = 0.01,
    imposed_strain_x: float = 1e-3,
) -> str:
    """Generate a single-CQUAD4 constant-strain patch verification deck."""
    for name, value in (("elastic_modulus_Pa", elastic_modulus_Pa), ("thickness_m", thickness_m)):
        _positive(name, value)
    if not -1 < poisson < .5: raise ValueError("invalid Poisson ratio")
    if imposed_strain_x == 0: raise ValueError("imposed strain must be nonzero")
    ux = imposed_strain_x
    return f"""$ AeroFrame-DT CQUAD4 constant-strain patch
SOL 101
CEND
TITLE = AFDT CONSTANT STRAIN PATCH
SUBCASE 1
 SPC = 1
 DISPLACEMENT(PRINT) = ALL
 STRESS(PRINT) = ALL
 SPCFORCES(PRINT) = ALL
BEGIN BULK
MAT1,1,{elastic_modulus_Pa:.9E},,{poisson:.8f}
PSHELL,1,1,{thickness_m:.9E}
GRID,1,,0.,0.,0.
GRID,2,,1.,0.,0.
GRID,3,,1.,1.,0.
GRID,4,,0.,1.,0.
CQUAD4,1,1,1,2,3,4
SPC1,1,23456,1,THRU,4
SPC1,1,1,1,4
SPCD,1,2,1,{ux:.9E}
SPCD,1,3,1,{ux:.9E}
LOAD,1,1.,1.,1
ENDDATA
"""


def nastran_cantilever_modal_bdf(model: BeamBenchmark, modes: int = 6) -> str:
    model.validate()
    if modes < 1: raise ValueError("modes must be positive")
    static = nastran_cantilever_bdf(model, solution=103)
    lines = static.splitlines()
    output: list[str] = []
    for line in lines:
        if line == "  LOAD = 1": continue
        if line.startswith("  FORCE"): continue
        if line == "BEGIN BULK":
            output.extend(["  METHOD = 10", "BEGIN BULK", f"EIGRL,10,,,{modes}"])
        elif line.startswith("FORCE,1,"): continue
        else: output.append(line)
    return "\n".join(output)


def ansys_cantilever_modal_apdl(model: BeamBenchmark, modes: int = 6) -> str:
    model.validate()
    if modes < 1: raise ValueError("modes must be positive")
    pre = ansys_cantilever_apdl(model).split("/SOLU")[0]
    return pre + f"""/SOLU
ANTYPE,MODAL
MODOPT,LANB,{modes}
MXPAND,{modes},,,,YES
SOLVE
FINISH
/POST1
*CFOPEN,afdt_modal_results,csv
*VWRITE,'mode,frequency_Hz'
(A)
*DO,AFDT_I,1,{modes}
  SET,1,AFDT_I
  *GET,AFDT_F,MODE,AFDT_I,FREQ
  *VWRITE,AFDT_I,AFDT_F
  (I8,',',E24.16)
*ENDDO
*CFCLOSE
FINISH
"""


def ansys_eigen_buckling_apdl(model: BeamBenchmark, preload_N: float, modes: int = 5) -> str:
    model.validate(); _positive("preload_N", preload_N)
    if modes < 1: raise ValueError("modes must be positive")
    pre = ansys_cantilever_apdl(model).split("/SOLU")[0]
    return pre + f"""FDELE,ALL,ALL
F,{model.elements + 1},FX,{-abs(preload_N):.12E}
/SOLU
ANTYPE,STATIC
PSTRES,ON
SOLVE
FINISH
/SOLU
ANTYPE,BUCKLE
BUCOPT,LANB,{modes}
MXPAND,{modes}
SOLVE
FINISH
/POST1
*CFOPEN,afdt_buckling_results,csv
*VWRITE,'mode,load_factor'
(A)
*DO,AFDT_I,1,{modes}
  SET,1,AFDT_I
  *GET,AFDT_LAMBDA,MODE,AFDT_I,FREQ
  *VWRITE,AFDT_I,AFDT_LAMBDA
  (I8,',',E24.16)
*ENDDO
*CFCLOSE
FINISH
"""


def ansys_contact_template(parameters: Mapping[str, float | str]) -> str:
    """Generate a contact-analysis APDL contract requiring premeshed components.

    The returned template expects a CDB with named components TARGET_FACE,
    CONTACT_FACE, FIXED_NODES, and LOAD_NODES. This avoids guessing topology.
    """
    required = {"cdb_path", "elastic_modulus_Pa", "poisson", "friction_coefficient", "normal_force_N", "tangential_force_N"}
    missing = sorted(required - set(parameters))
    if missing: raise KeyError(f"missing contact parameters: {', '.join(missing)}")
    return f"""! AeroFrame-DT nonlinear contact template
! Requires named components in imported CDB; topology is never guessed.
/CLEAR
/PREP7
CDREAD,DB,'{parameters['cdb_path']}'
MP,EX,1,{float(parameters['elastic_modulus_Pa']):.12E}
MP,PRXY,1,{float(parameters['poisson']):.12E}
ET,901,TARGE170
ET,902,CONTA174
KEYOPT,902,12,0
R,902
TB,FRIC,1
TBDATA,1,{float(parameters['friction_coefficient']):.12E}
CMSEL,S,TARGET_FACE
TYPE,901
REAL,902
ESURF
CMSEL,S,CONTACT_FACE
TYPE,902
REAL,902
ESURF
CMSEL,S,FIXED_NODES
D,ALL,ALL,0
CMSEL,S,LOAD_NODES
F,ALL,FZ,{float(parameters['normal_force_N']):.12E}
F,ALL,FX,{float(parameters['tangential_force_N']):.12E}
ALLSEL,ALL
/SOLU
ANTYPE,STATIC
NLGEOM,ON
AUTOTS,ON
NSUBST,20,200,5
CNVTOL,F,,1E-4,2
OUTRES,ALL,ALL
SOLVE
FINISH
/POST1
SET,LAST
! Integrated contact forces must be extracted over CONTACT_FACE.
! Do not use a local pressure peak as a margin quantity.
FINISH
"""
