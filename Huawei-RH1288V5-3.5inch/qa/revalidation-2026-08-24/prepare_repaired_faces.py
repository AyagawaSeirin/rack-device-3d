#!/usr/bin/env python3
"""Prepare repaired top/bottom candidates without non-uniform scaling.

Both inputs are new built-in-imagegen outputs already converted from a border
chroma field to RGBA by the installed imagegen helper. Crops remove only the
generated adjacent-face/protrusion band (top) or trim featureless fallback metal
to the verified 436:748 body ratio (bottom). Resizing is uniform.
"""

from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parent
STAGING = ROOT / "staging"
CANDIDATES = ROOT / "candidates"
PHYSICAL_RATIO = 436.0 / 748.0
LONG_EDGE = 2400
MARGIN = 24


def prepare(name: str, crop_box: tuple[int, int, int, int]) -> None:
    image = Image.open(STAGING / f"{name}-alpha.png").convert("RGBA")
    crop = image.crop(crop_box)
    width, height = crop.size
    ratio_error = abs(width / height - PHYSICAL_RATIO) / PHYSICAL_RATIO
    if ratio_error > 0.002:
        raise RuntimeError(f"{name}: crop ratio error {ratio_error:.4%}")

    scale = LONG_EDGE / height
    output_width = round(width * scale)
    crop = crop.resize((output_width, LONG_EDGE), Image.Resampling.LANCZOS)
    canvas = Image.new("RGBA", (output_width + MARGIN * 2, LONG_EDGE + MARGIN * 2), (0, 0, 0, 0))
    canvas.alpha_composite(crop, (MARGIN, MARGIN))
    CANDIDATES.mkdir(parents=True, exist_ok=True)
    canvas.save(CANDIDATES / f"{name}.png", optimize=True)
    print(name, crop_box, (width, height), (output_width, LONG_EDGE), f"ratio_error={ratio_error:.4%}")


def main() -> None:
    # Top: y=50 is the first row where the complete 436 mm body is present;
    # protruding rear/rack hardware above it is excluded. The bottom crop ends
    # in featureless metal below the verified label area.
    prepare("top", (39, 50, 915, 1553))
    # Bottom: exact underside detail is unavailable. The generated candidate is
    # intentionally featureless, so a centered ratio crop removes no evidence.
    prepare("bottom", (89, 145, 870, 1485))


if __name__ == "__main__":
    main()
