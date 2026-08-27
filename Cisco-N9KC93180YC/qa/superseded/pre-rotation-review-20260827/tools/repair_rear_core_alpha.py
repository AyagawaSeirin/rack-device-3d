#!/usr/bin/env python3
"""Make only the opaque rear chassis core fully opaque.

The standard view audit defines the core as an 8% inset of the tightly cropped
content bounds.  This exact rear asset fills its canvas, has no transparent
pixels in that core, and therefore needs only its accidental partial alpha
restored to 255.  RGB bytes and silhouette-edge alpha are invariants.
"""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
REAR = ROOT / "views" / "rear.png"
REPORT = ROOT / "qa" / "rear-alpha-repair.json"
EXPECTED_SIZE = (2200, 221)
EXPECTED_RGB_SHA256 = "ddd0723d2fad546fa81ee2ce11bdde30d5bb9480d4f7ee75b5c4b4269e56a059"


def digest(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


with Image.open(REAR) as source:
    image = source.convert("RGBA")

if image.size != EXPECTED_SIZE:
    raise SystemExit(f"unexpected rear size: {image.size}, expected {EXPECTED_SIZE}")

red, green, blue, alpha = image.split()
rgb_before = Image.merge("RGB", (red, green, blue))
rgb_sha_before = digest(rgb_before.tobytes())
if rgb_sha_before != EXPECTED_RGB_SHA256:
    raise SystemExit(
        f"unexpected rear RGB SHA-256: {rgb_sha_before}, expected {EXPECTED_RGB_SHA256}"
    )

width, height = image.size
core_box = (
    round(width * 0.08),
    round(height * 0.08),
    width - round(width * 0.08),
    height - round(height * 0.08),
)
alpha_pixels = bytearray(alpha.tobytes())
changed = []
for y in range(core_box[1], core_box[3]):
    row = y * width
    for x in range(core_box[0], core_box[2]):
        offset = row + x
        value = alpha_pixels[offset]
        if value != 255:
            changed.append((x, y, value))
            alpha_pixels[offset] = 255

repaired_alpha = Image.frombytes("L", image.size, bytes(alpha_pixels))
repaired = Image.merge("RGBA", (red, green, blue, repaired_alpha))
rgb_sha_after = digest(repaired.convert("RGB").tobytes())
if rgb_sha_after != rgb_sha_before:
    raise SystemExit("RGB changed during the alpha-only repair")

temporary = REAR.with_suffix(".alpha-repair.tmp.png")
repaired.save(temporary, format="PNG", optimize=True)
with Image.open(temporary) as check_source:
    check = check_source.convert("RGBA")
check_rgb_sha = digest(check.convert("RGB").tobytes())
if check_rgb_sha != rgb_sha_before:
    temporary.unlink(missing_ok=True)
    raise SystemExit("saved PNG does not preserve the original RGB bytes")

check_alpha = check.getchannel("A")
remaining_core_partial = sum(
    1
    for value in check_alpha.crop(core_box).tobytes()
    if value != 255
)
if remaining_core_partial:
    temporary.unlink(missing_ok=True)
    raise SystemExit(f"{remaining_core_partial} partially transparent core pixels remain")

os.replace(temporary, REAR)

report = {
    "status": "PASS",
    "operation": "alpha-only opaque-core repair",
    "path": str(REAR.relative_to(ROOT)),
    "size_px": list(image.size),
    "core_box_px": list(core_box),
    "changed_pixel_count": len(changed),
    "changed_alpha_below_250_count": sum(value < 250 for _, _, value in changed),
    "changed_alpha_250_to_254_count": sum(250 <= value <= 254 for _, _, value in changed),
    "changed_bbox_px": (
        [
            min(x for x, _, _ in changed),
            min(y for _, y, _ in changed),
            max(x for x, _, _ in changed) + 1,
            max(y for _, y, _ in changed) + 1,
        ]
        if changed
        else None
    ),
    "rgb_sha256_before": rgb_sha_before,
    "rgb_sha256_after": rgb_sha_after,
    "rgb_unchanged": rgb_sha_before == rgb_sha_after,
    "alpha_sha256_before": digest(alpha.tobytes()),
    "alpha_sha256_after": digest(repaired_alpha.tobytes()),
    "png_sha256_after": digest(REAR.read_bytes()),
    "remaining_non_opaque_core_pixels": remaining_core_partial,
    "silhouette_edge_alpha_policy": "unchanged outside the audit core",
}
REPORT.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
print(json.dumps(report, indent=2))
