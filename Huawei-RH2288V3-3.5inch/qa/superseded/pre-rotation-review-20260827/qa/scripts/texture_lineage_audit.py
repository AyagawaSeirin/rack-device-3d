#!/usr/bin/env python3
"""Prove that both GLBs embed the current six approved face assets."""

from __future__ import annotations

import hashlib
import io
import json
from pathlib import Path

from PIL import Image, ImageChops
from pygltflib import GLTF2


ROOT = Path(__file__).resolve().parents[2]
VIEWS = ROOT / "views"
FACES = ("front", "rear", "left", "right", "top", "bottom")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_path(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def expected_face(face: str, web: bool) -> Image.Image:
    image = Image.open(VIEWS / f"{face}.png").convert("RGBA")
    bounds = image.getchannel("A").getbbox()
    if bounds is None:
        raise RuntimeError(f"{face}: empty alpha")
    image = image.crop(bounds).convert("RGB")
    max_edge = 2048 if web else 4096
    if max(image.size) > max_edge:
        scale = max_edge / max(image.size)
        image = image.resize(
            (max(1, round(image.width * scale)), max(1, round(image.height * scale))),
            Image.Resampling.LANCZOS,
        )
    return image


def audit(path: Path, web: bool) -> dict:
    gltf = GLTF2().load_binary(path)
    blob = gltf.binary_blob()
    records = []
    for face in FACES:
        material = next(
            material
            for material in gltf.materials
            if (material.name or "").startswith(face.upper() + " approved evidence texture")
        )
        texture_index = material.pbrMetallicRoughness.baseColorTexture.index
        image_index = gltf.textures[texture_index].source
        image_def = gltf.images[image_index]
        buffer_view = gltf.bufferViews[image_def.bufferView]
        start = int(buffer_view.byteOffset or 0)
        end = start + int(buffer_view.byteLength)
        embedded_bytes = bytes(blob[start:end])
        embedded = Image.open(io.BytesIO(embedded_bytes)).convert("RGB")
        expected = expected_face(face, web)
        pixel_equal = embedded.size == expected.size and ImageChops.difference(
            embedded, expected
        ).getbbox() is None
        records.append(
            {
                "face": face,
                "approved_view": f"views/{face}.png",
                "approved_view_sha256": sha256_path(VIEWS / f"{face}.png"),
                "material": material.name,
                "embedded_image_index": image_index,
                "embedded_png_sha256": sha256_bytes(embedded_bytes),
                "embedded_size_px": list(embedded.size),
                "expected_size_px": list(expected.size),
                "decoded_pixels_equal_current_approved_view": pixel_equal,
            }
        )
    return {
        "path": str(path.relative_to(ROOT)),
        "web": web,
        "faces": records,
        "status": "PASS" if all(item["decoded_pixels_equal_current_approved_view"] for item in records) else "FAIL",
    }


def main() -> None:
    result = {
        "models": [
            audit(ROOT / "model" / "Huawei-RH2288V3-3.5inch.glb", False),
            audit(ROOT / "model" / "Huawei-RH2288V3-3.5inch-web.glb", True),
        ]
    }
    result["status"] = "PASS" if all(model["status"] == "PASS" for model in result["models"]) else "FAIL"
    output = ROOT / "qa" / "audits" / "texture-lineage.json"
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(result["status"], output)


if __name__ == "__main__":
    main()
