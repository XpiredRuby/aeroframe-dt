from __future__ import annotations

import math
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from aeroframe_dt.hand_calcs import (
    fastener_group_shear,
    fastener_group_tension,
    lug_net_section,
    margin_of_safety,
    pin_shear,
    projected_bearing,
    rectangular_plate_bending,
    resultant_2d,
    shear_tension_interaction,
    tension_with_explicit_prying,
    two_plane_shear_out,
)


class HandCalculationTests(unittest.TestCase):
    def test_basic_stresses(self) -> None:
        self.assertAlmostEqual(lug_net_section(1200, 0.10, 0.04, 0.02).demand, 1_000_000.0)
        self.assertAlmostEqual(projected_bearing(800, 0.04, 0.02).demand, 1_000_000.0)
        self.assertAlmostEqual(two_plane_shear_out(1200, 0.05, 0.04, 0.02).demand, 1_000_000.0)
        expected_pin = 1000 / (2 * math.pi * 0.02**2 / 4)
        self.assertAlmostEqual(pin_shear(1000, 0.02, 2).demand, expected_pin)
        self.assertAlmostEqual(rectangular_plate_bending(100, 0.05, 0.01).demand, 120_000_000.0)

    def test_margin(self) -> None:
        self.assertAlmostEqual(margin_of_safety(300.0, 100.0, 1.5), 1.0)
        self.assertTrue(math.isinf(margin_of_safety(300.0, 0.0)))

    def test_fastener_group_shear_equilibrium(self) -> None:
        points = [(-1.0, -1.0), (-1.0, 1.0), (1.0, -1.0), (1.0, 1.0)]
        loads = fastener_group_shear(points, (40.0, 20.0), 80.0)
        self.assertAlmostEqual(sum(v[0] for v in loads), 40.0)
        self.assertAlmostEqual(sum(v[1] for v in loads), 20.0)
        moment = sum(x * fy - y * fx for (x, y), (fx, fy) in zip(points, loads))
        self.assertAlmostEqual(moment, 80.0)

    def test_fastener_group_tension_equilibrium(self) -> None:
        points = [(-1.0, -1.0), (-1.0, 1.0), (1.0, -1.0), (1.0, 1.0)]
        loads = fastener_group_tension(points, 100.0, 40.0, -20.0)
        self.assertAlmostEqual(sum(loads), 100.0)
        self.assertAlmostEqual(sum(y * q for (_, y), q in zip(points, loads)), 40.0)
        self.assertAlmostEqual(sum(-x * q for (x, _), q in zip(points, loads)), -20.0)

    def test_interaction_and_prying(self) -> None:
        result = shear_tension_interaction(50, 100, 25, 100, exponent=1.0)
        self.assertAlmostEqual(result.demand, 0.75)
        self.assertAlmostEqual(result.margin, 1 / 0.75 - 1)
        self.assertAlmostEqual(tension_with_explicit_prying(100, prying_factor=0.2), 120)
        self.assertAlmostEqual(tension_with_explicit_prying(100, prying_increment_N=15), 115)
        with self.assertRaises(ValueError):
            tension_with_explicit_prying(100)

    def test_resultant(self) -> None:
        self.assertEqual(resultant_2d((3, 4)), 5)


if __name__ == "__main__":
    unittest.main()
