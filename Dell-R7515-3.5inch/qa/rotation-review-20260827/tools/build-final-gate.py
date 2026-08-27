#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("root", type=Path)
    args = parser.parse_args()
    root = args.root.resolve()
    qa = root / "qa" / "rotation-review-20260827"
    frozen = json.loads((qa / "frozen-hashes.json").read_text())
    evidence = json.loads((qa / "final-evidence-summary.json").read_text())
    inventory = json.loads((qa / "feature-inventory-review-summary.json").read_text())
    texture_sampling = json.loads((qa / "final-audits" / "texture-sampling.json").read_text())
    audit_names = ("views", "standard", "web", "rotation-structure-standard", "rotation-structure-web")
    audits = {name: json.loads((qa / "final-audits" / f"{name}.json").read_text()) for name in audit_names}
    comparison_faces = {}
    for face in ("front", "rear", "left", "right", "top", "bottom"):
        folder = qa / "matched-camera" / "three-standard" / face
        expected = [folder / name for name in ("source.png", "render.png", "overlay.png", "difference.png", "sheet.png")]
        comparison_faces[face] = {"files": [str(path.relative_to(root)) for path in expected],
                                  "complete": all(path.is_file() for path in expected)}
    checks = {
        "preReviewArchive": (root / "qa/superseded/pre-rotation-review-20260827/SNAPSHOT.md").is_file(),
        "frozenHashes": evidence.get("status") == "PASS" and all(item.get("match") for item in evidence.get("frozenHashChecks", {}).values()),
        "auditViews": audits["views"].get("status") == "PASS" and audits["views"].get("unresolvedCount") == 0,
        "auditStandard": audits["standard"].get("status") == "PASS" and audits["standard"].get("error_count") == 0,
        "auditWeb": audits["web"].get("status") == "PASS" and audits["web"].get("error_count") == 0,
        "rotationStructureStandard": audits["rotation-structure-standard"].get("status") == "PASS" and audits["rotation-structure-standard"].get("errorCount") == 0,
        "rotationStructureWeb": audits["rotation-structure-web"].get("status") == "PASS" and audits["rotation-structure-web"].get("errorCount") == 0,
        "loads40": evidence.get("loads", {}).get("actual") == 40 and evidence.get("loads", {}).get("uniqueNonces") == 40 and all(item.get("pass") for item in evidence.get("loads", {}).get("combos", [])),
        "rotationFourCombinations": evidence.get("rotation", {}).get("yawFrames") == 288 and all(item.get("pass") for item in evidence.get("rotation", {}).get("combos", [])),
        "inventory": inventory.get("status") == "PASS" and inventory.get("sourceRows") == inventory.get("reviewRows"),
        "matchedCamera": all(item["complete"] for item in comparison_faces.values()),
        "textureSamplingAndAtlas": texture_sampling.get("status") == "PASS" and texture_sampling.get("errorCount") == 0,
        "official3DReview": (qa / "official-3d-review.md").is_file(),
    }
    bottom_rows = inventory.get("statusCounts", {}).get("PASS_BOTTOM_FALLBACK", 0)
    errors = [name for name, passed in checks.items() if not passed]
    result = {
        "model": root.name, "frozen": frozen, "checks": checks,
        "audits": {name: {"status": value.get("status"),
                           "errors": value.get("errors", []),
                           "errorCount": value.get("errorCount", value.get("error_count", 0)),
                           "unresolvedCount": value.get("unresolvedCount", 0)} for name, value in audits.items()},
        "loads": evidence.get("loads"),
        "rotation": evidence.get("rotation"),
        "inventory": inventory,
        "textureSampling": texture_sampling,
        "matchedCamera": comparison_faces,
        "errors": errors, "errorCount": len(errors),
        "status": ("PASS_WITH_BOTTOM_FALLBACK" if bottom_rows else "PASS") if not errors else "REWORK",
    }
    (qa / "final-gate.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"model": root.name, "status": result["status"],
                      "errorCount": len(errors), "failedChecks": errors}, indent=2))


if __name__ == "__main__":
    main()
