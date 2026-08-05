# F23 — Material Re-selection — AF-DT-1000

**Claim boundary:** educational / representative / portfolio only. Non-OEM, non-certified.

**Source: MMPDS-2026, Volume I, 1 July 2026**, accessed via Knovel.

F20 found that the part envelope requires stock at least **6.000 in** thick while the allowables were
cited from the **2.001–2.500 in** band. F21 found that the citation was to a cancelled handbook. This
document reads the current handbook and resolves both — and the resolution is not the one either
finding anticipated.

---

## 1. The finding: 7075-T7351 plate does not exist at 6 inches

**Table 3.7.9.0(b2)**, 7075 sheet and plate, T7351 temper. The tabulated thickness bands are:

    0.250-0.499  0.500-1.000  1.001-1.500  1.501-2.000
    2.001-2.500  2.501-3.000  3.001-3.500  3.501-4.000

**The table ends at 4.000 in.**

F20 framed this as *the wrong band was selected*. That was too generous. **There is no band.** MMPDS
publishes no design allowables for 7075-T7351 plate thick enough to make this part, so the part
cannot be substantiated as a monolithic machining from 7075-T7351 plate at all.

F20 §1.2 offered three ways out and recommended checking option A — re-cite the allowables at the
correct band — first, because it was free. **Option A does not exist.** The remaining options were
splitting the part, changing to a forging, or shrinking the envelope. There turned out to be a
fourth, and it is better than all three.

## 2. The locator changed, and so did the values

**MIL-HDBK-5J Table 3.7.6.0(b3) is MMPDS Table 3.7.9.0(b2).** In MMPDS-2026, §3.7.6 is alloy 7056;
7075 is §3.7.9. Every locator this project cites had to be re-found rather than renumbered.

**This vindicates F21's rule against inferring the mapping.** MMPDS preserves the *style* of
MIL-HDBK-5 numbering while reassigning the numbers, which is the worst possible case for inference:
an inferred citation would have looked right and pointed at a different alloy.

At the 2.001–2.500 in band, A-basis, against what this project has been carrying:

| Property | Project (MIL-HDBK-5J) | MMPDS-2026 | Δ |
|---|---|---|---|
| Ftu, L | 65 | **66** | +1.5% |
| Ftu, LT | 66 | 66 | — |
| Ftu, ST | 62 | 62 | — |
| Fbru, e/D = 2.0 | 131 | **132** | +0.8% |

**Equivalence did not hold.** Two values moved. The table footer reads *Last Revised: MMPDS-2026,
Item 15-13* — it was revised this year. Both moves are favourable and both are small, but F21 §3.2
warned that 2003 equivalence licenses nothing about 2026, and it was right to.

## 3. Resolution: 7050-T7451 plate

**Table 3.7.4.0(b1)**, AMS 4050. Thickness bands run to **8.000 in**, with an explicit
**5.001–6.000 in** band. This is the alloy that exists precisely because 7075 runs out — 7050 was
developed for thick sections, where its lower quench sensitivity retains strength that 7075 loses.

**7050-T7451 plate, 5.001–6.000 in, A-basis:**

| Property | L | LT | ST |
|---|---|---|---|
| Ftu, ksi | **70** | **70** | 66 |
| Fty, ksi | 60 | 60 | 57 |
| Fcy, ksi | 57 | 63 | 62 |
| Fsu, ksi | 43 (L-S) | 43 (T-S) | 35 (S-L) |
| Fbru, e/D = 2.0 | 137 | **138** | — |
| Fbry, e/D = 2.0 | 105 | 106 | — |

`E = 10.3e3 ksi`, `Ec = 10.6e3 ksi`, `G = 3.9e3 ksi`, `μ = 0.33`, `ω = 0.102 lb/in³`.

**The 6-inch-thick 7050 is stronger than the 2.5-inch-thick 7075 this project has been using** —
Ftu 70 against 65/66, Fbru 138 against 131. The material problem and the strength problem solve each
other.

### 3.1 Elastic constants are identical

`E`, `Ec`, `G` and `μ` are **the same as 7075-T7351 to the tabulated precision**. Density rises 1%,
0.101 → 0.102 lb/in³.

This matters more than the strength numbers. The FE stiffness model is unchanged, so **F5 linear
elastic, F7 contact and F17 modal carry over essentially intact** rather than needing re-running.
A material change that would normally invalidate the entire FE chain does not, here, because the two
alloys are elastically indistinguishable and differ only in strength and metallurgy.

## 4. Margin

Allowable loads rescale directly with `Ftu` and `Ftux`; the Melcon-Hoblit `Kt`, `Ktru` and `Kbr`
factors are geometric and unchanged. Reproducing the released numbers first, as a check on the
method:

    7075-T7351, 2.001-2.500 in, MIL-HDBK-5J A-basis
      elastic         Ra = 0.39090  Rtr = 0.77400  ->  MS = +0.0784   (released: +0.078)
      elastic-plastic Ra = 0.36463  Rtr = 0.72198  ->  MS = +0.1561   (released: +0.156)

Both reproduce. Rescaling to 7050-T7451 at 5.001–6.000 in, A-basis:

    7050-T7451, 5.001-6.000 in, MMPDS-2026 A-basis
      elastic         Ra = 0.36298  Rtr = 0.72977  ->  MS = +0.148
      elastic-plastic Ra = 0.33859  Rtr = 0.68072  ->  MS = +0.231   [NOT CLAIMABLE - see 4.1]

**On the elastic basis, which is the honest comparison, the margin nearly doubles: +0.078 → +0.148.**

### 4.1 Why the elastic-plastic number is not claimable

`t_eff/t = 0.7300` was **measured on 7075 properties** — F16 used bilinear isotropic hardening with
yield 358.5 MPa, which is 7075-T7351's `Fty` of 52 ksi at that band. **7050-T7451 has `Fty` = 60
ksi (414 MPa).** A higher yield means *less* plasticity at the bearing edge, so less redistribution,
so `t_eff/t` moves back **toward** the elastic 0.681 rather than staying at 0.730.

**The +0.231 figure assumes a measurement taken on a different material.** It is recorded here to
show the shape of the answer and must not be quoted. **The governing margin under 7050 is the
elastic bound, `MS = +0.148`, until the elastic-plastic contact run is repeated with 7050
properties.** That is a ~40 minute Ansys job and it is the only solver work this change requires.

### 4.2 Ekvall method scatter

At the A-basis-consistent pairing (99% probability, 95% confidence, factor 1.195):

| Basis | 7075-T7351 | 7050-T7451 |
|---|---|---|
| Elastic | −0.098 | **−0.039** |
| Elastic-plastic | −0.032 | +0.030 *(not claimable, §4.1)* |

**The elastic case remains negative.** It improves substantially — −0.098 to −0.039 — but does not
clear. The project's long-standing worst case only goes positive on the elastic-plastic basis, and
that basis needs re-measuring. **No claim is made here that the fitting clears A-basis method
scatter.**

## 5. REQ-012 unblocks

**7050-T7451 plate has published S/N curves.** MMPDS-2026 §3.7.4.2.8 provides:

| Figure | Content |
|---|---|
| 3.7.4.2.8(a), (b), (c1), (c2), (e) | best-fit S/N, unnotched, long transverse |
| **3.7.4.2.8(f)** | **best-fit S/N, notched, `Kt = 3.0`** |
| 3.7.4.2.8(g) | best-fit S/N, notched, `Kt = 2.6` |
| 3.7.4.2.8(d) | strain-life, cyclic stress-strain, mean-stress curves |

Fatigue crack growth data for T7451 plate is at §3.7.4.2.9(a)–(c), so **F9 damage tolerance has a
7050 basis as well** and does not have to carry 7075 data across an alloy change.

**REQ-012 has been closed as permanently blocked for the life of this project** on the grounds that
no S-N data exists for the T7351 temper. That was true, and remains true: MMPDS-2026 provides S/N
curves for 7075 only in the **T6** temper (§3.7.9.1.8). §3.7.9.2, covering T73/T7351, has
stress-strain, crack growth and residual strength — **no S/N**.

**So the blocker was never about fatigue data being unavailable. It was about 7075-T7351
specifically.** Changing to 7050-T7451 for a reason that has nothing to do with fatigue — the
thickness limit — removes it as a side effect. The notched `Kt = 3.0` curve is directly applicable
to a loaded bore.

**Ceiling moves from 17/18 to 18/18**, conditional on the safe-life analysis actually being built
and passing. It is not verified yet; it is now *possible*, which it demonstrably was not before.

## 6. Consequences

| Deliverable | Effect |
|---|---|
| Geometry (Rev D) | **unchanged** — no Rev E, envelope stays 16.000 × 6.000 × 9.000 in |
| F5 linear elastic FE | carries over — identical `E`, `μ` |
| F7 elastic contact | carries over — ratio is elastic and material-independent at equal `E` |
| **F16 elastic-plastic** | **must be re-run** at `Fty` = 60 ksi — the one Ansys job |
| F17 modal | carries over; frequencies shift ~0.5% on the 1% density rise |
| F9 damage tolerance | re-derive on 7050 `K_Ic` and `da/dN`; ST threshold 35 ksi√in to 6.000 in |
| F12 / F18 / F19 Ekvall | **limitation** — Ekvall's 243 lug tests are a 1986 population whose alloy coverage this project has not verified for 7050 |
| F13 tolerance stack | re-propagate at the new operating point |
| F20 cost | material cost rises; 7050 plate is more expensive than 7075, and buy-to-fly 5.36 is unchanged |
| **REQ-012** | **unblocks** — see §5 |
| SCC | 7050-T7451 ST threshold **35 ksi**, 0.750–6.000 in, against 39 ksi for 7075-T7351. Lower, but ST remains out of the primary load path by design |

## 7. Recommendation

**Change the material to 7050-T7451 plate, per AMS 4050, allowables from MMPDS-2026 Table
3.7.4.0(b1), 5.001–6.000 in band, A-basis.**

It is the only option that fixes the thickness problem without touching the geometry, and it
improves the margin, the fatigue position and the fracture data simultaneously. The alternatives —
splitting the fitting into a bolted assembly, or moving to a hand forging — both introduce new
failure modes into the primary load path to solve a problem that a material substitution solves
outright.

For completeness, the forging route was checked and **is** viable: Table 3.7.9.0(f), 7075-T7352 hand
forging, covers 5.001–6.000 in. But its allowables are markedly worse — `Ftu` 61/59/57 L/LT/ST at
that thickness against 7050's 70/70/66 — and the 5.001–6.000 band is **S-basis, not A-basis**, which
this project's single-load-path argument does not accept.

## 8. Limitations

1. **The elastic-plastic margin is not claimable** until F16 is re-run on 7050 properties. §4.1.
2. **The A-basis Ekvall worst case remains negative** on the defensible elastic basis (−0.039).
3. **Ekvall applicability to 7050 is unverified.** The correlation, the specimen basis and the
   method cross-check all rest on a 1986 dataset whose alloy composition this project has read for
   `t/D` range but not for alloy. If 7050 lugs are absent from it, F12/F18/F19 need restating.
4. **The margin rescaling assumes the governing failure mode does not change.** Net tension governed
   the axial term for 7075 (`P'tu` 308,750 lb against `P'bru` 409,200 lb) and the same ordering holds
   at 7050's allowables, but the full interaction has not been recomputed from first principles.
5. **No cost impact is quantified.** 7050 plate is more expensive per pound than 7075 and F20's
   `ASSUMED_COST_BASIS` rates were not alloy-specific.
6. **REQ-012 is unblocked, not closed.** No safe-life analysis has been performed.
