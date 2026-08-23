#!/usr/bin/env python3
"""Place approved transparent face assets on the exact WebGL QA canvas."""

from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[2]
VIEWS = ROOT / "views"
OUT = ROOT / "qa" / "reference-canvas"
CANVAS = (1600, 1000)
BACKGROUND = (208, 208, 208, 255)

# Matched to the viewer fit policy: overall silhouette is 90% of horizontal
# canvas for wide faces and 84% of vertical canvas for top/bottom.  References
# remain body-only where canonical evidence deliberately excludes front ears.
TARGETS = {
    "front": (1440, round(1440 * 43 / 482.6)),
    "rear": (round(1440 * 436 / 482.6), round(1440 * 43 / 482.6)),
    "left": (round(1440 * 708 / 714), round(1440 * 43 / 714)),
    "right": (round(1440 * 708 / 714), round(1440 * 43 / 714)),
    "top": (round(840 * 436 / 714), round(840 * 708 / 714)),
    "bottom": (round(840 * 436 / 714), round(840 * 708 / 714)),
}


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    for face, size in TARGETS.items():
        source = Image.open(VIEWS / f"{face}.png").convert("RGBA")
        bbox = source.getchannel("A").point(lambda value: 255 if value > 8 else 0).getbbox()
        if not bbox:
            raise RuntimeError(f"empty source: {face}")
        crop = source.crop(bbox).resize(size, Image.Resampling.LANCZOS)
        canvas = Image.new("RGBA", CANVAS, BACKGROUND)
        xy = ((CANVAS[0] - size[0]) // 2, (CANVAS[1] - size[1]) // 2)
        canvas.alpha_composite(crop, xy)
        canvas.convert("RGB").save(OUT / f"{face}.png", optimize=True)
        print(face, size, xy)


if __name__ == "__main__":
    main()
