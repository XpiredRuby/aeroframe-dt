# Software Access and No-Purchase Validation Plan

## 1. Confirmed Texas A&M student software

Texas A&M's public eligibility page lists student access to:

- Altair 2025–2026
- ANSYS 2026–2027
- MATLAB 2026
- SOLIDWORKS Student Premium 2026–2027
- STAR-CCM+ 2026–2027
- Tecplot Academic Suite
- LabVIEW System Design
- Microsoft Azure for Students

Access can depend on department participation and exceptions.

## 2. HPRC options

TAMU HPRC documents:

- STAR-CCM+
- ANSYS
- COMSOL
- OpenFOAM
- MATLAB and scientific software

Some HPRC access may require an account, faculty sponsor, course connection, license tokens, and batch-queue use.

## 3. Free industry-relevant tools

### Flight software and autonomy
- ROS 2
- NASA cFS
- OpenCV
- Eigen
- GTSAM
- CMake
- GTest
- Docker/Podman
- GitHub Actions

### Aircraft and CFD
- OpenVSP/VSPAERO
- AVL
- SU2
- OpenFOAM
- JSBSim
- OpenMDAO
- Tecplot through TAMU

### Space
- GMAT
- Orekit
- poliastro
- STK/PySTK if TAMU academic licensing is available

### Propulsion
- pyCycle
- OpenMDAO
- Cantera
- NASA C-MAPSS
- public compressor/turbine maps

### Digital thread
- Capella
- Papyrus
- SysML-compatible tools where available
- SQLite
- Graphviz
- NIST AP242/QIF benchmark files

## 4. Validation substitutes when physical testing is unavailable

A project may still be top-tier when it uses:

1. public experimental data;
2. independent analytical models;
3. two different solvers;
4. code-to-code comparisons;
5. numerical convergence;
6. uncertainty analysis;
7. frozen blind validation cases;
8. external technical review.

The key is that the validation evidence must not come solely from the model being validated.

## 5. Prohibited portfolio claims

Do not claim:

- certified;
- flight qualified;
- airworthy;
- FAA compliant;
- DO-178C compliant;
- production ready;
- flight proven;
- validated against hardware when only simulated;
- OEM geometry or loads when representative assumptions are used.

Use:

- “DO-178C-inspired”
- “AS9102-style”
- “ARP4754A-informed”
- “representative”
- “public-data validated”
- “software-in-the-loop”
- “hardware-executed on Raspberry Pi”
