#!/usr/bin/env python3
"""Build dimension-ledger view canvases without anisotropically scaling source pixels."""

from pathlib import Path
from PIL import Image, ImageChops, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
INTERMEDIATE = ROOT / "qa" / "intermediate"
VIEWS = ROOT / "views"

SPECS = {
    "front": (INTERMEDIATE / "front-alpha.png", (3072, 553)),
    "rear": (INTERMEDIATE / "rear-alpha-corrected.png", (3072, 553)),
    "left": (INTERMEDIATE / "left-alpha-corrected.png", (3072, 335)),
    "right": (INTERMEDIATE / "right-alpha-corrected.png", (3072, 335)),
    "top": (INTERMEDIATE / "top-alpha.png", (1729, 3072)),
    "bottom": (INTERMEDIATE / "bottom-alpha-corrected.png", (1729, 3072)),
}


def alpha_bbox(image: Image.Image):
    return image.getchannel("A").point(lambda value: 255 if value > 8 else 0).getbbox()


def steel_canvas(size, seed):
    """Neutral closed-surface continuation used only outside the uniformly fitted source."""
    width, height = size
    # Pillow's C-backed noise/gradient operations keep 5K-pixel texture builds fast.
    grain = Image.effect_noise(size, 1.7).convert("L")
    grain = grain.point(lambda value: 196 + round((value - 128) * 0.035))
    vertical = Image.linear_gradient("L").resize(size).point(
        lambda value: round((128 - value) * 0.035)
    )
    base = ImageChops.add(grain, vertical, scale=1, offset=0)
    image = Image.merge(
        "RGBA",
        (base, base.point(lambda value: min(255, value + 2)), base.point(lambda value: min(255, value + 4)), Image.new("L", size, 255)),
    )
    draw = ImageDraw.Draw(image)
    line = (112, 117, 122, 255)
    draw.line((0, 1, width - 1, 1), fill=line, width=max(1, min(size) // 250))
    draw.line((0, height - 2, width - 1, height - 2), fill=line, width=max(1, min(size) // 250))
    draw.line((1, 0, 1, height - 1), fill=line, width=max(1, min(size) // 250))
    draw.line((width - 2, 0, width - 2, height - 1), fill=line, width=max(1, min(size) // 250))
    return image


def build(face, source_path, target_size):
    source = Image.open(source_path).convert("RGBA")
    bbox = alpha_bbox(source)
    if not bbox:
        raise RuntimeError(f"empty source: {source_path}")
    source = source.crop(bbox)
    target_width, target_height = target_size
    scale = min(target_width / source.width, target_height / source.height)
    fitted = source.resize(
        (max(1, round(source.width * scale)), max(1, round(source.height * scale))),
        Image.Resampling.LANCZOS,
    )
    canvas = steel_canvas(target_size, face)
    x = (target_width - fitted.width) // 2
    y = (target_height - fitted.height) // 2
    canvas.alpha_composite(fitted, (x, y))
    if face == "top":
        # Exact service-angle evidence shows three subdued factory label blocks
        # across the fixed front strip. Preserve only their verified color/size
        # impression; never invent a serial, QR code, or pseudo text.
        draw = ImageDraw.Draw(canvas)
        labels = [
            ((-90, 330), (70, 30), (45, 48, 51, 255)),
            ((0, 330), (70, 26), (232, 201, 36, 255)),
            ((90, 330), (50, 26), (224, 226, 224, 255)),
        ]
        for (cx_mm, cz_mm), (w_mm, d_mm), color in labels:
            cx = round((cx_mm + 224) / 448 * target_width)
            cy = round((cz_mm + 397.95) / 795.9 * target_height)
            rw = round(w_mm / 448 * target_width)
            rh = round(d_mm / 795.9 * target_height)
            draw.rounded_rectangle((cx-rw//2, cy-rh//2, cx+rw//2, cy+rh//2), radius=max(2, rh//10), fill=color)
    # These are opaque closed-surface projection textures. True silhouette alpha is
    # retained separately in qa/intermediate/*-alpha*.png for inspection.
    canvas.putalpha(255)
    VIEWS.mkdir(parents=True, exist_ok=True)
    output = VIEWS / f"{face}.png"
    canvas.save(output, optimize=True)
    return output, source.size, fitted.size, (x, y)


def main():
    for face, (source, target) in SPECS.items():
        output, cropped, fitted, offset = build(face, source, target)
        print(f"{face}: {source.name} crop={cropped} fit={fitted} offset={offset} -> {output.name} {target}")


if __name__ == "__main__":
    main()
