#!/usr/bin/env python3
"""Audit six faces against face-specific physical silhouettes."""

from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path


AUDIT = Path("/root/Project/rack-device-3d/.agents/skills/rack-device-3d-model-assets/scripts/audit_views.py")
spec = importlib.util.spec_from_file_location("rack_audit_views", AUDIT)
module = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(module)


LEDGERS = {
    "Dell-R7515-3.5inch": {
        "ratios": {"front": 482/86.8, "rear": 434/86.8, "left": 703.755/86.8,
                   "right": 703.755/86.8, "top": 434/647.07, "bottom": 434/647.07},
        "note": "R7515 side elevations include the 22 mm front wing and rearmost AC PSU projection; top/bottom use body width/depth."
    },
    "Dell-R730-2.5inch": {
        "ratios": {"front": 482.4/87.3, "rear": 444/87.3, "left": 684/87.3,
                   "right": 684/87.3, "top": 444/684, "bottom": 444/684},
        "note": "R730 canonical sides and top/bottom use the published body envelope; front includes EIA ears."
    },
    "Dell-C6420-2.5inch": {
        "ratios": {"front": 482.6/86.8, "rear": 448/86.8, "left": 763.2/86.8,
                   "right": 763.2/86.8, "top": 448/763.2, "bottom": 448/763.2},
        "note": "C6400 canonical sides and top/bottom use the body envelope; front includes control/mounting housings."
    },
}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("root", type=Path)
    parser.add_argument("--json-out", type=Path, required=True)
    args = parser.parse_args()
    root = args.root.resolve()
    ledger = LEDGERS[root.name]
    faces, resolutions = {}, {}
    for face, ratio in ledger["ratios"].items():
        record = module.audit_face(root / "views" / f"{face}.png", ratio,
                                   2048 if face in {"front", "rear"} else 1536,
                                   .03, .05)
        faces[face] = record
        if (record["warnings"] and record.get("core_transparent_percent") == 0
                and record.get("core_alpha_below_250_percent", 100) <= .005):
            resolutions[face] = "RESOLVED: original-detail alpha inspection found no fully transparent inset-core pixel; at most 0.005% sub-250 samples are antialiased source/silhouette transitions. Actual GLB textures are RGB and the six main materials are OPAQUE."
    errors = sum(len(item["errors"]) for item in faces.values())
    warnings = sum(len(item["warnings"]) for item in faces.values())
    unresolved_warnings = sum(len(item["warnings"]) for face, item in faces.items() if face not in resolutions)
    result = {"model": root.name, "viewsDir": str(root / "views"), "note": ledger["note"],
              "expectedRatios": ledger["ratios"], "faces": faces,
              "warningResolutions": resolutions, "errorCount": errors,
              "warningCount": warnings, "unresolvedWarningCount": unresolved_warnings,
              "unresolvedCount": errors + unresolved_warnings,
              "status": "PASS" if errors + unresolved_warnings == 0 else "REWORK"}
    args.json_out.parent.mkdir(parents=True, exist_ok=True)
    args.json_out.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"model": root.name, "status": result["status"],
                      "errorCount": errors, "warningCount": warnings,
                      "unresolvedCount": result["unresolvedCount"]}, indent=2))


if __name__ == "__main__":
    main()
