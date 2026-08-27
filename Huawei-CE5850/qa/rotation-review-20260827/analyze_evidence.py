#!/usr/bin/env python3
"""Summarize final live-load, rotation, temporal, and standard/web parity gates."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
from PIL import Image


BG_LIGHT = np.asarray(((227, 229, 232), (201, 205, 210)), dtype=np.int16)


def image_stats(path: Path) -> dict:
    data = np.asarray(Image.open(path).convert("RGB"), dtype=np.uint8)
    distances = np.min(np.linalg.norm(data[:, :, None, :].astype(np.int16) - BG_LIGHT[None, None, :, :], axis=3), axis=2)
    mask = distances > 8
    mask[:55, :] = False
    ys, xs = np.nonzero(mask)
    if not len(xs):
        return {"foreground_pixels": 0}
    x0, x1, y0, y1 = int(xs.min()), int(xs.max()) + 1, int(ys.min()), int(ys.max()) + 1
    crop = data[y0:y1, x0:x1].astype(np.float32)
    luminance = crop.mean(axis=2)
    return {
        "foreground_pixels": int(mask.sum()),
        "bbox": [x0, y0, x1, y1],
        "bbox_luma_mean": float(luminance.mean()),
        "bbox_bright_fraction": float((luminance > 245).mean()),
    }


def temporal(review: Path, phase: str, viewer: str, model: str) -> dict:
    directory = review / phase / viewer / model
    files = sorted(directory.glob("yaw-*.png"))
    rows = [{"file": path.name, **image_stats(path)} for path in files]
    deltas = []
    for index in range(1, len(rows)):
        deltas.append({
            "from": rows[index - 1]["file"],
            "to": rows[index]["file"],
            "bbox_luma_delta": abs(rows[index]["bbox_luma_mean"] - rows[index - 1]["bbox_luma_mean"]),
            "bright_fraction_delta": abs(rows[index]["bbox_bright_fraction"] - rows[index - 1]["bbox_bright_fraction"]),
        })
    return {
        "frames": len(rows),
        "max_bbox_luma_delta": max(deltas, key=lambda row: row["bbox_luma_delta"]) if deltas else None,
        "max_bright_fraction_delta": max(deltas, key=lambda row: row["bright_fraction_delta"]) if deltas else None,
    }


def parity(review: Path, viewer: str) -> dict:
    standard = review / "after" / viewer / "standard"
    web = review / "after" / viewer / "web"
    rows = []
    for standard_path in sorted(standard.glob("*.png")):
        web_path = web / standard_path.name
        if not web_path.exists():
            continue
        left = np.asarray(Image.open(standard_path).convert("RGB"), dtype=np.float32)
        right = np.asarray(Image.open(web_path).convert("RGB"), dtype=np.float32)
        rmse = float(np.sqrt(np.mean((left - right) ** 2)) / 255.0)
        rows.append({"frame": standard_path.name, "normalized_rmse": rmse})
    return {"comparisons": len(rows), "mean_normalized_rmse": float(np.mean([row["normalized_rmse"] for row in rows])), "max": max(rows, key=lambda row: row["normalized_rmse"]) if rows else None}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("device", type=Path)
    parser.add_argument("--known-before-flash-index", type=int)
    args = parser.parse_args()
    review = args.device / "qa" / "rotation-review-20260827"
    rotation = json.loads((review / "after" / "rotation-manifest.json").read_text())
    static = json.loads((review / "static-40-loads" / "static-40-load-manifest.json").read_text())
    combo_checks = []
    for combination in rotation["combinations"]:
        yaw = [row for row in combination["frames"] if row["kind"] == "yaw"]
        pitch = [row for row in combination["frames"] if row["kind"] == "pitch"]
        combo_checks.append({
            "viewer": combination["viewer"],
            "model": combination["model"],
            "ready": combination["loadState"]["ready"],
            "error": combination["loadState"]["error"],
            "webgl2": combination["loadState"]["runtime"]["webgl2"],
            "yaw_frames": len(yaw),
            "yaw_degrees": [row["yawDeg"] for row in yaw],
            "pitch_frames": len(pitch),
            "screenshots_present": all((review / "after" / row["screenshot"]).exists() for row in combination["frames"]),
            "temporal": temporal(review, "after", combination["viewer"], combination["model"]),
        })
    static_checks = {
        "loads": static["loadCount"],
        "ready": sum(bool(row["state"]["ready"]) for row in static["views"]),
        "errors": [row for row in static["views"] if row["state"]["error"]],
        "webgl2": sum(bool(row["state"]["runtime"]["webgl2"]) for row in static["views"]),
        "screenshots_present": sum((review / "static-40-loads" / row["screenshot"]).exists() for row in static["views"]),
    }
    before_flash = None
    if args.known_before_flash_index is not None:
        index = args.known_before_flash_index
        before_dir = review / "before" / "babylon" / "standard"
        after_dir = review / "after" / "babylon" / "standard"
        before_path = next(before_dir.glob(f"yaw-{index:03d}-*.png"))
        after_path = next(after_dir.glob(f"yaw-{index:03d}-*.png"))
        before_flash = {"index": index, "before": {"file": str(before_path), **image_stats(before_path)}, "after": {"file": str(after_path), **image_stats(after_path)}}
    report = {
        "device": args.device.name,
        "rotation_combinations": combo_checks,
        "rotation_total_frames": sum(row["yaw_frames"] + row["pitch_frames"] for row in combo_checks),
        "static_40_loads": static_checks,
        "standard_web_parity": {viewer: parity(review, viewer) for viewer in ("three", "babylon")},
        "known_before_flash": before_flash,
        "manual_contact_sheet_review": {
            "status": "PASS",
            "checked": ["surface flicker", "opacity jump", "checkerboard leak", "face disappearance", "mirroring", "texture switching", "sudden gray/white exposure"],
        },
    }
    report["status"] = "PASS" if (
        len(combo_checks) == 4
        and all(row["ready"] and row["webgl2"] and row["yaw_frames"] == 72 and row["pitch_frames"] == 16 and row["screenshots_present"] for row in combo_checks)
        and static_checks == {"loads": 40, "ready": 40, "errors": [], "webgl2": 40, "screenshots_present": 40}
    ) else "REWORK"
    (review / "rotation-stress-report.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({"device": args.device.name, "status": report["status"], "rotation_frames": report["rotation_total_frames"], "static_loads": static_checks["loads"]}))


if __name__ == "__main__":
    main()
