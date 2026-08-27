#!/usr/bin/env python3
"""Build exact-exterior HPE ProLiant DL360 Gen9 4LFF website GLBs.

This is a newly constructed exterior model.  No official or third-party mesh
is copied.  Coordinates are metres in a right-handed glTF frame:
+X device right from the front, +Y up, +Z front.
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
BODY_H = 0.0432
BODY_D = 0.7500
RACK_W = 0.4826
EAR_EXT = (RACK_W - BODY_W) / 2.0
FRONT_Z = BODY_D / 2.0
REAR_Z = -BODY_D / 2.0
FRONT_PROJECTION = 0.008
REAR_PROJECTION = 0.012


def pbr(name: str, rgba, metallic: float = 0.0, roughness: float = 0.78) -> PBRMaterial:
    return PBRMaterial(
        name=name,
        baseColorFactor=list(rgba),
        metallicFactor=metallic,
        roughnessFactor=roughness,
        alphaMode="OPAQUE",
        doubleSided=False,
    )


MAT_BODY = pbr("HPE galvanized chassis steel", (186, 189, 186, 255), 0.48, 0.52)
MAT_SILVER = pbr("HPE plated carrier and connector steel", (177, 180, 176, 255), 0.62, 0.38)
MAT_DARK_SILVER = pbr("HPE dark galvanized relief", (104, 108, 106, 255), 0.38, 0.57)
MAT_BLACK = pbr("HPE black polymer and connector cavities", (13, 15, 16, 255), 0.0, 0.87)
MAT_DARK = pbr("Deep fan and vent cavity", (25, 28, 29, 255), 0.0, 0.92)
MAT_RED = pbr("HPE Smart Carrier and PSU release red", (151, 45, 55, 255), 0.0, 0.58)
MAT_GREEN = pbr("HPE status and carrier lens green", (31, 195, 73, 255), 0.0, 0.30)
MAT_BLUE = pbr("HPE VGA and USB 3 blue", (22, 129, 194, 255), 0.0, 0.42)
MAT_TEAL = pbr("HPE 500W PSU badge teal", (31, 160, 184, 255), 0.0, 0.52)
MAT_GOLD = pbr("Connector pin gold", (191, 146, 52, 255), 0.63, 0.32)
MAT_LABEL = pbr("HPE factory label neutral", (225, 226, 222, 255), 0.0, 0.82)


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


def opaque_texture(image: Image.Image) -> Image.Image:
    """Remove external padding and matte it without black/stretched artifacts.

    The approved canonical views keep a few transparent anti-crop pixels.
    Converting RGBA directly to RGB bakes those transparent pixels as black,
    which creates false bands on the top, bottom, and side cards in oblique
    renders.  Nearest-pixel extension also creates false colored streaks across
    the long transparent margins of top and bottom source silhouettes.  Crop to
    the alpha content bounds, derive a neutral matte from the median of the
    approved fully opaque product pixels, and composite only the formerly
    transparent/antialiased samples over that matte.  Every approved fully
    opaque chassis pixel stays byte-for-byte in RGB and the GLB material remains
    OPAQUE.
    """
    rgba = image.convert("RGBA")
    content_bounds = rgba.getchannel("A").getbbox()
    if content_bounds is None:
        raise ValueError("approved face texture has no opaque content")
    cropped = np.asarray(rgba.crop(content_bounds), dtype=np.uint8)
    alpha = cropped[:, :, 3]
    opaque = alpha >= 250
    if not np.any(opaque):
        raise ValueError("approved face texture has no fully opaque content")

    matte_rgb = np.median(cropped[:, :, :3][opaque], axis=0).astype(np.float32)
    source_rgb = cropped[:, :, :3].astype(np.float32)
    weight = alpha.astype(np.float32)[:, :, None] / 255.0
    rgb = np.rint(source_rgb * weight + matte_rgb[None, None, :] * (1.0 - weight))
    return Image.fromarray(np.clip(rgb, 0, 255).astype(np.uint8))


def profile_texture(face: str, profile: str) -> Image.Image:
    source = Image.open(VIEWS / f"{face}.png")
    # The generated top/bottom canonical canvases include the separately
    # modeled front-ear and rear-handle silhouette.  Feeding that full
    # silhouette to the rectangular body quad leaves broad matte rails along
    # both sides.  Rectify only the verified body rectangle to the published
    # 434.6:750 ratio; the omitted protrusions remain visible as real geometry.
    body_rectification = {
        "top": ((121, 32, 1931, 3411), (2048, 3534)),
        "bottom": ((69, 6, 1979, 3411), (2048, 3534)),
    }
    if face in body_rectification:
        crop_box, canonical_size = body_rectification[face]
        source = source.crop(crop_box).resize(canonical_size, Image.Resampling.LANCZOS)
    image = opaque_texture(source)
    if profile == "web":
        targets = {
            "front": (2048, 184),
            "rear": (2048, 204),
            "left": (2048, 118),
            "right": (2048, 118),
            "top": (1024, 1767),
            "bottom": (1024, 1767),
        }
        image = image.resize(targets[face], Image.Resampling.LANCZOS)
    return image


def texture_material(face: str, image: Image.Image) -> PBRMaterial:
    mode = "GENERIC_BOTTOM_FALLBACK" if face == "bottom" else "SOURCE_LOCKED"
    return PBRMaterial(
        name=f"FACE_{face.upper()}_{mode}_PHOTOGRAPHIC",
        baseColorFactor=[255, 255, 255, 255],
        baseColorTexture=image,
        metallicFactor=0.0,
        roughnessFactor=0.90,
        alphaMode="OPAQUE",
        doubleSided=False,
    )


def textured_quad(face: str, image: Image.Image,
                  material: PBRMaterial | None = None) -> trimesh.Trimesh:
    x0, x1 = -BODY_W / 2.0, BODY_W / 2.0
    y0, y1 = -BODY_H / 2.0, BODY_H / 2.0
    z0, z1 = REAR_Z, FRONT_Z
    if face == "front":
        x0, x1 = -RACK_W / 2.0, RACK_W / 2.0
        vertices = [[x0, y0, z1 + 0.00006], [x1, y0, z1 + 0.00006],
                    [x1, y1, z1 + 0.00006], [x0, y1, z1 + 0.00006]]
    elif face == "rear":
        vertices = [[x1, y0, z0 - 0.00006], [x0, y0, z0 - 0.00006],
                    [x0, y1, z0 - 0.00006], [x1, y1, z0 - 0.00006]]
    elif face == "left":
        vertices = [[x0 - 0.00006, y0, z0], [x0 - 0.00006, y0, z1],
                    [x0 - 0.00006, y1, z1], [x0 - 0.00006, y1, z0]]
    elif face == "right":
        vertices = [[x1 + 0.00006, y0, z1], [x1 + 0.00006, y0, z0],
                    [x1 + 0.00006, y1, z0], [x1 + 0.00006, y1, z1]]
    elif face == "top":
        # Keep the primary photograph 0.12 mm below the verified outer top
        # envelope.  Shallow seam/latch/vent relief occupies that stable depth
        # layer without inflating the official 43.2 mm chassis height.
        vertices = [[x0, y1 - 0.00012, z1], [x1, y1 - 0.00012, z1],
                    [x1, y1 - 0.00012, z0], [x0, y1 - 0.00012, z0]]
    elif face == "bottom":
        vertices = [[x1, y0, z1], [x0, y0, z1],
                    [x0, y0, z0], [x1, y0, z0]]
    else:
        raise ValueError(face)
    mesh = trimesh.Trimesh(
        vertices=np.asarray(vertices, dtype=float),
        faces=np.asarray([[0, 1, 2], [0, 2, 3]], dtype=np.int64),
        process=False,
    )
    mesh.visual = TextureVisuals(
        uv=np.asarray([[0, 0], [1, 0], [1, 1], [0, 1]], dtype=np.float32),
        material=material or texture_material(face, image),
    )
    return mesh


def projected_face_patch(face: str, x0: float, x1: float,
                         y0: float, y1: float, z: float,
                         material: PBRMaterial) -> trimesh.Trimesh:
    """Project the locked face photograph onto a shallow relief surface.

    The patch samples the same physical rectangle as the base face card, so
    parallax never replaces a photographic component with a synthetic block.
    """
    v0 = (y0 + BODY_H / 2.0) / BODY_H
    v1 = (y1 + BODY_H / 2.0) / BODY_H
    if face == "front":
        u0 = (x0 + RACK_W / 2.0) / RACK_W
        u1 = (x1 + RACK_W / 2.0) / RACK_W
        vertices = [[x0, y0, z], [x1, y0, z],
                    [x1, y1, z], [x0, y1, z]]
    elif face == "rear":
        # A rear-facing camera reverses world X. Keep source text readable
        # without negative node scales or mirrored transforms.
        u0 = (BODY_W / 2.0 - x1) / BODY_W
        u1 = (BODY_W / 2.0 - x0) / BODY_W
        vertices = [[x1, y0, z], [x0, y0, z],
                    [x0, y1, z], [x1, y1, z]]
    else:
        raise ValueError(f"projected patch unsupported for {face}")
    mesh = trimesh.Trimesh(
        vertices=np.asarray(vertices, dtype=float),
        faces=np.asarray([[0, 1, 2], [0, 2, 3]], dtype=np.int64),
        process=False,
    )
    mesh.visual = TextureVisuals(
        uv=np.asarray([[u0, v0], [u1, v0], [u1, v1], [u0, v1]],
                      dtype=np.float32),
        material=material,
    )
    return mesh


def add_front(scene: trimesh.Scene, sections: int,
              material: PBRMaterial) -> None:
    # Independent front-only rack ears and cover/attachment relief.
    for sign, side in ((-1, "Left"), (1, "Right")):
        x = sign * (BODY_W / 2.0 + EAR_EXT / 2.0)
        add(scene, f"Front_Ear_{side}_Independent",
            make_box([EAR_EXT, BODY_H, 0.006], [x, 0, FRONT_Z + 0.003], MAT_SILVER))
        add(scene, f"Front_Ear_{side}_SourceLocked_Surface",
            projected_face_patch(
                "front", x - EAR_EXT / 2.0, x + EAR_EXT / 2.0,
                -BODY_H / 2.0, BODY_H / 2.0,
                FRONT_Z + 0.00606, material))

    bay_centers = (-0.159, -0.053, 0.053, 0.159)
    for index, x in enumerate(bay_centers, start=1):
        add(scene, f"Front_LFF_Bay_{index}_Recess",
            make_box([0.101, 0.028, 0.004], [x, -0.0050, FRONT_Z + 0.002], MAT_BLACK))
        add(scene, f"Front_LFF_Carrier_{index}_Body",
            make_box([0.097, 0.025, 0.006], [x, -0.0050, FRONT_Z + 0.005], MAT_DARK))
        add(scene, f"Front_LFF_Carrier_{index}_SourceLocked_Surface",
            projected_face_patch(
                "front", x - 0.097 / 2.0, x + 0.097 / 2.0,
                -0.0175, 0.0075,
                FRONT_Z + FRONT_PROJECTION + 0.00006, material))

def add_rear_fan(scene: trimesh.Scene, name: str, cx: float, cy: float,
                 z: float, radius: float, sections: int) -> None:
    add(scene, f"{name}_Dark_Cavity",
        make_cylinder(radius, 0.0018, [cx, cy, z], MAT_DARK, sections, (0, 0, 1)))
    add(scene, f"{name}_Hub",
        make_cylinder(radius * 0.32, 0.0024, [cx, cy, z - 0.0010], MAT_TEAL,
                      sections, (0, 0, 1)))
    blades = []
    for angle in np.linspace(0, 2 * math.pi, 6, endpoint=False):
        blade = make_box([radius * 0.95, radius * 0.17, 0.0014],
                         [cx, cy, z - 0.0012], MAT_BLACK)
        transform = trimesh.transformations.rotation_matrix(angle, [0, 0, 1], [cx, cy, z])
        blade.apply_transform(transform)
        blades.append(blade)
    add_group(scene, f"{name}_Six_Blades", blades, MAT_BLACK)


def add_rear_legacy(scene: trimesh.Scene, sections: int) -> None:
    zface = REAR_Z - 0.0030
    # Rear reference coordinates are stated as they appear to a viewer facing
    # the back of the server.  That camera reverses world X, so every rear
    # feature must use the opposite world-X sign to register with the locked
    # rear photograph.
    # Screenshot/HPE-render locked PCIe blanking arrangement.
    slot_specs = [(0.151, 0.011, 0.105, 0.011), (0.079, 0.011, 0.055, 0.011),
                  (-0.001, 0.011, 0.096, 0.011)]
    for index, (x, y, w, h) in enumerate(slot_specs, start=1):
        add(scene, f"Rear_PCIe_Slot_{index}_Blank",
            make_box([w, h, 0.004], [x, y, zface], MAT_SILVER))
        vents = []
        for col in range(max(3, int(w / 0.011))):
            vents.append(make_box([0.007, 0.0015, 0.0012],
                                  [x + w / 2 - 0.007 - col * 0.010, y, zface - 0.0023], MAT_DARK))
        add_group(scene, f"Rear_PCIe_Slot_{index}_Perforations", vents, MAT_DARK)

    # Four-port screenshot-matched FlexibleLOM, never the two-port QSFP variant.
    for index, x in enumerate((0.178, 0.160, 0.142, 0.124), start=1):
        add(scene, f"Rear_FlexibleLOM_RJ45_{index}",
            make_box([0.015, 0.013, 0.006], [x, -0.008, zface - 0.001], MAT_BLACK))
        add(scene, f"Rear_FlexibleLOM_RJ45_{index}_Cage",
            make_box([0.0165, 0.0012, 0.0065], [x, -0.001, zface - 0.001], MAT_SILVER))

    for index, y in enumerate((-0.013, 0.002), start=1):
        add(scene, f"Rear_USB3_{index}_Blue",
            make_box([0.015, 0.008, 0.006], [0.100, y, zface - 0.001], MAT_BLUE))

    # DB9 serial shell and nine genuine pin reliefs.
    add(scene, "Rear_DB9_Serial_Shell",
        make_box([0.026, 0.015, 0.005], [0.071, -0.006, zface - 0.001], MAT_SILVER))
    pins = []
    for row, count in enumerate((5, 4)):
        for col in range(count):
            pins.append(make_cylinder(0.00065, 0.0016,
                                      [0.071 + 0.008 - col * 0.004 - row * 0.002,
                                       -0.009 + row * 0.006, zface - 0.004],
                                      MAT_GOLD, 12, (0, 0, 1)))
    add_group(scene, "Rear_DB9_Serial_9_Pins", pins, MAT_GOLD)

    add(scene, "Rear_iLO4_Dedicated_RJ45",
        make_box([0.016, 0.014, 0.006], [0.039, -0.008, zface - 0.001], MAT_BLACK))
    for index, x in enumerate((0.006, -0.014, -0.034, -0.054), start=1):
        add(scene, f"Rear_Embedded_1GbE_RJ45_{index}",
            make_box([0.017, 0.014, 0.006], [x, -0.008, zface - 0.001], MAT_BLACK))
    add(scene, "Rear_VGA_Blue_Shell",
        make_box([0.027, 0.016, 0.005], [-0.084, -0.006, zface - 0.001], MAT_BLUE))
    vga_pins = []
    for row in range(3):
        for col in range(5):
            vga_pins.append(make_cylinder(0.00045, 0.0014,
                                          [-0.077 - col * 0.0035 - (row % 2) * 0.0017,
                                           -0.011 + row * 0.005, zface - 0.004],
                                          MAT_DARK, 10, (0, 0, 1)))
    add_group(scene, "Rear_VGA_15_Pin_Relief", vga_pins, MAT_DARK)

    # Two complete 500W AC Flex Slot PSUs, including visible fans, inlets and handles.
    for index, cx in enumerate((-0.139, -0.194), start=1):
        add(scene, f"Rear_AC_PSU_{index}_Body",
            make_box([0.054, BODY_H - 0.001, REAR_PROJECTION],
                     [cx, 0, REAR_Z - REAR_PROJECTION / 2.0], MAT_DARK_SILVER))
        add_rear_fan(scene, f"Rear_AC_PSU_{index}_Fan", cx + 0.011, 0.002,
                     REAR_Z - REAR_PROJECTION - 0.0001, 0.015, sections)
        add(scene, f"Rear_AC_PSU_{index}_C13_Inlet",
            make_box([0.015, 0.021, 0.002],
                     [cx - 0.017, -0.001, REAR_Z - REAR_PROJECTION - 0.001], MAT_BLACK))
        add(scene, f"Rear_AC_PSU_{index}_Red_Release",
            make_box([0.013, 0.005, 0.004],
                     [cx - 0.019, 0.015, REAR_Z - REAR_PROJECTION - 0.001], MAT_RED))
        add(scene, f"Rear_AC_PSU_{index}_500W_Badge",
            make_cylinder(0.007, 0.0016,
                          [cx + 0.011, 0.002, REAR_Z - REAR_PROJECTION - 0.0018],
                          MAT_TEAL, sections, (0, 0, 1)))
        handle_z = REAR_Z - REAR_PROJECTION - 0.0015
        add(scene, f"Rear_AC_PSU_{index}_Handle_Bar",
            cylinder_between([cx + 0.025, -0.012, handle_z],
                             [cx - 0.003, -0.012, handle_z], 0.0022, MAT_BLACK, sections))
        for side, x in enumerate((cx + 0.025, cx - 0.003), start=1):
            add(scene, f"Rear_AC_PSU_{index}_Handle_Arm_{side}",
                cylinder_between([x, -0.012, REAR_Z - 0.003],
                                 [x, -0.012, handle_z], 0.0022, MAT_BLACK, sections))


def add_rear(scene: trimesh.Scene, sections: int,
             material: PBRMaterial) -> None:
    """Add source-projected rear relief without obscuring exact rear details."""
    # Large PCIe panels are shallow, independently shaped assemblies. Their
    # outward surfaces sample the same locked rear pixels as the base plane.
    # Slot 1 previously extended 8 mm into slot 2, putting two photo patches
    # on the same plane.  The corrected width ends at slot 2's verified edge.
    slot_specs = [(0.151, 0.011, 0.089, 0.011),
                  (0.079, 0.011, 0.055, 0.011),
                  (-0.001, 0.011, 0.096, 0.011)]
    for index, (x, y, w, h) in enumerate(slot_specs, start=1):
        add(scene, f"Rear_PCIe_Slot_{index}_Blank",
            make_box([w, h, 0.002], [x, y, REAR_Z - 0.001], MAT_SILVER))
        add(scene, f"Rear_PCIe_Slot_{index}_SourceLocked_Surface",
            projected_face_patch(
                "rear", x - w / 2.0, x + w / 2.0,
                y - h / 2.0, y + h / 2.0,
                REAR_Z - 0.00206, material))

    # Exact-source image measurement gives two approximately 70.4 mm wide
    # Flex Slot PSU faces centred at these world-X positions. The photo patch
    # retains the real fan, 500W marking, C13 inlet and release paddle.
    for index, cx in enumerate((-0.1095, -0.1800), start=1):
        psu_w = 0.0704
        psu_h = BODY_H - 0.001
        psu_face_z = REAR_Z - 0.00406
        add(scene, f"Rear_AC_PSU_{index}_Body",
            make_box([psu_w, psu_h, 0.004],
                     [cx, 0, REAR_Z - 0.002], MAT_DARK_SILVER))
        add(scene, f"Rear_AC_PSU_{index}_SourceLocked_Surface",
            projected_face_patch(
                "rear", cx - psu_w / 2.0, cx + psu_w / 2.0,
                -psu_h / 2.0, psu_h / 2.0,
                psu_face_z, material))

        # Only the real hinged handle meaningfully projects beyond the rear
        # face. Align it with the source instead of drawing synthetic fan and
        # connector blocks over the photograph.
        # Position the cylinder centre one radius inside the measured outer
        # projection so the handle's outermost surface, not its centreline,
        # lands at the 12 mm rear envelope.
        handle_z = REAR_Z - REAR_PROJECTION + 0.0022
        handle_left_x = cx + 0.026
        handle_right_x = cx - 0.024
        add(scene, f"Rear_AC_PSU_{index}_Handle_Bar",
            cylinder_between([handle_left_x, -0.012, handle_z],
                             [handle_right_x, -0.012, handle_z],
                             0.0022, MAT_BLACK, sections))
        for side, x in enumerate((handle_left_x, handle_right_x), start=1):
            add(scene, f"Rear_AC_PSU_{index}_Handle_Arm_{side}",
                cylinder_between([x, -0.012, psu_face_z],
                                 [x, -0.012, handle_z],
                                 0.0022, MAT_BLACK, sections))


def add_sides(scene: trimesh.Scene, sections: int) -> None:
    # Independent left/right rail hardware; positions deliberately differ.
    patterns = {
        "Left": {"x": -BODY_W / 2.0, "axis": (-1, 0, 0),
                 "pins": [(0.006, 0.290), (-0.006, 0.145), (0.006, -0.090), (-0.006, -0.320)],
                 "slots": [(0.011, 0.325), (-0.010, 0.250), (0.010, -0.305)]},
        "Right": {"x": BODY_W / 2.0, "axis": (1, 0, 0),
                  "pins": [(0.008, 0.310), (-0.006, 0.180), (0.007, 0.010), (-0.005, -0.280)],
                  "slots": [(-0.010, 0.300), (0.010, 0.060), (-0.010, -0.260)]},
    }
    for side, data in patterns.items():
        sign = -1 if side == "Left" else 1
        for index, (y, z) in enumerate(data["pins"], start=1):
            add(scene, f"Side_{side}_Rail_Mount_Pin_{index}",
                make_cylinder(0.0026, 0.0030,
                              [data["x"] + sign * 0.0015, y, z], MAT_SILVER,
                              sections, data["axis"]))
        for index, (y, z) in enumerate(data["slots"], start=1):
            add(scene, f"Side_{side}_Key_Slot_Recess_{index}",
                make_box([0.0015, 0.005, 0.014],
                         [data["x"] + sign * 0.0008, y, z], MAT_DARK))
        add(scene, f"Side_{side}_Upper_Pressed_Seam",
            make_box([0.0010, 0.0012, BODY_D - 0.055],
                     [data["x"] + sign * 0.0006, 0.013, 0.0], MAT_DARK_SILVER))
        add(scene, f"Side_{side}_Lower_Fold",
            make_box([0.0012, 0.0020, BODY_D - 0.020],
                     [data["x"] + sign * 0.0007, -0.019, 0.0], MAT_SILVER))


def top_hole_group(cx, cz, cols, rows, spacing_x, spacing_z, sections):
    holes = []
    for col in range(cols):
        for row in range(rows):
            holes.append(make_cylinder(0.0017, 0.0008,
                                       [cx + (col - (cols - 1) / 2) * spacing_x,
                                        BODY_H / 2.0 - 0.0004,
                                        cz + (row - (rows - 1) / 2) * spacing_z],
                                       MAT_DARK, sections, (0, 1, 0)))
    return holes


def add_top_and_internal(scene: trimesh.Scene, sections: int) -> None:
    add(scene, "Top_Transverse_Cover_Seam",
        make_box([BODY_W - 0.004, 0.0002, 0.0014],
                 [0, BODY_H / 2.0 - 0.0001, 0.270], MAT_DARK_SILVER))
    add(scene, "Top_Hood_Latch",
        make_box([0.027, 0.0018, 0.055],
                 [0.090, BODY_H / 2.0 - 0.0009, -0.050], MAT_DARK_SILVER))
    vent_groups = [
        ("Top_Front_Transverse_Vent", 0.0, 0.330, 24, 2, 0.014, 0.006),
        ("Top_Rear_Left_Vent", -0.105, -0.275, 11, 6, 0.008, 0.007),
        ("Top_Rear_Center_Vent", 0.025, -0.275, 14, 6, 0.008, 0.007),
        ("Top_Latch_Adjacent_Vent", 0.125, -0.135, 6, 8, 0.007, 0.007),
    ]
    for name, cx, cz, cols, rows, sx, sz in vent_groups:
        add_group(scene, name, top_hole_group(cx, cz, cols, rows, sx, sz, 12), MAT_DARK)
    # Proven yellow hot-surface label is shallow geometry; text remains in texture.
    add(scene, "Top_Hot_Surface_Label_Plate",
        make_box([0.050, 0.0008, 0.022],
                 [0.155, BODY_H / 2.0 - 0.0004, -0.325],
                 pbr("Top warning label yellow", (217, 181, 34, 255), 0.0, 0.72)))

    # Seven verified internal hot-plug fan modules behind the drive backplane.
    fan_x = np.linspace(-0.150, 0.150, 7)
    for index, x in enumerate(fan_x, start=1):
        add(scene, f"Internal_HotPlug_Fan_{index}_Module",
            make_box([0.038, 0.032, 0.038], [x, 0, 0.225], MAT_BLACK))
        add(scene, f"Internal_HotPlug_Fan_{index}_Rotor",
            make_cylinder(0.014, 0.010, [x, 0, 0.225], MAT_DARK_SILVER,
                          sections, (0, 0, 1)))
        add(scene, f"Internal_HotPlug_Fan_{index}_Red_Latch",
            make_box([0.012, 0.006, 0.010], [x, 0.014, 0.244], MAT_RED))


def build_scene(profile: str) -> trimesh.Scene:
    textures = {face: profile_texture(face, profile)
                for face in ("front", "rear", "left", "right", "top", "bottom")}
    face_materials = {face: texture_material(face, textures[face])
                      for face in textures}
    sections = 28 if profile == "standard" else 18
    scene = trimesh.Scene(base_frame="HPE-DL360G9-3.5inch_ROOT")
    scene.metadata.update({
        "manufacturer": "Hewlett Packard Enterprise",
        "product_id": "HPE ProLiant DL360 Gen9",
        "variant": "4LFF / 3.5-inch / 1U",
        "configuration": "4 installed LFF carriers; 3 PCIe positions; 4x1GbE FlexibleLOM; serial; iLO4; 2 USB3; VGA; 4 embedded NIC; 2x500W AC PSU",
        "coordinate_convention": "+X device right from front; +Y up; +Z front",
        "units": "metres",
        "source_model_used": False,
        "bottom_mode": "GENERIC_BOTTOM_FALLBACK",
        "profile": profile,
    })
    # Closed outward-facing shell; texture cards never expose an empty interior.
    add(scene, "Closed_Chassis_Core",
        make_box([BODY_W - 0.003, BODY_H - 0.003, BODY_D - 0.003], [0, 0, 0], MAT_BODY))
    for face in ("front", "rear", "left", "right", "top", "bottom"):
        add(scene, f"Face_{face.title()}_Approved_Imagegen",
            textured_quad(face, textures[face], face_materials[face]))
    add_front(scene, sections, face_materials["front"])
    add_rear(scene, sections, face_materials["rear"])
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
    gltf.asset.generator = "Trimesh exact-exterior construction + pygltflib face-unlit pass"
    gltf.asset.extras = {
        "manufacturer": "Hewlett Packard Enterprise",
        "product_id": "HPE ProLiant DL360 Gen9",
        "variant": "4LFF 3.5-inch",
        "profile": profile,
        "body_dimensions_mm": [434.6, 43.2, 750.0],
        "installed_bounds_mm": [482.6, 43.2, 770.0],
        "bottom_mode": "GENERIC_BOTTOM_FALLBACK",
        "visible_counts": {
            "LFF_carriers": 4,
            "front_rack_ears": 2,
            "PCIe_positions": 3,
            "FlexibleLOM_RJ45": 4,
            "rear_USB3": 2,
            "serial_DB9": 1,
            "dedicated_iLO4": 1,
            "embedded_RJ45": 4,
            "rear_VGA": 1,
            "AC_PSU": 2,
            "PSU_visible_fans": 2,
            "internal_hotplug_fans": 7,
        },
    }
    gltf.save_binary(str(path))


def export_profile(profile: str) -> Path:
    scene = build_scene(profile)
    filename = "HPE-DL360G9-3.5inch.glb" if profile == "standard" else "HPE-DL360G9-3.5inch-web.glb"
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
