#!/usr/bin/env python3
"""Build a machine-readable final gate summary from the saved evidence."""

from __future__ import annotations

import csv
import hashlib
import json
from datetime import datetime
from pathlib import Path

from PIL import Image


VIEWS = ("front", "rear", "left", "right", "top", "bottom", "front-left", "front-right", "rear-left", "rear-right")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    target = Path(__file__).resolve().parents[1]
    identity = (target / "source" / "identity-manifest.md").read_text(encoding="utf-8")
    identity_verified = "status: VERIFIED" in identity

    lock_rows = list(csv.DictReader((target / "source" / "face-source-lock.csv").open(encoding="utf-8")))
    source_locks = []
    for row in lock_rows:
        primary = target / row["primary_source_path"]
        output = target / row["final_output_path"]
        source_locks.append(
            {
                "face": row["face"],
                "mode": row["production_mode"],
                "primary": row["primary_source_path"],
                "declared_sha256": row["sha256"],
                "actual_sha256": sha256(primary),
                "sha256_match": sha256(primary) == row["sha256"],
                "output": row["final_output_path"],
                "output_exists": output.is_file(),
            }
        )

    models = {}
    for tier, filename in (("standard", "HPE-DL360G10-2.5inch.glb"), ("web", "HPE-DL360G10-2.5inch-web.glb")):
        path = target / "model" / filename
        audit = json.loads((target / "qa" / "final" / f"glb-{tier}-audit.json").read_text(encoding="utf-8"))
        manifest = json.loads((target / "qa" / "manifests" / ("HPE-DL360G10-2.5inch-parts.json" if tier == "standard" else "HPE-DL360G10-2.5inch-web-parts.json")).read_text(encoding="utf-8"))
        models[tier] = {
            "path": str(path.relative_to(target)),
            "bytes": path.stat().st_size,
            "sha256": sha256(path),
            "audit_status": audit["status"],
            "audit_errors": audit["error_count"],
            "audit_warnings": audit["warning_count"],
            "dimensions_xyz_mm": audit["geometry"]["dimensions_xyz"],
            "nodes": audit["counts"]["nodes"],
            "manifest_nodes": manifest["nodes"],
            "manifest_visible_parts": len(manifest["visibleParts"]),
        }

    render_groups = []
    for viewer in ("viewer-a", "viewer-b"):
        for tier in ("standard", "web"):
            model_path = target / models[tier]["path"]
            render_dir = target / "qa" / "final" / "webgl-renders" / viewer / tier
            files = []
            for view in VIEWS:
                path = render_dir / f"{view}.png"
                with Image.open(path) as image:
                    dimensions = list(image.size)
                files.append(
                    {
                        "view": view,
                        "path": str(path.relative_to(target)),
                        "size_px": dimensions,
                        "newer_than_loaded_glb": path.stat().st_mtime > model_path.stat().st_mtime,
                    }
                )
            render_groups.append(
                {
                    "viewer": viewer,
                    "tier": tier,
                    "load_count": len(files),
                    "all_1200x800": all(item["size_px"] == [1200, 800] for item in files),
                    "all_current": all(item["newer_than_loaded_glb"] for item in files),
                    "files": files,
                }
            )

    views_audit = json.loads((target / "qa" / "final" / "views-audit.json").read_text(encoding="utf-8"))
    comparison = json.loads((target / "qa" / "comparisons" / "comparison-summary.json").read_text(encoding="utf-8"))
    alpha_evidence = sorted((target / "qa" / "final" / "alpha-inspection").glob("viewer-*-front-checker-*.png"))
    closeups = sorted((target / "qa" / "final" / "closeups").glob("*.png"))
    optional_files = sorted(path.name for path in (target / "source" / "optional-3d").iterdir() if path.is_file())

    gates = {
        "identity_verified": identity_verified,
        "six_source_locks_valid": len(source_locks) == 6 and all(item["sha256_match"] and item["output_exists"] for item in source_locks),
        "bottom_search_log_and_fallback_declared": (target / "source" / "underside-search-log.md").is_file() and any(item["face"] == "bottom" and item["mode"] == "GENERIC_BOTTOM_FALLBACK" for item in source_locks),
        "formal_glbs_audit_pass": all(item["audit_status"] == "PASS" and item["audit_errors"] == 0 for item in models.values()),
        "parts_manifests_current": all(item["nodes"] == item["manifest_nodes"] == item["manifest_visible_parts"] for item in models.values()),
        "views_audit_pass": views_audit["status"] == "PASS" and views_audit["error_count"] == 0,
        "six_comparisons_pass": comparison["status"] == "PASS" and comparison["comparison_count"] == 6,
        "dual_viewer_40_loads_current": sum(group["load_count"] for group in render_groups) == 40 and all(group["all_1200x800"] and group["all_current"] for group in render_groups),
        "light_dark_checker_evidence": len(alpha_evidence) == 4,
        "rack_ear_logo_text_closeups": len(closeups) >= 3,
        "official_exact_3d_not_found_documented": optional_files == ["README.md"] and "No exact public official HPE 3D/CAD/AR file was found" in (target / "source" / "optional-3d" / "README.md").read_text(encoding="utf-8"),
    }
    status = "PASS_WITH_BOTTOM_FALLBACK" if all(gates.values()) else "BLOCKED"
    summary = {
        "status": status,
        "generated_at": datetime.now().astimezone().isoformat(),
        "subject": "HPE ProLiant DL360 Gen10 8SFF 2.5-inch, standard 6+2 carrier arrangement, dual 500W AC PSU",
        "gates": gates,
        "models": models,
        "source_locks": source_locks,
        "webgl": {
            "viewer_a": "native WebGL2 GLB parser/renderer",
            "viewer_b": "Three.js r128 GLTFLoader",
            "required_views_per_load": list(VIEWS),
            "total_actual_loads": sum(group["load_count"] for group in render_groups),
            "groups": render_groups,
        },
        "comparisons": {"status": comparison["status"], "count": comparison["comparison_count"]},
        "alpha_inspection_count": len(alpha_evidence),
        "closeup_count": len(closeups),
        "official_exact_3d": {"found": False, "stored_files": optional_files, "note": "Only the search record is stored; no exact public official 3D/CAD/AR file was found."},
        "remaining_risk": "Exact underside evidence is unavailable after documented exhaustive search; the conservative opaque bottom is GENERIC_BOTTOM_FALLBACK.",
    }
    output = target / "qa" / "final" / "final-gate-summary.json"
    output.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": status, "gates": gates, "total_actual_loads": summary["webgl"]["total_actual_loads"]}, ensure_ascii=False, indent=2))
    return 0 if status != "BLOCKED" else 1


if __name__ == "__main__":
    raise SystemExit(main())
