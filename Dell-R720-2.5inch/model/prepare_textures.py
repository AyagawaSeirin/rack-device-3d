#!/usr/bin/env python3
"""Create opaque, aspect-preserving standard/web textures from approved views."""

from __future__ import annotations

from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
VIEWS = ROOT / "views"
TEXTURES = ROOT / "model" / "textures"
BACKGROUNDS = {
    "front": (18, 20, 22),
    "rear": (150, 154, 154),
    "left": (174, 177, 176),
    "right": (174, 177, 176),
    "top": (174, 177, 176),
    "bottom": (174, 177, 176),
}


def opaque_face(face: str) -> Image.Image:
    source = Image.open(VIEWS / f"{face}.png").convert("RGBA")
    background = Image.new("RGBA", source.size, (*BACKGROUNDS[face], 255))
    return Image.alpha_composite(background, source).convert("RGB")


def web_size(image: Image.Image, long_edge: int = 1600) -> tuple[int, int]:
    scale = long_edge / max(image.size)
    return max(1, round(image.width * scale)), max(1, round(image.height * scale))


def main() -> None:
    for profile in ("standard", "web"):
        (TEXTURES / profile).mkdir(parents=True, exist_ok=True)
    for face in ("front", "rear", "left", "right", "top", "bottom"):
        standard = opaque_face(face)
        standard.save(TEXTURES / "standard" / f"{face}.png", format="PNG", optimize=True)
        web = standard.resize(web_size(standard), Image.Resampling.LANCZOS)
        web.save(TEXTURES / "web" / f"{face}.png", format="PNG", optimize=True)
        print(face, "standard", standard.size, "web", web.size)


if __name__ == "__main__":
    main()
