# Stress Report — Index

**Status:** superseded. **All release gates listed below are now closed.**

**The released stress report is
[`STRESS_REPORT_AF-DT-1000.md`](STRESS_REPORT_AF-DT-1000.md).**

This file was the framework placeholder created before any margin could be released. It is retained
because its §5 gate list is the record of what had to be true first, and closing that list is itself
part of the evidence trail.

---

## Release gates — original list and closure

| Gate | Status | Closed by |
|---|---|---|
| Source-backed representative load cases | **CLOSED** | `loads/LOAD_BASIS_AF-DT-1000_revC.md` — 617,776 N at 59.04°, provenance and frame recorded |
| Frozen geometry revision | **CLOSED** | Rev D, `cad/build_revD.py`, mass verified to 0.01% against FE |
| Product-form-specific material and fastener allowables | **CLOSED** | MIL-HDBK-5J Table 3.7.6.0(b3) p.3-373 — 7075-T7351 plate, **2.001-2.500 in** band, A and B basis, L/LT/ST |
| Safety-factor policy | **CLOSED** | 1.15 fitting factor per FAR 25.625, applied per AA-SM-009-005 for the combined oblique case |
| Benchmark evidence | **CLOSED** | Ekvall (1986), 243 lug tests, predicted/test 0.85-1.19 — `docs/F12_CORRELATION_AF-DT-1000.md` |
| Extraction-rule identifiers | **PARTIAL** | FE extraction locations recorded per run; formal identifier scheme not yet applied |

The material allowable gate was the last to close, and closing it moved the margin from +0.165 to
**+0.078** — the assumed `Ftu = 71 ksi` was 9% optimistic against the A-basis value of 65 ksi.

## Released result

| | |
|---|---|
| **Governing margin** | **`MS = +0.078`** |
| Failure mode | combined bearing / transverse at the lug bore |
| Basis | A-basis allowables, thick-lug corrected, 1.15 fitting factor |

See [`MARGIN_SUMMARY.md`](MARGIN_SUMMARY.md) for the authoritative figure and the full correction
chain, and [`STRESS_REPORT_AF-DT-1000.md`](STRESS_REPORT_AF-DT-1000.md) for the report itself.

## Scope and load path

Representative forward pylon-to-wingbox attachment fitting, educational use only.
Load path per [`LOAD_PATH_AND_FBD.md`](LOAD_PATH_AND_FBD.md).

## Classical methods implemented

Unchanged from the original framework: lug net-section stress; projected bearing stress; two-plane
shear-out using the physical edge ligament; pin and fastener shear; rectangular-section bending;
eccentric fastener-group shear distribution; general elastic fastener-group tension distribution;
simultaneous shear/tension interaction; prying augmentation only when an explicit sourced increment
or factor is supplied.

**Added since:** thick-lug bearing-distribution correction measured by contact FE
(`F7_CONTACT_THICK_LUG.md`), pin bending (`F6_PIN_BENDING_THICK_LUG.md`), and damage tolerance
(`F9_DAMAGE_TOLERANCE.md`, `F9b_SPECTRUM_AND_INTERVAL.md`).

## Claim boundary

Educational / representative / portfolio only. Non-OEM, non-certified. Geometry and load case are
`SYNTHETIC_TEST_ONLY`; the damage-tolerance spectrum is `SYNTHETIC_SPECTRUM`. **Material allowables
are real.** Not checked or approved by a licensed stress engineer.
