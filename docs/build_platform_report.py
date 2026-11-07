"""Assemble docs/ai_hub_platform_structure.html from the house template, the inline flowchart SVG and the report body.

Data layer: documentation. No spatial data; no CRS applies. Run from the docs folder.
"""
from __future__ import annotations

import html.parser
from pathlib import Path

HERE = Path(__file__).resolve().parent
TEMPLATE = Path(r"C:\Users\po.nienchen\.claude\skills\pp_workflow_report\template.html")


def main() -> None:
    """Write the HTML report and parse-check it."""
    tpl = TEMPLATE.read_text(encoding="utf-8")
    head = tpl.split("<header>")[0].replace("[PROJECT] — [report title]", "AI_Hub — how the gateway works")
    svg = (HERE / "ai_hub_platform_flow.svg").read_text(encoding="utf-8")
    body = (HERE / "platform_report_body.html").read_text(encoding="utf-8").replace("{{SVG}}", svg)
    out = HERE / "ai_hub_platform_structure.html"
    out.write_text(head + body, encoding="utf-8")
    html.parser.HTMLParser().feed(out.read_text("utf-8"))
    print(f"written and parsed: {out} ({out.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
