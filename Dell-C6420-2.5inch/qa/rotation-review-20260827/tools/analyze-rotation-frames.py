#!/usr/bin/env python3
"""Analyze orbit continuity, checker opacity, overlays and same-angle stability."""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path

import numpy as np
from PIL import Image


LIGHT = (np.asarray((215, 219, 224), dtype=np.float32), np.asarray((159, 166, 173), dtype=np.float32))
DARK = (np.asarray((61, 66, 72), dtype=np.float32), np.asarray((24, 28, 32), dtype=np.float32))


def load(path: Path) -> np.ndarray:
    return np.asarray(Image.open(path).convert("RGB"), dtype=np.float32)


def distance_to_checker(array: np.ndarray, colors) -> np.ndarray:
    return np.minimum(*(np.max(np.abs(array - color), axis=2) for color in colors))


def erode(mask: np.ndarray, iterations: int = 2) -> np.ndarray:
    core = mask.copy()
    for _ in range(iterations):
        core = core & np.roll(core, 1, 0) & np.roll(core, -1, 0) & np.roll(core, 1, 1) & np.roll(core, -1, 1)
        core[[0, -1], :] = False
        core[:, [0, -1]] = False
    return core


def robust_limit(values, floor):
    values = np.asarray(values, dtype=float)
    median = float(np.median(values))
    mad = float(np.median(np.abs(values - median)))
    return max(floor, median + 8.0 * max(mad, 1e-9)), median, mad


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("combo", type=Path)
    parser.add_argument("--json-out", type=Path, required=True)
    args = parser.parse_args()
    manifest = json.loads((args.combo / "rotation-manifest.json").read_text())
    yaw_files = sorted((args.combo / "yaw-frames").glob("*.png"))
    yaw_arrays = [load(path) for path in yaw_files]
    metrics = []
    for path, array in zip(yaw_files, yaw_arrays):
        object_mask = distance_to_checker(array, LIGHT) > 20
        overlay = np.max(np.abs(array - np.asarray((37, 42, 48), dtype=np.float32)), axis=2) < 18
        pixels = array[object_mask] if np.any(object_mask) else array.reshape(-1, 3)
        metrics.append({
            "file": path.name,
            "objectFraction": float(np.mean(object_mask)),
            "objectMeanRGB": [float(value) for value in np.mean(pixels, axis=0)],
            "objectMeanLuma": float(np.mean(pixels @ np.asarray((.2126, .7152, .0722), dtype=np.float32))),
            "overlayFraction": float(np.mean(overlay)),
        })
    adjacent = []
    for index in range(len(yaw_arrays)):
        other = (index + 1) % len(yaw_arrays)
        adjacent.append({
            "from": yaw_files[index].name,
            "to": yaw_files[other].name,
            "pixelMAE": float(np.mean(np.abs(yaw_arrays[index] - yaw_arrays[other]))),
            "objectFractionDelta": float(abs(metrics[index]["objectFraction"] - metrics[other]["objectFraction"])),
            "objectLumaDelta": float(abs(metrics[index]["objectMeanLuma"] - metrics[other]["objectMeanLuma"])),
        })
    mae_limit, mae_median, mae_mad = robust_limit([x["pixelMAE"] for x in adjacent], 18.0) if adjacent else (0, 0, 0)
    area_limit, area_median, area_mad = robust_limit([x["objectFractionDelta"] for x in adjacent], .05) if adjacent else (0, 0, 0)
    luma_limit, luma_median, luma_mad = robust_limit([x["objectLumaDelta"] for x in adjacent], 18.0) if adjacent else (0, 0, 0)
    anomalies = [x for x in adjacent if x["pixelMAE"] > mae_limit or x["objectFractionDelta"] > area_limit or x["objectLumaDelta"] > luma_limit]

    stable_groups = defaultdict(list)
    for record in manifest["frames"]:
        if record["kind"] == "stable":
            stable_groups[(record["checker"], record["yaw"], record["pitch"])].append(args.combo / record["filename"])
    stable_results = []
    for key, files in sorted(stable_groups.items()):
        arrays = [load(path) for path in sorted(files)]
        pair_mae = [float(np.mean(np.abs(arrays[0] - item))) for item in arrays[1:]]
        pair_max = [float(np.max(np.abs(arrays[0] - item))) for item in arrays[1:]]
        stable_results.append({"checker": key[0], "yaw": key[1], "pitch": key[2], "samples": len(arrays), "maxMAE": max(pair_mae, default=0), "maxPixelDelta": max(pair_max, default=0)})
    unstable = [x for x in stable_results if x["samples"] != 3 or x["maxMAE"] > .02 or x["maxPixelDelta"] > 2]

    checker_pairs = []
    pitch = {(x["checker"], x["yaw"], x["pitch"]): args.combo / x["filename"] for x in manifest["frames"] if x["kind"] == "pitch-checker"}
    for yaw in (0, 90, 180, 270):
        for pitch_value in (-35, -15, 15, 35):
            light, dark = load(pitch[("light", yaw, pitch_value)]), load(pitch[("dark", yaw, pitch_value)])
            object_mask = erode((distance_to_checker(light, LIGHT) > 24) & (distance_to_checker(dark, DARK) > 24))
            delta = np.max(np.abs(light - dark), axis=2)
            changed = float(np.mean(delta[object_mask] > 12)) if np.any(object_mask) else 1.0
            checker_pairs.append({"yaw": yaw, "pitch": pitch_value, "objectPixels": int(np.sum(object_mask)), "objectChangedFraction": changed, "objectMedianDelta": float(np.median(delta[object_mask])) if np.any(object_mask) else 255.0})
    checker_failures = [x for x in checker_pairs if x["objectPixels"] == 0 or x["objectChangedFraction"] > .05 or x["objectMedianDelta"] > 2]

    overlay_frames = [x["file"] for x in metrics if x["overlayFraction"] > .85]
    expected_files = {x["filename"] for x in manifest["frames"]}
    missing = sorted(name for name in expected_files if not (args.combo / name).is_file())
    runtime = manifest.get("runtime", {})
    errors = []
    if len(yaw_files) != 72 or manifest.get("yawFrames") != 72 or manifest.get("yawStepDegrees") != 5: errors.append("72 x 5-degree yaw contract failed")
    if manifest.get("pitchCheckerFrames") != 32: errors.append("multi-pitch light/dark checker contract failed")
    if manifest.get("stableFrames") != 18 or len(stable_groups) != 6: errors.append("same-angle stable-frame contract failed")
    if missing: errors.append("manifest screenshots are missing")
    if not runtime.get("webgl2"): errors.append("viewer is not WebGL2")
    if runtime.get("overlayVisible"): errors.append("loading overlay visible at capture")
    if overlay_frames: errors.append("loading overlay pixels dominate yaw frames")
    if anomalies: errors.append("abrupt yaw-frame discontinuity exceeds robust limits")
    if unstable: errors.append("same-angle frames are not stable")
    if checker_failures: errors.append("model appearance changes with checker depth/brightness")
    result = {
        "combo": str(args.combo), "runtime": runtime, "frameCount": len(expected_files),
        "yaw": {"count": len(yaw_files), "thresholds": {"pixelMAE": {"limit": mae_limit, "median": mae_median, "mad": mae_mad}, "objectFractionDelta": {"limit": area_limit, "median": area_median, "mad": area_mad}, "objectLumaDelta": {"limit": luma_limit, "median": luma_median, "mad": luma_mad}}, "anomalies": anomalies, "frames": metrics, "adjacent": adjacent},
        "stable": {"groups": stable_results, "failures": unstable},
        "checkerOpacity": {"pairs": checker_pairs, "failures": checker_failures},
        "overlayFrames": overlay_frames, "missingFiles": missing,
        "errors": errors, "errorCount": len(errors), "status": "PASS" if not errors else "REVIEW",
    }
    args.json_out.parent.mkdir(parents=True, exist_ok=True)
    args.json_out.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"combo": str(args.combo), "status": result["status"], "errorCount": len(errors), "yawAnomalies": len(anomalies), "stableFailures": len(unstable), "checkerFailures": len(checker_failures)}, indent=2))


if __name__ == "__main__":
    main()
