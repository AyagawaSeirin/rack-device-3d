#!/usr/bin/env python3
"""Build the Dell EMC PowerEdge C6400 + four C6420 2.5-inch AC GLBs.

This is a newly authored exact-exterior website model.  It does not reuse an
official or third-party mesh.  Coordinate convention: +X is device-right when
seen from the front, +Y is up, and +Z is the 24-drive front.  Units are metres.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
from PIL import Image
from pygltflib import GLTF2
import trimesh
from trimesh.visual import TextureVisuals
from trimesh.visual.material import PBRMaterial


ROOT = Path(__file__).resolve().parents[1]
MODEL = ROOT / "model"
VIEWS = ROOT / "views"

# Dell published physical dimensions.  The body datums and the fully installed
# silhouette are kept separate so texture rectification and GLB bounds are both
# auditable.
BODY_W = 0.4480
BODY_H = 0.0868
BODY_D = 0.7632
INSTALLED_W = 0.4826
INSTALLED_D = 0.7973
BODY_FRONT = BODY_D / 2.0
BODY_REAR = -BODY_D / 2.0
OUTER_FRONT = INSTALLED_D / 2.0
OUTER_REAR = -INSTALLED_D / 2.0

# Rotation-stability depth ledger.  The photographic cards are deliberately
# inset behind physical relief; boundaries, ports/grilles and handles occupy
# distinct outward layers.  This prevents equal-depth writes and z-fighting
# without changing Dell's published installed envelope.
FRONT_TEXTURE_Z = OUTER_FRONT - 0.00045
REAR_TEXTURE_Z = OUTER_REAR + 0.00012
SIDE_TEXTURE_X = BODY_W / 2.0 - 0.00045
TOP_TEXTURE_Y = BODY_H / 2.0 - 0.00045
REAR_BOUNDARY_Z = OUTER_REAR + 0.00010
REAR_PORT_Z = OUTER_REAR + 0.000065
REAR_GRILLE_Z = OUTER_REAR + 0.00003
REAR_OUTERMOST_Z = OUTER_REAR + 0.00003


def pbr(name: str, rgba, metallic: float = 0.0, roughness: float = 0.82) -> PBRMaterial:
    return PBRMaterial(
        name=name,
        baseColorFactor=list(rgba),
        metallicFactor=metallic,
        roughnessFactor=roughness,
        alphaMode="OPAQUE",
        doubleSided=False,
    )


MAT_CHASSIS = pbr("C6400 galvanized and silver chassis", (151, 156, 158, 255), 0.42, 0.55)
MAT_LIGHT = pbr("C6400 light plated steel", (196, 198, 196, 255), 0.48, 0.46)
MAT_DARK_SILVER = pbr("C6400 dark plated frame", (82, 86, 86, 255), 0.34, 0.55)
MAT_BLACK = pbr("C6420 connector and recess black", (12, 14, 15, 255), 0.0, 0.90)
MAT_DARK = pbr("C6420 deep vent cavity", (28, 31, 32, 255), 0.0, 0.92)
MAT_ORANGE = pbr("Dell 2.5-inch carrier orange release", (233, 91, 22, 255), 0.0, 0.54)
MAT_BLUE = pbr("Dell C6420 blue pull handle", (18, 86, 168, 255), 0.0, 0.48)
MAT_GREEN = pbr("EPP PSU green release", (41, 143, 91, 255), 0.0, 0.52)
MAT_LED = pbr("Dell status lens", (84, 143, 113, 255), 0.0, 0.30)


def set_material(mesh: trimesh.Trimesh, material: PBRMaterial) -> trimesh.Trimesh:
    mesh.visual = TextureVisuals(
        uv=np.zeros((len(mesh.vertices), 2), dtype=np.float32), material=material
    )
    return mesh


def make_box(extents, center, material=MAT_CHASSIS) -> trimesh.Trimesh:
    mesh = trimesh.creation.box(extents=np.asarray(extents, dtype=float))
    mesh.apply_translation(np.asarray(center, dtype=float))
    return set_material(mesh, material)


def make_cylinder(radius, height, center, material, sections=24, axis=(0, 0, 1)):
    mesh = trimesh.creation.cylinder(radius=radius, height=height, sections=sections)
    axis = np.asarray(axis, dtype=float)
    axis /= np.linalg.norm(axis)
    mesh.apply_transform(trimesh.geometry.align_vectors([0.0, 0.0, 1.0], axis))
    mesh.apply_translation(np.asarray(center, dtype=float))
    return set_material(mesh, material)


def make_torus(major, minor, center, material, major_sections=20, minor_sections=8):
    mesh = trimesh.creation.torus(
        major_radius=major,
        minor_radius=minor,
        major_sections=major_sections,
        minor_sections=minor_sections,
    )
    mesh.apply_translation(np.asarray(center, dtype=float))
    return set_material(mesh, material)


def add(scene: trimesh.Scene, name: str, mesh: trimesh.Trimesh) -> None:
    mesh.metadata["name"] = name
    scene.add_geometry(mesh, node_name=name, geom_name=name)


def add_group(scene: trimesh.Scene, name: str, meshes, material: PBRMaterial) -> None:
    if not meshes:
        return
    merged = trimesh.util.concatenate(meshes)
    set_material(merged, material)
    add(scene, name, merged)


def frame_bars(cx, cy, width, height, z, depth=0.00018, bar=0.00055,
               material=MAT_DARK_SILVER):
    return [
        make_box([width, bar, depth], [cx, cy + height / 2.0, z], material),
        make_box([width, bar, depth], [cx, cy - height / 2.0, z], material),
        make_box([bar, height, depth], [cx - width / 2.0, cy, z], material),
        make_box([bar, height, depth], [cx + width / 2.0, cy, z], material),
    ]


def prepare_texture(face: str, profile: str) -> Image.Image:
    source = Image.open(VIEWS / f"{face}.png").convert("RGBA")
    # The GLB main faces are intentionally opaque.  Alpha from chroma removal is
    # edge anti-aliasing only, so it is composited over face-matched metal/black.
    fills = {
        "front": (22, 23, 24, 255),
        "rear": (31, 33, 34, 255),
        "left": (143, 147, 148, 255),
        "right": (143, 147, 148, 255),
        "top": (152, 156, 157, 255),
        "bottom": (151, 155, 156, 255),
    }
    opaque = Image.new("RGBA", source.size, fills[face])
    opaque.alpha_composite(source)
    image = opaque.convert("RGB")
    limit = 4096 if profile == "standard" else 2048
    if max(image.size) > limit:
        scale = limit / max(image.size)
        image = image.resize(
            (max(1, round(image.width * scale)), max(1, round(image.height * scale))),
            Image.Resampling.LANCZOS,
        )
    out_dir = MODEL / "textures" / profile
    out_dir.mkdir(parents=True, exist_ok=True)
    output = out_dir / f"{face}.jpg"
    image.save(output, format="JPEG", quality=95 if profile == "standard" else 90,
               optimize=True, subsampling=0)
    return Image.open(output).convert("RGB")


def texture_material(face: str, image: Image.Image) -> PBRMaterial:
    return PBRMaterial(
        name=f"SOURCE_LOCKED_{face.upper()}_opaque_texture",
        baseColorFactor=[255, 255, 255, 255],
        baseColorTexture=image,
        metallicFactor=0.0,
        roughnessFactor=0.90,
        alphaMode="OPAQUE",
        doubleSided=False,
    )


def textured_quad(face: str, image: Image.Image) -> trimesh.Trimesh:
    bx0, bx1 = -BODY_W / 2.0, BODY_W / 2.0
    iy0, iy1 = -BODY_H / 2.0, BODY_H / 2.0
    bz0, bz1 = BODY_REAR, BODY_FRONT
    if face == "front":
        x0, x1, z = -INSTALLED_W / 2.0, INSTALLED_W / 2.0, FRONT_TEXTURE_Z
        verts = [[x0, iy0, z], [x1, iy0, z], [x1, iy1, z], [x0, iy1, z]]
    elif face == "rear":
        z = REAR_TEXTURE_Z
        verts = [[bx1, iy0, z], [bx0, iy0, z], [bx0, iy1, z], [bx1, iy1, z]]
    elif face == "left":
        x = -SIDE_TEXTURE_X
        verts = [[x, iy0, bz0], [x, iy0, bz1],
                 [x, iy1, bz1], [x, iy1, bz0]]
    elif face == "right":
        x = SIDE_TEXTURE_X
        verts = [[x, iy0, bz1], [x, iy0, bz0],
                 [x, iy1, bz0], [x, iy1, bz1]]
    elif face == "top":
        verts = [[bx0, TOP_TEXTURE_Y, bz1], [bx1, TOP_TEXTURE_Y, bz1],
                 [bx1, TOP_TEXTURE_Y, bz0], [bx0, TOP_TEXTURE_Y, bz0]]
    elif face == "bottom":
        verts = [[bx1, iy0, bz1], [bx0, iy0, bz1],
                 [bx0, iy0, bz0], [bx1, iy0, bz0]]
    else:
        raise ValueError(face)
    uv = np.asarray([[0, 0], [1, 0], [1, 1], [0, 1]], dtype=np.float32)
    mesh = trimesh.Trimesh(
        vertices=np.asarray(verts, dtype=float),
        faces=np.asarray([[0, 1, 2], [0, 2, 3]], dtype=np.int64),
        process=False,
    )
    mesh.visual = TextureVisuals(uv=uv, material=texture_material(face, image))
    return mesh


def build_front(scene: trimesh.Scene, sections: int) -> None:
    # Full-width front control/rack ears and their side returns establish the
    # exact 482.6 mm overall width and 797.3 mm installed depth.
    ear_w = (INSTALLED_W - BODY_W) / 2.0
    # Keep the broad ear metal behind the source-locked front plane so it adds
    # true oblique thickness without hiding the real Dell EMC/PowerEdge marks.
    ear_outer = OUTER_FRONT - 0.00015
    ear_z = (BODY_FRONT + ear_outer) / 2.0
    ear_d = ear_outer - BODY_FRONT
    for sign, side in ((-1, "Left"), (1, "Right")):
        x = sign * (BODY_W / 2.0 + ear_w / 2.0)
        add(scene, f"Front_Rack_Control_Ear_{side}",
            make_box([ear_w, BODY_H, ear_d], [x, 0.0, ear_z], MAT_CHASSIS))
        for idx, y in enumerate((-0.030, 0.030), start=1):
            add(scene, f"Front_Rack_Hole_Recess_{side}_{idx}",
                make_cylinder(0.0034, 0.00018,
                              [x, y, OUTER_FRONT - 0.00009], MAT_BLACK,
                              sections, (0, 0, 1)))

    # Twenty-four independently named vertical 2.5-inch carriers.  Their frames,
    # silver handle relief and orange release rings are true geometry while the
    # source-locked plane supplies exact labels and fine surface treatment.
    drive_left, drive_right = -0.194, 0.194
    pitch = (drive_right - drive_left) / 24.0
    carrier_w = pitch * 0.92
    face_z = OUTER_FRONT - 0.00011
    for index in range(24):
        x = drive_left + (index + 0.5) * pitch
        meshes = frame_bars(x, 0.0, carrier_w, 0.0750, face_z,
                            depth=0.00020, bar=0.00042, material=MAT_DARK_SILVER)
        meshes.append(make_box([0.00115, 0.054, 0.00020],
                               [x + carrier_w * 0.26, 0.002, face_z], MAT_LIGHT))
        add_group(scene, f"Front_Drive_Carrier_{index + 1:02d}_Frame_Handle",
                  meshes, MAT_DARK_SILVER)
        add(scene, f"Front_Drive_Carrier_{index + 1:02d}_Orange_Release_Ring",
            make_torus(0.00175, 0.00042,
                       [x - carrier_w * 0.12, -0.0320, OUTER_FRONT - 0.00042],
                       MAT_ORANGE, 20 if sections >= 24 else 16, 8))

    # Separate visible control/identity relief at each side.  Dell EMC,
    # PowerEdge and C6400 remain preserved in the photographic front texture.
    add_group(scene, "Front_Left_DellEMC_Control_Panel_Relief",
              frame_bars(-0.210, 0.0, 0.024, 0.053, face_z,
                         0.00020, 0.00050, MAT_DARK_SILVER), MAT_DARK_SILVER)
    add_group(scene, "Front_Right_PowerEdge_C6400_ID_Panel_Relief",
              frame_bars(0.210, 0.0, 0.024, 0.053, face_z,
                         0.00020, 0.00050, MAT_DARK_SILVER), MAT_DARK_SILVER)
    for index, (x, y) in enumerate(((-0.211, -0.022), (-0.211, -0.013),
                                    (0.211, -0.022), (0.211, -0.013)), start=1):
        add(scene, f"Front_Control_Status_Lens_{index}",
            make_cylinder(0.00145, 0.00020, [x, y, OUTER_FRONT - 0.00010],
                          MAT_LED, sections, (0, 0, 1)))


def build_rear(scene: trimesh.Scene, sections: int) -> None:
    # As at the front, module bodies sit behind the exact rear texture while
    # their seams, ports, handles and grilles remain true outward geometry.
    rear_outer = OUTER_REAR + 0.00015
    rear_z = (BODY_REAR + rear_outer) / 2.0
    rear_d = BODY_REAR - rear_outer
    center_w = 0.096
    side_w = (BODY_W - center_w) / 2.0
    module_h = BODY_H / 2.0

    # Four complete C6420 sleds, in the official rear order: 3/4 left and 1/2
    # right.  No sled is treated as the delivered chassis by itself.
    sled_specs = (
        (3, -center_w / 2.0 - side_w / 2.0, module_h / 2.0, "Left_Upper"),
        (4, -center_w / 2.0 - side_w / 2.0, -module_h / 2.0, "Left_Lower"),
        (1, center_w / 2.0 + side_w / 2.0, module_h / 2.0, "Right_Upper"),
        (2, center_w / 2.0 + side_w / 2.0, -module_h / 2.0, "Right_Lower"),
    )
    for sled, x, y, label in sled_specs:
        add(scene, f"Rear_C6420_Sled_{sled}_{label}_Body",
            make_box([side_w - 0.0014, module_h - 0.0012, rear_d],
                     [x, y, rear_z], MAT_DARK_SILVER))
        add_group(scene, f"Rear_C6420_Sled_{sled}_{label}_Boundary",
                  frame_bars(x, y, side_w - 0.0010, module_h - 0.0010,
                             REAR_BOUNDARY_Z, 0.00004, 0.00065, MAT_LIGHT), MAT_LIGHT)

        # Two blue USB-A inserts, one dedicated iDRAC RJ45, one VGA, a blank
        # low-profile slot, status lens, and blue service pull handle per sled.
        port_base_x = x + (-0.030 if x < 0 else 0.030)
        usb = [
            make_box([0.0090, 0.0032, 0.00005],
                     [port_base_x - 0.006, y + 0.004, REAR_PORT_Z], MAT_BLUE),
            make_box([0.0090, 0.0032, 0.00005],
                     [port_base_x - 0.006, y - 0.002, REAR_PORT_Z], MAT_BLUE),
        ]
        add_group(scene, f"Rear_C6420_Sled_{sled}_USB_A_Blue_2", usb, MAT_BLUE)
        add_group(scene, f"Rear_C6420_Sled_{sled}_iDRAC_RJ45",
                  frame_bars(port_base_x + 0.009, y + 0.002, 0.0130, 0.0100,
                             REAR_PORT_Z, 0.00005, 0.00045, MAT_BLACK), MAT_BLACK)
        add_group(scene, f"Rear_C6420_Sled_{sled}_VGA",
                  frame_bars(port_base_x + 0.028, y + 0.002, 0.0125, 0.0070,
                             REAR_PORT_Z, 0.00005, 0.00040, MAT_BLACK), MAT_BLACK)
        add(scene, f"Rear_C6420_Sled_{sled}_PCIe_Blank",
            make_box([0.050, 0.0045, 0.00005],
                     [x + (-0.044 if x < 0 else 0.044), y + 0.013, REAR_PORT_Z],
                     MAT_DARK_SILVER))
        add(scene, f"Rear_C6420_Sled_{sled}_Blue_Pull_Handle",
            make_box([0.0032, 0.019, 0.00006],
                     [(-center_w / 2.0 - 0.005) if x < 0 else (center_w / 2.0 + 0.005),
                      y, REAR_OUTERMOST_Z], MAT_BLUE))
        add(scene, f"Rear_C6420_Sled_{sled}_Status_Lens",
            make_cylinder(0.00125, 0.00006,
                          [x + (0.064 if x < 0 else -0.064), y - 0.012,
                           REAR_OUTERMOST_Z], MAT_LED, sections, (0, 0, 1)))

    # The two center EPP 1600 W modules are shared C6400 AC power supplies.
    for number, y in ((1, module_h / 2.0), (2, -module_h / 2.0)):
        add(scene, f"Rear_Shared_AC_EPP1600W_PSU_{number}_Body",
            make_box([center_w - 0.0012, module_h - 0.0012, rear_d],
                     [0.0, y, rear_z], MAT_DARK_SILVER))
        add_group(scene, f"Rear_Shared_AC_EPP1600W_PSU_{number}_Boundary",
                  frame_bars(0.0, y, center_w - 0.0010, module_h - 0.0010,
                             REAR_BOUNDARY_Z, 0.00004, 0.00065, MAT_LIGHT), MAT_LIGHT)
        add_group(scene, f"Rear_Shared_AC_EPP1600W_PSU_{number}_IEC_C14",
                  frame_bars(0.021, y, 0.027, 0.017, REAR_PORT_Z,
                             0.00005, 0.00075, MAT_BLACK), MAT_BLACK)
        add_group(scene, f"Rear_Shared_AC_EPP1600W_PSU_{number}_Fan_Cavity",
                  [make_torus(0.0108, 0.0010,
                              [-0.020, y, OUTER_REAR + 0.00101], MAT_DARK,
                              24 if sections >= 24 else 18, 8),
                   make_cylinder(0.0030, 0.00005,
                                 [-0.020, y, REAR_PORT_Z], MAT_DARK,
                                 sections, (0, 0, 1))], MAT_DARK)
        grille = []
        for offset in np.linspace(-0.010, 0.010, 5):
            grille.append(make_box([0.0010, 0.025, 0.00005],
                                   [-0.020 + float(offset), y, REAR_GRILLE_Z], MAT_LIGHT))
            grille.append(make_box([0.025, 0.0010, 0.00005],
                                   [-0.020, y + float(offset), REAR_GRILLE_Z], MAT_LIGHT))
        add_group(scene, f"Rear_Shared_AC_EPP1600W_PSU_{number}_Fan_Grille",
                  grille, MAT_LIGHT)
        add(scene, f"Rear_Shared_AC_EPP1600W_PSU_{number}_Green_Release",
            make_box([0.009, 0.004, 0.00006],
                     [0.039, y - 0.014, REAR_OUTERMOST_Z], MAT_GREEN))


def build_side_top_relief(scene: trimesh.Scene, sections: int) -> None:
    # Side details are authored from independent left/right locks.  The right
    # side has the real QR/part-label block in its texture; it is not mirrored to
    # the left.  Fastener/stamp placement is likewise deliberately asymmetric.
    side_specs = {
        "Left": (-1, [(-0.020, -0.290), (0.019, -0.065), (-0.021, 0.175),
                      (0.020, 0.320)]),
        "Right": (1, [(0.018, -0.315), (-0.021, -0.145), (0.019, 0.090),
                      (-0.020, 0.286)]),
    }
    for side, (sign, positions) in side_specs.items():
        x = sign * (BODY_W / 2.0 - 0.00010)
        for idx, (y, z) in enumerate(positions, start=1):
            add(scene, f"Side_{side}_Independent_Fastener_{idx}",
                make_cylinder(0.0021, 0.00020, [x, y, z], MAT_LIGHT,
                              sections, (sign, 0, 0)))
        # Long shallow stamped rail relief, different longitudinal positions.
        zc = -0.035 if sign < 0 else 0.022
        add(scene, f"Side_{side}_Stamped_Longitudinal_Rib",
            make_box([0.00020, 0.0060, 0.310], [x, 0.010 * sign, zc], MAT_LIGHT))

    # Three separately evidenced top cover/service regions, seam recesses and
    # perimeter fasteners.  The detailed Dell label blocks remain in the texture.
    top_seam_y = BODY_H / 2.0 - 0.00020
    top_fastener_y = BODY_H / 2.0 - 0.00010
    seams = []
    for z in (-0.216, 0.118, 0.302):
        seams.append(make_box([BODY_W - 0.008, 0.00016, 0.0010],
                              [0.0, top_seam_y, z], MAT_DARK_SILVER))
    for x in (-0.164, 0.164):
        seams.append(make_box([0.0010, 0.00016, 0.268],
                              [x, top_seam_y, 0.185], MAT_DARK_SILVER))
    add_group(scene, "Top_Three_Independent_Cover_Service_Panel_Seams", seams,
              MAT_DARK_SILVER)
    screws = []
    for x, z in ((-0.205, 0.350), (0.205, 0.350), (-0.205, 0.020),
                 (0.205, 0.020), (-0.205, -0.350), (0.205, -0.350)):
        screws.append(make_cylinder(0.0018, 0.00020,
                                    [x, top_fastener_y, z], MAT_LIGHT,
                                    sections, (0, 1, 0)))
    add_group(scene, "Top_Cover_Perimeter_Fasteners_6", screws, MAT_LIGHT)


def build_scene(profile: str) -> trimesh.Scene:
    textures = {face: prepare_texture(face, profile)
                for face in ("front", "rear", "left", "right", "top", "bottom")}
    sections = 24 if profile == "standard" else 18
    scene = trimesh.Scene(base_frame="Dell_C6400_C6420_2_5inch_ROOT")
    scene.metadata.update({
        "manufacturer": "Dell Technologies / Dell EMC",
        "product_family": "PowerEdge C Series",
        "enclosure": "PowerEdge C6400",
        "compute_sled": "PowerEdge C6420",
        "installed_configuration": "2U C6400; four C6420 sleds; 24 x 2.5-inch front carriers; two shared EPP 1600 W AC PSUs",
        "coordinate_convention": "+X device right from front; +Y up; +Z 24-drive front",
        "units": "metres",
        "source_model_used": False,
        "official_public_exact_3d_found": False,
        "bottom_mode": "GENERIC_BOTTOM_FALLBACK",
        "profile": profile,
    })

    add(scene, "Closed_C6400_Chassis_Core",
        make_box([BODY_W - 0.0020, BODY_H - 0.0020, BODY_D - 0.0020],
                 [0, 0, 0], MAT_CHASSIS))
    for face in ("front", "rear", "left", "right", "top", "bottom"):
        label = "BottomFallback" if face == "bottom" else "SourceLocked"
        add(scene, f"Face_{face.title()}_{label}", textured_quad(face, textures[face]))

    build_front(scene, sections)
    build_rear(scene, sections)
    build_side_top_relief(scene, sections)
    return scene


def add_asset_metadata(path: Path, profile: str) -> None:
    gltf = GLTF2().load_binary(str(path))
    used = list(gltf.extensionsUsed or [])
    if "KHR_materials_unlit" not in used:
        used.append("KHR_materials_unlit")
    gltf.extensionsUsed = used
    for material in gltf.materials or []:
        if material.name and material.name.startswith("SOURCE_LOCKED_"):
            material.extensions = dict(material.extensions or {})
            material.extensions["KHR_materials_unlit"] = {}
            material.alphaMode = "OPAQUE"
            material.doubleSided = False
    gltf.asset.generator = "Trimesh self-authored exact-exterior construction + pygltflib unlit texture pass"
    gltf.asset.extras = {
        "manufacturer": "Dell Technologies / Dell EMC",
        "product_family": "PowerEdge C Series",
        "enclosure": "PowerEdge C6400",
        "compute_sled": "PowerEdge C6420",
        "configuration": "2U / 4x C6420 / 24x2.5-inch / 2x shared EPP 1600W AC",
        "profile": profile,
        "body_dimensions_mm": [448.0, 86.8, 763.2],
        "installed_bounds_mm": [482.6, 86.8, 797.3],
        "bottom_mode": "GENERIC_BOTTOM_FALLBACK",
        "official_public_exact_3d_found": False,
        "source_model_used": False,
        "visible_counts": {
            "2_5_inch_drive_carriers": 24,
            "C6420_compute_sleds": 4,
            "shared_AC_EPP1600W_PSU": 2,
            "sled_USB_A": 8,
            "sled_iDRAC_RJ45": 4,
            "sled_VGA": 4,
            "sled_blue_pull_handles": 4,
        },
    }
    gltf.save_binary(str(path))


def export_profile(profile: str) -> Path:
    scene = build_scene(profile)
    name = "Dell-C6420-2.5inch.glb" if profile == "standard" else "Dell-C6420-2.5inch-web.glb"
    output = MODEL / name
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_bytes(scene.export(file_type="glb", include_normals=True))
    add_asset_metadata(output, profile)
    return output


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--profile", choices=("standard", "web", "both"), default="both")
    args = parser.parse_args()
    profiles = ("standard", "web") if args.profile == "both" else (args.profile,)
    result = []
    for profile in profiles:
        output = export_profile(profile)
        result.append({"profile": profile, "path": str(output), "bytes": output.stat().st_size})
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
