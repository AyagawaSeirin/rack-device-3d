#!/usr/bin/env python3
"""Audit the exact visible configuration shared by both R620 GLBs."""

from __future__ import annotations

import json
from io import BytesIO
from pathlib import Path

from PIL import Image
from pygltflib import GLTF2


ROOT = Path(__file__).resolve().parents[1]
EXPECTED_VISIBLE = {
    "SFF_carriers": 10,
    "front_rack_latches": 2,
    "PCIe_low_profile_blanks": 3,
    "iDRAC7_RJ45": 1,
    "DB9_serial": 1,
    "rear_VGA": 1,
    "rear_USB2": 2,
    "network_adapter_RJ45": 4,
    "network_adapter_SFP": 0,
    "AC_PSU_750W": 2,
    "DC_PSU": 0,
    "IEC_AC_inlets": 2,
    "PSU_visible_fans": 2,
    "rear_rack_ears": 0,
}
EXPECTED_DIMS = [0.4824, 0.0428, 0.7521]


def image_dimensions(gltf: GLTF2) -> list[list[int]]:
    blob = gltf.binary_blob()
    result: list[list[int]] = []
    for item in gltf.images:
        if item.uri is not None or item.bufferView is None:
            raise ValueError("All images must be embedded GLB bufferViews")
        view = gltf.bufferViews[item.bufferView]
        start = view.byteOffset or 0
        with Image.open(BytesIO(blob[start:start + view.byteLength])) as image:
            result.append(list(image.size))
    return result


def load(profile: str, filename: str) -> dict[str, object]:
    path = ROOT / "model" / filename
    gltf = GLTF2().load_binary(path)
    names = [node.name or "" for node in gltf.nodes]
    materials = [material.name or "" for material in gltf.materials]
    return {
        "profile": profile,
        "path": str(path.relative_to(ROOT)),
        "extras": gltf.asset.extras or {},
        "names": names,
        "materials": materials,
        "image_dimensions": image_dimensions(gltf),
        "external_images": [item.uri for item in gltf.images if item.uri],
        "external_buffers": [item.uri for item in gltf.buffers if item.uri],
        "mirrored": [node.name for node in gltf.nodes if node.scale and node.scale[0] * node.scale[1] * node.scale[2] < 0],
        "counts": {
            "scenes": len(gltf.scenes), "nodes": len(gltf.nodes),
            "meshes": len(gltf.meshes), "materials": len(gltf.materials),
            "textures": len(gltf.textures), "images": len(gltf.images),
        },
    }


def count_suffix(names: list[str], prefix: str, suffix: str) -> int:
    return sum(name.startswith(prefix) and name.endswith(suffix) for name in names)


def main() -> None:
    standard = load("standard", "Dell-R620-2.5inch.glb")
    web = load("web", "Dell-R620-2.5inch-web.glb")
    checks: list[dict[str, object]] = []
    errors: list[str] = []

    def check(name: str, condition: bool, detail: object) -> None:
        checks.append({"check": name, "status": "PASS" if condition else "FAIL", "detail": detail})
        if not condition:
            errors.append(f"{name}: {detail}")

    for item in (standard, web):
        profile = item["profile"]
        extras = item["extras"]
        names = item["names"]
        materials = item["materials"]
        check(f"{profile}_identity", extras.get("manufacturer") == "Dell" and extras.get("product_id") == "PowerEdge R620", extras)
        check(f"{profile}_variant", extras.get("variant") == "10x2.5-inch SFF no bezel", extras.get("variant"))
        check(f"{profile}_profile_marker", extras.get("profile") == profile, extras.get("profile"))
        check(f"{profile}_self_built", extras.get("source_model_used") is False, extras.get("source_model_used"))
        check(f"{profile}_bottom_mode", extras.get("bottom_mode") == "GENERIC_BOTTOM_FALLBACK", extras.get("bottom_mode"))
        check(f"{profile}_visible_counts", extras.get("visible_counts") == EXPECTED_VISIBLE, extras.get("visible_counts"))
        check(f"{profile}_closed_core", names.count("Closed_Chassis_Core") == 1, names.count("Closed_Chassis_Core"))
        check(f"{profile}_six_faces", all(names.count(f"Face_{face}_Approved_Imagegen") == 1 for face in ("Front", "Rear", "Left", "Right", "Top", "Bottom")), names[:8])
        check(f"{profile}_ten_sff_carriers", count_suffix(names, "Front_SFF_Drive_", "_Handle_Top") == 10, count_suffix(names, "Front_SFF_Drive_", "_Handle_Top"))
        check(f"{profile}_three_low_profile_slots", count_suffix(names, "Rear_LowProfile_PCIe_Blank_", "_Top") == 3, count_suffix(names, "Rear_LowProfile_PCIe_Blank_", "_Top"))
        check(f"{profile}_dual_ac_psus", count_suffix(names, "Rear_750W_AC_PSU_", "_Frame_Top") == 2, count_suffix(names, "Rear_750W_AC_PSU_", "_Frame_Top"))
        check(f"{profile}_no_mirroring", not item["mirrored"], item["mirrored"])
        check(f"{profile}_no_external_resources", not item["external_images"] and not item["external_buffers"], {"images": item["external_images"], "buffers": item["external_buffers"]})
        check(f"{profile}_six_embedded_images", len(item["image_dimensions"]) == 6, item["image_dimensions"])
        check(f"{profile}_six_face_materials", sum(name.startswith("FACE_") and "PHOTOGRAPHIC" in name for name in materials) == 6, materials)
        check(f"{profile}_no_wrong_model_tokens", not any(token in name.lower() for name in names + materials for token in ("r620xd", "r720", "8sff")), "no R620xd/R720/8SFF node or material names")

    check("same_nodes_between_profiles", standard["names"] == web["names"], {"standard": len(standard["names"]), "web": len(web["names"])})
    check("same_materials_between_profiles", standard["materials"] == web["materials"], {"standard": len(standard["materials"]), "web": len(web["materials"])})
    check("same_counts_between_profiles", standard["counts"] == web["counts"], {"standard": standard["counts"], "web": web["counts"]})
    for profile in ("standard", "web"):
        audit = json.loads((ROOT / "qa" / f"glb-{profile}-audit.json").read_text(encoding="utf-8"))
        dimensions = audit["geometry"]["dimensions_xyz"]
        check(f"{profile}_installed_dimensions", all(abs(a - b) <= 0.0008 for a, b in zip(dimensions, EXPECTED_DIMS)), dimensions)
        check(f"{profile}_skill_glb_audit", audit["status"] == "PASS" and audit["error_count"] == 0 and audit["warning_count"] == 0, {"status": audit["status"], "errors": audit["error_count"], "warnings": audit["warning_count"]})

    output = {
        "status": "PASS" if not errors else "FAIL",
        "error_count": len(errors),
        "errors": errors,
        "expected_configuration": {
            "identity": "Dell PowerEdge R620, not R620xd/R720",
            "front": "10 x 2.5-inch SFF, two rows by five columns, all carriers installed, no bezel",
            "rear": "3 low-profile PCIe positions; iDRAC7; DB9; VGA; 2 USB2; 4 Base-T RJ45",
            "power": "2 x matching Dell 750W hot-plug AC PSU",
            "bottom": "GENERIC_BOTTOM_FALLBACK",
        },
        "profiles": {
            item["profile"]: {key: value for key, value in item.items() if key not in {"names", "materials", "extras"}}
            for item in (standard, web)
        },
        "checks": checks,
    }
    (ROOT / "qa" / "structure-audit.json").write_text(json.dumps(output, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": output["status"], "checks": len(checks), "errors": len(errors)}, indent=2))
    raise SystemExit(0 if not errors else 1)


if __name__ == "__main__":
    main()
