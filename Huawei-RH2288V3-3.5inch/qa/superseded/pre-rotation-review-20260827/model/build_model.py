#!/usr/bin/env python3
"""Build the evidence-locked Huawei FusionServer RH2288 V3 12-LFF GLBs.

Right-handed glTF coordinates: +X is device-right from the front, +Y is up,
and +Z points toward the front. Authored dimensions are millimetres.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
from PIL import Image
import trimesh
from trimesh.visual import TextureVisuals
from trimesh.visual.material import PBRMaterial
from pygltflib import GLTF2


ROOT = Path(__file__).resolve().parents[1]
VIEWS = ROOT / "views"
MODEL = ROOT / "model"
MM = 0.001

BODY_W = 447.0
OVERALL_W = 482.6
HEIGHT = 86.1
DEPTH = 748.0
FRONT_Z = DEPTH / 2.0
REAR_Z = -DEPTH / 2.0


def material(
    name: str,
    rgba: tuple[int, int, int, int],
    roughness: float = 0.72,
    metallic: float = 0.0,
) -> PBRMaterial:
    return PBRMaterial(
        name=name,
        baseColorFactor=list(rgba),
        metallicFactor=metallic,
        roughnessFactor=roughness,
        alphaMode="OPAQUE",
        doubleSided=False,
    )


ZINC = material("Galvanized zinc sheet metal", (164, 170, 173, 255), 0.55, 0.18)
ZINC_DARK = material("Galvanized recessed metal", (100, 107, 110, 255), 0.66, 0.12)
BLACK = material("Black grille and connector", (10, 12, 13, 255), 0.84)
CHARCOAL = material("Dark carrier/control polymer", (34, 37, 39, 255), 0.82)
GREEN = material("Huawei yellow-green accent", (184, 211, 22, 255), 0.42)
BLUE = material("VGA blue polymer", (30, 105, 208, 255), 0.52)
TEAL = material("Serial-port teal plate", (30, 154, 142, 255), 0.58)
SILVER = material("Fastener and fan-guard silver", (194, 199, 202, 255), 0.36, 0.58)


def texture_material(face: str, web: bool) -> PBRMaterial:
    image = Image.open(VIEWS / f"{face}.png").convert("RGBA")
    bounds = image.getchannel("A").getbbox()
    if bounds is None:
        raise RuntimeError(f"{face}: empty alpha matte")
    # Transparent canvas belongs to the elevation deliverable, not to the GLB.
    # Every equipment surface is deliberately embedded as an opaque RGB texture.
    image = image.crop(bounds).convert("RGB")
    max_edge = 2048 if web else 4096
    if max(image.size) > max_edge:
        scale = max_edge / max(image.size)
        image = image.resize(
            (max(1, round(image.width * scale)), max(1, round(image.height * scale))),
            Image.Resampling.LANCZOS,
        )
    return PBRMaterial(
        name=f"{face.upper()} approved evidence texture" + (" WEB" if web else ""),
        baseColorFactor=[255, 255, 255, 255],
        baseColorTexture=image,
        metallicFactor=0.0,
        roughnessFactor=0.76,
        alphaMode="OPAQUE",
        doubleSided=False,
    )


def add(scene: trimesh.Scene, mesh: trimesh.Trimesh, name: str) -> None:
    mesh.metadata["name"] = name
    scene.add_geometry(mesh, node_name=name, geom_name=name)


def add_box(scene: trimesh.Scene, name: str, extents, center, mat: PBRMaterial) -> None:
    mesh = trimesh.creation.box(extents=np.asarray(extents, dtype=float) * MM)
    mesh.apply_translation(np.asarray(center, dtype=float) * MM)
    mesh.visual.material = mat
    add(scene, mesh, name)


def add_cylinder(
    scene: trimesh.Scene,
    name: str,
    radius: float,
    length: float,
    center,
    axis,
    mat: PBRMaterial,
    sections: int = 18,
) -> None:
    mesh = trimesh.creation.cylinder(radius=radius * MM, height=length * MM, sections=sections)
    direction = np.asarray(axis, dtype=float)
    direction /= np.linalg.norm(direction)
    mesh.apply_transform(trimesh.geometry.align_vectors([0.0, 0.0, 1.0], direction))
    mesh.apply_translation(np.asarray(center, dtype=float) * MM)
    mesh.visual.material = mat
    add(scene, mesh, name)


def add_rod_between(
    scene: trimesh.Scene,
    name: str,
    start,
    end,
    radius: float,
    mat: PBRMaterial,
    sections: int = 10,
) -> None:
    start_array = np.asarray(start, dtype=float)
    end_array = np.asarray(end, dtype=float)
    vector = end_array - start_array
    add_cylinder(
        scene,
        name,
        radius,
        float(np.linalg.norm(vector)),
        (start_array + end_array) / 2.0,
        vector,
        mat,
        sections,
    )


def add_quad(scene: trimesh.Scene, name: str, vertices_mm, mat: PBRMaterial) -> None:
    vertices = np.asarray(vertices_mm, dtype=float) * MM
    faces = np.asarray([[0, 1, 2], [0, 2, 3]], dtype=int)
    uv = np.asarray([[0.0, 0.0], [1.0, 0.0], [1.0, 1.0], [0.0, 1.0]], dtype=float)
    mesh = trimesh.Trimesh(vertices=vertices, faces=faces, process=False)
    mesh.visual = TextureVisuals(uv=uv, material=mat)
    add(scene, mesh, name)


def add_quad_uv(
    scene: trimesh.Scene,
    name: str,
    vertices_mm,
    uv_coordinates,
    mat: PBRMaterial,
) -> None:
    vertices = np.asarray(vertices_mm, dtype=float) * MM
    faces = np.asarray([[0, 1, 2], [0, 2, 3]], dtype=int)
    mesh = trimesh.Trimesh(vertices=vertices, faces=faces, process=False)
    mesh.visual = TextureVisuals(uv=np.asarray(uv_coordinates, dtype=float), material=mat)
    add(scene, mesh, name)


def add_frame(
    scene: trimesh.Scene,
    prefix: str,
    width: float,
    height: float,
    center_x: float,
    center_y: float,
    z: float,
    outward: int,
    bar: float,
    depth: float,
    mat: PBRMaterial,
) -> None:
    center_z = z + outward * depth / 2.0
    add_box(
        scene,
        f"{prefix}_Top",
        (width, bar, depth),
        (center_x, center_y + height / 2.0 - bar / 2.0, center_z),
        mat,
    )
    add_box(
        scene,
        f"{prefix}_Bottom",
        (width, bar, depth),
        (center_x, center_y - height / 2.0 + bar / 2.0, center_z),
        mat,
    )
    add_box(
        scene,
        f"{prefix}_Left",
        (bar, height - 2 * bar, depth),
        (center_x - width / 2.0 + bar / 2.0, center_y, center_z),
        mat,
    )
    add_box(
        scene,
        f"{prefix}_Right",
        (bar, height - 2 * bar, depth),
        (center_x + width / 2.0 - bar / 2.0, center_y, center_z),
        mat,
    )


def add_open_front_panel(
    scene: trimesh.Scene,
    name: str,
    width: float,
    height: float,
    depth: float,
    center_x: float,
    mat: PBRMaterial,
) -> None:
    """Create front/side ear geometry with no rear-facing cap."""
    x0, x1 = center_x - width / 2.0, center_x + width / 2.0
    y0, y1 = -height / 2.0, height / 2.0
    z0, z1 = FRONT_Z - depth, FRONT_Z
    vertices = np.asarray(
        [
            (x0, y0, z0), (x1, y0, z0), (x1, y1, z0), (x0, y1, z0),
            (x0, y0, z1), (x1, y0, z1), (x1, y1, z1), (x0, y1, z1),
        ],
        dtype=float,
    ) * MM
    faces = np.asarray(
        [
            (4, 5, 6), (4, 6, 7),  # front, +Z
            (0, 4, 7), (0, 7, 3),  # left, -X
            (1, 2, 6), (1, 6, 5),  # right, +X
            (3, 7, 6), (3, 6, 2),  # top, +Y
            (0, 1, 5), (0, 5, 4),  # bottom, -Y
        ],
        dtype=int,
    )
    mesh = trimesh.Trimesh(vertices=vertices, faces=faces, process=False)
    mesh.visual.material = mat
    add(scene, mesh, name)


def add_textured_shell(scene: trimesh.Scene, web: bool) -> dict[str, PBRMaterial]:
    tex = {
        face: texture_material(face, web)
        for face in ("front", "rear", "left", "right", "top", "bottom")
    }
    add_box(
        scene,
        "Closed_Chassis_Sheet_Metal_447x748x86.1mm",
        (BODY_W, HEIGHT, DEPTH),
        (0, 0, 0),
        ZINC,
    )

    add_quad(
        scene,
        "Texture_FRONT_12LFF_and_Control_Ears",
        [
            (-OVERALL_W / 2, -HEIGHT / 2, FRONT_Z + 0.10),
            (OVERALL_W / 2, -HEIGHT / 2, FRONT_Z + 0.10),
            (OVERALL_W / 2, HEIGHT / 2, FRONT_Z + 0.10),
            (-OVERALL_W / 2, HEIGHT / 2, FRONT_Z + 0.10),
        ],
        tex["front"],
    )
    add_quad(
        scene,
        "Texture_REAR_No_Drives_SM211_Dual_Stacked_AC",
        [
            (BODY_W / 2, -HEIGHT / 2, REAR_Z - 0.10),
            (-BODY_W / 2, -HEIGHT / 2, REAR_Z - 0.10),
            (-BODY_W / 2, HEIGHT / 2, REAR_Z - 0.10),
            (BODY_W / 2, HEIGHT / 2, REAR_Z - 0.10),
        ],
        tex["rear"],
    )
    add_quad(
        scene,
        "Texture_LEFT_Independent",
        [
            (-BODY_W / 2 - 0.10, -HEIGHT / 2, REAR_Z),
            (-BODY_W / 2 - 0.10, -HEIGHT / 2, FRONT_Z),
            (-BODY_W / 2 - 0.10, HEIGHT / 2, FRONT_Z),
            (-BODY_W / 2 - 0.10, HEIGHT / 2, REAR_Z),
        ],
        tex["left"],
    )
    add_quad(
        scene,
        "Texture_RIGHT_Independent",
        [
            (BODY_W / 2 + 0.10, -HEIGHT / 2, FRONT_Z),
            (BODY_W / 2 + 0.10, -HEIGHT / 2, REAR_Z),
            (BODY_W / 2 + 0.10, HEIGHT / 2, REAR_Z),
            (BODY_W / 2 + 0.10, HEIGHT / 2, FRONT_Z),
        ],
        tex["right"],
    )
    add_quad_uv(
        scene,
        "Texture_TOP_Cover",
        [
            (BODY_W / 2, HEIGHT / 2 + 0.10, REAR_Z),
            (-BODY_W / 2, HEIGHT / 2 + 0.10, REAR_Z),
            (-BODY_W / 2, HEIGHT / 2 + 0.10, FRONT_Z),
            (BODY_W / 2, HEIGHT / 2 + 0.10, FRONT_Z),
        ],
        [(1.0, 1.0), (0.0, 1.0), (0.0, 0.0), (1.0, 0.0)],
        tex["top"],
    )
    add_quad(
        scene,
        "Texture_BOTTOM_Generic_Fallback",
        [
            (-BODY_W / 2, -HEIGHT / 2 - 0.10, REAR_Z),
            (BODY_W / 2, -HEIGHT / 2 - 0.10, REAR_Z),
            (BODY_W / 2, -HEIGHT / 2 - 0.10, FRONT_Z),
            (-BODY_W / 2, -HEIGHT / 2 - 0.10, FRONT_Z),
        ],
        tex["bottom"],
    )
    return tex


def add_front_relief_region(
    scene: trimesh.Scene,
    name: str,
    pixel_box: tuple[int, int, int, int],
    front_z: float,
    front_mat: PBRMaterial,
) -> None:
    image_width, image_height = 4096.0, 731.0
    x0, image_y0, x1, image_y1 = pixel_box
    physical_x_min = -OVERALL_W / 2.0 + (x0 / image_width) * OVERALL_W
    physical_x_max = -OVERALL_W / 2.0 + (x1 / image_width) * OVERALL_W
    physical_y_top = HEIGHT / 2.0 - (image_y0 / image_height) * HEIGHT
    physical_y_bottom = HEIGHT / 2.0 - (image_y1 / image_height) * HEIGHT
    u0, u1 = x0 / image_width, x1 / image_width
    v_bottom, v_top = 1.0 - image_y1 / image_height, 1.0 - image_y0 / image_height
    width = physical_x_max - physical_x_min
    height = physical_y_top - physical_y_bottom
    add_box(
        scene,
        f"{name}_Backing",
        (width, height, front_z - FRONT_Z),
        (
            (physical_x_min + physical_x_max) / 2.0,
            (physical_y_bottom + physical_y_top) / 2.0,
            (FRONT_Z + front_z) / 2.0,
        ),
        CHARCOAL,
    )
    add_quad_uv(
        scene,
        f"{name}_Source_Locked_Relief",
        [
            (physical_x_min, physical_y_bottom, front_z + 0.02),
            (physical_x_max, physical_y_bottom, front_z + 0.02),
            (physical_x_max, physical_y_top, front_z + 0.02),
            (physical_x_min, physical_y_top, front_z + 0.02),
        ],
        [(u0, v_bottom), (u1, v_bottom), (u1, v_top), (u0, v_top)],
        front_mat,
    )


def add_front_geometry(scene: trimesh.Scene, front_mat: PBRMaterial) -> None:
    # The black control/mounting ears are front-only, separate mechanical parts.
    ear_width = (OVERALL_W - BODY_W) / 2.0
    for side, x in (
        ("L", -BODY_W / 2 - ear_width / 2),
        ("R", BODY_W / 2 + ear_width / 2),
    ):
        # Front/side walls only: no false rear mounting-ear surface.
        add_open_front_panel(
            scene,
            f"FRONT_Control_Rack_Ear_{side}",
            ear_width,
            HEIGHT,
            1.2,
            x,
            BLACK,
        )

    # Twelve independent source-locked 3.5-inch carriers: 3 rows x 4 columns.
    # A two-pixel inset exposes the original lower seam between adjacent carriers.
    x_edges = (240, 1148, 2056, 2964, 3872)
    y_edges = (0, 244, 488, 731)
    index = 0
    for row in range(3):
        for column in range(4):
            add_front_relief_region(
                scene,
                f"FRONT_LFF_Carrier_{index:02d}_R{row}_C{column}",
                (
                    x_edges[column] + 2,
                    y_edges[row] + 2,
                    x_edges[column + 1] - 2,
                    y_edges[row + 1] - 2,
                ),
                FRONT_Z + 2.0,
                front_mat,
            )
            index += 1

    # Fine control-ear switches, LEDs, Huawei logo and RH2288 V3 badge remain
    # source-photographic detail on the front plane. Adding closed miniature
    # boxes here would expose false control silhouettes in a pure rear view.


def add_slot_cover(
    scene: trimesh.Scene,
    prefix: str,
    width: float,
    height: float,
    x: float,
    y: float,
    z: float,
    vertical: bool = False,
) -> None:
    add_frame(scene, prefix, width, height, x, y, z, -1, 1.2, 1.8, ZINC_DARK)
    if vertical:
        for row in range(6):
            for column in range(2):
                add_box(
                    scene,
                    f"{prefix}_Vent_{row}_{column}",
                    (3.0, 4.0, 1.0),
                    (x + (column - 0.5) * 5.0, y + 13.0 - row * 5.2, z - 1.4),
                    BLACK,
                )
    else:
        vent_count = 12
        for vent in range(vent_count):
            add_box(
                scene,
                f"{prefix}_Vent_{vent:02d}",
                (4.0, 4.5, 1.0),
                (x - 28.0 + vent * (56.0 / (vent_count - 1)), y, z - 1.4),
                BLACK,
            )


def add_rear_relief_region(
    scene: trimesh.Scene,
    name: str,
    pixel_box: tuple[int, int, int, int],
    front_z: float,
    rear_mat: PBRMaterial,
) -> None:
    """Raise one exact-source rear region without replacing photographic pixels."""
    image_width, image_height = 4096.0, 789.0
    x0, y0, x1, y1 = pixel_box
    physical_x_max = BODY_W / 2.0 - (x0 / image_width) * BODY_W
    physical_x_min = BODY_W / 2.0 - (x1 / image_width) * BODY_W
    physical_y_top = HEIGHT / 2.0 - (y0 / image_height) * HEIGHT
    physical_y_bottom = HEIGHT / 2.0 - (y1 / image_height) * HEIGHT
    u0, u1 = x0 / image_width, x1 / image_width
    v0, v1 = 1.0 - y1 / image_height, 1.0 - y0 / image_height
    add_quad_uv(
        scene,
        name,
        [
            (physical_x_max, physical_y_bottom, front_z),
            (physical_x_min, physical_y_bottom, front_z),
            (physical_x_min, physical_y_top, front_z),
            (physical_x_max, physical_y_top, front_z),
        ],
        [(u0, v0), (u1, v0), (u1, v1), (u0, v1)],
        rear_mat,
    )


def add_rear_geometry(scene: trimesh.Scene, rear_mat: PBRMaterial) -> None:
    # Untextured backing geometry remains inside the exact photographic relief
    # surfaces below, avoiding flat icon-like overlays in the final rear view.
    z = REAR_Z + 2.00

    # Screen-left in a straight rear view is +X in the canonical frame.
    for row, y in enumerate((29.0, 8.0, -13.0)):
        add_slot_cover(scene, f"REAR_IO_Module_2_Blank_PCIe_{row}", 96.0, 17.0, 147.0, y, z)
    for row, y in enumerate((29.0, 8.0, -13.0)):
        add_slot_cover(scene, f"REAR_IO_Module_1_Blank_PCIe_{row}", 102.0, 17.0, -47.0, y, z)

    add_slot_cover(scene, "REAR_Onboard_Slot_4_Blank", 19.0, 66.0, 58.0, 4.0, z, True)
    add_slot_cover(scene, "REAR_Onboard_Slot_5_Blank", 19.0, 66.0, 31.0, 4.0, z, True)

    # SM211 flexible NIC: exactly two GE RJ45 ports below I/O module 2.
    for index, x in enumerate((169.0, 137.0), start=1):
        add_box(
            scene,
            f"REAR_SM211_Flexible_NIC_GE{index}_RJ45",
            (20.0, 16.0, 2.3),
            (x, -32.0, z - 1.65),
            BLACK,
        )
        add_box(
            scene,
            f"REAR_SM211_Flexible_NIC_GE{index}_LED",
            (2.0, 2.0, 2.5),
            (x - 6.0, -23.5, z - 1.8),
            GREEN,
        )

    # Standard console/management group: 2x USB, Mgmt, VGA, DB9 and UID.
    for index, x in enumerate((8.0, -12.0), start=1):
        add_box(
            scene,
            f"REAR_USB_3_0_{index}",
            (15.0, 7.0, 2.2),
            (x, -32.0, z - 1.6),
            BLUE,
        )
    add_box(scene, "REAR_Mgmt_RJ45", (20.0, 17.0, 2.3), (-39.0, -32.0, z - 1.65), BLACK)
    add_box(scene, "REAR_VGA", (24.0, 13.0, 2.4), (-72.0, -32.0, z - 1.7), BLUE)
    add_box(scene, "REAR_DB9_Serial", (25.0, 13.0, 2.4), (-106.0, -32.0, z - 1.7), TEAL)
    add_cylinder(scene, "REAR_UID_Button", 2.5, 2.0, (-122.0, -32.0, z - 1.7), (0, 0, 1), GREEN, 18)

    # Two identical WEPW80015 AC PSUs vertically stacked on the same side.
    psu_x = -177.0
    for index, y in enumerate((21.0, -21.0), start=1):
        prefix = f"REAR_AC_PSU_{index}"
        add_frame(scene, f"{prefix}_Module_Frame", 86.0, 39.0, psu_x, y, z, -1, 1.5, 3.0, ZINC_DARK)
        add_box(scene, f"{prefix}_IEC_C14_Inlet", (24.0, 22.0, 3.0), (psu_x - 23.0, y, z - 2.0), BLACK)
        add_box(scene, f"{prefix}_Lime_Ejector", (6.0, 26.0, 4.2), (psu_x - 8.0, y, z - 2.6), GREEN)
        fan_x = psu_x + 22.0
        add_cylinder(scene, f"{prefix}_Fan_Rotor", 14.0, 3.0, (fan_x, y, z - 2.0), (0, 0, 1), BLACK, 32)
        add_cylinder(scene, f"{prefix}_Fan_Hub", 4.0, 3.6, (fan_x, y, z - 2.5), (0, 0, 1), ZINC_DARK, 24)
        for guard in range(4):
            offset = 10.0
            if guard == 0:
                start, end = (fan_x - offset, y - offset, z - 3.6), (fan_x + offset, y + offset, z - 3.6)
            elif guard == 1:
                start, end = (fan_x - offset, y + offset, z - 3.6), (fan_x + offset, y - offset, z - 3.6)
            elif guard == 2:
                start, end = (fan_x - 13.0, y, z - 3.8), (fan_x + 13.0, y, z - 3.8)
            else:
                start, end = (fan_x, y - 13.0, z - 3.8), (fan_x, y + 13.0, z - 3.8)
            add_rod_between(scene, f"{prefix}_Fan_Guard_{guard}", start, end, 0.75, SILVER)
        # Black cord-retainer loop remains true protruding geometry.
        add_box(scene, f"{prefix}_Cord_Loop_Mid", (38.0, 3.0, 4.0), (fan_x, y, z - 6.5), BLACK)
        add_box(scene, f"{prefix}_Cord_Loop_Outer", (3.0, 30.0, 4.0), (fan_x + 18.0, y, z - 6.5), BLACK)

    # Seven non-overlapping source-locked relief regions partition the complete
    # rear. They reuse the approved rear image and UV subranges, so straight rear
    # photography is preserved while major modules sit at their real depth order.
    add_rear_relief_region(scene, "REAR_Relief_IO_Module_2", (0, 0, 1320, 610), REAR_Z - 1.0, rear_mat)
    add_rear_relief_region(scene, "REAR_Relief_SM211", (0, 610, 1320, 789), REAR_Z - 1.7, rear_mat)
    add_rear_relief_region(scene, "REAR_Relief_Onboard_Slots_4_5", (1320, 0, 1850, 789), REAR_Z - 1.1, rear_mat)
    add_rear_relief_region(scene, "REAR_Relief_IO_Module_1", (1850, 0, 3200, 610), REAR_Z - 1.0, rear_mat)
    add_rear_relief_region(scene, "REAR_Relief_Management_Console", (1850, 610, 3200, 789), REAR_Z - 1.7, rear_mat)
    add_rear_relief_region(scene, "REAR_Relief_AC_PSU_1", (3200, 0, 4096, 394), REAR_Z - 3.0, rear_mat)
    add_rear_relief_region(scene, "REAR_Relief_AC_PSU_2", (3200, 394, 4096, 789), REAR_Z - 3.0, rear_mat)


def add_top_relief_region(
    scene: trimesh.Scene,
    name: str,
    pixel_box: tuple[int, int, int, int],
    y: float,
    top_mat: PBRMaterial,
) -> None:
    image_width, image_height = 1836.0, 3072.0
    x0, image_y0, x1, image_y1 = pixel_box
    physical_x_min = -BODY_W / 2.0 + (x0 / image_width) * BODY_W
    physical_x_max = -BODY_W / 2.0 + (x1 / image_width) * BODY_W
    physical_z_min = REAR_Z + (image_y0 / image_height) * DEPTH
    physical_z_max = REAR_Z + (image_y1 / image_height) * DEPTH
    u0, u1 = x0 / image_width, x1 / image_width
    v_top, v_bottom = 1.0 - image_y0 / image_height, 1.0 - image_y1 / image_height
    add_quad_uv(
        scene,
        name,
        [
            (physical_x_max, y, physical_z_min),
            (physical_x_min, y, physical_z_min),
            (physical_x_min, y, physical_z_max),
            (physical_x_max, y, physical_z_max),
        ],
        [(u1, v_top), (u0, v_top), (u0, v_bottom), (u1, v_bottom)],
        top_mat,
    )


def add_side_and_top_geometry(scene: trimesh.Scene, top_mat: PBRMaterial) -> None:
    # Long stamped top rail lips are silhouette-affecting and remain distinct.
    add_box(scene, "LEFT_Upper_Rail_Lip", (3.0, 10.0, 724.0), (-BODY_W / 2 - 0.8, 36.0, 0.0), ZINC)
    add_box(scene, "RIGHT_Upper_Rail_Lip", (3.0, 10.0, 724.0), (BODY_W / 2 + 0.8, 36.0, 0.0), ZINC)

    left_x = -BODY_W / 2 - 1.4
    for index, (y, zc) in enumerate(((-18.0, -284.0), (2.0, -145.0), (18.0, 18.0), (-17.0, 175.0), (15.0, 307.0))):
        add_cylinder(scene, f"LEFT_Panel_Fastener_{index}", 2.0, 1.1, (left_x, y, zc), (1, 0, 0), SILVER)

    right_x = BODY_W / 2 + 1.4
    for index, (y, zc) in enumerate(((17.0, -305.0), (-16.0, -178.0), (1.0, -42.0), (18.0, 104.0), (-17.0, 230.0), (10.0, 326.0))):
        add_cylinder(scene, f"RIGHT_Panel_Fastener_{index}", 2.0, 1.1, (right_x, y, zc), (1, 0, 0), SILVER)

    # Near-flush source-locked latch relief; no synthetic gray overlay is placed
    # over the photographed latch, labels or green release detail.
    add_top_relief_region(
        scene,
        "TOP_Service_Latch_Source_Locked_Relief",
        (820, 1360, 1016, 1910),
        HEIGHT / 2 + 0.22,
        top_mat,
    )


def build_scene(web: bool) -> trimesh.Scene:
    scene = trimesh.Scene(base_frame="Huawei_RH2288V3_H22M03_12LFF_ROOT")
    scene.metadata.update(
        {
            "asset": "Huawei FusionServer RH2288 V3 / H22M-03 12x3.5-inch LFF",
            "configuration": "12 LFF, no rear disks, SM211 2xGE, dual vertically stacked 460 W AC PSU",
            "body_dimensions_mm": [BODY_W, HEIGHT, DEPTH],
            "front_mounting_span_mm": OVERALL_W,
            "coordinate_convention": "+X device-right from front, +Y up, +Z front",
            "bottom_evidence": "GENERIC_BOTTOM_FALLBACK",
        }
    )
    textures = add_textured_shell(scene, web)
    add_front_geometry(scene, textures["front"])
    add_rear_geometry(scene, textures["rear"])
    add_side_and_top_geometry(scene, textures["top"])
    return scene


def mark_face_materials_unlit(path: Path) -> None:
    """Keep source-photograph color stable across independent web viewers."""
    gltf = GLTF2().load_binary(path)
    used = list(gltf.extensionsUsed or [])
    if "KHR_materials_unlit" not in used:
        used.append("KHR_materials_unlit")
    gltf.extensionsUsed = used
    for face_material in gltf.materials:
        if "approved evidence texture" not in (face_material.name or ""):
            continue
        extensions = dict(face_material.extensions or {})
        extensions["KHR_materials_unlit"] = {}
        face_material.extensions = extensions
    gltf.save_binary(path)


def main() -> None:
    MODEL.mkdir(parents=True, exist_ok=True)
    outputs = (
        (False, MODEL / "Huawei-RH2288V3-3.5inch.glb"),
        (True, MODEL / "Huawei-RH2288V3-3.5inch-web.glb"),
    )
    for web, path in outputs:
        scene = build_scene(web)
        path.write_bytes(scene.export(file_type="glb", include_normals=True))
        mark_face_materials_unlit(path)
        print(path, path.stat().st_size, "bytes", len(scene.geometry), "geometry objects")


if __name__ == "__main__":
    main()
