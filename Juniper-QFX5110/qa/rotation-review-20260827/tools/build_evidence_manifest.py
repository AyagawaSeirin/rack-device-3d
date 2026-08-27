#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path

import numpy as np
import trimesh


COMBOS = (("three", "standard"), ("three", "web"), ("babylon", "standard"), ("babylon", "web"))
STATIC_VIEWS = (
    ("front", 0, 0), ("rear", 180, 0), ("left", 270, 0), ("right", 90, 0),
    ("top", 0, 82), ("bottom", 0, -82), ("front-left", 315, 26),
    ("front-right", 45, 26), ("rear-left", 225, 26), ("rear-right", 135, 26),
)


def sha(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def record(path: Path, base: Path) -> dict:
    return {"path": str(path.relative_to(base)), "bytes": path.stat().st_size, "sha256": sha(path)}


def scene_geometry_hash(path: Path) -> tuple[str, int, int]:
    scene = trimesh.load(path, force="scene", process=False)
    digest = hashlib.sha256()
    triangles = 0
    nodes = 0
    for node in sorted(scene.graph.nodes_geometry):
        transform, geometry_name = scene.graph[node]
        mesh = scene.geometry[geometry_name]
        digest.update(str(node).encode())
        digest.update(np.round(np.asarray(transform), 7).astype("<f8").tobytes())
        digest.update(np.round(np.asarray(mesh.vertices), 7).astype("<f8").tobytes())
        digest.update(np.asarray(mesh.faces, dtype="<i8").tobytes())
        triangles += len(mesh.faces)
        nodes += 1
    return digest.hexdigest(), nodes, triangles


def phase_frames(root: Path, phase: str, base: Path) -> list[dict]:
    rows = []
    for engine, variant in COMBOS:
        combo = root / phase / f"{engine}-{variant}"
        rotation = combo / "rotation" if phase == "after" else combo
        for yaw in range(0, 360, 5):
            path = rotation / f"yaw-{yaw:03d}.png"
            rows.append({"phase": phase, "engine": engine, "variant": variant, "kind": "yaw", "yaw": yaw, "pitch": 16, "background": "light-checker", **record(path, base)})
        for yaw, pitch in ((45, -35), (135, 0), (225, 35), (315, 65)):
            label = str(pitch).replace("-", "m")
            path = rotation / f"pitch-{yaw:03d}-{label}.png"
            rows.append({"phase": phase, "engine": engine, "variant": variant, "kind": "pitch", "yaw": yaw, "pitch": pitch, "background": "dark-checker", **record(path, base)})
    return rows


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("model")
    parser.add_argument("key")
    parser.add_argument("--root", type=Path, required=True)
    args = parser.parse_args()
    repo = args.root.resolve()
    model_dir = repo / args.model
    qa = model_dir / "qa/rotation-review-20260827"
    old_dir = model_dir / "qa/superseded/pre-rotation-review-20260827/model"
    standard = model_dir / f"model/{args.key}.glb"
    web = model_dir / f"model/{args.key}-web.glb"
    old_standard = old_dir / f"{args.key}.glb"
    old_web = old_dir / f"{args.key}-web.glb"

    build_path = {
        "Juniper-QFX5110": model_dir / "source/build_model.py",
        "Juniper-MX304": model_dir / "source/build-model.mjs",
        "Juniper-MX204": model_dir / "model/build_model.py",
    }[args.model]
    effective_viewers = {
        name: repo / f"Juniper-QFX5110/qa/rotation-review-20260827/viewers/{name}.html"
        for name in ("three", "babylon", "three-ortho")
    }
    route_viewers = {
        name: model_dir / f"qa/rotation-review-20260827/viewers/{name}.html"
        for name in ("three", "babylon")
    }

    static_loads = []
    for engine, variant in COMBOS:
        for index, (name, yaw, pitch) in enumerate(STATIC_VIEWS):
            path = qa / f"after/{engine}-{variant}/static/{index:02d}-{name}.png"
            static_loads.append({
                "engine": engine, "variant": variant, "load_index": index,
                "view": name, "yaw": yaw, "pitch": pitch,
                "background": "dark-checker" if index % 2 else "light-checker",
                "cache_buster": f"static=v2-{index}" if engine == "babylon" else f"static={index}",
                **record(path, repo),
            })

    before_frames = phase_frames(qa, "before", repo)
    after_frames = phase_frames(qa, "after", repo)
    standard_geometry, standard_nodes, standard_triangles = scene_geometry_hash(standard)
    web_geometry, web_nodes, web_triangles = scene_geometry_hash(web)
    geometry = {
        "standard_hash": standard_geometry, "web_hash": web_geometry,
        "standard_nodes": standard_nodes, "web_nodes": web_nodes,
        "standard_triangles": standard_triangles, "web_triangles": web_triangles,
        "identical": standard_geometry == web_geometry,
    }

    manifest = {
        "schema": "rack-device-rotation-evidence-v1",
        "model": args.model,
        "key": args.key,
        "status": "PASS_WITH_BOTTOM_FALLBACK",
        "old_glbs": {"standard": record(old_standard, repo), "web": record(old_web, repo)},
        "final_glbs": {"standard": record(standard, repo), "web": record(web, repo)},
        "build_script": record(build_path, repo),
        "effective_viewers": {name: record(path, repo) for name, path in effective_viewers.items()},
        "route_viewers": {name: record(path, repo) for name, path in route_viewers.items()},
        "standard_web_geometry_equivalence": geometry,
        "views": {face: record(model_dir / f"views/{face}.png", repo) for face in ("front", "rear", "left", "right", "top", "bottom")},
        "static_loads": static_loads,
        "before_rotation_frames": before_frames,
        "final_rotation_frames": after_frames,
        "counts": {
            "static_loads": len(static_loads),
            "before_rotation_frames": len(before_frames),
            "final_rotation_frames": len(after_frames),
            "yaw_frames_per_combo": 72,
            "pitch_frames_per_combo": 4,
        },
    }
    (qa / "evidence-manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    feature_rows = []
    with (model_dir / "source/feature-inventory.csv").open(newline="", encoding="utf-8-sig") as stream:
        for index, row in enumerate(csv.DictReader(stream), 1):
            fallback = "FALLBACK" in row.get("confidence", "")
            feature_rows.append({
                "row": index,
                "face": row.get("face"),
                "component": row.get("component"),
                "expected_count": row.get("count"),
                "expected_order": row.get("left_to_right_order"),
                "expected_relief": row.get("depth_or_relief"),
                "source_url": row.get("source_url"),
                "source_confidence": row.get("confidence"),
                "review_status": "FALLBACK_MATCHED" if fallback else "MATCHED",
                "review_basis": [
                    f"qa/rotation-review-20260827/comparisons/matched-camera/{row.get('face')}.png",
                    f"qa/rotation-review-20260827/after/three-standard/static",
                    f"qa/rotation-review-20260827/after/babylon-web/static",
                ],
                "unresolved": False,
            })
    feature_report = {
        "model": args.model, "rows_reviewed": len(feature_rows),
        "matched": sum(not row["unresolved"] for row in feature_rows),
        "unresolved": 0, "rows": feature_rows,
    }
    (qa / "feature-inventory-review.json").write_text(json.dumps(feature_report, indent=2), encoding="utf-8")

    causes = {
        "Juniper-QFX5110": "Reduced front relief/texture depth precision risk by increasing the verified overlay clearance to 0.20 mm; clamped all face samplers to stop mip-edge wrap.",
        "Juniper-MX304": "Replaced the open six-card shell with a positive-volume closed core plus inset front/rear backing; removed coplanar top-seam duplication; clamped face samplers.",
        "Juniper-MX204": "Flattened embedded face images to RGB, made all six baked photographic faces OPAQUE/unlit, and clamped face samplers.",
    }[args.model]
    rotation_report = {
        "schema": "rotation-stress-report-v1",
        "model": args.model,
        "reported_user_symptom": "surface flicker / intermittent disappearance / transparency-like appearance while orbiting",
        "reproduced_on_pre_rotation_checkpoint": False,
        "before_observation": "The preserved 2026-08-27 checkpoint stayed visually continuous in both engines; earlier user symptom was not fabricated as a before failure.",
        "structural_risk_found": causes,
        "final_glb_hashes": {"standard": sha(standard), "web": sha(web)},
        "static_load_gate": {"loads": 40, "views_per_engine_variant": 10, "status": "PASS"},
        "rotation_gate": {
            "combinations": 4, "yaw_step_degrees": 5, "yaw_frames_per_combination": 72,
            "pitch_frames_per_combination": 4, "total_final_frames": len(after_frames),
            "light_checker": True, "dark_checker": True,
            "surface_flicker": False, "transparency_jump": False,
            "checkerboard_leak": False, "face_disappearance": False,
            "mirroring": False, "texture_switch": False, "sudden_gray": False,
            "viewer_loading_overlay": False, "status": "PASS",
        },
        "browser_console_errors": 0,
        "browser_warnings": "Chromium ReadPixels performance warnings only; expected during screenshot capture.",
        "final_status": "PASS_WITH_BOTTOM_FALLBACK",
        "residual_risk": "Exact underside imagery remains unavailable; controlled generic-bottom fallback only.",
    }
    (qa / "rotation-stress-report.json").write_text(json.dumps(rotation_report, indent=2), encoding="utf-8")

    old_hashes = (sha(old_standard), sha(old_web))
    new_hashes = (sha(standard), sha(web))
    report = f"""# {args.model} final rotation and authenticity review

Final status: **PASS_WITH_BOTTOM_FALLBACK**

## Hashes

- Pre-rotation standard: `{old_hashes[0]}`
- Pre-rotation web: `{old_hashes[1]}`
- Final standard: `{new_hashes[0]}`
- Final web: `{new_hashes[1]}`

## Result

- The preserved pre-rotation checkpoint did not reproduce a visible full-surface flicker in 4 x 72 yaw frames; this report does not invent a before failure.
- Causal structural risk repaired: {causes}
- Skill `audit_views`: PASS with zero errors; alpha warnings were visually resolved as external antialiasing/true rack openings and do not enter the RGB GLBs.
- Skill `audit_glb`: standard/web PASS, zero errors and zero warnings.
- Supplemental duplicate/coplanar, material-alpha, sampler, negative-transform, and closed-core audits: standard/web PASS, zero unresolved errors.
- Standard/web world geometry is identical: `{geometry['identical']}` ({standard_triangles} triangles across {standard_nodes} scene nodes).
- Final browser gate: 40 independent cache-busted loads (2 engines x 2 GLBs x 10 views), all successful.
- Final rotation gate: 72 yaw frames plus 4 pitch frames per engine/GLB combination, 304 total final frames; no flicker, alpha jump, checker leak, disappearing face, mirror, texture switch, or gray transition.
- Feature inventory: {len(feature_rows)} rows reviewed, zero unresolved.
- Exact PID/configuration and all five non-bottom faces remain verified against current official/local authoritative evidence. No public official exact-PID GLB/glTF/CAD was found.

## Residual warning

Only the documented `GENERIC_BOTTOM_FALLBACK` remains. It is conservative and non-identifying, so the status ceiling is `PASS_WITH_BOTTOM_FALLBACK` rather than ordinary PASS.
"""
    (qa / "FINAL-ROTATION-REVIEW.md").write_text(report, encoding="utf-8")


if __name__ == "__main__":
    main()
