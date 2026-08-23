#!/usr/bin/env python3
"""Audit required exterior feature groups by GLB node name."""

from __future__ import annotations

import json
from pathlib import Path

from pygltflib import GLTF2


ROOT = Path(__file__).resolve().parents[2]
MODEL = ROOT / "model" / "Huawei-RH1288V5-3.5inch.glb"

GROUPS = {
    "rack_ears": ["FrontRackEar_Left", "FrontRackEar_Right"],
    "four_lff_carriers": [f"LFFCarrier{i}_Handle" for i in range(1, 5)],
    "four_lff_release_accents": [f"LFFCarrier{i}_ReleaseAccent" for i in range(1, 5)],
    "three_rear_pcie_regions": [f"RearPCIeBlank_{i}_Frame" for i in range(1, 4)],
    "lom_ports": [f"RearLOM_RJ45_{i}_Socket" for i in range(1, 5)],
    "dual_900w_ac_psu_bodies": [f"ACPSU_900W_{i}_Body" for i in range(1, 3)],
    "dual_ac_c14_inlets": [f"ACPSU_900W_{i}_IEC_C14" for i in range(1, 3)],
    "dual_psu_fans": [f"ACPSU_900W_{i}_FanCavity" for i in range(1, 3)],
    "top_vent_bands": ["TopVentBandFront_Recess", "TopVentBandRear_Recess"],
    "independent_side_relief": ["LeftSideUpperRailRelief", "RightSideUpperRailRelief", "LeftRearRailCutout", "RightFrontVentRelief"],
    "six_appearance_surfaces": [
        "FrontExactAppearanceSurface", "RearExactAppearanceSurface",
        "RightIndependentAppearanceSurface", "LeftIndependentAppearanceSurface",
        "TopExactAppearanceSurface", "BottomFallbackAppearanceSurface",
    ],
}


def main() -> None:
    gltf = GLTF2().load_binary(str(MODEL))
    names = {node.name for node in gltf.nodes or [] if node.name}
    checks = {}
    for group, required in GROUPS.items():
        missing = [name for name in required if name not in names]
        checks[group] = {"expected": len(required), "found": len(required) - len(missing), "missing": missing, "status": "PASS" if not missing else "FAIL"}
    report = {
        "model": MODEL.name,
        "node_count": len(gltf.nodes or []),
        "checks": checks,
        "status": "PASS" if all(item["status"] == "PASS" for item in checks.values()) else "FAIL",
    }
    output = ROOT / "qa" / "feature-audit.json"
    output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
