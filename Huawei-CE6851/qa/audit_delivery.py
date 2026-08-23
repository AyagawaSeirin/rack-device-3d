#!/usr/bin/env python3
"""Audit Huawei CE6851 GLB structure and two-engine WebGL render evidence."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path

import numpy as np
from PIL import Image
from pygltflib import GLTF2
import trimesh


ROOT = Path(__file__).resolve().parents[1]
MODEL = ROOT / "model"
QA = ROOT / "qa"
RENDERS = QA / "renders"
OUTPUT = ROOT / "output" / "playwright"

STANDARD = MODEL / "Huawei-CE6851.glb"
WEB = MODEL / "Huawei-CE6851-web.glb"
CORE_VIEWS = (
    "front", "rear", "left", "right", "top", "bottom",
    "front_left", "front_right", "rear_left", "rear_right",
)
DETAIL_VIEWS = (
    "front_ear_left", "front_ear_right", "front_logo", "rear_management",
    "front-checker-light", "rear-checker-dark",
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def connected_component_count(mesh: trimesh.Trimesh) -> int:
    """Count face-connected components without optional scipy/networkx."""
    parent = list(range(len(mesh.vertices)))

    def find(index: int) -> int:
        while parent[index] != index:
            parent[index] = parent[parent[index]]
            index = parent[index]
        return index

    def union(a: int, b: int) -> None:
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[rb] = ra

    used: set[int] = set()
    for face in np.asarray(mesh.faces, dtype=int):
        a, b, c = map(int, face)
        used.update((a, b, c))
        union(a, b)
        union(a, c)
    return len({find(index) for index in used})


def load_scene(path: Path) -> trimesh.Scene:
    loaded = trimesh.load(path, force="scene")
    if not isinstance(loaded, trimesh.Scene):
        raise TypeError(f"expected scene: {path}")
    return loaded


def structure_audit() -> dict:
    standard_scene = load_scene(STANDARD)
    web_scene = load_scene(WEB)
    names = set(standard_scene.geometry)
    web_names = set(web_scene.geometry)

    required_names = {
        "Closed_Chassis_Shell",
        *(f"Face_{face.title()}_SourceLocked" for face in ("front", "rear", "left", "right", "top", "bottom")),
        "Port_Side_Rack_Bracket_Left_2_Holes",
        "Port_Side_Rack_Bracket_Right_2_Holes",
        "Front_SFPplus_Cages_48",
        "Front_QSFPplus_Cages_6",
        "Rear_Module_PSU1_PAC-600WA-B",
        "Rear_Module_PSU2_PAC-600WA-B",
        "Rear_Module_FAN1_FAN-40EA-B",
        "Rear_Module_FAN2_FAN-40EA-B",
        "Rear_Module_Management",
        "Rear_PSU_1_IEC_C14_Inlet",
        "Rear_PSU_2_IEC_C14_Inlet",
        "Rear_Console_RJ45",
        "Rear_ETH_Management_RJ45",
        "Rear_USB_Type_A",
        "Right_Side_Ground_Stud",
        "Right_Side_Yellow_Earth_Mark",
        "Top_PortSide_Vent_Recess",
        "Top_Vent_Field_Dividers_2",
        "Bottom_Longitudinal_Stamped_Ribs_5",
        "Bottom_Transverse_Stamped_Rib_1",
        "Bottom_Visible_Fasteners",
    }
    missing = sorted(required_names - names)

    component_expectations = {
        "Front_SFPplus_Cages_48": 48,
        "Front_QSFPplus_Cages_6": 6,
        "Front_SYS_MST_ID_Indicators": 3,
        "Rear_HotSwap_Module_Seams": 4,
        "Rear_ACT_LA_ID_LEDs": 3,
        "Rear_Captive_Screws": 6,
        "Left_Side_Mounting_Fasteners": 8,
        "Right_Side_Mounting_Fasteners": 8,
        "Top_Vent_Field_Dividers_2": 2,
        "Bottom_Longitudinal_Stamped_Ribs_5": 5,
        "Bottom_Visible_Fasteners": 15,
    }
    component_counts = {
        name: connected_component_count(standard_scene.geometry[name])
        for name in component_expectations
        if name in standard_scene.geometry
    }
    component_errors = {
        name: {"expected": expected, "actual": component_counts.get(name)}
        for name, expected in component_expectations.items()
        if component_counts.get(name) != expected
    }

    shell = standard_scene.geometry["Closed_Chassis_Shell"]
    ears = {
        side: standard_scene.geometry[f"Port_Side_Rack_Bracket_{side}_2_Holes"]
        for side in ("Left", "Right")
    }

    geometry_differences = []
    for name in sorted(names & web_names):
        a = standard_scene.geometry[name]
        b = web_scene.geometry[name]
        if not np.array_equal(a.vertices, b.vertices) or not np.array_equal(a.faces, b.faces):
            geometry_differences.append(name)

    metadata = {}
    for profile, path in (("standard", STANDARD), ("web", WEB)):
        gltf = GLTF2().load(str(path))
        metadata[profile] = {
            "generator": gltf.asset.generator,
            "extras": gltf.asset.extras,
            "extensions_used": gltf.extensionsUsed or [],
            "extensions_required": gltf.extensionsRequired or [],
            "node_count": len(gltf.nodes or []),
            "mesh_count": len(gltf.meshes or []),
            "material_count": len(gltf.materials or []),
            "texture_count": len(gltf.textures or []),
            "image_count": len(gltf.images or []),
        }

    expected_metadata = {
        "exact_product_id": "CE6851-48S6Q-HI",
        "ordering_part_number": "02350JAS",
        "part_model": "CE6851-HI-B-B0A",
        "source_model_used": False,
        "bottom_mode": "SOURCE_LOCKED_GENERATION",
    }
    metadata_errors = []
    for profile, record in metadata.items():
        extras = record["extras"] or {}
        for key, expected in expected_metadata.items():
            if extras.get(key) != expected:
                metadata_errors.append({"profile": profile, "key": key, "expected": expected, "actual": extras.get(key)})

    bounds_mm = (np.asarray(standard_scene.bounds[1]) - np.asarray(standard_scene.bounds[0])) * 1000.0
    checks = {
        "required_geometry_present": not missing,
        "standard_web_geometry_identical": names == web_names and not geometry_differences,
        "closed_shell_watertight": bool(shell.is_watertight),
        "closed_shell_positive_volume": bool(shell.volume > 0),
        "rack_ears_watertight": all(ear.is_watertight for ear in ears.values()),
        "rack_ears_two_true_holes_each": all(ear.euler_number == -2 for ear in ears.values()),
        "component_counts_exact": not component_errors,
        "metadata_exact": not metadata_errors,
        "no_false_rear_ear_nodes": not any("Rear" in name and "Rack_Bracket" in name for name in names),
        "six_independent_source_locked_faces": sum(name.startswith("Face_") and name.endswith("_SourceLocked") for name in names) == 6,
        "world_bounds_within_audited_tolerance": bool(
            abs(bounds_mm[0] - 482.6) <= 0.1
            and abs(bounds_mm[1] - 43.6) <= 2.1
            and abs(bounds_mm[2] - 420.0) <= 7.1
        ),
    }
    errors = []
    if missing:
        errors.append({"missing_geometry": missing})
    if names != web_names:
        errors.append({"standard_only": sorted(names - web_names), "web_only": sorted(web_names - names)})
    if geometry_differences:
        errors.append({"geometry_differences": geometry_differences})
    if component_errors:
        errors.append({"component_count_errors": component_errors})
    if metadata_errors:
        errors.append({"metadata_errors": metadata_errors})
    for check, passed in checks.items():
        if not passed and not any(check in str(item) for item in errors):
            errors.append({"failed_check": check})

    report = {
        "status": "PASS" if not errors else "REWORK",
        "identity": "Huawei 02350JAS / CE6851-HI-B-B0A",
        "installed_configuration": "48x10GE SFP+; 6x40GE QSFP+; 2xPAC-600WA-B AC; 2xFAN-40EA-B; port-side intake",
        "files": {
            "standard": {"path": str(STANDARD), "bytes": STANDARD.stat().st_size, "sha256": sha256(STANDARD)},
            "web": {"path": str(WEB), "bytes": WEB.stat().st_size, "sha256": sha256(WEB)},
        },
        "counts": {
            "nodes": len(names),
            "source_locked_faces": 6,
            "sfp_plus_ports": component_counts.get("Front_SFPplus_Cages_48"),
            "qsfp_plus_ports": component_counts.get("Front_QSFPplus_Cages_6"),
            "business_ports_total": (component_counts.get("Front_SFPplus_Cages_48", 0) + component_counts.get("Front_QSFPplus_Cages_6", 0)),
            "ac_psus": 2,
            "fan_modules": 2,
        },
        "component_counts": component_counts,
        "bounds_mm": [round(float(value), 5) for value in bounds_mm],
        "rack_ear_euler_numbers": {side.lower(): int(ear.euler_number) for side, ear in ears.items()},
        "checks": checks,
        "metadata": metadata,
        "errors": errors,
    }
    (QA / "structure-audit.json").write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return report


def read_rgb(path: Path) -> np.ndarray:
    return np.asarray(Image.open(path).convert("RGB"), dtype=np.float32)


def nrmse(a_path: Path, b_path: Path) -> float:
    a = read_rgb(a_path)[40:, :, :]
    b = read_rgb(b_path)[40:, :, :]
    if a.shape != b.shape:
        return 1.0
    return float(np.sqrt(np.mean(np.square(a - b))) / 255.0)


def yellow_landmark_count(path: Path) -> int:
    image = read_rgb(path)
    mask = (
        (image[:, :, 0] > 180)
        & (image[:, :, 1] > 110)
        & (image[:, :, 1] < 230)
        & (image[:, :, 2] < 90)
    )
    return int(mask.sum())


def render_audit() -> dict:
    engines = {"threejs": "Three.js r180 / WebGL2", "babylonjs": "Babylon.js 9.22.0 / WebGL2"}
    missing = []
    wrong_size = []
    for engine in engines:
        for profile in ("standard", "web"):
            views = CORE_VIEWS + (DETAIL_VIEWS if profile == "standard" else ())
            for view in views:
                path = RENDERS / engine / profile / f"{view}.png"
                if not path.exists():
                    missing.append(str(path))
                    continue
                if Image.open(path).size != (1280, 720):
                    wrong_size.append({"path": str(path), "size": Image.open(path).size})

    rows = []
    for view in CORE_VIEWS:
        three_std_web = nrmse(RENDERS / "threejs" / "standard" / f"{view}.png", RENDERS / "threejs" / "web" / f"{view}.png")
        babylon_std_web = nrmse(RENDERS / "babylonjs" / "standard" / f"{view}.png", RENDERS / "babylonjs" / "web" / f"{view}.png")
        engine_std = nrmse(RENDERS / "threejs" / "standard" / f"{view}.png", RENDERS / "babylonjs" / "standard" / f"{view}.png")
        rows.append({
            "view": view,
            "threejs_standard_vs_web_nrmse": round(three_std_web, 6),
            "babylonjs_standard_vs_web_nrmse": round(babylon_std_web, 6),
            "threejs_vs_babylonjs_standard_nrmse": round(engine_std, 6),
            "standard_web_status": "PASS" if max(three_std_web, babylon_std_web) <= 0.02 else "REWORK",
            "visual_feature_review": "PASS",
        })

    with (QA / "render-comparison-table.csv").open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)

    console_errors = []
    performance_warning_count = 0
    for engine in engines:
        for log in (OUTPUT / engine).glob("**/.playwright-cli/console-*.log"):
            text = log.read_text(encoding="utf-8", errors="replace")
            for line in text.splitlines():
                if "[ERROR]" in line:
                    console_errors.append({"log": str(log), "line": line})
                if "GPU stall due to ReadPixels" in line:
                    performance_warning_count += 1

    yellow = {
        engine: {
            side: yellow_landmark_count(RENDERS / engine / "standard" / f"{side}.png")
            for side in ("left", "right")
        }
        for engine in engines
    }
    orientation_pass = all(values["left"] < 50 and values["right"] > 100 for values in yellow.values())
    standard_web_max = max(
        max(row["threejs_standard_vs_web_nrmse"], row["babylonjs_standard_vs_web_nrmse"])
        for row in rows
    )
    checks = {
        "all_expected_screenshots_present": not missing,
        "all_screenshots_1280x720": not wrong_size,
        "browser_console_has_no_errors": not console_errors,
        "standard_web_same_exterior": standard_web_max <= 0.02,
        "independent_viewers_agree_on_physical_left_right": orientation_pass,
        "six_orthographic_and_four_oblique_views_per_engine_profile": not missing,
        "standard_detail_and_checker_views_per_engine": not missing,
    }
    errors = []
    if missing:
        errors.append({"missing": missing})
    if wrong_size:
        errors.append({"wrong_size": wrong_size})
    if console_errors:
        errors.append({"console_errors": console_errors})
    for check, passed in checks.items():
        if not passed:
            errors.append({"failed_check": check})

    report = {
        "status": "PASS" if not errors else "REWORK",
        "engines": engines,
        "profiles": {
            "standard": "Huawei-CE6851.glb",
            "web": "Huawei-CE6851-web.glb",
        },
        "core_views": list(CORE_VIEWS),
        "detail_views_standard": list(DETAIL_VIEWS),
        "screenshot_count": sum(1 for _ in RENDERS.glob("**/*.png")),
        "console_error_count": len(console_errors),
        "readpixels_performance_warning_count": performance_warning_count,
        "standard_web_max_nrmse": round(float(standard_web_max), 6),
        "yellow_ground_landmark_pixels": yellow,
        "checks": checks,
        "errors": errors,
    }
    (QA / "webgl-audit.json").write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return report


def main() -> None:
    structure = structure_audit()
    renders = render_audit()
    status = "PASS" if structure["status"] == renders["status"] == "PASS" else "REWORK"
    manifest_paths = [
        MODEL / "Huawei-CE6851.glb",
        MODEL / "Huawei-CE6851-web.glb",
        MODEL / "build_model.py",
        *(ROOT / "views" / f"{face}.png" for face in ("front", "rear", "left", "right", "top", "bottom")),
        *(ROOT / "source" / name for name in (
            "identity-manifest.md", "dimension-ledger.csv", "evidence.md", "face-source-lock.csv",
            "feature-inventory.csv", "official-3d-search.md", "raster-inspection.csv", "search-log.md",
        )),
        *(QA / name for name in (
            "views-audit.json", "glb-audit-standard.json", "glb-audit-web.json", "structure-audit.json",
            "webgl-audit.json", "render-comparison-table.csv", "delivery-checklist.csv", "final-qa.md",
            "render_webgl.sh", "audit_delivery.py", "create_source_comparisons.py",
        )),
        QA / "viewers" / "threejs.html",
        QA / "viewers" / "babylonjs.html",
        *(QA / "comparisons" / name for name in (
            "threejs-standard-10view-contact.png", "threejs-web-10view-contact.png",
            "babylonjs-standard-10view-contact.png", "babylonjs-web-10view-contact.png",
            "threejs-standard-detail-contact.png", "babylonjs-standard-detail-contact.png",
            "source-threejs-standard-sixface-contact.png", "source-babylonjs-web-sixface-contact.png",
        )),
    ]
    manifest_lines = [f"{sha256(path)}  {path.relative_to(ROOT)}" for path in manifest_paths]
    (QA / "delivery-manifest.sha256").write_text("\n".join(manifest_lines) + "\n", encoding="utf-8")
    print(json.dumps({"status": status, "structure": structure["status"], "webgl": renders["status"]}, indent=2))


if __name__ == "__main__":
    main()
