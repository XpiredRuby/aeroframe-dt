"""
F7 contact model geometry: Rev D lug + steel pin as two separate bodies.

Purpose: measure the through-thickness bearing distribution that the thin-lug
method assumes uniform. At t/D = 1.25 the pin bends and bearing concentrates
toward the lug faces. See docs/F6_PIN_BENDING_THICK_LUG.md - the +0.710 margin
reaches zero at t_eff/t = 0.585, so this measurement decides whether it holds.

Result: t_eff/t = 0.742, MS corrected to about +0.25. See
docs/F7_CONTACT_THICK_LUG.md.

Pin geometry choices, made to match the F6 hand calculation exactly so the two
can be compared:
  - diameter 1.998 in, giving 0.001 in radial clearance in the 2.000 in bore.
    A small clearance avoids initial interference at solve start.
  - length = t1 + 2*gap + t2 = 2.500 + 0.060 + 1.250 = 3.810 in
    This places each flat end at the CENTROID of a balanced-shear clevis ear
    (t2 = 0.5*t1, gap = 0.030 in). Fixing the ends therefore reproduces the
    moment arm t1/4 + g + t2/2 used in the F6 bending calculation.

Requires AF-DT-1000_fitting_revD.step in the working directory, produced by
build_revD.py. Everything is written in MILLIMETRES, so no rescale step is
needed afterwards.

SYNTHETIC_TEST_ONLY. Educational / representative only. Non-OEM, non-certified.
"""

import cadquery as cq
from OCP.gp import gp_Trsf
from OCP.BRepBuilderAPI import BRepBuilderAPI_Transform

MM = 25.4

# ---- lug: reuse the verified Rev D build, rescaled to true millimetres ----
lug_in = cq.importers.importStep("AF-DT-1000_fitting_revD.step").val()
t = gp_Trsf()
t.SetScaleFactor(MM)
lug = cq.Shape.cast(BRepBuilderAPI_Transform(lug_in.wrapped, t, True).Shape())

# ---- pin ----
D_PIN_BORE = 2.000 * MM          # bore diameter, 50.80 mm
D_PIN = 1.998 * MM               # pin diameter, 50.7492 mm -> 0.0127 mm radial clearance
T_LUG = 2.500 * MM               # 63.50
GAP = 0.030 * MM                 # 0.762
T_EAR = 0.500 * 2.500 * MM       # balanced-shear clevis ear, 31.75
L_PIN = T_LUG + 2 * GAP + T_EAR  # 96.774 mm

BORE_Z = 6.500 * MM              # bore axis height, 165.10 mm

pin = (
    cq.Workplane("XZ")
    .workplane(offset=-L_PIN / 2.0)
    .center(0.0, BORE_Z)
    .circle(D_PIN / 2.0)
    .extrude(L_PIN)
    .val()
)

# ---- verify before writing ----
bbl = lug.BoundingBox()
bbp = pin.BoundingBox()
vol_lug = lug.Volume()
vol_pin = pin.Volume()

print("lug  volume %.1f mm^3  mass %.4f kg at 2810" % (vol_lug, vol_lug * 1e-9 * 2810))
print("lug  bbox   X %.2f  Y %.2f  Z %.2f" % (bbl.xlen, bbl.ylen, bbl.zlen))
print("pin  volume %.1f mm^3  mass %.4f kg at 7850" % (vol_pin, vol_pin * 1e-9 * 7850))
print("pin  Y span %.3f .. %.3f  (length %.3f)" % (bbp.ymin, bbp.ymax, bbp.ylen))
print("radial clearance %.4f mm" % ((D_PIN_BORE - D_PIN) / 2.0))

# pin must protrude past both lug faces so the ends are clear of the lug
assert bbp.ymin < -T_LUG / 2.0, "pin does not protrude past the -Y lug face"
assert bbp.ymax > T_LUG / 2.0, "pin does not protrude past the +Y lug face"
assert abs(vol_lug * 1e-9 * 2810 - 7.65) < 0.01, "lug mass gate failed"

# the two bodies must not interfere, or contact will not initialise
inter = lug.intersect(pin)
vi = inter.Volume() if inter is not None else 0.0
print("interference volume %.6f mm^3 (must be ~0)" % vi)
assert vi < 1.0, "lug and pin interfere - contact will fail to initialise"

# ---- export as a two-solid assembly ----
assy = cq.Assembly()
assy.add(cq.Workplane(obj=lug), name="lug")
assy.add(cq.Workplane(obj=pin), name="pin")
assy.save("AF-DT-1000-f7-contact-mm.step")
print("\nwrote AF-DT-1000-f7-contact-mm.step  (2 bodies, millimetres)")

# ---- reference value for interpreting the result ----
P = 617776.0
p_cos = 4.0 * P / (3.141592653589793 * D_PIN_BORE * T_LUG)
print("\npeak contact pressure IF bearing were uniform through thickness:")
print("  p_max = 4P/(pi*D*t) = %.1f MPa" % p_cos)
print("\nNOTE: do not extract t_eff by dividing this by the measured peak. The")
print("measured peak also contains circumferential concentration from the radial")
print("clearance, which is unrelated to pin bending. Use the stiff-pin ratio")
print("method instead - see docs/F7_CONTACT_THICK_LUG.md section 3.")
