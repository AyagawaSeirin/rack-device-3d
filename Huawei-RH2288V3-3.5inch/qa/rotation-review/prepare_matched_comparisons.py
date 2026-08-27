#!/usr/bin/env python3
"""Fit locked elevation sources to the final GLB's canonical camera bounds."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import numpy as np
from PIL import Image


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "qa" / "rotation-review" / "after" / "matched-camera"
FACES = ("front", "rear", "left", "right", "top", "bottom")
HELPER = ROOT.parent / ".agents" / "skills" / "rack-device-3d-model-assets" / "scripts" / "create_comparison_sheet.py"


def source_path(face: str) -> Path:
    if ROOT.name == "Huawei-RH2288V3-3.5inch":
        return ROOT / "qa" / "reference" / f"{face}.png"
    if ROOT.name == "Huawei-CE6851":
        return ROOT / "views" / f"{face}.png"
    if ROOT.name == "Fortinet-FG1500D":
        return ROOT / "qa" / "reference" / f"{face}-1200x720.png"
    raise ValueError(f"unsupported scoped model: {ROOT.name}")


def content_bbox(image: Image.Image, *, white_render: bool) -> tuple[int, int, int, int]:
    rgba = np.asarray(image.convert("RGBA"))
    alpha = rgba[:, :, 3]
    if alpha.min() < 255:
        mask = alpha > 8
    else:
        rgb = rgba[:, :, :3].astype(np.int16)
        if white_render:
            background = np.array([255, 255, 255], dtype=np.int16)
        else:
            corners = np.stack((rgb[0, 0], rgb[0, -1], rgb[-1, 0], rgb[-1, -1]))
            background = np.median(corners, axis=0)
        mask = np.max(np.abs(rgb - background), axis=2) > 12
    ys, xs = np.nonzero(mask)
    if not len(xs):
        raise ValueError("no visible source/render content")
    return int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1


def main() -> int:
    summaries = []
    for face in FACES:
        render_path = OUT / "render" / f"{face}.png"
        source = Image.open(source_path(face)).convert("RGBA")
        render = Image.open(render_path).convert("RGB")
        render_bbox = content_bbox(render, white_render=True)
        source_bbox = content_bbox(source, white_render=False)
        source = source.crop(source_bbox)
        target_width = render_bbox[2] - render_bbox[0]
        target_height = render_bbox[3] - render_bbox[1]
        scale = min(target_width / source.width, target_height / source.height)
        source = source.resize(
            (max(1, round(source.width * scale)), max(1, round(source.height * scale))),
            Image.Resampling.LANCZOS,
        )
        canvas = Image.new("RGBA", render.size, (255, 255, 255, 255))
        center_x = (render_bbox[0] + render_bbox[2]) / 2
        center_y = (render_bbox[1] + render_bbox[3]) / 2
        x = round(center_x - source.width / 2)
        y = round(center_y - source.height / 2)
        canvas.alpha_composite(source, (x, y))
        matched_path = OUT / "reference" / f"{face}.png"
        canvas.convert("RGB").save(matched_path)
        comparison_path = OUT / "comparisons" / f"{face}.png"
        result = subprocess.run(
            [sys.executable, str(HELPER), str(matched_path), str(render_path), str(comparison_path)],
            check=True,
            capture_output=True,
            text=True,
        )
        entry = json.loads(result.stdout)
        entry.update({"face": face, "source": str(source_path(face)), "render_bbox": list(render_bbox)})
        summaries.append(entry)
    (OUT / "comparison-metrics.json").write_text(
        json.dumps({"model": ROOT.name, "method": "canonical camera; locked source fit to final render bounds without stretching", "faces": summaries}, indent=2) + "\n",
        encoding="utf-8",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
