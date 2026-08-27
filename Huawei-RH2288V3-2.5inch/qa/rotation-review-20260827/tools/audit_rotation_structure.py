#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
from collections import defaultdict
from io import BytesIO
from pathlib import Path

import numpy as np
from PIL import Image
from pygltflib import GLTF2
import trimesh


TEXTURE_MATERIAL_MARKERS = ("PhotographicSurface_opaque_texture", "evidence-locked texture")
PHOTO_MESH_MARKERS = ("PhotographicSurface", "Texture_FRONT", "Texture_REAR", "Texture_LEFT", "Texture_RIGHT", "Texture_TOP", "Texture_BOTTOM")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def node_local_matrix(node) -> np.ndarray:
    if node.matrix:
        return np.asarray(node.matrix, dtype=float).reshape((4, 4), order="F")
    matrix = np.eye(4)
    if node.translation:
        matrix[:3, 3] = node.translation
    if node.rotation:
        x, y, z, w = node.rotation
        matrix[:3, :3] = trimesh.transformations.quaternion_matrix([w, x, y, z])[:3, :3]
    if node.scale:
        matrix[:3, :3] = matrix[:3, :3] @ np.diag(node.scale)
    return matrix


def embedded_image_bytes(document: GLTF2, image_index: int, binary_blob: bytes) -> bytes:
    image = document.images[image_index]
    if image.uri:
        if image.uri.startswith("data:"):
            import base64
            return base64.b64decode(image.uri.split(",", 1)[1])
        return b""
    view = document.bufferViews[image.bufferView]
    start = view.byteOffset or 0
    return binary_blob[start:start + view.byteLength]


def triangle_key(triangle: np.ndarray, tolerance: float = 1e-8) -> tuple:
    points = [tuple(np.round(point / tolerance).astype(np.int64)) for point in triangle]
    return tuple(sorted(points))


def world_meshes(scene: trimesh.Scene) -> list[tuple[str, trimesh.Trimesh]]:
    result = []
    for node_name in scene.graph.nodes_geometry:
        transform, geometry_name = scene.graph[node_name]
        mesh = scene.geometry[geometry_name].copy()
        mesh.apply_transform(transform)
        result.append((node_name, mesh))
    return result


def projected_aabb_overlap(first: np.ndarray, second: np.ndarray, normal: np.ndarray) -> bool:
    drop_axis = int(np.argmax(np.abs(normal)))
    axes = [axis for axis in range(3) if axis != drop_axis]
    a = first[:, axes]
    b = second[:, axes]
    overlap = np.minimum(a.max(axis=0), b.max(axis=0)) - np.maximum(a.min(axis=0), b.min(axis=0))
    return bool(np.all(overlap > 1e-8))


def geometry_checks(scene: trimesh.Scene, separation_limit_m: float) -> dict:
    meshes = world_meshes(scene)
    duplicate_groups: dict[tuple, list[dict]] = defaultdict(list)
    triangles_by_mesh: dict[str, np.ndarray] = {}
    normals_by_mesh: dict[str, np.ndarray] = {}
    for mesh_name, mesh in meshes:
        triangles = mesh.triangles
        normals = mesh.face_normals
        triangles_by_mesh[mesh_name] = triangles
        normals_by_mesh[mesh_name] = normals
        for face_index, triangle in enumerate(triangles):
            duplicate_groups[triangle_key(triangle)].append({
                "mesh": mesh_name,
                "face_index": face_index,
                "normal": [round(float(value), 8) for value in normals[face_index]],
            })
    duplicates = [group for group in duplicate_groups.values() if len(group) > 1]
    opposite_duplicate_groups = 0
    for group in duplicates:
        normals = [np.asarray(item["normal"]) for item in group]
        if any(float(np.dot(normals[0], other)) < -0.999999 for other in normals[1:]):
            opposite_duplicate_groups += 1

    near_pairs: dict[tuple[str, str], dict] = {}
    photo_names = [name for name in triangles_by_mesh if any(marker in name for marker in PHOTO_MESH_MARKERS)]
    for photo_name in photo_names:
        for photo_triangle, photo_normal in zip(triangles_by_mesh[photo_name], normals_by_mesh[photo_name]):
            photo_normal = photo_normal / np.linalg.norm(photo_normal)
            for other_name, other_triangles in triangles_by_mesh.items():
                if other_name == photo_name or any(marker in other_name for marker in PHOTO_MESH_MARKERS):
                    continue
                for other_triangle, other_normal in zip(other_triangles, normals_by_mesh[other_name]):
                    other_normal = other_normal / np.linalg.norm(other_normal)
                    if abs(float(np.dot(photo_normal, other_normal))) < 0.99999:
                        continue
                    separation = abs(float(np.dot(photo_normal, other_triangle[0] - photo_triangle[0])))
                    if separation > separation_limit_m:
                        continue
                    if not projected_aabb_overlap(photo_triangle, other_triangle, photo_normal):
                        continue
                    key = (photo_name, other_name)
                    current = near_pairs.get(key)
                    if current is None or separation < current["minimum_separation_m"]:
                        near_pairs[key] = {
                            "photographic_mesh": photo_name,
                            "other_mesh": other_name,
                            "minimum_separation_m": separation,
                            "minimum_separation_mm": separation * 1000.0,
                        }

    core_records = []
    for name, mesh in meshes:
        if "ChassisBody" in name or "Closed_Chassis" in name:
            core_records.append({
                "mesh": name,
                "watertight": bool(mesh.is_watertight),
                "winding_consistent": bool(mesh.is_winding_consistent),
                "positive_volume": bool(mesh.volume > 0),
                "volume": float(mesh.volume),
                "euler_number": int(mesh.euler_number),
            })
    signature = hashlib.sha256()
    for name, mesh in sorted(meshes, key=lambda item: item[0]):
        signature.update(name.encode("utf-8"))
        signature.update(np.round(mesh.vertices, 7).astype("<f8").tobytes())
        signature.update(mesh.faces.astype("<i8").tobytes())
    return {
        "mesh_count": len(meshes),
        "triangle_count": sum(len(mesh.faces) for _, mesh in meshes),
        "exact_duplicate_triangle_group_count": len(duplicates),
        "exact_duplicate_triangle_instance_count": sum(len(group) for group in duplicates),
        "opposite_normal_duplicate_group_count": opposite_duplicate_groups,
        "duplicate_examples": duplicates[:30],
        "near_coplanar_limit_mm": separation_limit_m * 1000.0,
        "near_coplanar_photographic_pair_count": len(near_pairs),
        "near_coplanar_photographic_pairs": sorted(near_pairs.values(), key=lambda item: item["minimum_separation_m"]),
        "closed_core": core_records,
        "visible_geometry_signature": signature.hexdigest(),
    }


def material_checks(path: Path) -> dict:
    document = GLTF2().load_binary(str(path))
    blob = document.binary_blob()
    materials = []
    errors = []
    for index, material in enumerate(document.materials or []):
        factor = list((material.pbrMetallicRoughness.baseColorFactor if material.pbrMetallicRoughness else None) or [1, 1, 1, 1])
        texture_material = bool(material.name and any(marker in material.name for marker in TEXTURE_MATERIAL_MARKERS))
        record = {
            "index": index,
            "name": material.name,
            "alpha_mode": material.alphaMode or "OPAQUE",
            "base_color_factor": factor,
            "double_sided": bool(material.doubleSided),
            "unlit": bool(material.extensions and "KHR_materials_unlit" in material.extensions),
            "texture_material": texture_material,
        }
        materials.append(record)
        if record["alpha_mode"] != "OPAQUE":
            errors.append(f"material {index} {material.name}: alphaMode is {record['alpha_mode']}")
        if len(factor) != 4 or abs(float(factor[3]) - 1.0) > 1e-9:
            errors.append(f"material {index} {material.name}: baseColor alpha is not 1")
        if record["double_sided"]:
            errors.append(f"material {index} {material.name}: doubleSided is true")
        if texture_material and factor != [1.0, 1.0, 1.0, 1.0]:
            errors.append(f"material {index} {material.name}: photographic baseColorFactor is not neutral")

    images = []
    for index in range(len(document.images or [])):
        data = embedded_image_bytes(document, index, blob)
        if not data:
            images.append({"index": index, "external_or_missing": True})
            errors.append(f"image {index}: external or missing")
            continue
        image = Image.open(BytesIO(data))
        alpha_min = 255
        partial_alpha_pixels = 0
        if "A" in image.getbands():
            alpha = np.asarray(image.getchannel("A"))
            alpha_min = int(alpha.min())
            partial_alpha_pixels = int(np.count_nonzero(alpha < 255))
        images.append({
            "index": index,
            "bytes": len(data),
            "sha256": sha256_bytes(data),
            "mode": image.mode,
            "size_px": list(image.size),
            "alpha_min": alpha_min,
            "alpha_below_255_pixels": partial_alpha_pixels,
        })
        if partial_alpha_pixels:
            errors.append(f"image {index}: {partial_alpha_pixels} pixels have alpha below 255")

    negative_nodes = []
    for index, node in enumerate(document.nodes or []):
        determinant = float(np.linalg.det(node_local_matrix(node)[:3, :3]))
        if determinant < 0:
            negative_nodes.append({"index": index, "name": node.name, "determinant": determinant})
    external_buffers = [buffer.uri for buffer in document.buffers or [] if buffer.uri]
    external_images = [image.uri for image in document.images or [] if image.uri and not image.uri.startswith("data:")]
    if negative_nodes:
        errors.append(f"{len(negative_nodes)} negative/mirrored node transforms")
    if external_buffers or external_images:
        errors.append("external resources are present")
    return {
        "materials": materials,
        "images": images,
        "negative_transform_nodes": negative_nodes,
        "external_buffers": external_buffers,
        "external_images": external_images,
        "extensions_used": list(document.extensionsUsed or []),
        "errors": errors,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("glb", type=Path)
    parser.add_argument("--json-out", type=Path, required=True)
    parser.add_argument("--near-coplanar-limit-mm", type=float, default=0.25)
    args = parser.parse_args()
    scene = trimesh.load(args.glb, force="scene", process=False)
    geometry = geometry_checks(scene, args.near_coplanar_limit_mm / 1000.0)
    material = material_checks(args.glb)
    errors = list(material["errors"])
    if geometry["exact_duplicate_triangle_group_count"]:
        errors.append(f"{geometry['exact_duplicate_triangle_group_count']} exact duplicate triangle groups")
    if geometry["near_coplanar_photographic_pair_count"]:
        errors.append(f"{geometry['near_coplanar_photographic_pair_count']} photographic/geometry pairs at or below {args.near_coplanar_limit_mm} mm")
    if not geometry["closed_core"] or any(
        not item["watertight"] or not item["winding_consistent"] or not item["positive_volume"]
        for item in geometry["closed_core"]
    ):
        errors.append("closed core gate failed")
    report = {
        "path": str(args.glb),
        "bytes": args.glb.stat().st_size,
        "sha256": sha256_bytes(args.glb.read_bytes()),
        "status": "PASS" if not errors else "FAIL",
        "error_count": len(errors),
        "errors": errors,
        "geometry": geometry,
        "material_alpha_negative_transform": material,
    }
    args.json_out.parent.mkdir(parents=True, exist_ok=True)
    args.json_out.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({"status": report["status"], "errors": errors, "output": str(args.json_out)}))
    raise SystemExit(0 if not errors else 1)


if __name__ == "__main__":
    main()
