#!/usr/bin/env python3
"""Prove that standard and web GLBs share identical visible geometry/transforms."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np
import trimesh


ROOT = Path(__file__).resolve().parents[2]
STANDARD = ROOT / "model" / f"{ROOT.name}.glb"
WEB = ROOT / "model" / f"{ROOT.name}-web.glb"
OUTPUT = ROOT / "qa" / "rotation-review" / "after" / "standard-web-geometry-parity.json"


def digest(array: np.ndarray, dtype: str) -> str:
    canonical = np.ascontiguousarray(array, dtype=dtype)
    return hashlib.sha256(canonical.tobytes()).hexdigest()


def inspect(path: Path) -> dict:
    scene = trimesh.load(path, force="scene", process=False)
    meshes = {}
    for name in sorted(scene.geometry):
        mesh = scene.geometry[name]
        meshes[name] = {
            "vertices": len(mesh.vertices),
            "triangles": len(mesh.faces),
            "vertices_f64_sha256": digest(mesh.vertices, "<f8"),
            "faces_i64_sha256": digest(mesh.faces, "<i8"),
        }
    nodes = {}
    for node in sorted(scene.graph.nodes_geometry):
        transform, geometry = scene.graph[node]
        nodes[node] = {
            "geometry": geometry,
            "transform_f64_sha256": digest(transform, "<f8"),
        }
    return {
        "path": str(path),
        "file_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        "bounds_m": np.asarray(scene.bounds).tolist(),
        "mesh_count": len(meshes),
        "node_count": len(nodes),
        "meshes": meshes,
        "nodes": nodes,
    }


def main() -> int:
    standard = inspect(STANDARD)
    web = inspect(WEB)
    equal_meshes = standard["meshes"] == web["meshes"]
    equal_nodes = standard["nodes"] == web["nodes"]
    equal_bounds = standard["bounds_m"] == web["bounds_m"]
    result = {
        "model": ROOT.name,
        "standard": standard,
        "web": web,
        "checks": {
            "identical_mesh_names_counts_vertices_and_triangles": equal_meshes,
            "identical_node_geometry_bindings_and_transforms": equal_nodes,
            "identical_scene_bounds": equal_bounds,
        },
        "status": "PASS" if equal_meshes and equal_nodes and equal_bounds else "FAIL",
        "note": "Texture payloads may differ; this gate compares all visible mesh arrays, node bindings/transforms, and bounds.",
    }
    OUTPUT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"model": ROOT.name, "status": result["status"], "mesh_count": standard["mesh_count"], "node_count": standard["node_count"]}))
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
