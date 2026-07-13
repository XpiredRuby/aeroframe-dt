"""Blind-prediction preservation and public-data correlation metrics."""
from __future__ import annotations

from dataclasses import asdict, dataclass
from hashlib import sha256
import json
from math import sqrt
from pathlib import Path
from statistics import mean
from typing import Iterable, Mapping, Sequence


@dataclass(frozen=True)
class CorrelationMetrics:
    count: int
    rmse: float
    normalized_rmse: float
    mean_bias: float
    max_absolute_error: float
    r_squared: float | None

    def to_dict(self) -> dict:
        return asdict(self)


def metrics(observed: Sequence[float], predicted: Sequence[float]) -> CorrelationMetrics:
    if len(observed) != len(predicted) or not observed:
        raise ValueError("observed and predicted arrays must be equal and nonempty")
    errors = [p - y for y, p in zip(observed, predicted)]
    rmse = sqrt(mean(error * error for error in errors))
    span = max(observed) - min(observed)
    scale = span if span > 0 else max(abs(value) for value in observed)
    normalized = rmse / max(scale, 1e-30)
    avg = mean(observed)
    ss_tot = sum((value - avg) ** 2 for value in observed)
    ss_res = sum(error * error for error in errors)
    r2 = None if ss_tot == 0 else 1 - ss_res / ss_tot
    return CorrelationMetrics(len(observed), rmse, normalized, mean(errors), max(abs(error) for error in errors), r2)


def freeze_dataset(path: str | Path, dataset_id: str, source_uri: str, license_note: str) -> dict:
    file = Path(path)
    if not file.is_file():
        raise FileNotFoundError(file)
    return {
        "dataset_id": dataset_id,
        "path": file.as_posix(),
        "sha256": sha256(file.read_bytes()).hexdigest(),
        "bytes": file.stat().st_size,
        "source_uri": source_uri,
        "license_note": license_note,
        "frozen_before_prediction_review": True,
    }


def correlation_record(
    specimen_ids: Sequence[str],
    observed: Sequence[float],
    blind_prediction: Sequence[float],
    post_correlation_prediction: Sequence[float] | None,
    original_parameters: Mapping[str, float | str],
    updated_parameters: Mapping[str, float | str] | None,
    dataset_manifest: Mapping,
) -> dict:
    if len(specimen_ids) != len(observed) or len(observed) != len(blind_prediction):
        raise ValueError("specimen IDs, observations, and blind predictions must align")
    post = list(post_correlation_prediction) if post_correlation_prediction is not None else None
    if post is not None and len(post) != len(observed):
        raise ValueError("post-correlation predictions must align")
    changes: dict[str, dict] = {}
    if updated_parameters is not None:
        for key in sorted(set(original_parameters) | set(updated_parameters)):
            before, after = original_parameters.get(key), updated_parameters.get(key)
            if before != after:
                changes[key] = {"before": before, "after": after}
    rows = [
        {
            "specimen_id": specimen_ids[i], "observed": observed[i],
            "blind_prediction": blind_prediction[i],
            "post_correlation_prediction": None if post is None else post[i],
        }
        for i in range(len(observed))
    ]
    return {
        "dataset": dict(dataset_manifest),
        "blind_metrics": metrics(observed, blind_prediction).to_dict(),
        "post_correlation_metrics": None if post is None else metrics(observed, post).to_dict(),
        "original_parameters": dict(original_parameters),
        "updated_parameters": None if updated_parameters is None else dict(updated_parameters),
        "parameter_changes": changes,
        "rows": rows,
        "claim": "PUBLIC_DATA_CORRELATION_NOT_PHYSICAL_CERTIFICATION",
    }


def write_correlation_record(record: Mapping, path: str | Path) -> None:
    target = Path(path); target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n", encoding="utf-8")
