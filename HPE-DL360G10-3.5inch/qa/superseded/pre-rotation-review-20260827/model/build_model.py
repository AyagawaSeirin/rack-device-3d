#!/usr/bin/env python3
"""Build the exact locked HPE ProLiant DL360 Gen10 4LFF exterior GLBs.

This is an independent website asset reconstruction.  It does not ingest or
copy a third-party mesh.  The installed configuration is frozen by the user
row-4 front/rear lock and the HPE Gen10 documentation recorded in source/.

Coordinate convention (metres): +X right when viewed from the front, +Y up,
+Z toward the front.  The official 749.8 mm LFF depth is the complete visible
front-to-rear envelope; front carrier and rear PSU relief stays inside it.
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

BODY_W = 0.4346
BODY_H = 0.0429
OVERALL_D = 0.7498
RACK_W = 0.4826
EAR_EXT = (RACK_W - BODY_W) / 2.0
FRONT_Z = OVERALL_D / 2.0
REAR_Z = -OVERALL_D / 2.0
SHELL_FRONT_Z = FRONT_Z - 0.0080
SHELL_REAR_Z = REAR_Z + 0.0150
SHELL_D = SHELL_FRONT_Z - SHELL_REAR_Z
SHELL_CZ = (SHELL_FRONT_Z + SHELL_REAR_Z) / 2.0


def pbr(name: str, rgba, metallic: float = 0.0, roughness: float = 0.78) -> PBRMaterial:
    return PBRMaterial(
        name=name,
        baseColorFactor=list(rgba),
        metallicFactor=metallic,
        roughnessFactor=roughness,
        alphaMode="OPAQUE",
        doubleSided=False,
    )


MAT_BODY = pbr("HPE Gen10 galvanized chassis steel", (181, 186, 185, 255), 0.50, 0.55)
MAT_SILVER = pbr("HPE plated carrier and connector steel", (168, 173, 172, 255), 0.58, 0.43)
MAT_DARK_SILVER = pbr("HPE dark stamped steel", (89, 94, 94, 255), 0.40, 0.61)
MAT_BLACK = pbr("HPE black polymer and connector cavities", (11, 13, 14, 255), 0.0, 0.88)
MAT_VENT = pbr("Opaque dark vent recess", (22, 25, 26, 255), 0.0, 0.95)
MAT_MAGENTA = pbr("HPE Smart Carrier release magenta", (142, 20, 68, 255), 0.0, 0.55)
MAT_GREEN = pbr("HPE status and carrier lens green", (15, 202, 72, 255), 0.0, 0.30)
MAT_BLUE = pbr("HPE USB3 and VGA blue", (16, 109, 186, 255), 0.0, 0.42)
MAT_TEAL = pbr("HPE Flex Slot 500W 94 percent badge", (29, 156, 174, 255), 0.0, 0.52)
MAT_GOLD = pbr("Connector pin gold", (191, 146, 52, 255), 0.60, 0.34)
MAT_LABEL = pbr("HPE factory label neutral", (222, 224, 221, 255), 0.0, 0.82)
MAT_DARK_LABEL = pbr("HPE factory identification label", (20, 22, 22, 255), 0.0, 0.82)


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
    mesh.apply_transform(trimesh.geometry.align_vectors([0.0, 0.0, 1.0], axis))
    mesh.apply_translation(np.asarray(center, dtype=float))
    return set_material(mesh, material)


def cylinder_between(a, b, radius, material, sections=24):
    a = np.asarray(a, dtype=float)
    b = np.asarray(b, dtype=float)
    return make_cylinder(radius, np.linalg.norm(b - a), (a + b) / 2.0,
                         material, sections, b - a)


def add(scene: trimesh.Scene, name: str, mesh: trimesh.Trimesh) -> None:
    mesh.metadata["name"] = name
    scene.add_geometry(mesh, node_name=name, geom_name=name)


def add_group(scene: trimesh.Scene, name: str, meshes, material: PBRMaterial) -> None:
    if not meshes:
        return
    merged = trimesh.util.concatenate(meshes)
    set_material(merged, material)
    add(scene, name, merged)


def composite_opaque(image: Image.Image, background) -> Image.Image:
    """Retain photographic RGB while making every mapped chassis texel opaque."""
    rgba = image.convert("RGBA")
    base = Image.new("RGBA", rgba.size, background + (255,))
    base.alpha_composite(rgba)
    return base.convert("RGB")


def profile_texture(face: str, profile: str) -> Image.Image:
    source = Image.open(VIEWS / f"{face}.png")
    # Top/bottom generations include evidence-constrained ear/protrusion pixels
    # outside the rectangular sheet metal.  The ear volumes are modeled
    # separately, so map only the verified chassis plate to the body quad.
    if face == "top":
        source = source.crop((184, 128, 2230, 4003))
    elif face == "bottom":
        source = source.crop((113, 20, 2267, 3940))
    background = (24, 26, 27) if face == "front" else (210, 213, 211)
    image = composite_opaque(source, background)
    if profile == "web":
        targets = {
            "front": (2048, 182),
            "rear": (2048, 202),
            "left": (2048, 117),
            "right": (2048, 117),
            "top": (1195, 2048),
            "bottom": (1187, 2048),
        }
        image = image.resize(targets[face], Image.Resampling.LANCZOS)
    return image


def texture_material(face: str, image: Image.Image) -> PBRMaterial:
    mode = "GENERIC_BOTTOM_FALLBACK" if face == "bottom" else "SOURCE_LOCKED"
    return PBRMaterial(
        name=f"FACE_{face.upper()}_{mode}_PHOTOGRAPHIC_OPAQUE",
        baseColorFactor=[255, 255, 255, 255],
        baseColorTexture=image,
        metallicFactor=0.0,
        roughnessFactor=0.90,
        alphaMode="OPAQUE",
        doubleSided=False,
    )


def textured_quad(face: str, image: Image.Image) -> trimesh.Trimesh:
    x0, x1 = -BODY_W / 2.0, BODY_W / 2.0
    y0, y1 = -BODY_H / 2.0, BODY_H / 2.0
    z0, z1 = REAR_Z, FRONT_Z
    if face == "front":
        x0, x1 = -RACK_W / 2.0, RACK_W / 2.0
        vertices = [[x0, y0, z1 + 0.00015], [x1, y0, z1 + 0.00015],
                    [x1, y1, z1 + 0.00015], [x0, y1, z1 + 0.00015]]
    elif face == "rear":
        vertices = [[x1, y0, z0 - 0.00015], [x0, y0, z0 - 0.00015],
                    [x0, y1, z0 - 0.00015], [x1, y1, z0 - 0.00015]]
    elif face == "left":
        vertices = [[x0 - 0.00015, y0, z0], [x0 - 0.00015, y0, z1],
                    [x0 - 0.00015, y1, z1], [x0 - 0.00015, y1, z0]]
    elif face == "right":
        vertices = [[x1 + 0.00015, y0, z1], [x1 + 0.00015, y0, z0],
                    [x1 + 0.00015, y1, z0], [x1 + 0.00015, y1, z1]]
    elif face == "top":
        vertices = [[x0, y1 + 0.00015, z1], [x1, y1 + 0.00015, z1],
                    [x1, y1 + 0.00015, z0], [x0, y1 + 0.00015, z0]]
    elif face == "bottom":
        vertices = [[x1, y0 - 0.00015, z1], [x0, y0 - 0.00015, z1],
                    [x0, y0 - 0.00015, z0], [x1, y0 - 0.00015, z0]]
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


def add_front(scene: trimesh.Scene, sections: int) -> None:
    # Front-only ears: no rear ear inference is allowed for this lock.
    for sign, side in ((-1, "Left"), (1, "Right")):
        x = sign * (BODY_W / 2.0 + EAR_EXT / 2.0)
        add(scene, f"Front_Ear_{side}_Independent",
            make_box([EAR_EXT, BODY_H, 0.006], [x, 0, FRONT_Z - 0.003], MAT_BLACK))
        for index, y in enumerate((-0.013, 0.013), start=1):
            add(scene, f"Front_Ear_{side}_Fastener_Recess_{index}",
                make_cylinder(0.0022, 0.0012, [x, y, FRONT_Z - 0.0005],
                              MAT_VENT, 16, (0, 0, 1)))
    # HPE badge and exact ProLiant DL360 Gen10 identity remain legible in the
    # locked front texture; these shallow plates preserve physical relief.
    add(scene, "Front_Left_Drive_Bay_ID_Tab",
        make_box([0.019, 0.032, 0.003], [-0.207, -0.001, FRONT_Z - 0.0015], MAT_BLACK))
    add(scene, "Front_Right_HPE_ProLiant_ID_Plate",
        make_box([0.021, 0.032, 0.003], [0.207, -0.001, FRONT_Z - 0.0015], MAT_BLACK))

    # Single row of exactly four independent 3.5-inch HPE Smart Carriers.
    bay_centers = (-0.155, -0.052, 0.052, 0.155)
    for index, x in enumerate(bay_centers, start=1):
        add(scene, f"Front_LFF_Bay_{index}_Recess",
            make_box([0.098, 0.027, 0.003], [x, -0.005, FRONT_Z - 0.0065], MAT_VENT))
        add(scene, f"Front_LFF_Carrier_{index}_Body",
            make_box([0.095, 0.025, 0.006], [x, -0.005, FRONT_Z - 0.0030], MAT_BLACK))
        add(scene, f"Front_LFF_Carrier_{index}_Pull_Handle",
            make_box([0.070, 0.0055, 0.0045],
                     [x - 0.006, -0.012, FRONT_Z - 0.0023], MAT_DARK_SILVER))
        add(scene, f"Front_LFF_Carrier_{index}_Magenta_Release",
            make_box([0.012, 0.020, 0.0048],
                     [x + 0.039, -0.004, FRONT_Z - 0.0024], MAT_MAGENTA))
        add(scene, f"Front_LFF_Carrier_{index}_Status_Hub",
            make_cylinder(0.0078, 0.0026, [x + 0.017, -0.004, FRONT_Z - 0.0014],
                          MAT_DARK_SILVER, sections, (0, 0, 1)))
        add(scene, f"Front_LFF_Carrier_{index}_Green_Lens",
            make_cylinder(0.0017, 0.0008, [x + 0.017, -0.004, FRONT_Z - 0.0002],
                          MAT_GREEN, sections, (0, 0, 1)))
        add(scene, f"Front_LFF_Carrier_{index}_Label_Plate",
            make_box([0.019, 0.018, 0.0012],
                     [x - 0.035, -0.003, FRONT_Z - 0.0007], MAT_DARK_LABEL))
        vents = []
        for col in range(8):
            for row in range(2):
                vents.append(make_box([0.0076, 0.0021, 0.0011],
                                      [x - 0.030 + col * 0.0086,
                                       0.014 + row * 0.0040, FRONT_Z - 0.0006], MAT_VENT))
        add_group(scene, f"Front_LFF_Bay_{index}_Upper_Intake_16", vents, MAT_VENT)

    # Exact 4LFF upper control/media strip from the frozen front.
    add(scene, "Front_Optical_Drive_Blank",
        make_box([0.050, 0.006, 0.0024], [-0.042, 0.014, FRONT_Z - 0.0012], MAT_BLACK))
    add(scene, "Front_VGA_Optional_Blank",
        make_box([0.020, 0.009, 0.0023], [0.069, 0.014, FRONT_Z - 0.0011], MAT_BLACK))
    add(scene, "Front_iLO_Service_USB",
        make_box([0.013, 0.008, 0.0025], [0.103, 0.014, FRONT_Z - 0.0010], MAT_BLACK))
    add(scene, "Front_USB3_Blue",
        make_box([0.014, 0.006, 0.0025], [0.129, 0.014, FRONT_Z - 0.0010], MAT_BLUE))
    for idx, (x, mat) in enumerate(((0.158, MAT_BLUE), (0.172, MAT_GREEN),
                                    (0.184, MAT_GREEN), (0.196, MAT_GREEN)), start=1):
        add(scene, f"Front_Status_Lens_{idx}",
            make_cylinder(0.0010, 0.0008, [x, 0.014, FRONT_Z - 0.0002],
                          mat, 16, (0, 0, 1)))


def add_rear_fan(scene: trimesh.Scene, name: str, cx: float, cy: float,
                 z: float, radius: float, sections: int) -> None:
    # The approved rear photograph already carries the exact fan blades and
    # 500W/94% print.  Keep the relief immediately behind the opaque source
    # texture so it cannot become a synthetic solid disk that hides those
    # identity-bearing pixels; the separate PSU body and handle remain proud.
    add(scene, f"{name}_Dark_Cavity",
        make_cylinder(radius, 0.0010, [cx, cy, REAR_Z + 0.0015],
                      MAT_VENT, sections, (0, 0, 1)))
    add(scene, f"{name}_Hub",
        make_cylinder(radius * 0.34, 0.0010, [cx, cy, REAR_Z + 0.0014], MAT_LABEL,
                      sections, (0, 0, 1)))
    blades = []
    for angle in np.linspace(0, 2 * math.pi, 7, endpoint=False):
        blade = make_box([radius * 0.92, radius * 0.16, 0.0012],
                         [cx, cy, REAR_Z + 0.0014], MAT_BLACK)
        blade.apply_transform(trimesh.transformations.rotation_matrix(
            angle, [0, 0, 1], [cx, cy, z]))
        blades.append(blade)
    add_group(scene, f"{name}_Seven_Blades", blades, MAT_BLACK)


def add_rj45(scene, name, x, y, zface):
    add(scene, name, make_box([0.0160, 0.0130, 0.0045], [x, y, zface], MAT_BLACK))
    add(scene, f"{name}_Cage_Top",
        make_box([0.0168, 0.0012, 0.0048], [x, y + 0.0070, zface], MAT_SILVER))


def add_rear(scene: trimesh.Scene, sections: int) -> None:
    # Rear photograph is observed from behind: viewer-right is -X in the
    # front-oriented coordinate convention.  All rear X positions below are
    # therefore intentionally the world-space inverse of their image position.
    zface = REAR_Z + 0.0030
    # Gen10 1U upper arrangement: two full-height primary slot blanks and the
    # separately retained optional third slot/secondary-riser blank.  No rear drive.
    slot_specs = [(0.150, 0.009, 0.103, 0.021), (0.055, 0.009, 0.073, 0.021),
                  (-0.046, 0.009, 0.092, 0.017)]
    for index, (x, y, w, h) in enumerate(slot_specs, start=1):
        add(scene, f"Rear_PCIe_Slot_{index}_Blank",
            make_box([w, h, 0.0032], [x, y, zface], MAT_SILVER))
        vents = []
        cols = max(4, int(w / 0.009))
        rows = 2 if h > 0.019 else 1
        for col in range(cols):
            for row in range(rows):
                vents.append(make_box([0.0062, 0.0030, 0.0010],
                                      [x - w / 2 + 0.006 + col * (w - 0.012) / max(1, cols - 1),
                                       y + (row - (rows - 1) / 2) * 0.006,
                                       REAR_Z + 0.0002], MAT_VENT))
        add_group(scene, f"Rear_PCIe_Slot_{index}_Vent_Recesses", vents, MAT_VENT)

    # Four-port 331FLR FlexibleLOM bank at lower left.
    for index, x in enumerate((0.181, 0.161, 0.141, 0.121), start=1):
        add_rj45(scene, f"Rear_FlexibleLOM_331FLR_RJ45_{index}", x, -0.011, zface)

    # Two vertically stacked blue USB 3.0 ports.
    for index, y in enumerate((-0.014, 0.001), start=1):
        add(scene, f"Rear_USB3_{index}_Blue",
            make_box([0.014, 0.007, 0.0045], [0.094, y, zface], MAT_BLUE))

    # DB9 serial with genuine nine pin reliefs.
    add(scene, "Rear_DB9_Serial_Shell",
        make_box([0.026, 0.015, 0.0045], [0.064, -0.007, zface], MAT_SILVER))
    pins = []
    for row, count in enumerate((5, 4)):
        for col in range(count):
            pins.append(make_cylinder(0.00055, 0.0012,
                                      [0.072 - col * 0.004 - row * 0.002,
                                       -0.010 + row * 0.006, REAR_Z + 0.0001],
                                      MAT_GOLD, 10, (0, 0, 1)))
    add_group(scene, "Rear_DB9_Serial_9_Pins", pins, MAT_GOLD)

    add_rj45(scene, "Rear_Dedicated_iLO5_RJ45", 0.030, -0.011, zface)
    for index, x in enumerate((0.000, -0.020, -0.040, -0.060), start=1):
        add_rj45(scene, f"Rear_Embedded_331i_1GbE_RJ45_{index}", x, -0.011, zface)
    add(scene, "Rear_VGA_DB15_Blue_Shell",
        make_box([0.027, 0.016, 0.0045], [-0.091, -0.007, zface], MAT_BLUE))
    vga_pins = []
    for row in range(3):
        for col in range(5):
            vga_pins.append(make_cylinder(0.00042, 0.0010,
                                          [-0.084 - col * 0.0035 - (row % 2) * 0.0017,
                                           -0.012 + row * 0.005, REAR_Z + 0.0001],
                                          MAT_VENT, 10, (0, 0, 1)))
    add_group(scene, "Rear_VGA_15_Pin_Relief", vga_pins, MAT_VENT)

    # Exact dual HPE 500W Flex Slot Platinum hot-plug AC assembly.
    # Keep both 52 mm Flex Slot modules inside the verified 434.6 mm body.
    for index, cx in enumerate((-0.137, -0.190), start=1):
        add(scene, f"Rear_AC_PSU_{index}_500W_Body",
            make_box([0.052, BODY_H - 0.001, 0.014],
                     [cx, 0, REAR_Z + 0.007], MAT_DARK_SILVER))
        add_rear_fan(scene, f"Rear_AC_PSU_{index}_Fan", cx - 0.011, 0.002,
                     REAR_Z + 0.0006, 0.015, sections)
        add(scene, f"Rear_AC_PSU_{index}_IEC_C14_Inlet",
            make_box([0.015, 0.021, 0.0022],
                     [cx + 0.017, -0.002, REAR_Z + 0.0012], MAT_BLACK))
        add(scene, f"Rear_AC_PSU_{index}_Magenta_Release",
            make_box([0.013, 0.005, 0.0028],
                     [cx + 0.019, 0.015, REAR_Z + 0.0013], MAT_MAGENTA))
        add(scene, f"Rear_AC_PSU_{index}_Green_Status_Lens",
            make_cylinder(0.0032, 0.0010,
                          [cx + 0.004, 0.015, REAR_Z + 0.0011],
                          MAT_GREEN, 16, (0, 0, 1)))
        # Preserve the exact source-locked 500W/94% fan label in the texture;
        # do not cover it with an approximate raised badge disk.
        handle_z = REAR_Z + 0.0003
        add(scene, f"Rear_AC_PSU_{index}_Handle_Bar",
            cylinder_between([cx - 0.025, -0.012, handle_z],
                             [cx + 0.003, -0.012, handle_z], 0.0020, MAT_BLACK, sections))
        for side, x in enumerate((cx - 0.025, cx + 0.003), start=1):
            add(scene, f"Rear_AC_PSU_{index}_Handle_Arm_{side}",
                cylinder_between([x, -0.012, REAR_Z + 0.011],
                                 [x, -0.012, handle_z], 0.0020, MAT_BLACK, sections))


def add_sides(scene: trimesh.Scene, sections: int) -> None:
    # Separate evidence-derived patterns; left is never mirrored from right.
    patterns = {
        "Left": {
            "x": -BODY_W / 2.0, "axis": (-1, 0, 0),
            "pins": [(0.004, 0.230), (0.002, 0.060), (0.004, -0.120), (0.003, -0.300)],
            "slots": [(-0.007, 0.213), (-0.008, -0.135), (-0.006, -0.325)],
        },
        "Right": {
            "x": BODY_W / 2.0, "axis": (1, 0, 0),
            "pins": [(0.007, 0.275), (0.003, 0.090), (0.006, -0.105), (0.004, -0.290)],
            "slots": [(-0.006, 0.245), (-0.009, 0.015), (-0.007, -0.265)],
        },
    }
    for side, data in patterns.items():
        sign = -1 if side == "Left" else 1
        for index, (y, z) in enumerate(data["pins"], start=1):
            add(scene, f"Side_{side}_Rail_Mount_Spool_{index}",
                make_cylinder(0.0042, 0.0030,
                              [data["x"] + sign * 0.0015, y, z], MAT_DARK_SILVER,
                              sections, data["axis"]))
            add(scene, f"Side_{side}_Rail_Mount_Spool_{index}_Hub",
                make_cylinder(0.0022, 0.0035,
                              [data["x"] + sign * 0.0018, y, z], MAT_BLACK,
                              sections, data["axis"]))
        for index, (y, z) in enumerate(data["slots"], start=1):
            add(scene, f"Side_{side}_Key_Slot_Recess_{index}",
                make_box([0.0014, 0.0045, 0.010],
                         [data["x"] + sign * 0.0007, y, z], MAT_VENT))
        add(scene, f"Side_{side}_Upper_Pressed_Seam",
            make_box([0.0010, 0.0012, OVERALL_D - 0.035],
                     [data["x"] + sign * 0.00055, 0.013, 0.0], MAT_DARK_SILVER))
        add(scene, f"Side_{side}_Lower_Fold",
            make_box([0.0012, 0.0020, OVERALL_D - 0.020],
                     [data["x"] + sign * 0.0006, -0.019, 0.0], MAT_SILVER))


def top_slot_group(cx, cz, cols, rows, spacing_x, spacing_z):
    slots = []
    for col in range(cols):
        for row in range(rows):
            slots.append(make_box([0.0056, 0.0009, 0.0024],
                                  [cx + (col - (cols - 1) / 2) * spacing_x,
                                   BODY_H / 2.0 - 0.00110,
                                   cz + (row - (rows - 1) / 2) * spacing_z], MAT_VENT))
    return slots


def add_top_and_internal(scene: trimesh.Scene, sections: int) -> None:
    # Two-piece top cover with the front service-panel transverse seam.
    add(scene, "Top_Transverse_Cover_Seam",
        make_box([BODY_W - 0.003, 0.0010, 0.0015],
                 [0, BODY_H / 2.0 - 0.00100, -0.270], MAT_DARK_SILVER))
    add(scene, "Top_Black_Hood_Release_Latch",
        make_box([0.022, 0.0018, 0.055],
                 [0.000, BODY_H / 2.0 - 0.00180, -0.080], MAT_BLACK))
    vent_groups = [
        ("Top_Rear_Left_Slot_Vent", -0.092, 0.285, 13, 6, 0.0080, 0.0060),
        ("Top_Rear_Right_Slot_Vent", 0.145, 0.285, 9, 6, 0.0080, 0.0060),
        ("Top_Mid_Left_Slot_Vent", -0.110, 0.030, 9, 8, 0.0078, 0.0058),
    ]
    for name, cx, cz, cols, rows, sx, sz in vent_groups:
        add_group(scene, name, top_slot_group(cx, cz, cols, rows, sx, sz), MAT_VENT)
    add(scene, "Top_Factory_ID_Label_Left",
        make_box([0.090, 0.0007, 0.045],
                 [-0.142, BODY_H / 2.0 - 0.00120, -0.318], MAT_DARK_LABEL))
    add(scene, "Top_Factory_ID_Label_Right",
        make_box([0.074, 0.0007, 0.050],
                 [0.142, BODY_H / 2.0 - 0.00120, -0.318], MAT_DARK_LABEL))
    # User Guide/QuickSpecs: 2P uses seven fan modules.  They are distinct,
    # internal meshes and not exposed through a transparent shell.
    for index, x in enumerate(np.linspace(-0.150, 0.150, 7), start=1):
        add(scene, f"Internal_HotPlug_Fan_{index}_Module",
            make_box([0.038, 0.032, 0.038], [x, 0, 0.225], MAT_BLACK))
        add(scene, f"Internal_HotPlug_Fan_{index}_Rotor",
            make_cylinder(0.014, 0.010, [x, 0, 0.225], MAT_DARK_SILVER,
                          sections, (0, 0, 1)))
        add(scene, f"Internal_HotPlug_Fan_{index}_Magenta_Latch",
            make_box([0.012, 0.006, 0.010], [x, 0.014, 0.244], MAT_MAGENTA))


def build_scene(profile: str) -> trimesh.Scene:
    textures = {face: profile_texture(face, profile)
                for face in ("front", "rear", "left", "right", "top", "bottom")}
    sections = 28 if profile == "standard" else 18
    scene = trimesh.Scene(base_frame="HPE-DL360G10-3.5inch_ROOT")
    scene.metadata.update({
        "manufacturer": "Hewlett Packard Enterprise",
        "product_id": "HPE ProLiant DL360 Gen10",
        "orderable_generation_lock": "867958-B21 4LFF CTO generation",
        "variant": "4LFF / 3.5-inch / 1U",
        "configuration": "4 LFF carriers; P408i-a SR Gen10 internal; 3 PCIe positions; 331FLR 4x1GbE; 331i 4x1GbE; DB9; iLO5; 2 USB3; VGA; dual 500W AC Flex Slot PSU; seven-fan 2P arrangement",
        "coordinate_convention": "+X device right from front; +Y up; +Z front",
        "units": "metres",
        "source_model_used": False,
        "bottom_mode": "GENERIC_BOTTOM_FALLBACK",
        "profile": profile,
    })
    add(scene, "Closed_Chassis_Core",
        make_box([BODY_W - 0.003, BODY_H - 0.003, SHELL_D],
                 [0, 0, SHELL_CZ], MAT_BODY))
    for face in ("front", "rear", "left", "right", "top", "bottom"):
        add(scene, f"Face_{face.title()}_Approved_Imagegen",
            textured_quad(face, textures[face]))
    add_front(scene, sections)
    add_rear(scene, sections)
    add_sides(scene, sections)
    add_top_and_internal(scene, sections)
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
    gltf.asset.generator = "Independent Trimesh exact-exterior construction + pygltflib opaque face pass"
    gltf.asset.extras = {
        "manufacturer": "Hewlett Packard Enterprise",
        "product_id": "HPE ProLiant DL360 Gen10",
        "generation_and_variant": "867958-B21 generation; 4LFF 3.5-inch; 1U",
        "profile": profile,
        "official_dimensions_mm": {
            "body_width": 434.6, "height": 42.9, "overall_LFF_depth": 749.8,
            "front_rack_ear_span": 482.6,
        },
        "coordinate_convention": "+X device right from front; +Y up; +Z front",
        "bottom_mode": "GENERIC_BOTTOM_FALLBACK",
        "visible_counts": {
            "LFF_carriers": 4,
            "front_rack_ears": 2,
            "rear_rack_ears": 0,
            "PCIe_positions": 3,
            "FlexibleLOM_331FLR_RJ45": 4,
            "embedded_331i_RJ45": 4,
            "rear_USB3": 2,
            "serial_DB9": 1,
            "dedicated_iLO5": 1,
            "rear_VGA": 1,
            "AC_PSU_500W": 2,
            "PSU_C14_inlets": 2,
            "PSU_visible_fans": 2,
            "internal_hotplug_fans_2P": 7,
            "left_rail_spools": 4,
            "right_rail_spools": 4,
        },
        "configuration_absences": ["rear drive module", "DC PSU", "Gen9 rear", "Gen11 rear", "SFF front/backplane"],
        "source_manifest": "../source/identity-manifest.md",
        "feature_inventory": "../source/feature-inventory.csv",
    }
    gltf.save_binary(str(path))


def export_profile(profile: str) -> Path:
    scene = build_scene(profile)
    filename = "HPE-DL360G10-3.5inch.glb" if profile == "standard" else "HPE-DL360G10-3.5inch-web.glb"
    output = MODEL / filename
    output.parent.mkdir(parents=True, exist_ok=True)
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
