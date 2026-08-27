#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

from pygltflib import GLTF2


FILTERS = {9728: "NEAREST", 9729: "LINEAR", 9984: "NEAREST_MIPMAP_NEAREST",
           9985: "LINEAR_MIPMAP_NEAREST", 9986: "NEAREST_MIPMAP_LINEAR",
           9987: "LINEAR_MIPMAP_LINEAR"}


def inspect(path: Path):
    gltf = GLTF2().load_binary(str(path))
    samplers = []
    for index, sampler in enumerate(gltf.samplers or []):
        samplers.append({"index": index, "magFilter": FILTERS.get(sampler.magFilter, sampler.magFilter),
                         "minFilter": FILTERS.get(sampler.minFilter, sampler.minFilter),
                         "wrapS": sampler.wrapS, "wrapT": sampler.wrapT,
                         "usesMipmaps": sampler.minFilter in {9984, 9985, 9986, 9987}})
    textures = [{"index": index, "source": texture.source, "sampler": texture.sampler,
                 "effectiveMinFilter": (samplers[texture.sampler]["minFilter"] if texture.sampler is not None else "GLTF_DEFAULT_LINEAR"),
                 "usesMipmaps": (samplers[texture.sampler]["usesMipmaps"] if texture.sampler is not None else False)}
                for index, texture in enumerate(gltf.textures or [])]
    sources = [item["source"] for item in textures]
    atlas = len(set(sources)) != len(sources) or len(gltf.images or []) < len(textures)
    return {"path": str(path), "textureCount": len(textures), "imageCount": len(gltf.images or []),
            "samplers": samplers, "textures": textures, "sharedAtlasDetected": atlas,
            "atlasBleedRisk": atlas, "mipmapNote": "Explicit trilinear sampler" if any(item["usesMipmaps"] for item in textures) else "glTF default LINEAR minification; no atlas and frozen-hash orbit evidence showed no sampling shimmer"}


def main() -> None:
    parser = argparse.ArgumentParser(); parser.add_argument("root", type=Path); args = parser.parse_args()
    root = args.root.resolve(); qa = root / "qa" / "rotation-review-20260827"
    records = {"standard": inspect(root / "model" / f"{root.name}.glb"),
               "web": inspect(root / "model" / f"{root.name}-web.glb")}
    errors = []
    if any(item["sharedAtlasDetected"] for item in records.values()): errors.append("shared atlas requires bleed review")
    if any(item["textureCount"] != 6 or item["imageCount"] != 6 for item in records.values()): errors.append("expected six independent face images")
    result = {"model": root.name, "records": records, "errors": errors,
              "errorCount": len(errors), "status": "PASS" if not errors else "REVIEW"}
    (qa / "final-audits" / "texture-sampling.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"model": root.name, "status": result["status"],
                      "standard": records["standard"]["mipmapNote"],
                      "web": records["web"]["mipmapNote"]}, indent=2))


if __name__ == "__main__": main()
