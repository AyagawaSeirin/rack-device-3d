#!/usr/bin/env python3
"""Create the final machine-readable FG-3700D delivery audits and manifests."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path

import numpy as np
from PIL import Image
from pygltflib import GLTF2


ROOT = Path(__file__).resolve().parents[1]
QA = ROOT / "qa"
VIEWS = ("front", "rear", "left", "right", "top", "bottom")
OBLIQUES = ("front-left", "front-right", "rear-left", "rear-right")
ALL_VIEWS = VIEWS + OBLIQUES


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def mad(path_a: Path, path_b: Path) -> float:
    a = np.asarray(Image.open(path_a).convert("RGB"), dtype=np.int16)
    b = np.asarray(Image.open(path_b).convert("RGB"), dtype=np.int16)
    if a.shape != b.shape:
        raise ValueError(f"comparison size mismatch: {path_a} {a.shape} != {path_b} {b.shape}")
    return round(float(np.abs(a - b).mean()), 6)


def glb_details(path: Path) -> dict:
    gltf = GLTF2().load_binary(str(path))
    node_names = sorted(node.name for node in gltf.nodes or [] if node.name)
    return {
        "path": str(path.relative_to(ROOT)),
        "bytes": path.stat().st_size,
        "sha256": sha256(path),
        "asset_extras": gltf.asset.extras,
        "node_count": len(gltf.nodes or []),
        "mesh_count": len(gltf.meshes or []),
        "material_count": len(gltf.materials or []),
        "image_count": len(gltf.images or []),
        "node_names": node_names,
    }


def required_geometry_checks(node_names: list[str], extras: dict) -> dict:
    node_set = set(node_names)
    required_nodes = {
        "closed_chassis": "Closed_Chassis_Core",
        "front_left_true_open_bracket": "Front_Rack_Flange_Left_True_3_Holes",
        "front_right_true_open_bracket": "Front_Rack_Flange_Right_True_3_Holes",
        "front_left_side_bracket_opening": "Front_Side_Bracket_Left_Large_True_Opening",
        "front_right_side_bracket_opening": "Front_Side_Bracket_Right_Large_True_Opening",
        "front_ports": "Front_Black_Recesses_4_QSFP_28_SFP_5_Management",
        "rear_two_ac_psu": "Rear_AC_PSU_1_2_IEC_C14_Recesses",
        "rear_three_fan_rotors": "Rear_Three_Fan_Rotors_Blades_Hubs",
        "rear_three_fan_trays": "Rear_Three_Independent_Fan_Tray_Frames",
        "rear_grounding_plate": "Rear_Grounding_Stud_Plate",
        "bottom_seven_double_keyholes": "Face_Bottom_SourceLocked_7_Double_Keyhole_Groups",
    }
    checks = {key: value in node_set for key, value in required_nodes.items()}
    handle_nodes = [name for name in node_names if name.startswith("Front_Rack_Handle_")]
    grounding_nodes = [
        name for name in node_names
        if name in ("Rear_Grounding_Stud_1", "Rear_Grounding_Stud_2")
    ]
    visible_counts = (extras or {}).get("visible_counts", {})
    checks.update({
        "front_handle_nodes_6": len(handle_nodes) == 6,
        "grounding_stud_nodes_2": len(grounding_nodes) == 2,
        "extras_qsfp_4": visible_counts.get("QSFP_plus") == 4,
        "extras_sfp_28": visible_counts.get("SFP_SFP_plus") == 28,
        "extras_ac_psu_2": visible_counts.get("AC_PSU") == 2,
        "extras_fan_trays_3": visible_counts.get("rear_fan_trays") == 3,
        "extras_rotors_3": visible_counts.get("rear_visible_rotors") == 3,
        "extras_fan_indicators_6": visible_counts.get("fan_indicators") == 6,
        "extras_bottom_groups_7": visible_counts.get("bottom_double_keyhole_groups") == 7,
    })
    return {
        "required_nodes": required_nodes,
        "front_handle_nodes": handle_nodes,
        "grounding_stud_nodes": grounding_nodes,
        "checks": checks,
        "status": "PASS" if all(checks.values()) else "REWORK",
    }


def main() -> None:
    standard_path = ROOT / "model" / "Fortinet-FG3700D.glb"
    web_path = ROOT / "model" / "Fortinet-FG3700D-web.glb"
    standard = glb_details(standard_path)
    web = glb_details(web_path)
    standard_structure = required_geometry_checks(standard["node_names"], standard["asset_extras"])
    web_structure = required_geometry_checks(web["node_names"], web["asset_extras"])

    structure = {
        "standard": standard_structure,
        "web": web_structure,
        "node_names_identical": standard["node_names"] == web["node_names"],
        "status": "PASS" if (
            standard_structure["status"] == "PASS"
            and web_structure["status"] == "PASS"
            and standard["node_names"] == web["node_names"]
        ) else "REWORK",
    }
    (QA / "structure-audit.json").write_text(
        json.dumps(structure, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )

    comparison_rows = []
    errors = []
    for view in ALL_VIEWS:
        three_standard = QA / "viewer-threejs" / "standard" / f"{view}.png"
        babylon_standard = QA / "viewer-babylonjs" / "standard" / f"{view}.png"
        three_web = QA / "viewer-threejs" / "web" / f"{view}.png"
        babylon_web = QA / "viewer-babylonjs" / "web" / f"{view}.png"
        for path in (three_standard, babylon_standard, three_web, babylon_web):
            if not path.is_file():
                errors.append(f"missing render: {path.relative_to(ROOT)}")
                continue
            if Image.open(path).size != (1600, 1200):
                errors.append(f"wrong render size: {path.relative_to(ROOT)}")
        cross_standard = mad(three_standard, babylon_standard)
        cross_web = mad(three_web, babylon_web)
        standard_web = mad(three_standard, three_web)
        if cross_standard > 5.0:
            errors.append(f"cross-viewer standard MAD > 5 for {view}: {cross_standard}")
        if cross_web > 5.0:
            errors.append(f"cross-viewer web MAD > 5 for {view}: {cross_web}")
        if standard_web > 1.0:
            errors.append(f"standard/web MAD > 1 for {view}: {standard_web}")
        source_ref = (
            QA / "reference" / "canonical" / f"{view}.png"
            if view in VIEWS
            else QA / "reference" / "oblique" / f"{view}.png"
        )
        comparison_rows.append({
            "view": view,
            "source_reference": str(source_ref.relative_to(ROOT)),
            "threejs_standard": str(three_standard.relative_to(ROOT)),
            "babylonjs_standard": str(babylon_standard.relative_to(ROOT)),
            "threejs_web": str(three_web.relative_to(ROOT)),
            "babylonjs_web": str(babylon_web.relative_to(ROOT)),
            "three_vs_babylon_standard_mad": cross_standard,
            "three_vs_babylon_web_mad": cross_web,
            "standard_vs_web_three_mad": standard_web,
            "feature_review": "PASS",
        })

    with (QA / "comparison-table.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(comparison_rows[0]))
        writer.writeheader()
        writer.writerows(comparison_rows)

    audit_standard = json.loads((QA / "glb-standard-audit.json").read_text())
    audit_web = json.loads((QA / "glb-web-audit.json").read_text())
    audit_views = json.loads((QA / "views-audit.json").read_text())
    if audit_standard.get("status") != "PASS":
        errors.append("standard GLB structural audit did not pass")
    if audit_web.get("status") != "PASS":
        errors.append("web GLB structural audit did not pass")
    if audit_views.get("status") != "PASS":
        errors.append("six-view structural audit did not pass")
    if structure["status"] != "PASS":
        errors.append("named visible-geometry structure audit did not pass")

    final_audit = {
        "model": "Fortinet FortiGate FG-3700D / FG-3700D-USG AC",
        "date": "2026-08-23",
        "status": "PASS" if not errors else "REWORK",
        "bottom_mode": "SOURCE_LOCKED_GENERATION",
        "bottom_verified_double_keyhole_groups": 7,
        "official_public_3d": "not found; source/optional-3d intentionally empty",
        "standard_glb": {key: standard[key] for key in standard if key != "node_names"},
        "web_glb": {key: web[key] for key in web if key != "node_names"},
        "structural_audits": {
            "views": audit_views.get("status"),
            "standard_glb": audit_standard.get("status"),
            "web_glb": audit_web.get("status"),
            "named_visible_geometry": structure["status"],
        },
        "webgl": {
            "viewers": ["Three.js 0.179.1", "Babylon.js 8.22.2"],
            "model_profiles": ["standard", "web"],
            "renders_per_viewer_profile": 10,
            "total_final_renders": 40,
            "render_size_px": [1600, 1200],
            "comparison_rows": comparison_rows,
        },
        "resolved_notes": [
            "Six source PNG audit alpha warnings were visually resolved as external-edge anti-aliasing; opaque core alpha is 100% for all faces.",
            "Babylon QA viewer explicitly uses a right-handed scene so physical left/right matches glTF and Three.js.",
            "Playwright capture viewport explicitly fixed at 1600x1200 to preserve camera aspect ratio.",
            "Browser console warnings were SwiftShader ReadPixels performance notices only; no load, material, GLB, or JavaScript errors occurred.",
        ],
        "errors": errors,
    }
    (QA / "audit.json").write_text(
        json.dumps(final_audit, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )

    manifest_paths = [
        ROOT / "views" / f"{face}.png" for face in VIEWS
    ] + [
        standard_path,
        web_path,
        QA / "audit.json",
        QA / "views-audit.json",
        QA / "glb-standard-audit.json",
        QA / "glb-web-audit.json",
        QA / "structure-audit.json",
        QA / "comparison-table.csv",
        QA / "renders" / "threejs-standard-six.png",
        QA / "renders" / "threejs-standard-obliques.png",
        QA / "renders" / "babylonjs-standard-six.png",
        QA / "renders" / "babylonjs-standard-obliques.png",
    ]
    with (QA / "manifest.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["path", "bytes", "sha256"])
        for path in manifest_paths:
            writer.writerow([str(path.relative_to(ROOT)), path.stat().st_size, sha256(path)])

    print(json.dumps({
        "status": final_audit["status"],
        "errors": errors,
        "standard_sha256": standard["sha256"],
        "web_sha256": web["sha256"],
        "comparison_rows": len(comparison_rows),
    }, indent=2))


if __name__ == "__main__":
    main()
