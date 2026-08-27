#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
from PIL import Image


def robust_limit(values, floor):
    values = np.asarray(values, dtype=float)
    median = float(np.median(values))
    mad = float(np.median(np.abs(values - median)))
    return max(floor, median + 8.0 * max(mad, 1e-9)), median, mad


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("combo", type=Path)
    parser.add_argument("--json-out", type=Path, required=True)
    args = parser.parse_args()
    files = sorted((args.combo / "yaw-frames").glob("*.jpg"))
    arrays = [np.asarray(Image.open(path).convert("RGB"), dtype=np.float32) for path in files]
    sizes = [list(array.shape[:2][::-1]) for array in arrays]
    checker = [np.asarray((215, 219, 224), dtype=np.float32), np.asarray((159, 166, 173), dtype=np.float32)]
    frame_metrics = []
    for path, array in zip(files, arrays):
        distances = np.minimum(np.max(np.abs(array - checker[0]), axis=2), np.max(np.abs(array - checker[1]), axis=2))
        object_mask = distances > 20
        dark_overlay = np.max(np.abs(array - np.asarray((37, 42, 48), dtype=np.float32)), axis=2) < 18
        pixels = array[object_mask] if np.any(object_mask) else array.reshape(-1, 3)
        frame_metrics.append({
            "file": path.name,
            "objectFraction": float(np.mean(object_mask)),
            "objectMeanRGB": [float(value) for value in np.mean(pixels, axis=0)],
            "objectMeanLuma": float(np.mean(pixels @ np.asarray((0.2126, 0.7152, 0.0722), dtype=np.float32))),
            "darkOverlayFraction": float(np.mean(dark_overlay)),
        })
    adjacent = []
    if arrays:
        for index in range(len(arrays)):
            other = (index + 1) % len(arrays)
            adjacent.append({
                "from": files[index].name,
                "to": files[other].name,
                "pixelMAE": float(np.mean(np.abs(arrays[index] - arrays[other]))),
                "objectFractionDelta": float(abs(frame_metrics[index]["objectFraction"] - frame_metrics[other]["objectFraction"])),
                "objectLumaDelta": float(abs(frame_metrics[index]["objectMeanLuma"] - frame_metrics[other]["objectMeanLuma"])),
            })
    mae_limit, mae_median, mae_mad = robust_limit([item["pixelMAE"] for item in adjacent], 18.0) if adjacent else (0, 0, 0)
    area_limit, area_median, area_mad = robust_limit([item["objectFractionDelta"] for item in adjacent], 0.05) if adjacent else (0, 0, 0)
    luma_limit, luma_median, luma_mad = robust_limit([item["objectLumaDelta"] for item in adjacent], 18.0) if adjacent else (0, 0, 0)
    anomalies = [item for item in adjacent if item["pixelMAE"] > mae_limit or item["objectFractionDelta"] > area_limit or item["objectLumaDelta"] > luma_limit]
    overlay_frames = [item["file"] for item in frame_metrics if item["darkOverlayFraction"] > 0.85]
    errors = []
    if len(files) != 72:
        errors.append(f"expected 72 yaw frames, found {len(files)}")
    if len({tuple(size) for size in sizes}) > 1:
        errors.append("yaw frame dimensions are inconsistent")
    if overlay_frames:
        errors.append("loading overlay pixels dominate one or more frames")
    if anomalies:
        errors.append("abrupt adjacent-frame discontinuity exceeds robust thresholds")
    result = {
        "combo": str(args.combo),
        "frameCount": len(files),
        "uniformSize": sizes[0] if sizes and len({tuple(size) for size in sizes}) == 1 else None,
        "thresholds": {
            "pixelMAE": {"limit": mae_limit, "median": mae_median, "mad": mae_mad},
            "objectFractionDelta": {"limit": area_limit, "median": area_median, "mad": area_mad},
            "objectLumaDelta": {"limit": luma_limit, "median": luma_median, "mad": luma_mad},
        },
        "overlayFrames": overlay_frames,
        "anomalies": anomalies,
        "frames": frame_metrics,
        "adjacent": adjacent,
        "errors": errors,
        "errorCount": len(errors),
        "status": "PASS" if not errors else "REVIEW",
    }
    args.json_out.parent.mkdir(parents=True, exist_ok=True)
    args.json_out.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"combo": str(args.combo), "status": result["status"], "errorCount": len(errors), "anomalyCount": len(anomalies)}, indent=2))


if __name__ == "__main__":
    main()
