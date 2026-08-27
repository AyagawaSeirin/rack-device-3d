#!/usr/bin/env python3
"""Independent forced audit of the current RH2288 V3 deliverables."""

from __future__ import annotations

import csv
import hashlib
import json
import re
import struct
from io import BytesIO
from pathlib import Path

from PIL import Image, ImageChops
from pygltflib import GLTF2


ROOT = Path(__file__).resolve().parents[3]
MODEL = ROOT / "model"
VIEWS = ROOT / "views"
OUT = ROOT / "qa" / "forced-review-2026-08-24" / "audits" / "current-config.json"
FACES = ("front", "rear", "left", "right", "top", "bottom")
MODELS = {
    "standard": MODEL / "Huawei-RH2288V3-2.5inch.glb",
    "web": MODEL / "Huawei-RH2288V3-2.5inch-web.glb",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check(condition: bool, message: str, errors: list[str]) -> None:
    if not condition:
        errors.append(message)


def determinant3(flat: list[float]) -> float:
    # glTF stores matrices column-major.
    m = [[flat[col * 4 + row] for col in range(4)] for row in range(4)]
    a, b, c = m[0][:3]
    d, e, f = m[1][:3]
    g, h, i = m[2][:3]
    return a * (e * i - f * h) - b * (d * i - f * g) + c * (d * h - e * g)


def glb_header(path: Path) -> dict:
    payload = path.read_bytes()
    magic, version, declared = struct.unpack_from("<4sII", payload, 0)
    return {
        "magic": magic.decode("ascii", "replace"),
        "version": version,
        "declared_length": declared,
        "actual_length": len(payload),
    }


def node_bounds(gltf: GLTF2, node_name: str) -> list[list[float]] | None:
    node = next((node for node in gltf.nodes if node.name == node_name), None)
    if node is None or node.mesh is None:
        return None
    mins: list[list[float]] = []
    maxs: list[list[float]] = []
    for primitive in gltf.meshes[node.mesh].primitives:
        accessor_index = primitive.attributes.POSITION
        accessor = gltf.accessors[accessor_index]
        if accessor.min is None or accessor.max is None:
            return None
        mins.append(list(accessor.min))
        maxs.append(list(accessor.max))
    return [
        [min(values[index] for values in mins) for index in range(3)],
        [max(values[index] for values in maxs) for index in range(3)],
    ]


def prefix_bounds(gltf: GLTF2, prefix: str) -> list[list[float]] | None:
    bounds = [node_bounds(gltf, node.name or "") for node in gltf.nodes if (node.name or "").startswith(prefix)]
    bounds = [item for item in bounds if item is not None]
    if not bounds:
        return None
    return [
        [min(item[0][axis] for item in bounds) for axis in range(3)],
        [max(item[1][axis] for item in bounds) for axis in range(3)],
    ]


def center(bounds: list[list[float]]) -> list[float]:
    return [(bounds[0][axis] + bounds[1][axis]) / 2 for axis in range(3)]


def embedded_face(gltf: GLTF2, face: str) -> Image.Image:
    material_index = next(
        index for index, material in enumerate(gltf.materials)
        if (material.name or "").startswith(face.upper() + " ")
    )
    material = gltf.materials[material_index]
    texture_index = material.pbrMetallicRoughness.baseColorTexture.index
    image_index = gltf.textures[texture_index].source
    image_def = gltf.images[image_index]
    view = gltf.bufferViews[image_def.bufferView]
    blob = gltf.binary_blob()
    offset = view.byteOffset or 0
    return Image.open(BytesIO(blob[offset:offset + view.byteLength])).convert("RGB")


def expected_face(face: str, max_edge: int) -> Image.Image:
    source = Image.open(VIEWS / f"{face}.png").convert("RGBA")
    bbox = source.getchannel("A").getbbox()
    if bbox is None:
        raise RuntimeError(f"{face} has no visible content")
    image = source.crop(bbox).convert("RGB")
    if max(image.size) > max_edge:
        scale = max_edge / max(image.size)
        image = image.resize(
            (round(image.width * scale), round(image.height * scale)),
            Image.Resampling.LANCZOS,
        )
    return image


def audit_model(label: str, path: Path) -> tuple[dict, GLTF2]:
    errors: list[str] = []
    check(path.is_file(), "current GLB is missing", errors)
    check(path.stat().st_size > 1_000_000, "GLB is suspiciously small/placeholder-like", errors)
    header = glb_header(path)
    check(header["magic"] == "glTF", "invalid GLB magic", errors)
    check(header["version"] == 2, "GLB version is not 2", errors)
    check(header["declared_length"] == header["actual_length"], "GLB declared length mismatch", errors)

    gltf = GLTF2().load(path)
    names = [node.name or "" for node in gltf.nodes]
    bay_indices = sorted({
        int(match.group(1)) for name in names
        if (match := re.match(r"FRONT_Drive_Carrier_(\d\d)_", name))
    })
    psu_indices = sorted({
        int(match.group(1)) for name in names
        if (match := re.match(r"REAR_AC_PSU_(\d)_", name))
    })
    rear_drives = [name for name in names if name.startswith("REAR_Drive_")]
    dc_nodes = [name for name in names if "DC_PSU" in name.upper() or "PSU_DC" in name.upper()]
    fan_nodes = [name for name in names if "Fan" in name]
    mirrored_names = [name for name in names if "mirror" in name.lower()]
    negative_nodes = []
    for node in gltf.nodes:
        if node.scale is not None and node.scale[0] * node.scale[1] * node.scale[2] < 0:
            negative_nodes.append(node.name or "")
        if node.matrix is not None and determinant3(node.matrix) < 0:
            negative_nodes.append(node.name or "")

    check(len(gltf.nodes) == 453, f"expected 453 nodes, found {len(gltf.nodes)}", errors)
    check(len(gltf.meshes) == 453, f"expected 453 meshes, found {len(gltf.meshes)}", errors)
    check(bay_indices == list(range(24)), f"front bay indices are {bay_indices}", errors)
    check(psu_indices == [0, 1], f"AC PSU groups are {psu_indices}", errors)
    check(not rear_drives, f"rear-drive nodes found: {rear_drives}", errors)
    check(not dc_nodes, f"DC PSU nodes found: {dc_nodes}", errors)
    check(fan_nodes == ["REAR_AC_PSU_0_Fan", "REAR_AC_PSU_1_Fan"], f"unexpected exterior fan nodes: {fan_nodes}", errors)
    check(not mirrored_names, f"mirror-named nodes found: {mirrored_names}", errors)
    check(not negative_nodes, f"negative/mirrored transforms found: {negative_nodes}", errors)

    required_names = {
        "Closed_Chassis_Sheet_Metal_447x708x86.1mm",
        "Texture_FRONT_24SFF_and_Ears",
        "Texture_REAR_Corrected_No_Rear_Drives",
        "Texture_LEFT_Independent",
        "Texture_RIGHT_Independent",
        "Texture_TOP_Cover",
        "Texture_BOTTOM_Generic_Fallback",
        "FRONT_Left_USB_2_0",
        *(f"FRONT_Left_Ethernet_Indicator_{index}" for index in range(1, 5)),
        "FRONT_Right_Fault_Diagnostic_Display",
        "FRONT_Right_Health_Control",
        "FRONT_Right_UID_Control",
        "FRONT_Right_Power_Control",
        "FRONT_Right_NMI_Control",
        "FRONT_Right_VGA_Relief",
        "REAR_Flexible_NIC_RJ45_A1",
        "REAR_Flexible_NIC_RJ45_A2",
        "REAR_Mgmt_RJ45",
        "REAR_LAN_RJ45",
        "REAR_VGA",
        "REAR_DB9_Serial",
    }
    missing_names = sorted(required_names - set(names))
    check(not missing_names, f"required nodes missing: {missing_names}", errors)

    psu_bounds = [prefix_bounds(gltf, f"REAR_AC_PSU_{index}_") for index in (0, 1)]
    check(all(item is not None for item in psu_bounds), "cannot compute PSU bounds", errors)
    psu_centers = [center(item) for item in psu_bounds if item is not None]
    if len(psu_centers) == 2:
        check(abs(psu_centers[0][0] - psu_centers[1][0]) < 1e-6, "PSUs are not stacked at the same X", errors)
        check(abs(psu_centers[0][1] - psu_centers[1][1]) > 0.035, "PSUs are not vertically separated", errors)
        check(psu_centers[0][2] < -0.35 and psu_centers[1][2] < -0.35, "PSUs are not on the rear plane", errors)

    texture_matches: dict[str, dict] = {}
    max_edge = 4096 if label == "standard" else 2048
    for face in FACES:
        embedded = embedded_face(gltf, face)
        expected = expected_face(face, max_edge)
        difference = ImageChops.difference(embedded, expected)
        matches = embedded.size == expected.size and difference.getbbox() is None
        texture_matches[face] = {
            "embedded_size": list(embedded.size),
            "expected_size": list(expected.size),
            "pixel_exact_match_to_current_view": matches,
        }
        check(matches, f"{face} embedded texture does not match current view pixels", errors)

    face_materials = {}
    for face in FACES:
        material = next(material for material in gltf.materials if (material.name or "").startswith(face.upper() + " "))
        pbr = material.pbrMetallicRoughness
        state = {
            "name": material.name,
            "alphaMode": material.alphaMode,
            "doubleSided": material.doubleSided,
            "baseColorFactor": pbr.baseColorFactor,
            "metallicFactor": pbr.metallicFactor,
        }
        face_materials[face] = state
        check(material.alphaMode == "OPAQUE", f"{face} material is not OPAQUE", errors)
        check(material.doubleSided is not True, f"{face} material is double-sided", errors)
        check(pbr.baseColorFactor == [1.0, 1.0, 1.0, 1.0], f"{face} baseColorFactor is not neutral", errors)
        check(pbr.metallicFactor == 0.0, f"{face} photo material is metallic", errors)

    check(all(buffer.uri is None for buffer in gltf.buffers), "external buffer URI found", errors)
    check(all(image.uri is None for image in gltf.images), "external image URI found", errors)

    result = {
        "path": str(path.relative_to(ROOT)),
        "bytes": path.stat().st_size,
        "sha256": sha256(path),
        "header": header,
        "counts": {
            "nodes": len(gltf.nodes),
            "meshes": len(gltf.meshes),
            "materials": len(gltf.materials),
            "textures": len(gltf.textures),
            "images": len(gltf.images),
        },
        "front_bay_indices": bay_indices,
        "ac_psu_indices": psu_indices,
        "psu_centers_m": psu_centers,
        "rear_drive_nodes": rear_drives,
        "dc_psu_nodes": dc_nodes,
        "exterior_fan_nodes": fan_nodes,
        "texture_matches": texture_matches,
        "face_materials": face_materials,
        "errors": errors,
        "status": "PASS" if not errors else "FAIL",
    }
    return result, gltf


def audit_source_locks() -> dict:
    errors: list[str] = []
    allowed = {
        "front": "SOURCE_LOCKED_GENERATION",
        "rear": "SOURCE_LOCKED_GENERATION",
        "left": "MULTI_REFERENCE_RECONSTRUCTION",
        "right": "MULTI_REFERENCE_RECONSTRUCTION",
        "top": "SOURCE_LOCKED_GENERATION",
        "bottom": "GENERIC_BOTTOM_FALLBACK",
    }
    rows = list(csv.DictReader((ROOT / "source" / "face-source-lock.csv").open(encoding="utf-8", newline="")))
    by_face = {row["face"]: row for row in rows}
    check(set(by_face) == set(FACES), f"source-lock faces are {sorted(by_face)}", errors)
    for face, expected_mode in allowed.items():
        row = by_face.get(face)
        if row is None:
            continue
        check(row["production_mode"] == expected_mode, f"{face} mode is {row['production_mode']}", errors)
        output = ROOT / row["final_output_path"]
        check(output.is_file(), f"{face} final output missing", errors)
        if output.is_file():
            check(sha256(output) == row["final_sha256"], f"{face} final hash mismatch", errors)
        if face != "bottom":
            source = ROOT / row["primary_source_path"]
            check(source.is_file(), f"{face} primary source missing", errors)
            if source.is_file():
                check(sha256(source) == row["primary_sha256"], f"{face} primary source hash mismatch", errors)
            check(row["visual_origin"] in {"real-photograph", "official-photograph"}, f"{face} primary visual origin is {row['visual_origin']}", errors)
    check(by_face.get("left", {}).get("final_sha256") != by_face.get("right", {}).get("final_sha256"), "left and right final images have identical hashes", errors)
    check("qgserver-rh2288v3-6.jpg" not in by_face.get("rear", {}).get("supporting_source_paths", ""), "conflicting QGServer rear remains a support source", errors)
    return {
        "allowed_modes": allowed,
        "rows": rows,
        "errors": errors,
        "status": "PASS" if not errors else "FAIL",
    }


def main() -> None:
    models = {}
    gltfs = {}
    for label, path in MODELS.items():
        models[label], gltfs[label] = audit_model(label, path)

    cross_errors: list[str] = []
    standard_names = [node.name or "" for node in gltfs["standard"].nodes]
    web_names = [node.name or "" for node in gltfs["web"].nodes]
    check(standard_names == web_names, "standard/web node order or names differ", cross_errors)
    if standard_names == web_names:
        for name in standard_names:
            check(node_bounds(gltfs["standard"], name) == node_bounds(gltfs["web"], name), f"standard/web bounds differ for {name}", cross_errors)

    source_locks = audit_source_locks()
    result = {
        "identity": "Huawei FusionServer RH2288 V3 / H22M-03 / 24x2.5-inch SFF / no rear drives / dual stacked AC PSU",
        "models": models,
        "standard_web_geometry": {
            "errors": cross_errors,
            "status": "PASS" if not cross_errors else "FAIL",
        },
        "source_locks": source_locks,
    }
    result["status"] = "PASS" if (
        all(item["status"] == "PASS" for item in models.values())
        and not cross_errors
        and source_locks["status"] == "PASS"
    ) else "FAIL"
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(result["status"], OUT)
    if result["status"] != "PASS":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
