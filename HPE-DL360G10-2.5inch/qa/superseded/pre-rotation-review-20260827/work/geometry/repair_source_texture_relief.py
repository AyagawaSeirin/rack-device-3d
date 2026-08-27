#!/usr/bin/env python3
"""Repair coarse face overlays while retaining source-locked texture and relief geometry.

The existing GLBs contain the correct source-locked six-face textures, but several
large flat helper meshes sit in front of those textures.  This repair reorders the
front/rear/top/side relief so the source photograph remains the visible face while
thin seams, carrier frames, the top latch, rack ears, and separate PSU frames keep
real parallax and silhouette.
"""

from __future__ import annotations

import argparse
import json
import re
import struct
from pathlib import Path


JSON_CHUNK = 0x4E4F534A
BIN_CHUNK = 0x004E4942


def read_glb(path: Path) -> tuple[dict, bytes]:
    data = path.read_bytes()
    magic, version, declared_length = struct.unpack_from("<III", data, 0)
    if magic != 0x46546C67 or version != 2 or declared_length != len(data):
        raise ValueError(f"invalid GLB 2.0 header: {path}")
    offset = 12
    document = None
    binary = None
    while offset < len(data):
        chunk_length, chunk_type = struct.unpack_from("<II", data, offset)
        offset += 8
        chunk = data[offset : offset + chunk_length]
        offset += chunk_length
        if chunk_type == JSON_CHUNK:
            document = json.loads(chunk.decode("utf-8"))
        elif chunk_type == BIN_CHUNK:
            binary = chunk
    if document is None or binary is None:
        raise ValueError(f"GLB must contain JSON and BIN chunks: {path}")
    return document, binary


def write_glb(path: Path, document: dict, binary: bytes) -> None:
    json_bytes = json.dumps(
        document, ensure_ascii=False, separators=(",", ":")
    ).encode("utf-8")
    json_bytes += b" " * ((-len(json_bytes)) % 4)
    binary += b"\x00" * ((-len(binary)) % 4)
    total = 12 + 8 + len(json_bytes) + 8 + len(binary)
    header = struct.pack("<III", 0x46546C67, 2, total)
    payload = (
        header
        + struct.pack("<II", len(json_bytes), JSON_CHUNK)
        + json_bytes
        + struct.pack("<II", len(binary), BIN_CHUNK)
        + binary
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(payload)


def set_axis(node: dict, axis: int, value: float) -> None:
    translation = list(node.get("translation", [0.0, 0.0, 0.0]))
    translation[axis] = value
    node["translation"] = translation


def set_scale_axis(node: dict, axis: int, value: float) -> None:
    scale = list(node.get("scale", [1.0, 1.0, 1.0]))
    scale[axis] = value
    node["scale"] = scale


def repair(document: dict) -> dict:
    nodes = document["nodes"]
    by_name = {node.get("name"): node for node in nodes}

    # Front: keep the high-resolution source texture visible.  Carrier perimeter
    # rails remain in front as shallow relief; coarse handles, controls, and fills
    # move just behind the texture because their exact appearance is already baked.
    set_axis(by_name["FrontBody_TexturePlane"], 2, 351.0)
    front_hidden = re.compile(
        r"^SFF_Carrier_\d+_(PullHandle|HandleHub|ReleaseLatch)$"
        r"|^Front_DriveBay_ID_PullTab$"
        r"|^UniversalMediaBay_Upper_OpticalDisplay_Blank$"
        r"|^FrontControl_Backplate$"
        r"|^Front_(USB3_Port|iLO_Service_Port|Status_LED_\d+)$"
    )
    for node in nodes:
        if front_hidden.search(node.get("name", "")):
            set_axis(node, 2, 350.75)
            set_scale_axis(node, 2, 0.1)
    set_axis(by_name["UniversalMediaBay_Upper_Blank_Lip"], 2, 351.24)

    # Rear: the exact source texture carries the port/label/fan appearance.  Large
    # placeholder port and fan faces move behind it.  Thin four-sided PSU frames
    # are added in front so the two independent hot-plug modules retain relief.
    set_axis(by_name["Rear_TexturePlane"], 2, -350.6)
    rear_hidden = re.compile(
        r"^PCIe_.*_Vent_\d+$"
        r"|^FlexibleLOM_Blank_Vent_\d+$"
        r"|^Rear_(USB3_Port_\d+|Serial_DB9|iLO_Management_RJ45|VGA_Port)$"
        r"|^Embedded_1GbE_(RJ45|LED)_\d+$"
        r"|^PSU_\d+_(Fan|FanHub|FanBlade_\d+|IEC_C14_Inlet|ReleaseHandle|StatusLED)$"
    )
    for node in nodes:
        if rear_hidden.search(node.get("name", "")):
            set_axis(node, 2, -350.35)
            set_scale_axis(node, 2, 0.1)

    for name in (
        "PCIe_Blank_Slot1_Plate",
        "PCIe_Blank_Slot2_Plate",
        "PCIe_Blank_Slot3_Plate",
        "FlexibleLOM_Blank_Plate",
        "PSU_1_ModuleBody",
        "PSU_2_ModuleBody",
    ):
        node = by_name[name]
        set_axis(node, 2, -350.05)
        scale = list(node.get("scale", [1.0, 1.0, 1.0]))
        scale[2] = 0.45
        node["scale"] = scale

    existing_names = {node.get("name") for node in nodes}
    for psu_number, center_x in ((1, -119.0), (2, -168.0)):
        parent = by_name[f"PSU_{psu_number}_500W_AC"]
        frame_specs = (
            ("Top", [center_x, 18.5, -351.1], [46.0, 1.2, 1.0]),
            ("Bottom", [center_x, -18.5, -351.1], [46.0, 1.2, 1.0]),
            ("Left", [center_x + 22.4, 0.0, -351.1], [1.2, 38.0, 1.0]),
            ("Right", [center_x - 22.4, 0.0, -351.1], [1.2, 38.0, 1.0]),
        )
        for side, translation, scale in frame_specs:
            name = f"PSU_{psu_number}_Frame{side}_SourceTextureReveal"
            if name in existing_names:
                continue
            nodes.append(
                {
                    "name": name,
                    "mesh": 18,
                    "translation": translation,
                    "scale": scale,
                }
            )
            parent.setdefault("children", []).append(len(nodes) - 1)
            existing_names.add(name)

    # Top/side: source textures already contain the exact vent, label, fastener,
    # and rail-slot pattern.  Keep the top seam/latch and front-ear silhouette, but
    # move duplicated blocky cells and side markers behind their texture planes.
    for node in nodes:
        name = node.get("name", "")
        if re.match(r"^TopVent_.*_Cell_", name) or re.match(
            r"^Top_(Service_Label_.*_Relief|Front_Rivet_\d+)$", name
        ):
            set_axis(node, 1, 21.24)
            set_scale_axis(node, 1, 0.05)
        elif name.startswith("Left_Rail"):
            set_axis(node, 0, -217.2)
            set_scale_axis(node, 0, 0.05)
        elif name.startswith("Right_Rail"):
            set_axis(node, 0, 217.2)
            set_scale_axis(node, 0, 0.05)

    asset = document.setdefault("asset", {})
    generator = asset.get("generator", "rack-device-exact-exterior-builder")
    suffix = "/final-source-lock-relief-repair"
    if not generator.endswith(suffix):
        asset["generator"] = generator + suffix
    extras = asset.setdefault("extras", {})
    extras["visibleParts"] = len(nodes)
    extras["surfaceRepair"] = (
        "Source-locked face textures remain visually authoritative; coarse helper "
        "faces moved behind them while rack ears, carrier frames, PSU frames, top "
        "seam/latch, closed body, and separate assemblies retain visible relief."
    )
    return document


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    document, binary = read_glb(args.input)
    write_glb(args.output, repair(document), binary)
    print(f"wrote {args.output} ({args.output.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
