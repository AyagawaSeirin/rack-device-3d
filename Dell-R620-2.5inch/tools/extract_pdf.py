#!/usr/bin/env python3
"""Extract PDF text and render selected pages for source inspection."""

from __future__ import annotations

import argparse
from pathlib import Path

import pymupdf


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("pdf", type=Path)
    parser.add_argument("--text-out", type=Path, required=True)
    parser.add_argument("--render-dir", type=Path)
    parser.add_argument("--pages", help="Comma-separated one-based pages or ranges")
    parser.add_argument("--dpi", type=int, default=180)
    args = parser.parse_args()

    document = pymupdf.open(args.pdf)
    text_parts = []
    for index, page in enumerate(document):
        text_parts.append(f"\n\n===== PAGE {index + 1} =====\n\n{page.get_text()}")
    args.text_out.parent.mkdir(parents=True, exist_ok=True)
    args.text_out.write_text("".join(text_parts), encoding="utf-8")

    if not args.render_dir or not args.pages:
        return

    selected: set[int] = set()
    for token in args.pages.split(","):
        if "-" in token:
            first, last = (int(value) for value in token.split("-", 1))
            selected.update(range(first, last + 1))
        else:
            selected.add(int(token))
    args.render_dir.mkdir(parents=True, exist_ok=True)
    matrix = pymupdf.Matrix(args.dpi / 72.0, args.dpi / 72.0)
    for page_number in sorted(selected):
        if not 1 <= page_number <= len(document):
            raise ValueError(f"page {page_number} outside 1..{len(document)}")
        pixmap = document[page_number - 1].get_pixmap(matrix=matrix, alpha=False)
        stem = args.pdf.stem
        pixmap.save(args.render_dir / f"{stem}-p{page_number:02d}.png")


if __name__ == "__main__":
    main()
