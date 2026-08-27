#!/usr/bin/env python3
"""Consolidate the final exact-appearance gates into one checksum-backed audit."""

from __future__ import annotations

import csv
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
QA = ROOT / "qa"


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check(condition: bool, name: str, details: object, checks: list[dict]) -> None:
    checks.append({"gate": name, "status": "PASS" if condition else "FAIL", "details": details})


def main() -> None:
    checks: list[dict] = []
    models = {
        "standard": ROOT / "model" / "Dell-R7515-3.5inch.glb",
        "web": ROOT / "model" / "Dell-R7515-3.5inch-web.glb",
    }
    model_info = {
        key: {"path": path.relative_to(ROOT).as_posix(), "bytes": path.stat().st_size, "sha256": sha256(path)}
        for key, path in models.items()
    }

    build = read_json(QA / "build-manifest.json")
    build_match = all(
        build["outputs"][key]["bytes"] == info["bytes"]
        and build["outputs"][key]["sha256"] == info["sha256"]
        and build["outputs"][key]["bounds_mm"] == [[-241.0, -43.4, -358.22], [241.0, 43.4, 345.535]]
        for key, info in model_info.items()
    )
    check(build_match, "model_build_manifest_and_exact_bounds", {"models": model_info, "dimensions_mm": [482.0, 86.8, 703.755]}, checks)

    glb_audits = {key: read_json(QA / f"glb-audit-{key}.json") for key in models}
    glb_ok = all(
        audit["status"] == "PASS"
        and audit["error_count"] == 0
        and audit["warning_count"] == 0
        and audit["counts"]["unique_basecolor_images"] >= 6
        and not audit["external_buffers"]
        and not audit["geometry"]["mirrored_nodes"]
        for audit in glb_audits.values()
    )
    check(
        glb_ok,
        "standard_and_web_glb_structural_audit",
        {
            key: {
                "status": audit["status"],
                "errors": audit["error_count"],
                "warnings": audit["warning_count"],
                "counts": audit["counts"],
                "dimensions_xyz_m": audit["geometry"]["dimensions_xyz"],
                "mirrored_nodes": audit["geometry"]["mirrored_nodes"],
                "external_buffers": audit["external_buffers"],
            }
            for key, audit in glb_audits.items()
        },
        checks,
    )

    view_audit = read_json(QA / "views-audit.json")
    unresolved = [
        face for face, item in view_audit["faces"].items()
        if item["warnings"] and face not in view_audit.get("warning_resolutions", {})
    ]
    views_ok = view_audit["status"] == "PASS" and view_audit["error_count"] == 0 and not unresolved
    check(
        views_ok,
        "six_production_views",
        {
            "status": view_audit["status"],
            "errors": view_audit["error_count"],
            "warnings": view_audit["warning_count"],
            "resolved_warnings": view_audit.get("warning_resolutions", {}),
            "face_ratios": {face: item["ratio_error_percent"] for face, item in view_audit["faces"].items()},
        },
        checks,
    )

    with (ROOT / "source" / "face-source-lock.csv").open(newline="", encoding="utf-8") as handle:
        face_rows = list(csv.DictReader(handle))
    with (QA / "imagegen-generation-manifest.csv").open(newline="", encoding="utf-8") as handle:
        generation_rows = list(csv.DictReader(handle))
    faces = {row["face"] for row in face_rows}
    generation_faces = {row["face"] for row in generation_rows}
    generated_hashes_match = all(
        sha256(ROOT / row["raw_path"]) == row["raw_sha256"]
        and sha256(ROOT / row["keyed_path"]) == row["keyed_sha256"]
        and sha256(ROOT / row["final_path"]) == row["final_sha256"]
        and row["call_isolation"] == "independent_call"
        for row in generation_rows
    )
    face_modes = {row["face"]: row["production_mode"] for row in face_rows}
    independent_sides = next(row for row in generation_rows if row["face"] == "left")["final_sha256"] != next(
        row for row in generation_rows if row["face"] == "right"
    )["final_sha256"]
    face_lock_ok = (
        faces == generation_faces == {"front", "rear", "left", "right", "top", "bottom"}
        and generated_hashes_match
        and independent_sides
        and face_modes["bottom"] == "GENERIC_BOTTOM_FALLBACK"
    )
    check(
        face_lock_ok,
        "six_independent_source_locked_imagegen_faces",
        {
            "face_modes": face_modes,
            "independent_calls": len(generation_rows),
            "left_right_final_hashes_differ": independent_sides,
            "all_raw_keyed_final_hashes_match": generated_hashes_match,
        },
        checks,
    )

    evidence = read_json(QA / "viewer-load-evidence.json")
    required_views = {"front", "rear", "left", "right", "top", "bottom", "front-left", "front-right", "rear-left", "rear-right", "front-logo", "rear-psu"}
    required = {(viewer, model, view) for viewer in ("three", "babylon") for model in ("standard", "web") for view in required_views}
    actual = {(item["viewer"], item["model"], item["view"]) for item in evidence["loads"]}
    hashes_ok = all(item["serverModelSha256"] == model_info[item["model"]]["sha256"] for item in evidence["loads"])
    bytes_ok = all(item["serverModelBytes"] == model_info[item["model"]]["bytes"] for item in evidence["loads"])
    bounds_ok = all(
        all(abs(actual_value - expected_value) <= 0.0000001 for actual_value, expected_value in zip(item["bounds"]["size"], (0.482, 0.0868, 0.703755)))
        for item in evidence["loads"]
    )
    loads_ok = (
        evidence["count"] == len(evidence["loads"]) == 48
        and len({item["qaId"] for item in evidence["loads"]}) == 48
        and actual == required
        and all(item["status"] == "PASS" and item["webglVersion"] >= 1 for item in evidence["loads"])
        and hashes_ok and bytes_ok and bounds_ok
    )
    check(
        loads_ok,
        "two_independent_webgl_viewers_48_live_loads",
        {
            "count": evidence["count"],
            "matrix": "2 viewers x 2 GLBs x (6 orthographic + 4 oblique + 2 close-ups)",
            "viewers": sorted({item["viewer"] for item in evidence["loads"]}),
            "models": sorted({item["model"] for item in evidence["loads"]}),
            "unique_qa_ids": len({item["qaId"] for item in evidence["loads"]}),
            "server_hashes_match": hashes_ok,
            "server_bytes_match": bytes_ok,
            "viewer_bounds_match": bounds_ok,
            "first_server_received_at": evidence["loads"][0]["serverReceivedAt"],
            "last_server_received_at": evidence["loads"][-1]["serverReceivedAt"],
        },
        checks,
    )

    render_paths = sorted((QA / "renders").glob("*/*/*.png"))
    render_valid = len(render_paths) == 48 and all(path.stat().st_size > 0 and Image.open(path).size == (1280, 720) for path in render_paths)
    comparison_paths = sorted((QA / "comparisons").glob("*/*/*.png"))
    comparisons_valid = len(comparison_paths) == 24 and all(path.stat().st_size > 0 for path in comparison_paths)
    check(render_valid and comparisons_valid, "render_and_same_camera_comparison_artifacts", {"render_count": len(render_paths), "render_size_px": [1280, 720], "comparison_count": len(comparison_paths)}, checks)

    identity_text = (ROOT / "source" / "identity-manifest.md").read_text(encoding="utf-8")
    optional_text = (ROOT / "source" / "optional-3d" / "README.md").read_text(encoding="utf-8")
    bottom_text = (ROOT / "source" / "bottom-search-log.md").read_text(encoding="utf-8")
    identity_ok = all(token in identity_text for token in ("PowerEdge R7515", "12 x 3.5-inch", "two hot-plug EPP 750 W AC PSUs", "status: VERIFIED"))
    official_state = "NOT_FOUND_PUBLIC_EXACT"
    official_ok = "no exact public official 3D/CAD/AR binary" in optional_text and "R7525" in optional_text
    bottom_ok = "GENERIC_BOTTOM_FALLBACK" in bottom_text and "no usable exact-model underside" in bottom_text
    check(identity_ok, "exact_variant_identity_and_uniform_ac_lock", {"variant": "Dell PowerEdge R7515 12x3.5 LFF; no bezel; no rear drives; dual EPP 750W AC", "identity_status": "VERIFIED"}, checks)
    check(official_ok, "official_exact_3d_search_and_optional_backup", {"official_exact_public_3d": official_state, "optional_3d_record": "source/optional-3d/README.md", "substitute_model_used": False}, checks)
    check(bottom_ok, "bottom_search_exhaustion_and_controlled_fallback", {"bottom_mode": "GENERIC_BOTTOM_FALLBACK", "final_status_ceiling": "PASS_WITH_BOTTOM_FALLBACK"}, checks)

    failed = [item for item in checks if item["status"] != "PASS"]
    output = {
        "modelKey": "Dell-R7515-3.5inch",
        "generatedAt": datetime.now(timezone.utc).isoformat(),
        "status": "PASS_WITH_BOTTOM_FALLBACK" if not failed else "BLOCKED",
        "failed_gate_count": len(failed),
        "checks": checks,
        "models": model_info,
        "source_raster_count": sum(1 for path in (ROOT / "source").rglob("*") if path.is_file() and path.suffix.lower() in {".png", ".jpg", ".jpeg", ".webp"}),
        "remaining_risks": [
            "Exact R7515 underside imagery remains unavailable; bottom is a conservative non-identifying fallback.",
            "Surface textures are source-locked imagegen reconstructions rather than photogrammetry; minute fastener, finish and very small label details may differ although binding counts/layout/identity were checked.",
            "This is an exterior web replica, not Dell engineering CAD; internal geometry and manufacturing tolerances are intentionally out of scope.",
            "The official Dell product/3D routes were blocked by Akamai and no indexed exact public binary was found; absence cannot prove no non-public asset exists.",
        ],
    }
    (QA / "final-audit.json").write_text(json.dumps(output, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": output["status"], "failed_gate_count": len(failed), "gate_count": len(checks), "models": model_info}, indent=2))
    raise SystemExit(1 if failed else 0)


if __name__ == "__main__":
    main()
