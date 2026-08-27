#!/usr/bin/env python3
"""Rotation-focused GLB structural checks used by the 2026-08-27 review."""

from __future__ import annotations

import argparse
import io
import json
from collections import defaultdict
from pathlib import Path

import numpy as np
from PIL import Image
from pygltflib import GLTF2
import trimesh


def node_matrix(node) -> np.ndarray:
    if node.matrix:
        return np.asarray(node.matrix, dtype=float).reshape((4, 4), order="F")
    result = np.eye(4)
    if node.translation:
        result[:3, 3] = node.translation
    if node.rotation:
        x, y, z, w = node.rotation
        result[:3, :3] = trimesh.transformations.quaternion_matrix([w, x, y, z])[:3, :3]
    if node.scale:
        result[:3, :3] = result[:3, :3] @ np.diag(node.scale)
    return result


def image_alpha(document: GLTF2) -> list[dict]:
    blob = document.binary_blob() or b""
    rows = []
    for index, image_def in enumerate(document.images or []):
        data = None
        if image_def.bufferView is not None:
            view = document.bufferViews[image_def.bufferView]
            start = (view.byteOffset or 0)
            data = blob[start:start + view.byteLength]
        if not data:
            rows.append({"index": index, "name": image_def.name, "error": "image bytes unavailable"})
            continue
        with Image.open(io.BytesIO(data)) as image:
            alpha = image.convert("RGBA").getchannel("A")
            values = np.asarray(alpha)
            rows.append({
                "index": index,
                "name": image_def.name,
                "mode": image.mode,
                "size": list(image.size),
                "alpha_below_255": int(np.count_nonzero(values < 255)),
                "alpha_below_250": int(np.count_nonzero(values < 250)),
                "alpha_zero": int(np.count_nonzero(values == 0)),
            })
    return rows


def geometry_checks(path: Path) -> dict:
    scene = trimesh.load(path, force="scene", process=False)
    occurrences: dict[tuple, list[dict]] = defaultdict(list)
    bounds_rows = []
    topology = []
    for node_name in scene.graph.nodes_geometry:
        transform, geometry_name = scene.graph[node_name]
        mesh = scene.geometry[geometry_name]
        world_vertices = trimesh.transform_points(mesh.vertices, transform)
        world_bounds = np.vstack((world_vertices.min(axis=0), world_vertices.max(axis=0)))
        bounds_rows.append({"node": node_name, "geometry": geometry_name, "bounds": world_bounds.tolist(), "planar": bool(np.any(np.ptp(world_vertices, axis=0) < 1e-8))})
        welded = mesh.copy()
        welded.merge_vertices(merge_tex=True, merge_norm=True)
        topology.append({
            "node": node_name,
            "geometry": geometry_name,
            "triangles": int(len(mesh.faces)),
            "watertight": bool(welded.is_watertight),
            "winding_consistent": bool(welded.is_winding_consistent),
            "volume": float(welded.volume) if welded.is_volume else None,
        })
        for face_index, face in enumerate(mesh.faces):
            tri = world_vertices[face]
            key = tuple(sorted(tuple(np.round(vertex, 7)) for vertex in tri))
            normal = np.cross(tri[1] - tri[0], tri[2] - tri[0])
            length = np.linalg.norm(normal)
            if length:
                normal /= length
            occurrences[key].append({"node": node_name, "geometry": geometry_name, "face": face_index, "normal": normal.tolist()})

    duplicate_groups = []
    opposite_groups = []
    for items in occurrences.values():
        if len(items) < 2:
            continue
        compact = [{key: value for key, value in item.items() if key != "normal"} for item in items]
        duplicate_groups.append(compact)
        for left in range(len(items)):
            for right in range(left + 1, len(items)):
                if np.dot(items[left]["normal"], items[right]["normal"]) < -0.999:
                    opposite_groups.append([compact[left], compact[right]])

    surface_pairs = []
    critical_pairs = []
    for left_index, left in enumerate(bounds_rows):
        left_bounds = np.asarray(left["bounds"])
        for right in bounds_rows[left_index + 1:]:
            right_bounds = np.asarray(right["bounds"])
            for axis in range(3):
                projected = [index for index in range(3) if index != axis]
                overlap = np.minimum(left_bounds[1, projected], right_bounds[1, projected]) - np.maximum(left_bounds[0, projected], right_bounds[0, projected])
                if np.any(overlap <= 1e-7):
                    continue
                gaps = [abs(left_bounds[side_a, axis] - right_bounds[side_b, axis]) for side_a in (0, 1) for side_b in (0, 1)]
                gap = min(gaps)
                if gap > 0.00025:
                    continue
                row = {"left": left["node"], "right": right["node"], "axis": "xyz"[axis], "gap_mm": round(gap * 1000, 6), "projected_overlap_mm2": round(float(np.prod(overlap)) * 1_000_000, 6)}
                surface_pairs.append(row)
                names = (left["node"] + " " + right["node"]).lower()
                if any(token in names for token in ("texture_", "appearance", "source-locked", "fallback face", "reconstructed face", "exact source")):
                    critical_pairs.append(row)

    texture_tokens = ("texture_", "appearance", "source-locked", "fallback face", "reconstructed face", "exact source")
    core_tokens = ("chassis", "shell", "structuralbody", "closed_chassis")
    exact_critical = [row for row in critical_pairs if row["gap_mm"] <= 0.001]
    backing_risks = []
    for row in critical_pairs:
        left = row["left"].lower()
        right = row["right"].lower()
        if ((any(token in left for token in texture_tokens) and any(token in right for token in core_tokens))
                or (any(token in right for token in texture_tokens) and any(token in left for token in core_tokens))):
            backing_risks.append(row)
    cores = [row for row in topology if any(token in (row["node"] + " " + row["geometry"]).lower() for token in core_tokens) and row["watertight"]]
    return {
        "scene_geometry_count": len(bounds_rows),
        "triangle_occurrence_count": sum(len(items) for items in occurrences.values()),
        "duplicate_triangle_group_count": len(duplicate_groups),
        "opposite_duplicate_pair_count": len(opposite_groups),
        "duplicate_triangle_groups": duplicate_groups[:100],
        "opposite_duplicate_pairs": opposite_groups[:100],
        "near_or_coplanar_surface_pair_count": len(surface_pairs),
        "critical_textured_surface_pair_count": len(critical_pairs),
        "critical_textured_surface_pairs": critical_pairs[:200],
        "exact_critical_surface_pair_count": len(exact_critical),
        "exact_critical_surface_pairs": exact_critical[:100],
        "textured_card_backing_risk_count": len(backing_risks),
        "textured_card_backing_risks": backing_risks[:100],
        "closed_core_candidates": cores,
        "non_winding_consistent_meshes": [row for row in topology if not row["winding_consistent"]],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("glb", type=Path)
    parser.add_argument("--json-out", required=True, type=Path)
    args = parser.parse_args()
    document = GLTF2().load_binary(str(args.glb))
    parents = {}
    for parent_index, node in enumerate(document.nodes or []):
        for child in node.children or []:
            parents[child] = parent_index
    world_cache = {}
    def world(index: int) -> np.ndarray:
        if index not in world_cache:
            local = node_matrix(document.nodes[index])
            world_cache[index] = world(parents[index]) @ local if index in parents else local
        return world_cache[index]
    transforms = []
    for index, node in enumerate(document.nodes or []):
        determinant = float(np.linalg.det(world(index)[:3, :3]))
        if determinant < 0:
            transforms.append({"index": index, "name": node.name, "world_determinant": determinant})
    materials = []
    for index, material in enumerate(document.materials or []):
        pbr = material.pbrMetallicRoughness
        factor = list(pbr.baseColorFactor or [1, 1, 1, 1]) if pbr else [1, 1, 1, 1]
        materials.append({
            "index": index,
            "name": material.name,
            "alphaMode": material.alphaMode or "OPAQUE",
            "baseColorFactor": factor,
            "doubleSided": bool(material.doubleSided),
            "unlit": bool(material.extensions and "KHR_materials_unlit" in material.extensions),
            "main_surface_violation": bool((material.alphaMode or "OPAQUE") != "OPAQUE" or factor[3] < 1 or material.doubleSided),
        })
    report = {
        "path": str(args.glb),
        "materials": materials,
        "material_violation_count": sum(row["main_surface_violation"] for row in materials),
        "negative_world_transform_count": len(transforms),
        "negative_world_transforms": transforms,
        "embedded_images": image_alpha(document),
        "geometry": geometry_checks(args.glb),
    }
    errors = []
    if report["material_violation_count"]:
        errors.append("non-opaque, partial-alpha, or double-sided material")
    if transforms:
        errors.append("negative world transform")
    if any(row.get("alpha_below_255", 0) for row in report["embedded_images"]):
        errors.append("embedded base-color image contains alpha below 255")
    if report["geometry"]["duplicate_triangle_group_count"]:
        errors.append("duplicate triangles")
    if not report["geometry"]["closed_core_candidates"]:
        errors.append("no watertight closed core candidate")
    report["errors"] = errors
    report["status"] = "PASS" if not errors else "REWORK"
    args.json_out.parent.mkdir(parents=True, exist_ok=True)
    args.json_out.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n")
    print(json.dumps({"path": str(args.glb), "status": report["status"], "errors": errors, "critical_near_coplanar": report["geometry"]["critical_textured_surface_pair_count"]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
