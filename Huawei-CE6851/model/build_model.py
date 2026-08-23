#!/usr/bin/env python3
"""Build exact-exterior Huawei CE6851-HI-B-B0A standard/web GLBs.

Coordinate convention: +X device right from the port side, +Y up, +Z port side.
All authored dimensions are metres. This is a new exterior construction; no
official or third-party mesh is copied.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
from PIL import Image
from pygltflib import GLTF2
from shapely.geometry import Point, box as sbox
from shapely.ops import unary_union
import trimesh
from trimesh.visual import TextureVisuals
from trimesh.visual.material import PBRMaterial


ROOT = Path(__file__).resolve().parents[1]
VIEWS = ROOT / "views"
MODEL = ROOT / "model"
QA = ROOT / "qa"

BODY_W = 0.4420
BODY_H = 0.0436
BODY_D = 0.4200
RACK_W = 0.4826
EAR_EXT = (RACK_W - BODY_W) / 2.0
FRONT_Z = BODY_D / 2.0
REAR_Z = -BODY_D / 2.0


def pbr(name: str, rgba, metallic: float = 0.0, roughness: float = 0.78) -> PBRMaterial:
    return PBRMaterial(
        name=name,
        baseColorFactor=list(rgba),
        metallicFactor=metallic,
        roughnessFactor=roughness,
        alphaMode="OPAQUE",
        doubleSided=False,
    )


MAT_BODY = pbr("Huawei black powder-coated chassis", (0.075, 0.080, 0.078, 1.0), 0.04, 0.82)
MAT_BLACK = pbr("Connector and honeycomb black", (0.010, 0.012, 0.011, 1.0), 0.0, 0.90)
MAT_SILVER = pbr("Stamped and plated silver metal", (0.63, 0.64, 0.61, 1.0), 0.35, 0.46)
MAT_DARK_SILVER = pbr("Dark galvanized frame", (0.31, 0.32, 0.30, 1.0), 0.18, 0.62)
MAT_GREEN = pbr("Status green", (0.08, 0.48, 0.17, 1.0), 0.0, 0.35)
MAT_YELLOW = pbr("Grounding yellow", (0.96, 0.72, 0.03, 1.0), 0.0, 0.50)
MAT_PINK = pbr("Huawei management label pink", (0.84, 0.42, 0.47, 1.0), 0.0, 0.65)


def set_material(mesh: trimesh.Trimesh, material: PBRMaterial) -> trimesh.Trimesh:
    mesh.visual = TextureVisuals(
        uv=np.zeros((len(mesh.vertices), 2), dtype=np.float32), material=material
    )
    return mesh


def make_box(extents, center, material=MAT_BODY) -> trimesh.Trimesh:
    mesh = trimesh.creation.box(extents=np.asarray(extents, dtype=float))
    mesh.apply_translation(np.asarray(center, dtype=float))
    return set_material(mesh, material)


def make_cylinder(radius, height, center, material, sections=24, axis=(0, 0, 1)):
    mesh = trimesh.creation.cylinder(radius=radius, height=height, sections=sections)
    axis = np.asarray(axis, dtype=float)
    axis /= np.linalg.norm(axis)
    transform = trimesh.geometry.align_vectors([0.0, 0.0, 1.0], axis)
    mesh.apply_transform(transform)
    mesh.apply_translation(np.asarray(center, dtype=float))
    return set_material(mesh, material)


def cylinder_between(a, b, radius, material, sections=18):
    a = np.asarray(a, dtype=float)
    b = np.asarray(b, dtype=float)
    delta = b - a
    return make_cylinder(
        radius, np.linalg.norm(delta), (a + b) / 2.0, material, sections, delta
    )


def add(scene: trimesh.Scene, name: str, mesh: trimesh.Trimesh) -> None:
    mesh.metadata["name"] = name
    scene.add_geometry(mesh, node_name=name, geom_name=name)


def add_group(scene: trimesh.Scene, name: str, meshes, material: PBRMaterial) -> None:
    if not meshes:
        return
    merged = trimesh.util.concatenate(meshes)
    set_material(merged, material)
    add(scene, name, merged)


def tight_crop(image: Image.Image) -> Image.Image:
    rgba = image.convert("RGBA")
    alpha = rgba.getchannel("A").point(lambda value: 255 if value > 8 else 0)
    bbox = alpha.getbbox()
    if bbox:
        rgba = rgba.crop(bbox)
    return rgba


def flatten_rgba(image: Image.Image, background) -> Image.Image:
    rgba = image.convert("RGBA")
    base = Image.new("RGBA", rgba.size, background)
    base.alpha_composite(rgba)
    return base.convert("RGB")


def prepare_textures(profile: str) -> dict[str, Image.Image]:
    out_dir = QA / "work" / "model-textures" / profile
    out_dir.mkdir(parents=True, exist_ok=True)
    images = {face: tight_crop(Image.open(VIEWS / f"{face}.png")) for face in (
        "front", "rear", "left", "right", "top", "bottom"
    )}

    # front.png is the complete elevation. Ears are true separate geometry in
    # the GLB, so retain only the body-width center crop for the face texture.
    front = images["front"]
    body_px = round(front.width * BODY_W / RACK_W)
    body_x = max(0, (front.width - body_px) // 2)
    images["front"] = front.crop((body_x, 0, body_x + body_px, front.height))

    backgrounds = {
        "front": (135, 137, 132, 255),
        "rear": (17, 19, 18, 255),
        "left": (18, 20, 19, 255),
        "right": (18, 20, 19, 255),
        "top": (35, 37, 38, 255),
        "bottom": (36, 38, 38, 255),
    }
    limits = {
        "standard": {"front": 3072, "rear": 3072, "left": 3072, "right": 3072, "top": 2048, "bottom": 2048},
        "web": {"front": 2048, "rear": 2048, "left": 2048, "right": 2048, "top": 1536, "bottom": 1536},
    }[profile]
    result = {}
    for face, image in images.items():
        rgb = flatten_rgba(image, backgrounds[face])
        limit = limits[face]
        scale = limit / max(rgb.size)
        if abs(scale - 1.0) > 1e-6:
            rgb = rgb.resize(
                (max(1, round(rgb.width * scale)), max(1, round(rgb.height * scale))),
                Image.Resampling.LANCZOS,
            )
        rgb.save(out_dir / f"{face}.png", optimize=True)
        result[face] = rgb
    return result


def texture_material(face: str, image: Image.Image) -> PBRMaterial:
    return PBRMaterial(
        name=f"tex_{face}",
        baseColorFactor=[1.0, 1.0, 1.0, 1.0],
        baseColorTexture=image,
        metallicFactor=0.0,
        roughnessFactor=0.86,
        alphaMode="OPAQUE",
        doubleSided=False,
    )


def textured_quad(face: str, image: Image.Image) -> trimesh.Trimesh:
    eps = 0.00008
    x0, x1 = -BODY_W / 2, BODY_W / 2
    y0, y1 = -BODY_H / 2, BODY_H / 2
    z0, z1 = REAR_Z, FRONT_Z
    if face == "front":
        verts = [[x0, y0, z1 + eps], [x1, y0, z1 + eps], [x1, y1, z1 + eps], [x0, y1, z1 + eps]]
    elif face == "rear":
        verts = [[x1, y0, z0 - eps], [x0, y0, z0 - eps], [x0, y1, z0 - eps], [x1, y1, z0 - eps]]
    elif face == "left":
        verts = [[x0 - eps, y0, z0], [x0 - eps, y0, z1], [x0 - eps, y1, z1], [x0 - eps, y1, z0]]
    elif face == "right":
        verts = [[x1 + eps, y0, z1], [x1 + eps, y0, z0], [x1 + eps, y1, z0], [x1 + eps, y1, z1]]
    elif face == "top":
        verts = [[x0, y1 + eps, z1], [x1, y1 + eps, z1], [x1, y1 + eps, z0], [x0, y1 + eps, z0]]
    elif face == "bottom":
        # Natural underside view: with front at screen bottom, physical +X is screen left.
        # Order the corners in screen space (bottom-left, bottom-right,
        # top-right, top-left). This preserves the approved image orientation
        # and produces an outward -Y normal for single-sided rendering.
        verts = [[x1, y0 - eps, z1], [x0, y0 - eps, z1], [x0, y0 - eps, z0], [x1, y0 - eps, z0]]
    else:
        raise ValueError(face)
    uv = np.asarray([[0, 0], [1, 0], [1, 1], [0, 1]], dtype=np.float32)
    mesh = trimesh.Trimesh(
        vertices=np.asarray(verts), faces=np.asarray([[0, 1, 2], [0, 2, 3]]), process=False
    )
    mesh.visual = TextureVisuals(uv=uv, material=texture_material(face, image))
    return mesh


def rounded_rect(x0, y0, x1, y1, radius):
    cores = [sbox(x0 + radius, y0, x1 - radius, y1), sbox(x0, y0 + radius, x1, y1 - radius)]
    corners = [Point(x, y).buffer(radius, resolution=12)
               for x in (x0 + radius, x1 - radius)
               for y in (y0 + radius, y1 - radius)]
    return unary_union([*cores, *corners])


def rack_ear(sign: int) -> trimesh.Trimesh:
    width = EAR_EXT
    plate = sbox(-width / 2, -BODY_H / 2, width / 2, BODY_H / 2)
    for cy in (-0.0125, 0.0125):
        plate = plate.difference(rounded_rect(-0.0051, cy - 0.0037, 0.0051, cy + 0.0037, 0.0035))
    mesh = trimesh.creation.extrude_polygon(plate, height=0.0025, mid_plane=True)
    mesh.apply_translation([sign * (BODY_W / 2 + width / 2), 0, FRONT_Z - 0.00125])
    return set_material(mesh, MAT_BODY)


def frame_bars(cx, cy, width, height, z, depth=0.0007, bar=0.0010):
    return [
        make_box([width, bar, depth], [cx, cy + height / 2, z], MAT_SILVER),
        make_box([width, bar, depth], [cx, cy - height / 2, z], MAT_SILVER),
        make_box([bar, height, depth], [cx - width / 2, cy, z], MAT_SILVER),
        make_box([bar, height, depth], [cx + width / 2, cy, z], MAT_SILVER),
    ]


def build_scene(textures: dict[str, Image.Image]) -> trimesh.Scene:
    scene = trimesh.Scene(base_frame="Huawei-CE6851-HI-B-B0A")
    scene.metadata.update({
        "manufacturer": "Huawei Technologies Co., Ltd.",
        "product_id": "CE6851-48S6Q-HI",
        "ordering_part_number": "02350JAS",
        "part_model": "CE6851-HI-B-B0A",
        "configuration": "48x10GE SFP+; 6x40GE QSFP+; 2xPAC-600WA-B; 2xFAN-40EA-B; port-side intake",
        "units": "metres",
        "coordinate_convention": "+X right from port side; +Y up; +Z port side/front",
        "source_model_used": False,
        "bottom_mode": "SOURCE_LOCKED_GENERATION",
    })

    # Closed shell. Rear modules occupy the remaining depth to the -210 mm envelope.
    add(scene, "Closed_Chassis_Shell", make_box([BODY_W, BODY_H, 0.414], [0, 0, 0.003], MAT_BODY))
    for face in ("front", "rear", "left", "right", "top", "bottom"):
        add(scene, f"Face_{face.title()}_SourceLocked", textured_quad(face, textures[face]))

    # Separate port-side rack brackets with genuine openings.
    add(scene, "Port_Side_Rack_Bracket_Left_2_Holes", rack_ear(-1))
    add(scene, "Port_Side_Rack_Bracket_Right_2_Holes", rack_ear(1))

    # 48 SFP+ cages: three framed 2x8 banks, odds over evens as photographed.
    sfp_black, sfp_lips, bank_frames = [], [], []
    bank_centers = (-0.1595, -0.0385, 0.0815)
    port_number = 1
    for bank_index, bank_x in enumerate(bank_centers):
        bank_frames.extend(frame_bars(bank_x, 0, 0.1170, 0.0320, FRONT_Z + 0.00045))
        for col in range(8):
            x = bank_x - 0.0510 + col * (0.1020 / 7.0)
            for row, y in enumerate((0.0068, -0.0068)):
                number = bank_index * 16 + col * 2 + row + 1
                sfp_black.append(make_box([0.0122, 0.0084, 0.0018], [x, y, FRONT_Z + 0.00095], MAT_BLACK))
                sfp_lips.append(make_box([0.0128, 0.00055, 0.0020], [x, y + 0.0045, FRONT_Z + 0.0011], MAT_SILVER))
                sfp_lips.append(make_box([0.0128, 0.00055, 0.0020], [x, y - 0.0045, FRONT_Z + 0.0011], MAT_SILVER))
                port_number += 1
    add_group(scene, "Front_SFPplus_Cages_48", sfp_black, MAT_BLACK)
    add_group(scene, "Front_SFPplus_Cage_Lips_48", sfp_lips, MAT_SILVER)
    add_group(scene, "Front_SFPplus_Bank_Frames_3", bank_frames, MAT_SILVER)

    # Six QSFP+ cages in three two-port columns at device physical right.
    qsfp_black, qsfp_lips, qsfp_frames = [], [], []
    for col, x in enumerate((0.1570, 0.1845, 0.2110)):
        qsfp_frames.extend(frame_bars(x, 0, 0.0240, 0.0325, FRONT_Z + 0.00045))
        for row, y in enumerate((0.0068, -0.0068)):
            qsfp_black.append(make_box([0.0190, 0.0090, 0.0020], [x, y, FRONT_Z + 0.0010], MAT_BLACK))
            qsfp_lips.append(make_box([0.0198, 0.00065, 0.0022], [x, y + 0.0049, FRONT_Z + 0.00115], MAT_SILVER))
            qsfp_lips.append(make_box([0.0198, 0.00065, 0.0022], [x, y - 0.0049, FRONT_Z + 0.00115], MAT_SILVER))
    add_group(scene, "Front_QSFPplus_Cages_6", qsfp_black, MAT_BLACK)
    add_group(scene, "Front_QSFPplus_Cage_Lips_6", qsfp_lips, MAT_SILVER)
    add_group(scene, "Front_QSFPplus_Frames_3", qsfp_frames, MAT_SILVER)

    # Tiny front status indicators retain source texture identity while receiving relief.
    leds = [make_cylinder(0.00115, 0.0008, [-0.207 + i * 0.010, -0.0145, FRONT_Z + 0.0007],
                          MAT_GREEN if i < 2 else MAT_DARK_SILVER, 16, (0, 0, 1)) for i in range(3)]
    add_group(scene, "Front_SYS_MST_ID_Indicators", leds, MAT_GREEN)

    # Rear hot-swap module bodies: physical +X appears at source-view left.
    rear_modules = [
        ("PSU1_PAC-600WA-B", 0.169, 0.104),
        ("FAN1_FAN-40EA-B", 0.071, 0.092),
        ("Management", 0.000, 0.050),
        ("FAN2_FAN-40EA-B", -0.071, 0.092),
        ("PSU2_PAC-600WA-B", -0.169, 0.104),
    ]
    for name, x, width in rear_modules:
        add(scene, f"Rear_Module_{name}", make_box([width - 0.0012, 0.0414, 0.0060], [x, 0, -0.2070], MAT_BODY))

    # Module seams create real parallax beyond the source-locked rear plane.
    seam_x = (0.117, 0.025, -0.025, -0.117)
    add_group(scene, "Rear_HotSwap_Module_Seams", [
        make_box([0.0012, 0.0410, 0.0012], [x, 0, REAR_Z - 0.00045], MAT_BLACK) for x in seam_x
    ], MAT_BLACK)

    # Four projecting silver U handles: PSU, fan, fan, PSU.
    for index, x in enumerate((0.169, 0.071, -0.071, -0.169)):
        z_face, z_out = REAR_Z - 0.0002, REAR_Z - 0.0036
        handle = [
            cylinder_between([x, -0.012, z_face], [x, -0.012, z_out], 0.00115, MAT_SILVER),
            cylinder_between([x, 0.012, z_face], [x, 0.012, z_out], 0.00115, MAT_SILVER),
            cylinder_between([x, -0.012, z_out], [x, 0.012, z_out], 0.00115, MAT_SILVER),
        ]
        add_group(scene, f"Rear_HotSwap_Silver_Handle_{index+1}", handle, MAT_SILVER)

    # AC inlets and black retainer/ejector hardware.
    for index, x in enumerate((0.183, -0.183)):
        add(scene, f"Rear_PSU_{index+1}_IEC_C14_Inlet", make_box([0.026, 0.020, 0.0018], [x, 0.0005, REAR_Z - 0.0010], MAT_BLACK))
        add(scene, f"Rear_PSU_{index+1}_Power_Switch", make_box([0.008, 0.016, 0.0019], [x - np.sign(x) * 0.032, 0, REAR_Z - 0.0010], MAT_BLACK))
        # Restraint bar around the IEC connector.
        retainer = [
            cylinder_between([x - 0.014, -0.011, REAR_Z - 0.0012], [x - 0.014, 0.011, REAR_Z - 0.0012], 0.0009, MAT_DARK_SILVER),
            cylinder_between([x + 0.014, -0.011, REAR_Z - 0.0012], [x + 0.014, 0.011, REAR_Z - 0.0012], 0.0009, MAT_DARK_SILVER),
        ]
        add_group(scene, f"Rear_PSU_{index+1}_Cord_Retainer", retainer, MAT_DARK_SILVER)

    # Central management panel relief.
    add(scene, "Rear_Console_RJ45", make_box([0.0155, 0.0125, 0.0019], [0.008, 0.0080, REAR_Z - 0.0010], MAT_BLACK))
    add(scene, "Rear_ETH_Management_RJ45", make_box([0.0155, 0.0125, 0.0019], [0.008, -0.0070, REAR_Z - 0.0010], MAT_BLACK))
    add(scene, "Rear_USB_Type_A", make_box([0.0065, 0.0170, 0.0019], [-0.0105, 0.0005, REAR_Z - 0.0010], MAT_BLACK))
    add(scene, "Rear_Barcode_Pull_Tab", make_box([0.0180, 0.0030, 0.0040], [0.000, -0.0202, REAR_Z - 0.0018], MAT_SILVER))
    add_group(scene, "Rear_ACT_LA_ID_LEDs", [
        make_cylinder(0.0009, 0.0008, [-0.001, 0.008 - i * 0.006, REAR_Z - 0.0011], MAT_GREEN, 14, (0, 0, -1))
        for i in range(3)
    ], MAT_GREEN)

    # Module captive screws/status heads.
    screw_x = (0.216, 0.118, 0.025, -0.025, -0.118, -0.216)
    add_group(scene, "Rear_Captive_Screws", [
        make_cylinder(0.0020, 0.0010, [x, 0.0155, REAR_Z - 0.0007], MAT_DARK_SILVER, 18, (0, 0, -1))
        for x in screw_x
    ], MAT_DARK_SILVER)

    # Distinct left/right side mechanical evidence. Physical right has ground stud.
    add(scene, "Right_Side_Ground_Washer", make_cylinder(0.0052, 0.0011, [BODY_W/2 + 0.00055, -0.002, 0.000], MAT_SILVER, 24, (1, 0, 0)))
    add(scene, "Right_Side_Ground_Stud", make_cylinder(0.0024, 0.0048, [BODY_W/2 + 0.0030, -0.002, 0.000], MAT_DARK_SILVER, 20, (1, 0, 0)))
    add(scene, "Right_Side_Yellow_Earth_Mark", make_box([0.0007, 0.0085, 0.0085], [BODY_W/2 + 0.00035, -0.0110, 0.000], MAT_YELLOW))

    side_fasteners = {
        "Left": (-1, [-0.185, -0.155, 0.155, 0.185]),
        "Right": (1, [-0.185, -0.155, 0.155, 0.185]),
    }
    for label, (sign, zs) in side_fasteners.items():
        meshes = []
        for row_y in (-0.0105, 0.0105):
            for z in zs:
                meshes.append(make_cylinder(0.00165, 0.0008,
                    [sign * (BODY_W/2 + 0.0004), row_y, z], MAT_DARK_SILVER, 16, (sign, 0, 0)))
        add_group(scene, f"{label}_Side_Mounting_Fasteners", meshes, MAT_DARK_SILVER)

    # Top port-side perforation panel relief and three exact field divisions.
    add(scene, "Top_PortSide_Vent_Recess", make_box([BODY_W - 0.004, 0.0007, 0.065], [0, BODY_H/2 + 0.0002, FRONT_Z - 0.0325], MAT_BLACK))
    add_group(scene, "Top_Vent_Field_Dividers_2", [
        make_box([0.0014, 0.0009, 0.064], [x, BODY_H/2 + 0.00055, FRONT_Z - 0.0325], MAT_DARK_SILVER)
        for x in (-0.060, 0.100)
    ], MAT_DARK_SILVER)
    add(scene, "Top_Transverse_Cover_Seam", make_box([BODY_W - 0.004, 0.00065, 0.0015], [0, BODY_H/2 + 0.00045, FRONT_Z - 0.067], MAT_DARK_SILVER))

    # Exact underside stampings: five long ribs plus one transverse rear rib.
    ribs = [make_box([0.030, 0.0012, 0.125], [x, -BODY_H/2 - 0.00045, -0.060], MAT_DARK_SILVER)
            for x in (-0.160, -0.080, 0.000, 0.080, 0.160)]
    add_group(scene, "Bottom_Longitudinal_Stamped_Ribs_5", ribs, MAT_DARK_SILVER)
    add(scene, "Bottom_Transverse_Stamped_Rib_1", make_box([0.405, 0.0012, 0.018], [0, -BODY_H/2 - 0.00045, -0.176], MAT_DARK_SILVER))
    bottom_screws = []
    for x, z in ((-0.185,0.175),(-0.090,0.175),(0,0.175),(0.090,0.175),(0.185,0.175),
                 (-0.185,0.055),(-0.090,0.020),(0,-0.005),(0.090,0.020),(0.185,0.055),
                 (-0.185,-0.190),(-0.090,-0.190),(0,-0.190),(0.090,-0.190),(0.185,-0.190)):
        bottom_screws.append(make_cylinder(0.0015, 0.0007, [x, -BODY_H/2 - 0.0006, z], MAT_DARK_SILVER, 16, (0, -1, 0)))
    add_group(scene, "Bottom_Visible_Fasteners", bottom_screws, MAT_DARK_SILVER)

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
                material.pbrMetallicRoughness.baseColorFactor = [1.0, 1.0, 1.0, 1.0]
                material.pbrMetallicRoughness.metallicFactor = 0.0
                material.pbrMetallicRoughness.roughnessFactor = 0.86
    gltf.asset.generator = f"Huawei CE6851 exact-exterior new-build / trimesh+pygltflib / {profile}"
    gltf.asset.extras = {
        "manufacturer": "Huawei Technologies Co., Ltd.",
        "exact_product_id": "CE6851-48S6Q-HI",
        "ordering_part_number": "02350JAS",
        "part_model": "CE6851-HI-B-B0A",
        "installed_configuration": "48x10GE SFP+; 6x40GE QSFP+; dual PAC-600WA-B AC; dual FAN-40EA-B; port-side intake",
        "source_model_used": False,
        "bottom_mode": "SOURCE_LOCKED_GENERATION",
        "coordinate_convention": "+X device-right from port side; +Y up; +Z port side/front",
    }
    gltf.save_binary(str(path))


def export(profile: str, filename: str) -> Path:
    textures = prepare_textures(profile)
    scene = build_scene(textures)
    payload = trimesh.exchange.gltf.export_glb(scene, include_normals=True)
    path = MODEL / filename
    path.write_bytes(payload)
    patch_unlit_and_metadata(path, profile)
    return path


def main() -> None:
    MODEL.mkdir(parents=True, exist_ok=True)
    for profile, filename in (
        ("standard", "Huawei-CE6851.glb"),
        ("web", "Huawei-CE6851-web.glb"),
    ):
        path = export(profile, filename)
        print(f"wrote {path} ({path.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
