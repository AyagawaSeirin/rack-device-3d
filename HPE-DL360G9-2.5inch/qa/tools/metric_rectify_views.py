#!/usr/bin/env python3
"""Metric reconstruction of imagegen faces without scaling identifying components.

The source-locked generated product is kept at native pixel scale.  Where imagegen
under-ran a published face ratio, only verified featureless sheet-metal spans are
extended; components, ports, bays, logos, holes, and handles are never resized.
"""

from __future__ import annotations

import json
from collections import deque
from pathlib import Path

from PIL import Image, ImageDraw


ROOT = Path(__file__).resolve().parents[2]
TARGET_RATIO = {
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
SOURCE = {
    "front": "front-base-alpha.png",
    "rear": "rear-alpha.png",
    "left": "left-alpha.png",
    "right": "right-alpha.png",
    "top": "top-alpha.png",
    "bottom": "bottom-alpha.png",
}


def visible_bbox(im: Image.Image, threshold: int = 8) -> tuple[int, int, int, int]:
    bbox = im.getchannel("A").point(lambda value: 255 if value > threshold else 0).getbbox()
    if bbox is None:
        raise ValueError("no visible product")
    return bbox


def blank_front_microtext(im: Image.Image) -> None:
    """Remove unverifiable AI microtext while retaining carrier relief."""
    boxes = [
        (134, 343, 198, 400),
        (134, 412, 198, 469),
        (450, 343, 516, 400),
        (450, 412, 516, 469),
        (765, 343, 831, 400),
        (765, 412, 831, 469),
        (1075, 412, 1140, 469),
        (1388, 412, 1454, 469),
    ]
    for x0, y0, x1, y1 in boxes:
        # Suppress only neutral bright glyph pixels. The carrier panel, chamfers,
        # grooves, handles, and surrounding source-locked texture remain intact.
        pixels = im.load()
        for y in range(y0, y1):
            for x in range(x0, x1):
                red, green, blue, alpha = pixels[x, y]
                spread = max(red, green, blue) - min(red, green, blue)
                luminance = (red * 299 + green * 587 + blue * 114) // 1000
                if alpha > 0 and luminance > 112 and spread < 32:
                    texture = 35 + ((x * 17 + y * 11) % 11)
                    pixels[x, y] = (texture, texture + 1, texture + 1, alpha)


def insert_pattern(
    im: Image.Image,
    target_width: int,
    insert_x: int,
    sample_x: int,
    sample_width: int = 12,
) -> Image.Image:
    """Extend only a verified flat sheet-metal span; never resize components."""
    if target_width <= im.width:
        return im
    extra = target_width - im.width
    insert_x = max(1, min(im.width - 1, insert_x))
    sample_x = max(0, min(im.width - sample_width, sample_x))
    pattern = im.crop((sample_x, 0, sample_x + sample_width, im.height))
    fill = Image.new("RGBA", (extra, im.height), (0, 0, 0, 0))
    cursor = 0
    flip = False
    while cursor < extra:
        tile = pattern.transpose(Image.Transpose.FLIP_LEFT_RIGHT) if flip else pattern
        take = min(tile.width, extra - cursor)
        fill.alpha_composite(tile.crop((0, 0, take, tile.height)), (cursor, 0))
        cursor += take
        flip = not flip
    out = Image.new("RGBA", (target_width, im.height), (0, 0, 0, 0))
    out.alpha_composite(im.crop((0, 0, insert_x, im.height)), (0, 0))
    out.alpha_composite(fill, (insert_x, 0))
    out.alpha_composite(im.crop((insert_x, 0, im.width, im.height)), (insert_x + extra, 0))
    return out


def extend_edges(im: Image.Image, target_width: int) -> Image.Image:
    """Widen only the plain folded side margins of top/bottom sheet metal."""
    if target_width <= im.width:
        return im
    extra = target_width - im.width
    left_extra = extra // 2
    right_extra = extra - left_extra
    out = Image.new("RGBA", (target_width, im.height), (0, 0, 0, 0))
    left_band = im.crop((0, 0, min(8, im.width), im.height)).resize(
        (max(1, left_extra), im.height), Image.Resampling.BILINEAR
    )
    right_band = im.crop((max(0, im.width - 8), 0, im.width, im.height)).resize(
        (max(1, right_extra), im.height), Image.Resampling.BILINEAR
    )
    if left_extra:
        out.alpha_composite(left_band, (0, 0))
    out.alpha_composite(im, (left_extra, 0))
    if right_extra:
        out.alpha_composite(right_band, (left_extra + im.width, 0))
    return out


def stretch_featureless_span(
    im: Image.Image, target_width: int, span_start: int, span_end: int
) -> Image.Image:
    """Widen a long source-proven plain metal span; components remain untouched."""
    if target_width <= im.width:
        return im
    span_start = max(1, min(im.width - 2, span_start))
    span_end = max(span_start + 1, min(im.width - 1, span_end))
    extra = target_width - im.width
    span = im.crop((span_start, 0, span_end, im.height)).resize(
        (span_end - span_start + extra, im.height), Image.Resampling.BICUBIC
    )
    out = Image.new("RGBA", (target_width, im.height), (0, 0, 0, 0))
    out.alpha_composite(im.crop((0, 0, span_start, im.height)), (0, 0))
    out.alpha_composite(span, (span_start, 0))
    out.alpha_composite(
        im.crop((span_end, 0, im.width, im.height)),
        (span_start + span.width, 0),
    )
    return out


def insert_interpolated_band(im: Image.Image, target_width: int, insert_x: int) -> Image.Image:
    """Insert a plain metal separator by interpolating its two verified edges."""
    if target_width <= im.width:
        return im
    insert_x = max(1, min(im.width - 1, insert_x))
    extra = target_width - im.width
    left_column = im.crop((insert_x - 1, 0, insert_x, im.height)).resize(
        (extra, im.height), Image.Resampling.NEAREST
    )
    right_column = im.crop((insert_x, 0, insert_x + 1, im.height)).resize(
        (extra, im.height), Image.Resampling.NEAREST
    )
    band = Image.blend(left_column, right_column, 0.5)
    out = Image.new("RGBA", (target_width, im.height), (0, 0, 0, 0))
    out.alpha_composite(im.crop((0, 0, insert_x, im.height)), (0, 0))
    out.alpha_composite(band, (insert_x, 0))
    out.alpha_composite(
        im.crop((insert_x, 0, im.width, im.height)), (insert_x + extra, 0)
    )
    return out


def seal_internal_alpha(im: Image.Image) -> Image.Image:
    """Keep only border-connected external transparency; chassis/ports stay opaque."""
    rgba = im.copy().convert("RGBA")
    alpha = rgba.getchannel("A")
    width, height = rgba.size
    pix = alpha.load()
    external = bytearray(width * height)
    queue: deque[tuple[int, int]] = deque()

    def enqueue(x: int, y: int) -> None:
        idx = y * width + x
        if external[idx] or pix[x, y] >= 250:
            return
        external[idx] = 1
        queue.append((x, y))

    for x in range(width):
        enqueue(x, 0)
        enqueue(x, height - 1)
    for y in range(height):
        enqueue(0, y)
        enqueue(width - 1, y)
    while queue:
        x, y = queue.popleft()
        for nx, ny in ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)):
            if 0 <= nx < width and 0 <= ny < height:
                enqueue(nx, ny)

    out_alpha = Image.new("L", (width, height), 255)
    out_pix = out_alpha.load()
    for y in range(height):
        for x in range(width):
            if external[y * width + x]:
                out_pix[x, y] = pix[x, y]
    rgba.putalpha(out_alpha)
    return rgba


def pad_canvas(im: Image.Image, ratio: float) -> Image.Image:
    current = im.width / im.height
    if current < ratio:
        width, height = round(im.height * ratio), im.height
    else:
        width, height = im.width, round(im.width / ratio)
    out = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    out.alpha_composite(im, ((width - im.width) // 2, (height - im.height) // 2))
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


def process(face: str) -> dict:
    source_path = ROOT / "qa" / "work" / SOURCE[face]
    im = Image.open(source_path).convert("RGBA")
    if face == "front":
        blank_front_microtext(im)
    source_bbox = visible_bbox(im)
    im = im.crop(source_bbox)
    before = list(im.size)
    ratio = TARGET_RATIO[face]
    current = im.width / im.height

    method = "native_source_locked_ratio"
    if face in {"rear", "left", "right"} and current < ratio:
        target_width = round(im.height * ratio)
        settings = {
            "left": (780, 730),
        }
        if face == "rear":
            im = insert_interpolated_band(im, target_width, 1344)
        elif face == "right":
            im = stretch_featureless_span(im, target_width, 350, 650)
        else:
            insert_x, sample_x = settings[face]
            im = insert_pattern(im, target_width, insert_x, sample_x)
        method = "featureless_sheet_metal_span_extension"
    elif face in {"top", "bottom"} and current < ratio:
        target_width = round(im.height * ratio)
        im = extend_edges(im, target_width)
        method = "plain_folded_edge_extension"

    im = seal_internal_alpha(im)
    content_bbox = visible_bbox(im)
    content_ratio = (content_bbox[2] - content_bbox[0]) / (content_bbox[3] - content_bbox[1])
    im = pad_canvas(im, ratio)
    scale = LONG_EDGE[face] / max(im.size)
    im = im.resize(
        (max(1, round(im.width * scale)), max(1, round(im.height * scale))),
        Image.Resampling.LANCZOS,
    )
    target_path = ROOT / "views" / f"{face}.png"
    preview_path = ROOT / "qa" / "reference" / f"{face}-checkerboard.png"
    im.save(target_path, "PNG", optimize=True)
    checkerboard(im).save(preview_path, "PNG", optimize=True)
    return {
        "face": face,
        "source": str(source_path.relative_to(ROOT)),
        "source_bbox": list(source_bbox),
        "native_cropped_px": before,
        "method": method,
        "metric_content_px_before_export": [content_bbox[2] - content_bbox[0], content_bbox[3] - content_bbox[1]],
        "metric_content_ratio": content_ratio,
        "target_ratio": ratio,
        "ratio_error_percent": abs(content_ratio / ratio - 1.0) * 100.0,
        "output": str(target_path.relative_to(ROOT)),
        "output_canvas_px": list(im.size),
        "checkerboard": str(preview_path.relative_to(ROOT)),
    }


def main() -> None:
    results = [process(face) for face in TARGET_RATIO]
    report = {"method": "source-locked component-preserving metric reconstruction", "faces": results}
    path = ROOT / "qa" / "metric-rectification.json"
    path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
