# AeroFrame-DT — Project State

**Last updated: 2026-08-06**
**Repo:** `github.com/XpiredRuby/aeroframe-dt`, branch `main`
**Owner:** Ruby, Texas A&M aerospace senior (GitHub: XpiredRuby)

---

## 1. What this project is

A rigorous static stress substantiation of **one** aircraft part: a forward pylon-to-wingbox
attachment fitting (**AF-DT-1000**) on an MD-11-class aircraft.

The thesis is **depth over breadth on a single fitting**. Scope expansion was evaluated twice and
rejected both times. The project replicates a full V-model engineering lifecycle — requirements,
load basis, CAD/GD&T, hand analysis, multi-fidelity FEA, fatigue, damage tolerance, manufacturing
and inspection, digital thread, nonconformance/RCCA — to compensate for limited internship
experience in the aerospace job market.

**Claim boundary:** educational / representative / portfolio only. Non-OEM, non-certified.
Geometry and load case are `SYNTHETIC_TEST_ONLY`; the spectrum is `SYNTHETIC_SPECTRUM`; F20 cost
rates are `ASSUMED_COST_BASIS`. **Material allowables, S/N curves and fracture data are real**, from
MMPDS-2026.

---

## 2. Headline results

| | |
|---|---|
| **Material** | **7050-T7451 plate, AMS 4050**, MMPDS-2026 Table 3.7.4.0(b1), 5.001–6.000 in, A-basis |
| **Governing margin** | **`MS = +0.151`** |
| Worst-case tolerance stack | +0.128, 15.3% consumed, 6.54× to zero |
| A-basis-consistent method scatter | **−0.037** — negative, stated not buried |
| B-basis-consistent pairing | +0.048 |
| Critical crack size | 3.51 mm |
| **Safe life** | **5.25e5 flights mean; 1.31e5 at scatter factor 4** |
| First natural frequency | 1197.2 Hz — inside the plausible blade-passing band |
| **Requirements verified** | **18 of 18** |

**Margin history:**

| Stage | MS | Cause |
|---|---|---|
| Thin-lug, assumed Ftu 71 ksi | +0.710 | — |
| Thick-lug correction, elastic (F7) | +0.165 | `t/D = 1.25` invalidates uniform bearing |
| Real A-basis allowables | +0.078 | assumed Ftu was 9% optimistic |
| Elastic-plastic contact, 7075 (F16) | +0.156 | yielding redistributes the bearing peak |
| **Material re-selected, 7050 (F23/F24)** | **+0.151** | **7075 plate is not tabulated at 6.000 in** |

### Key geometry (Rev D, frozen — unchanged by the material change)

`D = 2.000`, `t = 2.500`, `W = 4.000`, `e = 2.500` in. `e/D = 1.25`, `W/D = 2.00`, **`t/D = 1.25`**.
Envelope **16.000 × 6.000 × 9.000 in — minimum stock thickness 6.000 in.** Mass 7.65 kg.

### Load basis (Rev C)

Resultant **617,776 N at 59.04° off the lug axis**, transverse-dominant. 9g emergency landing per
FAR 25.561, fitting factor 1.15 per FAR 25.625.

---

## 3. What happened on 2026-08-05/06

**The single most important sequence in the project.** Read F20 → F21 → F23 → F27 in order.

1. **F20** costed the part and derived that the envelope needs **6.000 in stock**.
2. **F21** found every allowable was cited from **MIL-HDBK-5J, cancelled in 2006** and removed from
   the 14 CFR 25.613 compliance path.
3. Reading MMPDS-2026 to fix the citation revealed **7075-T7351 plate is tabulated only to
   4.000 in**. Not the wrong band — **no band. The part could not be made from its stated material.**
4. **F23** re-selected to **7050-T7451**, which exists precisely because 7075 runs out in thick
   section. Elastic constants are identical, so the FE chain survived; geometry unchanged.
5. **F24** re-measured the contact ratio on 7050: `t_eff/t` 0.7300 → **0.6828**, margin **+0.151**.
6. **F25** re-read `K_Ic` and re-derived critical crack, 3.07 → **3.51 mm**.
7. **F26** issued **PCN-001** against the routing rather than editing it.
8. **F27** discovered that **REQ-012 was never blocked by missing fatigue data — it was blocked by
   the temper.** 7050-T7451 has a full S/N suite. **17/18 → 18/18.**

**Also confirmed:** MMPDS reassigns section numbers. MIL-HDBK-5J 3.7.6.0(b3) is MMPDS 3.7.9.0(b2);
**MMPDS §3.7.6 is alloy 7056.** An inferred mapping would have looked right and pointed at the wrong
material. And 2003 equivalence did not hold — `Ftu(L)` moved 65 → 66 ksi.

---

## 4. Open items

| Item | Blocker | Effect |
|---|---|---|
| **7050 inspection interval** | crack-growth Figures 3.7.4.2.9(a)–(c) are graphical, not digitised | the 4,500-flight figure is **unverified for the released material** — largest open item |
| Ekvall alloy coverage for 7050 | needs the 1986 paper re-read | F12/F18/F19 rest on an unverified applicability assumption |
| Three unmapped MMPDS locators | need one more Knovel session | F21 mapping is 6 of 9 closed |
| Stress report on 7050 | writing time only | §4, §6.3, §8 still on 7075 |
| Mesh-converge the elastic-plastic ratio | ~40 min Ansys | inherits F7's three-mesh study |
| Run the NASTRAN decks | needs a licence | four predictions frozen, untested |
| `K_t` for the lug bore | derivation | **the dominant uncertainty in F27** |
| Single vs redundant load path | design decision | fixes A-basis vs B-basis; B-basis clears the scatter case |

---

## 5. Working preferences

- **Short, plain words. No yapping.** Low on credits.
- **Ruby drives.** Only work on what she asks for. Mention concerns in a sentence; don't act on them
  unasked. *(Changed 2026-08-06 — this file previously said the opposite.)*
- **Only ask Ruby for:** Ansys/FEA runs, browser logins, library access, physical file moves.
- **Be honest.** Never guess numbers or citations — verify or say you can't.
- **After each milestone, give % complete.**
- **Scope cuts unwelcome.**
- **Filenames Ruby types must be lowercase alphanumeric only** — Ansys VDI keyboard constraint.
- **Binaries cannot be pushed** (.png, .step, .xlsx, .wbpz). SVG works.
- **Do not run two agents against this repo at once** — parallel writers caused stale-SHA collisions
  and duplicated work on 2026-08-05.

### GitHub mechanics

- `create_or_update_file` only. **`push_files` returns 403.**
- Overwrites need the **git blob SHA** (`git rev-parse HEAD:path`), not SHA-256.
- Clone to the compute node and work locally.
- **Large files are expensive.** The 36 KB thread JSON and the 24 KB stress report each cost real
  credits to commit. Batch them; don't rewrite twice.

---

## 6. Tools and sources

| | |
|---|---|
| **FEA** | Ansys Mechanical 2025 R2 + APDL, TAMU VDI |
| **Critical** | Work on **`C:\Users\vin`**, never `H:` |
| **Ansys warning** | This lineage has corrupted **four times**: 7/29 bad write, 8/02 disk-full, 8/04 and 8/05 persisted solve-state locks. If Solve greys out with no process running: kill `AnsysWBU.exe`, delete `.lock`, and if that fails **restore from a clean parent rather than repairing** |
| **Current Ansys project** | `f7plastic7050` on `C:\Users\vin` — 7050 properties, both systems solved |
| **MMPDS** | **Knovel via TAMU Libraries → Databases A–Z → Knovel**, search `mmpds`, MMPDS-2026 Vol I |
| **Hand calcs** | Abbott Aerospace AA-SM-009-002 / -005 |
| **CAD** | Onshape; CadQuery |
| **References** | MMPDS-2026 Vol I (1 July 2026); Ekvall 1986 *J. Aircraft* 23(5) |

---

## 7. Lessons the project has paid for

- **Accuracy over speed.** Claude has made documented errors — mis-diagnosing a stress singularity
  twice, mis-assigning load components, unnecessary geometry revisions, claiming F16 would settle
  the double-counting question when it could not, and misreading a completed solve as failed.
  **Ruby caught several. All are recorded rather than erased.**
- **Failures stay visible.** Four of eight blind predictions failed and are still committed.
- **Three deck-level defects were found by inspection, not by result** — `NMODIF`, `SECDATA`,
  `PBEAM`. **All three produce believable numbers.**
- **A document can invalidate its own count by existing.** F21 reported 58 citations; publishing it
  made the figure 65, then 53. Fixed by classifying populations, not by patching the number.
- **Check the thickness band on every property, not just strength.** 7050's `K_Ic` also falls with
  section — 33 ksi√in at 1–2 in, 27 at 5–6. Same trap, different table.
- **A blocker can be about the wrong thing.** REQ-012 was "no fatigue data" for two months. It was
  really "no fatigue data *for this temper*", and a materials decision dissolved it.
- **Cost is set by the envelope, not the finished mass.**
- **Sequencing matters.** The thread's forward query correctly predicted that the elastic-plastic
  run would invalidate the tolerance scheme.

---

## 8. PROMPT TO PASTE INTO THE NEW CHAT

Copy everything below the line, and attach this file.

---

I'm Ruby (GitHub: XpiredRuby), Texas A&M aerospace senior. I'm continuing a portfolio project called
AeroFrame-DT. I've attached PROJECT_STATE.md — read it first.

Quick version: a rigorous stress substantiation of ONE aircraft part, a forward pylon-to-wingbox
attachment fitting (AF-DT-1000) on an MD-11-class aircraft. Repo is
github.com/XpiredRuby/aeroframe-dt, branch main. **18 of 18 requirements verified**, governing
margin MS = +0.151 on 7050-T7451, 27 analysis documents, 45 verification rows, hash-verified digital
thread.

HOW TO WORK WITH ME

Short, plain words. No yapping. I'm low on credits.

**I drive. Only work on what I ask for.** If you spot something you think matters, tell me in a
sentence — don't go do it. Don't hand me menus of options either; if I ask you to decide, decide.

If it's GitHub or software, you do it — you have write access. Commit with create_or_update_file
(needs the git blob SHA when overwriting; `git rev-parse HEAD:path`). push_files returns 403. Clone
to your compute node and work locally. Large files cost real credits — batch them.

Only ask me for: Ansys/FEA runs, browser logins, library access, physical file moves.

Be honest. Never guess numbers or citations — verify or say you can't. If you get something wrong,
say so plainly and correct it in the repo rather than quietly fixing it.

After each milestone, give % complete.

Filenames I have to type must be lowercase alphanumeric only — my Ansys VDI can't do Shift. You
can't push binaries. Don't run a second agent against this repo while you're working.

When giving me Ansys instructions, one step at a time. This project's Ansys files have corrupted
four times, most recently a persisted solve-state lock that greys out Solve. Don't repair it —
rebuild from a clean parent.

WHAT I WANT NEXT

Read PROJECT_STATE.md, check the repo, then tell me the highest-value remaining work. The biggest
open item is the 7050 inspection interval — the crack-growth curves in MMPDS are graphical and
nobody has digitised them, so the 4,500-flight figure is unverified for the released material.
