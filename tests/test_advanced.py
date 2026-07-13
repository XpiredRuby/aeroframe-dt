import math, tempfile, unittest
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from aeroframe_dt.benchmarks import cantilever_tip_deflection, simply_supported_square_plate_center_deflection
from aeroframe_dt.digital_thread import EvidenceGraph
from aeroframe_dt.f06 import parse_grid_point_force_balance, resultant
from aeroframe_dt.fatigue import SpectrumBlock, critical_crack_size, miner_damage, paris_growth_cycles
from aeroframe_dt.margins import build_margin_rows, governing_row
from aeroframe_dt.uncertainty import UniformVariable, monte_carlo

class AdvancedTests(unittest.TestCase):
    def test_cantilever(self): self.assertAlmostEqual(cantilever_tip_deflection(100,2,200e9,1e-6),0.0013333333333)
    def test_plate_sign_and_scale(self):
        w=simply_supported_square_plate_center_deflection(1000,1,.01,70e9,.33)
        self.assertGreater(w,0); self.assertLess(w,.01)
    def test_fatigue(self):
        r=miner_damage([SpectrumBlock(1000,120e6,20e6)],1e9,-.1,500e6)
        self.assertGreater(r.miner_damage,0)
        n=paris_growth_cycles(.001,.005,80e6,.05,1e-28,3.0,steps=1000)
        self.assertGreater(n,0)
        ac=critical_crack_size(30e6,150e6,.05)
        self.assertTrue(0<ac<.05)
    def test_margins(self):
        rows=build_margin_rows([{'check_id':'a','margin':.2},{'check_id':'b','margin':-.1}],{'load_case_id':'LC','geometry_revision':'A','source_id':'S','extraction_rule_id':'E','allowable_source_id':'A','safety_factor_source_id':'SF'})
        self.assertEqual(governing_row(rows)['check_id'],'b')
    def test_uncertainty_deterministic(self):
        v=[UniformVariable('x',0,1)]
        self.assertEqual(monte_carlo(lambda d:d['x'],v,100,7),monte_carlo(lambda d:d['x'],v,100,7))
    def test_digital_thread_invalidation(self):
        with tempfile.TemporaryDirectory() as d:
            g=EvidenceGraph(Path(d)/'x.db')
            for i,k in [('R','requirement'),('C','cad'),('A','analysis'),('I','inspection')]: g.add_artifact(i,k,'A')
            g.link('R','C','allocated_to'); g.link('C','A','analyzed_by'); g.link('A','I','verified_by')
            self.assertEqual(g.invalidate_downstream('C','revision'),['C','A','I'])
            g.close()
    def test_f06(self):
        rows=parse_grid_point_force_balance('  10 SPC 1.0D+02 -2.0 3.0 4.0 5.0 6.0\n')
        self.assertEqual(resultant(rows)['fx'],100.0)
if __name__=='__main__': unittest.main()
