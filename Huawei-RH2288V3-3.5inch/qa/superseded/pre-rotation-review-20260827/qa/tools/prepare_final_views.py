from __future__ import annotations

import json
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "qa" / "imagegen-raw" / "new" / "selected"
OUT = ROOT / "views"

RATIOS = {
    "front": 482.6 / 86.1,
    "rear": 447.0 / 86.1,
    "left": 748.0 / 86.1,
    "right": 748.0 / 86.1,
    "top": 447.0 / 748.0,
    "bottom": 447.0 / 748.0,
}

FINAL_SIZES = {
    "front": (4096, round(4096 / RATIOS["front"])),
    "rear": (4096, round(4096 / RATIOS["rear"])),
    "left": (4096, round(4096 / RATIOS["left"])),
    "right": (4096, round(4096 / RATIOS["right"])),
    "top": (round(3072 * RATIOS["top"]), 3072),
    "bottom": (round(3072 * RATIOS["bottom"]), 3072),
}

# All generated candidates were shorter/narrower than the published physical
# ratios. Correct only documented feature-free metal or module-divider strips;
# no carrier, logo, port, vent, latch, fastener, PSU, handle, label or silhouette
# feature is scaled independently.
INSERT_FRACTIONS = {
    "front": [0.075, 0.29, 0.50, 0.71, 0.925],
    "rear": [0.30, 0.48, 0.77],
    "left": [0.18, 0.36, 0.55, 0.71, 0.86],
    "right": [0.18, 0.35, 0.52, 0.69, 0.84],
    "top": [0.16, 0.35, 0.65, 0.84],
    "bottom": [0.20, 0.40, 0.60, 0.80],
}

SAMPLE_WIDTHS = {
    "front": 80,
    "rear": 100,
    "left": 150,
    "right": 160,
    "top": 90,
    "bottom": 180,
}


def alpha_crop(path: Path) -> tuple[Image.Image, tuple[int, int, int, int]]:
    image = Image.open(path).convert("RGBA")
    mask = image.getchannel("A").point(lambda value: 255 if value > 32 else 0)
    bbox = mask.getbbox()
    if bbox is None:
        raise RuntimeError(f"no visible product pixels: {path}")
    return image.crop(bbox), bbox


def insert_feature_free_columns(
    image: Image.Image, positions: list[int], total: int, sample_width: int
) -> Image.Image:
    if total < 0:
        raise RuntimeError("this repair only permits feature-free extension")
    if total == 0:
        return image
    widths = [total // len(positions)] * len(positions)
    for index in range(total % len(positions)):
        widths[index] += 1
    offset = 0
    for original_x, width in zip(positions, widths):
        x = max(1, min(image.width - 1, original_x + offset))
        half = sample_width // 2
        start = max(0, x - half)
        end = min(image.width, start + sample_width)
        start = max(0, end - sample_width)
        field = image.crop((start, 0, end, image.height)).resize(
            (end - start + width, image.height), Image.Resampling.LANCZOS
        )
        canvas = Image.new(
            "RGBA", (image.width + width, image.height), (0, 0, 0, 0)
        )
        left = image.crop((0, 0, start, image.height))
        right = image.crop((end, 0, image.width, image.height))
        canvas.paste(left, (0, 0), left)
        canvas.paste(field, (start, 0), field)
        canvas.paste(right, (end + width, 0), right)
        image = canvas
        offset += width
    return image


def prepare(face: str) -> dict:
    source = SRC / f"{face}-alpha.png"
    image, bbox = alpha_crop(source)
    before_size = image.size
    target_width = round(image.height * RATIOS[face])
    insert = target_width - image.width
    positions = [round(image.width * fraction) for fraction in INSERT_FRACTIONS[face]]
    image = insert_feature_free_columns(
        image, positions, insert, SAMPLE_WIDTHS[face]
    )
    pre_resize_ratio = image.width / image.height
    if abs(pre_resize_ratio / RATIOS[face] - 1.0) > 0.002:
        raise RuntimeError(
            f"{face}: corrected ratio {pre_resize_ratio:.6f} != {RATIOS[face]:.6f}"
        )
    final_size = FINAL_SIZES[face]
    image = image.resize(final_size, Image.Resampling.LANCZOS)
    OUT.mkdir(parents=True, exist_ok=True)
    destination = OUT / f"{face}.png"
    image.save(destination, optimize=True)
    return {
        "face": face,
        "source": str(source.relative_to(ROOT)),
        "source_bbox_alpha_gt_32": list(bbox),
        "tight_before_size": list(before_size),
        "feature_free_columns_inserted": insert,
        "insertion_positions_before_offsets": positions,
        "resampled_feature_free_field_width": SAMPLE_WIDTHS[face],
        "pre_resize_size": [target_width, before_size[1]],
        "physical_ratio": RATIOS[face],
        "pre_resize_ratio": pre_resize_ratio,
        "final_size": list(final_size),
        "output": str(destination.relative_to(ROOT)),
    }


records = [prepare(face) for face in ("front", "rear", "left", "right", "top", "bottom")]
(ROOT / "qa" / "view-preparation-final.json").write_text(
    json.dumps(records, indent=2) + "\n", encoding="utf-8"
)
print(json.dumps(records, indent=2))
