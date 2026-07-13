from __future__ import annotations

import json
import math
from pathlib import Path
import tempfile
import unittest

from aeroframe_dt.correlation import correlation_record, metrics
from aeroframe_dt.materials import FastenerCandidate, MaterialCandidate, rank_fasteners, rank_materials
from aeroframe_dt.units import Quantity, convert
from aeroframe_dt.uncertainty import UniformVariable, latin_hypercube, probability_of_failure
from aeroframe_dt.step_ap242 import compare_pmi_inventory, inventory_step_text
from aeroframe_dt.f06 import parse_buckling_eigenvalues, parse_grid_displacements, parse_real_eigenvalues
from aeroframe_dt.afgrow import AFGROWCase, compare_growth_histories, parse_growth_csv, write_neutral_package
from aeroframe_dt.batch import ansys_batch_run, nastran_batch_run
from aeroframe_dt.cad_automation import CADParameter, freecad_parameter_macro, solidworks_global_variables_macro, validate_functional_constraints
from aeroframe_dt.convergence import ConvergencePoint, assess_convergence, compare_solver_results
from aeroframe_dt.digital_exchange import qif_style_inspection_xml, validate_qif_sidecar
from aeroframe_dt.dynamics import cantilever_bending_frequency_Hz, compare_frequency, euler_column_buckling_load_N, single_dof_transmissibility
from aeroframe_dt.extraction import extraction_summary, integrate_force_moment, integrate_tractions, linearize_stress_through_thickness, weighted_average
from aeroframe_dt.inspection import Nonconformance, capability, crossed_gage_rr, disposition_complete
from aeroframe_dt.load_cases import LoadCombination, combine_resultants, load_cases_from_json
from aeroframe_dt.manifest import RunManifest, sha256_file
from aeroframe_dt.optimization import DesignVariable, evaluate_candidates, full_factorial, pareto_front
from aeroframe_dt.release import audit_repository, create_source_release
from aeroframe_dt.reporting import ReportSection, engineering_report, markdown_to_basic_html
from aeroframe_dt.solver_decks import BeamBenchmark, PlateBenchmark, ansys_cantilever_apdl, ansys_plate_apdl, nastran_cantilever_bdf, production_solver_contract, nastran_quad_patch_bdf, nastran_cantilever_modal_bdf, ansys_cantilever_modal_apdl, ansys_eigen_buckling_apdl, ansys_contact_template
from aeroframe_dt.solver_results import ResultRecord, metric_map, validate_equilibrium, write_long_csv, read_long_csv
from aeroframe_dt.substantiation import run_substantiation

ROOT = Path(__file__).resolve().parents[1]


class SubstantiationPipelineTests(unittest.TestCase):
    def test_integrated_pipeline(self):
        data = json.loads((ROOT / "examples/synthetic_substantiation_case.json").read_text())
        result = run_substantiation(data)
        self.assertEqual(result.status, "PASS")
        self.assertGreater(len(result.checks), 8)
        self.assertLess(max(abs(x) for x in result.equilibrium_force_residual_N), 1e-9)
        self.assertIsNotNone(result.governing_check)
        for row in result.checks:
            self.assertTrue(row["allowable_source_id"])
            self.assertTrue(row["safety_factor_source_id"])


class LoadEnvelopeTests(unittest.TestCase):
    def test_load_case_json_and_combination(self):
        cases = load_cases_from_json(ROOT / "examples" / "synthetic_load_envelope.json")
        self.assertEqual(len(cases), 2)
        combination = LoadCombination("COMB-1", {"SYNTH-LC-001": 1.0, "SYNTH-LC-002": 0.5}, "SYNTHETIC", "A", "unit test")
        result = combine_resultants(combination, cases)
        self.assertAlmostEqual(result.force_N[0], -15000.0)
        self.assertAlmostEqual(result.force_N[2], -90000.0)


class ConvergenceTests(unittest.TestCase):
    def test_convergence_and_solver_comparison(self):
        points = [
            ConvergencePoint(0.08, 101.0), ConvergencePoint(0.04, 100.25),
            ConvergencePoint(0.02, 100.0625), ConvergencePoint(0.01, 100.015625),
        ]
        result = assess_convergence(points, 0.02)
        self.assertTrue(result.monotonic)
        self.assertAlmostEqual(result.apparent_order, 2.0, places=10)
        self.assertTrue(result.passed)
        self.assertTrue(compare_solver_results(100.0, 101.0, 0.02)["passed"])

    def test_nonmonotonic_rejected(self):
        result = assess_convergence([ConvergencePoint(0.04, 10), ConvergencePoint(0.02, 11), ConvergencePoint(0.01, 10.5)])
        self.assertFalse(result.monotonic)
        self.assertFalse(result.passed)


class DynamicsTests(unittest.TestCase):
    def test_dynamics_oracles(self):
        f1 = cantilever_bending_frequency_Hz(1, 1.0, 70e9, 1e-6, 2.8)
        self.assertGreater(f1, 0)
        self.assertGreater(euler_column_buckling_load_N(70e9, 1e-6, 1.0), 0)
        self.assertGreater(single_dof_transmissibility(1.0, 0.05), 1.0)
        self.assertTrue(compare_frequency(1, f1, f1 * 1.02, 0.05).passed)


class DeckTests(unittest.TestCase):
    def setUp(self):
        self.beam = BeamBenchmark(1.0, 0.04, 0.08, 70e9, 0.33, 2800, 1000, 10)
        self.plate = PlateBenchmark(1.0, 0.01, 70e9, 0.33, 1000, 10)

    def test_decks_have_required_controls(self):
        bdf = nastran_cantilever_bdf(self.beam)
        self.assertIn("SPC1,1,123456,1", bdf)
        self.assertIn("GRID,11", bdf)
        apdl = ansys_cantilever_apdl(self.beam)
        self.assertIn("ANTYPE,STATIC", apdl)
        self.assertIn("AFDT_TIP_UZ", apdl)
        plate = ansys_plate_apdl(self.plate)
        self.assertIn("SHELL181", plate)
        self.assertIn("AFDT_CENTER_UZ", plate)
        patch = nastran_quad_patch_bdf()
        self.assertIn("CQUAD4", patch)
        self.assertIn("SPCD,1,3,1", patch)
        self.assertIn("SOL 103", nastran_cantilever_modal_bdf(self.beam))
        self.assertIn("ANTYPE,MODAL", ansys_cantilever_modal_apdl(self.beam))
        self.assertIn("ANTYPE,BUCKLE", ansys_eigen_buckling_apdl(self.beam, 1000))
        contact = ansys_contact_template({"cdb_path":"mesh.cdb","elastic_modulus_Pa":70e9,"poisson":.33,"friction_coefficient":.2,"normal_force_N":-1000,"tangential_force_N":100})
        self.assertIn("CONTA174", contact)
        self.assertIn("Integrated contact forces", contact)

    def test_production_contract_requires_provenance(self):
        with self.assertRaises(KeyError):
            production_solver_contract({"solver": "ANSYS"})
        text = production_solver_contract({
            "geometry_revision": "A", "load_case_id": "LC", "material_id": "MAT",
            "mesh_revision": "M1", "contact_friction": 0.2, "bolt_preload_N": 10,
            "solver": "ANSYS", "solver_version": "2026",
        })
        self.assertIn("integrated contact resultants", text)


class F06ExtendedTests(unittest.TestCase):
    def test_modal_displacement_and_buckling_tables(self):
        modal = "REAL EIGENVALUES\n 1 1 3.94784E+01 6.28318E+00 1.00000E+00 2.00000E+00 7.89568E+01\n PAGE 1\n"
        self.assertEqual(parse_real_eigenvalues(modal)[0]["cycles_Hz"], 1.0)
        disp = "D I S P L A C E M E N T   V E C T O R\n 10 G 1.0E-3 2.0E-3 3.0E-3 0.0 0.0 0.0\n PAGE 2\n"
        self.assertEqual(parse_grid_displacements(disp)[0]["t3"], 0.003)
        buckling = "BUCKLING EIGENVALUES\n 1 2.50E+00\n 2 4.00E+00\n PAGE 3\n"
        self.assertEqual(parse_buckling_eigenvalues(buckling)[1]["load_factor"], 4.0)


class SolverResultTests(unittest.TestCase):
    def test_long_result_roundtrip_and_equilibrium(self):
        row = ResultRecord("R1", "LC1", "A", "M1", "TEST", "1", "tip_uz", -0.001, "m", "node displacement", "tip")
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "results.csv"
            write_long_csv([row], path)
            loaded = read_long_csv(path)
            self.assertEqual(metric_map(loaded)["tip_uz"], -0.001)
        eq = validate_equilibrium((10, -5, 2), (1, 2, 3), (-10, 5, -2), (-1, -2, -3))
        self.assertTrue(eq["passed"])


class CADAndExchangeTests(unittest.TestCase):
    def test_macros_and_constraints(self):
        params = [CADParameter("hole_diameter", 40, "mm", 20, 70, "hole")]
        self.assertIn("UpsertEquation", solidworks_global_variables_macro(params))
        self.assertIn("Spreadsheet::Sheet", freecad_parameter_macro(params))
        violations = validate_functional_constraints({"lug_width_m": .1, "hole_diameter_m": .04, "lug_thickness_m": .02, "edge_distance_m": .04, "flange_thickness_m": .01})
        self.assertTrue(any("1.5D" in item for item in violations))

    def test_qif_sidecar(self):
        xml = qif_style_inspection_xml("P", "A", [{"id": "C1", "feature_id": "F1", "requirement_id": "R1", "nominal": 1, "lower": .9, "upper": 1.1, "units": "mm", "method": "CMM"}])
        self.assertEqual(validate_qif_sidecar(xml), [])
        self.assertIn("OPEN_EQUIVALENT_NOT_SCHEMA_VALID_QIF", xml)


class CorrelationAndSTEPTests(unittest.TestCase):
    def test_blind_correlation_preserves_predictions(self):
        record = correlation_record(["S1", "S2"], [10.0, 20.0], [9.0, 22.0], [9.8, 20.5], {"mu": 0.2}, {"mu": 0.25}, {"dataset_id": "D1"})
        self.assertIn("blind_metrics", record)
        self.assertEqual(record["rows"][0]["blind_prediction"], 9.0)
        self.assertIn("mu", record["parameter_changes"])
        self.assertGreater(metrics([1, 2], [1, 2]).r_squared, 0.99)

    def test_step_inventory_screen(self):
        text = "ISO-10303-21;HEADER;FILE_SCHEMA(('AP242_MANAGED_MODEL_BASED_3D_ENGINEERING_MIM_LF'));ENDSEC;DATA;#1=DATUM('A');#2=POSITION_TOLERANCE('P');ENDSEC;END-ISO-10303-21;"
        inv = inventory_step_text(text)
        self.assertTrue(inv.likely_ap242)
        self.assertEqual(inv.pmi_entity_types["DATUM"], 1)
        self.assertTrue(compare_pmi_inventory(["C1", "C2"], inv)["passed_inventory_screen"])


class ExtractionAndUncertaintyTests(unittest.TestCase):
    def test_structural_extraction(self):
        self.assertAlmostEqual(weighted_average([10, 20], [1, 3]), 17.5)
        force = integrate_tractions([(10, 0, 0), (20, 0, 0)], [2, 1])
        self.assertEqual(force, (40, 0, 0))
        resultant, moment = integrate_force_moment([(0, 1, 0)], [(10, 0, 0)])
        self.assertEqual(resultant, (10, 0, 0)); self.assertEqual(moment, (0, 0, -10))
        linear = linearize_stress_through_thickness([-1, 0, 1], [80, 100, 120])
        self.assertAlmostEqual(linear.membrane_Pa, 100)
        self.assertAlmostEqual(linear.bending_gradient_Pa_per_m, 20)
        self.assertIn("singularity", extraction_summary([1, 2, 100])["warning"])

    def test_latin_hypercube_and_failure_probability(self):
        variables = [UniformVariable("x", 0, 1)]
        first = latin_hypercube(lambda d: d["x"], variables, 100, 9)
        second = latin_hypercube(lambda d: d["x"], variables, 100, 9)
        self.assertEqual(first, second)
        self.assertEqual(probability_of_failure([-1, 1, -2, 3]), .5)


class InspectionTests(unittest.TestCase):
    def test_capability_gage_rr_and_ncr(self):
        cap = capability([9.99, 10.0, 10.01, 10.0], 9.8, 10.2)
        self.assertGreater(cap.cpk, 1)
        rr = crossed_gage_rr({
            "P1": {"A": [1.0, 1.01], "B": [1.0, 1.02]},
            "P2": {"A": [2.0, 2.01], "B": [2.0, 2.02]},
        })
        self.assertGreaterEqual(rr.percent_gage_rr, 0)
        ncr = Nonconformance("N1", "C1", 1.2, "limit", "contain", "assess", "rework", "cause", "action", "verify", "A", "CLOSED")
        self.assertTrue(disposition_complete(ncr))


class UnitsAndTradeTests(unittest.TestCase):
    def test_explicit_unit_conversion(self):
        self.assertAlmostEqual(Quantity(1, "in").to_si(), 0.0254)
        self.assertAlmostEqual(convert(1, "ksi", "MPa"), 6.894757293168)

    def test_source_gated_material_fastener_trade(self):
        mats = [
            MaterialCandidate("M1", "A", "plate", "T", 2800, 70e9, .33, 400e6, 250e6, 600e6, "SRC", "PUBLISHED", "", ""),
            MaterialCandidate("M2", "B", "plate", "T", 4400, 110e9, .34, 800e6, 450e6, 900e6, "SRC", "PUBLISHED", "", ""),
        ]
        ranked = rank_materials(mats, .001, 100e6, 80e6, 200e6)
        self.assertEqual(ranked[0]["material_id"], "M1")
        fasteners = [FastenerCandidate("F1", "S1", "Ti", .01, 10000, 8000, 5000, "SRC", "PUBLISHED")]
        self.assertTrue(rank_fasteners(fasteners, 1000, 1000)[0]["feasible"])


class OptimizationTests(unittest.TestCase):
    def test_doe_evaluation_and_pareto(self):
        designs = full_factorial([DesignVariable("t", 1, 2, 2), DesignVariable("w", 2, 3, 2)])
        self.assertEqual(len(designs), 4)
        rows = evaluate_candidates(designs, lambda d: {"mass_kg": d["t"] * d["w"], "nominal_margin": d["t"] - 1, "robust_margin": d["t"] - 1.1, "manufacturable": True, "constraints": {"g": d["w"] - 2}})
        self.assertEqual(len(rows), 4)
        self.assertGreaterEqual(len(pareto_front(rows)), 1)


class AFGROWTests(unittest.TestCase):
    def test_neutral_package_and_parser(self):
        case = AFGROWCase("C1", "edge", "SOURCE", "SPECTRUM", .001, .005, .05, 80e6, "A")
        with tempfile.TemporaryDirectory() as directory:
            paths = write_neutral_package(case, [{"sequence": 1, "cycles": 10, "stress_max_Pa": 2, "stress_min_Pa": 1}], directory)
            self.assertTrue(all(path.exists() for path in paths))
            growth = Path(directory) / "growth.csv"
            growth.write_text("cycles,crack_length_m\n0,0.001\n10,0.002\n", encoding="utf-8")
            rows = parse_growth_csv(growth)
            self.assertEqual(compare_growth_histories(rows, rows)["max_relative_error"], 0)


class DigitalThreadExtendedTests(unittest.TestCase):
    def test_export_audit_and_revision(self):
        from aeroframe_dt.digital_thread import EvidenceGraph
        with tempfile.TemporaryDirectory() as directory:
            graph = EvidenceGraph(Path(directory) / "evidence.db")
            graph.add_artifact("REQ", "requirement", "A", metadata={"owner":"stress"})
            graph.add_artifact("CAD", "cad", "A")
            graph.add_artifact("FE", "analysis", "A")
            graph.link("REQ", "CAD", "allocated_to"); graph.link("CAD", "FE", "analyzed_by")
            self.assertEqual(graph.audit(), [])
            self.assertIn("digraph", graph.export_dot())
            impacted = graph.revise_artifact("CAD", "B", "thickness change")
            self.assertEqual(impacted, ["CAD", "FE"])
            self.assertEqual(graph.artifact("FE")["status"], "STALE")
            self.assertEqual(graph.artifact("REQ")["metadata"].get("owner"), "stress")
            graph.close()


class ManifestReleaseReportingTests(unittest.TestCase):
    def test_manifest_hash_report_and_release(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "x.txt").write_text("abc", encoding="utf-8")
            manifest = RunManifest("R1", "TEST", "1", "PASS")
            manifest.add_file(root / "x.txt", "input")
            out = root / "manifest.json"; manifest.write(out)
            self.assertEqual(sha256_file(root / "x.txt"), json.loads(out.read_text())["inputs"][0]["sha256"])
        report = engineering_report("Title", "D1", "A", [ReportSection("Scope", "Body")], ["Limit"], [{"artifact": "x", "status": "PASS"}])
        self.assertIn("Evidence index", report)
        self.assertIn("<h1>Title</h1>", markdown_to_basic_html(report, "Title"))

    def test_repo_audit_no_errors_after_cache_cleanup(self):
        issues = audit_repository(ROOT)
        errors = [item for item in issues if item.severity == "ERROR" and "__pycache__" not in item.path]
        self.assertEqual(errors, [])


class BatchTests(unittest.TestCase):
    def test_batch_commands_are_argv_not_shell(self):
        ansys = ansys_batch_run("R", "ansys", "in.dat", "out.log", ".", 4)
        self.assertEqual(ansys.command[:3], ("ansys", "-b", "-np"))
        nastran = nastran_batch_run("R", "nastran", "m.bdf", ".", "scratch")
        self.assertIn("scr=scratch", nastran.command)


if __name__ == "__main__":
    unittest.main()
