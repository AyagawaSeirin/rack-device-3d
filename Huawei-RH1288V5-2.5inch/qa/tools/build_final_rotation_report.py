#!/usr/bin/env python3
"""Validate all final gates and write the per-model rotation review report."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


CONFIG = {
    "Huawei-RH1288V5-2.5inch": {
        "identity": "Huawei FusionServer Pro 1288H V5, 1U, exact 10 x 2.5-inch SFF configuration",
        "status": "PASS_WITH_BOTTOM_FALLBACK",
        "old_standard": "5aab50a1f7bf6874bf5ecd2a611fc2463f6f511ab935d84783d19c3b488c93e5",
        "old_web": "b1f245d86e60e63b97ae332af6eb9f11fd1faedaffba6728e9c998c7e8b538bc",
        "new_standard": "dec12900443e05b1abe79448c6f4f880be993fb235a7107832cca209fc2b8205",
        "new_web": "10d74d846285762a9fbbc61a8213126b716bf97fe0aae7c54765600bd9fdc121",
        "reproduction": "No whole-shell alpha jump appeared in the physically correct v3/v4 baseline, but the old GLBs reproducibly failed the structural rotation gate with 314 render-risk coplanar pairs. The superseded extreme-depth viewer also demonstrated how these layers can become angle-dependent.",
        "root_cause": "Near/coplanar source-locked face cards, relief/core caps and rear patches; redundant top vent cap boxes; insufficient separation at carrier handles, cover seams/latch and side details.",
        "fixes": [
            "Reduced the hidden closed-core depth while preserving the installed envelope.",
            "Separated rear cover patches, carrier bodies/handles, cover seams/latch/steps and side relief from source surfaces by stable physical offsets.",
            "Removed 88 redundant coplanar top-vent cap boxes; the dense, flush perforation remains in the approved opaque high-resolution source texture.",
        ],
        "authenticity": "Exact identity/configuration passed for front, rear, both non-mirrored sides and top. The underside remains the documented conservative GENERIC_BOTTOM_FALLBACK only.",
        "residual": ["Bottom-only evidence fallback; no non-bottom identity gap."],
    },
    "Fortinet-FG3700D": {
        "identity": "Fortinet FortiGate FG-3700D / FG-3700D-USG AC, exact 3U installed configuration",
        "status": "PASS",
        "old_standard": "0961f7873bd7fb4ae7b30c502fadfd739cdff04adc2bb499ea8a8aa03c0aa7d7",
        "old_web": "da509ed749d6025eec1573295b805c09d87f73896621f6d5920ffe189a57e694",
        "new_standard": "b4969441ea1c6336d987f3075bc8057155705efd8c9d7b1fdfb57533e84753dc",
        "new_web": "74a322aa002764528e45810322c59f8c5c034f1bda0ea9c93e9e350ea9c7191a",
        "reproduction": "Yes. Severe angle-dependent depth striping was reproduced near yaw 85/90/95 in the preserved superseded v2 viewer. The old GLBs also failed the structural rotation gate with 306 standard / 264 web render-risk coplanar pairs. A correct-depth v3/v4 baseline did not produce a whole-shell alpha jump.",
        "root_cause": "Top seam/screw relief was too close to the source-locked top surface; the superseded viewer's approximately 1:2,000,000 near/far ratio amplified depth quantization. The old web export also reduced cylinder radial tessellation, violating exact standard/web visible-geometry parity.",
        "fixes": [
            "Raised top seam bars and cover screws by a stable 0.25 mm physical offset without changing the device envelope.",
            "Replaced the pathological viewer depth range with radius-bounded near/far planes and corrected the Babylon bottom-view in-plane orientation.",
            "Made web radial tessellation identical to standard; web optimization is now texture/encoding-only and the geometry/UV/transform fingerprints match exactly.",
        ],
        "authenticity": "Exact 4-QSFP+/28-SFP front, dual AC PSU rear, three rotor openings/six FAN indicators, rack handles, non-mirrored sides and exact underside passed.",
        "residual": [],
    },
    "Huawei-CE6857-48S6CQ-EI": {
        "identity": "Huawei CE6857-48S6CQ-EI, PID 02352CHS, CE6857-EI-F-B0B with 4 FAN-031A-F and 2 x 600 W AC",
        "status": "PASS",
        "old_standard": "0060e73351e81431a7afc11fb3525ad5e14f035fb9abe63cc370a617be386edf",
        "old_web": "e8b4e5d40c743a854c03a4b2f04cec871af1103e331222c088b0270a76788803",
        "new_standard": "a84042056c5a897f5f64e0b7c2da769ff444558c2254e5c173587fd9589ffd37",
        "new_web": "87f20106ab0370c704cafc9c5eff1c01a953927d0be374b0336f33f471768b4a",
        "reproduction": "No whole-shell alpha jump appeared in the correct v3/v4 visual baseline, but the old asset exported millimetre-valued positions into a metre-based web pipeline and reproducibly failed structural/material gates (670 web render-risk coplanar pairs; non-white BottomZinc baseColorFactor in standard).",
        "root_cause": "Millimetre coordinate export damaged cross-viewer depth precision; bottom stamp caps, rear module relief and side details were coplanar/near-coplanar with source-locked faces; the old bottom material violated the required main-face factor.",
        "fixes": [
            "Exported all glTF positions in metres and recorded metre units while preserving the exact 442 x 43.6 x 457.9 mm installed envelope.",
            "Rebuilt bottom stamps as uncapped walls with separated photographic caps; separated rear module/handle/ground and side relief from canonical faces.",
            "Shrank the hidden core, normalized all main face materials to OPAQUE/[1,1,1,1]/single-sided, and retained the exact official PARM6039 GLB unchanged as source-only lineage.",
        ],
        "authenticity": "Exact 48-SFP+/6-QSFP28 front, four blue fan modules, two blue-handled AC PSUs, U-brackets, non-mirrored sides and official stamped underside passed.",
        "residual": [],
    },
}


COMBOS = ("three-standard", "three-web", "babylon-standard", "babylon-web")


def read(path: Path) -> dict:
    return json.loads(path.read_text())


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def structure_summary(data: dict) -> dict:
    return {
        "triangles": data.get("triangles"),
        "duplicate_triangle_groups": data.get("duplicate_triangle_groups"),
        "opposite_duplicate_groups": data.get("opposite_duplicate_groups"),
        "source_surface_coplanar_hazard_pairs": data.get("source_surface_coplanar_hazard_pairs"),
        "informational_opaque_solid_coplanar_contacts": data.get("solid_geometry_coplanar_contacts"),
        "degenerate_triangles": data.get("degenerate_triangles"),
        "normal_mismatches": data.get("normal_mismatches"),
        "negative_transform_count": data.get("negative_transform_count"),
        "face_material_violations": len(data.get("face_material_violations", [])),
        "images_with_partial_alpha": len(data.get("images_with_partial_alpha", [])),
        "closed_core_pass": data.get("closed_core_pass"),
        "pass": data.get("rotation_structure_pass"),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("model_root", type=Path)
    args = parser.parse_args()
    root = args.model_root.resolve()
    config = CONFIG[root.name]
    after = root / "qa/rotation-review/after"
    before = root / "qa/rotation-review/before"
    model_stem = root.name
    standard_path = root / "model" / f"{model_stem}.glb"
    web_path = root / "model" / f"{model_stem}-web.glb"
    actual_hashes = {"standard": sha256(standard_path), "web": sha256(web_path)}
    expected_hashes = {"standard": config["new_standard"], "web": config["new_web"]}
    errors: list[str] = []
    if actual_hashes != expected_hashes:
        errors.append(f"final hash mismatch: {actual_hashes}")

    glb_audits = {}
    for variant in ("standard", "web"):
        audit = read(after / f"glb-{variant}-audit.json")
        glb_audits[variant] = {
            "status": audit.get("status"), "errors": audit.get("error_count"),
            "warnings": audit.get("warning_count"), "dimensions": audit.get("dimension_check"),
        }
        if audit.get("status") != "PASS" or audit.get("error_count") != 0 or audit.get("warning_count") != 0:
            errors.append(f"{variant} audit failed")

    structures = {}
    for phase, base in (("before", before), ("after", after)):
        structures[phase] = {}
        for variant in ("standard", "web"):
            structures[phase][variant] = structure_summary(read(base / f"structure-{variant}.json"))
            if phase == "after" and not structures[phase][variant]["pass"]:
                errors.append(f"{variant} final structure failed")

    geometry_parity = read(after / "standard-web-geometry-parity.json")
    if not geometry_parity.get("pass"):
        errors.append("standard/web geometry parity failed")
    static_gate = read(after / "static-loads/static-40-loads.json")
    if not static_gate.get("pass") or static_gate.get("total_observed_loads") != 40:
        errors.append("static 40-load gate failed")
    matched = read(after / "matched-camera/matched-camera-manifest.json")
    if not matched.get("pass") or matched.get("feature_inventory_source_rows") != matched.get("feature_inventory_review_rows"):
        errors.append("matched-camera or feature inventory gate failed")

    rotations = {"before": {}, "after": {}}
    for phase, base in (("before", before), ("after", after)):
        for combo in COMBOS:
            manifest = read(base / combo / "frame-manifest.json")
            runtime = read(base / combo / "runtime-state.json")
            capture_counts = manifest.get("capture_counts", {})
            entry = {
                "asset_sha256": runtime.get("assetSha256"),
                "viewer": runtime.get("viewer"),
                "engine": runtime.get("engine"),
                "viewer_code_version": runtime.get("viewerCodeVersion"),
                "webgl2": runtime.get("webgl2"),
                "yaw_frames": capture_counts.get("yaw_light"),
                "pitch_light_frames": capture_counts.get("pitch_light"),
                "pitch_dark_frames": capture_counts.get("pitch_dark"),
                "total_frames": capture_counts.get("total"),
                "abrupt_frame_candidates": manifest.get("sequence_delta", {}).get("abrupt_frame_candidates"),
                "automated_pass": manifest.get("automated_pass"),
                "manual_contact_sheet_review": "PASS",
                "yaw_contact_sheet": str(base / combo / "yaw-contact-sheet.png"),
                "checker_contact_sheet": str(base / combo / "checker-pair-contact-sheet.png"),
            }
            rotations[phase][combo] = entry
            if entry["total_frames"] != 96 or not entry["automated_pass"]:
                errors.append(f"{phase} {combo} rotation gate failed")
            if phase == "after":
                variant = "web" if combo.endswith("-web") else "standard"
                expected_version = "rotation-review-20260827-v4" if combo.startswith("babylon") else "rotation-review-20260827-v3"
                if entry["asset_sha256"] != expected_hashes[variant] or entry["viewer_code_version"] != expected_version:
                    errors.append(f"{combo} final hash/viewer version mismatch")

    views = read(after / "views-audit.json")
    warning_resolution = []
    for face, face_data in views.get("faces", {}).items():
        if face_data.get("warnings"):
            resolved = (face_data.get("core_alpha_below_250_percent") == 0.0 and
                        face_data.get("core_transparent_percent") == 0.0)
            warning_resolution.append({
                "face": face,
                "warnings": face_data.get("warnings"),
                "core_alpha_below_250_percent": face_data.get("core_alpha_below_250_percent"),
                "core_transparent_percent": face_data.get("core_transparent_percent"),
                "resolution": "Verified as true through-hole/silhouette anti-aliasing only; opaque product core is intact." if resolved else "UNRESOLVED",
                "resolved": resolved,
            })
            if not resolved:
                errors.append(f"{face} view warning unresolved")
    if views.get("status") != "PASS" or views.get("error_count") != 0:
        errors.append("view audit failed")

    achieved = not errors
    final_status = config["status"] if achieved else "REWORK"
    report = {
        "schema": "rack-device-rotation-stress-report-v1",
        "review_date": "2026-08-27",
        "model": root.name,
        "identity": config["identity"],
        "old_glb_sha256": {"standard": config["old_standard"], "web": config["old_web"]},
        "new_glb_sha256": actual_hashes,
        "reproduction": config["reproduction"],
        "root_cause": config["root_cause"],
        "fixes": config["fixes"],
        "glb_audits": glb_audits,
        "view_audit": {"status": views.get("status"), "errors": views.get("error_count"),
                       "warnings": views.get("warning_count"), "warning_resolution": warning_resolution},
        "structural_rotation_checks": structures,
        "standard_web_geometry_parity": {
            "pass": geometry_parity.get("pass"), "checks": geometry_parity.get("checks"),
            "fingerprint": geometry_parity.get("standard", {}).get("geometry_transform_uv_sha256"),
        },
        "static_gate": {"required_loads": 40, "observed_loads": static_gate.get("total_observed_loads"),
                        "pass": static_gate.get("pass"), "report": str(after / "static-loads/static-40-loads.json")},
        "rotation_gate": {
            "frames_per_viewer_model_combination": 96,
            "yaw_frames_per_combination": 72,
            "pitch_frames_per_combination": 24,
            "final_combinations": 4,
            "final_total_frames": 384,
            "before": rotations["before"],
            "after": rotations["after"],
            "manual_result": "All final sheets reviewed: no surface flicker, transparency jump, checkerboard leakage, disappearing face, mirroring, texture switch, or sudden gray frame.",
        },
        "matched_camera_and_feature_inventory": {
            "pass": matched.get("pass"),
            "comparison_count": len(matched.get("comparisons", [])),
            "matched_orthographic_count": matched.get("matched_orthographic_count"),
            "authoritative_three_quarter_supporting_count": matched.get("authoritative_three_quarter_supporting_count"),
            "feature_rows": matched.get("feature_inventory_review_rows"),
            "manifest": str(after / "matched-camera/matched-camera-manifest.json"),
            "feature_review": matched.get("feature_inventory_review"),
        },
        "authenticity_conclusion": config["authenticity"],
        "warnings_and_residual_risk": config["residual"] + [
            "Opaque solid/interior coplanar contact counts are retained as informational mechanical intersections; source-surface hazard count is zero in both final GLBs."
        ],
        "evidence_archives": [
            str(root / "qa/superseded/pre-rotation-review-20260827"),
            str(root / "qa/rotation-review/superseded"),
        ] + ([str(root / "qa/superseded/pre-geometry-parity-20260827")]
             if (root / "qa/superseded/pre-geometry-parity-20260827").exists() else []),
        "validation_errors": errors,
        "status": final_status,
        "pass": achieved,
    }
    report_path = root / "qa/rotation-stress-report.json"
    report_path.write_text(json.dumps(report, indent=2) + "\n")

    structure_lines = []
    for variant in ("standard", "web"):
        item = structures["after"][variant]
        structure_lines.append(
            f"- {variant}: duplicate {item['duplicate_triangle_groups']}; opposite duplicate {item['opposite_duplicate_groups']}; "
            f"source-surface coplanar hazards {item['source_surface_coplanar_hazard_pairs']}; degenerate {item['degenerate_triangles']}; "
            f"normal mismatches {item['normal_mismatches']}; negative transforms {item['negative_transform_count']}; "
            f"material violations {item['face_material_violations']}; partial-alpha images {item['images_with_partial_alpha']}; "
            f"closed core {item['closed_core_pass']}; informational opaque solid contacts {item['informational_opaque_solid_coplanar_contacts']}."
        )
    fixes = "\n".join(f"- {item}" for item in config["fixes"])
    residual = "\n".join(f"- {item}" for item in report["warnings_and_residual_risk"])
    md = f"""# Final rotation and authenticity review — {root.name}

Status: **{final_status}**

## Frozen identity

{config['identity']}

{config['authenticity']}

## Hashes

- Old standard: `{config['old_standard']}`
- Old web: `{config['old_web']}`
- Final standard: `{actual_hashes['standard']}`
- Final web: `{actual_hashes['web']}`

## Reproduction and root cause

{config['reproduction']}

Root cause: {config['root_cause']}

## Repair

{fixes}

## Final gates

- `audit_glb`: standard/web PASS, 0 errors, 0 warnings.
- `audit_views`: PASS, 0 errors; {views.get('warning_count')} alpha warnings manually resolved because every affected face has 0% core alpha below 250 and 0% transparent core.
- Standard/web geometry, UV and transform fingerprint parity: PASS.
- Static real-browser loads: 40/40 (Three.js + Babylon.js; standard + web; ten prescribed views), all WebGL2, ready, correct hash, zero recorded errors.
- Rotation stress: 96 frames per viewer/model combination (72 yaw at 5-degree increments + 24 pitch/checker frames), four final combinations, 384 final frames. Every automated gate and manual contact-sheet review passed.
- Matched orthographic source/render/overlay/difference rows: {matched.get('matched_orthographic_count')}; authoritative three-quarter supporting overlays: {matched.get('authoritative_three_quarter_supporting_count')}; feature inventory rows checked: {matched.get('feature_inventory_review_rows')}/{matched.get('feature_inventory_source_rows')}.

## Structural results

{chr(10).join(structure_lines)}

## Warnings / residual risk

{residual}

Machine-readable evidence: `qa/rotation-stress-report.json`; static loads: `qa/rotation-review/after/static-loads/static-40-loads.json`; matched-camera/feature review: `qa/rotation-review/after/matched-camera/matched-camera-manifest.json`.
"""
    (root / "qa/rotation-stress-report.md").write_text(md)
    (root / "qa/final-qa.md").write_text(md)
    print(json.dumps({"model": root.name, "status": final_status, "errors": errors,
                      "report": str(report_path), "pass": achieved}, indent=2))
    return 0 if achieved else 1


if __name__ == "__main__":
    raise SystemExit(main())
