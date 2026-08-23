from __future__ import annotations

import json
from pathlib import Path

import numpy as np
from PIL import Image


ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / "qa" / "imagegen-raw" / "selected"
OUT = ROOT / "views"
LONG_EDGES = {
    "front": 4096,
    "rear": 4096,
    "left": 4096,
    "right": 4096,
    "top": 3072,
    "bottom": 3072,
}
PHYSICAL_RATIOS = {
    "front": 482.6 / 86.1,
    "rear": 447.0 / 86.1,
    "left": 748.0 / 86.1,
    "right": 748.0 / 86.1,
    "top": 447.0 / 748.0,
    "bottom": 447.0 / 748.0,
}


def prepare(face: str) -> dict:
    src = RAW / f"{face}-alpha.png"
    im = Image.open(src).convert("RGBA")
    alpha = np.asarray(im.getchannel("A"))
    ys, xs = np.where(alpha > 32)
    if len(xs) == 0:
        raise RuntimeError(f"no product pixels in {src}")
    bbox = (int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1)
    cropped = im.crop(bbox)
    w, h = cropped.size
    long_edge = LONG_EDGES[face]
    scale = long_edge / max(w, h)
    dst_size = (max(1, round(w * scale)), max(1, round(h * scale)))
    resized = cropped.resize(dst_size, Image.Resampling.LANCZOS)
    OUT.mkdir(parents=True, exist_ok=True)
    dst = OUT / f"{face}.png"
    resized.save(dst, optimize=True)
    ratio = dst_size[0] / dst_size[1]
    target = PHYSICAL_RATIOS[face]
    return {
        "face": face,
        "source": str(src.relative_to(ROOT)),
        "source_canvas": list(im.size),
        "alpha_bbox_threshold_32": list(bbox),
        "tight_source_size": [w, h],
        "final_size": list(dst_size),
        "tight_ratio": ratio,
        "physical_ratio": target,
        "ratio_error_percent": abs(ratio / target - 1) * 100,
        "output": str(dst.relative_to(ROOT)),
    }


records = [prepare(face) for face in LONG_EDGES]
(ROOT / "qa" / "view-preparation.json").write_text(
    json.dumps(records, indent=2) + "\n", encoding="utf-8"
)
print(json.dumps(records, indent=2))
