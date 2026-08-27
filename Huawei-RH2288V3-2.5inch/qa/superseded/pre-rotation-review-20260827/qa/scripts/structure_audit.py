#!/usr/bin/env python3
"""Configuration-specific structural audit for the corrected RH2288 V3 model."""

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
    bays = sorted({int(match.group(1)) for name in names
                   if (match := re.match(r"FRONT_Drive_Carrier_(\d\d)_", name))})
    psus = sorted({int(match.group(1)) for name in names
                   if (match := re.match(r"REAR_AC_PSU_(\d)_", name))})
    rear_drive_names = [name for name in names if name.startswith("REAR_Drive_")]
    mirrored = [name for name in names if "Mirror" in name or "Mirrored" in name]
    front_usb_names = [name for name in names if name.startswith("FRONT_") and "USB" in name]
    left_ethernet_indicators = [
        name for name in names if name.startswith("FRONT_Left_Ethernet_Indicator_")
    ]
    right_control_names = [
        "FRONT_Right_Fault_Diagnostic_Display",
        "FRONT_Right_Health_Control",
        "FRONT_Right_UID_Control",
        "FRONT_Right_Power_Control",
        "FRONT_Right_NMI_Control",
        "FRONT_Right_VGA_Relief",
    ]
    requirements = {
        "front_bay_indices_are_00_through_23": bays == list(range(24)),
        "dual_ac_psu_indices_are_0_and_1": psus == [0, 1],
        "no_rear_drive_geometry": not rear_drive_names,
        "closed_chassis_node_present": "Closed_Chassis_Sheet_Metal_447x708x86.1mm" in names,
        "independent_left_texture_node": "Texture_LEFT_Independent" in names,
        "independent_right_texture_node": "Texture_RIGHT_Independent" in names,
        "no_mirror_named_nodes": not mirrored,
        "two_port_flexible_nic": all(f"REAR_Flexible_NIC_RJ45_A{i}" in names for i in (1, 2)),
        "standard_mgmt_cluster": all(name in names for name in
                                     ("REAR_Mgmt_RJ45", "REAR_LAN_RJ45", "REAR_VGA", "REAR_DB9_Serial")),
        "exactly_one_front_usb_on_physical_left": front_usb_names == ["FRONT_Left_USB_2_0"],
        "four_front_ethernet_indicators_on_physical_left": sorted(left_ethernet_indicators)
        == [f"FRONT_Left_Ethernet_Indicator_{index}" for index in range(1, 5)],
        "complete_right_diagnostic_control_group": all(name in names for name in right_control_names),
    }
    return {
        "path": str(path),
        "sha256": sha256(path),
        "node_count": len(names),
        "front_bay_indices": bays,
        "ac_psu_indices": psus,
        "rear_drive_names": rear_drive_names,
        "mirrored_node_names": mirrored,
        "front_usb_names": front_usb_names,
        "left_ethernet_indicator_names": sorted(left_ethernet_indicators),
        "right_control_names": [name for name in right_control_names if name in names],
        "requirements": requirements,
        "status": "PASS" if all(requirements.values()) else "FAIL",
    }


def main() -> None:
    result = {
        "identity": "Huawei FusionServer RH2288 V3 / H22M-03 24x2.5-inch SFF",
        "power": "dual hot-swap AC, vertically stacked on one rear side",
        "bottom": "GENERIC_BOTTOM_FALLBACK",
        "left_view_sha256": sha256(ROOT / "views" / "left.png"),
        "right_view_sha256": sha256(ROOT / "views" / "right.png"),
        "left_right_images_are_byte_distinct": sha256(ROOT / "views" / "left.png") != sha256(ROOT / "views" / "right.png"),
        "models": [
            audit(MODEL / "Huawei-RH2288V3-2.5inch.glb"),
            audit(MODEL / "Huawei-RH2288V3-2.5inch-web.glb"),
        ],
    }
    result["status"] = "PASS" if (
        result["left_right_images_are_byte_distinct"]
        and all(model["status"] == "PASS" for model in result["models"])
    ) else "FAIL"
    output = ROOT / "qa" / "audits" / "structure.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(result["status"], output)


if __name__ == "__main__":
    main()
