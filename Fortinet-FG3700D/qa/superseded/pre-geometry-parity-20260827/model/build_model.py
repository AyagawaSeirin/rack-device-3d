#!/usr/bin/env python3
"""Build the exact-exterior Fortinet FortiGate FG-3700D AC GLBs.

This is a newly constructed website asset.  No third-party or official mesh is
copied.  Coordinate convention: +X device right from the port/front face,
+Y up, +Z port/front.  Dimensions are authored in metres.
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

import numpy as np
from PIL import Image
from pygltflib import GLTF2
from shapely.geometry import Point, Polygon, box as sbox
from shapely.ops import unary_union
import trimesh
from trimesh.visual import TextureVisuals
from trimesh.visual.material import PBRMaterial


ROOT = Path(__file__).resolve().parents[1]
MODEL = ROOT / "model"

BODY_W = 0.437
BODY_H = 0.133
BODY_D = 0.579
RACK_W = 0.4826
EAR_EXT = (RACK_W - BODY_W) / 2.0
FRONT_Z = BODY_D / 2.0
REAR_Z = -BODY_D / 2.0

FRONT_HANDLE_PROJECTION = 0.034
REAR_PSU_PROJECTION = 0.020


def pbr(name: str, rgba, metallic: float = 0.0, roughness: float = 0.78) -> PBRMaterial:
    """Create an opaque glTF PBR material using 8-bit source colors."""
    return PBRMaterial(
        name=name,
        baseColorFactor=list(rgba),
        metallicFactor=metallic,
        roughnessFactor=roughness,
        alphaMode="OPAQUE",
        doubleSided=False,
    )


MAT_BODY = pbr("FG3700D warm-white powder-coated steel", (232, 230, 216, 255), 0.02, 0.84)
MAT_WHITE = pbr("FG3700D rack and tray white", (255, 255, 255, 255), 0.0, 1.0)
MAT_GRID = pbr("FG3700D warm-white fan grille steel", (232, 230, 216, 255), 0.03, 0.80)
MAT_BLACK = pbr("Connector fan and recess black", (10, 11, 10, 255), 0.0, 0.90)
MAT_DARK = pbr("Dark fan cavity", (27, 29, 27, 255), 0.02, 0.87)
MAT_FAN = pbr("Fan blade charcoal", (48, 50, 47, 255), 0.08, 0.72)
MAT_SILVER = pbr("Polished rack handle and fastener steel", (190, 192, 186, 255), 0.72, 0.23)
MAT_DARK_SILVER = pbr("Connector cage plated metal", (118, 121, 115, 255), 0.42, 0.45)
MAT_GREEN = pbr("PSU release green", (34, 133, 86, 255), 0.0, 0.58)
MAT_LED = pbr("Status lens gray-green", (92, 112, 91, 255), 0.0, 0.30)


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


def texture_material(face: str, image: Image.Image) -> PBRMaterial:
    return PBRMaterial(
        name=f"SOURCE_LOCKED_{face.upper()}_photographic_texture",
        baseColorFactor=[255, 255, 255, 255],
        baseColorTexture=image.convert("RGB"),
        metallicFactor=0.0,
        roughnessFactor=0.88,
        alphaMode="OPAQUE",
        doubleSided=False,
    )


def textured_quad(face: str, image: Image.Image) -> trimesh.Trimesh:
    """Create an outward-facing canonical body plane."""
    # The closed core is inset, so the photographic surfaces can sit on the
    # exact body datum without z-fighting or inflating the verified bounds.
    eps = 0.0
    x0, x1 = -BODY_W / 2.0, BODY_W / 2.0
    y0, y1 = -BODY_H / 2.0, BODY_H / 2.0
    z0, z1 = REAR_Z, FRONT_Z
    if face == "front":
        verts = [[x0, y0, z1 + eps], [x1, y0, z1 + eps],
                 [x1, y1, z1 + eps], [x0, y1, z1 + eps]]
    elif face == "rear":
        verts = [[x1, y0, z0 - eps], [x0, y0, z0 - eps],
                 [x0, y1, z0 - eps], [x1, y1, z0 - eps]]
    elif face == "left":
        verts = [[x0 - eps, y0, z0], [x0 - eps, y0, z1],
                 [x0 - eps, y1, z1], [x0 - eps, y1, z0]]
    elif face == "right":
        verts = [[x1 + eps, y0, z1], [x1 + eps, y0, z0],
                 [x1 + eps, y1, z0], [x1 + eps, y1, z1]]
    elif face == "top":
        verts = [[x0, y1 + eps, z1], [x1, y1 + eps, z1],
                 [x1, y1 + eps, z0], [x0, y1 + eps, z0]]
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


def bottom_slot_shape(cx: float, cz: float, mirror: int) -> Polygon:
    """One verified stamped rail/key slot in the underside plane."""
    x0 = cx + mirror * 0.0045
    narrow = sbox(x0 - 0.00165, cz - 0.0085, x0 + 0.00165, cz + 0.0085)
    shoulder = sbox(
        x0 - 0.0026,
        cz + (0.0020 if mirror < 0 else -0.0080),
        x0 + 0.0026,
        cz + (0.0080 if mirror < 0 else -0.0020),
    )
    return unary_union([narrow, shoulder])


def bottom_holed_plane(image: Image.Image) -> tuple[trimesh.Trimesh, list[tuple[float, float]]]:
    """Texture the exact bottom while retaining seven groups of true double holes."""
    body = sbox(-BODY_W / 2.0, REAR_Z, BODY_W / 2.0, FRONT_Z)
    groups = [
        (-0.183, -0.225), (0.000, -0.225), (0.177, -0.225),
        (-0.091, -0.058), (0.082, -0.058),
        (-0.155, 0.084), (0.158, 0.084),
    ]
    holes = []
    for cx, cz in groups:
        holes.append(bottom_slot_shape(cx, cz, -1))
        holes.append(bottom_slot_shape(cx, cz, 1))
    surface = body.difference(unary_union(holes))
    verts2d, faces = trimesh.creation.triangulate_polygon(surface, engine="earcut")
    verts = np.column_stack([
        verts2d[:, 0],
        np.full(len(verts2d), -BODY_H / 2.0),
        verts2d[:, 1],
    ])
    faces = np.asarray(faces, dtype=np.int64)
    test = np.cross(verts[faces[0, 1]] - verts[faces[0, 0]],
                    verts[faces[0, 2]] - verts[faces[0, 0]])
    if test[1] > 0:
        faces = faces[:, [0, 2, 1]]

    # Natural underside: camera at -Y, physical +X at screen left and +Z/front
    # at screen bottom.  glTF texture UVs use the same approved portrait image.
    u = (BODY_W / 2.0 - verts[:, 0]) / BODY_W
    v = (FRONT_Z - verts[:, 2]) / BODY_D
    uv = np.column_stack([u, v]).astype(np.float32)
    mesh = trimesh.Trimesh(vertices=verts, faces=faces, process=False)
    mesh.visual = TextureVisuals(uv=uv, material=texture_material("bottom", image))
    return mesh, groups


def rounded_rect(x0, y0, x1, y1, radius):
    cores = [sbox(x0 + radius, y0, x1 - radius, y1),
             sbox(x0, y0 + radius, x1, y1 - radius)]
    corners = [Point(x, y).buffer(radius, resolution=12)
               for x in (x0 + radius, x1 - radius)
               for y in (y0 + radius, y1 - radius)]
    return unary_union([*cores, *corners])


def rack_ear(sign: int) -> trimesh.Trimesh:
    """Front rack flange with a large lightening opening and two true rack holes."""
    outer = sbox(-EAR_EXT / 2.0, -BODY_H / 2.0, EAR_EXT / 2.0, BODY_H / 2.0)
    cutout = rounded_rect(-0.0046, -0.034, 0.0046, 0.034, 0.0032)
    rack_holes = unary_union([
        Point(0, -0.052).buffer(0.0038, resolution=16),
        Point(0, 0.052).buffer(0.0038, resolution=16),
    ])
    plate = outer.difference(unary_union([cutout, rack_holes]))
    mesh = trimesh.creation.extrude_polygon(plate, height=0.003, engine="earcut")
    mesh.apply_translation([
        sign * (BODY_W / 2.0 + EAR_EXT / 2.0),
        0.0,
        FRONT_Z - 0.0015,
    ])
    return set_material(mesh, MAT_WHITE)


def side_bracket_frame(sign: int) -> trimesh.Trimesh:
    """The deep side plate of the supplied front rack bracket with a true opening."""
    depth = 0.145
    outer = rounded_rect(FRONT_Z - depth, -0.059, FRONT_Z - 0.004, 0.059, 0.004)
    inner = rounded_rect(FRONT_Z - depth + 0.013, -0.046,
                         FRONT_Z - 0.017, 0.046, 0.005)
    frame = outer.difference(inner)
    mesh = trimesh.creation.extrude_polygon(frame, height=0.0024, engine="earcut")
    # Shapely X/Y map to model Z/Y; the extrusion axis becomes model X.
    matrix = np.array([
        [0, 0, 1, 0],
        [0, 1, 0, 0],
        [1, 0, 0, 0],
        [0, 0, 0, 1],
    ], dtype=float)
    mesh.apply_transform(matrix)
    x = sign * (BODY_W / 2.0 + 0.0012)
    if sign < 0:
        mesh.apply_scale([-1, 1, 1])
    mesh.apply_translation([x, 0, 0])
    return set_material(mesh, MAT_WHITE)


def frame_bars(cx, cy, width, height, z, depth=0.0010, bar=0.0011,
               material=MAT_DARK_SILVER):
    return [
        make_box([width, bar, depth], [cx, cy + height / 2.0, z], material),
        make_box([width, bar, depth], [cx, cy - height / 2.0, z], material),
        make_box([bar, height, depth], [cx - width / 2.0, cy, z], material),
        make_box([bar, height, depth], [cx + width / 2.0, cy, z], material),
    ]


def build_front_geometry(scene: trimesh.Scene, sections: int) -> None:
    add(scene, "Front_Rack_Flange_Left_True_3_Holes", rack_ear(-1))
    add(scene, "Front_Rack_Flange_Right_True_3_Holes", rack_ear(1))
    add(scene, "Front_Side_Bracket_Left_Large_True_Opening", side_bracket_frame(-1))
    add(scene, "Front_Side_Bracket_Right_Large_True_Opening", side_bracket_frame(1))

    # Separate polished U-shaped pull handles. Their outer edge is exactly 34 mm
    # in front of the chassis datum, matching the dimension ledger.
    handle_radius = 0.0042
    bar_z = FRONT_Z + FRONT_HANDLE_PROJECTION - handle_radius
    anchor_z = FRONT_Z + 0.0010
    for sign, side in ((-1, "Left"), (1, "Right")):
        x = sign * (BODY_W / 2.0 - 0.010)
        add(scene, f"Front_Rack_Handle_{side}_Vertical",
            cylinder_between([x, -0.044, bar_z], [x, 0.044, bar_z],
                             handle_radius, MAT_SILVER, sections))
        for idx, y in enumerate((-0.044, 0.044)):
            add(scene, f"Front_Rack_Handle_{side}_Arm_{idx}",
                cylinder_between([x, y, anchor_z], [x, y, bar_z],
                                 handle_radius, MAT_SILVER, sections))

    z_black = FRONT_Z + 0.00055
    z_frame = FRONT_Z + 0.00115
    black, frames, lips = [], [], []

    # Four verified QSFP+ cages 1-4.
    for number, x in enumerate((-0.121, -0.096, -0.071, -0.046), start=1):
        black.append(make_box([0.0200, 0.0145, 0.0012], [x, -0.042, z_black], MAT_BLACK))
        frames.extend(frame_bars(x, -0.042, 0.0212, 0.0157, z_frame,
                                 depth=0.0014, bar=0.0011))
        lips.append(make_box([0.0165, 0.0010, 0.0017],
                             [x, -0.0341, z_frame + 0.0002], MAT_DARK_SILVER))

    # Twenty-eight verified SFP/SFP+ cages: odd ports above even ports in four
    # mechanically framed groups (2 + 4 + 4 + 4 columns).
    sfp_x = [
        0.000, 0.015,
        0.032, 0.047, 0.062, 0.077,
        0.093, 0.108, 0.123, 0.138,
        0.155, 0.170, 0.185, 0.200,
    ]
    for col, x in enumerate(sfp_x):
        for row, y in enumerate((-0.0325, -0.0520)):
            number = 5 + col * 2 + row
            black.append(make_box([0.0128, 0.0094, 0.0013], [x, y, z_black], MAT_BLACK))
            frames.extend(frame_bars(x, y, 0.0138, 0.0104, z_frame,
                                     depth=0.0015, bar=0.00075))
            lips.append(make_box([0.0108, 0.0010, 0.0018],
                                 [x, y + 0.0056, z_frame + 0.00025], MAT_DARK_SILVER))
            assert 5 <= number <= 32

    # Source-matched front management and console relief.
    for name, x, y, w, h in (
        ("Console_RJ45", -0.1665, -0.0330, 0.0150, 0.0190),
        ("USB_A", -0.1665, -0.0530, 0.0150, 0.0090),
        ("MGMT_1_RJ45", -0.1430, -0.0315, 0.0150, 0.0190),
        ("MGMT_2_RJ45", -0.1430, -0.0520, 0.0150, 0.0190),
        ("USB_MGMT_MiniB", -0.1995, -0.0520, 0.0090, 0.0052),
    ):
        black.append(make_box([w, h, 0.0013], [x, y, z_black], MAT_BLACK))
        frames.extend(frame_bars(x, y, w + 0.0014, h + 0.0014, z_frame,
                                 depth=0.0014, bar=0.00065))

    add_group(scene, "Front_Black_Recesses_4_QSFP_28_SFP_5_Management", black, MAT_BLACK)
    add_group(scene, "Front_Metal_Cage_Frames_4_QSFP_28_SFP_5_Management", frames,
              MAT_DARK_SILVER)
    add_group(scene, "Front_Transceiver_Latch_Lips", lips, MAT_DARK_SILVER)

    leds = []
    for idx, y in enumerate((-0.0295, -0.0367, -0.0440, -0.0513)):
        leds.append(make_box([0.0022, 0.0022, 0.0010],
                             [-0.1810, y, FRONT_Z + 0.0011], MAT_LED))
    add_group(scene, "Front_Status_Alarm_HA_Power_Lenses_4", leds, MAT_LED)


def fan_rotor_mesh(cx: float, sections: int) -> list[trimesh.Trimesh]:
    meshes = [
        make_cylinder(0.033, 0.0012, [cx, 0.0, REAR_Z - 0.0010],
                      MAT_DARK, sections, (0, 0, 1)),
        make_cylinder(0.009, 0.0018, [cx, 0.0, REAR_Z - 0.0020],
                      MAT_FAN, sections, (0, 0, 1)),
    ]
    for idx in range(7):
        angle = idx * (2.0 * math.pi / 7.0)
        blade = make_box([0.024, 0.0070, 0.0010],
                         [cx + math.cos(angle) * 0.016,
                          math.sin(angle) * 0.016,
                          REAR_Z - 0.0018], MAT_FAN)
        transform = trimesh.transformations.rotation_matrix(angle + 0.45, [0, 0, 1],
                                                             [cx, 0, REAR_Z - 0.0018])
        blade.apply_transform(transform)
        meshes.append(blade)
    return meshes


def build_rear_geometry(scene: trimesh.Scene, sections: int) -> None:
    # Two AC hot-swap PSUs remain separate and source-matched left/right modules.
    psu_centers = (-0.194, 0.194)
    psu_seams, iec, loops, releases = [], [], [], []
    for idx, x in enumerate(psu_centers, start=1):
        psu_seams.extend(frame_bars(x, -0.010, 0.046, 0.101, REAR_Z - 0.0017,
                                    depth=0.0020, bar=0.0014, material=MAT_WHITE))
        iec.append(make_box([0.028, 0.043, 0.0022],
                            [x, -0.019, REAR_Z - 0.0018], MAT_BLACK))

        loop_radius = 0.0035
        loop_z = REAR_Z - REAR_PSU_PROJECTION + loop_radius
        anchor_z = REAR_Z - 0.0010
        x0, x1 = x - 0.020, x + 0.020
        y0, y1 = -0.046, -0.018
        loops.append(cylinder_between([x0, y0, loop_z], [x1, y0, loop_z],
                                      loop_radius, MAT_BLACK, sections))
        loops.append(cylinder_between([x0, y0, loop_z], [x0, y1, loop_z],
                                      loop_radius, MAT_BLACK, sections))
        loops.append(cylinder_between([x1, y0, loop_z], [x1, y1, loop_z],
                                      loop_radius, MAT_BLACK, sections))
        loops.append(cylinder_between([x0, y1, anchor_z], [x0, y1, loop_z],
                                      loop_radius, MAT_BLACK, sections))
        loops.append(cylinder_between([x1, y1, anchor_z], [x1, y1, loop_z],
                                      loop_radius, MAT_BLACK, sections))
        releases.append(make_box([0.017, 0.006, 0.005],
                                 [x + (-0.010 if idx == 1 else 0.010), -0.057,
                                  REAR_Z - 0.004], MAT_GREEN))

    add_group(scene, "Rear_AC_PSU_1_2_Module_Seams", psu_seams, MAT_WHITE)
    add_group(scene, "Rear_AC_PSU_1_2_IEC_C14_Recesses", iec, MAT_BLACK)
    add_group(scene, "Rear_AC_PSU_1_2_Black_Pull_Loops", loops, MAT_BLACK)
    add_group(scene, "Rear_AC_PSU_1_2_Green_Release_Tabs", releases, MAT_GREEN)

    fan_centers = (-0.091, 0.000, 0.091)
    fan_meshes, grille_white, tray_frames = [], [], []
    for cx in fan_centers:
        fan_meshes.extend(fan_rotor_mesh(cx, sections))
        tray_frames.extend(frame_bars(cx, 0.0, 0.084, 0.094, REAR_Z - 0.0027,
                                      depth=0.0020, bar=0.0016, material=MAT_GRID))
        # Independent square-perforated tray geometry over each visible rotor.
        for offset in np.linspace(-0.036, 0.036, 10):
            grille_white.append(make_box([0.0012, 0.090, 0.0016],
                                         [cx + float(offset), 0.0, REAR_Z - 0.0030], MAT_GRID))
        for offset in np.linspace(-0.040, 0.040, 11):
            grille_white.append(make_box([0.080, 0.0012, 0.0016],
                                         [cx, float(offset), REAR_Z - 0.0031], MAT_GRID))

    add_group(scene, "Rear_Three_Fan_Rotors_Blades_Hubs", fan_meshes, MAT_FAN)
    add_group(scene, "Rear_Three_Independent_Fan_Tray_Frames", tray_frames, MAT_GRID)
    add_group(scene, "Rear_Three_Square_Perforated_Grilles", grille_white, MAT_GRID)

    indicators = []
    for idx, x in enumerate((-0.132, -0.115, -0.043, -0.026, 0.071, 0.132), start=1):
        indicators.append(make_cylinder(0.0030, 0.0014,
                                        [x, -0.027, REAR_Z - 0.0042], MAT_LED,
                                        sections, (0, 0, 1)))
    add_group(scene, "Rear_FAN_Status_Indicators_6", indicators, MAT_LED)

    add(scene, "Rear_Grounding_Stud_Plate",
        make_box([0.018, 0.050, 0.0018], [0.160, -0.006, REAR_Z - 0.0022], MAT_DARK_SILVER))
    for idx, y in enumerate((0.012, -0.023)):
        add(scene, f"Rear_Grounding_Stud_{idx + 1}",
            make_cylinder(0.0044, 0.0060, [0.160, y, REAR_Z - 0.0050],
                          MAT_SILVER, sections, (0, 0, 1)))


def build_side_and_cover_relief(scene: trimesh.Scene, sections: int) -> None:
    # Non-mirrored side embossing derived independently from the two locked sides.
    side_data = {
        "Left": {
            "x": -BODY_W / 2.0 - 0.0014,
            "axis": (-1, 0, 0),
            "standoffs": [(-0.050, -0.247), (-0.048, -0.118),
                           (-0.047, 0.054), (-0.045, 0.232)],
            "screws": [(0.008, -0.035), (0.009, 0.105), (-0.050, 0.179)],
        },
        "Right": {
            "x": BODY_W / 2.0 + 0.0014,
            "axis": (1, 0, 0),
            "standoffs": [(-0.048, -0.250), (-0.047, -0.008),
                           (-0.046, 0.150), (-0.045, 0.264)],
            "screws": [(0.006, -0.082), (0.007, 0.073), (-0.050, 0.038)],
        },
    }
    for side, data in side_data.items():
        for idx, (y, z) in enumerate(data["standoffs"]):
            add(scene, f"{side}_Stamped_Standoff_{idx + 1}",
                make_cylinder(0.0040, 0.0028, [data["x"], y, z], MAT_WHITE,
                              sections, data["axis"]))
        for idx, (y, z) in enumerate(data["screws"]):
            add(scene, f"{side}_Independent_Fastener_{idx + 1}",
                make_cylinder(0.0022, 0.0011,
                              [data["x"] + (-0.0005 if side == "Left" else 0.0005), y, z],
                              MAT_SILVER, sections, data["axis"]))

    # The removable top cover sits slightly proud and retains separate edge relief.
    cover_edges = [
        make_box([BODY_W - 0.006, 0.0012, 0.0020],
                 [0.0, BODY_H / 2.0 - 0.00035, FRONT_Z - 0.003], MAT_WHITE),
        make_box([BODY_W - 0.006, 0.0012, 0.0020],
                 [0.0, BODY_H / 2.0 - 0.00035, REAR_Z + 0.003], MAT_WHITE),
    ]
    add_group(scene, "Top_Removable_Cover_Front_Rear_Seam_Relief", cover_edges, MAT_WHITE)

    top_screws = []
    for idx, (x, z) in enumerate(((-0.180, 0.278), (-0.055, 0.278), (0.070, 0.278),
                                  (0.195, 0.278), (-0.150, -0.278), (0.000, -0.278),
                                  (0.150, -0.278))):
        top_screws.append(make_cylinder(0.0021, 0.0008,
                                        [x, BODY_H / 2.0 - 0.00015, z], MAT_SILVER,
                                        sections, (0, 1, 0)))
    add_group(scene, "Top_Cover_Perimeter_Screws_7", top_screws, MAT_SILVER)


def build_scene(profile: str) -> trimesh.Scene:
    textures_dir = MODEL / "textures" / profile
    textures = {
        face: Image.open(textures_dir / f"{face}.png").convert("RGB")
        for face in ("front", "rear", "left", "right", "top", "bottom")
    }
    sections = 24 if profile == "standard" else 18
    scene = trimesh.Scene(base_frame="Fortinet-FG3700D_ROOT")
    scene.metadata.update({
        "manufacturer": "Fortinet, Inc.",
        "product_family": "FortiGate",
        "product_id": "FG-3700D",
        "installed_configuration": "FG-3700D-USG AC; 2 AC PSU; 3 rear fan trays; 4 QSFP+; 28 SFP/SFP+",
        "coordinate_convention": "+X right from front; +Y up; +Z port/front",
        "units": "metres",
        "source_model_used": False,
        "bottom_mode": "SOURCE_LOCKED_GENERATION",
        "bottom_verified_double_keyhole_groups": 7,
        "profile": profile,
    })

    # A closed load-bearing core prevents an exposed empty interior.  The exact
    # source-locked surface planes sit immediately outside it.
    add(scene, "Closed_Chassis_Core",
        make_box([BODY_W - 0.004, BODY_H - 0.004, BODY_D - 0.004], [0, 0, 0], MAT_BODY))
    for face in ("front", "rear", "left", "right", "top"):
        add(scene, f"Face_{face.title()}_SourceLocked", textured_quad(face, textures[face]))

    bottom_mesh, bottom_groups = bottom_holed_plane(textures["bottom"])
    add(scene, "Face_Bottom_SourceLocked_7_Double_Keyhole_Groups", bottom_mesh)
    backings = []
    for cx, cz in bottom_groups:
        backings.append(make_box([0.018, 0.0010, 0.026],
                                 [cx, -BODY_H / 2.0 + 0.0010, cz], MAT_DARK))
    add_group(scene, "Bottom_7_Double_Keyhole_Dark_Interior_Backings", backings, MAT_DARK)

    build_front_geometry(scene, sections)
    build_rear_geometry(scene, sections)
    build_side_and_cover_relief(scene, sections)
    return scene


def add_unlit_extension(path: Path, profile: str) -> None:
    """Use unlit on the six photographic face materials only."""
    gltf = GLTF2().load_binary(str(path))
    extensions_used = list(gltf.extensionsUsed or [])
    if "KHR_materials_unlit" not in extensions_used:
        extensions_used.append("KHR_materials_unlit")
    gltf.extensionsUsed = extensions_used
    for material in gltf.materials or []:
        if material.name and (
            material.name.startswith("SOURCE_LOCKED_")
            or material.name == "FG3700D rack and tray white"
        ):
            material.extensions = dict(material.extensions or {})
            material.extensions["KHR_materials_unlit"] = {}
            material.alphaMode = "OPAQUE"
            material.doubleSided = False
    gltf.asset.generator = "Trimesh exact-exterior construction + pygltflib unlit face pass"
    gltf.asset.extras = {
        "manufacturer": "Fortinet, Inc.",
        "product_id": "FG-3700D",
        "configuration": "FG-3700D-USG AC",
        "profile": profile,
        "body_dimensions_mm": [437, 133, 579],
        "installed_bounds_mm": [482.6, 133, 633],
        "visible_counts": {
            "QSFP_plus": 4,
            "SFP_SFP_plus": 28,
            "AC_PSU": 2,
            "rear_fan_trays": 3,
            "rear_visible_rotors": 3,
            "fan_indicators": 6,
            "grounding_studs": 2,
            "bottom_double_keyhole_groups": 7,
        },
    }
    gltf.save_binary(str(path))


def export_profile(profile: str) -> Path:
    scene = build_scene(profile)
    filename = "Fortinet-FG3700D.glb" if profile == "standard" else "Fortinet-FG3700D-web.glb"
    output = MODEL / filename
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_bytes(scene.export(file_type="glb", include_normals=True))
    add_unlit_extension(output, profile)
    return output


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--profile", choices=("standard", "web", "both"), default="both")
    args = parser.parse_args()
    profiles = ("standard", "web") if args.profile == "both" else (args.profile,)
    outputs = []
    for profile in profiles:
        output = export_profile(profile)
        outputs.append({"profile": profile, "path": str(output), "bytes": output.stat().st_size})
    print(json.dumps(outputs, indent=2))


if __name__ == "__main__":
    main()
