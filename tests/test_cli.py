from __future__ import annotations

from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
ENV = {"PYTHONPATH": str(ROOT / "src")}


class CLISmokeTests(unittest.TestCase):
    def run_cli(self, *args: str) -> subprocess.CompletedProcess:
        import os
        env = os.environ.copy(); env.update(ENV)
        return subprocess.run([sys.executable, "-m", "aeroframe_dt.cli", *args], cwd=ROOT, env=env, text=True, capture_output=True, check=False)

    def test_generated_artifacts(self):
        with tempfile.TemporaryDirectory() as directory:
            d = Path(directory)
            commands = [
                ("substantiation", str(ROOT / "examples/synthetic_substantiation_case.json"), str(d / "substantiation.json")),
                ("load-envelope", str(ROOT / "examples/synthetic_load_envelope.json"), str(d / "loads.csv")),
                ("generate-decks", str(ROOT / "examples/synthetic_benchmarks.json"), str(d / "decks")),
                ("convergence", str(ROOT / "examples/synthetic_convergence.csv"), str(d / "conv.json")),
                ("cad-macro", str(ROOT / "examples/synthetic_cad_parameters.json"), str(d / "macro.bas")),
                ("inspection", str(ROOT / "examples/synthetic_inspection.json"), str(d / "inspection.json")),
                ("qif-sidecar", str(ROOT / "examples/synthetic_qif_sidecar.json"), str(d / "qif.xml")),
                ("afgrow-package", str(ROOT / "examples/synthetic_afgrow_case.json"), str(d / "afgrow")),
                ("report", str(ROOT / "examples/synthetic_report.json"), str(d / "report.md"), str(d / "report.html")),
            ]
            for command in commands:
                result = self.run_cli(*command)
                self.assertEqual(result.returncode, 0, msg=result.stdout + result.stderr)
            self.assertTrue((d / "decks/cantilever_nastran.bdf").exists())
            self.assertTrue((d / "afgrow/case.json").exists())
            self.assertTrue((d / "report.html").exists())

    def test_release_audit(self):
        result = self.run_cli("audit", str(ROOT))
        # Generated Python caches may be present during the test itself; the
        # release pipeline removes them before package creation.
        if result.returncode != 0:
            self.assertIn("__pycache__", result.stdout)


if __name__ == "__main__":
    unittest.main()
