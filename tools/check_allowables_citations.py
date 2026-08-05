#!/usr/bin/env python3
"""F21 - inventory every material-allowables citation in the repository.

MIL-HDBK-5J was cancelled in March 2006 and superseded by MMPDS. This project cites
it throughout. The numbers are not in question - MMPDS-01 and MIL-HDBK-5J were issued
as technically equivalent documents for the 2003 transition year - but the citation
is to a cancelled document, and for a report written in the shape of a certification
substantiation that is a defect worth fixing.

This tool finds every citation, classifies it by the specific table or figure invoked,
and tracks the status of its MMPDS equivalent.

WHAT THIS TOOL DOES NOT DO. It does not invent MMPDS locators. Every entry starts at
status TO_VERIFY and only moves to CONFIRMED when someone has opened MMPDS and checked
the section number and the values. A tool that guessed the mapping would be worse than
no tool, because the guesses would look like citations.

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

CITATION = re.compile(r"MIL-HDBK-5J?", re.IGNORECASE)

# Locators the project actually invokes, with what each supplies. The MMPDS column is
# deliberately empty: it is filled in by hand after the handbook has been opened.
LOCATORS = {
    "3.7.6.0(b3)": ("7075-T7351 plate design mechanical properties, "
                    "2.001-2.500 in band - the governing allowables", ""),
    "3.7.6.0(b1)": ("7075-T7351 plate, 0.500-1.000 in band - F12 correlation basis", ""),
    "3.1.2.3.1(b)": ("short-transverse property and SCC guidance", ""),
    "3.1.2.1.6": ("plane-strain fracture toughness K_Ic, information only", ""),
    "3.7.6.2.9(b)": ("da/dN crack growth rate data, F9 damage tolerance", ""),
    "3.7.6.2": ("S-N fatigue section - the REQ-012 blocker; "
                "no curves for the T7351 temper in 5J", ""),
}

# The transition facts, all verifiable from the cancellation notices themselves.
TRANSITION = {
    "superseded_document": "MIL-HDBK-5J, 31 January 2003",
    "superseding_document": "MMPDS (Metallic Materials Properties Development and "
                            "Standardization), maintained by Battelle for the FAA",
    "cancellation": "MIL-HDBK-5J cancelled; MMPDS named as replacement",
    "equivalence_note": "MMPDS-01 and MIL-HDBK-5J were issued as technically equivalent "
                        "for the 2003 transition year, so the VALUES used in this "
                        "project are not in question - only the currency of the citation",
    "regulatory_note": "specific reference to MIL-HDBK-5 was removed from 14 CFR 23.613 "
                       "and 25.613; the FAA accepts MMPDS for metallic design allowables "
                       "and encourages the latest revision for new certification",
}


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
            rows.append({
                "file": str(path.relative_to(ROOT)),
                "line": number,
                "locator": locator,
                "supplies": LOCATORS.get(locator, ("general reference", ""))[0],
                "mmpds_equivalent": LOCATORS.get(locator, ("", ""))[1] or "TO_VERIFY",
                "status": "CONFIRMED" if LOCATORS.get(locator, ("", ""))[1] else "TO_VERIFY",
                "context": line.strip()[:160],
            })
    return rows


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    rows = scan()

    with (OUT / "f21_citation_inventory.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["file", "line", "locator", "supplies",
                                               "mmpds_equivalent", "status", "context"],
                                lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)

    files = sorted({row["file"] for row in rows})
    located = [row for row in rows if row["locator"]]
    confirmed = [row for row in rows if row["status"] == "CONFIRMED"]

    print(f"Citations found      : {len(rows)} across {len(files)} files")
    print(f"Tied to a locator    : {len(located)}")
    print(f"MMPDS mapping        : {len(confirmed)} confirmed, "
          f"{len(rows) - len(confirmed)} to verify")
    print()
    print("Locators invoked by this project:")
    for key, (supplies, mmpds) in LOCATORS.items():
        hits = sum(1 for row in rows if row["locator"] == key)
        state = mmpds if mmpds else "TO_VERIFY"
        print(f"  {key:16s} {hits:2d} citation(s)  [{state}]  {supplies}")
    print()
    print("Transition basis:")
    for key, value in TRANSITION.items():
        print(f"  {key}: {value}")
    print()
    print("Written: results/f21_citation_inventory.csv")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
