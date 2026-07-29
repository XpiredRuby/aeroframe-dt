# Pin Bending and Thick-Lug Check — AF-DT-1000

**Closes the open item** "Pin bending check at t/D = 1.25 (not covered by thin-lug method)".

**Headline: the +0.710 margin is not robust to the thick-lug assumption.** It reaches zero if
bearing concentrates into 58.5% of the lug thickness. This is the most significant caveat on the
margin found so far, and it is larger than the Ftux sensitivity already recorded.

**Claim boundary:** educational / representative / portfolio only. Non-OEM, non-certified.
All numbers `SYNTHETIC_TEST_ONLY`.

---

## 1. Why this check is needed

    t / D = 63.5 / 50.8 = 1.250

The Melcon-Hoblit method used for the +0.710 margin is a **thin-lug** method. It assumes bearing
pressure is **uniform through the lug thickness**. That assumption degrades as t/D rises, because
the pin bends under load and the lug bears harder near its faces than at mid-thickness.

Common guidance treats t/D above roughly 0.6 as needing a pin-bending assessment.
**This lug is at 1.250, more than double that.** The check was listed as open from the start and is
closed here.

## 2. Pin geometry and section properties

    d = 50.80 mm
    S = pi*d^3/32 = 12,870.4 mm^3
    A = pi*d^2/4  =  2,026.8 mm^2

Applied resultant `P = 617,776 N` (Rev C load basis).

## 3. Pin shear — not critical

Double shear, as in a standard lug-clevis joint:

    tau = P / (2A) = 617,776 / 4,053.7 = 152.4 MPa

Low for any steel pin. **Shear does not govern.**

## 4. Pin bending — governs

Symmetric clevis, lug thickness `t1` central, two ears of thickness `t2`, gap `g` each side. Treating
the pin as a simply supported beam with the lug load distributed over `t1`:

    M = (P/2) * (t1/4 + g + t2/2)
    sigma = M / S

**The clevis geometry is not defined in this project** — only the single lug AF-DT-1000 is scoped.
The mating fitting appears as `AF-DT-2000_pylon_attachment_assembly` but its dimensions were never
established here. The calculation is therefore run across a range of representative clevis
proportions rather than a single assumed value.

| Clevis assumption | t2 (mm) | gap (mm) | Bending stress (MPa) |
|---|---|---|---|
| t2 = 0.50 t1, gap 0.030 in | 31.75 | 0.762 | **780.3** |
| t2 = 0.50 t1, gap 0.060 in | 31.75 | 1.524 | 798.6 |
| t2 = 0.75 t1, gap 0.030 in | 47.62 | 0.762 | 970.8 |
| t2 = 1.00 t1, gap 0.030 in | 63.50 | 0.762 | 1161.3 |

`t2 = 0.5 t1` is the balanced-shear proportion and is taken as the reference case: **780 MPa**.

**Bending exceeds shear by a factor of 5.1.** Pin bending, not pin shear, is the governing pin
failure mode in this joint.

### Pin material requirement

Using a bending modulus of rupture of `1.5 * Ftu` for a solid circular section:

| Candidate pin material | Ftu (MPa) | Fb = 1.5 Ftu | MS at 780 MPa |
|---|---|---|---|
| 15-5PH H1025 | 1069 | 1603 | +1.05 |
| 4340 at 180 ksi | 1241 | 1862 | +1.39 |
| PH13-8Mo H1000 | 1413 | 2120 | +1.72 |
| 4340 at 200 ksi | 1379 | 2068 | +1.65 |

**The joint requires a high-strength steel pin.** For contrast, 7075-T6 at Ftu = 572 MPa gives
`Fb = 858 MPa` and `MS = +0.10` at the reference case — and **negative** for any clevis with ears
thicker than half the lug. An aluminium pin is not viable here.

**Caveat:** the 1.5 plastic bending factor is a standard textbook value for solid rounds, not one
verified against a specific source in this project. The pin material has never been specified. These
margins establish the class of pin required; they are not a substantiation of a chosen pin.

## 5. Effect on the lug margin — the significant finding

If pin bending concentrates bearing over an effective thickness `t_eff < t`, the nominal bearing and
net-section stresses rise by `t / t_eff`. Reworking the oblique interaction of
`docs/F5_MARGIN_CROSSCHECK.md` with that factor:

| t_eff / t | Ra | Rtr | MS |
|---|---|---|---|
| 1.00 | 0.2437 | 0.4899 | **+0.710** |
| 0.90 | 0.2707 | 0.5443 | +0.539 |
| 0.80 | 0.3046 | 0.6124 | +0.368 |
| 0.70 | 0.3481 | 0.6998 | +0.197 |
| 0.60 | 0.4061 | 0.8165 | +0.026 |
| 0.50 | 0.4873 | 0.9798 | **-0.145** |

**MS reaches zero at t_eff / t = 0.585.**

The margin is far more sensitive to this than to the Ftux uncertainty already on record (a 10%
reduction in Ftux takes MS from +0.71 to about +0.5). A modest 20% concentration of bearing halves
the margin.

**No claim is made about the actual value of t_eff.** Establishing it requires either a published
thick-lug correction traceable to AFFDL-TR-69-42 or NASA TM X-73305, or an FE model with explicit
pin-lug contact. Both are out of reach right now, and inventing a factor would be exactly the
unverified number this project refuses to carry.

What can be said: **at t/D = 1.25 the uniform-bearing assumption is not automatically safe, and the
margin's sensitivity to it is steep.**

## 6. Why the existing FE does not settle this

The Rev D run (`docs/F5_FE_REVD_LINEAR_ELASTIC.md`) used an Ansys **Bearing Load**, which applies a
cosine pressure distribution around the bore circumference but is **uniform through the thickness**.
It therefore embeds the same thin-lug assumption being questioned here and cannot confirm or refute
it.

Resolving it requires modelling the pin as a separate body with contact — which is precisely
**phase F7**. This check defines what F7 needs to answer.

## 7. Conclusions

1. **Pin bending governs the pin**, at roughly 780 MPa for a balanced clevis, 5.1x the shear stress.
2. **A high-strength steel pin is required.** Aluminium is not viable. Steels from 155 ksi upward
   give MS between +1.05 and +1.72.
3. **Pin bending stress is sensitive to clevis geometry** — 49% higher if the ears are as thick as
   the lug. The clevis is undefined and should be pinned down before any pin is selected.
4. **The +0.710 lug margin is sensitive to the thick-lug effect**, reaching zero at
   `t_eff / t = 0.585`. This is now the largest known caveat on the margin.
5. **F7 contact analysis is no longer optional polish.** It is the analysis that determines whether
   the headline margin holds.

## 8. Open

- [ ] Establish `t_eff / t` from a traceable thick-lug correction, or from F7 contact FE
- [ ] Define the clevis geometry of the mating fitting (AF-DT-2000)
- [ ] Select and substantiate a specific pin material and size
- [ ] Verify the 1.5 plastic bending factor against a citable source rather than textbook practice
