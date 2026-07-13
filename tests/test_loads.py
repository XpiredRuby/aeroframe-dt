from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from aeroframe_dt.loads import AppliedLoad, Resultant, SupportModel, assemble_resultant, solve_two_station_supports


class LoadModelTests(unittest.TestCase):
    def test_resultant_includes_moment_arm(self) -> None:
        result = assemble_resultant([AppliedLoad("L1", (2.0, 0.0, 0.0), (0.0, 0.0, -10.0))])
        self.assertEqual(result.force_N, (0.0, 0.0, -10.0))
        self.assertEqual(result.moment_Nm, (0.0, 20.0, 0.0))

    def test_two_station_equilibrium(self) -> None:
        result = Resultant((100.0, 50.0, -200.0), (30.0, 80.0, -40.0), (0.0, 0.0, 0.0))
        model = SupportModel(2.0, 0.6, 0.5, fitting_gauge_m=1.0)
        solution = solve_two_station_supports(result, model)
        self.assertLess(solution.residual_force_norm_N, 1e-12)
        self.assertLess(solution.residual_moment_norm_Nm, 1e-12)
        self.assertAlmostEqual(solution.aft_station_reaction_N[2], 40.0)
        self.assertAlmostEqual(solution.aft_station_reaction_N[1], 20.0)

    def test_invalid_share_rejected(self) -> None:
        with self.assertRaises(ValueError):
            solve_two_station_supports(
                Resultant((0, 0, 0), (0, 0, 0), (0, 0, 0)),
                SupportModel(1.0, 1.2, 0.5),
            )


if __name__ == "__main__":
    unittest.main()
