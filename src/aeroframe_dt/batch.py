"""Safe batch-command construction and run-directory management."""
from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime, timezone
import json
from pathlib import Path
import shlex
from typing import Mapping, Sequence


@dataclass(frozen=True)
class BatchRun:
    run_id: str
    solver: str
    executable: str
    command: tuple[str, ...]
    working_directory: str
    input_file: str
    output_file: str
    environment: Mapping[str, str]
    created_utc: str

    def to_dict(self) -> dict:
        return asdict(self)

    def shell_preview(self) -> str:
        return " ".join(shlex.quote(part) for part in self.command)


def ansys_batch_run(run_id: str, executable: str, input_file: str, output_file: str, working_directory: str, processors: int = 2) -> BatchRun:
    if processors < 1:
        raise ValueError("processors must be positive")
    command = (executable, "-b", "-np", str(processors), "-i", input_file, "-o", output_file)
    return BatchRun(run_id, "ANSYS_MAPDL", executable, command, working_directory, input_file, output_file, {}, datetime.now(timezone.utc).isoformat())


def nastran_batch_run(run_id: str, executable: str, input_file: str, working_directory: str, scratch: str | None = None) -> BatchRun:
    command = [executable, input_file]
    if scratch:
        command.append(f"scr={scratch}")
    output_file = str(Path(input_file).with_suffix(".f06"))
    return BatchRun(run_id, "NASTRAN_OR_OPTISTRUCT", executable, tuple(command), working_directory, input_file, output_file, {}, datetime.now(timezone.utc).isoformat())


def write_run_contract(run: BatchRun, path: str | Path) -> None:
    target = Path(path); target.parent.mkdir(parents=True, exist_ok=True)
    payload = run.to_dict(); payload["shell_preview"] = run.shell_preview()
    target.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
