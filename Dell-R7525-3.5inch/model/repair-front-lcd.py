#!/usr/bin/env python3
"""Apply the accepted imagegen inactive-LCD patch without changing the face canvas.

The built-in edit correctly removed the unsupported IP string but changed the
overall canvas.  This script uses only its inactive-screen pixels and feathers
them into the exact original LCD interior.  Every pixel outside that verified
rectangle remains byte-for-byte unchanged.
"""

from pathlib import Path
from PIL import Image, ImageFilter


ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "views" / "front.png"
GENERATED = ROOT / "qa" / "rotation-review" / "imagegen" / "front-lcd-edit-rejected-canvas-drift.png"
OUTPUT = ROOT / "qa" / "rotation-review" / "imagegen" / "front-lcd-fixed.png"

# Source is the plain inactive LCD interior in the built-in imagegen edit.
SOURCE_BOX = (1447, 238, 1601, 265)
# Destination is only the unsupported text-bearing LCD interior in the locked
# 2400x432 face.  The physical bezel and LCD border are intentionally untouched.
TARGET_BOX = (1772, 33, 1958, 62)


def main() -> None:
    original = Image.open(TARGET).convert("RGBA")
    generated = Image.open(GENERATED).convert("RGB")
    before = original.copy()

    patch = generated.crop(SOURCE_BOX).resize(
        (TARGET_BOX[2] - TARGET_BOX[0], TARGET_BOX[3] - TARGET_BOX[1]),
        Image.Resampling.LANCZOS,
    ).convert("RGBA")
    mask = Image.new("L", patch.size, 255)
    mask = mask.filter(ImageFilter.GaussianBlur(radius=1.2))
    original.paste(patch, TARGET_BOX[:2], mask)

    # Preserve the original alpha exactly, including the already approved
    # external transparency and fully opaque product core.
    original.putalpha(before.getchannel("A"))
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    original.save(OUTPUT, optimize=True)

    changed = 0
    before_bytes = before.tobytes()
    after_bytes = original.tobytes()
    for i in range(0, len(before_bytes), 4):
        if before_bytes[i:i+4] != after_bytes[i:i+4]:
            changed += 1
    print(f"wrote {OUTPUT}; changed_pixels={changed}; target_box={TARGET_BOX}")


if __name__ == "__main__":
    main()
