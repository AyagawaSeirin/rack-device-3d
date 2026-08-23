#!/usr/bin/env python3
"""Write the final asset manifest and consolidated acceptance record."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def record(category: str, relative_path: str) -> dict:
    path = ROOT / relative_path
    return {
        "category": category,
        "path": relative_path,
        "bytes": path.stat().st_size,
        "sha256": sha256(path),
    }


def load(relative_path: str) -> dict:
    return json.loads((ROOT / relative_path).read_text(encoding="utf-8"))


def main() -> None:
    views = load("qa/audits/views.json")
    glb_standard = load("qa/audits/glb-standard.json")
    glb_web = load("qa/audits/glb-web.json")
    structure = load("qa/audits/structure.json")
    browser = load("qa/audits/browser.json")
    texture_lineage = load("qa/audits/texture-lineage.json")
    component_statuses = {
        "views": views["status"],
        "glb_standard": glb_standard["status"],
        "glb_web": glb_web["status"],
        "configuration_structure": structure["status"],
        "webgl_browser_matrix": browser["status"],
        "embedded_texture_lineage": texture_lineage["status"],
    }
    final_status = (
        "PASS_WITH_BOTTOM_FALLBACK"
        if all(status == "PASS" for status in component_statuses.values())
        else "REWORK"
    )

    paths = []
    for face in ("front", "rear", "left", "right", "top", "bottom"):
        paths.append(("approved-view", f"views/{face}.png"))
    paths.extend(
        [
            ("model", "model/Huawei-RH2288V3-3.5inch.glb"),
            ("model", "model/Huawei-RH2288V3-3.5inch-web.glb"),
            ("builder", "model/build_model.py"),
            ("source-record", "source/identity-manifest.md"),
            ("source-record", "source/face-source-lock.csv"),
            ("source-record", "source/feature-inventory.csv"),
            ("source-record", "source/evidence.md"),
            ("source-record", "source/optional-3d/README.md"),
            ("audit", "qa/audits/views.json"),
            ("audit", "qa/audits/glb-standard.json"),
            ("audit", "qa/audits/glb-web.json"),
            ("audit", "qa/audits/structure.json"),
            ("audit", "qa/audits/browser.json"),
            ("audit", "qa/audits/texture-lineage.json"),
            ("viewer", "qa/viewers/three.html"),
            ("viewer", "qa/viewers/babylon.html"),
            ("comparison", "qa/comparisons/three-standard-ten-views.png"),
            ("comparison", "qa/comparisons/three-web-ten-views.png"),
            ("comparison", "qa/comparisons/babylon-standard-ten-views.png"),
            ("comparison", "qa/comparisons/babylon-web-ten-views.png"),
            ("comparison", "qa/comparisons/two-engines-two-variants-forty-views.png"),
            ("comparison", "qa/comparisons/front-source-vs-three-standard.png"),
            ("comparison", "qa/comparisons/rear-source-vs-three-standard.png"),
            ("comparison", "qa/comparisons/left-source-vs-three-standard.png"),
            ("comparison", "qa/comparisons/right-source-vs-three-standard.png"),
            ("comparison", "qa/comparisons/top-source-vs-three-standard.png"),
            ("comparison", "qa/comparisons/bottom-source-vs-three-standard.png"),
            ("report", "qa/COMPARISON-TABLE.md"),
            ("report", "qa/QA_REPORT.md"),
        ]
    )
    files = [record(category, path) for category, path in paths]

    consolidated = {
        "model_key": "Huawei-RH2288V3-3.5inch",
        "identity": "Huawei FusionServer RH2288 V3 / H22M-03 12x3.5-inch LFF",
        "status": final_status,
        "bottom": "GENERIC_BOTTOM_FALLBACK",
        "component_statuses": component_statuses,
        "body_dimensions_mm": [447.0, 86.1, 748.0],
        "front_mounting_span_mm": 482.6,
        "world_bounds_m": glb_standard["geometry"]["dimensions_xyz"],
        "maximum_view_ratio_error_percent": max(
            face.get("ratio_error_percent", 0.0) for face in views["faces"].values()
        ),
        "standard_web_maximum_normalized_rmse": browser[
            "maximum_standard_web_normalized_rmse"
        ],
        "webgl_render_count": browser["actual_render_count"],
        "model_files": [
            item for item in files if item["category"] == "model"
        ],
        "reports": ["qa/COMPARISON-TABLE.md", "qa/QA_REPORT.md"],
    }
    (ROOT / "qa" / "audit.json").write_text(
        json.dumps(consolidated, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    manifest = {
        "model_key": consolidated["model_key"],
        "identity": consolidated["identity"],
        "status": final_status,
        "file_count": len(files),
        "files": files,
    }
    (ROOT / "qa" / "asset-manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(final_status, len(files), "files")


if __name__ == "__main__":
    main()
