#!/usr/bin/env python3
"""Tight-crop chroma-key outputs, preserve aspect ratio, and emit alpha QA."""

from __future__ import annotations

import json
import sys
from pathlib import Path

from PIL import Image, ImageDraw


ROOT = Path(__file__).resolve().parents[2]
RATIOS = {
    "front": 482.6 / 43.2,
    "rear": 434.7 / 43.2,
    "left": 698.5 / 43.2,
    "right": 698.5 / 43.2,
    "top": 434.7 / 698.5,
    "bottom": 434.7 / 698.5,
}
LONG_EDGE = {
    "front": 3072,
    "rear": 3072,
    "left": 3072,
    "right": 3072,
    "top": 2048,
    "bottom": 2048,
}


def alpha_bbox(im: Image.Image, threshold: int = 8) -> tuple[int, int, int, int]:
    alpha = im.getchannel("A").point(lambda value: 255 if value > threshold else 0)
    bbox = alpha.getbbox()
    if not bbox:
        raise ValueError("no non-transparent content")
    return bbox


def pad_to_ratio(im: Image.Image, target_ratio: float) -> Image.Image:
    width, height = im.size
    ratio = width / height
    if ratio < target_ratio:
        out_width = int(round(height * target_ratio))
        out_height = height
    else:
        out_width = width
        out_height = int(round(width / target_ratio))
    out = Image.new("RGBA", (out_width, out_height), (0, 0, 0, 0))
    out.alpha_composite(im, ((out_width - width) // 2, (out_height - height) // 2))
    return out


def checkerboard(im: Image.Image, max_edge: int = 1400) -> Image.Image:
    scale = min(1.0, max_edge / max(im.size))
    preview = im.resize(
        (max(1, round(im.width * scale)), max(1, round(im.height * scale))),
        Image.Resampling.LANCZOS,
    )
    tile = max(8, min(preview.size) // 12)
    bg = Image.new("RGBA", preview.size, (238, 238, 238, 255))
    draw = ImageDraw.Draw(bg)
    for y in range(0, preview.height, tile):
        for x in range(0, preview.width, tile):
            if ((x // tile) + (y // tile)) % 2:
                draw.rectangle((x, y, x + tile - 1, y + tile - 1), fill=(188, 188, 188, 255))
    bg.alpha_composite(preview)
    return bg.convert("RGB")


def finalize(face: str) -> dict:
    source = ROOT / "qa" / "work" / f"{face}-alpha.png"
    target = ROOT / "views" / f"{face}.png"
    preview_path = ROOT / "qa" / "reference" / f"{face}-checkerboard.png"
    im = Image.open(source).convert("RGBA")
    bbox = alpha_bbox(im)
    im = im.crop(bbox)

    # Keep only legitimate anti-aliased edge alpha. Interior/high-alpha pixels are opaque.
    rgba = list(im.getdata())
    hardened = []
    for red, green, blue, alpha in rgba:
        if alpha >= 245:
            alpha = 255
        elif alpha <= 4:
            alpha = 0
        hardened.append((red, green, blue, alpha))
    im.putdata(hardened)
    im = pad_to_ratio(im, RATIOS[face])

    long_edge = LONG_EDGE[face]
    scale = long_edge / max(im.size)
    size = (max(1, round(im.width * scale)), max(1, round(im.height * scale)))
    im = im.resize(size, Image.Resampling.LANCZOS)
    target.parent.mkdir(parents=True, exist_ok=True)
    im.save(target, format="PNG", optimize=True)
    checkerboard(im).save(preview_path, format="PNG", optimize=True)

    alpha = im.getchannel("A")
    histogram = alpha.histogram()
    transparent = histogram[0]
    opaque = histogram[255]
    partial = im.width * im.height - transparent - opaque
    return {
        "face": face,
        "source": str(source.relative_to(ROOT)),
        "output": str(target.relative_to(ROOT)),
        "source_bbox": list(bbox),
        "size": list(im.size),
        "content_ratio_target": RATIOS[face],
        "content_ratio_output": im.width / im.height,
        "transparent_pixels": transparent,
        "opaque_pixels": opaque,
        "partial_alpha_pixels": partial,
        "checkerboard": str(preview_path.relative_to(ROOT)),
    }


def main() -> None:
    faces = sys.argv[1:] or list(RATIOS)
    results = [finalize(face) for face in faces]
    report = ROOT / "qa" / "views-finalize.json"
    report.write_text(json.dumps({"faces": results}, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"faces": results}, indent=2))


if __name__ == "__main__":
    main()

