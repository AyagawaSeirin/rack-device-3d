#!/usr/bin/env python3
"""Prepare the six approved transparent canonical faces.

The generated images are orthographic source-locked assets on a chroma matte.  This
script uses the already-removed alpha versions, tight-crops the verified product,
applies Dell-dimension orthographic rectification, and writes the canonical views.
"""

from pathlib import Path
from PIL import Image, ImageFilter


ROOT = Path(__file__).resolve().parents[1]
STAGING = ROOT / "qa" / "imagegen-generated"
VIEWS = ROOT / "views"
VIEWS.mkdir(parents=True, exist_ok=True)


SPECS = {
    # face: (source, output size, explicit source crop or None)
    "front": ("front-alpha.png", (3203, 576), None),              # 482.6 : 86.8
    "rear": ("rear-alpha.png", (2973, 576), None),                # 448 : 86.8
    # Side textures cover Dell's published 763.2 mm body datum.  Verified front
    # rack/control projections and rear sled/PSU projections are separate GLB
    # geometry and establish the 797.3 mm installed bound.
    "left": ("left-alpha.png", (3376, 384), None),                 # 763.2 : 86.8
    "right": ("right-alpha.png", (3376, 384), None),               # 763.2 : 86.8
    # Top/bottom canonical textures cover the body; rack/control/handle protrusions
    # are separate GLB geometry.  Crops deliberately exclude those protrusions.
    "top": ("top-alpha.png", (1803, 3072), (84, 60, 878, 1511)),  # 448 : 763.2
    "bottom": ("bottom-alpha.png", (1803, 3072), (114, 82, 846, 1521)),
}


def blur_region(im: Image.Image, box: tuple[int, int, int, int], radius: float) -> None:
    """Turn unverified tiny AI glyphs into neutral photographic microprint."""
    region = im.crop(box).filter(ImageFilter.GaussianBlur(radius=radius))
    im.alpha_composite(region, dest=(box[0], box[1]))


for face, (name, size, explicit_crop) in SPECS.items():
    im = Image.open(STAGING / name).convert("RGBA")

    # The top source has accurate panel/label block geometry.  Tiny generated glyphs
    # that are not legible in the binding photograph are neutralized, while diagrams,
    # warning-color blocks, seams and all mechanical details remain in place.
    if face == "top":
        blur_region(im, (118, 408, 850, 790), 1.05)
        blur_region(im, (175, 88, 780, 300), 0.75)

    # The right-side part label is identity-neutral and unreadable in the real source;
    # retain its real block, not fabricated serial glyphs.
    if face == "right":
        blur_region(im, (1710, 370, 1855, 440), 0.8)

    crop = explicit_crop or im.getchannel("A").getbbox()
    if not crop:
        raise RuntimeError(f"No opaque content in {name}")
    im = im.crop(crop)

    # Orthographic rectification is anchored to Dell's published face dimensions.
    # It repairs generated camera/proportion drift and does not change feature counts.
    im = im.resize(size, Image.Resampling.LANCZOS)
    im.save(VIEWS / f"{face}.png", optimize=True)
    print(face, name, "crop", crop, "->", size)
