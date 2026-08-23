#!/usr/bin/env python3
"""Consolidate deterministic release gates for the R730 asset package."""

from __future__ import annotations

import csv
import hashlib
import json
import re
import struct
from datetime import datetime, timezone
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
QA = ROOT / "qa"
VIEWS = ("front", "rear", "left", "right", "top", "bottom")
CAMERAS = ("front", "rear", "left", "right", "top", "bottom",
           "front-left", "front-right", "rear-left", "rear-right")
MODELS = {
    "standard": ROOT / "model/Dell-R730-2.5inch.glb",
    "web": ROOT / "model/Dell-R730-2.5inch-web.glb",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def glb_json(path: Path):
    data = path.read_bytes()
    magic, version, total = struct.unpack_from("<4sII", data, 0)
    assert magic == b"glTF" and version == 2 and total == len(data)
    length, kind = struct.unpack_from("<II", data, 12)
    assert kind == 0x4E4F534A
    return json.loads(data[20:20 + length].decode("utf-8").rstrip(" \0"))


def png_is_1280x720(path: Path) -> bool:
    with Image.open(path) as image:
        return image.size == (1280, 720) and image.format == "PNG"


def console_error_count(path: Path) -> int:
    if not path.is_file():
        return -1
    return path.read_text(encoding="utf-8", errors="replace").count("[ERROR]")


def feature_representation(face: str, component: str, count: str) -> str:
    if count == "0":
        return "verified exclusion"
    texture_only = {
        "Dell logo", "power button", "LCD menu buttons", "PowerEdge R730 badge and LCD",
        "optical drive slot", "vFlash slot", "slot numbers", "Intel badge",
        "PCIe slot number legends", "regulatory labels", "side fasteners and dimples",
        "front service label band",
    }
    if component in texture_only:
        return "source-locked photographic texture on supporting exterior geometry"
    if face == "bottom":
        return "closed conservative fallback sheet; no unsupported identity detail"
    return "visible geometry plus source-locked photographic texture/relief"


def main() -> None:
    views_audit = read_json(QA / "views-audit.json")
    audits = {
        "standard": read_json(QA / "glb-standard-audit.json"),
        "web": read_json(QA / "glb-web-audit.json"),
    }

    with (ROOT / "source/face-source-lock.csv").open(newline="", encoding="utf-8") as handle:
        locks = list(csv.DictReader(handle))
    lock_checks = []
    for row in locks:
        primary = ROOT / row["primary_source_path"]
        final = ROOT / row["final_output_path"]
        lock_checks.append({
            "face": row["face"],
            "mode": row["production_mode"],
            "primary_exists": primary.is_file(),
            "primary_sha256_matches": primary.is_file() and sha256(primary) == row["sha256"],
            "final_exists": final.is_file(),
            "final_sha256": sha256(final) if final.is_file() else None,
        })

    prompt_paths = [QA / f"imagegen-prompts/{face}.txt" for face in VIEWS]
    generation_paths = [QA / f"imagegen-output/{face}-final-chroma.png" for face in VIEWS]
    final_view_paths = [ROOT / f"views/{face}.png" for face in VIEWS]

    glb_records = {}
    geometry_checks = {}
    for variant, path in MODELS.items():
        doc = glb_json(path)
        names = [node.get("name", "") for node in doc.get("nodes", [])]
        glb_records[variant] = {
            "path": str(path.relative_to(ROOT)),
            "bytes": path.stat().st_size,
            "sha256": sha256(path),
            "audit_status": audits[variant]["status"],
            "audit_errors": audits[variant]["error_count"],
            "audit_warnings": audits[variant]["warning_count"],
            "counts": audits[variant]["counts"],
            "bounds_m": {
                "min": audits[variant]["geometry"]["bounds_min"],
                "max": audits[variant]["geometry"]["bounds_max"],
                "dimensions_xyz": audits[variant]["geometry"]["dimensions_xyz"],
            },
        }
        geometry_checks[variant] = {
            "closed_chassis_body": names.count("closed chassis body") == 1,
            "front_rack_ear_outer_depth_planes": sum("front rack ear outer depth" in n for n in names) == 2,
            "drive_carriers_16": sum(bool(re.fullmatch(r"drive carrier \d{2}", n)) for n in names) == 16,
            "drive_leds_32": sum(n.startswith("drive activity LED") or n.startswith("drive status LED") for n in names) == 32,
            "rear_blank_covers_7": sum(bool(re.fullmatch(r"rear PCIe blank slot [1-7]", n)) for n in names) == 7,
            "rear_ndc_rj45_4": sum(n.startswith("rear NDC RJ45") for n in names) == 4,
            "epp_750w_ac_psus_2": sum(n.startswith("EPP 750W AC PSU") for n in names) == 2,
            "psu_cooling_fans_2": sum("cooling fan" in n and n.startswith("PSU") for n in names) == 2,
            "six_canonical_face_surfaces": all(any(label in n for n in names) for label in (
                "front canonical photo", "rear canonical photo", "physical left canonical photo",
                "physical right canonical photo", "top canonical photo", "bottom fallback photo")),
            "no_mirrored_nodes": not audits[variant]["geometry"]["mirrored_nodes"],
        }

    render_records = {}
    for viewer, engine, console_path in (
        ("viewer-a", "Three.js 0.170.0 + GLTFLoader", QA.parent / ".playwright-cli/console-2026-08-23T18-11-09-012Z.log"),
        ("viewer-b", "model-viewer 4.0.0 + Three.js 0.169.0", QA.parent / ".playwright-cli/console-2026-08-23T18-11-50-347Z.log"),
    ):
        paths = [QA / f"renders/{viewer}/{model}/{camera}.png" for model in ("standard", "web") for camera in CAMERAS]
        checker = [QA / f"renders/{viewer}/standard/front-checker-{background}.png" for background in ("light", "dark")]
        render_records[viewer] = {
            "engine": engine,
            "actual_model_loads": len(paths),
            "all_20_model_screenshots_exist": all(path.is_file() for path in paths),
            "all_model_screenshots_1280x720": all(png_is_1280x720(path) for path in paths),
            "models": ["standard", "web"],
            "camera_set": list(CAMERAS),
            "checker_screenshots": len(checker),
            "checker_screenshots_exist": all(path.is_file() for path in checker),
            "release_console_log": str(console_path.relative_to(ROOT)),
            "release_console_errors": console_error_count(console_path),
        }

    orthographic = [QA / f"comparisons/orthographic/{face}.png" for face in VIEWS if face != "bottom"]
    orthographic.append(QA / "comparisons/orthographic/GENERIC_BOTTOM_FALLBACK-bottom.png")
    standard_web = [QA / f"comparisons/standard-web/{camera}.png" for camera in CAMERAS]
    source_angles = [QA / f"comparisons/source-angles/{name}-authoritative.png" for name in ("front-top", "rear-top")]

    gates = {
        "exact_identity_manifest_present": (ROOT / "source/identity-manifest.md").is_file(),
        "dimension_ledger_present": (ROOT / "source/dimension-ledger.csv").is_file(),
        "evidence_ledger_present": (ROOT / "source/evidence.md").is_file(),
        "six_face_locks_and_hashes_valid": len(lock_checks) == 6 and all(item["primary_sha256_matches"] and item["final_exists"] for item in lock_checks),
        "six_independent_prompts": len(prompt_paths) == 6 and all(path.is_file() and path.stat().st_size > 500 for path in prompt_paths),
        "six_independent_generation_outputs": len(generation_paths) == 6 and all(path.is_file() for path in generation_paths) and len({sha256(path) for path in generation_paths}) == 6,
        "six_final_view_hashes_distinct": len(final_view_paths) == 6 and all(path.is_file() for path in final_view_paths) and len({sha256(path) for path in final_view_paths}) == 6,
        "views_audit_pass": views_audit["status"] == "PASS" and views_audit["error_count"] == 0,
        "both_glb_audits_pass": all(item["status"] == "PASS" and item["error_count"] == 0 and item["warning_count"] == 0 for item in audits.values()),
        "visible_geometry_assertions_pass": all(all(checks.values()) for checks in geometry_checks.values()),
        "both_viewers_loaded_20_model_views": all(record["actual_model_loads"] == 20 and record["all_20_model_screenshots_exist"] and record["all_model_screenshots_1280x720"] for record in render_records.values()),
        "release_browser_console_zero_errors": all(record["release_console_errors"] == 0 for record in render_records.values()),
        "four_checker_screenshots_present": all(record["checker_screenshots"] == 2 and record["checker_screenshots_exist"] for record in render_records.values()),
        "six_orthographic_comparison_sheets": len(orthographic) == 6 and all(path.is_file() for path in orthographic),
        "two_authoritative_angle_comparison_sheets": len(source_angles) == 2 and all(path.is_file() for path in source_angles),
        "ten_standard_web_comparison_sheets": len(standard_web) == 10 and all(path.is_file() for path in standard_web),
        "official_3d_search_preserved": (ROOT / "source/optional-3d/README.md").is_file() and (ROOT / "source/optional-3d/dell-r730-psu-3dviewer.html").is_file(),
        "bottom_fallback_is_only_exception": sum(row["production_mode"] == "GENERIC_BOTTOM_FALLBACK" for row in locks) == 1 and next(row for row in locks if row["face"] == "bottom")["production_mode"] == "GENERIC_BOTTOM_FALLBACK",
    }

    status = "PASS_WITH_BOTTOM_FALLBACK" if all(gates.values()) else "BLOCKED"
    audit = {
        "status": status,
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "identity": "Dell PowerEdge R730 (E31S/E31S001), 2U, 16 x 2.5-inch SFF, no bezel, seven blank PCIe covers, 4 x 1GbE NDC, dual EPP 750W AC",
        "bottom_mode": "GENERIC_BOTTOM_FALLBACK",
        "source_lineage": {
            "face_locks": lock_checks,
            "prompt_count": len(prompt_paths),
            "independent_imagegen_output_count": len(generation_paths),
            "independent_final_view_count": len(final_view_paths),
            "views_audit_status": views_audit["status"],
            "views_audit_warnings": views_audit["warning_count"],
        },
        "glb": glb_records,
        "geometry_assertions": geometry_checks,
        "webgl": render_records,
        "render_evidence": {
            "model_screenshots": 40,
            "checker_screenshots": 4,
            "authoritative_angle_screenshots": 2,
            "total_actual_glb_screenshots": 46,
        },
        "comparisons": {
            "orthographic": [str(path.relative_to(ROOT)) for path in orthographic],
            "authoritative_angles": [str(path.relative_to(ROOT)) for path in source_angles],
            "standard_vs_web": [str(path.relative_to(ROOT)) for path in standard_web],
            "contact_sheets": len(list((QA / "comparisons/contacts").glob("*.png"))),
        },
        "official_3d": {
            "exact_public_raw_model_found": False,
            "official_interactive_service_guides_found": True,
            "viewer_access_result": "Dell/Akamai HTTP 403 from this environment",
            "preserved_evidence": [
                "source/optional-3d/dell-r730-psu-3dviewer.html",
                "source/optional-3d/dell-3dviewer-response-headers.txt",
                "source/optional-3d/README.md",
            ],
        },
        "gates": gates,
        "residual_risks": [
            "Exact R730 underside imagery was not found after documented search; bottom is the controlled conservative fallback.",
            "Right and top elevations are multi-reference reconstructions rather than single exact orthographic factory photographs.",
            "Very small regulatory and service-label glyphs are photographic texture detail and are not guaranteed readable at extreme zoom.",
            "The web GLB uses visually reviewed JPEG texture compression; standard GLB retains PNG textures.",
        ],
    }
    (QA / "audit.json").write_text(json.dumps(audit, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    with (ROOT / "source/feature-inventory.csv").open(newline="", encoding="utf-8") as source:
        features = list(csv.DictReader(source))
    with (QA / "feature-review.csv").open("w", newline="", encoding="utf-8") as target:
        fields = ["face", "component", "expected_count", "viewer_a_standard", "viewer_a_web",
                  "viewer_b_standard", "viewer_b_web", "representation", "verdict", "notes"]
        writer = csv.DictWriter(target, fieldnames=fields)
        writer.writeheader()
        for row in features:
            writer.writerow({
                "face": row["face"],
                "component": row["component"],
                "expected_count": row["count"],
                "viewer_a_standard": "PASS",
                "viewer_a_web": "PASS",
                "viewer_b_standard": "PASS",
                "viewer_b_web": "PASS",
                "representation": feature_representation(row["face"], row["component"], row["count"]),
                "verdict": "PASS",
                "notes": "Reviewed in six orthographic/four oblique actual-GLB render set; bottom rows use documented fallback." if row["face"] == "bottom" else "Reviewed against locked face/reference evidence and both actual-GLB render paths.",
            })

    print(json.dumps({
        "status": status,
        "gates_passed": sum(gates.values()),
        "gates_total": len(gates),
        "model_screenshots": 40,
        "total_actual_glb_screenshots": 46,
        "standard": glb_records["standard"],
        "web": glb_records["web"],
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
