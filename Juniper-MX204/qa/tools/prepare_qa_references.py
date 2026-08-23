#!/usr/bin/env python3
"""Prepare 1600x900 orthographic and authoritative three-quarter QA references."""

from pathlib import Path
from PIL import Image


ROOT = Path(__file__).resolve().parents[2]
QA = ROOT / "qa"
SIZE = (1600, 900)


def checker(size=SIZE, dark=False):
    w, h = size
    tile = 36
    colors = ((52, 56, 60, 255), (37, 40, 43, 255)) if dark else ((245, 246, 247, 255), (217, 221, 224, 255))
    out = Image.new("RGBA", size)
    px = out.load()
    for y in range(h):
        for x in range(w):
            px[x, y] = colors[((x // tile) + (y // tile)) & 1]
    return out


def fit(image, max_w, max_h):
    im = image.convert("RGBA")
    scale = min(max_w / im.width, max_h / im.height)
    return im.resize((max(1, round(im.width * scale)), max(1, round(im.height * scale))), Image.Resampling.LANCZOS)


def place(image, path, max_w=1500, max_h=820, background=None):
    canvas = checker() if background is None else Image.new("RGBA", SIZE, background)
    im = fit(image, max_w, max_h)
    canvas.alpha_composite(im, ((SIZE[0]-im.width)//2, (SIZE[1]-im.height)//2))
    path.parent.mkdir(parents=True, exist_ok=True)
    canvas.convert("RGB").save(path, quality=96)


def main():
    ortho = QA / "reference" / "orthographic"
    for face in ("front", "rear", "left", "right", "top", "bottom"):
        image = Image.open(ROOT / "views" / f"{face}.png")
        place(image, ortho / f"{face}.png")

    quarter = {
        "front-left": ROOT / "source" / "originals" / "mx204-left-high.jpg",
        "front-right": ROOT / "source" / "originals" / "mx204-right-high.jpg",
        "rear-left": ROOT / "source" / "third-party" / "ebay-236254786705-rear-top.jpg",
        "rear-right": ROOT / "source" / "third-party" / "ebay-226170261047-rear-top.jpg",
    }
    for name, path in quarter.items():
        place(Image.open(path), QA / "reference" / "three-quarter" / f"{name}.png",
              max_w=1500, max_h=820, background=(246, 246, 246, 255))

    close = QA / "renders" / "closeups"
    close.mkdir(parents=True, exist_ok=True)
    front = Image.open(QA / "renders" / "three-standard" / "front.png")
    rear = Image.open(QA / "renders" / "three-standard" / "rear.png")
    crops = {
        "front-left-ear.png": front.crop((35, 300, 260, 610)),
        "front-logo-model.png": front.crop((120, 330, 1500, 570)),
        "rear-fans-psus.png": rear.crop((360, 300, 1510, 610)),
    }
    for name, image in crops.items():
        image.resize((image.width*2, image.height*2), Image.Resampling.LANCZOS).save(close / name)


if __name__ == "__main__":
    main()
