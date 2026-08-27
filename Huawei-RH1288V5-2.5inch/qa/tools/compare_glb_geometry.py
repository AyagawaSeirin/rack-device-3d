#!/usr/bin/env python3
"""Prove standard/web visible geometry, UVs, transforms, and orientation are identical."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import numpy as np
import trimesh


def fingerprint(path: Path) -> dict:
    scene = trimesh.load(path, force="scene", process=False)
    digest = hashlib.sha256()
    geometries = []
    for name in sorted(scene.geometry):
        geometry = scene.geometry[name]
        vertices = np.asarray(geometry.vertices, dtype="<f8")
        faces = np.asarray(geometry.faces, dtype="<i8")
        digest.update(name.encode())
        digest.update(vertices.tobytes())
        digest.update(faces.tobytes())
        uv = getattr(getattr(geometry, "visual", None), "uv", None)
        if uv is not None:
            digest.update(np.asarray(uv, dtype="<f8").tobytes())
        geometries.append({"name": name, "vertices": len(vertices), "triangles": len(faces)})
    nodes = []
    for node_name in sorted(scene.graph.nodes_geometry):
        transform, geometry_name = scene.graph[node_name]
        transform = np.asarray(transform, dtype="<f8")
        digest.update(node_name.encode())
        digest.update(str(geometry_name).encode())
        digest.update(transform.tobytes())
        nodes.append({"node": node_name, "geometry": geometry_name,
                      "determinant": float(np.linalg.det(transform[:3, :3]))})
    return {
        "geometry_transform_uv_sha256": digest.hexdigest(),
        "bounds": np.asarray(scene.bounds, dtype=float).tolist(),
        "geometry_count": len(geometries),
        "node_geometry_count": len(nodes),
        "triangles": sum(item["triangles"] for item in geometries),
        "negative_determinant_nodes": [item for item in nodes if item["determinant"] < 0],
        "geometries": geometries,
        "nodes": nodes,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("standard", type=Path)
    parser.add_argument("web", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    standard = fingerprint(args.standard)
    web = fingerprint(args.web)
    checks = {
        "geometry_transform_uv_fingerprint_equal": standard["geometry_transform_uv_sha256"] == web["geometry_transform_uv_sha256"],
        "bounds_equal": bool(np.allclose(standard["bounds"], web["bounds"], atol=1e-9, rtol=0)),
        "no_negative_transform_standard": not standard["negative_determinant_nodes"],
        "no_negative_transform_web": not web["negative_determinant_nodes"],
    }
    report = {
        "schema": "rack-device-standard-web-visible-geometry-parity-v1",
        "standard_path": str(args.standard),
        "web_path": str(args.web),
        "standard": standard,
        "web": web,
        "checks": checks,
        "pass": all(checks.values()),
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({"output": str(args.output), "checks": checks, "pass": report["pass"]}, indent=2))
    return 0 if report["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
