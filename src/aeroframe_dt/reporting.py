"""Deterministic Markdown and HTML engineering-report generation."""
from __future__ import annotations

from dataclasses import dataclass
from html import escape
import json
from pathlib import Path
from typing import Iterable, Mapping, Sequence


@dataclass(frozen=True)
class ReportSection:
    title: str
    body_markdown: str


def markdown_table(rows: Sequence[Mapping], columns: Sequence[str] | None = None) -> str:
    if not rows:
        return "_No rows._"
    columns = list(columns or rows[0].keys())
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join("---" for _ in columns) + " |"
    body = ["| " + " | ".join(str(row.get(column, "")) for column in columns) + " |" for row in rows]
    return "\n".join([header, separator, *body])


def engineering_report(
    title: str,
    document_id: str,
    revision: str,
    sections: Iterable[ReportSection],
    limitations: Iterable[str],
    evidence: Iterable[Mapping[str, str]],
) -> str:
    lines = [
        f"# {title}", "", f"**Document:** `{document_id}`  ", f"**Revision:** `{revision}`  ",
        "**Claim:** Representative, non-OEM, educational structural-engineering evidence.  ", "",
        "## Document control", "",
        "This report is generated from source-controlled inputs and compact result manifests. "
        "It is not a certification report and does not establish OEM accuracy.", "",
    ]
    for section in sections:
        lines.extend([f"## {section.title}", "", section.body_markdown.strip(), ""])
    lines.extend(["## Limitations", ""])
    lines.extend(f"- {item}" for item in limitations)
    evidence_rows = list(evidence)
    lines.extend(["", "## Evidence index", "", markdown_table(evidence_rows), ""])
    return "\n".join(lines)


def markdown_to_basic_html(markdown: str, title: str) -> str:
    """Convert the generated Markdown subset to standalone HTML without dependencies."""
    lines = markdown.splitlines(); html_lines: list[str] = []; in_list = False; in_code = False
    table_rows: list[list[str]] = []

    def flush_table() -> None:
        nonlocal table_rows
        if not table_rows: return
        html_lines.append("<table>")
        for index, cells in enumerate(table_rows):
            tag = "th" if index == 0 else "td"
            if index == 1 and all(set(cell) <= {"-", ":"} for cell in cells):
                continue
            html_lines.append("<tr>" + "".join(f"<{tag}>{escape(cell.strip())}</{tag}>" for cell in cells) + "</tr>")
        html_lines.append("</table>"); table_rows = []

    for line in lines:
        if line.startswith("```"):
            flush_table()
            if in_list: html_lines.append("</ul>"); in_list = False
            html_lines.append("</code></pre>" if in_code else "<pre><code>"); in_code = not in_code; continue
        if in_code:
            html_lines.append(escape(line)); continue
        if line.startswith("|") and line.endswith("|"):
            table_rows.append(line.strip("|").split("|")); continue
        flush_table()
        if line.startswith("# "): html_lines.append(f"<h1>{escape(line[2:])}</h1>")
        elif line.startswith("## "): html_lines.append(f"<h2>{escape(line[3:])}</h2>")
        elif line.startswith("### "): html_lines.append(f"<h3>{escape(line[4:])}</h3>")
        elif line.startswith("- "):
            if not in_list: html_lines.append("<ul>"); in_list = True
            html_lines.append(f"<li>{escape(line[2:])}</li>")
        elif not line.strip():
            if in_list: html_lines.append("</ul>"); in_list = False
        else:
            if in_list: html_lines.append("</ul>"); in_list = False
            html_lines.append(f"<p>{escape(line)}</p>")
    flush_table()
    if in_list: html_lines.append("</ul>")
    return """<!doctype html><html><head><meta charset="utf-8"><title>{}</title>
<style>body{{font-family:Arial,sans-serif;max-width:1100px;margin:40px auto;line-height:1.45;padding:0 20px}}table{{border-collapse:collapse;width:100%}}th,td{{border:1px solid #999;padding:6px;text-align:left}}code,pre{{background:#f4f4f4}}pre{{padding:12px;overflow:auto}}</style>
</head><body>{}</body></html>\n""".format(escape(title), "\n".join(html_lines))


def write_report(markdown: str, markdown_path: str | Path, html_path: str | Path | None = None, title: str = "AeroFrame-DT Report") -> None:
    md = Path(markdown_path); md.parent.mkdir(parents=True, exist_ok=True); md.write_text(markdown, encoding="utf-8")
    if html_path is not None:
        html = Path(html_path); html.parent.mkdir(parents=True, exist_ok=True); html.write_text(markdown_to_basic_html(markdown, title), encoding="utf-8")


def evidence_index_from_manifests(paths: Iterable[str | Path]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for path in paths:
        item = json.loads(Path(path).read_text(encoding="utf-8"))
        rows.append({
            "artifact": Path(path).as_posix(),
            "run_id": str(item.get("run_id", "")),
            "status": str(item.get("status", item.get("claim_level", ""))),
            "tool": str(item.get("tool", item.get("method", ""))),
        })
    return rows
