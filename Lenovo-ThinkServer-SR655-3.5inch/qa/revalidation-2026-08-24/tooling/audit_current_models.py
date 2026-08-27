#!/usr/bin/env python3
import hashlib
import io
import json
import re
import struct
from pathlib import Path

from PIL import Image, ImageChops


ROOT = Path(__file__).resolve().parents[3]
MODEL_DIR = ROOT / "model"
OUTPUT = ROOT / "qa" / "revalidation-2026-08-24" / "current-models-audit.json"
MODELS = {
    "standard": MODEL_DIR / "Lenovo-ThinkServer-SR655-3.5inch.glb",
    "web": MODEL_DIR / "Lenovo-ThinkServer-SR655-3.5inch-web.glb",
}
FACE_FILLS = {
    "front": (16, 17, 18, 255),
    "rear": (184, 187, 186, 255),
    "left": (175, 178, 177, 255),
    "right": (175, 178, 177, 255),
    "top": (177, 180, 179, 255),
    "bottom": (166, 168, 167, 255),
}
FACE_MATERIALS = {
    "front": "FrontPhotographicSurface_opaque_texture",
    "rear": "RearPhotographicSurface_opaque_texture",
    "right": "RightPhotographicSurface_opaque_texture",
    "left": "LeftPhotographicSurface_opaque_texture",
    "top": "TopPhotographicSurface_opaque_texture",
    "bottom": "BottomPhotographicSurface_opaque_texture",
}
EXPECTED_EXTRAS = {
    "manufacturer": "Lenovo",
    "product": "ThinkSystem SR655",
    "variant": "B5VK AUR9 12x3.5 LFF, 8-slot PCIe-rich rear, 2x750W AC",
    "coordinate_convention": "+X device right, +Y up, +Z front",
    "build_type": "newly constructed exact exterior replica; official viewer mesh not copied",
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def load_glb(path: Path):
    data = path.read_bytes()
    magic, version, declared_length = struct.unpack_from("<4sII", data, 0)
    if magic != b"glTF" or version != 2 or declared_length != len(data):
        raise ValueError("invalid GLB header")
    offset = 12
    document = None
    binary = None
    while offset < len(data):
        chunk_length, chunk_type = struct.unpack_from("<I4s", data, offset)
        offset += 8
        chunk = data[offset:offset + chunk_length]
        offset += chunk_length
        if chunk_type == b"JSON":
            document = json.loads(chunk)
        elif chunk_type == b"BIN\x00":
            binary = chunk
    if document is None or binary is None:
        raise ValueError("GLB does not contain embedded JSON and BIN chunks")
    return document, binary


def buffer_view_bytes(document, binary, index):
    view = document["bufferViews"][index]
    offset = view.get("byteOffset", 0)
    return binary[offset:offset + view["byteLength"]]


def expected_face(face: str, web: bool) -> Image.Image:
    with Image.open(ROOT / "views" / f"{face}.png") as source_file:
        source = source_file.convert("RGBA")
    background = Image.new("RGBA", source.size, FACE_FILLS[face])
    expected = Image.alpha_composite(background, source).convert("RGB")
    if web:
        expected.thumbnail((2048, 2048), Image.Resampling.LANCZOS)
    return expected


def count_indices(names, pattern):
    regex = re.compile(pattern)
    return sorted({int(match.group(1)) for name in names if (match := regex.match(name))})


reports = {}
global_errors = []

for kind, path in MODELS.items():
    errors = []
    document, binary = load_glb(path)
    names = [node.get("name", "") for node in document.get("nodes", [])]
    scene = document["scenes"][document.get("scene", 0)]
    extras = scene.get("extras", {})
    if extras != EXPECTED_EXTRAS:
        errors.append("scene identity metadata does not match the exact AC target")

    feature_counts = {
        "lff_carriers": count_indices(names, r"LFFCarrier_(\d+)_"),
        "pcie_bank_a_slots": count_indices(names, r"RearPCIe_BankA_(\d+)_"),
        "pcie_bank_b_slots": count_indices(names, r"RearPCIe_BankB_(\d+)_"),
        "pcie_bank_c_slots": count_indices(names, r"RearPCIe_BankC_(\d+)_"),
        "psu_modules": count_indices(names, r"PSU(\d+)_Body$"),
        "psu_c14_inlets": count_indices(names, r"PSU(\d+)_C14Inlet$"),
        "psu_orange_handles": count_indices(names, r"PSU(\d+)_OrangeHandle$"),
        "ocp_ports": count_indices(names, r"OCPPort(\d+)$"),
        "left_raised_bosses": count_indices(names, r"LeftRaisedBoss(\d+)$"),
        "right_raised_bosses": count_indices(names, r"RightRaisedBoss(\d+)$"),
        "left_side_slots": count_indices(names, r"LeftSideSlot(\d+)$"),
    }
    expected_counts = {
        "lff_carriers": list(range(1, 13)),
        "pcie_bank_a_slots": [1, 2, 3],
        "pcie_bank_b_slots": [1, 2, 3],
        "pcie_bank_c_slots": [1, 2],
        "psu_modules": [1, 2],
        "psu_c14_inlets": [1, 2],
        "psu_orange_handles": [1, 2],
        "ocp_ports": [1, 2],
        "left_raised_bosses": [1, 2, 3, 4],
        "right_raised_bosses": [1, 2, 3, 4],
        "left_side_slots": [1, 2],
    }
    for key, expected in expected_counts.items():
        if feature_counts[key] != expected:
            errors.append(f"feature-node audit failed for {key}: {feature_counts[key]}")

    photo_nodes = sorted(name for name in names if name.endswith("PhotographicSurface"))
    expected_photo_nodes = sorted(name.replace("_opaque_texture", "") for name in FACE_MATERIALS.values())
    if photo_nodes != expected_photo_nodes:
        errors.append("six photographic surface nodes are missing or substituted")

    texture_results = {}
    materials = document.get("materials", [])
    textures = document.get("textures", [])
    images = document.get("images", [])
    for face, material_name in FACE_MATERIALS.items():
        matches = [material for material in materials if material.get("name") == material_name]
        if len(matches) != 1:
            errors.append(f"{face}: expected exactly one named photographic material")
            continue
        material = matches[0]
        if material.get("alphaMode", "OPAQUE") != "OPAQUE":
            errors.append(f"{face}: photographic material is not OPAQUE")
        if "KHR_materials_unlit" not in material.get("extensions", {}):
            errors.append(f"{face}: photographic material is not KHR_materials_unlit")
        texture_index = material["pbrMetallicRoughness"]["baseColorTexture"]["index"]
        image_index = textures[texture_index]["source"]
        image_def = images[image_index]
        if "uri" in image_def:
            errors.append(f"{face}: image is external instead of embedded")
            continue
        embedded_bytes = buffer_view_bytes(document, binary, image_def["bufferView"])
        with Image.open(io.BytesIO(embedded_bytes)) as embedded_file:
            embedded = embedded_file.convert("RGB")
        expected = expected_face(face, web=(kind == "web"))
        dimensions_match = embedded.size == expected.size
        pixel_equal = dimensions_match and ImageChops.difference(embedded, expected).getbbox() is None
        if not pixel_equal:
            errors.append(f"{face}: embedded texture pixels do not match the current approved view pipeline")
        texture_results[face] = {
            "embedded_dimensions": list(embedded.size),
            "expected_dimensions": list(expected.size),
            "pixel_equal_to_current_approved_view_pipeline": pixel_equal,
            "embedded_png_sha256": hashlib.sha256(embedded_bytes).hexdigest(),
        }

    negative_scales = []
    for index, node in enumerate(document.get("nodes", [])):
        scale = node.get("scale")
        if scale is not None and scale[0] * scale[1] * scale[2] < 0:
            negative_scales.append({"node": index, "name": node.get("name"), "scale": scale})
    if negative_scales:
        errors.append("negative/mirrored node transforms detected")

    external_resources = []
    for buffer in document.get("buffers", []):
        if buffer.get("uri"):
            external_resources.append(buffer["uri"])
    for image_def in images:
        if image_def.get("uri"):
            external_resources.append(image_def["uri"])
    if external_resources:
        errors.append("external resources detected")

    report = {
        "status": "PASS" if not errors else "FAIL",
        "path": str(path.relative_to(ROOT)),
        "bytes": path.stat().st_size,
        "sha256": sha256(path),
        "asset": document.get("asset"),
        "scene_identity_metadata": extras,
        "counts": {
            "scenes": len(document.get("scenes", [])),
            "nodes": len(document.get("nodes", [])),
            "meshes": len(document.get("meshes", [])),
            "materials": len(materials),
            "textures": len(textures),
            "images": len(images),
        },
        "feature_indices": feature_counts,
        "photographic_surface_nodes": photo_nodes,
        "texture_lineage": texture_results,
        "negative_or_mirrored_transforms": negative_scales,
        "external_resources": external_resources,
        "errors": errors,
    }
    reports[kind] = report
    global_errors.extend(f"{kind}: {error}" for error in errors)

standard_names = [node.get("name", "") for node in load_glb(MODELS["standard"])[0].get("nodes", [])]
web_names = [node.get("name", "") for node in load_glb(MODELS["web"])[0].get("nodes", [])]
same_exterior_structure = standard_names == web_names
if not same_exterior_structure:
    global_errors.append("standard/web node-name structure differs")

output = {
    "status": "PASS" if not global_errors else "FAIL",
    "models": reports,
    "standard_web_same_exterior_node_structure": same_exterior_structure,
    "errors": global_errors,
}
OUTPUT.write_text(json.dumps(output, indent=2) + "\n", encoding="utf-8")
print(json.dumps(output, indent=2))
raise SystemExit(1 if global_errors else 0)
