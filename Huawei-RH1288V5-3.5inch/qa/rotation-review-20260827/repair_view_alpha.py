#!/usr/bin/env python3
"""Restore opacity in the verified chassis core without changing RGB pixels."""

from pathlib import Path
import json

import numpy as np
from PIL import Image


ROOT = Path(__file__).resolve().parents[2]
RESULTS = []
for face in ("right", "top"):
    path = ROOT / "views" / f"{face}.png"
    image = Image.open(path).convert("RGBA")
    array = np.asarray(image).copy()
    alpha = array[:, :, 3]
    ys, xs = np.nonzero(alpha > 0)
    x0, x1 = int(xs.min()), int(xs.max()) + 1
    y0, y1 = int(ys.min()), int(ys.max()) + 1
    inset_x = max(1, round((x1 - x0) * 0.08))
    inset_y = max(1, round((y1 - y0) * 0.08))
    core = alpha[y0 + inset_y:y1 - inset_y, x0 + inset_x:x1 - inset_x]
    changed = int(np.count_nonzero(core < 255))
    core[core < 255] = 255
    Image.fromarray(array, "RGBA").save(path, optimize=True)
    RESULTS.append({"face": face, "path": str(path), "content_bbox": [x0, y0, x1, y1], "core_inset": [inset_x, inset_y], "alpha_pixels_restored": changed, "rgb_changed": 0})

(Path(__file__).resolve().parent / "alpha-repair-result.json").write_text(json.dumps(RESULTS, indent=2) + "\n")
print(json.dumps(RESULTS))
