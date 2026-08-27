#!/usr/bin/env python3
"""Register canonical six-face PNGs to the frozen Three.js standard camera canvases."""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

from PIL import Image


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
FACES = ("front", "rear", "left", "right", "top", "bottom")


def tiled_background(render: Image.Image, tile_size: int = 28) -> Image.Image:
    tile = render.crop((0, 0, tile_size, tile_size))
    canvas = Image.new("RGB", render.size)
    for y in range(0, render.height, tile_size):
        for x in range(0, render.width, tile_size):
            canvas.paste(tile, (x, y))
    return canvas


def render_bounds(render: Image.Image) -> tuple[int, int, int, int]:
    rgb = render.convert("RGB")
    counts = Counter(rgb.getdata())
    background = {color for color, count in counts.most_common(8) if count > rgb.width * rgb.height * 0.01}
    mask = Image.new("1", rgb.size)
    mask.putdata([pixel not in background for pixel in rgb.getdata()])
    bounds = mask.getbbox()
    if bounds is None:
        raise RuntimeError("render foreground could not be located")
    return bounds


def source_crop(source: Image.Image) -> Image.Image:
    rgba = source.convert("RGBA")
    alpha_bounds = rgba.getchannel("A").getbbox()
    if alpha_bounds is None:
        raise RuntimeError("canonical source is fully transparent")
    return rgba.crop(alpha_bounds)


def main() -> None:
    output_dir = HERE / "matched-camera" / "source-canvas"
    output_dir.mkdir(parents=True, exist_ok=True)
    records = []
    for face in FACES:
        render_path = HERE / "orthographic" / "three-standard" / f"{face}.png"
        source_path = ROOT / "views" / f"{face}.png"
        with Image.open(render_path) as raw_render, Image.open(source_path) as raw_source:
            render = raw_render.convert("RGB")
            bounds = render_bounds(render)
            source = source_crop(raw_source)
            target_width = bounds[2] - bounds[0]
            target_height = bounds[3] - bounds[1]
            scale = min(target_width / source.width, target_height / source.height)
            fitted = source.resize(
                (max(1, round(source.width * scale)), max(1, round(source.height * scale))),
                Image.Resampling.LANCZOS,
            )
            center_x = (bounds[0] + bounds[2]) / 2
            center_y = (bounds[1] + bounds[3]) / 2
            paste_x = round(center_x - fitted.width / 2)
            paste_y = round(center_y - fitted.height / 2)
            canvas = tiled_background(render).convert("RGBA")
            canvas.alpha_composite(fitted, (paste_x, paste_y))
            output_path = output_dir / f"{face}.png"
            canvas.convert("RGB").save(output_path)
            records.append({
                "face": face,
                "canonical": str(source_path.relative_to(ROOT)),
                "render": str(render_path.relative_to(ROOT)),
                "output": str(output_path.relative_to(ROOT)),
                "renderBoundsPx": list(bounds),
                "canonicalCropPx": [source.width, source.height],
                "registeredSizePx": [fitted.width, fitted.height],
                "registration": "aspect-preserving contain at the actual rendered silhouette center; no stretching",
            })
    manifest = {
        "model": ROOT.name,
        "camera": "Three.js standard frozen viewer; front/rear/left/right pitch 0; top/bottom pitch +/-89.9",
        "canvasPx": [640, 400],
        "background": "exact 28 px checker tile sampled from the corresponding actual render",
        "records": records,
        "status": "PASS" if len(records) == 6 else "REWORK",
    }
    (HERE / "matched-camera" / "registration.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"model": ROOT.name, "status": manifest["status"], "faces": len(records)}, indent=2))


if __name__ == "__main__":
    main()
