#!/usr/bin/env python3
"""Build the new QFX5110-48S-AFI exterior GLBs from locked project assets."""

from __future__ import annotations

import io
from pathlib import Path

import numpy as np
from PIL import Image
from pygltflib import GLTF2, Sampler
from shapely.geometry import Point, box as shapely_box
import trimesh
from trimesh.visual import TextureVisuals
from trimesh.visual.material import PBRMaterial


ROOT = Path(__file__).resolve().parents[1]
VIEWS = ROOT / "views"
MODEL = ROOT / "model"
QA = ROOT / "qa"

# Official body dimensions in metres.
BODY_W = 0.440944
BODY_H = 0.043688
BODY_D = 0.520192
RACK_W = 0.482600
EAR_EXT = (RACK_W - BODY_W) / 2.0

FRONT_Z = BODY_D / 2.0
REAR_Z = -BODY_D / 2.0


def pbr(name: str, rgba: tuple[float, float, float, float], metallic: float, roughness: float) -> PBRMaterial:
    return PBRMaterial(
        name=name,
        baseColorFactor=list(rgba),
        metallicFactor=metallic,
        roughnessFactor=roughness,
        alphaMode="OPAQUE",
        doubleSided=False,
    )


MAT_BODY = pbr("body_dark_gray", (0.31, 0.33, 0.35, 1.0), 0.05, 0.72)
MAT_EDGE = pbr("edge_gray", (0.39, 0.41, 0.42, 1.0), 0.08, 0.62)
MAT_BLACK = pbr("recess_black", (0.018, 0.021, 0.024, 1.0), 0.0, 0.83)
MAT_SILVER = pbr("galvanized_silver", (0.57, 0.59, 0.59, 1.0), 0.52, 0.48)
MAT_GOLD = pbr("connector_gold", (0.82, 0.48, 0.10, 1.0), 0.78, 0.30)
MAT_BLUE = pbr("juniper_azure_afi", (0.22, 0.72, 0.91, 1.0), 0.0, 0.54)
MAT_GREEN = pbr("status_green", (0.05, 0.46, 0.16, 1.0), 0.0, 0.42)


def set_material(mesh: trimesh.Trimesh, material: PBRMaterial) -> trimesh.Trimesh:
    mesh.visual = TextureVisuals(uv=np.zeros((len(mesh.vertices), 2), dtype=np.float32), material=material)
    return mesh


def make_box(extents, center, material=MAT_BODY) -> trimesh.Trimesh:
    mesh = trimesh.creation.box(extents=np.asarray(extents, dtype=float))
    mesh.apply_translation(np.asarray(center, dtype=float))
    return set_material(mesh, material)


def make_cylinder(radius, height, center, material, sections=24, axis="z") -> trimesh.Trimesh:
    mesh = trimesh.creation.cylinder(radius=radius, height=height, sections=sections)
    if axis == "x":
        mesh.apply_transform(trimesh.transformations.rotation_matrix(np.pi / 2.0, [0, 1, 0]))
    elif axis == "y":
        mesh.apply_transform(trimesh.transformations.rotation_matrix(np.pi / 2.0, [1, 0, 0]))
    mesh.apply_translation(np.asarray(center, dtype=float))
    return set_material(mesh, material)


def flatten_rgba(image: Image.Image, color=(80, 84, 88, 255)) -> Image.Image:
    image = image.convert("RGBA")
    background = Image.new("RGBA", image.size, color)
    background.alpha_composite(image)
    return background.convert("RGB")


def prepare_textures(profile: str) -> dict[str, Image.Image]:
    out_dir = QA / "work" / "model-textures" / profile
    out_dir.mkdir(parents=True, exist_ok=True)

    images = {face: Image.open(VIEWS / f"{face}.png").convert("RGBA") for face in ["front", "rear", "left", "right", "top", "bottom"]}

    # front.png includes separate front ears. The body material uses the exact centred body-width crop;
    # the ears themselves are real perforated geometry with a galvanized material.
    front = images["front"]
    body_px = round(front.width * BODY_W / RACK_W)
    body_x = (front.width - body_px) // 2
    images["front"] = front.crop((body_x, 0, body_x + body_px, front.height))

    result: dict[str, Image.Image] = {}
    max_edges = {
        "standard": {"front": 3742, "rear": 4096, "left": 4096, "right": 4096, "top": 3072, "bottom": 3072},
        "web": {"front": 2048, "rear": 2048, "left": 2048, "right": 2048, "top": 1536, "bottom": 1536},
    }[profile]
    for face, image in images.items():
        image = flatten_rgba(image)
        limit = max_edges[face]
        scale = min(1.0, limit / max(image.size))
        if scale < 1.0:
            image = image.resize((max(1, round(image.width * scale)), max(1, round(image.height * scale))), Image.Resampling.LANCZOS)
        image.save(out_dir / f"{face}.png", optimize=True)
        result[face] = image
    return result


def texture_material(name: str, image: Image.Image) -> PBRMaterial:
    return PBRMaterial(
        name=f"tex_{name}",
        baseColorFactor=[1.0, 1.0, 1.0, 1.0],
        baseColorTexture=image,
        metallicFactor=0.0,
        roughnessFactor=0.88,
        alphaMode="OPAQUE",
        doubleSided=False,
    )


def textured_quad(face: str, image: Image.Image) -> trimesh.Trimesh:
    eps = 0.00008
    if face == "front":
        verts = [[-BODY_W/2, -BODY_H/2, FRONT_Z+eps], [BODY_W/2, -BODY_H/2, FRONT_Z+eps],
                 [BODY_W/2, BODY_H/2, FRONT_Z+eps], [-BODY_W/2, BODY_H/2, FRONT_Z+eps]]
        uvs = [[0, 0], [1, 0], [1, 1], [0, 1]]
    elif face == "rear":
        verts = [[BODY_W/2, -BODY_H/2, REAR_Z-eps], [-BODY_W/2, -BODY_H/2, REAR_Z-eps],
                 [-BODY_W/2, BODY_H/2, REAR_Z-eps], [BODY_W/2, BODY_H/2, REAR_Z-eps]]
        uvs = [[0, 0], [1, 0], [1, 1], [0, 1]]
    elif face == "left":
        verts = [[-BODY_W/2-eps, -BODY_H/2, FRONT_Z], [-BODY_W/2-eps, BODY_H/2, FRONT_Z],
                 [-BODY_W/2-eps, BODY_H/2, REAR_Z], [-BODY_W/2-eps, -BODY_H/2, REAR_Z]]
        uvs = [[0, 0], [0, 1], [1, 1], [1, 0]]
    elif face == "right":
        verts = [[BODY_W/2+eps, -BODY_H/2, REAR_Z], [BODY_W/2+eps, BODY_H/2, REAR_Z],
                 [BODY_W/2+eps, BODY_H/2, FRONT_Z], [BODY_W/2+eps, -BODY_H/2, FRONT_Z]]
        uvs = [[1, 0], [1, 1], [0, 1], [0, 0]]
    elif face == "top":
        verts = [[-BODY_W/2, BODY_H/2+eps, FRONT_Z], [BODY_W/2, BODY_H/2+eps, FRONT_Z],
                 [BODY_W/2, BODY_H/2+eps, REAR_Z], [-BODY_W/2, BODY_H/2+eps, REAR_Z]]
        uvs = [[0, 0], [1, 0], [1, 1], [0, 1]]
    elif face == "bottom":
        verts = [[-BODY_W/2, -BODY_H/2-eps, FRONT_Z], [-BODY_W/2, -BODY_H/2-eps, REAR_Z],
                 [BODY_W/2, -BODY_H/2-eps, REAR_Z], [BODY_W/2, -BODY_H/2-eps, FRONT_Z]]
        uvs = [[0, 0], [0, 1], [1, 1], [1, 0]]
    else:
        raise ValueError(face)
    mesh = trimesh.Trimesh(vertices=np.asarray(verts), faces=np.asarray([[0, 1, 2], [0, 2, 3]]), process=False)
    mesh.visual = TextureVisuals(uv=np.asarray(uvs, dtype=np.float32), material=texture_material(face, image))
    return mesh


def rear_overlay_quad(x_center: float, width: float, z: float, material: PBRMaterial) -> trimesh.Trimesh:
    """Project the locked rear photograph onto a separately projecting rear module."""
    half = width / 2.0
    u0 = (BODY_W / 2.0 - (x_center + half)) / BODY_W
    u1 = (BODY_W / 2.0 - (x_center - half)) / BODY_W
    h = 0.0408
    verts = [
        [x_center + half, -h/2, z], [x_center - half, -h/2, z],
        [x_center - half, h/2, z], [x_center + half, h/2, z],
    ]
    uvs = [[u0, 0.02], [u1, 0.02], [u1, 0.98], [u0, 0.98]]
    mesh = trimesh.Trimesh(vertices=np.asarray(verts), faces=np.asarray([[0, 1, 2], [0, 2, 3]]), process=False)
    mesh.visual = TextureVisuals(uv=np.asarray(uvs, dtype=np.float32), material=material)
    return mesh


def front_overlay_group(
    rects: list[tuple[float, float, float, float]],
    z: float,
    material: PBRMaterial,
) -> trimesh.Trimesh:
    """Project exact locked front-photo crops onto shallow port relief faces."""
    vertices: list[list[float]] = []
    faces: list[list[int]] = []
    uvs: list[list[float]] = []
    for x_center, y_center, width, height in rects:
        x0 = x_center - width / 2.0
        x1 = x_center + width / 2.0
        y0 = y_center - height / 2.0
        y1 = y_center + height / 2.0
        u0 = (x0 + BODY_W / 2.0) / BODY_W
        u1 = (x1 + BODY_W / 2.0) / BODY_W
        v0 = (y0 + BODY_H / 2.0) / BODY_H
        v1 = (y1 + BODY_H / 2.0) / BODY_H
        base = len(vertices)
        vertices.extend([[x0, y0, z], [x1, y0, z], [x1, y1, z], [x0, y1, z]])
        faces.extend([[base, base + 1, base + 2], [base, base + 2, base + 3]])
        uvs.extend([[u0, v0], [u1, v0], [u1, v1], [u0, v1]])
    mesh = trimesh.Trimesh(
        vertices=np.asarray(vertices),
        faces=np.asarray(faces),
        process=False,
    )
    mesh.visual = TextureVisuals(uv=np.asarray(uvs, dtype=np.float32), material=material)
    return mesh


def add(scene: trimesh.Scene, name: str, mesh: trimesh.Trimesh) -> None:
    scene.add_geometry(mesh, node_name=name, geom_name=name)


def add_group(scene: trimesh.Scene, name: str, meshes: list[trimesh.Trimesh], material: PBRMaterial) -> None:
    if not meshes:
        return
    combined = trimesh.util.concatenate(meshes)
    set_material(combined, material)
    add(scene, name, combined)


def rack_ear(sign: int) -> trimesh.Trimesh:
    plate = shapely_box(-EAR_EXT/2, -BODY_H/2, EAR_EXT/2, BODY_H/2)
    for y in (-0.0134, 0.0134):
        plate = plate.difference(Point(0, y).buffer(0.0062, resolution=32))
    plate = plate.difference(Point(0, 0).buffer(0.00235, resolution=24))
    mesh = trimesh.creation.extrude_polygon(plate, height=0.0030, mid_plane=True)
    mesh.apply_translation([sign * (BODY_W/2 + EAR_EXT/2), 0, FRONT_Z + 0.0015])
    return set_material(mesh, MAT_SILVER)


def build_scene(textures: dict[str, Image.Image]) -> trimesh.Scene:
    scene = trimesh.Scene(base_frame="QFX5110-48S-AFI")
    scene.metadata.update({
        "manufacturer": "Juniper Networks",
        "product_id": "QFX5110-48S-AFI",
        "power": "dual 650W AC",
        "airflow": "AFI FRU-to-port",
        "coordinate_convention": "+X device-right from front; +Y up; +Z front",
        "construction": "new exterior model; no official mesh used",
    })

    add(scene, "Closed_Chassis_Body", make_box([BODY_W, BODY_H, BODY_D], [0, 0, 0], MAT_BODY))
    for face in ["front", "rear", "left", "right", "top", "bottom"]:
        add(scene, f"Face_{face.title()}_SourceLocked", textured_quad(face, textures[face]))

    # One shared copy of the locked rear photograph is also projected onto the outer planes of
    # independently projecting management, fan and PSU geometry. This retains real labels/materials
    # while the separate blocks and handles create the required parallax and depth.
    front_module_material = texture_material("front_modules", textures["front"])
    rear_module_material = texture_material("rear_modules", textures["rear"])

    add(scene, "Front_Rack_Ear_Left", rack_ear(-1))
    add(scene, "Front_Rack_Ear_Right", rack_ear(1))

    # Front port depth and connector relief. The exact source-photo crops are placed on the
    # shallow outer relief faces so generic black boxes cannot obscure the real cage pixels.
    front_black: list[trimesh.Trimesh] = []
    front_rects: list[tuple[float, float, float, float]] = []
    x_positions = np.linspace(-0.168, 0.161, 24)
    for y in (0.0072, -0.0072):
        for x in x_positions:
            front_black.append(make_box([0.0122, 0.0082, 0.0008], [x, y, FRONT_Z + 0.0004], MAT_BLACK))
            front_rects.append((x, y, 0.0122, 0.0082))
    add_group(scene, "Front_SFP_Cage_Relief_48", front_black, MAT_BLACK)
    add(
        scene,
        "Front_SFP_SourceLocked_Overlay_48",
        # Keep a deterministic 0.20 mm clearance beyond the relief-box outer
        # surface (FRONT_Z + 0.00080).  The previous 0.06 mm separation was
        # needlessly close to the WebGL depth precision used by orbit viewers.
        front_overlay_group(front_rects, FRONT_Z + 0.00100, front_module_material),
    )

    qsfp_black: list[trimesh.Trimesh] = []
    qsfp_rects: list[tuple[float, float, float, float]] = []
    for x in (0.1835, 0.2050):
        for y in (0.0072, -0.0072):
            qsfp_black.append(make_box([0.0186, 0.0086, 0.0008], [x, y, FRONT_Z + 0.0004], MAT_BLACK))
            qsfp_rects.append((x, y, 0.0186, 0.0086))
    add_group(scene, "Front_QSFP28_Cage_Relief_4", qsfp_black, MAT_BLACK)
    add(
        scene,
        "Front_QSFP28_SourceLocked_Overlay_4",
        front_overlay_group(qsfp_rects, FRONT_Z + 0.00100, front_module_material),
    )

    add(scene, "Front_GM_RJ45_Relief", make_box([0.0155, 0.0145, 0.0008], [-0.201, 0.0075, FRONT_Z + 0.0004], MAT_BLACK))
    add(
        scene,
        "Front_GM_RJ45_SourceLocked_Overlay",
        front_overlay_group([(-0.201, 0.0075, 0.0155, 0.0145)], FRONT_Z + 0.00100, front_module_material),
    )
    add(scene, "Front_PPS_OUT", make_cylinder(0.0036, 0.0048, [-0.201, -0.0097, FRONT_Z + 0.0024], MAT_GOLD))
    add(scene, "Front_10M_OUT", make_cylinder(0.0036, 0.0048, [-0.1835, -0.0097, FRONT_Z + 0.0024], MAT_GOLD))
    add(scene, "Front_ESD_Terminal", make_cylinder(0.0031, 0.0022, [-0.216, -0.0160, FRONT_Z + 0.0011], MAT_BLACK))

    # Rear management block and port relief. Management is screen-left in the rear reference, physical +X.
    add(scene, "Rear_Management_Panel", make_box([0.060, 0.0412, 0.00309], [0.188, 0, REAR_Z - 0.001545], MAT_EDGE))
    add(scene, "Rear_Management_SourceLocked_Overlay", rear_overlay_quad(0.188, 0.060, REAR_Z - 0.00325, rear_module_material))

    fan_x = [0.126, 0.079, 0.032, -0.015, -0.062]
    for index, x in enumerate(fan_x):
        add(scene, f"Rear_Fan_Module_{index}", make_box([0.0448, 0.0408, 0.02064], [x, 0, REAR_Z - 0.01032], MAT_BLACK))
        add(scene, f"Rear_Fan_SourceLocked_Overlay_{index}", rear_overlay_quad(x, 0.0448, REAR_Z - 0.02080, rear_module_material))

    psu_x = [-0.126, -0.190]
    for index, x in enumerate(psu_x):
        add(scene, f"Rear_AC_PSU_{index}", make_box([0.0600, 0.0408, 0.02684], [x, 0, REAR_Z - 0.01342], MAT_BLACK))
        add(scene, f"Rear_PSU_SourceLocked_Overlay_{index}", rear_overlay_quad(x, 0.0600, REAR_Z - 0.02700, rear_module_material))

    # Side mounting/rail slots as shallow real relief; each side keeps its distinct locked pattern.
    left_slots = []
    for y, zs in [(0.0105, np.linspace(0.205, -0.170, 7)), (-0.0105, np.linspace(0.175, -0.150, 6))]:
        for z in zs:
            left_slots.append(make_box([0.0007, 0.0065, 0.0020], [-BODY_W/2-0.00035, y, z], MAT_BLACK))
    add_group(scene, "Left_Side_Mount_Slots", left_slots, MAT_BLACK)
    right_slots = []
    for y, zs in [(0.0105, np.linspace(0.205, -0.175, 7)), (-0.0105, np.linspace(0.205, -0.175, 7))]:
        for z in zs:
            right_slots.append(make_box([0.0007, 0.0065, 0.0020], [BODY_W/2+0.00035, y, z], MAT_BLACK))
    add_group(scene, "Right_Side_Mount_Slots", right_slots, MAT_BLACK)

    # Slight top cover relief and perimeter fasteners.
    add(scene, "Top_Front_Cover_Seam", make_box([BODY_W-0.004, 0.0004, 0.0030], [0, BODY_H/2-0.0002, FRONT_Z-0.009], MAT_EDGE))
    add(scene, "Top_Rear_Cover_Seam", make_box([BODY_W-0.004, 0.0004, 0.0030], [0, BODY_H/2-0.0002, REAR_Z+0.009], MAT_EDGE))
    screws = []
    for z in (FRONT_Z-0.012, REAR_Z+0.012):
        for x in np.linspace(-0.185, 0.185, 5):
            screws.append(make_cylinder(0.00125, 0.0002, [x, BODY_H/2-0.0001, z], MAT_SILVER, sections=16, axis="y"))
    add_group(scene, "Top_Cover_Fasteners", screws, MAT_SILVER)

    return scene


def patch_unlit_and_metadata(path: Path, profile: str) -> None:
    gltf = GLTF2().load(str(path))
    if "KHR_materials_unlit" not in (gltf.extensionsUsed or []):
        gltf.extensionsUsed = list(gltf.extensionsUsed or []) + ["KHR_materials_unlit"]
    for material in gltf.materials or []:
        if material.name and material.name.startswith("tex_"):
            material.extensions = dict(material.extensions or {})
            material.extensions["KHR_materials_unlit"] = {}
            material.alphaMode = "OPAQUE"
            material.doubleSided = False
            if material.pbrMetallicRoughness:
                material.pbrMetallicRoughness.metallicFactor = 0.0
                material.pbrMetallicRoughness.roughnessFactor = 0.88
                material.pbrMetallicRoughness.baseColorFactor = [1.0, 1.0, 1.0, 1.0]
    # Face UVs reach their exact 0/1 borders.  Clamp prevents mip/bilinear
    # sampling from wrapping the opposite edge into a grazing-angle seam.
    gltf.samplers = [Sampler(wrapS=33071, wrapT=33071)]
    for texture in gltf.textures or []:
        texture.sampler = 0
    gltf.asset.generator = f"QFX5110 exact-exterior new-build / trimesh+pygltflib / {profile}"
    gltf.asset.extras = {
        "manufacturer": "Juniper Networks",
        "exact_product_id": "QFX5110-48S-AFI",
        "installed_configuration": "48 SFP+ + 4 QSFP28; five AFI fans; two 650W AC-AFI PSUs; front ears",
        "source_model_used": False,
        "bottom_mode": "GENERIC_BOTTOM_FALLBACK",
    }
    gltf.save_binary(str(path))


def export(profile: str, filename: str) -> Path:
    textures = prepare_textures(profile)
    scene = build_scene(textures)
    data = trimesh.exchange.gltf.export_glb(scene, include_normals=True)
    path = MODEL / filename
    path.write_bytes(data)
    patch_unlit_and_metadata(path, profile)
    return path


def main() -> None:
    MODEL.mkdir(parents=True, exist_ok=True)
    standard = export("standard", "Juniper-QFX5110.glb")
    web = export("web", "Juniper-QFX5110-web.glb")
    for path in (standard, web):
        print(path, path.stat().st_size)


if __name__ == "__main__":
    main()
