#!/usr/bin/env python3
"""Create source/render/overlay/difference evidence from final live GLB loads."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path

import numpy as np
from PIL import Image, ImageChops, ImageEnhance


FACES = ("front", "rear", "left", "right", "top", "bottom")
BACKGROUND = np.asarray(((227, 229, 232), (201, 205, 210)), dtype=np.int16)
CANVAS = (1200, 800)


def crop_source(path: Path) -> Image.Image:
    image = Image.open(path).convert("RGBA")
    bbox = image.getchannel("A").getbbox()
    if bbox is None:
        raise RuntimeError(f"empty source {path}")
    return image.crop(bbox)


def crop_render(path: Path, body_only_fraction: float | None = None) -> Image.Image:
    image = Image.open(path).convert("RGB")
    data = np.asarray(image)
    distances = np.min(np.linalg.norm(data[:, :, None, :].astype(np.int16) - BACKGROUND[None, None, :, :], axis=3), axis=2)
    mask = distances > 8
    mask[:55, :] = False
    ys, xs = np.nonzero(mask)
    if not len(xs):
        raise RuntimeError(f"no rendered object found in {path}")
    x0, x1, y0, y1 = int(xs.min()), int(xs.max()) + 1, int(ys.min()), int(ys.max()) + 1
    if body_only_fraction:
        width = x1 - x0
        trim = round(width * (1 - body_only_fraction) / 2)
        x0 += trim
        x1 -= trim
    cropped = data[y0:y1, x0:x1].copy()
    cropped_distances = distances[y0:y1, x0:x1]
    cropped[cropped_distances <= 8] = 255
    return Image.fromarray(cropped, "RGB").convert("RGBA")


def place(image: Image.Image, target_long: int) -> Image.Image:
    scale = min(target_long / image.width, (CANVAS[1] - 80) / image.height)
    size = (max(1, round(image.width * scale)), max(1, round(image.height * scale)))
    resized = image.resize(size, Image.Resampling.LANCZOS)
    canvas = Image.new("RGBA", CANVAS, (255, 255, 255, 255))
    canvas.alpha_composite(resized, ((CANVAS[0] - size[0]) // 2, (CANVAS[1] - size[1]) // 2))
    return canvas.convert("RGB")


def sheet(source: Image.Image, render: Image.Image) -> tuple[Image.Image, Image.Image, Image.Image]:
    overlay = Image.blend(source, render, 0.5)
    difference = ImageEnhance.Contrast(ImageChops.difference(source, render)).enhance(2.0)
    combined = Image.new("RGB", (CANVAS[0] * 4, CANVAS[1]), "white")
    for index, panel in enumerate((source, render, overlay, difference)):
        combined.paste(panel, (index * CANVAS[0], 0))
    return overlay, difference, combined


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("device", type=Path)
    parser.add_argument("--ce-front-body-only", action="store_true")
    args = parser.parse_args()
    review = args.device / "qa" / "rotation-review-20260827"
    output = review / "matched-camera"
    rows = []
    for viewer in ("three", "babylon"):
        for face in FACES:
            source_raw = crop_source(args.device / "views" / f"{face}.png")
            body_fraction = 442.0 / 482.6 if args.ce_front_body_only and face == "front" else None
            render_raw = crop_render(review / "static-40-loads" / viewer / "standard" / f"{face}.png", body_fraction)
            source = place(source_raw, 1080)
            render = place(render_raw, 1080)
            overlay, difference, combined = sheet(source, render)
            directory = output / viewer / face
            directory.mkdir(parents=True, exist_ok=True)
            source.save(directory / "source.png")
            render.save(directory / "render.png")
            overlay.save(directory / "overlay.png")
            difference.save(directory / "difference.png")
            combined.save(directory / "comparison.png")
            rows.append({"viewer": viewer, "face": face, "source": str(directory / "source.png"), "render": str(directory / "render.png"), "overlay": str(directory / "overlay.png"), "difference": str(directory / "difference.png"), "comparison": str(directory / "comparison.png")})
    with (output / "comparison-index.csv").open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    main()
