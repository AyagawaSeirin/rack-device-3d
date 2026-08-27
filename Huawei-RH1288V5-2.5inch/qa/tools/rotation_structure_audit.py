#!/usr/bin/env python3
"""Audit GLB failure modes that become visible during camera orbit.

This complements the skill's audit_glb.py with world-space duplicate/overlap,
normal, material-alpha, transform, and closed-core checks.  It intentionally
reports open decorative/photo planes separately from the required closed core.
"""

from __future__ import annotations

import argparse
import io
import json
from collections import defaultdict
from pathlib import Path

import numpy as np
import trimesh
from PIL import Image
from pygltflib import GLTF2
from shapely.geometry import Polygon
from shapely.strtree import STRtree


FACE_HINTS = ("face", "source_locked", "canonical", "front", "rear", "left", "right", "top", "bottom")
CORE_HINTS = ("closed chassis", "chassis core", "chassis_core", "closed_chassis", "body core", "body_core")
SOURCE_SURFACE_HINTS = (
    "source-locked", "source_locked", "source-matched", "source matched",
    "canonical", "photo surface", "closed cover face", "non-mirrored face",
    "fallback face",
)
PLANE_TOLERANCE_M = 0.00020
EXACT_PLANE_TOLERANCE_M = 0.000002


def canonical_plane(normal: np.ndarray, point: np.ndarray) -> tuple[np.ndarray, float]:
    normal = normal / np.linalg.norm(normal)
    for value in normal:
        if abs(value) > 1e-12:
            if value < 0:
                normal = -normal
            break
    return normal, -float(np.dot(normal, point))


def projected_polygon(triangle: np.ndarray, normal: np.ndarray) -> Polygon:
    axis = int(np.argmax(np.abs(normal)))
    coords = np.delete(triangle, axis, axis=1)
    return Polygon(coords)


def is_source_surface(item: dict) -> bool:
    name = (item["node"] + " " + item["geometry"]).lower()
    return any(hint in name for hint in SOURCE_SURFACE_HINTS)


def image_alpha(gltf: GLTF2, index: int) -> dict:
    image = gltf.images[index]
    payload = None
    if image.bufferView is not None:
        view = gltf.bufferViews[image.bufferView]
        blob = gltf.binary_blob()
        start = int(view.byteOffset or 0)
        payload = blob[start:start + int(view.byteLength)]
    elif image.uri and image.uri.startswith("data:"):
        import base64
        payload = base64.b64decode(image.uri.split(",", 1)[1])
    if payload is None:
        return {"index": index, "name": image.name, "embedded": False}
    with Image.open(io.BytesIO(payload)) as raster:
        rgba = raster.convert("RGBA")
        alpha = np.asarray(rgba.getchannel("A"), dtype=np.uint8)
        return {
            "index": index,
            "name": image.name,
            "embedded": True,
            "mode": raster.mode,
            "size": list(raster.size),
            "alpha_min": int(alpha.min()),
            "alpha_max": int(alpha.max()),
            "alpha_lt_255_pixels": int(np.count_nonzero(alpha < 255)),
            "alpha_lt_255_percent": round(float(np.mean(alpha < 255) * 100.0), 8),
        }


def audit(path: Path) -> dict:
    scene = trimesh.load(path, force="scene", process=False)
    gltf = GLTF2().load_binary(str(path))
    instances: list[tuple[str, str, trimesh.Trimesh, np.ndarray]] = []
    negative_transforms = []
    for node_name in scene.graph.nodes_geometry:
        transform, geom_name = scene.graph.get(node_name)
        determinant = float(np.linalg.det(transform[:3, :3]))
        if determinant < 0:
            negative_transforms.append({"node": node_name, "geometry": geom_name, "determinant": determinant})
        mesh = scene.geometry[geom_name].copy()
        mesh.apply_transform(transform)
        instances.append((node_name, geom_name, mesh, transform))

    triangles = []
    degenerates = []
    normal_mismatches = []
    exact_keys: dict[tuple, list[int]] = defaultdict(list)
    plane_groups: dict[tuple, list[int]] = defaultdict(list)
    mesh_checks = []
    for node_name, geom_name, mesh, _ in instances:
        welded = mesh.copy()
        welded.merge_vertices()
        mesh_checks.append({
            "node": node_name,
            "geometry": geom_name,
            "faces": int(len(mesh.faces)),
            "watertight": bool(welded.is_watertight),
            "winding_consistent": bool(welded.is_winding_consistent),
        })
        verts = np.asarray(mesh.vertices, dtype=np.float64)
        cached_normals = mesh._cache.cache.get("vertex_normals")
        vnorm = np.asarray(cached_normals, dtype=np.float64) if cached_normals is not None and len(cached_normals) == len(verts) else None
        for face_index, face in enumerate(np.asarray(mesh.faces, dtype=np.int64)):
            tri = verts[face]
            cross = np.cross(tri[1] - tri[0], tri[2] - tri[0])
            area2 = float(np.linalg.norm(cross))
            if area2 < 1e-14:
                degenerates.append({"node": node_name, "geometry": geom_name, "face": int(face_index)})
                continue
            outward = cross / area2
            if vnorm is not None:
                supplied = vnorm[face].mean(axis=0)
                supplied_length = float(np.linalg.norm(supplied))
                if supplied_length > 1e-12 and float(np.dot(outward, supplied / supplied_length)) < -0.25:
                    normal_mismatches.append({"node": node_name, "geometry": geom_name, "face": int(face_index)})
            normal, distance = canonical_plane(outward, tri[0])
            record = {
                "node": node_name,
                "geometry": geom_name,
                "face": int(face_index),
                "triangle": tri,
                "normal": outward,
                "canonical_normal": normal,
                "distance": distance,
            }
            tri_index = len(triangles)
            triangles.append(record)
            exact_vertex_key = tuple(sorted(tuple(np.round(v / 1e-7).astype(np.int64)) for v in tri))
            exact_keys[exact_vertex_key].append(tri_index)
            plane_key = tuple(np.round(normal / 2e-4).astype(np.int64)) + (int(round(distance / PLANE_TOLERANCE_M)),)
            plane_groups[plane_key].append(tri_index)

    duplicate_groups = []
    opposite_duplicate_groups = []
    for indices in exact_keys.values():
        nodes = {triangles[i]["node"] for i in indices}
        if len(indices) < 2 or len(nodes) < 2:
            continue
        entry = [{"node": triangles[i]["node"], "geometry": triangles[i]["geometry"], "face": triangles[i]["face"]} for i in indices]
        duplicate_groups.append(entry)
        if any(float(np.dot(triangles[indices[0]]["normal"], triangles[i]["normal"])) < -0.99 for i in indices[1:]):
            opposite_duplicate_groups.append(entry)

    overlap_pairs = []
    seen_pairs = set()
    for indices in plane_groups.values():
        if len(indices) < 2:
            continue
        projected = []
        projected_indices = []
        for left_index in indices:
            left = triangles[left_index]
            left_poly = projected_polygon(left["triangle"], left["canonical_normal"])
            if not left_poly.is_valid or left_poly.area <= 1e-14:
                continue
            projected.append(left_poly)
            projected_indices.append(left_index)
        if len(projected) < 2:
            continue
        tree = STRtree(projected)
        for local_left, left_poly in enumerate(projected):
            left_index = projected_indices[local_left]
            left = triangles[left_index]
            for local_right in tree.query(left_poly, predicate="intersects"):
                local_right = int(local_right)
                if local_right <= local_left:
                    continue
                right_index = projected_indices[local_right]
                pair_key = (min(left_index, right_index), max(left_index, right_index))
                if pair_key in seen_pairs:
                    continue
                seen_pairs.add(pair_key)
                right = triangles[right_index]
                if left["node"] == right["node"]:
                    continue
                if abs(float(np.dot(left["canonical_normal"], right["canonical_normal"]))) < 0.9999:
                    continue
                separation = abs(left["distance"] - right["distance"])
                if separation > PLANE_TOLERANCE_M:
                    continue
                right_poly = projected[local_right]
                area = float(left_poly.intersection(right_poly).area)
                if area <= 1e-12:
                    continue
                overlap_pairs.append({
                    "left": {"node": left["node"], "geometry": left["geometry"], "face": left["face"]},
                    "right": {"node": right["node"], "geometry": right["geometry"], "face": right["face"]},
                    "separation_mm": round(separation * 1000.0, 7),
                    "overlap_area_mm2": round(area * 1_000_000.0, 7),
                    "same_facing": bool(float(np.dot(left["normal"], right["normal"])) > 0),
                    "classification": "exact-coplanar" if separation <= EXACT_PLANE_TOLERANCE_M else "near-coplanar",
                })

    images = [image_alpha(gltf, i) for i in range(len(gltf.images or []))]
    materials = []
    face_material_violations = []
    for index, material in enumerate(gltf.materials or []):
        pbr = material.pbrMetallicRoughness
        factor = list(pbr.baseColorFactor or [1, 1, 1, 1]) if pbr else [1, 1, 1, 1]
        item = {
            "index": index,
            "name": material.name,
            "alphaMode": material.alphaMode or "OPAQUE",
            "baseColorFactor": factor,
            "doubleSided": bool(material.doubleSided),
            "baseColorTexture": pbr.baseColorTexture.index if pbr and pbr.baseColorTexture else None,
        }
        materials.append(item)
        lowered = (material.name or "").lower()
        if item["baseColorTexture"] is not None and any(hint in lowered for hint in FACE_HINTS):
            reasons = []
            if item["alphaMode"] != "OPAQUE": reasons.append("alphaMode")
            if factor != [1, 1, 1, 1]: reasons.append("baseColorFactor")
            if item["doubleSided"]: reasons.append("doubleSided")
            if reasons:
                face_material_violations.append({"material": item, "reasons": reasons})

    core_meshes = [m for m in mesh_checks if any(h in (m["node"] + " " + m["geometry"]).lower() for h in CORE_HINTS)]
    render_hazards = [p for p in overlap_pairs if p["same_facing"]]
    source_surface_hazards = [p for p in render_hazards if is_source_surface(p["left"]) or is_source_surface(p["right"])]
    solid_contacts = [p for p in render_hazards if p not in source_surface_hazards]
    result = {
        "path": str(path),
        "byte_size": path.stat().st_size,
        "scene_instances": len(instances),
        "triangles": len(triangles),
        "duplicate_triangle_groups": len(duplicate_groups),
        "duplicate_triangle_examples": duplicate_groups[:50],
        "opposite_duplicate_groups": len(opposite_duplicate_groups),
        "opposite_duplicate_examples": opposite_duplicate_groups[:50],
        "coplanar_overlap_pairs": len(overlap_pairs),
        "render_coplanar_hazard_pairs": len(render_hazards),
        "source_surface_coplanar_hazard_pairs": len(source_surface_hazards),
        "source_surface_coplanar_hazard_examples": sorted(source_surface_hazards, key=lambda p: (-p["overlap_area_mm2"], p["separation_mm"]))[:100],
        "solid_geometry_coplanar_contacts": len(solid_contacts),
        "opposite_facing_coplanar_contacts": sum(not p["same_facing"] for p in overlap_pairs),
        "exact_coplanar_overlap_pairs": sum(p["classification"] == "exact-coplanar" for p in overlap_pairs),
        "near_coplanar_overlap_pairs": sum(p["classification"] == "near-coplanar" for p in overlap_pairs),
        "coplanar_overlap_examples": sorted(overlap_pairs, key=lambda p: (-p["overlap_area_mm2"], p["separation_mm"]))[:100],
        "degenerate_triangles": len(degenerates),
        "degenerate_examples": degenerates[:50],
        "normal_mismatches": len(normal_mismatches),
        "normal_mismatch_examples": normal_mismatches[:50],
        "negative_transform_count": len(negative_transforms),
        "negative_transforms": negative_transforms,
        "materials": materials,
        "face_material_violations": face_material_violations,
        "images": images,
        "images_with_partial_alpha": [i for i in images if i.get("alpha_lt_255_pixels", 0) > 0],
        "mesh_checks": mesh_checks,
        "closed_core_candidates": core_meshes,
        "closed_core_pass": bool(core_meshes) and all(m["watertight"] and m["winding_consistent"] for m in core_meshes),
    }
    result["rotation_structure_pass"] = (
        result["duplicate_triangle_groups"] == 0
        and result["source_surface_coplanar_hazard_pairs"] == 0
        and result["degenerate_triangles"] == 0
        and result["normal_mismatches"] == 0
        and result["negative_transform_count"] == 0
        and not result["face_material_violations"]
        and not result["images_with_partial_alpha"]
        and result["closed_core_pass"]
    )
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("glb", type=Path)
    parser.add_argument("--json-out", type=Path)
    args = parser.parse_args()
    report = audit(args.glb)
    payload = json.dumps(report, indent=2, ensure_ascii=False)
    if args.json_out:
        args.json_out.parent.mkdir(parents=True, exist_ok=True)
        args.json_out.write_text(payload + "\n", encoding="utf-8")
    print(json.dumps({
        "path": report["path"],
        "triangles": report["triangles"],
        "duplicate_triangle_groups": report["duplicate_triangle_groups"],
        "opposite_duplicate_groups": report["opposite_duplicate_groups"],
        "coplanar_overlap_pairs": report["coplanar_overlap_pairs"],
        "render_coplanar_hazard_pairs": report["render_coplanar_hazard_pairs"],
        "source_surface_coplanar_hazard_pairs": report["source_surface_coplanar_hazard_pairs"],
        "solid_geometry_coplanar_contacts": report["solid_geometry_coplanar_contacts"],
        "opposite_facing_coplanar_contacts": report["opposite_facing_coplanar_contacts"],
        "exact_coplanar_overlap_pairs": report["exact_coplanar_overlap_pairs"],
        "near_coplanar_overlap_pairs": report["near_coplanar_overlap_pairs"],
        "degenerate_triangles": report["degenerate_triangles"],
        "normal_mismatches": report["normal_mismatches"],
        "negative_transform_count": report["negative_transform_count"],
        "face_material_violations": len(report["face_material_violations"]),
        "images_with_partial_alpha": len(report["images_with_partial_alpha"]),
        "closed_core_pass": report["closed_core_pass"],
        "rotation_structure_pass": report["rotation_structure_pass"],
    }, indent=2))


if __name__ == "__main__":
    main()
