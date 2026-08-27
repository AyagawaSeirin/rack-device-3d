#!/usr/bin/env python3
"""Audit exact-configuration structure shared by the standard and web GLBs."""

from __future__ import annotations

import json
from io import BytesIO
from pathlib import Path

from PIL import Image
from pygltflib import GLTF2


ROOT = Path(__file__).resolve().parents[1]
EXPECTED_VISIBLE = {
    "LFF_carriers": 8,
    "front_rack_latches": 2,
    "PCIe_low_profile_blanks": 3,
    "PCIe_full_height_blanks": 4,
    "iDRAC7_RJ45": 1,
    "DB9_serial": 1,
    "rear_VGA": 1,
    "rear_USB2": 2,
    "network_adapter_RJ45": 4,
    "AC_PSU_750W": 2,
    "IEC_AC_inlets": 2,
    "PSU_visible_fans": 2,
}
EXPECTED_DIMS = [0.4824, 0.0873, 0.7410]


def image_dimensions(gltf: GLTF2) -> list[list[int]]:
    blob = gltf.binary_blob()
    dimensions: list[list[int]] = []
    for item in gltf.images:
        if item.uri is not None or item.bufferView is None:
            raise ValueError("All GLB images must be embedded bufferView resources")
        view = gltf.bufferViews[item.bufferView]
        start = view.byteOffset or 0
        with Image.open(BytesIO(blob[start : start + view.byteLength])) as image:
            dimensions.append(list(image.size))
    return dimensions


def load(profile: str, filename: str) -> dict[str, object]:
    path = ROOT / "model" / filename
    gltf = GLTF2().load_binary(path)
    extras = gltf.asset.extras or {}
    names = [node.name or "" for node in gltf.nodes]
    material_names = [material.name or "" for material in gltf.materials]
    external_images = [item.uri for item in gltf.images if item.uri]
    external_buffers = [item.uri for item in gltf.buffers if item.uri]
    mirrored = [node.name for node in gltf.nodes if node.scale and node.scale[0] * node.scale[1] * node.scale[2] < 0]
    return {
        "profile": profile,
        "path": str(path.relative_to(ROOT)),
        "gltf": gltf,
        "extras": extras,
        "node_names": names,
        "material_names": material_names,
        "image_dimensions": image_dimensions(gltf),
        "external_images": external_images,
        "external_buffers": external_buffers,
        "mirrored_nodes": mirrored,
        "counts": {
            "scenes": len(gltf.scenes),
            "nodes": len(gltf.nodes),
            "meshes": len(gltf.meshes),
            "materials": len(gltf.materials),
            "textures": len(gltf.textures),
            "images": len(gltf.images),
        },
    }


def prefix_instances(names: list[str], prefix: str, edge_suffix: str = "_Top") -> int:
    return sum(name.startswith(prefix) and name.endswith(edge_suffix) for name in names)


def main() -> None:
    standard = load("standard", "Dell-R720-3.5inch.glb")
    web = load("web", "Dell-R720-3.5inch-web.glb")
    errors: list[str] = []
    checks: list[dict[str, object]] = []

    def check(name: str, condition: bool, detail: object) -> None:
        checks.append({"check": name, "status": "PASS" if condition else "FAIL", "detail": detail})
        if not condition:
            errors.append(f"{name}: {detail}")

    for item in (standard, web):
        extras = item["extras"]
        names = item["node_names"]
        materials = item["material_names"]
        profile = item["profile"]
        check(f"{profile}_identity", extras.get("manufacturer") == "Dell" and extras.get("product_id") == "PowerEdge R720", extras)
        check(f"{profile}_variant", extras.get("variant") == "8LFF 3.5-inch no bezel", extras.get("variant"))
        check(f"{profile}_profile_marker", extras.get("profile") == profile, extras.get("profile"))
        check(f"{profile}_self_built", extras.get("source_model_used") is False, extras.get("source_model_used"))
        check(f"{profile}_bottom_mode", extras.get("bottom_mode") == "GENERIC_BOTTOM_FALLBACK", extras.get("bottom_mode"))
        check(f"{profile}_visible_counts", extras.get("visible_counts") == EXPECTED_VISIBLE, extras.get("visible_counts"))
        check(f"{profile}_closed_core", names.count("Closed_Chassis_Core") == 1, names.count("Closed_Chassis_Core"))
        check(f"{profile}_six_independent_faces", all(names.count(f"Face_{face}_Approved_Imagegen") == 1 for face in ("Front", "Rear", "Left", "Right", "Top", "Bottom")), names[:7])
        check(f"{profile}_eight_lff_carriers", prefix_instances(names, "Front_LFF_") == 8, prefix_instances(names, "Front_LFF_"))
        check(f"{profile}_three_low_profile_slots", prefix_instances(names, "Rear_PCIe_LowProfile_Blank_") == 3, prefix_instances(names, "Rear_PCIe_LowProfile_Blank_"))
        check(f"{profile}_four_full_height_slots", prefix_instances(names, "Rear_PCIe_FullHeight_Blank_") == 4, prefix_instances(names, "Rear_PCIe_FullHeight_Blank_"))
        check(f"{profile}_dual_psu_frames", prefix_instances(names, "Rear_AC_PSU_", "_Top") == 2, prefix_instances(names, "Rear_AC_PSU_", "_Top"))
        check(f"{profile}_dual_psu_outer_photos", sum(name.endswith("SourceLocked_OuterFace") for name in names) == 2, [name for name in names if name.endswith("SourceLocked_OuterFace")])
        check(f"{profile}_front_ear_rear_closures", sum(name.endswith("Rear_Closure") for name in names) == 2, [name for name in names if name.endswith("Rear_Closure")])
        check(f"{profile}_no_mirroring", not item["mirrored_nodes"], item["mirrored_nodes"])
        check(f"{profile}_no_external_resources", not item["external_images"] and not item["external_buffers"], {"images": item["external_images"], "buffers": item["external_buffers"]})
        check(f"{profile}_eight_embedded_images", len(item["image_dimensions"]) == 8, item["image_dimensions"])
        check(f"{profile}_six_source_locked_materials", sum(name.startswith("FACE_") and "PHOTOGRAPHIC" in name for name in materials) == 8, materials)
        check(f"{profile}_no_r720xd_or_flexbay", not any("r720xd" in name.lower() or "flex" in name.lower() for name in names + materials), "no forbidden node/material names")

    check("same_node_names_between_profiles", standard["node_names"] == web["node_names"], {"standard": len(standard["node_names"]), "web": len(web["node_names"])})
    check("same_material_names_between_profiles", standard["material_names"] == web["material_names"], {"standard": len(standard["material_names"]), "web": len(web["material_names"])})
    check("same_structure_counts_between_profiles", standard["counts"] == web["counts"], {"standard": standard["counts"], "web": web["counts"]})
    for profile in ("standard", "web"):
        audit = json.loads((ROOT / "qa" / f"glb-{profile}-audit.json").read_text(encoding="utf-8"))
        dimensions = audit["geometry"]["dimensions_xyz"]
        check(f"{profile}_installed_dimensions", all(abs(a - b) <= 0.0002 for a, b in zip(dimensions, EXPECTED_DIMS)), dimensions)
        check(f"{profile}_skill_glb_audit", audit["status"] == "PASS" and audit["error_count"] == 0 and audit["warning_count"] == 0, {"status": audit["status"], "errors": audit["error_count"], "warnings": audit["warning_count"]})

    serializable = {
        "status": "PASS" if not errors else "FAIL",
        "error_count": len(errors),
        "errors": errors,
        "expected_configuration": {
            "identity": "Dell PowerEdge R720 (not R720xd)",
            "front": "8 x 3.5-inch LFF, 2x4, no bezel",
            "rear": "3 low-profile + 4 full-height PCIe blanks; iDRAC7; DB9; VGA; 2 USB2; 4 RJ45",
            "power": "2 x Dell 750W hot-plug AC PSU with IEC inlets and visible fans",
            "branding": "factory Dell and PowerEdge R720 marks retained in source-locked front face",
            "bottom": "GENERIC_BOTTOM_FALLBACK",
        },
        "profiles": {
            item["profile"]: {
                key: value
                for key, value in item.items()
                if key not in {"gltf", "node_names", "material_names", "extras"}
            }
            for item in (standard, web)
        },
        "checks": checks,
    }
    output = ROOT / "qa" / "structure-audit.json"
    output.write_text(json.dumps(serializable, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": serializable["status"], "checks": len(checks), "errors": len(errors)}, indent=2))
    raise SystemExit(0 if not errors else 1)


if __name__ == "__main__":
    main()
