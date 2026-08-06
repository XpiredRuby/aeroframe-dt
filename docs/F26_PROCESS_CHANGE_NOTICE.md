# F26 — Process Change Notice PCN-001 — AF-DT-1000

**Claim boundary:** educational / representative / portfolio only. Non-OEM, non-certified.

**Against:** `F13_MANUFACTURING_INSPECTION.md`, Rev D process plan
**Cause:** F23 material re-selection, 7075-T7351 → 7050-T7451
**Status:** MANDATORY — the affected operations call up a material this part cannot be made from

---

## Why a change notice rather than a rewrite

The F13 routing is released work. **A released routing is amended by notice, not edited in place**,
so that the shop can see what changed and why, and so the superseded instruction remains legible in
the record. That is also how the F15 nonconformance was handled, and the same reasoning applies:
the history is part of the evidence.

`F13_MANUFACTURING_INSPECTION.md` is **not** being edited. It is read together with this notice.

## Changes

### Op 010 — Receiving

**Was:**

> Receive 7075-T7351 plate, AMS 4078 or AMS-QQ-A-250/12, thickness band 2.001–2.500 in. Verify
> certificate and rolling direction marking.

**Now:**

> **Receive 7050-T7451 plate, AMS 4050, thickness band 5.001–6.000 in.** Verify certificate and
> rolling direction marking.

**Reason.** F23 established that MMPDS-2026 tabulates 7075-T7351 plate **only to 4.000 in**, while
the Rev D envelope of 16.000 × 6.000 × 9.000 in requires stock at least **6.000 in** thick. The old
instruction called up a plate that cannot produce this part. 7050-T7451 is tabulated to 8.000 in;
allowables are MMPDS-2026 Table 3.7.4.0(b1), 5.001–6.000 in band, A-basis.

**The band check remains a receiving gate and is now more important, not less.** The 5.001–6.000
band is the last band before properties drop again at 6.001–7.000 (`Ftu` L 70 → 69, ST 66 → 66).
Stock outside the band voids the margin exactly as before.

### Op 040 — Stress relief

**Unchanged, but the justification is restated.** The original reason was that **T7351 is already
stress-relieved by stretching** as part of the temper, so any post-machining thermal cycle would
alter it. **T7451 is likewise a stretched, stress-relieved temper.** The instruction — natural
stabilisation only, no thermal treatment — stands on the same reasoning for the new alloy.

### §3.1 — Grain orientation hold point

**Was:** MIL-HDBK-5J Table 3.7.6.0(b3) gives `Ftu(ST)` = 62 ksi against 65 (L) and 66 (LT); Table
3.1.2.3.1(b) flags 7075-T7351 as SCC-susceptible in ST with a **39 ksi** threshold. A 90° blank
rotation costs 6% of `Ftu`.

**Now:** MMPDS-2026 Table 3.7.4.0(b1) gives, for 7050-T7451 at 5.001–6.000 in, **`Ftu` = 70 ksi in
both L and LT, and 66 ksi in ST**. The SCC threshold in ST is **35 ksi** over 0.750–6.000 in.

**The hold point is retained, and its rationale shifts.** For 7075 the orientation bought 1 ksi of
`Ftu` between L and LT as well as keeping ST out of the load path. **For 7050 the L and LT ultimate
strengths are equal**, so the orientation no longer buys directional strength — but ST is still the
weakest direction (66 against 70, a **6% loss**, the same penalty as before) and its SCC threshold
is **lower than 7075's was**. A 90° blank rotation is therefore no less serious than it was, and the
hold point at op 020 and the certificate re-verification at op 110 both stand unchanged.

### §7 — Tolerance stack

**Superseded by `MARGIN_SUMMARY.md` §6**, which carries the stack at the released 7050 operating
point: nominal **+0.151**, worst case **+0.128**, **15.3%** of margin consumed, **6.54×** tolerance
widening to reach zero. `tools/run_f13_inspection_plan.py` computes all three material bases and
reports the 7050 case as the released one.

The F13 §7 derivation itself remains valid **as an elastic-basis derivation** and is correctly
labelled as such throughout that document. It is not withdrawn.

## Not changed

- **The 10 inspection characteristics** — dimensional and geometric, material-independent
- **Datum scheme, fixturing sequence, bore-last single setup** — geometry-driven
- **Op 090, no cold expansion and no shot peen** — the reasoning in F13 §3.2 is that the residual
  field is not in the F9 model. F25 re-derived F9 on 7050 and **still does not model it**, so the
  exclusion stands for the same reason
- **Op 120 eddy-current bore inspection** — the NDI threshold of 1.27 mm is unchanged, but note
  that **F25 §3 leaves the 4,500-flight inspection interval unverified for 7050**, because the
  crack-growth curves have not been digitised. The inspection method is unaffected; its *interval*
  is an open item

## Effectivity

All units. There is no prior production — this is a paper change to a released routing, applied
before first article.
