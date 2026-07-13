"""Open digital-thread exchange manifests and QIF-style inspection XML."""
from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from hashlib import sha256
import json
from pathlib import Path
import xml.etree.ElementTree as ET
from typing import Iterable


@dataclass(frozen=True)
class ModelExchangeRecord:
    model_id: str
    revision: str
    native_file: str
    exchange_file: str
    exchange_format: str
    coordinate_system: str
    units: str
    pmi_authority: str
    native_sha256: str
    exchange_sha256: str
    created_utc: str
    claim_level: str = "REPRESENTATIVE_NON_OEM"

    def to_dict(self) -> dict:
        return asdict(self)


def file_hash(path: str | Path) -> str:
    return sha256(Path(path).read_bytes()).hexdigest()


def build_model_exchange_record(
    model_id: str,
    revision: str,
    native_file: str | Path,
    exchange_file: str | Path,
    exchange_format: str,
    coordinate_system: str,
    units: str,
    pmi_authority: str,
) -> ModelExchangeRecord:
    native, exchange = Path(native_file), Path(exchange_file)
    if not native.is_file() or not exchange.is_file():
        raise FileNotFoundError("native and exchange files must exist")
    return ModelExchangeRecord(
        model_id, revision, native.as_posix(), exchange.as_posix(), exchange_format,
        coordinate_system, units, pmi_authority, file_hash(native), file_hash(exchange),
        datetime.now(timezone.utc).isoformat(),
    )


def write_exchange_manifest(record: ModelExchangeRecord, path: str | Path) -> None:
    Path(path).write_text(json.dumps(record.to_dict(), indent=2, sort_keys=True) + "\n", encoding="utf-8")


def qif_style_inspection_xml(part_id: str, revision: str, characteristics: Iterable[dict]) -> str:
    """Build a transparent QIF-style open XML sidecar.

    This is not represented as schema-valid QIF. It preserves identifiers and
    measurement links until a licensed/standards-compliant QIF writer is used.
    """
    root = ET.Element("AeroFrameQIFSidecar", attrib={
        "partId": part_id, "revision": revision,
        "claimLevel": "OPEN_EQUIVALENT_NOT_SCHEMA_VALID_QIF",
    })
    chars = ET.SubElement(root, "Characteristics")
    for item in characteristics:
        required = {"id", "feature_id", "requirement_id", "nominal", "lower", "upper", "units", "method"}
        missing = required - set(item)
        if missing:
            raise KeyError(f"characteristic missing: {', '.join(sorted(missing))}")
        node = ET.SubElement(chars, "Characteristic", attrib={
            "id": str(item["id"]), "featureId": str(item["feature_id"]),
            "requirementId": str(item["requirement_id"]), "units": str(item["units"]),
        })
        ET.SubElement(node, "Nominal").text = str(item["nominal"])
        ET.SubElement(node, "LowerLimit").text = str(item["lower"])
        ET.SubElement(node, "UpperLimit").text = str(item["upper"])
        ET.SubElement(node, "InspectionMethod").text = str(item["method"])
    ET.indent(root)
    return ET.tostring(root, encoding="unicode", xml_declaration=True) + "\n"


def validate_qif_sidecar(xml_text: str) -> list[str]:
    root = ET.fromstring(xml_text)
    issues: list[str] = []
    if root.tag != "AeroFrameQIFSidecar": issues.append("unexpected root tag")
    if root.attrib.get("claimLevel") != "OPEN_EQUIVALENT_NOT_SCHEMA_VALID_QIF": issues.append("claim level missing")
    ids: set[str] = set()
    for node in root.findall("./Characteristics/Characteristic"):
        identifier = node.attrib.get("id", "")
        if not identifier: issues.append("blank characteristic id")
        if identifier in ids: issues.append(f"duplicate characteristic id: {identifier}")
        ids.add(identifier)
        for child in ("Nominal", "LowerLimit", "UpperLimit", "InspectionMethod"):
            if node.findtext(child) in (None, ""): issues.append(f"{identifier}: missing {child}")
    if not ids: issues.append("no characteristics")
    return issues
