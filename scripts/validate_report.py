#!/usr/bin/env python3
"""Validate structural invariants of an evidence-based product teardown HTML."""

from __future__ import annotations

import argparse
import re
import sys
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path


class ReportParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.counts: Counter[str] = Counter()
        self.ids: list[str] = []
        self.anchors: list[str] = []
        self.title_depth = 0
        self.title_text: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self.counts[tag] += 1
        values = dict(attrs)
        if values.get("id"):
            self.ids.append(values["id"] or "")
        href = values.get("href")
        if tag == "a" and href and href.startswith("#"):
            self.anchors.append(href[1:])
        if tag == "title":
            self.title_depth += 1

    def handle_endtag(self, tag: str) -> None:
        if tag == "title" and self.title_depth:
            self.title_depth -= 1

    def handle_data(self, data: str) -> None:
        if self.title_depth:
            self.title_text.append(data)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("report", type=Path)
    parser.add_argument("--require-all-layers", action="store_true")
    args = parser.parse_args()

    if not args.report.is_file():
        print(f"ERROR: file not found: {args.report}")
        return 2

    source = args.report.read_text(encoding="utf-8")
    parsed = ReportParser()
    parsed.feed(source)
    errors: list[str] = []

    if not "".join(parsed.title_text).strip():
        errors.append("missing non-empty <title>")
    if parsed.counts["h1"] != 1:
        errors.append(f"expected exactly one <h1>, found {parsed.counts['h1']}")
    if parsed.counts["main"] != 1:
        errors.append(f"expected exactly one <main>, found {parsed.counts['main']}")

    duplicates = sorted(item for item, count in Counter(parsed.ids).items() if count > 1)
    if duplicates:
        errors.append("duplicate ids: " + ", ".join(duplicates))
    missing = sorted(set(parsed.anchors) - set(parsed.ids))
    if missing:
        errors.append("unresolved anchors: " + ", ".join(missing))

    forbidden = re.findall(r"\b(?:TODO|CONTINUE|PLACEHOLDER)\b", source, re.IGNORECASE)
    if forbidden:
        errors.append("unfinished placeholder tokens found")

    evidence_ids = re.findall(r"\bE-[SPCLR]\d{2,}\b", source)
    if not evidence_ids:
        errors.append("no evidence IDs such as E-S01/E-P01/E-C01/E-L01/E-R01 found")

    labels = ["页面事实", "代码事实", "合理推断", "尚未确认", "产品建议"]
    if not any(label in source for label in labels):
        errors.append("no evidence-level label found")

    if args.require_all_layers:
        for layer in ("用户层", "技术层", "模型层", "数据层"):
            if layer not in source:
                errors.append(f"missing required layer: {layer}")

    if errors:
        for error in errors:
            print("ERROR:", error)
        return 1

    print(f"OK: {args.report}")
    print(f"Evidence references: {len(evidence_ids)}; unique: {len(set(evidence_ids))}")
    print(f"Sections: {parsed.counts['section']}; tables: {parsed.counts['table']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
