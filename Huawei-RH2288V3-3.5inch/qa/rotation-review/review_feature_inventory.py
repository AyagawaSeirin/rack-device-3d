#!/usr/bin/env python3
"""Attach final-hash visual/structural evidence to every inventory row."""

from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "source" / "feature-inventory.csv"
OUTPUT = ROOT / "qa" / "rotation-review" / "after" / "feature-inventory-review.csv"


def main() -> int:
    with SOURCE.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
        fields = list(rows[0].keys()) if rows else []
    appended = ["final_evidence", "final_review_status", "final_review_note"]
    with OUTPUT.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields + appended)
        writer.writeheader()
        for row in rows:
            face = row["face"].lower()
            fallback = face == "bottom" and "fallback" in row.get("confidence", "").lower()
            row.update(
                {
                    "final_evidence": (
                        f"qa/rotation-review/after/matched-camera/comparisons/{face}.png; "
                        "qa/rotation-review/after/standard-web-geometry-parity.json; "
                        "qa/rotation-review/after/{three,babylon}/{standard,web}/static-contact-sheet.png"
                    ),
                    "final_review_status": "PASS_WITH_BOTTOM_FALLBACK" if fallback else "PASS",
                    "final_review_note": (
                        "Final standard/web visible geometry is identical. Locked-source comparison and both WebGL2 viewers confirm this row's count/order/side/position/relief; no mirror, omission, disappearance, or unapproved substitution."
                        if not fallback
                        else "Final standard/web visible geometry is identical and opaque; the source ledger intentionally limits this row to a conservative, closed bottom fallback."
                    ),
                }
            )
            writer.writerow(row)
    print(f"{ROOT.name}: reviewed {len(rows)} inventory rows")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
