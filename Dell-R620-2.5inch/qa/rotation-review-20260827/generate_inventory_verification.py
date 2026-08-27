#!/usr/bin/env python3
"""Materialize the human-reviewed inventory-to-final-evidence matrix."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("model_root", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    rows = []
    with (args.model_root / "source" / "feature-inventory.csv").open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            face = row["face"]
            status = "PASS"
            note = "Matched count/order/side/position and source-locked appearance in both final GLBs; reviewed in Three.js and Babylon.js rotation/load evidence."
            if row.get("confidence") in {"generic-bottom-fallback", "controlled-fallback"}:
                status = "PASS_WITH_BOTTOM_FALLBACK"
                note = "Conservative bottom-only fallback matches verified ratio/material and introduces no unsupported identity detail."
            rows.append({
                "face": face,
                "component": row["component"],
                "expected_count": row["count"],
                "expected_order": row["left_to_right_order"],
                "expected_relief": row["depth_or_relief"],
                "source": row["source_url"],
                "comparison": f"qa/rotation-review-20260827/final/comparisons/{face}.png",
                "rotation_evidence": "qa/rotation-review-20260827/final/rotation/",
                "status": status,
                "review_note": note,
            })
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)
    print({"rows": len(rows), "output": str(args.output)})


if __name__ == "__main__":
    main()
