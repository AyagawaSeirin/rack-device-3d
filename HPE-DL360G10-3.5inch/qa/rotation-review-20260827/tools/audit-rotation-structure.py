#!/usr/bin/env python3
"""Rotation-stability structural checks not covered by the baseline GLB audit."""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import defaultdict
from pathlib import Path

import numpy as np
import trimesh
from pygltflib import GLTF2


TOL = 1e-7


def world_meshes(path: Path):
    scene = trimesh.load(path, force="scene", process=False)
    result = []
    for node_name in scene.graph.nodes_geometry:
        transform, geometry_name = scene.graph[node_name]
        mesh = scene.geometry[geometry_name].copy()
        mesh.apply_transform(transform)
        result.append((str(node_name), mesh))
    return result


def triangle_key(triangle: np.ndarray) -> tuple:
    points = sorted(tuple(np.round(point, 7)) for point in triangle)
    return tuple(points)


def axis_surfaces(meshes):
    grouped = defaultdict(dict)
    for node_name, mesh in meshes:
        triangles = np.asarray(mesh.triangles)
        for triangle in triangles:
            spans = np.ptp(triangle, axis=0)
            axis_candidates = np.where(spans <= TOL)[0]
            if not len(axis_candidates):
                continue
            axis = int(axis_candidates[0])
            coord = round(float(np.mean(triangle[:, axis])), 7)
            uv_axes = [value for value in range(3) if value != axis]
            rect = [
                float(np.min(triangle[:, uv_axes[0]])),
                float(np.max(triangle[:, uv_axes[0]])),
                float(np.min(triangle[:, uv_axes[1]])),
                float(np.max(triangle[:, uv_axes[1]])),
            ]
            normal = np.cross(triangle[1] - triangle[0], triangle[2] - triangle[0])
            sign = 1 if normal[axis] >= 0 else -1
            key = (axis, coord)
            existing = grouped[key].get((node_name, sign))
            if existing is None:
                grouped[key][(node_name, sign)] = rect
            else:
                existing[0] = min(existing[0], rect[0])
                existing[1] = max(existing[1], rect[1])
                existing[2] = min(existing[2], rect[2])
                existing[3] = max(existing[3], rect[3])
    return grouped


def overlap_area(a, b):
    width = min(a[1], b[1]) - max(a[0], b[0])
    height = min(a[3], b[3]) - max(a[2], b[2])
    return max(0.0, width) * max(0.0, height)


def material_checks(path: Path):
    document = GLTF2().load_binary(str(path))
    violations = []
    records = []
    for index, material in enumerate(document.materials or []):
        pbr = material.pbrMetallicRoughness
        factor = list(pbr.baseColorFactor or [1, 1, 1, 1]) if pbr else [1, 1, 1, 1]
        textured = bool(pbr and pbr.baseColorTexture is not None)
        record = {
            "index": index,
            "name": material.name,
            "alphaMode": material.alphaMode or "OPAQUE",
            "baseColorFactor": factor,
            "doubleSided": bool(material.doubleSided),
            "textured": textured,
            "unlit": bool(material.extensions and "KHR_materials_unlit" in material.extensions),
        }
        records.append(record)
        if record["alphaMode"] != "OPAQUE":
            violations.append({"material": material.name, "reason": "alphaMode is not OPAQUE"})
        if len(factor) >= 4 and abs(float(factor[3]) - 1.0) > 1e-8:
            violations.append({"material": material.name, "reason": "baseColor alpha is not 1"})
        if record["doubleSided"]:
            violations.append({"material": material.name, "reason": "doubleSided is true"})
        if textured and any(abs(float(factor[i]) - 1.0) > 1e-8 for i in range(4)):
            violations.append({"material": material.name, "reason": "textured baseColorFactor is not [1,1,1,1]"})
    negative = []
    for index, node in enumerate(document.nodes or []):
        if node.matrix:
            determinant = float(np.linalg.det(np.asarray(node.matrix, dtype=float).reshape(4, 4)[:3, :3]))
        else:
            scale = node.scale or [1, 1, 1]
            determinant = float(scale[0] * scale[1] * scale[2])
        if determinant < 0:
            negative.append({"index": index, "name": node.name, "determinant": determinant})
    return records, violations, negative


def audit(path: Path):
    meshes = world_meshes(path)
    global_min = np.min([mesh.bounds[0] for _, mesh in meshes], axis=0)
    global_max = np.max([mesh.bounds[1] for _, mesh in meshes], axis=0)
    occurrences = defaultdict(list)
    open_meshes = []
    core_meshes = []
    for node_name, mesh in meshes:
        if not mesh.is_watertight:
            open_meshes.append(node_name)
        lowered = node_name.lower()
        if any(token in lowered for token in ("closed", "shell", "structuralbody", "chassisstructuralbody")):
            welded = trimesh.Trimesh(vertices=mesh.vertices.copy(), faces=mesh.faces.copy(), process=True)
            core_meshes.append({
                "node": node_name,
                "watertight": bool(welded.is_watertight),
                "windingConsistent": bool(welded.is_winding_consistent),
                "volume": float(welded.volume),
            })
        for triangle in np.asarray(mesh.triangles):
            normal = np.cross(triangle[1] - triangle[0], triangle[2] - triangle[0])
            norm = np.linalg.norm(normal)
            if norm:
                normal = normal / norm
            occurrences[triangle_key(triangle)].append((node_name, normal.tolist()))

    exact_same_facing = []
    exact_reverse = []
    for values in occurrences.values():
        if len(values) < 2:
            continue
        for left in range(len(values)):
            for right in range(left + 1, len(values)):
                first, second = values[left], values[right]
                if first[0] == second[0]:
                    continue
                dot = float(np.dot(first[1], second[1]))
                target = exact_same_facing if dot > 0.999 else exact_reverse
                if len(target) < 250:
                    target.append({"nodes": [first[0], second[0]], "normalDot": dot})

    same_facing_coplanar = defaultdict(float)
    opposite_facing_contacts = defaultdict(float)
    for (axis, coord), entries in axis_surfaces(meshes).items():
        items = [(node, sign, rect) for (node, sign), rect in entries.items()]
        for left in range(len(items)):
            for right in range(left + 1, len(items)):
                node_a, sign_a, rect_a = items[left]
                node_b, sign_b, rect_b = items[right]
                if node_a == node_b:
                    continue
                area = overlap_area(rect_a, rect_b)
                if area <= 1e-10:
                    continue
                pair = tuple(sorted((node_a, node_b))) + (axis, coord)
                target = same_facing_coplanar if sign_a == sign_b else opposite_facing_contacts
                target[pair] += area

    same_records = [
        {"nodes": [key[0], key[1]], "axis": key[2], "plane": key[3], "projectedOverlapArea": area,
         "exteriorRisk": bool(abs(key[3] - global_min[key[2]]) <= 2e-7 or abs(key[3] - global_max[key[2]]) <= 2e-7 or any(token in (key[0] + key[1]).lower() for token in ("appearance", "canonical", "source", "approved_imagegen")))}
        for key, area in sorted(same_facing_coplanar.items(), key=lambda value: value[1], reverse=True)
    ]
    exterior_same_records = [record for record in same_records if record["exteriorRisk"]]
    opposite_records = [
        {"nodes": [key[0], key[1]], "axis": key[2], "plane": key[3], "projectedContactArea": area}
        for key, area in sorted(opposite_facing_contacts.items(), key=lambda value: value[1], reverse=True)
    ]
    materials, material_violations, negative = material_checks(path)
    core_errors = [record for record in core_meshes if not record["watertight"] or not record["windingConsistent"] or record["volume"] <= 0]
    errors = []
    if material_violations:
        errors.append("material-alpha/sidedness violation")
    if negative:
        errors.append("negative or mirrored node transform")
    if exact_same_facing:
        errors.append("exact same-facing duplicate triangles")
    if exterior_same_records:
        errors.append("exterior same-facing coplanar overlap")
    if not core_meshes or core_errors:
        errors.append("closed-core check failed")
    data = path.read_bytes()
    return {
        "path": str(path),
        "bytes": len(data),
        "sha256": hashlib.sha256(data).hexdigest(),
        "meshCount": len(meshes),
        "materialAlpha": {"materials": materials, "violations": material_violations},
        "negativeTransforms": negative,
        "duplicates": {"sameFacingExact": exact_same_facing, "reverseExact": exact_reverse},
        "coplanar": {"sameFacingOverlaps": same_records[:500], "exteriorSameFacingOverlaps": exterior_same_records[:500], "oppositeFacingContacts": opposite_records[:500]},
        "closedCore": {"candidates": core_meshes, "errors": core_errors},
        "openMeshes": open_meshes,
        "errors": errors,
        "errorCount": len(errors),
        "status": "PASS" if not errors else "REWORK",
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("glb", type=Path)
    parser.add_argument("--json-out", type=Path, required=True)
    args = parser.parse_args()
    result = audit(args.glb)
    args.json_out.parent.mkdir(parents=True, exist_ok=True)
    args.json_out.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({key: result[key] for key in ("path", "status", "errorCount", "errors")}, indent=2))


if __name__ == "__main__":
    main()
