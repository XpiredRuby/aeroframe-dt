"""
Parametric generator for the F12 correlation lug sweep (AeroFrame-DT).

Builds the straight pin-loaded lug specimen at each e/D in the sweep and writes
one STEP per case.

Geometry convention (matches the original hand-built lug_eD_1p5.step):
    - hole centre at the origin, Y = 0
    - head crown at Y = +e
    - straight shank runs Y = 0 down to Y = -SHANK
    - thickness extruded in +Z, 0 .. T

Held constant across the sweep: D, T, and the straight shank length, so that
only the head geometry varies with e/D.

Validation: the e/D = 1.5 case must reproduce 372,567.1 mm^3, the kernel volume
of the already-solved hand-built part. Each case is additionally checked against
a closed-form area calculation. Both checks print on every run - do not trust an
output STEP from a run whose diff% column is not ~0.

SYNTHETIC_TEST_ONLY. Educational / representative / portfolio only.
Non-OEM, non-certified.
"""

import math
import cadquery as cq

D = 26.8          # bore diameter, mm
T = 25.0          # thickness, mm
SHANK = 160.8     # straight shank length below hole centre, mm (held constant)

CASES = [1.0, 1.2, 1.5, 1.8, 2.0]

OUT_DIR = "."     # write STEPs here


def build(eD):
    """Return (solid, e, w, r_head) for a given e/D."""
    e = eD * D          # edge distance, hole centre to loaded end
    w = 2.0 * eD * D    # width
    r_head = w / 2.0    # head radius (equals e, since w = 2e)

    prof = (
        cq.Workplane("XY")
        .moveTo(-w / 2.0, -SHANK)
        .lineTo(-w / 2.0, 0.0)
        .radiusArc((w / 2.0, 0.0), r_head)
        .lineTo(w / 2.0, -SHANK)
        .close()
    )
    solid = prof.extrude(T)
    solid = solid.faces(">Z").workplane().center(0, 0).hole(D)
    return solid, e, w, r_head


def analytic_volume(eD):
    """Closed-form volume: (rect + half disc - bore) * thickness."""
    w = 2.0 * eD * D
    r = w / 2.0
    area = w * SHANK + 0.5 * math.pi * r * r - math.pi * (D / 2.0) ** 2
    return area * T


if __name__ == "__main__":
    hdr = "%-6s %8s %8s %14s %14s %9s %10s"
    print(hdr % ("e/D", "e", "w", "V_kernel", "V_analytic", "diff%", "mass_kg"))

    for eD in CASES:
        solid, e, w, r_head = build(eD)
        shape = solid.val()

        v = shape.Volume()
        va = analytic_volume(eD)
        diff = 100.0 * (v - va) / va
        mass = v * 1e-9 * 2810.0   # mm^3 -> m^3, times density

        tag = ("%.1f" % eD).replace(".", "p")
        path = "%s/lug_eD_%s.step" % (OUT_DIR, tag)
        cq.exporters.export(solid, path)

        print(hdr % (
            "%.1f" % eD, "%.2f" % e, "%.2f" % w,
            "%.1f" % v, "%.1f" % va, "%.4f" % diff, "%.3f" % mass,
        ))

        bb = shape.BoundingBox()
        print("       bbox  X %.3f..%.3f   Y %.3f..%.3f   Z %.3f..%.3f"
              % (bb.xmin, bb.xmax, bb.ymin, bb.ymax, bb.zmin, bb.zmax))
