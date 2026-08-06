# F25 — Damage Tolerance and Source Closure on 7050-T7451 — AF-DT-1000

**Claim boundary:** educational / representative / portfolio only. Non-OEM, non-certified.

**Source: MMPDS-2026, Volume I, 1 July 2026.**

F23 re-selected the material to 7050-T7451 and F24 re-derived the margin. This document closes the
three remaining consequences: the fracture data, the citation mapping, and the cost basis.

---

## 1. Fracture toughness — read, not carried over

`F9_DAMAGE_TOLERANCE.md` used `K_Ic = 25 ksi-sqrt(in)`, the **L-T minimum for 7075-T7351** from
MIL-HDBK-5J Table 3.1.2.1.6. That value does not apply to the released material.

**MMPDS-2026, 7050-T7451 plate, 5.00–6.00 in thickness, `K_Ic` in ksi-sqrt(in):**

| Orientation | Max | Avg | Min | Lots | Specimens |
|---|---|---|---|---|---|
| **L-T** | 40 | 31 | **27** | 1 | 209 |
| T-L | 30 | 24 | 22 | 1 | 209 |
| S-L | 30 | 26 | 22 | 1 | 213 |

**`K_Ic = 27 ksi-sqrt(in)` is used** — the L-T minimum, matching the chosen grain orientation and
following the same conservative convention F9 applied to 7075.

Note the thickness band matters here too: at 1.00–1.99 in the L-T minimum is 33, falling to 27 at
5.00–6.00 in. **Reading the toughness at the wrong thickness would have been the same class of error
F23 found in the strength allowables**, and in the same favourable-looking direction.

## 2. Critical crack size

Re-solved with the project's own `critical_crack_size` routine, finite-width edge-crack geometry,
ligament width 38.0 mm. Reproducing F9 first as a check on the method:

    7075, K_Ic = 25 ksi-sqrt(in), sigma_tr = 241.2 MPa  ->  a_c = 3.068 mm   (F9 published 3.07)
    7050, K_Ic = 27 ksi-sqrt(in), sigma_tr = 240.5 MPa  ->  a_c = 3.514 mm

The transverse stress falls 0.3% because `t_eff/t` moved from 0.6809 to 0.6828 (F24); the toughness
rises 8%. Both act favourably.

**`a_c = 3.51 mm`, up from 3.07 mm — a 14.5% increase.**

Against the same ligament this is **9.2% of the available ligament**, up from 8.1%.

For reference, using the L-T *average* of 31 rather than the minimum would give 4.39 mm. **The
minimum is retained.**

## 3. Inspection interval — NOT re-derived

`F9b_SPECTRUM_AND_INTERVAL.md` sets a **4,500-flight** interval by integrating Paris crack growth
from the 1.27 mm NDI detection threshold to `a_c`.

**That integration has not been repeated on 7050.** MMPDS-2026 provides `da/dN` data for 7050-T7451
plate at Figures **3.7.4.2.9(a) through (c)**, but those are graphical and have not been digitised by
this project — the same limitation that has always applied to the 7075 curves.

**Direction is favourable but the magnitude is unknown.** `a_c` grew 14.5%, which lengthens the
available growth path, so the existing 4,500-flight interval is conservative *on that count alone*.
**7050's crack growth rate is a different curve and has not been read**, so no claim is made that the
interval is conservative overall. **The 4,500-flight figure should be treated as unverified for the
released material** until the curves are digitised.

This is the largest open item left in the damage tolerance chain and it is a data-digitisation task,
not an analysis task.

## 4. Citation mapping — partially closed

F21 inventoried 32 evidence citations of MIL-HDBK-5J across six locators, all `TO_VERIFY`, with a
standing rule that **no MMPDS locator would be written until the handbook was opened**. It has been.
**MMPDS reassigns the section numbers**, so none of these could have been inferred:

| MIL-HDBK-5J | MMPDS-2026 | Content | Status |
|---|---|---|---|
| Table 3.7.6.0(b3) | **Table 3.7.9.0(b2)** | 7075-T7351 plate allowables | **CONFIRMED** |
| Section 3.7.6.2 | **Section 3.7.9.2** | T73/T7351 — confirmed to contain **no S/N curves** | **CONFIRMED** |
| Figure 3.7.6.2.9(b) | **Figures 3.7.9.2.9(a)–(c)** | 7075 `da/dN` | **CONFIRMED** |
| — | **Table 3.7.4.0(b1)** | **7050-T7451 plate allowables — the released basis** | **CONFIRMED** |
| — | **Figures 3.7.4.2.8(a)–(h)** | 7050-T7451 S/N, incl. notched `Kt = 3.0` | **CONFIRMED** |
| — | **Figures 3.7.4.2.9(a)–(c)** | 7050-T7451 `da/dN` | **CONFIRMED** |
| Table 3.7.6.0(b1) | not located | 7075-T651 plate, F12 correlation basis | **TO_VERIFY** |
| Table 3.1.2.1.6 | not located | `K_Ic` table — the 7050 data in §1 was read, but the MMPDS table number was not recorded | **TO_VERIFY** |
| Table 3.1.2.3.1(b) | not located | SCC thresholds — the 7050 value of 35 ksi was read, table number not recorded | **TO_VERIFY** |

**Three of nine remain unverified**, and are marked as such rather than inferred from the pattern.
The three confirmed reassignments (3.7.6 → 3.7.9) make the pattern look obvious, which is exactly
why the remaining three are not being filled in by analogy: **§3.7.6 in MMPDS is alloy 7056**, and
guessing would have produced citations that looked right and pointed at the wrong material.

## 5. Cost — direction only

F20 modelled recurring cost on `ASSUMED_COST_BASIS` rates that were **not alloy-specific**.

**7050-T7451 plate is more expensive per pound than 7075-T7351** — it is a lower-volume,
thick-section aerospace alloy. F20 found material to be the dominant cost element at nominal and
high rates (60–62% of unit cost), so **the material change raises unit cost, and raises it in the
term that already dominated.**

**No revised figure is given.** Alloy-specific pricing was not available, and inventing one would
violate the rule that made F20's assumed rates acceptable in the first place — that they are
declared assumptions reported as ranges, not quotations.

**What does not change:** buy-to-fly of 5.36 and material utilisation of 18.6% are geometric and
unaffected. The envelope still requires 6.000 in stock. F20's central finding — that cost is set by
the envelope rather than by finished mass — is unaffected.

## 6. Carried forward

| Item | Status |
|---|---|
| **`F13_MANUFACTURING_INSPECTION.md` operation 010** | **calls up 7075-T7351 plate, band 2.001–2.500 in — materially wrong shop instruction, must be amended to 7050-T7451, AMS 4050, 5.001–6.000 in** |
| F13 §64 SCC paragraph | cites 7075's 39 ksi ST threshold; 7050-T7451 is **35 ksi** over 0.750–6.000 in |
| `STRESS_REPORT_AF-DT-1000.md` | §4 allowables, §6.3 margin, §8 damage tolerance all still on 7075 |
| `F9_DAMAGE_TOLERANCE.md` | superseded by §1–2 above; not re-issued |
| `F9b_SPECTRUM_AND_INTERVAL.md` | interval unverified for 7050 — §3 |

## 7. Limitations

1. **The inspection interval is not re-derived.** §3. This is the most consequential gap.
2. **`K_Ic` remains "information only"** in the handbook, not a design allowable — the same caveat
   F9 carried.
3. **One lot.** The 5.00–6.00 in L-T toughness data is from a single lot, 209 specimens. F9's 7075
   L-T basis drew on 65 specimens across more lots. Larger specimen count, narrower lot coverage.
4. **Three citations remain unmapped.** §4.
5. **No cost figure is revised.** §5.
6. The critical crack size assumes the same finite-width edge-crack geometry and ligament width F9
   used, including its documented concern that `F` near the bore exceeds 1.12 and the quoted `a_c`
   is therefore non-conservative. **That limitation transfers unchanged.**
