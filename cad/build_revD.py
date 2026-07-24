"""
AeroFrame-DT :: AF-DT-1000 Forward Pylon-to-Wingbox Attachment Fitting
Parametric rebuild, Rev D.

Changes from Rev A geometry:
  1. t_lug  1.500 -> 2.500 in   (F5 rev B sizing: closes MS at all orientations)
  2. t_web  0.750 -> 1.250 in   (proportion to the thicker lug; also required for
                                 the blend radius to fit - see note below)
  3. Blend radii applied to ALL junction edges, not one.

Rev A used cq.selectors.NearestToPointSelector, which returns a SINGLE edge. Only one
fillet of the intended set was created and the try/except never fired, so the partial
application was silent. This script selects edge groups explicitly and asserts the
resulting face count, so a failure is loud.

Note on r_blend vs t_web: a fillet of radius r on both sides of a web of thickness t
requires 2r < t. With rev A values (r=0.500, t_web=0.750) this is violated (1.000 > 0.750),
which is the likely geometric reason the original fillets could not all be built.

All values SYNTHETIC_TEST_ONLY. Representative / educational. Non-OEM, non-certified.
"""

import cadquery as cq
import json

# ---------------- PARAMETERS (inches) ----------------
P = {
    "d_pin":     2.000,
    "t_lug":     2.500,   # REV D  (was 1.500)
    "w_lug":     4.000,
    "e_center":  2.500,
    "t_flange":  1.000,
    "t_web":     2.500,   # REV D  (was 0.750) - matched to t_lug, constant-thickness blade
    "r_blend":   0.500,
    "g_y":       4.000,   # REV D (was 2.000) - clears the 2.500 blade
    "p_x":       1.500,
    "L_station": 16.000,
    "d_fast":    0.250,
    "web_height": 3.000,
}
d_pin, t_lug, w_lug = P["d_pin"], P["t_lug"], P["w_lug"]
e_center, t_flange, t_web = P["e_center"], P["t_flange"], P["t_web"]
r_blend, g_y, p_x = P["r_blend"], P["g_y"], P["p_x"]
L_station, d_fast, web_height = P["L_station"], P["d_fast"], P["web_height"]

# ---------------- PRE-BUILD CHECKS ----------------
assert e_center > d_pin / 2, "edge distance must leave a positive ligament"
assert w_lug > d_pin, "lug width must exceed pin diameter"
assert 2 * r_blend < t_web, (
    f"blend radius {r_blend} will not fit on a web of thickness {t_web}: "
    f"need 2*r_blend < t_web ({2*r_blend} < {t_web})"
)
assert t_lug > 0 and t_flange > 0
assert g_y / 2 > t_lug / 2 + 2 * d_fast, (
    f"fastener gauge {g_y} puts holes inside the {t_lug} thick blade")
assert (w_lug + 2.0) / 2 - g_y / 2 > 2 * d_fast, "fastener too close to flange edge"

# ---------------- 1. FLANGE ----------------
flange = cq.Workplane("XY").box(
    L_station, w_lug + 2.0, t_flange, centered=(True, True, False)
)

# ---------------- 2. WEB ----------------
web = (
    cq.Workplane("XY")
    .workplane(offset=t_flange)
    .box(w_lug, t_web, web_height, centered=(True, True, False))
)

# ---------------- 3. LUG ----------------
lug_z0 = t_flange + web_height
lug = (
    cq.Workplane("XY")
    .workplane(offset=lug_z0)
    .box(w_lug, t_lug, 2 * e_center, centered=(True, True, False))
)

# ---------------- 4. UNION AND BLEND ----------------
# Blend each junction immediately after its union, selecting edges by a thin
# box around the junction plane. This targets the group, not one nearest edge.
def blend_at_plane(shape, z_plane, radius, pad=0.05):
    sel = cq.selectors.BoxSelector(
        (-L_station, -(w_lug + 4.0), z_plane - pad),
        (L_station,  (w_lug + 4.0), z_plane + pad),
    )
    edges = shape.edges(sel)
    n = len(edges.vals())
    if n == 0:
        raise RuntimeError(f"no edges found at z={z_plane}")
    return shape.edges(sel).fillet(radius), n

fitting = flange.union(web).union(lug)
fitting, n1 = blend_at_plane(fitting, t_flange, r_blend)
print(f"blade/flange junction : filleted {n1} edges at r={r_blend}")
# t_web == t_lug, so blade is constant thickness: no web/lug step to blend.
assert abs(t_web - t_lug) < 1e-9, "rev D assumes constant-thickness blade"

# ---------------- 5. FASTENER HOLES ----------------
fitting = (
    fitting.faces(">Z[0]")
    .workplane(centerOption="CenterOfBoundBox")
    .rarray(p_x, g_y, 4, 2, center=True)
    .hole(d_fast)
)

# ---------------- 6. PIN BORE (transverse, through t_lug, along Y) ----------
lug_top_z = lug_z0 + 2 * e_center
hole_z = lug_top_z - e_center
bore = (
    cq.Workplane("XZ")
    .workplane(offset=-(t_lug / 2 + 1.0))
    .center(0.0, hole_z)
    .circle(d_pin / 2)
    .extrude(t_lug + 2.0)
)
fitting = fitting.cut(bore)

# ---------------- 7. VERIFY ----------------
solid = fitting.val()
vol = solid.Volume()
bb = solid.BoundingBox()
print(f"\nvolume       : {vol:.4f} in^3")
print(f"bbox (in)    : X {bb.xlen:.3f}  Y {bb.ylen:.3f}  Z {bb.zlen:.3f}")
print(f"faces        : {len(solid.Faces())}")
print(f"edges        : {len(solid.Edges())}")

assert abs(bb.ylen - (w_lug + 2.0)) < 1e-6, "flange width wrong"
assert abs(bb.xlen - L_station) < 1e-6, "station length wrong"

# count cylindrical faces to prove the bore and the fillets exist
from OCP.BRepAdaptor import BRepAdaptor_Surface
from OCP.GeomAbs import GeomAbs_SurfaceType
radii = []
for f in solid.Faces():
    a = BRepAdaptor_Surface(f.wrapped)
    if a.GetType() == GeomAbs_SurfaceType.GeomAbs_Cylinder:
        radii.append(round(a.Cylinder().Radius(), 4))
from collections import Counter
print(f"cyl radii    : {dict(Counter(radii))}")

n_bore = sum(1 for r in radii if abs(r - d_pin / 2) < 1e-4)
n_fast = sum(1 for r in radii if abs(r - d_fast / 2) < 1e-4)
n_fill = sum(1 for r in radii if abs(r - r_blend) < 1e-4)
print(f"bore faces {n_bore} | fastener faces {n_fast} | blend faces {n_fill}")
assert n_bore >= 1, "PIN BORE MISSING"
assert n_fast == 8, f"expected 8 fastener holes, found {n_fast}"
assert n_fill >= 4, f"BLEND UNDER-APPLIED: only {n_fill} blend faces (rev A bug)"

# ---------------- 8. EXPORT ----------------
cq.exporters.export(fitting, "AF-DT-1000_fitting_revD.step")
cq.exporters.export(fitting, "AF-DT-1000_fitting_revD.stl")
with open("parameters_revD.json", "w") as fh:
    json.dump(P, fh, indent=2)
print("\nexported: AF-DT-1000_fitting_revD.step / .stl / parameters_revD.json")
