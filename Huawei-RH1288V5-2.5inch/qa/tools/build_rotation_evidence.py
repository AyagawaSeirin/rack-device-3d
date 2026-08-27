#!/usr/bin/env python3
"""Build deterministic manifests and contact sheets for orbit-stress captures."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def pixels(path: Path, size=(160, 120)) -> np.ndarray:
    return np.asarray(Image.open(path).convert("RGB").resize(size, Image.Resampling.BILINEAR), dtype=np.float32)


def sheet(paths: list[Path], output: Path, columns: int, thumb=(200, 150)) -> None:
    label_h = 20
    rows = (len(paths) + columns - 1) // columns
    canvas = Image.new("RGB", (columns * thumb[0], rows * (thumb[1] + label_h)), (40, 43, 47))
    draw = ImageDraw.Draw(canvas)
    for index, path in enumerate(paths):
        row, column = divmod(index, columns)
        image = Image.open(path).convert("RGB")
        image.thumbnail(thumb, Image.Resampling.LANCZOS)
        x = column * thumb[0] + (thumb[0] - image.width) // 2
        y = row * (thumb[1] + label_h) + (thumb[1] - image.height) // 2
        canvas.paste(image, (x, y))
        draw.text((column * thumb[0] + 4, row * (thumb[1] + label_h) + thumb[1] + 3), path.stem, fill=(235, 237, 239))
    output.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(output, optimize=True)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("combo_dir", type=Path)
    args = parser.parse_args()
    root = args.combo_dir
    yaw_paths = sorted((root / "yaw-light").glob("yaw-*.jpg"))
    pitch_light = sorted((root / "pitch-light").glob("*.jpg"))
    pitch_dark = sorted((root / "pitch-dark").glob("*.jpg"))
    runtime_path = root / "runtime-state.json"
    runtime = json.loads(runtime_path.read_text(encoding="utf-8")) if runtime_path.exists() else {}

    records = []
    arrays = []
    for path in yaw_paths:
        array = pixels(path)
        arrays.append(array)
        records.append({
            "file": str(path.relative_to(root)),
            "yaw_degrees": int(path.stem.split("-")[1]),
            "pitch_degrees": 12,
            "background": "light-checker",
            "sha256": sha256(path),
            "size_px": list(Image.open(path).size),
            "mean_rgb": [round(float(value), 4) for value in array.mean(axis=(0, 1))],
        })
    diffs = []
    if arrays:
        for index in range(len(arrays)):
            following = arrays[(index + 1) % len(arrays)]
            diffs.append(float(np.mean(np.abs(arrays[index] - following))))
    median = float(np.median(diffs)) if diffs else 0.0
    mad = float(np.median(np.abs(np.asarray(diffs) - median))) if diffs else 0.0
    threshold = max(median + 8.0 * max(mad, 0.15), median * 2.0, 6.0)
    abrupt = [
        {"from_yaw": records[i]["yaw_degrees"], "to_yaw": records[(i + 1) % len(records)]["yaw_degrees"], "mean_abs_rgb_delta": round(value, 5)}
        for i, value in enumerate(diffs) if value > threshold
    ]
    for record, value in zip(records, diffs):
        record["next_frame_mean_abs_rgb_delta"] = round(value, 5)

    pitch_records = []
    dark_by_name = {p.name: p for p in pitch_dark}
    checker_pairs = []
    for light in pitch_light:
        dark = dark_by_name.get(light.name)
        item = {"light_file": str(light.relative_to(root)), "light_sha256": sha256(light)}
        if dark:
            light_array, dark_array = pixels(light), pixels(dark)
            delta = np.mean(np.abs(light_array - dark_array), axis=2)
            item.update({
                "dark_file": str(dark.relative_to(root)),
                "dark_sha256": sha256(dark),
                "paired_mean_abs_rgb_delta": round(float(delta.mean()), 5),
                "stable_surface_pixel_percent": round(float(np.mean(delta < 12.0) * 100.0), 5),
            })
            checker_pairs.extend([light, dark])
        pitch_records.append(item)

    material_failures = []
    for material in runtime.get("materials", []):
        if runtime.get("viewer") == "three":
            if material.get("transparent") or material.get("opacity") != 1 or material.get("side") != 0 or not material.get("depthWrite", True):
                material_failures.append(material)
        elif runtime.get("viewer") == "babylon":
            if material.get("alpha") != 1 or material.get("needAlphaBlending") or material.get("backFaceCulling") is False:
                material_failures.append(material)

    report = {
        "combo_dir": str(root),
        "runtime_state": runtime,
        "capture_counts": {"yaw_light": len(yaw_paths), "pitch_light": len(pitch_light), "pitch_dark": len(pitch_dark), "total": len(yaw_paths) + len(pitch_light) + len(pitch_dark)},
        "yaw_step_degrees": 5,
        "yaw_frame_manifest": records,
        "pitch_checker_pair_manifest": pitch_records,
        "sequence_delta": {
            "median_mean_abs_rgb_delta": round(median, 5),
            "mad": round(mad, 5),
            "candidate_threshold": round(threshold, 5),
            "abrupt_frame_candidates": abrupt,
        },
        "runtime_material_failures": material_failures,
        "automated_gate": {
            "webgl2": runtime.get("webgl2") is True,
            "correct_frame_counts": len(yaw_paths) == 72 and len(pitch_light) == 12 and len(pitch_dark) == 12,
            "no_runtime_errors": not runtime.get("errors"),
            "no_runtime_material_failures": not material_failures,
            "no_abrupt_frame_candidates": not abrupt,
        },
        "manual_review_required": ["yaw contact sheet", "light/dark pitch-pair contact sheet", "surface continuity, mirror, gray-shift, disappearance, checker leakage"],
    }
    report["automated_pass"] = all(report["automated_gate"].values())
    (root / "frame-manifest.json").write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    sheet(yaw_paths, root / "yaw-contact-sheet.png", 12)
    sheet(checker_pairs, root / "checker-pair-contact-sheet.png", 8)
    print(json.dumps({"combo_dir": str(root), "counts": report["capture_counts"], "sequence_delta": report["sequence_delta"], "automated_gate": report["automated_gate"], "automated_pass": report["automated_pass"]}, indent=2))


if __name__ == "__main__":
    main()
