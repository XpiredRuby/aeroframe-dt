# F22 — Composite Material Trade — AF-DT-1000

**Claim boundary:** educational / representative / portfolio only. Non-OEM, non-certified.
**This is a screening trade, not a sizing.** No laminate allowables were available, so nothing here
sizes a composite fitting. It establishes whether the question is worth asking, and answers it.

**Question:** should AF-DT-1000 be a carbon-fibre composite part instead of a machined 7075-T7351
aluminium fitting?

**Answer: no — and the reason is specific to this joint rather than general to composites.** The
single measurement that most improved the metal design, F16's elastic-plastic contact result, is the
measurement of a mechanism a composite does not have.

---

## 0. Why this trade exists

Composite structure dominates modern airframes, and laminate literacy is close to a universal
requirement in structural analysis roles. A project that never mentions composites is a project with
a visible hole in it.

The wrong way to close that hole is to redesign the fitting in carbon and declare victory. The right
way is to ask the question honestly against the evidence this project has already produced — and to
report the answer even when it is negative. **A negative result reached from the project's own
measurements is worth more than a positive result reached by assumption.**

This trade also respects the project thesis. No new geometry, no new part, no scope expansion. Same
fitting, same load, same governing question.

---

## 1. What the fitting actually demands

Four properties of this joint, all established elsewhere in this project, determine the answer.

| # | Established | Source |
|---|---|---|
| 1 | **`t/D = 1.25`** — a thick lug. The pin bends; bearing is not uniform through the thickness | F6, F7 |
| 2 | **`t_eff/t = 0.681` elastic, `0.730` elastic-plastic.** Yielding redistributes the bearing peak and *recovers* effective thickness | F16 |
| 3 | **Peak local plastic strain 6.46%**, at the contact edge | F16 |
| 4 | **Load acts 59.04° off the lug axis** — transverse-dominant, not axial | Load rev C |

Items 2 and 3 are the crux. **The metal's margin improved from `+0.078` to `+0.156` because the
material yielded.** That is not a modelling refinement; it is a physical mechanism doing structural
work. F16 measured it.

---

## 2. The governing argument

**A composite laminate has no equivalent to the mechanism in item 2.**

When the pin bends in a thick metallic lug, bearing pressure concentrates at the bore edges. The
aluminium responds by yielding locally, which softens the peak, spreads load into the underloaded
mid-thickness, and raises the effective bearing thickness. That is precisely what F16 measured:
`t_eff/t` rose 7.2%, and the margin nearly doubled.

Carbon/epoxy is essentially linear-elastic to failure in the fibre direction. There is no yield
plateau to redistribute through. In a composite lug under the same pin flexure:

- the through-thickness bearing peak **stays peaked** — no plastic softening
- the concentration is carried by **matrix-dominated through-thickness and interlaminar
  properties**, which are the weakest directions in the laminate by an order of magnitude
- the 6.46% local strain that the aluminium absorbed as plastic deformation has no benign
  equivalent; in a laminate, strain of that magnitude at a bearing edge is **damage** —
  matrix cracking, fibre crushing, delamination onset

So the thickness that makes this joint difficult — `t/D = 1.25`, driving pin flexure and
through-thickness gradients — loads a composite in exactly the direction composites are worst, and
removes the mechanism the metal used to cope.

**This is a joint whose governing physics selects against laminates.** Not because composites are
weak, but because this particular joint concentrates load through the thickness and then relies on
plastic redistribution to survive it.

### 2.1 Load direction compounds it

The resultant acts **59.04° off the lug axis**. A composite lug can be tailored — fibres steered to
follow the load path — but tailoring is only an advantage when the load direction is known,
stable, and preferably axial. Here it is strongly transverse and comes from a 9g emergency landing
condition, which is a limit case rather than a steady operating one.

Achieving competent off-axis strength drives the laminate toward quasi-isotropic, which surrenders
most of the directional advantage that motivates using composite in the first place. **A
quasi-isotropic laminate carries a fraction of its unidirectional strength**, and at that point it
is competing against 7075 on specific strength without its main structural argument.

### 2.2 Order-of-magnitude comparison

**These are representative engineering magnitudes, not allowables**, and are marked as such. They
are included to show the direction and size of the effect, and no margin anywhere in this project
uses them.

| Property class | 7075-T7351 plate | CFRP laminate (representative) | Consequence here |
|---|---|---|---|
| In-plane strength | moderate, isotropic | high in fibre direction | favours composite — *if* load is aligned |
| Off-axis / quasi-isotropic strength | unchanged, isotropic | substantially reduced | **erases the advantage at 59°** |
| Through-thickness / interlaminar | comparable to in-plane | **roughly an order of magnitude lower** | **governing weakness for a thick lug** |
| Post-yield redistribution | yes — measured, `t_eff/t` +7.2% | **none** | **decisive** |
| Bearing behaviour | ductile, progressive | brittle onset, damage accumulates | worsens the thick-lug case |

The trade turns on the two bottom rows, and neither depends on the precise values.

---

## 3. Where the composite case would be stronger

Reporting only the reasons for the answer already reached is how a trade study becomes an
advertisement. The composite case has genuine strengths, and two of them apply here.

**Buy-to-fly.** F20 established a buy-to-fly of **5.36** and material utilisation of **18.6%** —
over 80% of the purchased plate becomes chips, and material dominates unit cost at nominal and high
rates. Composite processing is near-net-shape. **On raw material efficiency the composite wins
outright**, and it wins against the largest single cost element identified in F20.

**Mass.** The fitting is 7.65 kg. Specific strength favours CFRP where the load is alignable.

**Corrosion and SCC.** 7075-T7351 is a stress-corrosion-resistant temper chosen partly for that
reason, and the short-transverse direction still carries the lowest properties and the SCC caveat.
A composite has no equivalent concern.

**What would have to change for the composite to win.** The trade flips if the fitting becomes
**thin** (`t/D` well below 1, so the pin does not bend and bearing stays uniform through the
thickness), the load becomes **predominantly axial** (so fibres can be steered usefully), and mass
becomes the binding constraint rather than margin. **None of those describe AF-DT-1000.** They do
describe plenty of other airframe fittings, which is why composite lugs exist and are used.

---

## 4. What changing material would do to the rest of the project

Worth stating explicitly, because it shows how much of a substantiation is material-dependent.

| Deliverable | Survives? |
|---|---|
| Load basis, free bodies, fitting factor | **Yes** — material-independent |
| Melcon-Hoblit lug method | **No** — an isotropic-metal method |
| Ekvall correlation (243 metallic lug tests) | **No** — wrong population entirely |
| F16 elastic-plastic contact | **No** — the mechanism does not exist |
| F9 damage tolerance, `K_Ic`, Paris growth | **No** — composites have no equivalent crack-growth framework; certification uses a no-growth / BVID philosophy with damage thresholds rather than crack sizes |
| F13 inspection plan | **Partly** — dimensional characteristics survive; penetrant does not, and ultrasonic acceptance criteria change completely |
| MMPDS allowables (F21) | **No** — metallic handbook; composite allowables are program-specific and generated by test |
| Digital thread, requirements, verification matrix | **Yes** — process infrastructure is material-agnostic |

**Roughly half the analysis chain is method-specific to metals.** That is itself a useful finding:
it quantifies how much of a substantiation package is portable across a material change, and the
answer is "less than people assume."

It also names the practical barrier. **Composite allowables are not published in a handbook.** There
is no MMPDS for laminates; allowables are developed per material system, per lay-up, per process, by
coupon and element testing. A student project cannot obtain them, which means a composite version of
this fitting **could not have been substantiated at all** — only asserted.

---

## 5. Conclusion

**Retain 7075-T7351.** The decision rests on three findings the project measured rather than assumed:

1. **`t/D = 1.25` drives pin flexure and through-thickness bearing gradients**, loading a laminate in
   its weakest direction.
2. **Plastic redistribution is doing real structural work here** — F16 measured `t_eff/t` rising from
   0.681 to 0.730 and the margin moving from `+0.078` to `+0.156`. A composite forfeits that.
3. **The 59.04° off-axis load** forces a quasi-isotropic lay-up, surrendering the tailoring advantage
   that justifies composite in the first place.

The composite case is genuinely stronger on buy-to-fly, mass, and corrosion — and on the first of
those it beats the metal design against F20's dominant cost element. It still loses, because the
governing failure mode is a through-thickness bearing concentration and this fitting survives it by
yielding.

---

## 6. Limitations

1. **No laminate allowables were used, because none were available.** Section 2.2 gives
   representative magnitudes only. **This trade cannot size a composite fitting and does not
   attempt to.**
2. **No composite bearing/bypass analysis was performed.** A real assessment would evaluate the
   bearing–bypass interaction envelope for a specific lay-up, with clamp-up and hole-quality effects,
   against test-derived allowables.
3. **No laminate optimisation was attempted.** A steered or hybrid lay-up, a metallic bearing bushing
   in a composite blade, or a metal–composite hybrid fitting might change the answer. The bushing
   option in particular is common practice precisely because it addresses the bearing weakness
   identified in §2, and it is **not** evaluated here.
4. **Failure criteria are named, not applied.** No Tsai-Wu, no maximum-strain, no delamination
   analysis.
5. The conclusion is a **screening** conclusion. It says the composite route is not promising for
   this fitting and explains why. It does not prove that no composite design could work.
