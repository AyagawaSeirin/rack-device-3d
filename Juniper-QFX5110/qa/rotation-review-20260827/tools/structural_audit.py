#!/usr/bin/env python3
"""Rotation-risk structural audit for a self-contained GLB.

This supplements the skill audit with exact/near-coplanar geometry, embedded
image alpha, sampler wrap, negative-transform, and closed-core checks.
"""

from __future__ import annotations

import argparse
from collections import defaultdict
from io import BytesIO
import json
from pathlib import Path

import numpy as np
from PIL import Image
from pygltflib import GLTF2
import trimesh


CLAMP_TO_EDGE = 33071
COPLANAR_LIMIT_M = 0.00025
RISK_GAP_M = 0.00005
EXACT_M = 0.0000001


def embedded_image(gltf: GLTF2, index: int) -> Image.Image:
    image = gltf.images[index]
    if image.bufferView is None:
        raise ValueError(f"image {index} is not embedded in a bufferView")
    view = gltf.bufferViews[image.bufferView]
    blob = gltf.binary_blob()
    start = (view.byteOffset or 0)
    return Image.open(BytesIO(blob[start:start + view.byteLength])).copy()


def world_meshes(path: Path):
    scene = trimesh.load(path, force="scene", process=False)
    records = []
    for node in scene.graph.nodes_geometry:
        transform, geometry_name = scene.graph[node]
        mesh = scene.geometry[geometry_name].copy()
        mesh.apply_transform(transform)
        records.append((str(node), mesh, np.asarray(transform, dtype=float)))
    return scene, records


def texture_material(material) -> bool:
    pbr = material.pbrMetallicRoughness
    return bool(pbr and pbr.baseColorTexture is not None)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("glb", type=Path)
    parser.add_argument("--json-out", type=Path, required=True)
    args = parser.parse_args()

    gltf = GLTF2().load(str(args.glb))
    scene, meshes = world_meshes(args.glb)

    material_violations = []
    textured_materials = []
    for index, material in enumerate(gltf.materials or []):
        if not texture_material(material):
            continue
        pbr = material.pbrMetallicRoughness
        factor = list(pbr.baseColorFactor or [1, 1, 1, 1])
        entry = {
            "index": index,
            "name": material.name,
            "alphaMode": material.alphaMode or "OPAQUE",
            "baseColorFactor": factor,
            "doubleSided": bool(material.doubleSided),
            "unlit": "KHR_materials_unlit" in (material.extensions or {}),
        }
        textured_materials.append(entry)
        if entry["alphaMode"] != "OPAQUE" or factor != [1.0, 1.0, 1.0, 1.0] or entry["doubleSided"]:
            material_violations.append(entry)

    image_alpha = []
    image_errors = []
    for index in range(len(gltf.images or [])):
        try:
            image = embedded_image(gltf, index)
            if "A" in image.getbands():
                alpha = np.asarray(image.getchannel("A"), dtype=np.uint8)
                below_255 = int(np.count_nonzero(alpha < 255))
                below_250 = int(np.count_nonzero(alpha < 250))
            else:
                below_255 = below_250 = 0
            image_alpha.append({
                "index": index,
                "mode": image.mode,
                "size": list(image.size),
                "alpha_below_255_pixels": below_255,
                "alpha_below_250_pixels": below_250,
            })
        except Exception as exc:
            image_errors.append({"index": index, "error": str(exc)})

    sampler_violations = []
    samplers = []
    for index, sampler in enumerate(gltf.samplers or []):
        entry = {"index": index, "wrapS": sampler.wrapS or 10497, "wrapT": sampler.wrapT or 10497}
        samplers.append(entry)
        if entry["wrapS"] != CLAMP_TO_EDGE or entry["wrapT"] != CLAMP_TO_EDGE:
            sampler_violations.append(entry)
    for index, texture in enumerate(gltf.textures or []):
        if texture.sampler is None or texture.sampler >= len(samplers):
            sampler_violations.append({"texture": index, "sampler": texture.sampler, "reason": "default REPEAT"})

    negative_transforms = []
    exact_triangle_map = defaultdict(list)
    degenerate = []
    plane_records = {0: [], 1: [], 2: []}
    triangle_count = 0
    for node, mesh, transform in meshes:
        determinant = float(np.linalg.det(transform[:3, :3]))
        if determinant < 0:
            negative_transforms.append({"node": node, "determinant": determinant})
        triangles = np.asarray(mesh.triangles, dtype=float)
        for face_index, tri in enumerate(triangles):
            triangle_count += 1
            cross = np.cross(tri[1] - tri[0], tri[2] - tri[0])
            norm = float(np.linalg.norm(cross))
            if norm < 1e-14:
                degenerate.append({"node": node, "face": face_index})
                continue
            unit = cross / norm
            canonical = tuple(sorted(tuple(float(v) for v in row) for row in np.round(tri, 7)))
            exact_triangle_map[canonical].append({"node": node, "face": face_index, "normal": unit.tolist()})
            axis = int(np.argmax(np.abs(unit)))
            if abs(unit[axis]) < 0.9999:
                continue
            other = [value for value in (0, 1, 2) if value != axis]
            lo = np.min(tri[:, other], axis=0)
            hi = np.max(tri[:, other], axis=0)
            plane_records[axis].append({
                "node": node,
                "face": face_index,
                "coord": float(np.mean(tri[:, axis])),
                "lo": lo,
                "hi": hi,
            })

    exact_duplicates = []
    opposite_duplicates = []
    for occurrences in exact_triangle_map.values():
        if len(occurrences) < 2:
            continue
        exact_duplicates.append(occurrences)
        for left in range(len(occurrences)):
            for right in range(left + 1, len(occurrences)):
                if np.dot(occurrences[left]["normal"], occurrences[right]["normal"]) < -0.9999:
                    opposite_duplicates.append([occurrences[left], occurrences[right]])

    pair_stats = {}
    for axis, records in plane_records.items():
        records.sort(key=lambda item: item["coord"])
        for left_index, left in enumerate(records):
            right_index = left_index + 1
            while right_index < len(records):
                right = records[right_index]
                gap = right["coord"] - left["coord"]
                if gap > COPLANAR_LIMIT_M:
                    break
                right_index += 1
                if left["node"] == right["node"]:
                    continue
                overlap = np.minimum(left["hi"], right["hi"]) - np.maximum(left["lo"], right["lo"])
                if np.any(overlap <= 1e-9):
                    continue
                area = float(overlap[0] * overlap[1])
                key = (left["node"], right["node"], axis, round(gap, 8))
                stat = pair_stats.setdefault(key, {"node_a": left["node"], "node_b": right["node"], "axis": axis, "gap_mm": gap * 1000, "overlap_area_m2": 0.0, "triangle_pairs": 0})
                stat["overlap_area_m2"] += area
                stat["triangle_pairs"] += 1

    coplanar_pairs = sorted(pair_stats.values(), key=lambda item: (item["gap_mm"], -item["overlap_area_m2"]))
    visible_words = ("texture", "face_", "source-locked", "reconstructed", "fallback")
    unresolved_coplanar = [
        pair for pair in coplanar_pairs
        if pair["gap_mm"] < RISK_GAP_M * 1000
        and pair["overlap_area_m2"] > 1e-8
        and any(word in (pair["node_a"] + " " + pair["node_b"]).lower() for word in visible_words)
    ]

    closed_nodes = []
    for node, mesh, _ in meshes:
        if "closed" not in node.lower() and "chassis core" not in node.lower():
            continue
        # glTF boxes commonly duplicate corner positions so each face can carry
        # a distinct normal/UV. Rebuild from position+index only before testing
        # topological closure; otherwise those valid hard edges look open.
        merged = trimesh.Trimesh(
            vertices=mesh.vertices.copy(),
            faces=mesh.faces.copy(),
            process=True,
        )
        closed_nodes.append({
            "node": node,
            "watertight": bool(merged.is_watertight),
            "winding_consistent": bool(merged.is_winding_consistent),
            "volume_m3": float(merged.volume),
        })
    closed_core_pass = bool(closed_nodes) and any(item["watertight"] and item["winding_consistent"] and item["volume_m3"] > 0 for item in closed_nodes)

    errors = []
    if material_violations:
        errors.append("textured material alpha/factor/double-sided violation")
    if image_errors or any(item["alpha_below_255_pixels"] for item in image_alpha):
        errors.append("embedded base-color image contains alpha below 255 or could not be read")
    if sampler_violations:
        errors.append("texture sampler is not CLAMP_TO_EDGE")
    if negative_transforms:
        errors.append("negative/mirrored transform")
    if exact_duplicates:
        errors.append("exact duplicate triangle")
    if opposite_duplicates:
        errors.append("opposite-facing duplicate triangle")
    if degenerate:
        errors.append("degenerate triangle")
    if unresolved_coplanar:
        errors.append("visible texture geometry has coplanar/near-coplanar overlap below 0.05 mm")
    if not closed_core_pass:
        errors.append("no positive-volume watertight closed core")

    report = {
        "schema": "rotation-risk-structural-audit-v1",
        "path": str(args.glb),
        "byte_size": args.glb.stat().st_size,
        "triangle_count": triangle_count,
        "node_geometry_count": len(meshes),
        "textured_materials": textured_materials,
        "material_violations": material_violations,
        "embedded_image_alpha": image_alpha,
        "image_errors": image_errors,
        "samplers": samplers,
        "sampler_violations": sampler_violations,
        "negative_transforms": negative_transforms,
        "degenerate_triangles": degenerate,
        "exact_duplicate_triangle_groups": exact_duplicates,
        "opposite_duplicate_triangle_pairs": opposite_duplicates,
        "coplanar_or_near_pairs_within_0_25mm": coplanar_pairs[:250],
        "unresolved_visible_coplanar_pairs_below_0_05mm": unresolved_coplanar,
        "closed_core_nodes": closed_nodes,
        "closed_core_pass": closed_core_pass,
        "errors": errors,
        "error_count": len(errors),
        "status": "PASS" if not errors else "REWORK",
    }
    args.json_out.parent.mkdir(parents=True, exist_ok=True)
    args.json_out.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps({"status": report["status"], "errors": errors, "triangles": triangle_count, "coplanar_pairs": len(coplanar_pairs)}, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
