#!/usr/bin/env python3
"""Validate requirement IDs and verification-matrix references."""

from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as stream:
        return list(csv.DictReader(stream))


def main() -> int:
    requirements = read_csv(ROOT / "requirements" / "requirements.csv")
    verification = read_csv(ROOT / "requirements" / "verification_matrix.csv")
    ids = [row["requirement_id"] for row in requirements]
    errors: list[str] = []
    if len(ids) != len(set(ids)):
        errors.append("Duplicate requirement_id found")
    id_set = set(ids)
    for row in requirements:
        parent = row["parent_id"].strip()
        if parent and parent not in id_set:
            errors.append(f"Unknown parent {parent} for {row['requirement_id']}")
        evidence = row["evidence_path"].strip()
        if evidence and not (ROOT / evidence).exists():
            errors.append(f"Missing evidence path {evidence} for {row['requirement_id']}")
    for row in verification:
        if row["requirement_id"] not in id_set:
            errors.append(f"Verification {row['verification_id']} references unknown requirement")
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print(f"Traceability OK: {len(requirements)} requirements, {len(verification)} verification rows")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
