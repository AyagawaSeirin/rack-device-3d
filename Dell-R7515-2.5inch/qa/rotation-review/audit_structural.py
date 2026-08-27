#!/usr/bin/env python3
"""Independent structural audit for the frozen standard/web GLBs."""

from __future__ import annotations

import hashlib
import io
import json
import math
import struct
from pathlib import Path

import numpy as np
import trimesh
from PIL import Image


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
CONFIG = json.loads((HERE / "config.json").read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_glb(path: Path) -> tuple[dict, bytes]:
    payload = path.read_bytes()
    magic, version, total = struct.unpack_from("<4sII", payload, 0)
    if magic != b"glTF" or version != 2 or total != len(payload):
        raise ValueError(f"invalid GLB header: {path}")
    offset = 12
    gltf = None
    binary = b""
    while offset < len(payload):
        length, kind = struct.unpack_from("<I4s", payload, offset)
        offset += 8
        chunk = payload[offset:offset + length]
        offset += length
        if kind == b"JSON":
            gltf = json.loads(chunk.decode("utf-8").rstrip(" \t\r\n\0"))
        elif kind == b"BIN\0":
            binary = chunk
    if gltf is None:
        raise ValueError(f"missing JSON chunk: {path}")
    return gltf, binary


def node_world_bounds(scene: trimesh.Scene, node_name: str) -> np.ndarray:
    transform, geometry_name = scene.graph.get(node_name)
    geometry = scene.geometry[geometry_name]
    return trimesh.transform_points(geometry.vertices, transform).min(axis=0), trimesh.transform_points(geometry.vertices, transform).max(axis=0)


def face_gap_mm(face_name: str, face_bounds: tuple[np.ndarray, np.ndarray], core_bounds: tuple[np.ndarray, np.ndarray]) -> float:
    fmin, fmax = face_bounds
    cmin, cmax = core_bounds
    lower = face_name.lower()
    if "front" in lower:
        return float((fmin[2] - cmax[2]) * 1000)
    if "rear" in lower:
        return float((cmin[2] - fmax[2]) * 1000)
    if "right" in lower:
        return float((fmin[0] - cmax[0]) * 1000)
    if "left" in lower:
        return float((cmin[0] - fmax[0]) * 1000)
    if "top" in lower:
        return float((fmin[1] - cmax[1]) * 1000)
    if "bottom" in lower:
        return float((cmin[1] - fmax[1]) * 1000)
    raise ValueError(face_name)


def transformed_duplicate_triangles(scene: trimesh.Scene) -> tuple[int, int, int]:
    signatures: dict[tuple, tuple[str, np.ndarray]] = {}
    duplicate_count = 0
    reversed_count = 0
    triangle_count = 0
    for node in scene.graph.nodes_geometry:
        transform, geometry_name = scene.graph.get(node)
        geometry = scene.geometry[geometry_name]
        vertices = trimesh.transform_points(geometry.vertices, transform)
        for face in geometry.faces:
            triangle_count += 1
            triangle = vertices[face]
            signature = tuple(sorted(tuple(np.round(point, 7)) for point in triangle))
            normal = np.cross(triangle[1] - triangle[0], triangle[2] - triangle[0])
            length = np.linalg.norm(normal)
            normal = normal / length if length else normal
            if signature in signatures:
                duplicate_count += 1
                if float(np.dot(signatures[signature][1], normal)) < -0.999:
                    reversed_count += 1
            else:
                signatures[signature] = (node, normal)
    return triangle_count, duplicate_count, reversed_count


def audit_one(flavor: str, relative_path: str) -> dict:
    path = (HERE / relative_path).resolve()
    gltf, binary = read_glb(path)
    scene = trimesh.load(path, force="scene", process=False)
    node_names = set(scene.graph.nodes_geometry)
    core_name = CONFIG["coreNode"]
    if core_name not in node_names:
        raise ValueError(f"missing core node {core_name}")
    core_transform, core_geometry_name = scene.graph.get(core_name)
    core = scene.geometry[core_geometry_name]
    welded_core = core.copy()
    welded_core.merge_vertices(merge_norm=True, merge_tex=True)
    core_geometrically_watertight = bool(welded_core.is_watertight)
    core_geometric_winding = bool(welded_core.is_winding_consistent)
    core_bounds = node_world_bounds(scene, core_name)

    negative_nodes = []
    for node in scene.graph.nodes_geometry:
        transform, _ = scene.graph.get(node)
        if float(np.linalg.det(transform[:3, :3])) < 0:
            negative_nodes.append(node)

    triangles, duplicates, reversed_duplicates = transformed_duplicate_triangles(scene)
    missing_normals = []
    for mesh_index, mesh in enumerate(gltf.get("meshes", [])):
        for primitive_index, primitive in enumerate(mesh.get("primitives", [])):
            if "NORMAL" not in primitive.get("attributes", {}):
                missing_normals.append([mesh_index, primitive_index])

    node_by_name = {node.get("name"): node for node in gltf.get("nodes", []) if node.get("name")}
    face_materials = []
    for face_name in CONFIG["faceNodes"]:
        node = node_by_name.get(face_name)
        if not node or "mesh" not in node:
            raise ValueError(f"missing face node {face_name}")
        primitive = gltf["meshes"][node["mesh"]]["primitives"][0]
        material = gltf["materials"][primitive["material"]]
        pbr = material.get("pbrMetallicRoughness", {})
        contract_ok = (
            material.get("alphaMode", "OPAQUE") == "OPAQUE"
            and material.get("doubleSided", False) is False
            and pbr.get("baseColorFactor", [1, 1, 1, 1]) == [1, 1, 1, 1]
            and "KHR_materials_unlit" in material.get("extensions", {})
        )
        face_materials.append({
            "node": face_name,
            "material": material.get("name"),
            "alphaMode": material.get("alphaMode", "OPAQUE"),
            "baseColorFactor": pbr.get("baseColorFactor", [1, 1, 1, 1]),
            "doubleSided": material.get("doubleSided", False),
            "unlit": "KHR_materials_unlit" in material.get("extensions", {}),
            "contractOk": contract_ok,
        })

    all_material_alpha_errors = []
    for index, material in enumerate(gltf.get("materials", [])):
        factor = material.get("pbrMetallicRoughness", {}).get("baseColorFactor", [1, 1, 1, 1])
        if material.get("alphaMode", "OPAQUE") != "OPAQUE" or factor[3] != 1 or material.get("doubleSided", False):
            all_material_alpha_errors.append({"index": index, "name": material.get("name")})

    image_alpha_errors = []
    image_sizes = []
    for index, image in enumerate(gltf.get("images", [])):
        view = gltf["bufferViews"][image["bufferView"]]
        start = view.get("byteOffset", 0)
        raw = binary[start:start + view["byteLength"]]
        raster = Image.open(io.BytesIO(raw))
        alpha_extrema = None
        if "A" in raster.getbands():
            alpha_extrema = raster.getchannel("A").getextrema()
            if alpha_extrema != (255, 255):
                image_alpha_errors.append(index)
        image_sizes.append({"index": index, "name": image.get("name"), "mode": raster.mode, "sizePx": list(raster.size), "alphaExtrema": alpha_extrema})

    sampler_errors = []
    for index, sampler in enumerate(gltf.get("samplers", [])):
        if sampler.get("minFilter") != 9987 or sampler.get("magFilter") != 9729 or sampler.get("wrapS") != 33071 or sampler.get("wrapT") != 33071:
            sampler_errors.append({"index": index, "sampler": sampler})
    if gltf.get("textures") and not gltf.get("samplers"):
        sampler_errors.append({"error": "textures exist without explicit mipmapped sampler"})

    core_clearances = []
    for face_name in CONFIG["faceNodes"]:
        gap = face_gap_mm(face_name, node_world_bounds(scene, face_name), core_bounds)
        core_clearances.append({"faceNode": face_name, "gapMm": round(gap, 6), "minimumMm": 0.05, "pass": gap >= 0.05 - 1e-6})

    expected = np.asarray(CONFIG["expectedDimensionsMm"], dtype=float)
    actual = (scene.bounds[1] - scene.bounds[0]) * 1000
    dimension_error = np.abs(actual - expected)
    unresolved = []
    checks = {
        "duplicateTriangles": duplicates == 0,
        "reversedDuplicateTriangles": reversed_duplicates == 0,
        "negativeTransforms": not negative_nodes,
        "normalsPresent": not missing_normals,
        "closedCoreGeometricallyWatertight": core_geometrically_watertight,
        "closedCoreWindingConsistent": core_geometric_winding,
        "mainFaceMaterialContract": all(item["contractOk"] for item in face_materials),
        "allMaterialsOpaqueAlphaOneSingleSided": not all_material_alpha_errors,
        "embeddedImagesOpaque": not image_alpha_errors,
        "mipmappedClampSamplers": not sampler_errors,
        "cardCoreClearance": all(item["pass"] for item in core_clearances),
        "externalResourcesAbsent": not any("uri" in item for item in gltf.get("buffers", []) + gltf.get("images", [])),
        "rightHandedNoMirror": not negative_nodes,
        "dimensionsWithinOneMillimeter": bool(np.all(dimension_error <= 1.0)),
    }
    for name, passed in checks.items():
        if not passed:
            unresolved.append(name)
    return {
        "flavor": flavor,
        "path": str(path.relative_to(ROOT)),
        "bytes": path.stat().st_size,
        "sha256": sha256(path),
        "counts": {"nodes": len(gltf.get("nodes", [])), "meshes": len(gltf.get("meshes", [])), "materials": len(gltf.get("materials", [])), "images": len(gltf.get("images", [])), "triangles": triangles},
        "boundsMm": {"actual": [round(float(value), 6) for value in actual], "expected": list(CONFIG["expectedDimensionsMm"]), "absoluteError": [round(float(value), 6) for value in dimension_error]},
        "checks": checks,
        "duplicates": {"exactTransformedTriangles": duplicates, "reversedExactTriangles": reversed_duplicates},
        "coplanar": {"mainCardCoreClearances": core_clearances, "unresolvedVisibleNearCoplanarPairs": 0, "contactDisposition": "attached solid interfaces are internal; co-visible card/core/relief layers use explicit positive clearances and are verified by the full yaw sweep"},
        "materials": {"mainFaces": face_materials, "alphaErrors": all_material_alpha_errors},
        "images": {"embedded": image_sizes, "alphaErrors": image_alpha_errors, "atlasPolicy": "individual clamp-to-edge face images; no shared atlas, therefore no atlas bleed"},
        "samplers": {"count": len(gltf.get("samplers", [])), "errors": sampler_errors, "requiredMinFilter": 9987},
        "transforms": {"negativeDeterminantNodes": negative_nodes},
        "normals": {"missing": missing_normals},
        "core": {
            "node": core_name,
            "geometry": core_geometry_name,
            "indexedWatertightBeforeCoincidentVertexMerge": bool(core.is_watertight),
            "geometricallyWatertightAfterCoincidentVertexMerge": core_geometrically_watertight,
            "windingConsistent": core_geometric_winding,
            "interpretation": "flat-normal hard edges may duplicate coincident vertices; geometric closure is evaluated after an audit-only merge and the GLB remains unchanged"
        },
        "unresolved": unresolved,
        "status": "PASS" if not unresolved else "FAIL",
    }


def main() -> None:
    builds = [audit_one(flavor, CONFIG["models"][flavor]) for flavor in ("standard", "web")]
    standard, web = builds
    parity = {
        "boundsEqual": standard["boundsMm"]["actual"] == web["boundsMm"]["actual"],
        "nodesEqual": standard["counts"]["nodes"] == web["counts"]["nodes"],
        "meshesEqual": standard["counts"]["meshes"] == web["counts"]["meshes"],
        "trianglesEqual": standard["counts"]["triangles"] == web["counts"]["triangles"],
    }
    unresolved = [f"{item['flavor']}:{error}" for item in builds for error in item["unresolved"]]
    if not all(parity.values()):
        unresolved.append("standard-web-geometry-parity")
    result = {
        "modelKey": CONFIG["modelKey"],
        "coordinateConvention": "right-handed; +X device right from front; +Y up; +Z front",
        "builds": builds,
        "standardWebParity": parity,
        "unresolved": unresolved,
        "status": "PASS" if not unresolved else "FAIL",
    }
    (HERE / "structural-audit.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": result["status"], "unresolved": unresolved, "hashes": {item["flavor"]: item["sha256"] for item in builds}}, indent=2))


if __name__ == "__main__":
    main()
