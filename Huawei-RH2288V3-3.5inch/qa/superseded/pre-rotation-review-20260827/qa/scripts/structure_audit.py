#!/usr/bin/env python3
"""Configuration-specific structural audit for the 12-LFF RH2288 V3 GLBs."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

from pygltflib import GLTF2


ROOT = Path(__file__).resolve().parents[2]
MODEL = ROOT / "model"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def audit(path: Path) -> dict:
    gltf = GLTF2().load(path)
    names = [node.name or "" for node in gltf.nodes]
    carrier_matches = {
        (int(match.group(1)), int(match.group(2)), int(match.group(3)))
        for name in names
        if (match := re.match(r"FRONT_LFF_Carrier_(\d\d)_R(\d)_C(\d)_", name))
    }
    carrier_indices = sorted({item[0] for item in carrier_matches})
    carrier_positions = sorted({(item[1], item[2]) for item in carrier_matches})
    psu_indices = sorted(
        {
            int(match.group(1))
            for name in names
            if (match := re.match(r"REAR_AC_PSU_(\d)_", name))
        }
    )
    sm211_ports = sorted(
        name for name in names if re.fullmatch(r"REAR_SM211_Flexible_NIC_GE[12]_RJ45", name)
    )
    rear_drive_names = [name for name in names if "REAR_Drive" in name or "Rear_Disk" in name]
    rear_ear_names = [name for name in names if name.startswith("REAR_") and "Ear" in name]
    mirrored = [name for name in names if "Mirror" in name or "Mirrored" in name]
    materials_opaque = all((material.alphaMode or "OPAQUE") == "OPAQUE" for material in gltf.materials)
    textured_materials = [
        material
        for material in gltf.materials
        if material.pbrMetallicRoughness
        and material.pbrMetallicRoughness.baseColorTexture is not None
    ]
    requirements = {
        "twelve_lff_carrier_indices_00_through_11": carrier_indices == list(range(12)),
        "lff_carrier_layout_is_three_rows_by_four_columns": carrier_positions
        == [(row, column) for row in range(3) for column in range(4)],
        "separate_front_control_ears": all(
            any(name == f"FRONT_Control_Rack_Ear_{side}" or name.startswith(f"FRONT_Control_Rack_Ear_{side}_") for name in names)
            for side in ("L", "R")
        ),
        "no_rear_ear_geometry": not rear_ear_names,
        "dual_ac_psu_indices_are_1_and_2": psu_indices == [1, 2],
        "psu_fans_and_cord_loops_are_geometry": all(
            all(
                f"REAR_AC_PSU_{index}_{suffix}" in names
                for suffix in ("Fan_Rotor", "Fan_Hub", "Cord_Loop_Outer", "Lime_Ejector")
            )
            for index in (1, 2)
        ),
        "no_rear_drive_geometry": not rear_drive_names,
        "sm211_has_exactly_two_ge_ports": sm211_ports
        == ["REAR_SM211_Flexible_NIC_GE1_RJ45", "REAR_SM211_Flexible_NIC_GE2_RJ45"],
        "standard_management_console_group": all(
            name in names
            for name in (
                "REAR_USB_3_0_1",
                "REAR_USB_3_0_2",
                "REAR_Mgmt_RJ45",
                "REAR_VGA",
                "REAR_DB9_Serial",
                "REAR_UID_Button",
            )
        ),
        "blank_pcie_and_onboard_slots_present": all(
            name in names
            for name in (
                "REAR_IO_Module_2_Blank_PCIe_0_Top",
                "REAR_IO_Module_2_Blank_PCIe_1_Top",
                "REAR_IO_Module_2_Blank_PCIe_2_Top",
                "REAR_Onboard_Slot_4_Blank_Top",
                "REAR_Onboard_Slot_5_Blank_Top",
                "REAR_IO_Module_1_Blank_PCIe_0_Top",
                "REAR_IO_Module_1_Blank_PCIe_1_Top",
                "REAR_IO_Module_1_Blank_PCIe_2_Top",
            )
        ),
        "closed_447x748x86_1_body_present": "Closed_Chassis_Sheet_Metal_447x748x86.1mm" in names,
        "independent_left_and_right_textures": all(
            name in names for name in ("Texture_LEFT_Independent", "Texture_RIGHT_Independent")
        ),
        "top_service_latch_is_source_locked_relief_geometry":
        "TOP_Service_Latch_Source_Locked_Relief" in names,
        "all_materials_are_opaque": materials_opaque,
        "six_embedded_face_textures": len(textured_materials) == 6 and len(gltf.images) == 6,
        "no_mirrored_named_nodes": not mirrored,
    }
    return {
        "path": str(path.relative_to(ROOT)),
        "bytes": path.stat().st_size,
        "sha256": sha256(path),
        "node_count": len(names),
        "mesh_count": len(gltf.meshes),
        "material_count": len(gltf.materials),
        "texture_count": len(gltf.textures),
        "front_lff_carrier_indices": carrier_indices,
        "front_lff_row_column_positions": carrier_positions,
        "ac_psu_indices": psu_indices,
        "sm211_ports": sm211_ports,
        "rear_drive_names": rear_drive_names,
        "rear_ear_names": rear_ear_names,
        "mirrored_node_names": mirrored,
        "requirements": requirements,
        "status": "PASS" if all(requirements.values()) else "FAIL",
    }


def main() -> None:
    result = {
        "identity": "Huawei FusionServer RH2288 V3 / H22M-03 12x3.5-inch LFF",
        "rear_configuration": "no rear disks; SM211 2xGE; dual vertically stacked 460 W AC PSU",
        "bottom": "GENERIC_BOTTOM_FALLBACK",
        "left_view_sha256": sha256(ROOT / "views" / "left.png"),
        "right_view_sha256": sha256(ROOT / "views" / "right.png"),
        "left_right_images_are_byte_distinct": sha256(ROOT / "views" / "left.png")
        != sha256(ROOT / "views" / "right.png"),
        "models": [
            audit(MODEL / "Huawei-RH2288V3-3.5inch.glb"),
            audit(MODEL / "Huawei-RH2288V3-3.5inch-web.glb"),
        ],
    }
    result["standard_web_external_structure_matches"] = {
        key: result["models"][0][key] == result["models"][1][key]
        for key in (
            "node_count",
            "mesh_count",
            "material_count",
            "texture_count",
            "front_lff_carrier_indices",
            "front_lff_row_column_positions",
            "ac_psu_indices",
            "sm211_ports",
        )
    }
    result["status"] = "PASS" if (
        result["left_right_images_are_byte_distinct"]
        and all(result["standard_web_external_structure_matches"].values())
        and all(model["status"] == "PASS" for model in result["models"])
    ) else "FAIL"
    output = ROOT / "qa" / "audits" / "structure.json"
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(result["status"], output)


if __name__ == "__main__":
    main()
