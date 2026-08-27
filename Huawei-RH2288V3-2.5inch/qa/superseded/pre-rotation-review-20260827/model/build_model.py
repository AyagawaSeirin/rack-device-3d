#!/usr/bin/env python3
"""Build the evidence-locked Huawei FusionServer RH2288 V3 24-SFF GLBs.

Right-handed coordinates: +X is device-right from the front, +Y is up,
and +Z points toward the front. Authored dimensions are millimetres.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
from PIL import Image
import trimesh
from trimesh.visual import TextureVisuals
from trimesh.visual.material import PBRMaterial


ROOT = Path(__file__).resolve().parents[1]
VIEWS = ROOT / "views"
MODEL = ROOT / "model"
MM = 0.001

BODY_W = 447.0
OVERALL_W = 482.6
HEIGHT = 86.1
DEPTH = 708.0
FRONT_Z = DEPTH / 2.0
REAR_Z = -DEPTH / 2.0


def material(name: str, rgba: tuple[int, int, int, int], roughness: float = 0.72,
             metallic: float = 0.0) -> PBRMaterial:
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
CHARCOAL = material("Dark drive carrier polymer", (34, 37, 39, 255), 0.82)
GREEN = material("Huawei yellow-green accent", (184, 211, 22, 255), 0.42)
BLUE = material("VGA blue polymer", (30, 105, 208, 255), 0.52)
SILVER = material("Fastener silver", (194, 199, 202, 255), 0.36, 0.58)


def texture_material(face: str, web: bool) -> PBRMaterial:
    image = Image.open(VIEWS / f"{face}.png").convert("RGBA")
    bounds = image.getchannel("A").getbbox()
    if bounds is None:
        raise RuntimeError(f"{face}: empty alpha matte")
    # The texture plane is the physical face itself. Transparent canvas padding
    # belongs only to the elevation deliverable, never to the OPAQUE GLB material.
    image = image.crop(bounds).convert("RGB")
    max_edge = 2048 if web else 4096
    if max(image.size) > max_edge:
        scale = max_edge / max(image.size)
        image = image.resize(
            (max(1, round(image.width * scale)), max(1, round(image.height * scale))),
            Image.Resampling.LANCZOS,
        )
    return PBRMaterial(
        name=f"{face.upper()} evidence-locked texture" + (" WEB" if web else ""),
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


def add_cylinder(scene: trimesh.Scene, name: str, radius: float, length: float,
                 center, axis, mat: PBRMaterial, sections: int = 18) -> None:
    mesh = trimesh.creation.cylinder(radius=radius * MM, height=length * MM, sections=sections)
    direction = np.asarray(axis, dtype=float)
    direction /= np.linalg.norm(direction)
    mesh.apply_transform(trimesh.geometry.align_vectors([0.0, 0.0, 1.0], direction))
    mesh.apply_translation(np.asarray(center, dtype=float) * MM)
    mesh.visual.material = mat
    add(scene, mesh, name)


def add_quad(scene: trimesh.Scene, name: str, vertices_mm, mat: PBRMaterial) -> None:
    vertices = np.asarray(vertices_mm, dtype=float) * MM
    faces = np.asarray([[0, 1, 2], [0, 2, 3]], dtype=int)
    uv = np.asarray([[0.0, 0.0], [1.0, 0.0], [1.0, 1.0], [0.0, 1.0]], dtype=float)
    mesh = trimesh.Trimesh(vertices=vertices, faces=faces, process=False)
    mesh.visual = TextureVisuals(uv=uv, material=mat)
    add(scene, mesh, name)


def add_frame(scene: trimesh.Scene, prefix: str, width: float, height: float,
              center_x: float, center_y: float, z: float, outward: int,
              bar: float, depth: float, mat: PBRMaterial) -> None:
    center_z = z + outward * depth / 2.0
    add_box(scene, f"{prefix}_Top", (width, bar, depth),
            (center_x, center_y + height / 2.0 - bar / 2.0, center_z), mat)
    add_box(scene, f"{prefix}_Bottom", (width, bar, depth),
            (center_x, center_y - height / 2.0 + bar / 2.0, center_z), mat)
    add_box(scene, f"{prefix}_Left", (bar, height - 2 * bar, depth),
            (center_x - width / 2.0 + bar / 2.0, center_y, center_z), mat)
    add_box(scene, f"{prefix}_Right", (bar, height - 2 * bar, depth),
            (center_x + width / 2.0 - bar / 2.0, center_y, center_z), mat)


def add_textured_shell(scene: trimesh.Scene, web: bool) -> None:
    tex = {face: texture_material(face, web) for face in
           ("front", "rear", "left", "right", "top", "bottom")}
    add_box(scene, "Closed_Chassis_Sheet_Metal_447x708x86.1mm",
            (BODY_W, HEIGHT, DEPTH), (0, 0, 0), ZINC)

    add_quad(scene, "Texture_FRONT_24SFF_and_Ears",
             [(-OVERALL_W / 2, -HEIGHT / 2, FRONT_Z + 0.10),
              (OVERALL_W / 2, -HEIGHT / 2, FRONT_Z + 0.10),
              (OVERALL_W / 2, HEIGHT / 2, FRONT_Z + 0.10),
              (-OVERALL_W / 2, HEIGHT / 2, FRONT_Z + 0.10)], tex["front"])
    add_quad(scene, "Texture_REAR_Corrected_No_Rear_Drives",
             [(BODY_W / 2, -HEIGHT / 2, REAR_Z - 0.10),
              (-BODY_W / 2, -HEIGHT / 2, REAR_Z - 0.10),
              (-BODY_W / 2, HEIGHT / 2, REAR_Z - 0.10),
              (BODY_W / 2, HEIGHT / 2, REAR_Z - 0.10)], tex["rear"])
    add_quad(scene, "Texture_LEFT_Independent",
             [(-BODY_W / 2 - 0.10, -HEIGHT / 2, REAR_Z),
              (-BODY_W / 2 - 0.10, -HEIGHT / 2, FRONT_Z),
              (-BODY_W / 2 - 0.10, HEIGHT / 2, FRONT_Z),
              (-BODY_W / 2 - 0.10, HEIGHT / 2, REAR_Z)], tex["left"])
    add_quad(scene, "Texture_RIGHT_Independent",
             [(BODY_W / 2 + 0.10, -HEIGHT / 2, FRONT_Z),
              (BODY_W / 2 + 0.10, -HEIGHT / 2, REAR_Z),
              (BODY_W / 2 + 0.10, HEIGHT / 2, REAR_Z),
              (BODY_W / 2 + 0.10, HEIGHT / 2, FRONT_Z)], tex["right"])
    add_quad(scene, "Texture_TOP_Cover",
             [(BODY_W / 2, HEIGHT / 2 + 0.10, REAR_Z),
              (-BODY_W / 2, HEIGHT / 2 + 0.10, REAR_Z),
              (-BODY_W / 2, HEIGHT / 2 + 0.10, FRONT_Z),
              (BODY_W / 2, HEIGHT / 2 + 0.10, FRONT_Z)], tex["top"])
    add_quad(scene, "Texture_BOTTOM_Generic_Fallback",
             [(-BODY_W / 2, -HEIGHT / 2 - 0.10, REAR_Z),
              (BODY_W / 2, -HEIGHT / 2 - 0.10, REAR_Z),
              (BODY_W / 2, -HEIGHT / 2 - 0.10, FRONT_Z),
              (-BODY_W / 2, -HEIGHT / 2 - 0.10, FRONT_Z)], tex["bottom"])


def add_front_geometry(scene: trimesh.Scene) -> None:
    ear_width = (OVERALL_W - BODY_W) / 2.0
    for side, x in (("L", -BODY_W / 2 - ear_width / 2), ("R", BODY_W / 2 + ear_width / 2)):
        add_box(scene, f"FRONT_Rack_Ear_{side}", (ear_width, HEIGHT, 5.0),
                (x, 0, FRONT_Z - 3.1), BLACK)
        for index, y in enumerate((-27.0, 0.0, 27.0)):
            add_cylinder(scene, f"FRONT_Rack_Ear_{side}_Fastener_{index}", 2.4, 1.2,
                         (x, y, FRONT_Z + 0.8), (0, 0, 1), SILVER)

    bay_pitch = 15.55
    bay_width = 14.75
    first_x = -bay_pitch * 23.0 / 2.0
    for bay in range(24):
        x = first_x + bay * bay_pitch
        add_frame(scene, f"FRONT_Drive_Carrier_{bay:02d}_Frame", bay_width, 69.0,
                  x, -0.5, FRONT_Z + 0.25, 1, 1.15, 1.7, CHARCOAL)
        add_box(scene, f"FRONT_Drive_Carrier_{bay:02d}_Top_Latch", (11.8, 5.2, 2.0),
                (x, 29.0, FRONT_Z + 1.3), CHARCOAL)
        add_box(scene, f"FRONT_Drive_Carrier_{bay:02d}_Green_Status_Strip", (11.6, 1.5, 2.2),
                (x, 23.3, FRONT_Z + 1.45), GREEN)
        add_box(scene, f"FRONT_Drive_Carrier_{bay:02d}_Bottom_Handle", (11.6, 3.0, 2.0),
                (x, -30.4, FRONT_Z + 1.3), CHARCOAL)
        for row in range(3):
            for column in range(2):
                add_box(scene, f"FRONT_Drive_Carrier_{bay:02d}_Vent_{row}_{column}",
                        (3.2, 5.2, 1.0),
                        (x + (column - 0.5) * 4.6, 12.0 - row * 8.0, FRONT_Z + 1.45), BLACK)

    # Operator/control-panel relief from Huawei whitepaper Figure 4-4.
    # Branding remains source-locked in the texture. Physical-left and
    # physical-right controls are intentionally asymmetric and must not be
    # mirrored or copied from the rejected merchant-photo arrangement.
    for side, x in (("L", -OVERALL_W / 2 + 8.5), ("R", OVERALL_W / 2 - 8.5)):
        add_frame(scene, f"FRONT_{side}_Operator_Panel_Bevel", 14.0, 75.0, x, 0,
                  FRONT_Z + 0.35, 1, 1.0, 1.5, CHARCOAL)

    left_x = -OVERALL_W / 2 + 8.5
    right_x = OVERALL_W / 2 - 8.5
    add_box(scene, "FRONT_Left_USB_2_0", (5.0, 10.0, 1.4),
            (left_x, 24.0, FRONT_Z + 1.7), BLACK)
    for index, y in enumerate((10.0, 3.0, -4.0, -11.0), start=1):
        add_box(scene, f"FRONT_Left_Ethernet_Indicator_{index}", (4.0, 2.2, 1.3),
                (left_x, y, FRONT_Z + 1.65), GREEN)

    add_box(scene, "FRONT_Right_Fault_Diagnostic_Display", (8.0, 6.0, 1.4),
            (right_x, 28.0, FRONT_Z + 1.7), BLACK)
    for name, y, mat in (("Health", 18.0, GREEN), ("UID", 10.0, BLUE),
                         ("Power", 2.0, GREEN), ("NMI", -6.0, BLACK)):
        add_box(scene, f"FRONT_Right_{name}_Control", (4.0, 2.4, 1.3),
                (right_x, y, FRONT_Z + 1.65), mat)
    add_box(scene, "FRONT_Right_VGA_Relief", (10.5, 8.0, 1.4),
            (right_x, -19.0, FRONT_Z + 1.7), BLUE)


def add_rear_geometry(scene: trimesh.Scene) -> None:
    z = REAR_Z - 0.30
    outward = -1

    # Rear screen-right corresponds to device-left (-X) in the canonical frame.
    psu_x = -174.0
    for index, y in enumerate((21.0, -21.0)):
        add_frame(scene, f"REAR_AC_PSU_{index}_Frame", 92.0, 39.0, psu_x, y,
                  z, outward, 1.5, 2.2, ZINC_DARK)
        add_box(scene, f"REAR_AC_PSU_{index}_IEC_C14_Inlet", (22.0, 18.0, 2.4),
                (psu_x - 21.0, y, z - 1.6), BLACK)
        add_cylinder(scene, f"REAR_AC_PSU_{index}_Fan", 13.0, 2.2,
                     (psu_x + 21.0, y, z - 1.6), (0, 0, 1), BLACK, 28)
        add_box(scene, f"REAR_AC_PSU_{index}_Ejector_Handle", (5.0, 29.0, 4.2),
                (psu_x + 40.0, y, z - 2.4), CHARCOAL)
        add_box(scene, f"REAR_AC_PSU_{index}_AC_Latch", (5.0, 15.0, 4.2),
                (psu_x - 40.0, y, z - 2.4), GREEN)

    # Six standard PCIe blanks: two independent three-slot banks, no rear drives.
    for bank, x in enumerate((104.0, 22.0)):
        for row, y in enumerate((26.0, 6.0, -14.0)):
            add_frame(scene, f"REAR_PCIe_Bank_{bank}_Slot_{row}", 68.0, 15.5, x, y,
                      z, outward, 1.2, 1.6, ZINC_DARK)
            for vent in range(8):
                add_box(scene, f"REAR_PCIe_Bank_{bank}_Slot_{row}_Vent_{vent}",
                        (4.2, 5.0, 1.0), (x - 25.0 + vent * 7.0, y, z - 1.3), BLACK)

    # Exact two-port flexible NIC plus standard management/USB/VGA/serial cluster.
    for index, x in enumerate((183.0, 153.0)):
        add_box(scene, f"REAR_Flexible_NIC_RJ45_A{index + 1}", (17.0, 15.0, 2.0),
                (x, -31.0, z - 1.5), BLACK)
    for index, x in enumerate((-71.0, -53.0)):
        add_box(scene, f"REAR_USB_{index}", (13.0, 6.0, 2.0),
                (x, -31.0, z - 1.5), BLUE)
    add_box(scene, "REAR_Mgmt_RJ45", (17.0, 15.0, 2.0), (-28.0, -31.0, z - 1.5), BLACK)
    add_box(scene, "REAR_LAN_RJ45", (17.0, 15.0, 2.0), (-5.0, -31.0, z - 1.5), BLACK)
    add_box(scene, "REAR_VGA", (20.0, 10.0, 2.0), (23.0, -31.0, z - 1.5), BLUE)
    add_box(scene, "REAR_DB9_Serial", (21.0, 10.0, 2.0), (52.0, -31.0, z - 1.5), BLACK)


def add_side_and_top_geometry(scene: trimesh.Scene) -> None:
    # Independent left wall. The evidence-locked vent remains in the face texture;
    # duplicating it as a relief grid would create a false second vent at oblique angles.
    left_x = -BODY_W / 2 - 0.6
    for index, (y, zc) in enumerate(((-20.0, -250.0), (0.0, -95.0), (18.0, 70.0),
                                     (-15.0, 195.0), (17.0, 298.0))):
        add_cylinder(scene, f"LEFT_Panel_Fastener_{index}", 2.0, 1.0,
                     (left_x - 0.3, y, zc), (1, 0, 0), SILVER)

    # Independent right wall: intentionally no copied left-side vent.
    right_x = BODY_W / 2 + 0.6
    for index, (y, zc) in enumerate(((18.0, -275.0), (-17.0, -160.0), (2.0, -32.0),
                                     (19.0, 89.0), (-18.0, 212.0), (11.0, 305.0))):
        add_cylinder(scene, f"RIGHT_Panel_Fastener_{index}", 2.0, 1.0,
                     (right_x + 0.3, y, zc), (1, 0, 0), SILVER)

    # Top seam, vent and recessed-latch positions are already source-locked in the
    # photographic top plane. No duplicate relief is layered over those features.


def build_scene(web: bool) -> trimesh.Scene:
    scene = trimesh.Scene(base_frame="Huawei_RH2288V3_H22M03_ROOT")
    scene.metadata.update({
        "asset": "Huawei FusionServer RH2288 V3 / H22M-03 24x2.5-inch",
        "configuration": "24 SFF, no rear drives, dual vertically stacked AC PSU",
        "dimensions_mm": [OVERALL_W, HEIGHT, DEPTH],
        "body_dimensions_mm": [BODY_W, HEIGHT, DEPTH],
        "bottom_evidence": "GENERIC_BOTTOM_FALLBACK",
    })
    add_textured_shell(scene, web)
    add_front_geometry(scene)
    add_rear_geometry(scene)
    add_side_and_top_geometry(scene)
    return scene


def main() -> None:
    MODEL.mkdir(parents=True, exist_ok=True)
    outputs = (
        (False, MODEL / "Huawei-RH2288V3-2.5inch.glb"),
        (True, MODEL / "Huawei-RH2288V3-2.5inch-web.glb"),
    )
    for web, path in outputs:
        scene = build_scene(web)
        path.write_bytes(scene.export(file_type="glb", include_normals=True))
        print(path, path.stat().st_size, "bytes", len(scene.geometry), "geometry objects")


if __name__ == "__main__":
    main()
