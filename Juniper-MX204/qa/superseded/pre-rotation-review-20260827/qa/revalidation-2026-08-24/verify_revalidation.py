#!/usr/bin/env python3
"""Verify current MX204 face lineage and both GLB payloads from file bytes."""

from __future__ import annotations

import csv
from hashlib import sha256
from io import BytesIO
import json
from pathlib import Path
import struct

import numpy as np
from PIL import Image


ROOT = Path(__file__).resolve().parents[2]
FACES = ("front", "rear", "left", "right", "top", "bottom")


def digest(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def rgba(path_or_bytes) -> Image.Image:
    if isinstance(path_or_bytes, (str, Path)):
        return Image.open(path_or_bytes).convert("RGBA")
    return Image.open(BytesIO(path_or_bytes)).convert("RGBA")


def pixel_sha(image: Image.Image) -> str:
    return sha256(image.convert("RGBA").tobytes()).hexdigest()


def parse_glb(path: Path) -> tuple[dict, bytes, int]:
    payload = path.read_bytes()
    magic, version, declared_length = struct.unpack_from("<4sII", payload, 0)
    if magic != b"glTF" or version != 2 or declared_length != len(payload):
        raise ValueError(f"invalid GLB header: {path}")
    offset = 12
    chunks = []
    while offset < len(payload):
        length, kind = struct.unpack_from("<II", payload, offset)
        offset += 8
        chunks.append((kind, payload[offset:offset + length]))
        offset += length
    json_chunk = next(data for kind, data in chunks if kind == 0x4E4F534A)
    bin_chunk = next(data for kind, data in chunks if kind == 0x004E4942)
    return json.loads(json_chunk.decode("utf-8").rstrip(" \t\r\n\0")), bin_chunk, declared_length


def embedded_face_images(doc: dict, binary: bytes) -> dict[str, bytes]:
    result = {}
    for material in doc.get("materials", []):
        name = material.get("name", "")
        face = next((candidate for candidate in FACES if name.startswith(candidate.upper())), None)
        texture_info = material.get("pbrMetallicRoughness", {}).get("baseColorTexture")
        if face is None or texture_info is None:
            continue
        texture = doc["textures"][texture_info["index"]]
        image = doc["images"][texture["source"]]
        view = doc["bufferViews"][image["bufferView"]]
        start = view.get("byteOffset", 0)
        result[face] = binary[start:start + view["byteLength"]]
    return result


def component_counts(node_names: list[str]) -> dict[str, int]:
    tests = {
        "front_qsfp_ports": lambda n: n.startswith("FRONT_QSFP28_Port_"),
        "front_sfp_ports": lambda n: n.startswith("FRONT_SFPplus_Port_"),
        "rear_fan_housings": lambda n: n.startswith("REAR_Fan_Module_") and n.endswith("_Housing"),
        "rear_fan_handles": lambda n: n.startswith("REAR_Fan_") and n.endswith("_Rounded_Orange_Handle_Frame"),
        "rear_ac_psu_housings": lambda n: n.startswith("REAR_AC_PSU_") and n.endswith("_Housing"),
        "rear_iec_c14_inlets": lambda n: n.startswith("REAR_AC_PSU_") and n.endswith("_IEC_C14_Inlet"),
        "left_rail_sections": lambda n: n.startswith("LEFT_Rail_Section_") and n.endswith("_Top"),
        "right_rail_sections": lambda n: n.startswith("RIGHT_Rail_Section_") and n.endswith("_Top"),
        "top_cover_screws": lambda n: n.startswith("TOP_Cover_Screw_"),
    }
    return {key: sum(predicate(name) for name in node_names) for key, predicate in tests.items()}


def inspect_glb(path: Path, web: bool) -> dict:
    doc, binary, declared_length = parse_glb(path)
    embedded = embedded_face_images(doc, binary)
    face_results = {}
    for face in FACES:
        view_image = rgba(ROOT / "views" / f"{face}.png")
        actual = rgba(embedded[face])
        if web:
            scale = 2048 / max(view_image.size)
            expected = view_image.resize(
                (max(1, round(view_image.width * scale)), max(1, round(view_image.height * scale))),
                Image.Resampling.LANCZOS,
            ) if max(view_image.size) > 2048 else view_image
        else:
            expected = view_image
        face_results[face] = {
            "embedded_png_sha256": sha256(embedded[face]).hexdigest(),
            "embedded_size_px": list(actual.size),
            "embedded_pixel_sha256": pixel_sha(actual),
            "expected_pixel_sha256": pixel_sha(expected),
            "pixel_match": actual.size == expected.size and actual.tobytes() == expected.tobytes(),
        }
    node_names = [node.get("name", "") for node in doc.get("nodes", [])]
    return {
        "path": str(path),
        "byte_size": path.stat().st_size,
        "sha256": digest(path),
        "declared_length": declared_length,
        "counts": {
            "scenes": len(doc.get("scenes", [])),
            "nodes": len(doc.get("nodes", [])),
            "meshes": len(doc.get("meshes", [])),
            "materials": len(doc.get("materials", [])),
            "textures": len(doc.get("textures", [])),
            "images": len(doc.get("images", [])),
        },
        "external_buffer_uris": [b["uri"] for b in doc.get("buffers", []) if "uri" in b],
        "external_image_uris": [i["uri"] for i in doc.get("images", []) if "uri" in i],
        "component_counts": component_counts(node_names),
        "node_names_sha256": sha256("\n".join(node_names).encode()).hexdigest(),
        "face_images": face_results,
    }


def main() -> None:
    locks = list(csv.DictReader((ROOT / "source" / "face-source-lock.csv").open(newline="")))
    lock_results = {}
    for row in locks:
        source_path = ROOT / row["primary_source_path"]
        output_path = ROOT / row["final_output_path"]
        lock_results[row["face"]] = {
            "production_mode": row["production_mode"],
            "primary_source_path": row["primary_source_path"],
            "primary_source_declared_sha256": row["sha256"],
            "primary_source_actual_sha256": digest(source_path),
            "primary_source_hash_match": digest(source_path) == row["sha256"],
            "final_output_path": row["final_output_path"],
            "final_output_sha256": digest(output_path),
        }

    left = np.asarray(rgba(ROOT / "views" / "left.png"), dtype=np.float32)
    right_flipped = np.asarray(rgba(ROOT / "views" / "right.png").transpose(Image.Transpose.FLIP_LEFT_RIGHT), dtype=np.float32)
    mask = (left[:, :, 3] > 16) | (right_flipped[:, :, 3] > 16)
    left_values = left[:, :, :3][mask].reshape(-1)
    right_values = right_flipped[:, :, :3][mask].reshape(-1)
    correlation = float(np.corrcoef(left_values, right_values)[0, 1])
    rmse = float(np.sqrt(np.mean((left_values - right_values) ** 2)))

    standard = inspect_glb(ROOT / "model" / "Juniper-MX204.glb", web=False)
    web = inspect_glb(ROOT / "model" / "Juniper-MX204-web.glb", web=True)
    expected_components = {
        "front_qsfp_ports": 4,
        "front_sfp_ports": 8,
        "rear_fan_housings": 3,
        "rear_fan_handles": 3,
        "rear_ac_psu_housings": 2,
        "rear_iec_c14_inlets": 2,
        "left_rail_sections": 3,
        "right_rail_sections": 3,
        "top_cover_screws": 26,
    }
    checks = {
        "six_face_locks_present": set(lock_results) == set(FACES),
        "all_primary_source_hashes_match": all(item["primary_source_hash_match"] for item in lock_results.values()),
        "left_right_primary_sources_independent": lock_results["left"]["primary_source_actual_sha256"] != lock_results["right"]["primary_source_actual_sha256"],
        "left_right_final_not_mirrored": correlation < 0.95,
        "standard_embeds_current_view_pixels": all(item["pixel_match"] for item in standard["face_images"].values()),
        "web_embeds_expected_downscaled_current_pixels": all(item["pixel_match"] for item in web["face_images"].values()),
        "same_external_geometry_names": standard["node_names_sha256"] == web["node_names_sha256"],
        "standard_components_exact": standard["component_counts"] == expected_components,
        "web_components_exact": web["component_counts"] == expected_components,
        "both_self_contained": not standard["external_buffer_uris"] and not standard["external_image_uris"] and not web["external_buffer_uris"] and not web["external_image_uris"],
    }
    report = {
        "status": "PASS" if all(checks.values()) else "FAIL",
        "checks": checks,
        "face_source_locks": lock_results,
        "left_right_independence": {
            "comparison": "views/left.png versus horizontal flip of views/right.png, opaque-union RGB pixels",
            "pearson_correlation": round(correlation, 6),
            "rmse_0_to_255": round(rmse, 6),
            "old_pre_revalidation_imagemagick_ncc": 0.999204,
            "conclusion": "independent, not mirrored" if correlation < 0.95 else "mirrored/suspicious",
        },
        "expected_component_counts": expected_components,
        "standard_glb": standard,
        "web_glb": web,
    }
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
