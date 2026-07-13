#!/usr/bin/env python3
"""One-shot repository payload installer used only for the software completion sync."""
from __future__ import annotations

import base64
import io
from pathlib import Path
import shutil
import tarfile

ROOT = Path(__file__).resolve().parents[1]
CHUNKS = ROOT / ".software_sync" / "chunks"

def safe_extract(blob: bytes) -> None:
    with tarfile.open(fileobj=io.BytesIO(blob), mode="r:gz") as archive:
        root = ROOT.resolve()
        for member in archive.getmembers():
            target = (ROOT / member.name).resolve()
            if target != root and root not in target.parents:
                raise RuntimeError(f"unsafe archive member: {member.name}")
        archive.extractall(ROOT, filter="data")

def main() -> int:
    parts = sorted(CHUNKS.glob("chunk_*"))
    if not parts:
        raise RuntimeError("software payload chunks are missing")
    encoded = b"".join(p.read_bytes() for p in parts)
    safe_extract(base64.b64decode(encoded, validate=True))
    shutil.rmtree(ROOT / ".software_sync")
    print(f"installed {len(parts)} verified payload chunks")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
