# PMI and GD&T Definition — AF-DT-1000

**Closes AFDT-REQ-008.** Defines functional datums, geometric tolerances and inspection
requirements for the Rev D fitting.

**Every tolerance here is derived from the analysis, not selected by convention.** The margin is
`MS = +0.078` — thin enough that geometric variation is a genuine structural concern rather than a
drafting formality. §4 gives the sensitivity of the margin to each controlled feature.

**Claim boundary:** educational / representative / portfolio only. Non-OEM, non-certified.

---

## 1. Datum scheme

Datums are chosen to reflect **how the part is loaded and installed**, not how it is convenient to
machine.

| Datum | Feature | Justification |
|---|---|---|
| **A** | Flange underside, the 16.000 x 6.000 in face | **Primary.** Seats against the wingbox and reacts the entire load. The FE fixed support is applied here (area 6.1688e-2 m²), so it is the analysis reaction plane. |
| **B** | Pattern of 8 fastener holes, ⌀0.250 | **Secondary.** Locates the part in the plane of A and reacts the couple. |
| **C** | Pin bore, ⌀2.000 | **Tertiary.** Clocks the part and is the load introduction feature. |

**A is primary because the analysis says so.** Any deviation from flatness at A redistributes the
reaction and invalidates the fixed-support idealisation used throughout F5 and F7.

## 2. Geometric tolerances

| Feature | Control | Value | Derivation |
|---|---|---|---|
| Datum A flange underside | Flatness | **0.008** | Bolted-joint seating; ensures the fixed-support idealisation holds |
| Pin bore ⌀2.000 | Position to A, B | **⌀0.030 MMC** | §4.2 — margin reaches zero at 0.104 in offset; this is 14% of that |
| Pin bore ⌀2.000 | Size | **+0.002 / −0.000** | §4.3 — preserves the F7 contact clearance basis |
| Pin bore ⌀2.000 | Cylindricity | **0.002** | Bearing distribution; F7 assumed a true cylinder |
| Pin bore ⌀2.000 | Perpendicularity to A | **0.005** | Prevents pin cocking, which F6 does not model |
| Lug thickness 2.500 | Size | **±0.020** | §4.1 — 11% of the 0.182 in that would exhaust the margin |
| Fastener holes ⌀0.250 (8x) | Position to A | **⌀0.014 MMC** | Standard fastener float |
| Blend radii R0.500 | Profile | **0.015** | Stress concentration control at the blade/flange junction |
| All machined surfaces | Roughness | **Ra 63 µin** | General |
| **Pin bore** | **Roughness** | **Ra 32 µin** | §4.4 — crack initiation site, damage tolerance critical |

## 3. Material and process callouts

**Plate orientation — mandatory.** The part shall be machined from plate such that:

    lug axis         -> L  (rolling direction)
    transverse load  -> LT
    bore axis        -> ST

**This is a structural requirement, not a preference.** MIL-HDBK-5J Table 3.7.6.0(b3) gives
`Ftu(ST) = 62 ksi` against 65 and 66 for L and LT, and Table 3.1.2.3.1(b) flags 7075-T7351 as
**stress-corrosion susceptible in ST** with a 39 ksi threshold at this thickness. The orientation
keeps the weakest and most SCC-prone direction out of the primary load path. **An incorrectly
oriented blank is a structural nonconformance, not a cosmetic one.**

**Material:** 7075-T7351 plate per AMS 4078 or AMS-QQ-A-250/12, thickness band 2.001–2.500 in.

**Allowables basis:** A-basis, appropriate to a single-load-path fitting. If a redundant load path
is later demonstrated, B-basis applies and the margin improves to +0.111.

## 4. Tolerance derivation

### 4.1 Lug thickness — rigorous

Thickness appears in `Abr = D*t` and `Atn = (w−D)*t` but **not** in `e/D` or `W/D`, so the
Melcon-Hoblit K factors are unaffected and the sensitivity is exact:

| t (in) | MS |
|---|---|
| 2.500 nominal | +0.0785 |
| 2.480 | +0.0699 |
| 2.460 | +0.0612 |
| 2.440 | +0.0526 |
| 2.400 | +0.0353 |

    dMS/dt = 0.431 per inch
    MS = 0 at t = 2.318 in, i.e. 0.182 in (4.62 mm) of thickness loss

**Tolerance ±0.020 consumes 11% of the available thickness margin.** Comfortable, and thickness is
easy to hold.

### 4.2 Bore position — estimated from the F15 anchor

Edge distance enters `e/D`, which changes `Kt`, `Ktru` and `Kbr` through curves **not digitised in
this project**. The sensitivity is therefore anchored on the F15 nonconformance case, where
`e = 2.500 -> 1.900 in` took the margin from +0.078 to −0.370:

    dMS/de ~ 0.747 per inch
    MS = 0 at de = −0.104 in (−2.65 mm)

**Position tolerance ⌀0.030 permits 0.015 in radial offset — 14% of the 0.104 in that would exhaust
the margin.**

**This is an extrapolation from a single distant anchor and the relationship is not linear** —
the K factors vary nonlinearly with `e/D`. The tolerance is set conservatively for that reason. **A
proper allocation requires the AFFDL curves.**

**The F15 nonconformance was a 0.600 in position error — roughly 20x this tolerance.** That case is
now understood as clearly negative rather than marginal, which is what makes the tight tolerance
defensible.

### 4.3 Bore size

F7 modelled the pin at ⌀1.998 in a ⌀2.000 bore — **0.001 in radial clearance**, and the measured
`t_eff/t = 0.681` is specific to that fit. Bore size of **+0.002/−0.000** holds clearance between
0.001 and 0.002 in radial.

**Clearance affects the contact arc**, which is one of the effects the F7 ratio method deliberately
cancels — so the measured `t_eff` is robust to it. But an interference fit or a grossly oversize
bore would invalidate the model.

### 4.4 Bore surface roughness

`F9_DAMAGE_TOLERANCE.md` establishes `a_c = 3.07 mm` with a rogue-flaw start of 1.27 mm. **The bore
is the crack initiation site.** Ra 32 µin rather than the general Ra 63 reduces initiation risk at
the one location where a crack is critical.

## 5. Inspection requirements

| Characteristic | Method | Acceptance |
|---|---|---|
| Datum A flatness | CMM | 0.008 |
| Bore position | CMM | ⌀0.030 MMC to A, B |
| Bore size and cylindricity | Air gauge or CMM | ⌀2.000 +0.002/−0.000, cyl 0.002 |
| Lug thickness | Micrometer | 2.500 ±0.020 |
| Bore roughness | Profilometer | Ra 32 µin |
| **Bore subsurface** | **Eddy current** | **No indication ≥ 1.27 mm** |
| Material orientation | Certificate review | L/LT/ST per §3 |

**The eddy-current requirement is structural, not quality-assurance boilerplate.** `F9` establishes
that `a_c = 3.07 mm` is **below reliable visual detection**, and the 4,500-flight repeat inspection
interval is predicated on reliably finding a 1.27 mm flaw. **If the NDI method cannot achieve that
threshold, the inspection interval must shorten.**

**The executable inspection plan is `inspection_quality/inspection_plan_AF-DT-1000_revD.csv`**, with
process planning, measurement-system analysis and the tolerance stack in
`F13_MANUFACTURING_INSPECTION.md`.

## 6. Semantic PMI

For STEP AP242 export, each tolerance above shall carry:

- the datum reference frame (A, A-B, or A-B-C as tabulated);
- material condition modifiers where stated (MMC on both position callouts);
- a link to the originating requirement or analysis document.

The last item is what makes the PMI *semantic* rather than decorative: **each tolerance traces to the
analysis that justifies it**, so a tolerance change triggers re-evaluation of the margin it protects.

| Tolerance | Traces to |
|---|---|
| Bore position ⌀0.030 | `F15_NONCONFORMANCE_RCCA_AF-DT-1000.md`, `MARGIN_SUMMARY.md` §6 |
| Lug thickness ±0.020 | `MARGIN_SUMMARY.md` §4 |
| Bore size and cylindricity | `F7_CONTACT_THICK_LUG.md` §2 |
| Bore roughness Ra 32 | `F9_DAMAGE_TOLERANCE.md` §2 |
| Plate orientation | MIL-HDBK-5J Tables 3.7.6.0(b3) and 3.1.2.3.1(b) |
| Eddy current 1.27 mm | `F9b_SPECTRUM_AND_INTERVAL.md` §4 |

**This dependency is now machine-readable.** `F14_DIGITAL_THREAD.md` registers all ten
characteristics as descendants of the margin, and its forward query shows that the pending
elastic-plastic contact run would mark every tolerance in this document stale.

## 7. Limitations

1. **Bore position tolerance is extrapolated**, not derived. The AFFDL K-factor curves would allow a
   proper allocation. The value is set conservatively to compensate.
2. ~~**No statistical tolerance stack** has been performed.~~ **CLOSED by
   `F13_MANUFACTURING_INSPECTION.md` §7.** Simultaneous worst-case deviations take
   **MS +0.0784 → +0.0568**, consuming 27.6% of the margin. The exact thickness term agrees with
   the linearisation of §4.1 to 0.1%. Bore position remains the dominant term and remains
   extrapolated — limitation 1 above is unchanged and is now the binding one.
3. **No thermal or assembly-induced distortion** is considered.
4. **Fastener hole positions** use conventional float allocation rather than an analysed value; the
   fastener group is not the critical feature.
5. **Datum A flatness of 0.008** is a conventional bolted-joint value, not derived from a
   contact-pressure study of the flange interface.
