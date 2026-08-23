#!/usr/bin/env python3
"""Build exact-config Dell PowerEdge R7515 24-SFF standard and web GLBs.

Coordinates follow the project contract: +X device right when viewed from the
front, +Y up, +Z front.  Dimensions are authored in metres for glTF.
The model is newly constructed; no R7525 or official mesh is imported.
"""

from __future__ import annotations

import argparse
import gc
import json
import math
from pathlib import Path

import numpy as np
import trimesh
from PIL import Image
from shapely.geometry import Polygon
from trimesh.visual.material import PBRMaterial
from trimesh.visual.texture import TextureVisuals


ROOT = Path(__file__).resolve().parents[1]
VIEWS = ROOT / "views"
SOURCE = ROOT / "source"
MODEL = ROOT / "model"
TEXTURES = MODEL / "textures"

# Official installed dimensions, metres.
BODY_W = 0.434
OVERALL_W = 0.482
H = 0.0868
BODY_D = 0.64707
FRONT_PROJ = 0.03584
REAR_PROJ = 0.034685
OVERALL_D = FRONT_PROJ + BODY_D + REAR_PROJ
EAR_EXT = (OVERALL_W - BODY_W) / 2.0
Z_FRONT_REF = BODY_D / 2.0
Z_REAR_WALL = -BODY_D / 2.0
Z_FRONT_OUT = Z_FRONT_REF + FRONT_PROJ
Z_REAR_OUT = Z_REAR_WALL - REAR_PROJ
Y_TOP = H / 2.0
Y_BOTTOM = -H / 2.0


def alpha_crop(image: Image.Image) -> Image.Image:
    rgba = image.convert("RGBA")
    bbox = rgba.getchannel("A").point(lambda p: 255 if p > 8 else 0).getbbox()
    if not bbox:
        raise RuntimeError("transparent image has no product content")
    return rgba.crop(bbox)


def flatten_opaque(image: Image.Image) -> Image.Image:
    rgba = np.asarray(image.convert("RGBA"), dtype=np.uint8)
    alpha = rgba[..., 3]
    opaque = alpha >= 128
    fill = np.median(rgba[..., :3][opaque], axis=0).astype(np.uint8) if np.any(opaque) else np.array([90, 90, 90], dtype=np.uint8)
    a = rgba[..., 3:4].astype(np.float32) / 255.0
    rgb = (rgba[..., :3].astype(np.float32) * a + fill * (1.0 - a)).round().astype(np.uint8)
    return Image.fromarray(rgb, "RGB")


def fit_long_edge(image: Image.Image, edge: int) -> Image.Image:
    if max(image.size) == edge:
        return image
    scale = edge / max(image.size)
    size = (max(1, round(image.width * scale)), max(1, round(image.height * scale)))
    return image.resize(size, Image.Resampling.LANCZOS)


def crop_fraction(image: Image.Image, left: float, top: float, right: float, bottom: float) -> Image.Image:
    w, h = image.size
    return image.crop((round(w * left), round(h * top), round(w * right), round(h * bottom)))


def prepare_textures() -> dict[str, dict[str, Path]]:
    ear_fraction = EAR_EXT / OVERALL_W
    front_f = FRONT_PROJ / OVERALL_D
    rear_f = REAR_PROJ / OVERALL_D
    width_f = (1.0 - BODY_W / OVERALL_W) / 2.0

    def load_source(name: str) -> Image.Image:
        if name == "front-body":
            # Exact official 24-SFF elevation behind the installed security
            # bezel. Crop only the annotated canvas; external bezel geometry
            # and the DELL EMC emblem remain sourced from views/front.png.
            image = Image.open(SOURCE / "originals" / "official-front-24x2.5-manual.jpg").convert("RGBA")
            image = image.crop((25, 100, 829, 244))
            image = crop_fraction(image, ear_fraction, 0, 1 - ear_fraction, 1)
        elif name == "front-logo":
            image = alpha_crop(Image.open(VIEWS / "front.png"))
            image = crop_fraction(image, 0.402, 0.255, 0.624, 0.695)
        elif name in {"rear", "rear-psu-top", "rear-psu-bottom"}:
            image = alpha_crop(Image.open(VIEWS / "rear.png"))
            if name == "rear-psu-top":
                image = crop_fraction(image, 0.745, 0.000, 0.955, 0.500)
                image = image.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
            elif name == "rear-psu-bottom":
                image = crop_fraction(image, 0.745, 0.500, 0.955, 1.000)
                image = image.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
        elif name == "right-body":
            image = crop_fraction(alpha_crop(Image.open(VIEWS / "right.png")), front_f, 0, 1 - rear_f, 1)
        elif name == "left-body":
            image = crop_fraction(alpha_crop(Image.open(VIEWS / "left.png")), rear_f, 0, 1 - front_f, 1)
        elif name == "top-body":
            image = crop_fraction(alpha_crop(Image.open(VIEWS / "top.png")), width_f, rear_f, 1 - width_f, 1 - front_f)
            # trimesh/glTF top-face V convention is opposite the canonical PNG;
            # counter-flip only the embedded subtexture so front remains at the
            # bottom of both WebGL orthographic top renders.
            image = image.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
        elif name == "bottom":
            image = alpha_crop(Image.open(VIEWS / "bottom.png"))
        else:
            raise KeyError(name)
        return flatten_opaque(image)

    names = (
        "front-body", "front-logo", "rear", "rear-psu-top", "rear-psu-bottom",
        "left-body", "right-body", "top-body", "bottom",
    )
    output: dict[str, dict[str, Path]] = {"standard": {}, "web": {}}
    for directory in (TEXTURES / "standard", TEXTURES / "web"):
        directory.mkdir(parents=True, exist_ok=True)
    for name in names:
        source = load_source(name)
        if name == "front-body" and max(source.size) < 2048:
            standard = fit_long_edge(source, 2048)
        elif name in {"front-logo", "rear-psu-top", "rear-psu-bottom"} and max(source.size) < 1024:
            standard = fit_long_edge(source, 1024)
        else:
            standard = source
        standard_path = TEXTURES / "standard" / f"{name}.png"
        standard.save(standard_path, compress_level=6)
        output["standard"][name] = standard_path
        edge = 1024 if name in {"front-logo", "rear-psu-top", "rear-psu-bottom"} else (1536 if name in {"top-body", "bottom"} else 2048)
        web = fit_long_edge(source, edge)
        web_path = TEXTURES / "web" / f"{name}.png"
        web.save(web_path, compress_level=6)
        output["web"][name] = web_path
        del source, standard, web
        gc.collect()
    return output


def material_color(name: str, rgba: tuple[int, int, int, int], metallic: float = 0.0, roughness: float = 0.72) -> PBRMaterial:
    return PBRMaterial(
        name=name,
        baseColorFactor=rgba,
        metallicFactor=metallic,
        roughnessFactor=roughness,
        alphaMode="OPAQUE",
        doubleSided=False,
    )


def material_texture(name: str, path: Path) -> PBRMaterial:
    return PBRMaterial(
        name=name,
        baseColorFactor=(255, 255, 255, 255),
        baseColorTexture=Image.open(path).convert("RGB"),
        metallicFactor=0.0,
        roughnessFactor=0.68,
        alphaMode="OPAQUE",
        doubleSided=False,
    )


def assign_material(mesh: trimesh.Trimesh, material: PBRMaterial) -> trimesh.Trimesh:
    mesh.visual = TextureVisuals(material=material)
    mesh.metadata["material_name"] = material.name
    return mesh


def add_mesh(scene: trimesh.Scene, mesh: trimesh.Trimesh, name: str, material: PBRMaterial | None = None) -> None:
    mesh = mesh.copy()
    # Primitive and polygon extrusion constructors already return indexed,
    # outward-wound meshes.  Avoid trimesh's optional scipy-backed graph pass.
    mesh.remove_unreferenced_vertices()
    if material is not None:
        assign_material(mesh, material)
    scene.add_geometry(mesh, node_name=name, geom_name=name)


def add_box(scene: trimesh.Scene, name: str, extents: tuple[float, float, float], center: tuple[float, float, float], material: PBRMaterial, rotation_z: float = 0.0) -> None:
    transform = trimesh.transformations.translation_matrix(center)
    if rotation_z:
        transform = transform @ trimesh.transformations.rotation_matrix(rotation_z, [0, 0, 1])
    add_mesh(scene, trimesh.creation.box(extents=extents, transform=transform), name, material)


def add_cylinder_z(scene: trimesh.Scene, name: str, radius: float, height: float, center: tuple[float, float, float], material: PBRMaterial, sections: int = 32) -> None:
    mesh = trimesh.creation.cylinder(radius=radius, height=height, sections=sections)
    mesh.apply_translation(center)
    add_mesh(scene, mesh, name, material)


def add_cylinder_x(scene: trimesh.Scene, name: str, radius: float, height: float, center: tuple[float, float, float], material: PBRMaterial, sections: int = 24) -> None:
    mesh = trimesh.creation.cylinder(radius=radius, height=height, sections=sections)
    mesh.apply_transform(trimesh.transformations.rotation_matrix(math.pi / 2, [0, 1, 0]))
    mesh.apply_translation(center)
    add_mesh(scene, mesh, name, material)


def quad_mesh(name: str, vertices: list[tuple[float, float, float]], normal: tuple[float, float, float], material: PBRMaterial) -> trimesh.Trimesh:
    # UV origin follows the approved project convention: image top is v=0.
    uv = np.array([[0, 1], [1, 1], [1, 0], [0, 0]], dtype=np.float32)
    mesh = trimesh.Trimesh(
        vertices=np.asarray(vertices, dtype=np.float32),
        faces=np.array([[0, 1, 2], [0, 2, 3]], dtype=np.int64),
        vertex_normals=np.tile(np.asarray(normal, dtype=np.float32), (4, 1)),
        visual=TextureVisuals(uv=uv, material=material),
        process=False,
    )
    mesh.metadata["name"] = name
    return mesh


def add_textured_faces(scene: trimesh.Scene, textures: dict[str, Path]) -> dict[str, PBRMaterial]:
    mats = {key: material_texture(f"photo-{key}", path) for key, path in textures.items()}
    # Front body backing at nominal front plane; bezel geometry sits in front.
    add_mesh(scene, quad_mesh("front-photo", [
        (-BODY_W/2, Y_BOTTOM, Z_FRONT_REF + 0.00015),
        ( BODY_W/2, Y_BOTTOM, Z_FRONT_REF + 0.00015),
        ( BODY_W/2, Y_TOP,    Z_FRONT_REF + 0.00015),
        (-BODY_W/2, Y_TOP,    Z_FRONT_REF + 0.00015),
    ], (0, 0, 1), mats["front-body"]), "front-photo")

    add_mesh(scene, quad_mesh("rear-photo", [
        ( BODY_W/2, Y_BOTTOM, Z_REAR_WALL - 0.00015),
        (-BODY_W/2, Y_BOTTOM, Z_REAR_WALL - 0.00015),
        (-BODY_W/2, Y_TOP,    Z_REAR_WALL - 0.00015),
        ( BODY_W/2, Y_TOP,    Z_REAR_WALL - 0.00015),
    ], (0, 0, -1), mats["rear"]), "rear-photo")

    add_mesh(scene, quad_mesh("right-photo", [
        (BODY_W/2 + 0.00015, Y_BOTTOM, Z_FRONT_REF),
        (BODY_W/2 + 0.00015, Y_BOTTOM, Z_REAR_WALL),
        (BODY_W/2 + 0.00015, Y_TOP,    Z_REAR_WALL),
        (BODY_W/2 + 0.00015, Y_TOP,    Z_FRONT_REF),
    ], (1, 0, 0), mats["right-body"]), "right-photo")

    add_mesh(scene, quad_mesh("left-photo", [
        (-BODY_W/2 - 0.00015, Y_BOTTOM, Z_REAR_WALL),
        (-BODY_W/2 - 0.00015, Y_BOTTOM, Z_FRONT_REF),
        (-BODY_W/2 - 0.00015, Y_TOP,    Z_FRONT_REF),
        (-BODY_W/2 - 0.00015, Y_TOP,    Z_REAR_WALL),
    ], (-1, 0, 0), mats["left-body"]), "left-photo")

    add_mesh(scene, quad_mesh("top-photo", [
        (-BODY_W/2, Y_TOP + 0.00015, Z_FRONT_REF),
        ( BODY_W/2, Y_TOP + 0.00015, Z_FRONT_REF),
        ( BODY_W/2, Y_TOP + 0.00015, Z_REAR_WALL),
        (-BODY_W/2, Y_TOP + 0.00015, Z_REAR_WALL),
    ], (0, 1, 0), mats["top-body"]), "top-photo")

    add_mesh(scene, quad_mesh("bottom-photo", [
        ( BODY_W/2, Y_BOTTOM - 0.00015, Z_FRONT_REF),
        (-BODY_W/2, Y_BOTTOM - 0.00015, Z_FRONT_REF),
        (-BODY_W/2, Y_BOTTOM - 0.00015, Z_REAR_WALL),
        ( BODY_W/2, Y_BOTTOM - 0.00015, Z_REAR_WALL),
    ], (0, -1, 0), mats["bottom"]), "bottom-photo")

    # Source-derived raised Dell emblem patch, placed above the honeycomb ribs.
    logo_w, logo_h = 0.107, 0.032
    add_mesh(scene, quad_mesh("dell-emc-emblem", [
        (-logo_w/2, -logo_h/2, Z_FRONT_OUT + 0.0002),
        ( logo_w/2, -logo_h/2, Z_FRONT_OUT + 0.0002),
        ( logo_w/2,  logo_h/2, Z_FRONT_OUT + 0.0002),
        (-logo_w/2,  logo_h/2, Z_FRONT_OUT + 0.0002),
    ], (0, 0, 1), mats["front-logo"]), "dell-emc-emblem")
    return mats


def add_rack_ears(scene: trimesh.Scene, dark: PBRMaterial) -> None:
    # Exact front evidence proves the mounting-flange span but does not prove a
    # generic three-hole pattern. Keep the two front-only extensions separate
    # and solid; never invent unverified through-holes or rear ears.
    for side, x in (("left", -(BODY_W + EAR_EXT) / 2), ("right", (BODY_W + EAR_EXT) / 2)):
        add_box(scene, f"front-mounting-flange-{side}-solid", (EAR_EXT, H, 0.003), (x, 0, Z_FRONT_REF - 0.0015), dark)


def regular_hex(cx: float, cy: float, radius: float) -> list[tuple[float, float]]:
    return [(cx + radius * math.cos(math.radians(60 * i)), cy + radius * math.sin(math.radians(60 * i))) for i in range(6)]


def add_front_assemblies(scene: trimesh.Scene, graphite: PBRMaterial, black: PBRMaterial, silver: PBRMaterial, orange: PBRMaterial, green: PBRMaterial, blue: PBRMaterial) -> None:
    # The exact source-locked photo at the chassis plane preserves all 24 SFF
    # carriers and asymmetric controls without covering them with generic boxes.
    # The installed bezel is the silhouette/parallax assembly in front of it.
    depth = 0.008
    zbase = Z_FRONT_OUT - depth
    add_box(scene, "bezel-top-frame", (0.430, 0.005, depth), (0, Y_TOP - 0.0025, zbase + depth/2), graphite)
    add_box(scene, "bezel-bottom-frame", (0.430, 0.005, depth), (0, Y_BOTTOM + 0.0025, zbase + depth/2), graphite)
    add_box(scene, "bezel-left-lock-block", (0.033, 0.081, 0.015), (-0.205, 0, Z_FRONT_OUT - 0.0075), black)
    add_box(scene, "bezel-right-attachment-block", (0.033, 0.081, 0.015), (0.205, 0, Z_FRONT_OUT - 0.0075), black)
    add_cylinder_z(scene, "bezel-key-lock", 0.0085, 0.004, (-0.177, 0.020, Z_FRONT_OUT - 0.0018), graphite, 40)

    top_centers = [(-0.186 + 0.062 * i, 0.0165) for i in range(7)]
    bottom_centers = [(-0.155 + 0.062 * i, -0.0165) for i in range(6)]
    for index, (cx, cy) in enumerate(top_centers + bottom_centers):
        ring = Polygon(regular_hex(cx, cy, 0.031), [regular_hex(cx, cy, 0.0248)])
        mesh = trimesh.creation.extrude_polygon(ring, height=depth)
        mesh.apply_translation((0, 0, zbase))
        add_mesh(scene, mesh, f"bezel-hex-ring-{index:02d}", graphite)


def rear_x(u: float) -> float:
    return BODY_W / 2.0 - BODY_W * u


def add_rear_assemblies(scene: trimesh.Scene, silver: PBRMaterial, photo_mats: dict[str, PBRMaterial]) -> None:
    # The source-locked rear photo remains unobstructed for exact port, slot,
    # grille and stamped-panel appearance. Thin frames supply verified shallow
    # relief without replacing the photographic faces with generic rectangles.
    def add_frame(name: str, cx: float, cy: float, width: float, height: float) -> None:
        thickness = 0.0011
        depth = 0.0012
        z = Z_REAR_WALL - 0.0008
        add_box(scene, f"{name}-top", (width, thickness, depth), (cx, cy + height/2, z), silver)
        add_box(scene, f"{name}-bottom", (width, thickness, depth), (cx, cy - height/2, z), silver)
        add_box(scene, f"{name}-left", (thickness, height, depth), (cx - width/2, cy, z), silver)
        add_box(scene, f"{name}-right", (thickness, height, depth), (cx + width/2, cy, z), silver)

    add_frame("riser1B-slot-2-frame", rear_x(0.225), 0.023, 0.125, 0.018)
    add_frame("riser1B-slot-3-frame", rear_x(0.225), 0.003, 0.125, 0.018)
    add_frame("rear-exhaust-field-frame", rear_x(0.460), 0.004, 0.125, 0.067)
    add_frame("pcie-slot-4-frame", rear_x(0.625), 0.003, 0.016, 0.061)
    add_frame("pcie-slot-5-frame", rear_x(0.675), 0.003, 0.016, 0.061)

    # Two independent AC PSU volumes retain the official rear projection. Their
    # outer faces use exact source-locked photo crops, preserving IEC inputs,
    # orange latches, black handles, guarded fans and readable EPP 750W badges.
    psu_x = rear_x(0.850)
    psu_w, psu_h = 0.0911, 0.0420
    for index, y in enumerate((0.0210, -0.0210), start=1):
        add_box(scene, f"AC-PSU-{index}-volume", (psu_w, psu_h, REAR_PROJ), (psu_x, y, Z_REAR_WALL - REAR_PROJ/2), silver)
        mat = photo_mats["rear-psu-top" if index == 1 else "rear-psu-bottom"]
        z = Z_REAR_OUT - 0.00001
        add_mesh(scene, quad_mesh(f"AC-PSU-{index}-source-locked-face", [
            (psu_x + psu_w/2, y - psu_h/2, z),
            (psu_x - psu_w/2, y - psu_h/2, z),
            (psu_x - psu_w/2, y + psu_h/2, z),
            (psu_x + psu_w/2, y + psu_h/2, z),
        ], (0, 0, -1), mat), f"AC-PSU-{index}-source-locked-face")


def add_side_and_top_relief(scene: trimesh.Scene, silver: PBRMaterial, dark: PBRMaterial, black: PBRMaterial) -> None:
    # Independent left/right rail-stamping geometry; positions intentionally differ.
    add_box(scene, "right-side-upper-rail-stamping", (0.004, 0.018, 0.145), (BODY_W/2 - 0.001, 0.015, 0.145), silver)
    add_box(scene, "left-side-upper-rail-stamping", (0.004, 0.018, 0.155), (-BODY_W/2 + 0.001, 0.015, 0.135), silver)
    for index, (z, y) in enumerate(((0.205, -0.006), (0.065, -0.008), (-0.110, -0.004), (-0.250, -0.003))):
        add_cylinder_x(scene, f"right-side-black-plug-{index}", 0.004, 0.003, (BODY_W/2 + 0.0015, y, z), black)
    for index, (z, y) in enumerate(((0.235, -0.006), (0.095, -0.002), (-0.055, -0.007), (-0.205, -0.004))):
        add_cylinder_x(scene, f"left-side-black-plug-{index}", 0.004, 0.003, (-BODY_W/2 - 0.0015, y, z), black)

    # Separate front drive-backplane cover and top release latch.
    add_box(scene, "top-front-drive-backplane-cover", (0.424, 0.0028, 0.175), (0, Y_TOP - 0.0014, 0.232), silver)
    add_box(scene, "top-cover-release-latch", (0.020, 0.003, 0.045), (0.025, Y_TOP - 0.0015, 0.105), black)
    # Narrow verified top perforation rows near both edges; dark recessed slots.
    for side_x in (-0.202, 0.202):
        for i in range(27):
            add_box(scene, f"top-vent-{side_x:+.3f}-{i:02d}", (0.0035, 0.0015, 0.006), (side_x, Y_TOP - 0.00075, -0.235 + i*0.010), dark)


def build_scene(texture_paths: dict[str, Path]) -> trimesh.Scene:
    scene = trimesh.Scene(base_frame="R7515-origin")
    scene.units = "m"
    silver = material_color("galvanized-steel", (174, 178, 181, 255), metallic=0.12, roughness=0.68)
    graphite = material_color("bezel-graphite", (48, 48, 50, 255), metallic=0.0, roughness=0.82)
    black = material_color("mechanical-black", (19, 21, 23, 255), metallic=0.0, roughness=0.78)
    dark = material_color("recess-dark", (8, 10, 12, 255), metallic=0.0, roughness=0.88)
    orange = material_color("dell-release-orange", (211, 82, 18, 255), metallic=0.0, roughness=0.72)
    green = material_color("dell-epp-green", (48, 132, 102, 255), metallic=0.0, roughness=0.70)
    blue = material_color("connector-blue", (20, 93, 155, 255), metallic=0.0, roughness=0.65)
    teal = material_color("connector-teal", (31, 142, 145, 255), metallic=0.0, roughness=0.65)

    # Closed opaque chassis core; textures and relief sit over it.
    add_box(scene, "closed-chassis-core", (BODY_W, 0.0850, BODY_D), (0, -0.0009, 0), silver)
    photo_mats = add_textured_faces(scene, texture_paths)
    add_rack_ears(scene, graphite)
    add_front_assemblies(scene, graphite, black, silver, orange, green, blue)
    add_rear_assemblies(scene, silver, photo_mats)
    add_side_and_top_relief(scene, silver, dark, black)

    scene.metadata.update({
        "manufacturer": "Dell Technologies",
        "product": "PowerEdge R7515",
        "configuration": "24 x 2.5-inch SFF, security bezel installed, no rear drives, Riser 1B + slots 4/5, dual 750W AC PSU",
        "coordinate_convention": "+X right from front, +Y up, +Z front",
        "status": "PASS_WITH_BOTTOM_FALLBACK",
        "bottom_mode": "GENERIC_BOTTOM_FALLBACK",
    })
    return scene


def scene_bounds(scene: trimesh.Scene) -> dict:
    bounds = scene.bounds
    extents = bounds[1] - bounds[0]
    return {
        "min_m": [round(float(v), 8) for v in bounds[0]],
        "max_m": [round(float(v), 8) for v in bounds[1]],
        "extents_m": [round(float(v), 8) for v in extents],
        "extents_mm": [round(float(v * 1000.0), 4) for v in extents],
    }


def build(flavor: str, texture_paths: dict[str, Path]) -> dict:
    scene = build_scene(texture_paths)
    name = "Dell-R7515-2.5inch.glb" if flavor == "standard" else "Dell-R7515-2.5inch-web.glb"
    path = MODEL / name
    payload = trimesh.exchange.gltf.export_glb(scene, include_normals=True, unitize_normals=True)
    path.write_bytes(payload)
    triangles = sum(len(mesh.faces) for mesh in scene.geometry.values())
    vertices = sum(len(mesh.vertices) for mesh in scene.geometry.values())
    return {
        "flavor": flavor,
        "path": str(path.relative_to(ROOT)),
        "bytes": path.stat().st_size,
        "nodes": len(scene.graph.nodes_geometry),
        "meshes": len(scene.geometry),
        "triangles": triangles,
        "vertices": vertices,
        "bounds": scene_bounds(scene),
        "texture_paths": {key: str(value.relative_to(ROOT)) for key, value in texture_paths.items()},
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--flavor", choices=("standard", "web", "both"), default="both")
    args = parser.parse_args()
    MODEL.mkdir(parents=True, exist_ok=True)
    textures = prepare_textures()
    flavors = ("standard", "web") if args.flavor == "both" else (args.flavor,)
    builds = [build(flavor, textures[flavor]) for flavor in flavors]
    manifest = {
        "generator": "model/build_model.py",
        "newly_constructed": True,
        "official_mesh_imported": False,
        "dimensions_mm": {
            "body_width": BODY_W * 1000,
            "overall_width": OVERALL_W * 1000,
            "height": H * 1000,
            "body_depth": BODY_D * 1000,
            "front_projection": FRONT_PROJ * 1000,
            "rear_projection": REAR_PROJ * 1000,
            "overall_depth": OVERALL_D * 1000,
        },
        "visible_geometry": {
            "front_mounting_flange_extensions_without_unverified_holes": 2,
            "security_bezel_hex_rings": 13,
            "sff_carriers_source_textured_behind_bezel": 24,
            "sff_pull_handles_source_textured_behind_bezel": 24,
            "ac_psu_volumes": 2,
            "ac_psu_source_locked_end_faces": 2,
            "rear_source_textured_component_groups": "ports, Riser 1B slots, PCIe slots, exhaust, stamped seams",
            "rear_relieved_group_frames": 5,
            "top_vent_slots": 54,
            "independent_side_relief": True,
            "closed_chassis_core": True,
        },
        "builds": builds,
    }
    (MODEL / "build-manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(manifest, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
