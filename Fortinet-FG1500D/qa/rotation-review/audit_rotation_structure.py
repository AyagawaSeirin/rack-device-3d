#!/usr/bin/env python3
"""Cross-viewer stability-focused GLB audit: alpha, transforms and planar overlap."""

from __future__ import annotations

import argparse
import hashlib
import io
import json
from collections import defaultdict
from pathlib import Path

import numpy as np
from PIL import Image
from pygltflib import GLTF2
from shapely.geometry import Polygon
import trimesh


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def image_bytes(gltf: GLTF2, index: int) -> bytes:
    image = gltf.images[index]
    if image.bufferView is None:
        raise ValueError(f"image {index} is not embedded")
    view = gltf.bufferViews[image.bufferView]
    blob = gltf.binary_blob()
    start = int(view.byteOffset or 0)
    return bytes(blob[start:start + int(view.byteLength)])


def node_matrix(node) -> np.ndarray:
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


def world_determinants(gltf: GLTF2) -> list[dict]:
    nodes = gltf.nodes or []
    children = {child for node in nodes for child in (node.children or [])}
    roots = [index for index in range(len(nodes)) if index not in children]
    rows = []
    def visit(index: int, parent: np.ndarray) -> None:
        world = parent @ node_matrix(nodes[index])
        determinant = float(np.linalg.det(world[:3, :3]))
        rows.append({"index": index, "name": nodes[index].name, "determinant": determinant})
        for child in nodes[index].children or []:
            visit(child, world)
    for root in roots:
        visit(root, np.eye(4))
    return rows


def transformed_meshes(path: Path) -> list[tuple[str, trimesh.Trimesh]]:
    scene = trimesh.load(path, force="scene", process=False)
    result = []
    for node_name in scene.graph.nodes_geometry:
        transform, geometry_name = scene.graph.get(node_name)
        mesh = scene.geometry[geometry_name].copy()
        mesh.apply_transform(transform)
        result.append((str(node_name), mesh))
    return result


def planar_overlap_report(meshes: list[tuple[str, trimesh.Trimesh]], threshold_m: float) -> dict:
    plane_rows = []
    exact_triangles: dict[tuple, list[tuple[str, np.ndarray]]] = defaultdict(list)
    triangle_total = 0
    for name, mesh in meshes:
        vertices = np.asarray(mesh.vertices, dtype=float)
        faces = np.asarray(mesh.faces, dtype=int)
        for face in faces:
            triangle_total += 1
            tri = vertices[face]
            key = tuple(sorted(tuple(np.round(point, 8)) for point in tri))
            normal = np.cross(tri[1] - tri[0], tri[2] - tri[0])
            length = np.linalg.norm(normal)
            if length <= 1e-14:
                continue
            normal /= length
            exact_triangles[key].append((name, normal))
            axis = int(np.argmax(np.abs(normal)))
            if abs(normal[axis]) < 0.999999:
                continue
            coordinate = float(tri[:, axis].mean())
            if float(np.ptp(tri[:, axis])) > 1e-9:
                continue
            other = [item for item in range(3) if item != axis]
            polygon = Polygon(tri[:, other])
            if not polygon.is_valid or polygon.area <= 1e-14:
                continue
            plane_rows.append({"mesh": name, "axis": axis, "normal_sign": 1 if normal[axis] > 0 else -1, "coordinate": coordinate, "polygon": polygon, "bounds": polygon.bounds})
    duplicate = []
    opposite = []
    for entries in exact_triangles.values():
        unique_names = sorted({item[0] for item in entries})
        if len(entries) > 1:
            duplicate.append({"meshes": unique_names, "copies": len(entries)})
            if any(float(np.dot(entries[0][1], normal)) < -0.999999 for _, normal in entries[1:]):
                opposite.append({"meshes": unique_names, "copies": len(entries)})
    coplanar = []
    near = []
    plane_rows.sort(key=lambda item: (item["axis"], item["normal_sign"], item["coordinate"]))
    for index, first in enumerate(plane_rows):
        for second in plane_rows[index + 1:]:
            if second["axis"] != first["axis"] or second["normal_sign"] != first["normal_sign"]:
                if second["axis"] > first["axis"] or (second["axis"] == first["axis"] and second["normal_sign"] > first["normal_sign"]):
                    break
                continue
            separation = abs(first["coordinate"] - second["coordinate"])
            if separation >= threshold_m:
                if second["coordinate"] > first["coordinate"]:
                    break
                continue
            if first["mesh"] == second["mesh"]:
                continue
            a0,a1,a2,a3=first["bounds"];b0,b1,b2,b3=second["bounds"]
            if min(a2,b2)-max(a0,b0) <= 1e-10 or min(a3,b3)-max(a1,b1) <= 1e-10:
                continue
            overlap_area = float(first["polygon"].intersection(second["polygon"]).area)
            if overlap_area <= 1e-10:
                continue
            row = {"mesh_a": first["mesh"], "mesh_b": second["mesh"], "axis": first["axis"], "separation_mm": round(separation * 1000, 6), "overlap_area_mm2": round(overlap_area * 1_000_000, 6)}
            if separation <= 1e-8:
                coplanar.append(row)
            elif separation < threshold_m:
                near.append(row)
    def unique(rows):
        seen=set(); result=[]
        for row in rows:
            key=(row["mesh_a"],row["mesh_b"],row["axis"],row["separation_mm"])
            if key not in seen:seen.add(key);result.append(row)
        return result
    return {"triangle_count": triangle_total, "exact_duplicate_triangle_groups": duplicate, "opposite_orientation_duplicate_groups": opposite, "coplanar_overlap_pairs": unique(coplanar), "near_coplanar_overlap_pairs_under_threshold": unique(near), "near_coplanar_threshold_mm": threshold_m * 1000}


def audit(path: Path, threshold_mm: float) -> dict:
    gltf = GLTF2().load_binary(path)
    materials = []
    for index, material in enumerate(gltf.materials or []):
        pbr = material.pbrMetallicRoughness
        materials.append({"index": index, "name": material.name, "alphaMode": material.alphaMode or "OPAQUE", "baseColorFactor": list(pbr.baseColorFactor or [1,1,1,1]) if pbr else None, "doubleSided": bool(material.doubleSided), "unlit": bool((material.extensions or {}).get("KHR_materials_unlit"))})
    images = []
    for index, _ in enumerate(gltf.images or []):
        image = Image.open(io.BytesIO(image_bytes(gltf, index))).convert("RGBA")
        alpha = np.asarray(image.getchannel("A"), dtype=np.uint8)
        images.append({"index": index, "size": list(image.size), "alpha_min": int(alpha.min()), "alpha_max": int(alpha.max()), "alpha_lt_255_pixels": int(np.count_nonzero(alpha < 255)), "alpha_between_0_255_pixels": int(np.count_nonzero((alpha > 0) & (alpha < 255)))})
    determinants = world_determinants(gltf)
    meshes = transformed_meshes(path)
    core = []
    for name, mesh in meshes:
        lowered = name.lower()
        if any(token in lowered for token in ("closed", "shell", "chassis_sheet_metal", "chassis_body")):
            merged = mesh.copy()
            merged.merge_vertices()
            core.append({"name": name, "watertight": bool(merged.is_watertight), "winding_consistent": bool(merged.is_winding_consistent), "volume": float(merged.volume), "bounds": np.round(merged.bounds, 8).tolist()})
    planar = planar_overlap_report(meshes, threshold_mm / 1000)
    def is_core(name: str) -> bool:
        lowered = name.lower()
        return any(token in lowered for token in ("closed", "shell", "chassis_sheet_metal", "chassis_body"))
    def is_canonical(name: str) -> bool:
        lowered = name.lower()
        return name.startswith(("Face_", "Texture_", "CANONICAL_")) or "source_locked" in lowered
    def is_internal_core_contact(row: dict) -> bool:
        a, b = row["mesh_a"], row["mesh_b"]
        return (is_core(a) and not is_canonical(b)) or (is_core(b) and not is_canonical(a))
    planar["hazardous_coplanar_overlap_pairs"] = [
        row for row in planar["coplanar_overlap_pairs"]
        if row["overlap_area_mm2"] >= 1.0 and not is_internal_core_contact(row)
    ]
    planar["hazardous_near_coplanar_overlap_pairs"] = [
        row for row in planar["near_coplanar_overlap_pairs_under_threshold"]
        if row["overlap_area_mm2"] >= 1.0 and not is_internal_core_contact(row)
    ]
    planar["tolerance_note"] = "Sub-1 mm^2 solid-junction contacts and internal closed-core contacts are reported but are not draw-order hazards."
    failures = []
    if any(item["alphaMode"] != "OPAQUE" or item["baseColorFactor"][-1] != 1 or item["doubleSided"] for item in materials): failures.append("material-alpha-or-double-sided")
    if any(item["alpha_lt_255_pixels"] for item in images): failures.append("embedded-image-alpha")
    if any(item["determinant"] < 0 for item in determinants): failures.append("negative-transform")
    if planar["exact_duplicate_triangle_groups"]: failures.append("duplicate-triangles")
    if planar["hazardous_coplanar_overlap_pairs"]: failures.append("coplanar-overlap")
    if planar["hazardous_near_coplanar_overlap_pairs"]: failures.append("near-coplanar-risk")
    if not core or not any(item["watertight"] and item["winding_consistent"] and item["volume"] > 0 for item in core): failures.append("closed-core")
    return {"path": str(path), "bytes": path.stat().st_size, "sha256": sha256(path), "materials": materials, "images": images, "negative_world_transforms": [item for item in determinants if item["determinant"] < 0], "closed_core_candidates": core, "geometry": planar, "failures": failures, "status": "PASS" if not failures else "REWORK"}


def main() -> None:
    parser=argparse.ArgumentParser();parser.add_argument("models",nargs="+");parser.add_argument("--threshold-mm",type=float,default=.5);parser.add_argument("--out",required=True);args=parser.parse_args()
    report={"near_coplanar_threshold_mm":args.threshold_mm,"models":[audit(Path(item),args.threshold_mm) for item in args.models]};report["status"]="PASS" if all(item["status"]=="PASS" for item in report["models"]) else "REWORK";Path(args.out).parent.mkdir(parents=True,exist_ok=True);Path(args.out).write_text(json.dumps(report,indent=2,ensure_ascii=False)+"\n",encoding="utf-8");print(json.dumps({"status":report["status"],"out":args.out,"failures":{item["path"]:item["failures"] for item in report["models"]}},indent=2))


if __name__ == "__main__": main()
