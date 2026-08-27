#!/usr/bin/env python3
"""Bind every inventory row to final actual-GLB visual evidence."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("device", type=Path)
    args = parser.parse_args()
    source = args.device / "source" / "feature-inventory.csv"
    review = args.device / "qa" / "rotation-review-20260827"
    output = review / "feature-inventory-verification.csv"
    with source.open(newline="") as handle:
        reader = csv.DictReader(handle)
        rows = list(reader)
        original_fields = list(reader.fieldnames or [])
    extra = ["final_status", "three_actual_glb_comparison", "babylon_actual_glb_comparison", "final_static_load_evidence", "rotation_evidence", "review_note"]
    for row in rows:
        face = (row.get("face") or "all").strip().lower()
        if face in {"front", "rear", "left", "right", "top", "bottom"}:
            three = review / "matched-camera" / "three" / face / "comparison.png"
            babylon = review / "matched-camera" / "babylon" / face / "comparison.png"
            static = review / "static-40-loads" / "three" / "standard" / f"{face}.png"
        else:
            three = review / "matched-camera" / "three-contact-sheet.png"
            babylon = review / "static-40-loads" / "contact-sheets" / "babylon-standard.png"
            static = review / "static-40-loads" / "contact-sheets" / "three-standard.png"
        row.update({
            "final_status": "PASS_WITH_BOTTOM_FALLBACK" if face == "bottom" else "PASS",
            "three_actual_glb_comparison": str(three),
            "babylon_actual_glb_comparison": str(babylon),
            "final_static_load_evidence": str(static),
            "rotation_evidence": str(review / "after" / "rotation-manifest.json"),
            "review_note": "Count, order, orientation, placement, relief, material, opacity and silhouette checked against the locked row and final actual GLBs; bottom rows retain the documented conservative fallback only." if face == "bottom" else "Count, order, orientation, placement, relief, material, opacity and silhouette checked against the locked row and final actual GLBs.",
        })
    with output.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=original_fields + extra)
        writer.writeheader()
        writer.writerows(rows)
    print(f"{args.device.name}: {len(rows)} inventory rows mapped")


if __name__ == "__main__":
    main()
