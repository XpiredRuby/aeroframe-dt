"""
Rescale the Rev D fitting from inch-valued coordinates to true millimetres.

`build_revD.py` works in inches, but cadquery's STEP exporter declares
`SI_UNIT(.MILLI.,.METRE.)`. The exported file therefore describes a part 25.4x
too small - 16 mm long instead of 16 in, and about 0.47 grams instead of 7.65 kg.
Importing that file straight into a millimetre-based FE tool silently produces a
model of the wrong size, and every stress result from it would be meaningless.

This script applies a uniform 25.4 scale so the exported STEP is physically
correct when read in millimetres, and verifies against the published Rev D
figures before writing anything. If any gate fails it raises rather than
producing a file.

Run after build_revD.py, in the same directory.

Verified output:
    volume    2,723,301 mm^3 = 2.7233e-3 m^3
    mass      7.6525 kg at 2810 kg/m^3   (published Rev D target 7.65 kg)
    bbox      406.40 x 152.40 x 228.60 mm   (16 x 6 x 9 in)
    bore      1 continuous cylindrical face, r = 25.40 mm
    bore area 10,134.1 mm^2 = 1.0134e-2 m^2

SYNTHETIC_TEST_ONLY. Educational / representative only. Non-OEM, non-certified.
"""

import cadquery as cq
from OCP.gp import gp_Trsf
from OCP.BRepBuilderAPI import BRepBuilderAPI_Transform
from OCP.BRepAdaptor import BRepAdaptor_Surface
from OCP.GeomAbs import GeomAbs_SurfaceType
from collections import Counter

IN_TO_MM = 25.4
DENSITY = 2810.0          # kg/m^3
D_PIN_IN = 2.000
T_LUG_IN = 2.500

src = cq.importers.importStep("AF-DT-1000_fitting_revD.step").val()

trsf = gp_Trsf()
trsf.SetScaleFactor(IN_TO_MM)
scaled = cq.Shape.cast(BRepBuilderAPI_Transform(src.wrapped, trsf, True).Shape())

vol_mm3 = scaled.Volume()
vol_m3 = vol_mm3 * 1e-9
mass = vol_m3 * DENSITY
bb = scaled.BoundingBox()

print("volume   : %.1f mm^3   = %.6e m^3" % (vol_mm3, vol_m3))
print("mass     : %.4f kg   (target 7.65)" % mass)
print("bbox mm  : X %.2f  Y %.2f  Z %.2f" % (bb.xlen, bb.ylen, bb.zlen))
print("bbox Z   : %.2f .. %.2f" % (bb.zmin, bb.zmax))

# cylindrical face inventory - confirms bore, fasteners and blends survived
radii = []
for f in scaled.Faces():
    a = BRepAdaptor_Surface(f.wrapped)
    if a.GetType() == GeomAbs_SurfaceType.GeomAbs_Cylinder:
        radii.append(round(a.Cylinder().Radius(), 4))
print("cyl radii:", dict(Counter(radii)))

r_bore = D_PIN_IN / 2 * IN_TO_MM
n_bore = sum(1 for r in radii if abs(r - r_bore) < 1e-3)
bore_area_mm2 = 3.141592653589793 * D_PIN_IN * IN_TO_MM * T_LUG_IN * IN_TO_MM
print("bore     : %d face(s) at r = %.2f mm" % (n_bore, r_bore))
print("bore area: %.1f mm^2 = %.4e m^2" % (bore_area_mm2, bore_area_mm2 * 1e-6))

# gates - refuse to write a file that fails them
assert abs(mass - 7.65) < 0.01, "mass gate failed: %.4f" % mass
assert abs(bb.xlen - 16.0 * IN_TO_MM) < 1e-3, "station length wrong"
assert abs(bb.ylen - 6.0 * IN_TO_MM) < 1e-3, "flange width wrong"
assert n_bore >= 1, "pin bore missing after scaling"

cq.exporters.export(scaled, "AF-DT-1000_fitting_revD_mm.step")
print("\nwrote AF-DT-1000_fitting_revD_mm.step")
