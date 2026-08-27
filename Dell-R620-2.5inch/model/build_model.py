#!/usr/bin/env python3
"""Build new exact-exterior Dell PowerEdge R620 10SFF website GLBs.

No official or third-party mesh is copied. Coordinates are metres in a
right-handed glTF frame: +X device right as seen from the front, +Y up,
+Z front. The body, front latches, ten carriers, rear I/O/PCIe/PSUs,
side rail interfaces, top latch and vent relief are independent geometry.
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

import numpy as np
from PIL import Image
from pygltflib import GLTF2
import trimesh
from trimesh.visual import TextureVisuals
from trimesh.visual.material import PBRMaterial


ROOT = Path(__file__).resolve().parents[1]
VIEWS = ROOT / "views"
MODEL = ROOT / "model"

BODY_W = 0.4340
BODY_H = 0.0428
FLANGE_TO_REAR_BODY = 0.7310
FRONT_PROJECTION = 0.0204
FLANGE_TO_REAR_MOST = 0.7521
# Dell Figure 14 measures Zb/Zc from the EIA rack flange.  The complete body
# and installed envelope must therefore include Za as well.
BODY_D = FRONT_PROJECTION + FLANGE_TO_REAR_BODY
INSTALLED_D = FRONT_PROJECTION + FLANGE_TO_REAR_MOST
RACK_W = 0.4824
EAR_EXT = (RACK_W - BODY_W) / 2.0
FRONT_MOST_Z = BODY_D / 2.0
RACK_FLANGE_Z = FRONT_MOST_Z - FRONT_PROJECTION
REAR_BODY_Z = -BODY_D / 2.0
REAR_MOST_Z = RACK_FLANGE_Z - FLANGE_TO_REAR_MOST
REAR_PROJECTION = REAR_BODY_Z - REAR_MOST_Z


def pbr(name: str, rgba, metallic: float = 0.0, roughness: float = 0.78) -> PBRMaterial:
    return PBRMaterial(
        name=name,
        baseColorFactor=list(rgba),
        metallicFactor=metallic,
        roughnessFactor=roughness,
        alphaMode="OPAQUE",
        doubleSided=False,
    )


MAT_BODY = pbr("Dell R620 galvanized chassis steel", (184, 187, 185, 255), 0.42, 0.58)
MAT_SILVER = pbr("Dell plated carrier and connector steel", (169, 173, 172, 255), 0.48, 0.48)
MAT_DARK_SILVER = pbr("Dell dark galvanized relief", (91, 96, 95, 255), 0.31, 0.64)
MAT_BLACK = pbr("Dell black polymer", (14, 16, 17, 255), 0.0, 0.88)
MAT_DARK = pbr("Opaque port and fan cavity", (21, 24, 25, 255), 0.0, 0.93)
MAT_ORANGE = pbr("Dell release orange", (204, 82, 20, 255), 0.0, 0.56)
MAT_GREEN = pbr("Dell green status lens", (42, 190, 73, 255), 0.0, 0.30)
MAT_AMBER = pbr("Dell amber status lens", (231, 141, 25, 255), 0.0, 0.35)
MAT_BLUE = pbr("Dell VGA blue", (32, 119, 180, 255), 0.0, 0.42)
MAT_TEAL = pbr("Dell serial teal", (31, 145, 141, 255), 0.0, 0.48)
MAT_GOLD = pbr("Connector pin gold", (191, 145, 57, 255), 0.58, 0.34)
MAT_CLEAR_GRAY = pbr("AC PSU translucent handle approximation", (166, 174, 176, 255), 0.0, 0.42)


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


def cylinder_between(a, b, radius, material, sections=24):
    a = np.asarray(a, dtype=float)
    b = np.asarray(b, dtype=float)
    delta = b - a
    return make_cylinder(radius, np.linalg.norm(delta), (a + b) / 2.0,
                         material, sections, delta)


def add(scene: trimesh.Scene, name: str, mesh: trimesh.Trimesh) -> None:
    mesh.metadata["name"] = name
    scene.add_geometry(mesh, node_name=name, geom_name=name)


def add_group(scene: trimesh.Scene, name: str, meshes, material: PBRMaterial) -> None:
    if not meshes:
        return
    merged = trimesh.util.concatenate(meshes)
    set_material(merged, material)
    add(scene, name, merged)


def image_for_profile(face: str, profile: str) -> Image.Image:
    image = Image.open(VIEWS / f"{face}.png").convert("RGB")
    if face == "front":
        # The source-locked front includes the latch ears. They are separate
        # geometry in the GLB, so retain only the 434 mm chassis-body segment.
        crop = round(image.width * EAR_EXT / RACK_W)
        image = image.crop((crop, 0, image.width - crop, image.height))
    if profile == "web":
        targets = {
            "front": (2048, 202),
            "rear": (2048, 202),
            "left": (2048, 117),
            "right": (2048, 117),
            "top": (1182, 2048),
            "bottom": (1182, 2048),
        }
        image = image.resize(targets[face], Image.Resampling.LANCZOS)
    return image


def texture_material(face: str, image: Image.Image) -> PBRMaterial:
    mode = "GENERIC_BOTTOM_FALLBACK" if face == "bottom" else "SOURCE_LOCKED_IMAGEGEN"
    return PBRMaterial(
        name=f"FACE_{face.upper()}_{mode}_PHOTOGRAPHIC",
        baseColorFactor=[255, 255, 255, 255],
        baseColorTexture=image,
        metallicFactor=0.0,
        roughnessFactor=0.92,
        alphaMode="OPAQUE",
        doubleSided=False,
    )


def textured_quad(face: str, image: Image.Image) -> trimesh.Trimesh:
    x0, x1 = -BODY_W / 2.0, BODY_W / 2.0
    y0, y1 = -BODY_H / 2.0, BODY_H / 2.0
    z0, z1 = -BODY_D / 2.0, BODY_D / 2.0
    eps = 0.00004
    if face == "front":
        z = FRONT_MOST_Z - 0.0012
        vertices = [[x0, y0, z], [x1, y0, z], [x1, y1, z], [x0, y1, z]]
    elif face == "rear":
        z = REAR_BODY_Z - 0.00005
        vertices = [[x1, y0, z], [x0, y0, z], [x0, y1, z], [x1, y1, z]]
    elif face == "left":
        vertices = [[x0 - eps, y0, z0], [x0 - eps, y0, z1],
                    [x0 - eps, y1, z1], [x0 - eps, y1, z0]]
    elif face == "right":
        vertices = [[x1 + eps, y0, z1], [x1 + eps, y0, z0],
                    [x1 + eps, y1, z0], [x1 + eps, y1, z1]]
    elif face == "top":
        skin_y = y1 - 0.00055
        vertices = [[x0, skin_y, z1], [x1, skin_y, z1], [x1, skin_y, z0], [x0, skin_y, z0]]
    elif face == "bottom":
        skin_y = y0 + 0.00055
        vertices = [[x1, skin_y, z1], [x0, skin_y, z1], [x0, skin_y, z0], [x1, skin_y, z0]]
    else:
        raise ValueError(face)
    mesh = trimesh.Trimesh(
        vertices=np.asarray(vertices, dtype=float),
        faces=np.asarray([[0, 1, 2], [0, 2, 3]], dtype=np.int64),
        process=False,
    )
    mesh.visual = TextureVisuals(
        uv=np.asarray([[0, 0], [1, 0], [1, 1], [0, 1]], dtype=np.float32),
        material=texture_material(face, image),
    )
    return mesh


def add_frame(scene, prefix, cx, cy, width, height, depth, z, rail, material):
    add(scene, f"{prefix}_Top", make_box([width, rail, depth],
        [cx, cy + (height - rail) / 2.0, z], material))
    add(scene, f"{prefix}_Bottom", make_box([width, rail, depth],
        [cx, cy - (height - rail) / 2.0, z], material))
    add(scene, f"{prefix}_Left", make_box([rail, height - 2 * rail, depth],
        [cx - (width - rail) / 2.0, cy, z], material))
    add(scene, f"{prefix}_Right", make_box([rail, height - 2 * rail, depth],
        [cx + (width - rail) / 2.0, cy, z], material))


def add_front(scene: trimesh.Scene, sections: int) -> None:
    # Front-only rack latch assemblies.  Non-overlapping horizontal bands form
    # a solid latch around one real through-hole per ear.  The old solid body,
    # recess frame and coplanar fasteners occupied the same front plane.
    for sign, side in ((-1, "Physical_Left"), (1, "Physical_Right")):
        x_min = -RACK_W / 2.0 if sign < 0 else BODY_W / 2.0
        x_max = -BODY_W / 2.0 if sign < 0 else RACK_W / 2.0
        hole_x = (x_min + x_max) / 2.0
        radius, bands = 0.0037, 48
        band_h = BODY_H / bands
        for band in range(bands):
            y = -BODY_H / 2.0 + band_h * (band + 0.5)
            delta = abs(y)
            half = math.sqrt(radius * radius - delta * delta) if delta < radius else 0.0
            if half == 0:
                add(scene, f"Front_Rack_Latch_{side}_Band_{band + 1}",
                    make_box([x_max - x_min, band_h, FRONT_PROJECTION - 0.0005],
                             [hole_x, y, (RACK_FLANGE_Z + FRONT_MOST_Z - 0.0005) / 2.0], MAT_BLACK))
            else:
                left_w = hole_x - half - x_min
                right_w = x_max - (hole_x + half)
                if left_w > 0:
                    add(scene, f"Front_Rack_Latch_{side}_Hole_Left_{band + 1}",
                        make_box([left_w, band_h, FRONT_PROJECTION - 0.0005],
                                 [x_min + left_w / 2.0, y, (RACK_FLANGE_Z + FRONT_MOST_Z - 0.0005) / 2.0], MAT_BLACK))
                if right_w > 0:
                    add(scene, f"Front_Rack_Latch_{side}_Hole_Right_{band + 1}",
                        make_box([right_w, band_h, FRONT_PROJECTION - 0.0005],
                                 [hole_x + half + right_w / 2.0, y, (RACK_FLANGE_Z + FRONT_MOST_Z - 0.0005) / 2.0], MAT_BLACK))
        # One shallow raised latch bar establishes the official front envelope
        # without overlapping the band caps.
        add(scene, f"Front_Rack_Latch_{side}_Raised_Release",
            make_box([EAR_EXT * 0.42, BODY_H * 0.42, 0.0005],
                     [hole_x, -0.009, FRONT_MOST_Z - 0.00025], MAT_DARK_SILVER))

    # Narrow ten-drive control strip; text stays visible on the photo skin.
    control_x = -0.1980
    add_frame(scene, "Front_10Drive_Control_Strip_Frame", control_x, 0,
              0.0180, 0.0390, 0.0012, FRONT_MOST_Z - 0.0008,
              0.0012, MAT_BLACK)
    # Flush diagnostic lenses, power control, mini-USB and factory marks stay
    # in the locked photograph; duplicate colored caps formerly fought it.

    # Ten independent carrier/bay assemblies, two rows by five columns.
    x_centers = (-0.1540, -0.0780, -0.0020, 0.0740, 0.1500)
    y_centers = (0.0105, -0.0105)
    for col, cx in enumerate(x_centers):
        for row, cy in enumerate(y_centers):
            drive = col * 2 + row
            prefix = f"Front_SFF_Drive_{drive:02d}"
            add_frame(scene, f"{prefix}_Carrier_Perimeter", cx, cy,
                      0.0690, 0.0180, 0.0008, FRONT_MOST_Z - 0.0008,
                      0.0011, MAT_BLACK)
            # Raised handle frame leaves the photographic carrier face visible.
            add_frame(scene, f"{prefix}_Handle", cx + 0.0060, cy,
                      0.0500, 0.0120, 0.0006, FRONT_MOST_Z - 0.0003,
                      0.0017, MAT_BLACK)
            # Exact apertures, release ring and status lenses remain photo
            # detail inside the real raised handle perimeter.


def add_perforated_blank(scene, name, cx, cy, width, height, sections):
    z = REAR_BODY_Z - 0.00045
    add_frame(scene, name, cx, cy, width, height, 0.0007, z,
              0.0011, MAT_SILVER)
    # The verified perforation pattern remains in the rear photograph visible
    # through the open frame, avoiding a coarse repeated overlay.


def add_port_frame(scene, name, cx, cy, width, height, material=MAT_SILVER):
    add_frame(scene, name, cx, cy, width, height, 0.0007,
              REAR_BODY_Z - 0.00045, 0.0010, material)


def add_rear_fan(scene, name, cx, cy, radius, sections):
    z = REAR_MOST_Z + 0.00030
    add(scene, f"{name}_Cavity",
        make_cylinder(radius, 0.0006, [cx, cy, z], MAT_DARK,
                      sections, (0, 0, 1)))
    blades = []
    for angle in np.linspace(0, 2 * math.pi, 7, endpoint=False):
        blade = make_box([radius * 1.05, radius * 0.17, 0.00030],
                         [cx, cy, REAR_MOST_Z + 0.00016], MAT_BLACK)
        blade.apply_transform(trimesh.transformations.rotation_matrix(
            angle, [0, 0, 1], [cx, cy, REAR_MOST_Z + 0.00022]))
        blades.append(blade)
    add_group(scene, f"{name}_Seven_Blades", blades, MAT_BLACK)
    add(scene, f"{name}_Hub",
        make_cylinder(radius * 0.28, 0.00040,
                      [cx, cy, REAR_MOST_Z + 0.00020],
                      MAT_DARK_SILVER, sections, (0, 0, 1)))


def rear_photo_region_quad(name: str, image: Image.Image, cx: float, cy: float,
                           width: float, height: float, z: float) -> trimesh.Trimesh:
    """Crop an exact rear-photo region onto one protruding PSU outer face."""
    iw, ih = image.size
    screen_x = (BODY_W / 2.0 - cx) / BODY_W * iw
    screen_y = (BODY_H / 2.0 - cy) / BODY_H * ih
    crop_w = width / BODY_W * iw
    crop_h = height / BODY_H * ih
    crop = image.crop((max(0, round(screen_x - crop_w / 2.0)),
                       max(0, round(screen_y - crop_h / 2.0)),
                       min(iw, round(screen_x + crop_w / 2.0)),
                       min(ih, round(screen_y + crop_h / 2.0))))
    if crop.width < 1024:
        crop = crop.resize((1024, max(1, round(crop.height * 1024 / crop.width))),
                           Image.Resampling.LANCZOS)
    material = PBRMaterial(
        name=f"FACE_REAR_{name}_SOURCE_LOCKED_PHOTOGRAPHIC",
        baseColorFactor=[255, 255, 255, 255], baseColorTexture=crop,
        metallicFactor=0.0, roughnessFactor=0.92,
        alphaMode="OPAQUE", doubleSided=False)
    x0, x1 = cx - width / 2.0, cx + width / 2.0
    y0, y1 = cy - height / 2.0, cy + height / 2.0
    mesh = trimesh.Trimesh(
        vertices=np.asarray([[x1, y0, z], [x0, y0, z],
                             [x0, y1, z], [x1, y1, z]], dtype=float),
        faces=np.asarray([[0, 1, 2], [0, 2, 3]], dtype=np.int64), process=False)
    mesh.visual = TextureVisuals(
        uv=np.asarray([[0, 0], [1, 0], [1, 1], [0, 1]], dtype=np.float32),
        material=material)
    return mesh


def add_rear(scene: trimesh.Scene, sections: int, rear_image: Image.Image) -> None:
    # Rear screen-left is world +X; screen-right PSU block is world -X.
    for idx, cx in enumerate((0.161, 0.075, -0.011), start=1):
        add_perforated_blank(scene, f"Rear_LowProfile_PCIe_Blank_{idx}",
                             cx, 0.0105, 0.0780, 0.0165, sections)

    # Lower I/O: system ID, iDRAC, serial, VGA, two USB, quad Base-T.
    for idx, (cx, cy) in enumerate(((0.205, -0.006), (0.196, -0.006)), start=1):
        add(scene, f"Rear_SystemID_Round_{idx}",
            make_cylinder(0.0022, 0.0006,
                          [cx, cy, REAR_BODY_Z - 0.0007],
                          MAT_DARK if idx == 1 else MAT_GREEN,
                          16, (0, 0, 1)))
    add_port_frame(scene, "Rear_iDRAC7_Enterprise_RJ45", 0.173, -0.0085, 0.016, 0.013)
    add_port_frame(scene, "Rear_DB9_Serial", 0.139, -0.0085, 0.025, 0.013, MAT_TEAL)
    add_port_frame(scene, "Rear_DB15_VGA", 0.099, -0.0085, 0.026, 0.013, MAT_BLUE)
    add_port_frame(scene, "Rear_USB2_Upper", 0.068, -0.0040, 0.013, 0.006)
    add_port_frame(scene, "Rear_USB2_Lower", 0.068, -0.0130, 0.013, 0.006)
    for idx, cx in enumerate((0.041, 0.013, -0.015, -0.043), start=1):
        add_port_frame(scene, f"Rear_QuadBaseT_RJ45_{idx}", cx, -0.0090, 0.021, 0.014)
        # Connector pins and cavities remain exact photographic detail.

    # Two complete 750W AC hot-plug PSUs.
    for idx, cx in enumerate((-0.1245, -0.1855), start=1):
        psu_w, psu_h = 0.0590, 0.0405
        add_frame(scene, f"Rear_750W_AC_PSU_{idx}_Frame", cx, 0,
                  psu_w, psu_h, REAR_PROJECTION,
                  (REAR_BODY_Z + REAR_MOST_Z) / 2.0,
                  0.0012, MAT_DARK_SILVER)
        add(scene, f"Rear_750W_AC_PSU_{idx}_SourceLocked_OuterFace",
            rear_photo_region_quad(f"PSU_{idx}", rear_image, cx, 0,
                                   psu_w - 0.0024, psu_h - 0.0024,
                                   REAR_MOST_Z + 0.00045))
        inlet_x = cx + 0.0155
        fan_x = cx - 0.0145
        add_frame(scene, f"Rear_750W_AC_PSU_{idx}_IEC_C14",
                  inlet_x, -0.002, 0.0175, 0.0230, 0.0005,
                  REAR_MOST_Z + 0.00025, 0.0010, MAT_BLACK)
        # Fan, guarded hub, orange release and screws remain exact detail in
        # the source-locked PSU crop, avoiding several stacked coplanar disks.
        # U-shaped translucent handle approximation, kept within depth bounds.
        hz = REAR_MOST_Z + 0.00025
        hx = cx + 0.0005
        add(scene, f"Rear_750W_AC_PSU_{idx}_Handle_Top",
            make_box([0.0032, 0.0150, 0.0004], [hx, 0.0100, hz], MAT_CLEAR_GRAY))
        add(scene, f"Rear_750W_AC_PSU_{idx}_Handle_Bottom",
            make_box([0.0032, 0.0150, 0.0004], [hx, -0.0100, hz], MAT_CLEAR_GRAY))
        add(scene, f"Rear_750W_AC_PSU_{idx}_Handle_Bridge",
            make_box([0.0032, 0.0050, 0.0004], [hx, 0, hz], MAT_CLEAR_GRAY))


def add_sides(scene: trimesh.Scene, sections: int) -> None:
    patterns = {
        "Left": {
            "x": -BODY_W / 2.0, "axis": (-1, 0, 0),
            "pins": [(0.004, 0.285), (-0.004, 0.162),
                     (0.003, -0.014), (-0.004, -0.207), (0.004, -0.322)],
            "slots": [(0.013, 0.306), (0.012, 0.096),
                      (0.012, -0.118), (0.012, -0.296)],
        },
        "Right": {
            "x": BODY_W / 2.0, "axis": (1, 0, 0),
            "pins": [(0.002, 0.303), (-0.003, 0.190),
                     (0.004, 0.018), (-0.002, -0.178), (0.003, -0.320)],
            "slots": [(0.013, 0.284), (0.012, 0.075),
                      (0.012, -0.135), (0.012, -0.307)],
        },
    }
    for side, data in patterns.items():
        sign = -1 if side == "Left" else 1
        for idx, (y, z) in enumerate(data["pins"], start=1):
            add(scene, f"Side_{side}_Rail_Mount_Stud_{idx}",
                make_cylinder(0.0022, 0.0012,
                    [data["x"] + sign * 0.0008, y, z], MAT_SILVER,
                    sections, data["axis"]))
        for idx, (y, z) in enumerate(data["slots"], start=1):
            add(scene, f"Side_{side}_Independent_Rail_Slot_{idx}",
                make_box([0.00065, 0.0045, 0.0100],
                    [data["x"] + sign * 0.00045, y, z], MAT_DARK))
        # Long seams and stamped strips stay in the locked side photographs;
        # omitting redundant crossing boxes removes the side z-fighting cause.


def add_top(scene: trimesh.Scene, sections: int) -> None:
    y = BODY_H / 2.0 - 0.0002
    # Recessed latch relief, flush within the official height envelope.
    # The exact recessed rim remains in the locked top photograph; only its
    # raised handle needs parallax geometry.  The former full recess plate was
    # coplanar with the handle.
    add(scene, "Top_Cover_Latch_Handle",
        make_box([0.012, 0.0004, 0.038], [0.055, y, 0.085], MAT_BLACK))
    add(scene, "Top_Cover_Front_Perimeter_Seam",
        make_box([BODY_W - 0.004, 0.0004, 0.0012], [0, y, 0.345], MAT_DARK_SILVER))
    add(scene, "Top_Cover_Rear_Perimeter_Seam",
        make_box([BODY_W - 0.004, 0.0004, 0.0012], [0, y, -0.360], MAT_DARK_SILVER))

    # Faithful relief for dense vent fields; source-locked texture supplies
    # the exact photographic hole edges while these shallow recesses add depth.
    front_holes = []
    for row in range(3):
        for col in range(40):
            front_holes.append(make_cylinder(0.00115, 0.0004,
                [-0.205 + col * 0.0105, y, 0.350 + row * 0.0060],
                MAT_DARK, 10, (0, 1, 0)))
    add_group(scene, "Top_Front_Vent_Relief_3x40", front_holes, MAT_DARK)
    rear_holes = []
    for row in range(3):
        for col in range(28):
            x = -0.105 + col * 0.0072
            if 8 <= col <= 12 and row == 1:
                continue
            rear_holes.append(make_cylinder(0.0011, 0.0004,
                [x, y, -0.350 + row * 0.0060],
                MAT_DARK, 10, (0, 1, 0)))
    add_group(scene, "Top_Rear_Asymmetric_Vent_Relief", rear_holes, MAT_DARK)


def build_scene(profile: str) -> trimesh.Scene:
    textures = {face: image_for_profile(face, profile)
                for face in ("front", "rear", "left", "right", "top", "bottom")}
    sections = 28 if profile == "standard" else 18
    scene = trimesh.Scene(base_frame="Dell-R620-2.5inch_ROOT")
    scene.metadata.update({
        "manufacturer": "Dell",
        "product_id": "PowerEdge R620",
        "variant": "10x2.5-inch SFF / 1U / no bezel",
        "configuration": "10 installed SFF carriers; 3 LP PCIe blanks; iDRAC7; DB9; VGA; 2 USB2; quad 1GbE RJ45 RNDC; 2x750W AC PSU",
        "coordinate_convention": "+X device right from front; +Y up; +Z front",
        "units": "metres",
        "source_model_used": False,
        "bottom_mode": "GENERIC_BOTTOM_FALLBACK",
        "profile": profile,
    })
    add(scene, "Closed_Chassis_Core",
        make_box([BODY_W - 0.0020, BODY_H - 0.0020, BODY_D - 0.0040],
                 [0, 0, 0], MAT_BODY))
    for face in ("front", "rear", "left", "right", "top", "bottom"):
        add(scene, f"Face_{face.title()}_Approved_Imagegen",
            textured_quad(face, textures[face]))
    add_front(scene, sections)
    add_rear(scene, sections, textures["rear"])
    add_sides(scene, sections)
    add_top(scene, sections)
    return scene


def add_unlit_and_metadata(path: Path, profile: str) -> None:
    gltf = GLTF2().load_binary(str(path))
    extensions = list(gltf.extensionsUsed or [])
    if "KHR_materials_unlit" not in extensions:
        extensions.append("KHR_materials_unlit")
    gltf.extensionsUsed = extensions
    for material in gltf.materials or []:
        if material.name and material.name.startswith("FACE_"):
            material.extensions = dict(material.extensions or {})
            material.extensions["KHR_materials_unlit"] = {}
        material.alphaMode = "OPAQUE"
        material.doubleSided = False
    gltf.asset.generator = "Trimesh new exact-exterior construction + pygltflib source-lock metadata pass"
    gltf.asset.extras = {
        "manufacturer": "Dell",
        "product_id": "PowerEdge R620",
        "variant": "10x2.5-inch SFF no bezel",
        "profile": profile,
        "body_dimensions_mm": [434.0, 42.8, 751.4],
        "installed_bounds_mm": [482.4, 42.8, 772.5],
        "coordinate_convention": "+X device right from front; +Y up; +Z front",
        "source_model_used": False,
        "bottom_mode": "GENERIC_BOTTOM_FALLBACK",
        "visible_counts": {
            "SFF_carriers": 10,
            "front_rack_latches": 2,
            "PCIe_low_profile_blanks": 3,
            "iDRAC7_RJ45": 1,
            "DB9_serial": 1,
            "rear_VGA": 1,
            "rear_USB2": 2,
            "network_adapter_RJ45": 4,
            "network_adapter_SFP": 0,
            "AC_PSU_750W": 2,
            "DC_PSU": 0,
            "IEC_AC_inlets": 2,
            "PSU_visible_fans": 2,
            "rear_rack_ears": 0,
        },
    }
    gltf.save_binary(str(path))


def export_profile(profile: str) -> Path:
    MODEL.mkdir(parents=True, exist_ok=True)
    scene = build_scene(profile)
    filename = "Dell-R620-2.5inch.glb" if profile == "standard" else "Dell-R620-2.5inch-web.glb"
    output = MODEL / filename
    output.write_bytes(scene.export(file_type="glb", include_normals=True))
    add_unlit_and_metadata(output, profile)
    return output


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--profile", choices=("standard", "web", "both"), default="both")
    args = parser.parse_args()
    profiles = ("standard", "web") if args.profile == "both" else (args.profile,)
    results = []
    for profile in profiles:
        output = export_profile(profile)
        results.append({"profile": profile, "path": str(output), "bytes": output.stat().st_size})
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
