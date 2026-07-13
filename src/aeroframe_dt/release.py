"""Release auditing and reproducible source-package creation."""
from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
import json
from pathlib import Path
import tarfile
from typing import Iterable


PROHIBITED_SUFFIXES = {".db", ".rst", ".op2", ".h3d", ".full", ".emat", ".esav", ".osav"}


@dataclass(frozen=True)
class ReleaseIssue:
    path: str
    severity: str
    message: str


def audit_repository(root: str | Path) -> list[ReleaseIssue]:
    root_path = Path(root); issues: list[ReleaseIssue] = []
    required = [
        "PROJECT_STATE.md", "requirements/requirements.csv", "requirements/verification_matrix.csv",
        "loads/ASSUMPTIONS_AND_PROVENANCE.md", "benchmarks/BENCHMARK_LOCK.md",
        "docs/DECISIONS.md", "docs/RISKS_AND_LIMITATIONS.md", "docs/STRESS_REPORT.md", "CHANGELOG.md",
    ]
    for relative in required:
        if not (root_path / relative).is_file(): issues.append(ReleaseIssue(relative, "ERROR", "required project-control file is missing"))
    for path in root_path.rglob("*"):
        if not path.is_file() or ".git" in path.parts: continue
        relative = path.relative_to(root_path).as_posix()
        if path.suffix.lower() in PROHIBITED_SUFFIXES:
            issues.append(ReleaseIssue(relative, "ERROR", "large/proprietary solver database must not be committed"))
        if path.stat().st_size > 20 * 1024 * 1024:
            issues.append(ReleaseIssue(relative, "WARNING", "file exceeds 20 MiB; verify compact-result policy"))
        if "__pycache__" in path.parts or path.suffix == ".pyc":
            continue  # excluded from deterministic releases and ignored by Git
    return issues


def create_source_release(root: str | Path, output: str | Path, include: Iterable[str] | None = None) -> dict:
    root_path, output_path = Path(root), Path(output)
    issues = [issue for issue in audit_repository(root_path) if issue.severity == "ERROR"]
    if issues:
        raise ValueError("release audit failed: " + "; ".join(f"{item.path}: {item.message}" for item in issues))
    selected = set(include or [])
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with tarfile.open(output_path, "w:gz", format=tarfile.PAX_FORMAT) as archive:
        for path in sorted(root_path.rglob("*")):
            if not path.is_file() or ".git" in path.parts or "__pycache__" in path.parts or path.suffix == ".pyc": continue
            relative = path.relative_to(root_path).as_posix()
            if selected and not any(relative == prefix or relative.startswith(prefix.rstrip("/") + "/") for prefix in selected): continue
            info = archive.gettarinfo(str(path), arcname=f"aeroframe-dt/{relative}")
            info.mtime = 0; info.uid = info.gid = 0; info.uname = info.gname = ""
            with path.open("rb") as stream: archive.addfile(info, stream)
    digest = sha256(output_path.read_bytes()).hexdigest()
    manifest = {"archive": output_path.name, "sha256": digest, "bytes": output_path.stat().st_size}
    output_path.with_suffix(output_path.suffix + ".json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    return manifest
