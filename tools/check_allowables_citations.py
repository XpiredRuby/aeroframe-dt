#!/usr/bin/env python3
"""F21 - inventory every material-allowables citation in the repository.

MIL-HDBK-5J was cancelled - notice issued 2004, restated 2006 - and superseded by MMPDS.
This project cites it throughout. The numbers are not in question - MMPDS-01 and
MIL-HDBK-5J were issued as technically equivalent documents for the 2003 transition
year - but the citation is to a cancelled document, and for a report written in the
shape of a certification substantiation that is a defect worth fixing.

This tool finds every citation, classifies it by the specific table or figure invoked,
and tracks the status of its MMPDS equivalent.

WHAT THIS TOOL DOES NOT DO. It does not invent MMPDS locators. Every entry starts at
status TO_VERIFY and only moves to CONFIRMED when someone has opened MMPDS and checked
the section number. A tool that guessed the mapping would be worse than no tool,
because the guesses would look like citations.

Six locators were confirmed against MMPDS-2026 on 2026-08-06; see F25 section 4. Three
remain TO_VERIFY and are deliberately NOT filled in by analogy, even though the
confirmed ones make the pattern look obvious: MMPDS section 3.7.6 is alloy 7056, not
7075, so an inferred citation would point at the wrong material.

Run:  python tools/check_allowables_citations.py
Out:  results/f21_citation_inventory.csv
Exit: 0 always - this is an inventory, not a gate, until the mapping is confirmed.
"""

from __future__ import annotations

import csv
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results"

SCAN_SUFFIXES = {".md", ".py", ".csv"}
SKIP_DIRS = {".git", "__pycache__", "results"}

# Three populations, not one. The headline number counts ONLY files that actually
# rely on the allowables, because that is the population a restatement has to fix.
#
# This distinction was learned twice. F21 first reported 58 citations, a figure its
# own publication invalidated (65). Excluding F21 and this tool fixed that and gave
# 51 - which then moved to 53 the moment the README, changelog and project state
# described the finding. A count that changes when you write about it is measuring
# the wrong thing.
META = {
    "docs/F21_ALLOWABLES_GOVERNANCE.md",
    "tools/check_allowables_citations.py",
}

NARRATIVE = {
    "README.md",
    "CHANGELOG.md",
    "PROJECT_STATE.md",
    "docs/HANDOFF.md",
    "tools/build_f14_thread.py",
    "docs/F23_MATERIAL_RESELECTION.md",
    "docs/F25_DAMAGE_TOLERANCE_7050.md",
    "docs/F26_PROCESS_CHANGE_NOTICE.md",
}

CITATION = re.compile(r"MIL-HDBK-5J?", re.IGNORECASE)

# Locators the project invokes. The MMPDS column is filled in only where the handbook
# has actually been opened and the section number read.
LOCATORS = {
    "3.7.6.0(b3)": ("7075-T7351 plate design mechanical properties, "
                    "2.001-2.500 in band - superseded as the design basis by F23",
                    "MMPDS-2026 Table 3.7.9.0(b2)"),
    "3.7.6.0(b1)": ("7075-T7351 plate, 0.500-1.000 in band - F12 correlation basis", ""),
    "3.1.2.3.1(b)": ("short-transverse property and SCC guidance", ""),
    "3.1.2.1.6": ("plane-strain fracture toughness K_Ic, information only", ""),
    "3.7.6.2.9(b)": ("da/dN crack growth rate data, F9 damage tolerance",
                     "MMPDS-2026 Figures 3.7.9.2.9(a)-(c)"),
    "3.7.6.2": ("S-N fatigue section - the original REQ-012 blocker; no curves for the "
                "T73/T7351 temper, confirmed still absent in MMPDS-2026",
                "MMPDS-2026 Section 3.7.9.2"),
}

# The released material basis is no longer in this table at all. 7050-T7451 is cited
# directly from MMPDS-2026 and has no MIL-HDBK-5J ancestry to map.
RELEASED_BASIS = {
    "allowables": "MMPDS-2026 Table 3.7.4.0(b1), 7050-T7451 plate, 5.001-6.000 in, A-basis",
    "fatigue": "MMPDS-2026 Figures 3.7.4.2.8(a)-(h), incl. notched Kt = 3.0",
    "crack_growth": "MMPDS-2026 Figures 3.7.4.2.9(a)-(c)",
}

# The transition facts, all verifiable from the cancellation notices themselves.
TRANSITION = {
    "superseded_document": "MIL-HDBK-5J, 31 January 2003",
    "superseding_document": "MMPDS (Metallic Materials Properties Development and "
                            "Standardization), maintained by Battelle for the FAA",
    "cancellation": "MIL-HDBK-5J cancelled; MMPDS named as replacement",
    "edition_read": "MMPDS-2026, Volume I, 1 July 2026, accessed via Knovel",
    "equivalence_note": "MMPDS-01 and MIL-HDBK-5J were issued as technically equivalent "
                        "for the 2003 transition year. That equivalence did NOT hold to "
                        "2026: Ftu(L) moved 65 -> 66 ksi and Fbru(e/D 2.0) 131 -> 132 in "
                        "the 7075-T7351 2.001-2.500 in band",
    "regulatory_note": "specific reference to MIL-HDBK-5 was removed from 14 CFR 23.613 "
                       "and 25.613; the FAA accepts MMPDS for metallic design allowables "
                       "and encourages the latest revision for new certification",
}


def _population(relative: str) -> str:
    if relative in META:
        return "meta"
    if relative in NARRATIVE:
        return "narrative"
    return "evidence"


def scan() -> list[dict]:
    rows: list[dict] = []
    for path in sorted(ROOT.rglob("*")):
        if not path.is_file() or path.suffix not in SCAN_SUFFIXES:
            continue
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for number, line in enumerate(text.splitlines(), start=1):
            if not CITATION.search(line):
                continue
            locator = next((key for key in LOCATORS if key in line), "")
            mmpds = LOCATORS.get(locator, ("", ""))[1]
            rows.append({
                "file": str(path.relative_to(ROOT)),
                "line": number,
                "locator": locator,
                "supplies": LOCATORS.get(locator, ("general reference", ""))[0],
                "mmpds_equivalent": mmpds or "TO_VERIFY",
                "status": "CONFIRMED" if mmpds else "TO_VERIFY",
                "context": line.strip()[:160],
                "population": _population(str(path.relative_to(ROOT)).replace("\\", "/")),
            })
    return rows


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    rows = scan()

    with (OUT / "f21_citation_inventory.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["file", "line", "locator", "supplies",
                                               "mmpds_equivalent", "status", "context",
                                               "population"],
                                lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)

    substantive = [row for row in rows if row["population"] == "evidence"]
    narrative = [row for row in rows if row["population"] == "narrative"]
    meta = [row for row in rows if row["population"] == "meta"]
    files = sorted({row["file"] for row in substantive})
    located = [row for row in substantive if row["locator"]]
    confirmed = [row for row in substantive if row["status"] == "CONFIRMED"]

    print(f"Evidence citations   : {len(substantive)} across {len(files)} files")
    print(f"Narrative            : {len(narrative)} in README/changelog/state - excluded")
    print(f"Meta                 : {len(meta)} in F21 and this tool - excluded")
    print(f"Tied to a locator    : {len(located)}")
    print(f"MMPDS mapping        : {len(confirmed)} confirmed, "
          f"{len(substantive) - len(confirmed)} to verify")
    print()
    print("Locators invoked by this project:")
    for key, (supplies, mmpds) in LOCATORS.items():
        hits = sum(1 for row in substantive if row["locator"] == key)
        state = mmpds if mmpds else "TO_VERIFY"
        print(f"  {key:16s} {hits:2d} citation(s)  [{state}]")
        print(f"                     {supplies}")
    print()
    print("Released material basis - no MIL-HDBK-5J ancestry:")
    for key, value in RELEASED_BASIS.items():
        print(f"  {key}: {value}")
    print()
    print("Transition basis:")
    for key, value in TRANSITION.items():
        print(f"  {key}: {value}")
    print()
    print("Written: results/f21_citation_inventory.csv")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
