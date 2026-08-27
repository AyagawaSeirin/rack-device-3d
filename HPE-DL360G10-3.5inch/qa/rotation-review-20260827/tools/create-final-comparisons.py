#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
from PIL import Image, ImageChops


CHECKER = [np.asarray((215, 219, 224), dtype=np.int16), np.asarray((159, 166, 173), dtype=np.int16)]


def render_mask(image: Image.Image):
    rgb = np.asarray(image.convert("RGB"), dtype=np.int16)
    distance = np.minimum(np.max(np.abs(rgb - CHECKER[0]), axis=2), np.max(np.abs(rgb - CHECKER[1]), axis=2))
    mask = distance > 18
    ys, xs = np.where(mask)
    if not len(xs):
        raise RuntimeError("render object mask is empty")
    return Image.fromarray((mask * 255).astype(np.uint8), "L"), (int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("views", type=Path)
    parser.add_argument("renders", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    for index, face in enumerate(("front", "rear", "left", "right", "top", "bottom"), 1):
        source = Image.open(args.views / f"{face}.png").convert("RGBA")
        render = Image.open(args.renders / f"{index:02d}-{face}.png").convert("RGB")
        mask, bbox = render_mask(render)
        width, height = render.size
        render_canvas = Image.new("RGB", render.size, "white")
        render_canvas.paste(render, (0, 0), mask)
        source_bbox = source.getchannel("A").point(lambda value: 255 if value >= 8 else 0).getbbox()
        source_crop = source.crop(source_bbox)
        target_size = (bbox[2] - bbox[0], bbox[3] - bbox[1])
        source_crop = source_crop.resize(target_size, Image.Resampling.LANCZOS)
        reference_canvas = Image.new("RGB", render.size, "white")
        reference_canvas.paste(source_crop.convert("RGB"), (bbox[0], bbox[1]), source_crop.getchannel("A"))
        overlay = Image.blend(reference_canvas, render_canvas, 0.5)
        difference = ImageChops.difference(reference_canvas, render_canvas)
        face_dir = args.output / face
        face_dir.mkdir(parents=True, exist_ok=True)
        reference_canvas.save(face_dir / "reference.png")
        render_canvas.save(face_dir / "render.png")
        overlay.save(face_dir / "overlay.png")
        difference.save(face_dir / "difference.png")
        sheet = Image.new("RGB", (width * 4, height), "white")
        for column, panel in enumerate((reference_canvas, render_canvas, overlay, difference)):
            sheet.paste(panel, (column * width, 0))
        sheet.save(face_dir / "sheet.png")
        print(f"{face}: render_bbox={bbox} source_bbox={source_bbox} target={target_size}")


if __name__ == "__main__":
    main()
