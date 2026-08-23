#!/usr/bin/env python3
"""Keep only border-connected external transparency in canonical view PNGs.

The image-generation chroma matte intentionally produces soft partial alpha.
Main equipment surfaces, dark vents and connector cavities must be opaque, so
the final assets use a binary external silhouette.  Enclosed keyed regions are
rendered as dark pixels; true through-openings are supplied by GLB geometry.
"""

from pathlib import Path

import numpy as np
from PIL import Image
from scipy import ndimage


for path in sorted((Path(__file__).parents[1] / "views").glob("*.png")):
    image = Image.open(path).convert("RGBA")
    rgba = np.asarray(image).copy()
    alpha = rgba[:, :, 3]
    candidate = alpha < 250
    seed = np.zeros_like(candidate)
    seed[0, :] = candidate[0, :]
    seed[-1, :] = candidate[-1, :]
    seed[:, 0] = candidate[:, 0]
    seed[:, -1] = candidate[:, -1]
    external = ndimage.binary_propagation(seed, mask=candidate)
    interior = ~external
    keyed_inside = interior & (alpha < 32)
    rgba[keyed_inside, :3] = np.array([12, 13, 14], dtype=np.uint8)
    rgba[external, 3] = 0
    rgba[interior, 3] = 255
    temporary = path.with_suffix(".normalized.png")
    Image.fromarray(rgba, mode="RGBA").save(temporary, compress_level=3)
    temporary.replace(path)
    print(path.name, "external_transparent", int(external.sum()), "opaque", int(interior.sum()))
