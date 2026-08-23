from pathlib import Path

import numpy as np
from PIL import Image


root = Path(__file__).resolve().parents[2]
path = root / "qa" / "imagegen-raw" / "selected" / "right-alpha.png"
im = Image.open(path).convert("RGBA")
arr = np.array(im)
alpha = arr[:, :, 3]

# The physical side shell is opaque. Chroma removal may open black vent/hole
# pixels; keep the external silhouette antialiasing but restore all pixels
# strictly between each row's first and last product pixel to alpha 255.
for y in range(alpha.shape[0]):
    xs = np.where(alpha[y] > 32)[0]
    if len(xs) < 2:
        continue
    lo, hi = int(xs.min()) + 2, int(xs.max()) - 1
    if hi > lo:
        alpha[y, lo:hi] = 255

arr[:, :, 3] = alpha
Image.fromarray(arr, "RGBA").save(path, optimize=True)
print(path)
