#!/usr/bin/env python3
"""Extract official PDF text and render the evidence pages used for R7515."""

from pathlib import Path

import pymupdf


ROOT = Path(__file__).resolve().parents[1]
ORIGINALS = ROOT / "source" / "originals"
PAGES = ROOT / "source" / "pdf-pages"

PAGE_SELECTIONS = {
    "dell-emc-poweredge-r7515-technical-guide.pdf": [9, 10, 11, 12, 13],
    "dell-emc-poweredge-r7515-technical-specifications.pdf": [5, 6, 7, 8, 9, 10],
    "dell-poweredge-r7515-installation-service-manual.pdf": [
        9, 10, 11, 12, 13, 14, 15, 17, 20, 29, 30, 31,
        28, 35, 37, 39, 40, 41, 42, 43, 44, 45, 46, 51, 52,
        63, 68, 75, 76, 77, 78, 79, 81, 82, 89, 95, 96, 97,
        98, 99, 100, 101, 102, 103, 106, 108, 109, 111, 112,
        113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123,
        124, 125, 126, 127, 128, 129, 130,
    ],
    "dell-poweredge-r7515-spec-sheet.pdf": [1, 2, 3],
}


def main() -> None:
    PAGES.mkdir(parents=True, exist_ok=True)
    for name, one_based_pages in PAGE_SELECTIONS.items():
        source = ORIGINALS / name
        document = pymupdf.open(source)
        stem = source.stem
        text = "\n\n".join(
            f"===== PDF PAGE {index + 1} =====\n{page.get_text()}"
            for index, page in enumerate(document)
        )
        (PAGES / f"{stem}.txt").write_text(text, encoding="utf-8")
        for page_number in one_based_pages:
            page = document[page_number - 1]
            pixmap = page.get_pixmap(matrix=pymupdf.Matrix(2.5, 2.5), alpha=False)
            pixmap.save(PAGES / f"{stem}-p{page_number:03d}.png")


if __name__ == "__main__":
    main()
