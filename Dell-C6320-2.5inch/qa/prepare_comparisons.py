#!/usr/bin/env python3
"""Prepare same-camera reference frames and an authoritative oblique review board."""

import json
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
LOG = json.loads((ROOT / "qa/webgl-loads/load-events.json").read_text())
OUT = ROOT / "qa/comparisons"
REF_OUT = OUT / "reference-frames"
REF_OUT.mkdir(parents=True, exist_ok=True)

WIDTH, HEIGHT = 1280, 900
ASPECT = WIDTH / HEIGHT
FONT_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def checkerboard():
    canvas = Image.new("RGB", (WIDTH, HEIGHT), (238, 241, 245))
    draw = ImageDraw.Draw(canvas)
    for y in range(0, HEIGHT, 16):
        for x in range(0, WIDTH, 16):
            if (x // 16 + y // 16) % 2:
                draw.rectangle((x, y, x + 15, y + 15), fill=(223, 229, 235))
    return canvas


def projected_pixels(world_width, world_height):
    half_h = max(world_height / 2, (world_width / 2) / ASPECT) * 1.12
    px_per_unit = HEIGHT / (2 * half_h)
    return round(world_width * px_per_unit), round(world_height * px_per_unit)


face_dimensions = {
    "front": (482.3, 86.8), "rear": (482.3, 86.8),
    "left": (795.9, 86.8), "right": (795.9, 86.8),
    "top": (448.0, 795.9), "bottom": (448.0, 795.9),
}

for face, dimensions in face_dimensions.items():
    source = Image.open(ROOT / "views" / f"{face}.png").convert("RGB")
    size = projected_pixels(*dimensions)
    source = source.resize(size, Image.Resampling.LANCZOS)
    frame = checkerboard()
    frame.paste(source, ((WIDTH - size[0]) // 2, (HEIGHT - size[1]) // 2))
    frame.save(REF_OUT / f"{face}.png", optimize=True)


def fit(image, box):
    image = image.convert("RGB")
    scale = min(box[0] / image.width, box[1] / image.height)
    return image.resize((round(image.width * scale), round(image.height * scale)), Image.Resampling.LANCZOS)


records = {(item["viewer"], item["model"], item["view"]): item for item in LOG["records"]}
obliques = [
    ("front-left", ROOT / "source/third-party/ebay-maravi-c6300-1.webp", "Exact complete front three-quarter; primary front material/configuration evidence"),
    ("front-right", ROOT / "source/third-party/ebay-maravi-c6300-1.webp", "Exact complete front three-quarter; opposite-handed source unavailable, used only for counts/material"),
    ("rear-left", ROOT / "source/third-party/express-c6320-rear.jpg", "Exact populated C6300/C6320 rear-top supporting view"),
    ("rear-right", ROOT / "source/third-party/ebay-maravi-c6300-3.webp", "Exact stacked complete rear configuration supporting view"),
]

board = Image.new("RGB", (1800, 2480), (24, 28, 33))
draw = ImageDraw.Draw(board)
title_font = ImageFont.truetype(FONT_PATH, 28)
label_font = ImageFont.truetype(FONT_PATH, 20)
note_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 16)
draw.text((36, 22), "AUTHORITATIVE THREE-QUARTER SOURCE REVIEW · ACTUAL STANDARD GLB", font=title_font, fill=(245, 247, 249))
for row, (view, source_path, note) in enumerate(obliques):
    top = 76 + row * 595
    actual_path = ROOT / records[("three", "standard", view)]["screenshot"]
    actual = fit(Image.open(actual_path), (840, 510))
    source = fit(Image.open(source_path), (840, 510))
    ax, sx = 35 + (840 - actual.width) // 2, 925 + (840 - source.width) // 2
    board.paste(actual, (ax, top + 40 + (510 - actual.height) // 2))
    board.paste(source, (sx, top + 40 + (510 - source.height) // 2))
    draw.text((35, top), f"ACTUAL GLB · {view}", font=label_font, fill=(213, 238, 255))
    draw.text((925, top), f"REAL EXACT-SUBJECT SOURCE · {source_path.name}", font=label_font, fill=(225, 255, 219))
    draw.text((35, top + 558), note, font=note_font, fill=(220, 224, 229))
board.save(OUT / "authoritative-oblique-review.png", optimize=True)

print(json.dumps({
    "reference_frames": [str(REF_OUT / f"{face}.png") for face in face_dimensions],
    "oblique_review": str(OUT / "authoritative-oblique-review.png")
}, indent=2))
