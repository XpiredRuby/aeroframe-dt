"""Reproducibility manifests and file hashing utilities."""
from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from hashlib import sha256
import json
from pathlib import Path
from typing import Any, Iterable


def sha256_file(path: str | Path, chunk_size: int = 1024 * 1024) -> str:
    digest = sha256()
    with Path(path).open("rb") as stream:
        while chunk := stream.read(chunk_size):
            digest.update(chunk)
    return digest.hexdigest()


@dataclass(frozen=True)
class FileRecord:
    path: str
    sha256: str
    bytes: int
    role: str


@dataclass
class RunManifest:
    run_id: str
    tool: str
    tool_version: str
    status: str
    claim_level: str = "SYNTHETIC_TEST_ONLY"
    created_utc: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    inputs: list[FileRecord] = field(default_factory=list)
    outputs: list[FileRecord] = field(default_factory=list)
    parameters: dict[str, Any] = field(default_factory=dict)
    notes: list[str] = field(default_factory=list)

    def add_file(self, path: str | Path, role: str, output: bool = False, base: str | Path | None = None) -> FileRecord:
        path_obj = Path(path)
        shown = path_obj.relative_to(base).as_posix() if base is not None else path_obj.as_posix()
        record = FileRecord(shown, sha256_file(path_obj), path_obj.stat().st_size, role)
        (self.outputs if output else self.inputs).append(record)
        return record

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    def write(self, path: str | Path) -> None:
        target = Path(path)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(json.dumps(self.to_dict(), indent=2, sort_keys=True) + "\n", encoding="utf-8")


def inventory(root: str | Path, paths: Iterable[str | Path], role: str) -> list[FileRecord]:
    root_obj = Path(root)
    records: list[FileRecord] = []
    for item in paths:
        path = root_obj / item
        records.append(FileRecord(Path(item).as_posix(), sha256_file(path), path.stat().st_size, role))
    return records
