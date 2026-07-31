# F10 — Dynamics and Buckling, Analytical Assessment

**Partial closure of AFDT-REQ-014**, which requires modal and buckling analyses **with analytical
checks**. The analytical half is complete and given here. **The FE half has not been run** — see §5.

**Result: neither dynamics nor buckling is critical for this fitting**, and the analytical margins
are large enough that FE confirmation is a formality rather than a risk.

**Claim boundary:** educational / representative / portfolio only. Non-OEM, non-certified.

---

## 1. Model

The fitting is treated as a **cantilever**: the flange is bolted flat to the wingbox and is taken as
fixed; the blade and lug head project from it.

| Quantity | Value |
|---|---|
| Cantilever length `L` (flange top to lug top) | 0.2032 m |
| Blade width `w` | 0.1016 m |
| Blade thickness `t_web` | 0.0635 m |
| Second moment `I` about the weak axis | 5.5498e-6 m^4 |
| Section area `A` | 6.4516e-3 m^2 |
| Young's modulus `E` | 71.0 GPa (MIL-HDBK-5J, 10.3e3 ksi) |

**Mass split.** Total fitting 7.652 kg. The flange is
`0.4064 x 0.1524 x 0.0254 m x 2810 kg/m^3 = 4.421 kg` and does not participate, leaving
**3.232 kg cantilevered**, or `m' = 15.9 kg/m`.

Bending is taken about the **weak axis** — the axis resisting the transverse load `Fx`, which is the
dominant component and the softer direction.

## 2. First natural frequency

Continuous cantilever with distributed mass:

    f1 = (1.875^2 / 2*pi) * sqrt( E*I / (m' * L^4) )
       = **2133 Hz**

### Assessment

**Well clear of shaft-order excitation.** Turbofan N1 runs roughly 50-100 Hz and N2 roughly
200-300 Hz. The first mode is an order of magnitude above both, so **shaft-order resonance is not a
concern.**

**Not automatically clear of blade-passing.** Blade-passing frequency is `N1 x blade count`, which
for a large fan can reach the low kilohertz. **A 2133 Hz first mode is not comfortably separated
from that range**, and a real programme would check the specific engine's BPF and its harmonics
against this mode.

This is recorded as an **open item**, not dismissed. It is the one dynamics result here that is not
obviously benign.

**Conservatism.** Treating the flange as rigidly fixed overestimates stiffness; real bolted-joint
compliance would lower `f1` somewhat. The cantilever idealisation also ignores the lug head's
concentrated mass at the tip, which lowers `f1` further. **The true first mode is below 2133 Hz**,
moving it closer to the BPF range rather than away. FE would resolve this.

## 3. Buckling

**Buckling is not a credible failure mode for this fitting**, and the geometry says so before any
calculation.

    radius of gyration  r = sqrt(I/A) = 0.0293 m
    slenderness         L/r = 6.9

**Euler buckling only becomes relevant above `L/r` of roughly 40.** At 6.9 this member is
extremely stocky — it is a block, not a column.

Euler critical load, cantilever end condition (`K = 2`):

    Pcr = pi^2 * E * I / (K*L)^2 = 2.355e7 N = 23.5 MN

Against the maximum compressive component of **529,740 N**:

    MS_buckling = 23.5e6 / 529,740 - 1 = **+43.4**

**The fitting is 44 times the Euler load away from column buckling.** Yielding and bearing failure
occur at a small fraction of that, which is exactly why the static margin governs.

**Local buckling is also not credible** — there are no thin webs, flanges or panels. Minimum
section thickness is 25.4 mm on the flange and 63.5 mm through the blade.

## 4. Conclusions

1. **First mode approximately 2133 Hz**, an order of magnitude above shaft-order excitation.
2. **Blade-passing separation is not established** and remains open. The idealisations here all bias
   `f1` high, so the real mode sits lower.
3. **Buckling is not critical**, `MS = +43.4` on Euler, with `L/r = 6.9` placing the member far
   outside the slender regime.
4. **Neither mode competes with the static margin of +0.078.**

## 5. What remains for full REQ-014 closure

AFDT-REQ-014 requires **modal and buckling analyses with analytical checks**. The analytical checks
are complete. The FE analyses are not:

- [ ] **FE modal**, 6 modes, flange fixed. Compares against the 2133 Hz estimate and captures the
      tip mass and the true mode shape. **~30 min VDI.**
- [ ] **FE eigenvalue buckling**, 3 modes. May be blocked upstream — the F7 static analysis is
      nonlinear, and linear buckling cannot always be derived from a nonlinear solution. **~20 min
      VDI**, and a legitimate blocked result if it refuses.
- [ ] **Blade-passing frequency check** against the specific engine, once defined.

**The analytical margins are large enough that FE is expected to confirm rather than overturn.**
Buckling at `MS = +43.4` will not become critical. The modal result is the one worth running,
because the idealisation error is one-sided and the BPF separation is genuinely unresolved.
