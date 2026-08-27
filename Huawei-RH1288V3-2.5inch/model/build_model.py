#!/usr/bin/env python3
"""Build evidence-locked Huawei FusionServer RH1288 V3 H12M-03 GLBs.

Right-handed coordinates: +X is device-right as seen from the front, +Y is up,
and +Z points toward the front. Authored dimensions are millimetres; glTF is metres.
"""

from __future__ import annotations

import logging
from pathlib import Path

import numpy as np
from PIL import Image
import trimesh
from pygltflib import GLTF2
from trimesh.visual import TextureVisuals
from trimesh.visual.material import PBRMaterial


# Trimesh can fall back safely when SciPy is absent, but otherwise emits one
# traceback per small primitive while computing normals.  Keep the reproducible
# build log reserved for actionable export errors.
logging.getLogger("trimesh").setLevel(logging.ERROR)


ROOT = Path(__file__).resolve().parents[1]
VIEWS = ROOT / "views"
MODEL = ROOT / "model"
MM = 0.001

BODY_W = 436.0
OVERALL_W = 482.6
HEIGHT = 43.0
DEPTH = 708.0
SHELL_INSET = 1.0
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


ZINC = material("Galvanized zinc sheet metal", (171, 177, 179, 255), 0.58, 0.16)
ZINC_DARK = material("Galvanized recessed metal", (100, 106, 108, 255), 0.68, 0.10)
BLACK = material("Black grille and connector", (8, 10, 11, 255), 0.86)
CHARCOAL = material("Dark carrier polymer", (28, 31, 32, 255), 0.82)
GREEN = material("Huawei lime-green release accent", (185, 207, 26, 255), 0.44)
BLUE = material("VGA and USB blue polymer", (24, 104, 202, 255), 0.54)
TEAL = material("Serial connector teal polymer", (46, 164, 155, 255), 0.58)
SILVER = material("Fastener silver", (201, 204, 205, 255), 0.38, 0.52)


def texture_material(face: str, web: bool) -> PBRMaterial:
    image = Image.open(VIEWS / f"{face}.png").convert("RGBA")
    bounds = image.getchannel("A").getbbox()
    if bounds is None:
        raise RuntimeError(f"{face}: empty alpha matte")
    # External transparent canvas is not baked into the OPAQUE GLB surface.
    image = image.crop(bounds).convert("RGB")
    max_edge = 2048 if web else 4096
    if max(image.size) > max_edge:
        scale = max_edge / max(image.size)
        image = image.resize(
            (max(1, round(image.width * scale)), max(1, round(image.height * scale))),
            Image.Resampling.LANCZOS,
        )
    return PBRMaterial(
        name=f"{face.upper()} source-locked photo" + (" WEB" if web else ""),
        baseColorFactor=[255, 255, 255, 255],
        baseColorTexture=image,
        metallicFactor=0.0,
        roughnessFactor=0.78,
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
                 center, axis, mat: PBRMaterial, sections: int = 24) -> None:
    mesh = trimesh.creation.cylinder(radius=radius * MM, height=length * MM, sections=sections)
    direction = np.asarray(axis, dtype=float)
    direction /= np.linalg.norm(direction)
    mesh.apply_transform(trimesh.geometry.align_vectors([0.0, 0.0, 1.0], direction))
    mesh.apply_translation(np.asarray(center, dtype=float) * MM)
    mesh.visual.material = mat
    add(scene, mesh, name)


def add_quad(scene: trimesh.Scene, name: str, vertices_mm, mat: PBRMaterial,
             uv_coords=None) -> None:
    vertices = np.asarray(vertices_mm, dtype=float) * MM
    faces = np.asarray([[0, 1, 2], [0, 2, 3]], dtype=int)
    if uv_coords is None:
        uv_coords = [[0.0, 0.0], [1.0, 0.0], [1.0, 1.0], [0.0, 1.0]]
    uv = np.asarray(uv_coords, dtype=float)
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
    # Keep the watertight core 0.5 mm behind each main OPAQUE face. The prior
    # 0.1 mm card-to-shell gap was vulnerable to viewer-dependent depth ties.
    add_box(scene, "Closed_Chassis_436x708x43mm", (BODY_W - SHELL_INSET, HEIGHT - SHELL_INSET, DEPTH - SHELL_INSET), (0, 0, 0), ZINC)

    # Split the front image into a body panel and two separate front-only ear
    # planes.  Single-sided ear planes disappear correctly from the rear camera,
    # unlike solid ear boxes, while retaining the approved source pixels.
    ear_u = ((OVERALL_W - BODY_W) / 2.0) / OVERALL_W
    front_z = FRONT_Z
    add_quad(scene, "Texture_FRONT_8SFF_3over5_Body",
             [(-BODY_W / 2, -HEIGHT / 2, front_z),
              (BODY_W / 2, -HEIGHT / 2, front_z),
              (BODY_W / 2, HEIGHT / 2, front_z),
              (-BODY_W / 2, HEIGHT / 2, front_z)], tex["front"],
             [[ear_u, 0.0], [1.0 - ear_u, 0.0],
              [1.0 - ear_u, 1.0], [ear_u, 1.0]])
    add_quad(scene, "Texture_FRONT_Only_Rack_Ear_L",
             [(-OVERALL_W / 2, -HEIGHT / 2, front_z),
              (-BODY_W / 2, -HEIGHT / 2, front_z),
              (-BODY_W / 2, HEIGHT / 2, front_z),
              (-OVERALL_W / 2, HEIGHT / 2, front_z)], tex["front"],
             [[0.0, 0.0], [ear_u, 0.0], [ear_u, 1.0], [0.0, 1.0]])
    add_quad(scene, "Texture_FRONT_Only_Rack_Ear_R",
             [(BODY_W / 2, -HEIGHT / 2, front_z),
              (OVERALL_W / 2, -HEIGHT / 2, front_z),
              (OVERALL_W / 2, HEIGHT / 2, front_z),
              (BODY_W / 2, HEIGHT / 2, front_z)], tex["front"],
             [[1.0 - ear_u, 0.0], [1.0, 0.0],
              [1.0, 1.0], [1.0 - ear_u, 1.0]])
    # Rear screen-left maps to physical +X, so this winding is both outward and unmirrored.
    add_quad(scene, "Texture_REAR_SM212_4GE_Dual_AC",
             [(BODY_W / 2, -HEIGHT / 2, REAR_Z),
              (-BODY_W / 2, -HEIGHT / 2, REAR_Z),
              (-BODY_W / 2, HEIGHT / 2, REAR_Z),
              (BODY_W / 2, HEIGHT / 2, REAR_Z)], tex["rear"])
    # Physical-left evidence was generated rear-left/front-right for the -X camera.
    add_quad(scene, "Texture_LEFT_Independent_RearLeft_FrontRight",
             [(-BODY_W / 2, -HEIGHT / 2, REAR_Z),
              (-BODY_W / 2, -HEIGHT / 2, FRONT_Z),
              (-BODY_W / 2, HEIGHT / 2, FRONT_Z),
              (-BODY_W / 2, HEIGHT / 2, REAR_Z)], tex["left"])
    # Physical-right evidence was generated front-left/rear-right for the +X camera.
    add_quad(scene, "Texture_RIGHT_Independent_FrontLeft_RearRight",
             [(BODY_W / 2, -HEIGHT / 2, FRONT_Z),
              (BODY_W / 2, -HEIGHT / 2, REAR_Z),
              (BODY_W / 2, HEIGHT / 2, REAR_Z),
              (BODY_W / 2, HEIGHT / 2, FRONT_Z)], tex["right"])
    # Top and bottom assets use front at image bottom, rear at image top.
    add_quad(scene, "Texture_TOP_Closed_Cover",
             [(-BODY_W / 2, HEIGHT / 2, FRONT_Z),
              (BODY_W / 2, HEIGHT / 2, FRONT_Z),
              (BODY_W / 2, HEIGHT / 2, REAR_Z),
              (-BODY_W / 2, HEIGHT / 2, REAR_Z)], tex["top"])
    add_quad(scene, "Texture_BOTTOM_Generic_Fallback",
             [(BODY_W / 2, -HEIGHT / 2, FRONT_Z),
              (-BODY_W / 2, -HEIGHT / 2, FRONT_Z),
              (-BODY_W / 2, -HEIGHT / 2, REAR_Z),
              (BODY_W / 2, -HEIGHT / 2, REAR_Z)], tex["bottom"])


def add_drive_carrier(scene: trimesh.Scene, index: int, x: float, y: float) -> None:
    prefix = f"FRONT_SFF_Carrier_{index}"
    # Carrier frame bodies sit behind the evidence-locked photographic face;
    # only the real ejector/handle relief protrudes and casts parallax.
    add_frame(scene, prefix, 65.0, 18.0, x, y, FRONT_Z - 1.20, 1, 1.3, 1.0, CHARCOAL)
    # Raised right-hand ejector/latch and its verified lime accent create parallax.
    add_box(scene, f"{prefix}_Ejector", (7.0, 13.0, 2.8),
            (x + 27.0, y, FRONT_Z + 1.2), CHARCOAL)
    add_box(scene, f"{prefix}_Lime_Status", (1.4, 13.0, 2.0),
            (x + 22.6, y, FRONT_Z + 1.25), GREEN)
    # The exact silver latch face is already source-locked in the photograph;
    # keep its backing geometry recessed instead of covering it with a box.
    add_box(scene, f"{prefix}_Handle_Lip_Recessed", (6.0, 3.0, 0.4),
            (x - 26.2, y, FRONT_Z - 0.5), SILVER)


def add_front_geometry(scene: trimesh.Scene) -> None:
    # Exact asymmetric eight-bay front: three upper carriers and five lower carriers.
    # Centers are calibrated to the approved 4000 px content crop rather than to
    # a generic evenly filled 1U face.  This preserves Huawei's 3-over-5 layout.
    upper_x = (-150.0, -75.0, -8.0)
    lower_x = (-150.0, -75.0, -8.0, 63.0, 118.0)
    carrier_index = 0
    for x in upper_x:
        add_drive_carrier(scene, carrier_index, x, 10.0)
        carrier_index += 1
    for x in lower_x:
        add_drive_carrier(scene, carrier_index, x, -10.0)
        carrier_index += 1

    # Upper-right DVD and operator block above the two extra lower carriers.
    add_frame(scene, "FRONT_DVD_Drive", 90.0, 13.0, 76.0, 12.0,
              FRONT_Z - 1.15, 1, 1.0, 0.9, CHARCOAL)
    add_box(scene, "FRONT_DVD_Eject_Button", (5.0, 3.0, 2.2),
            (113.0, 12.0, FRONT_Z - 1.4), ZINC_DARK)
    add_box(scene, "FRONT_Fault_Diagnostic_Display", (40.0, 5.0, 2.0),
            (110.0, 4.0, FRONT_Z - 1.4), BLACK)
    for index, x in enumerate((132.0, 142.0, 152.0, 162.0), start=1):
        add_box(scene, f"FRONT_Network_Link_Indicator_{index}", (4.0, 2.0, 2.2),
                (x, 4.0, FRONT_Z - 1.4), GREEN)
    for name, x, mat in (("NMI", 122.0, BLACK), ("Power", 136.0, GREEN), ("UID", 150.0, BLUE)):
        add_cylinder(scene, f"FRONT_{name}_Control", 2.2, 2.0,
                     (x, 12.0, FRONT_Z - 1.4), (0, 0, 1), mat, 18)
    for index, x in enumerate((161.0, 178.0), start=1):
        add_frame(scene, f"FRONT_USB2_{index}", 12.0, 6.0, x, 12.0,
                  FRONT_Z - 1.40, 1, 1.1, 0.6, SILVER)
        add_box(scene, f"FRONT_USB2_{index}_Cavity", (8.0, 3.4, 0.7),
                (x, 12.0, FRONT_Z - 0.55), BLACK)
    # VGA is recessed and centered at the position measured from the approved
    # elevation.  Keeping its blue insert behind the photo prevents the former
    # bright plug-like projection while the texture retains the exact DB15 face.
    add_frame(scene, "FRONT_VGA_DB15", 29.0, 13.0, 160.0, -10.0,
              FRONT_Z - 1.40, 1, 1.2, 0.6, SILVER)
    add_box(scene, "FRONT_VGA_DB15_Blue", (21.0, 7.5, 0.5),
            (160.0, -10.0, FRONT_Z - 0.55), BLUE)


def add_rj45(scene: trimesh.Scene, name: str, x: float, y: float, z: float) -> None:
    add_frame(scene, name, 17.0, 13.5, x, y, z, -1, 1.1, 2.4, SILVER)
    add_box(scene, f"{name}_Cavity", (12.2, 8.5, 2.6), (x, y - 1.0, z - 1.7), BLACK)
    add_box(scene, f"{name}_Green_LED", (2.2, 1.5, 2.7), (x - 5.0, y + 5.0, z - 1.8), GREEN)


def add_rear_geometry(scene: trimesh.Scene) -> None:
    # Recessed rear frames start on the chassis-interior side of the photographic
    # rear plane.  On -Z, more-negative is outward; the previous sign put dark
    # fan/port recesses in front of the source texture.
    z = REAR_Z + 3.50
    # Two independent PCIe blank panels and dense real vent relief.
    for label, x, width in (("FullHeight", 147.0, 120.0), ("HalfHeight", 22.0, 110.0)):
        add_frame(scene, f"REAR_PCIe_{label}_Blank", width, 16.5, x, 10.0,
                  z, -1, 1.2, 2.0, ZINC_DARK)
        for vent in range(max(7, int(width // 7))):
            vx = x - width / 2 + 5.0 + vent * 7.0
            if vx < x + width / 2 - 4.0:
                add_box(scene, f"REAR_PCIe_{label}_Vent_{vent}", (3.3, 7.0, 1.5),
                        (vx, 10.0, z - 1.3), BLACK)

    # Requested SM212-visible four-GE FlexIO face at rear screen-left / physical +X.
    for index, x in enumerate((179.0, 161.0, 144.0, 126.0), start=1):
        add_rj45(scene, f"REAR_SM212_GE_RJ45_{index}", x, -10.0, z)
    add_rj45(scene, "REAR_Mgmt_RJ45", 93.0, -10.0, z)
    for index, x in enumerate((64.0, 43.0), start=1):
        add_frame(scene, f"REAR_USB3_{index}", 13.0, 7.0, x, -10.0,
                  z, -1, 1.0, 2.2, SILVER)
        add_box(scene, f"REAR_USB3_{index}_Blue", (9.0, 3.8, 2.5),
                (x, -10.0, z - 1.7), BLUE)
    add_frame(scene, "REAR_VGA_DB15", 29.0, 14.0, 19.0, -10.0,
              z, -1, 1.2, 2.3, SILVER)
    add_box(scene, "REAR_VGA_DB15_Blue", (21.0, 8.0, 2.6),
            (19.0, -10.0, z + 0.4), BLUE)
    add_frame(scene, "REAR_Serial_DSub", 29.0, 14.0, -15.0, -10.0,
              z, -1, 1.2, 2.3, SILVER)
    add_box(scene, "REAR_Serial_DSub_Teal", (21.0, 8.0, 2.6),
            (-15.0, -10.0, z + 0.4), TEAL)
    add_cylinder(scene, "REAR_UID_Indicator", 2.0, 1.8,
                 (91.0, 8.0, REAR_Z + 1.4), (0, 0, 1), BLUE, 18)

    # Two horizontally adjacent 750 W AC hot-swap PSUs at physical -X (rear screen-right).
    for index, x in enumerate((-82.0, -165.0), start=1):
        prefix = f"REAR_AC_PSU_{index}_750W"
        add_frame(scene, prefix, 77.0, 39.0, x, 0.0, z, -1, 1.4, 2.6, ZINC_DARK)
        fan_x = x + 18.0
        inlet_x = x - 21.0
        add_cylinder(scene, f"{prefix}_Fan_Recess", 14.5, 1.0,
                     (fan_x, 0.0, REAR_Z + 1.0), (0, 0, 1), BLACK, 32)
        add_box(scene, f"{prefix}_Fan_Protective_Handle", (29.0, 3.5, 2.2),
                (fan_x, -1.0, REAR_Z - 1.0), CHARCOAL)
        for sx in (-13.0, 13.0):
            for sy in (-13.0, 13.0):
                add_cylinder(scene, f"{prefix}_Fastener_{sx}_{sy}", 1.7, 1.6,
                             (fan_x + sx, sy, REAR_Z + 1.4), (0, 0, 1), SILVER, 16)
        add_frame(scene, f"{prefix}_IEC_C14", 22.0, 23.0, inlet_x, 0.0,
                  z, -1, 1.4, 3.0, SILVER)
        add_box(scene, f"{prefix}_IEC_C14_Cavity", (15.0, 16.0, 3.2),
                (inlet_x, 0.0, REAR_Z + 1.8), BLACK)
        add_box(scene, f"{prefix}_Lime_Release", (4.5, 20.0, 5.5),
                (inlet_x - 14.0, 0.0, REAR_Z - 2.35), GREEN)
        add_cylinder(scene, f"{prefix}_Green_Indicator", 2.4, 2.0,
                     (x + 32.0, 13.0, REAR_Z + 1.4), (0, 0, 1), GREEN, 18)


def add_side_geometry(scene: trimesh.Scene) -> None:
    # Physical-left: independent pin/slot pattern, no right-side vent or dark rail strip.
    left_x = -BODY_W / 2 - 0.65
    for index, (y, zc) in enumerate(((-4.0, -292.0), (-4.0, -160.0), (-3.0, 10.0),
                                     (-4.0, 150.0), (-4.0, 286.0))):
        add_cylinder(scene, f"LEFT_Rail_Attachment_Pin_{index}", 2.5, 1.5,
                     (left_x - 0.4, y, zc), (-1, 0, 0), SILVER, 20)
    add_box(scene, "LEFT_Rail_Rectangular_Slot", (1.7, 6.0, 34.0),
            (left_x - 0.5, -2.0, 122.0), BLACK)

    # Physical-right: verified long lower rail channel and one rear honeycomb vent.
    right_x = BODY_W / 2 + 0.65
    add_box(scene, "RIGHT_Long_Rail_Channel", (1.7, 4.5, 560.0),
            (right_x + 0.45, -16.0, 20.0), ZINC_DARK)
    for index, (y, zc) in enumerate(((-3.0, -295.0), (-4.0, -70.0), (-3.0, 170.0),
                                     (-4.0, 300.0))):
        add_cylinder(scene, f"RIGHT_Rail_Attachment_Pin_{index}", 2.4, 1.5,
                     (right_x + 0.4, y, zc), (1, 0, 0), SILVER, 20)
    add_box(scene, "RIGHT_Rear_Side_Vent_Recess", (1.8, 15.5, 112.0),
            (right_x + 0.5, 0.0, -260.0), BLACK)
    for row in range(3):
        for col in range(15):
            add_box(scene, f"RIGHT_Rear_Side_Vent_Cell_{row}_{col}", (2.0, 2.0, 4.2),
                    (right_x + 1.6, -5.0 + row * 5.0, -309.0 + col * 7.0), ZINC_DARK)


def add_top_bottom_geometry(scene: trimesh.Scene) -> None:
    # The real handle is recessed and nearly flush; keep all relief inside a
    # sub-millimetre visible envelope instead of creating a false 50 mm height.
    top_y = HEIGHT / 2 + 0.12
    # Two long evidence-backed cover breaks; they are recesses, not open vents.
    for name, zc in (("Front_Service_Lid_Seam", 268.0), ("Rear_Cover_Seam", -244.0)):
        add_box(scene, f"TOP_{name}", (392.0, 0.22, 1.8), (0.0, top_y, zc), ZINC_DARK)

    # Recessed center release pocket and narrow raised handle, calibrated to the
    # approved top view.  The recess stays below the photographic surface so it
    # cannot create the former broad double-frame artifact.
    add_box(scene, "TOP_Cover_Latch_Recess", (22.0, 0.25, 48.0),
            (0.0, HEIGHT / 2 - 0.18, 54.0), ZINC_DARK)
    for label, extents, center in (
        ("Left", (2.0, 0.18, 42.0), (-8.0, top_y + 0.09, 54.0)),
        ("Right", (2.0, 0.18, 42.0), (8.0, top_y + 0.09, 54.0)),
        ("Front", (18.0, 0.18, 2.0), (0.0, top_y + 0.09, 74.0)),
        ("Rear", (18.0, 0.18, 2.0), (0.0, top_y + 0.09, 34.0)),
    ):
        add_box(scene, f"TOP_Cover_Latch_Frame_{label}", extents, center, SILVER)
    add_box(scene, "TOP_Cover_Latch_Flip_Handle", (12.0, 0.18, 30.0),
            (0.0, top_y + 0.09, 54.0), ZINC)

    # Conservative bottom retains only perimeter fold relief proven by side silhouettes.
    bottom_y = -HEIGHT / 2 - 0.12
    for side, x in (("L", -BODY_W / 2 + 2.0), ("R", BODY_W / 2 - 2.0)):
        add_box(scene, f"BOTTOM_Verified_Folded_Edge_{side}", (3.0, 0.22, DEPTH - 4.0),
                (x, bottom_y, 0.0), ZINC_DARK)


def build_scene(web: bool) -> trimesh.Scene:
    scene = trimesh.Scene(base_frame="Huawei_RH1288V3_H12M03_ROOT")
    scene.metadata.update({
        "asset": "Huawei FusionServer RH1288 V3 / H12M-03 / 8x2.5-inch SFF",
        "configuration": "3-over-5 eight-carrier front; SM212 4GE; dual 750W AC PSU",
        "published_body_dimensions_mm": [BODY_W, HEIGHT, DEPTH],
        "rack_span_mm": OVERALL_W,
        "bottom_evidence": "GENERIC_BOTTOM_FALLBACK",
        "coordinate_convention": "+X device-right from front; +Y up; +Z front",
        "variant_exclusions": "RH1288H; V5/V6/V7; 3.5-inch; 10GE/IB; DC/HVDC",
    })
    add_textured_shell(scene, web)
    add_front_geometry(scene)
    add_rear_geometry(scene)
    add_side_geometry(scene)
    add_top_bottom_geometry(scene)
    return scene


def patch_source_locked_unlit(path: Path) -> None:
    """Keep photo-derived main faces identical under independent viewers."""
    document = GLTF2().load_binary(str(path))
    used = list(document.extensionsUsed or [])
    if "KHR_materials_unlit" not in used:
        used.append("KHR_materials_unlit")
    document.extensionsUsed = used
    for gltf_material in document.materials or []:
        if gltf_material.name and "source-locked photo" in gltf_material.name:
            extensions = dict(gltf_material.extensions or {})
            extensions["KHR_materials_unlit"] = {}
            gltf_material.extensions = extensions
            gltf_material.alphaMode = "OPAQUE"
            gltf_material.doubleSided = False
            if gltf_material.pbrMetallicRoughness:
                gltf_material.pbrMetallicRoughness.baseColorFactor = [1.0, 1.0, 1.0, 1.0]
    document.save_binary(str(path))


def main() -> None:
    MODEL.mkdir(parents=True, exist_ok=True)
    outputs = (
        (False, MODEL / "Huawei-RH1288V3-2.5inch.glb"),
        (True, MODEL / "Huawei-RH1288V3-2.5inch-web.glb"),
    )
    for web, path in outputs:
        scene = build_scene(web)
        path.write_bytes(scene.export(file_type="glb", include_normals=True))
        patch_source_locked_unlit(path)
        print(path, path.stat().st_size, "bytes", len(scene.geometry), "geometry objects")


if __name__ == "__main__":
    main()
