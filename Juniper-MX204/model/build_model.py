#!/usr/bin/env python3
"""Build the newly constructed exact-exterior Juniper MX204 GLBs.

Coordinate convention: +X device right from the front, +Y up, +Z front.
All authored dimensions below are millimetres and converted to glTF metres.
"""

from __future__ import annotations

from pathlib import Path
import math

import numpy as np
from PIL import Image
import trimesh
from pygltflib import GLTF2, Sampler
from trimesh.visual import TextureVisuals
from trimesh.visual.material import PBRMaterial
from shapely.geometry import Point, box
from shapely.ops import unary_union


ROOT = Path(__file__).resolve().parents[1]
VIEWS = ROOT / "views"
MODEL = ROOT / "model"

MM = 0.001
BODY_W = 447.0
OVERALL_W = 482.6
HEIGHT = 43.7
BODY_D = 470.0
OVERALL_D = 518.9
FRONT_Z = BODY_D / 2.0
REAR_Z = -BODY_D / 2.0
REAR_EXTREME_Z = FRONT_Z - OVERALL_D


def mat(name: str, rgba: tuple[int, int, int, int], roughness: float = 0.72,
        metallic: float = 0.0) -> PBRMaterial:
    return PBRMaterial(
        name=name,
        baseColorFactor=list(rgba),
        metallicFactor=metallic,
        roughnessFactor=roughness,
        alphaMode="OPAQUE",
        doubleSided=False,
    )


GRAY = mat("MX204 dark gray powder-coated steel", (83, 88, 92, 255), 0.78)
GRAY_LIGHT = mat("Galvanized mounting hardware", (150, 158, 162, 255), 0.48, 0.22)
GRAY_DARK = mat("Dark recessed metal", (45, 49, 52, 255), 0.82)
BLACK = mat("Connector and grille black", (10, 12, 13, 255), 0.88)
ORANGE = mat("Juniper AFO orange handle", (239, 77, 14, 255), 0.56)
GOLD = mat("Timing connector gold", (190, 126, 27, 255), 0.35, 0.58)
GREEN = mat("Status LED green", (27, 176, 75, 255), 0.30)
AMBER = mat("Status LED amber", (230, 148, 20, 255), 0.30)
SILVER = mat("Fastener silver", (190, 195, 198, 255), 0.32, 0.62)


def flatten_face(image: Image.Image) -> Image.Image:
    """Embed RGB only; external canvas alpha must never affect GLB surfaces."""
    rgba = image.convert("RGBA")
    background = Image.new("RGBA", rgba.size, (83, 88, 92, 255))
    background.alpha_composite(rgba)
    return background.convert("RGB")


def downscale(image: Image.Image, max_edge: int | None) -> Image.Image:
    rgb = flatten_face(image)
    if max_edge is None or max(rgb.size) <= max_edge:
        return rgb
    scale = max_edge / max(rgb.size)
    return rgb.resize((max(1, round(rgb.width * scale)),
                       max(1, round(rgb.height * scale))), Image.Resampling.LANCZOS)


def texture_material(face: str, web: bool) -> PBRMaterial:
    image = downscale(Image.open(VIEWS / f"{face}.png"), 2048 if web else None)
    return PBRMaterial(
        name=f"{face.upper()} source-locked photographic texture" + (" WEB" if web else ""),
        baseColorFactor=[1.0, 1.0, 1.0, 1.0],
        baseColorTexture=image,
        metallicFactor=0.0,
        roughnessFactor=0.76,
        alphaMode="OPAQUE",
        doubleSided=False,
    )


def add(scene: trimesh.Scene, geometry: trimesh.Trimesh, name: str) -> None:
    geometry.metadata["name"] = name
    scene.add_geometry(geometry, node_name=name, geom_name=name)


def add_box(scene: trimesh.Scene, name: str, extents_mm, center_mm, material: PBRMaterial) -> None:
    mesh = trimesh.creation.box(extents=np.asarray(extents_mm, dtype=float) * MM)
    mesh.apply_translation(np.asarray(center_mm, dtype=float) * MM)
    mesh.visual.material = material
    add(scene, mesh, name)


def add_cylinder(scene: trimesh.Scene, name: str, radius_mm: float, length_mm: float,
                 center_mm, axis, material: PBRMaterial, sections: int = 24) -> None:
    mesh = trimesh.creation.cylinder(radius=radius_mm * MM, height=length_mm * MM, sections=sections)
    axis = np.asarray(axis, dtype=float)
    axis /= np.linalg.norm(axis)
    transform = trimesh.geometry.align_vectors([0.0, 0.0, 1.0], axis)
    mesh.apply_transform(transform)
    mesh.apply_translation(np.asarray(center_mm, dtype=float) * MM)
    mesh.visual.material = material
    add(scene, mesh, name)


def add_cylinder_between(scene: trimesh.Scene, name: str, a_mm, b_mm,
                         radius_mm: float, material: PBRMaterial, sections: int = 20) -> None:
    a = np.asarray(a_mm, dtype=float)
    b = np.asarray(b_mm, dtype=float)
    delta = b - a
    add_cylinder(scene, name, radius_mm, float(np.linalg.norm(delta)), (a + b) / 2.0,
                 delta, material, sections)


def rounded_rect(x0, y0, x1, y1, radius):
    core_h = box(x0 + radius, y0, x1 - radius, y1)
    core_v = box(x0, y0 + radius, x1, y1 - radius)
    corners = [Point(x, y).buffer(radius, resolution=8)
               for x in (x0 + radius, x1 - radius)
               for y in (y0 + radius, y1 - radius)]
    return unary_union([core_h, core_v, *corners])


def ear_mesh(front: bool, left: bool) -> trimesh.Trimesh:
    width = (OVERALL_W - BODY_W) / 2.0
    outer = box(-width / 2.0, -HEIGHT / 2.0, width / 2.0, HEIGHT / 2.0)
    holes = []
    for cy in (-11.0, 11.0):
        holes.append(rounded_rect(-5.2, cy - 4.4, 5.2, cy + 4.4, 2.0))
    plate = outer.difference(unary_union(holes))
    mesh = trimesh.creation.extrude_polygon(plate, height=2.0, engine="earcut")
    mesh.apply_scale(MM)
    side = -1.0 if left else 1.0
    x = side * (BODY_W / 2.0 + width / 2.0)
    z = FRONT_Z - 2.0 if front else REAR_Z
    mesh.apply_translation([x * MM, 0.0, z * MM])
    mesh.visual.material = GRAY_LIGHT if front else GRAY_DARK
    return mesh


def fan_frame_mesh(x_mm: float, center_z_mm: float) -> trimesh.Trimesh:
    outer = rounded_rect(-21.0, -18.5, 21.0, 18.5, 5.0)
    inner = rounded_rect(-18.2, -15.7, 18.2, 15.7, 3.8)
    frame = outer.difference(inner)
    mesh = trimesh.creation.extrude_polygon(frame, height=10.0, engine="earcut")
    mesh.apply_scale(MM)
    mesh.apply_translation([x_mm * MM, 0.0, (center_z_mm - 5.0) * MM])
    mesh.visual.material = ORANGE
    return mesh


def add_quad(scene: trimesh.Scene, name: str, vertices_mm, material: PBRMaterial,
             uv_bounds=(0.0, 0.0, 1.0, 1.0)) -> None:
    vertices = np.asarray(vertices_mm, dtype=float) * MM
    faces = np.asarray([[0, 1, 2], [0, 2, 3]], dtype=int)
    u0, v0, u1, v1 = uv_bounds
    # Vertex order is bottom-left, bottom-right, top-right, top-left as seen
    # from the outward-facing canonical camera. glTF image origin is top-left.
    uv = np.asarray([[u0, v0], [u1, v0], [u1, v1], [u0, v1]], dtype=float)
    mesh = trimesh.Trimesh(vertices=vertices, faces=faces, process=False)
    mesh.visual = TextureVisuals(uv=uv, material=material)
    add(scene, mesh, name)


def build_scene(web: bool) -> trimesh.Scene:
    scene = trimesh.Scene(base_frame="MX204_ROOT")

    # Closed load-bearing chassis shell.
    add_box(scene, "Chassis_Closed_Sheet_Metal", (BODY_W, HEIGHT, BODY_D), (0, 0, 0), GRAY)

    # Canonical source-locked photographic face planes. Front/rear ears and all
    # protruding hardware remain separate geometry outside the textured body.
    tex = {face: texture_material(face, web) for face in ("front", "rear", "left", "right", "top", "bottom")}
    add_quad(scene, "Texture_FRONT_Body",
             [(-BODY_W/2, -HEIGHT/2, FRONT_Z+0.08), (BODY_W/2, -HEIGHT/2, FRONT_Z+0.08),
              (BODY_W/2, HEIGHT/2, FRONT_Z+0.08), (-BODY_W/2, HEIGHT/2, FRONT_Z+0.08)],
             tex["front"], (0.039, 0.021, 0.961, 0.979))
    add_quad(scene, "Texture_REAR_Body",
             [(BODY_W/2, -HEIGHT/2, REAR_Z-0.08), (-BODY_W/2, -HEIGHT/2, REAR_Z-0.08),
              (-BODY_W/2, HEIGHT/2, REAR_Z-0.08), (BODY_W/2, HEIGHT/2, REAR_Z-0.08)],
             tex["rear"], (0.039, 0.021, 0.961, 0.979))
    add_quad(scene, "Texture_LEFT_Body",
             [(-BODY_W/2-0.08, -HEIGHT/2, REAR_Z), (-BODY_W/2-0.08, -HEIGHT/2, FRONT_Z),
              (-BODY_W/2-0.08, HEIGHT/2, FRONT_Z), (-BODY_W/2-0.08, HEIGHT/2, REAR_Z)],
             tex["left"], (0.002, 0.032, 0.998, 0.980))
    add_quad(scene, "Texture_RIGHT_Body",
             [(BODY_W/2+0.08, -HEIGHT/2, FRONT_Z), (BODY_W/2+0.08, -HEIGHT/2, REAR_Z),
              (BODY_W/2+0.08, HEIGHT/2, REAR_Z), (BODY_W/2+0.08, HEIGHT/2, FRONT_Z)],
             tex["right"], (0.002, 0.032, 0.998, 0.980))
    add_quad(scene, "Texture_TOP_Cover",
             [(BODY_W/2, HEIGHT/2+0.08, REAR_Z), (-BODY_W/2, HEIGHT/2+0.08, REAR_Z),
              (-BODY_W/2, HEIGHT/2+0.08, FRONT_Z), (BODY_W/2, HEIGHT/2+0.08, FRONT_Z)],
             tex["top"], (0.004, 0.004, 0.996, 0.996))
    add_quad(scene, "Texture_BOTTOM_Fallback",
             [(-BODY_W/2, -HEIGHT/2-0.08, REAR_Z), (BODY_W/2, -HEIGHT/2-0.08, REAR_Z),
              (BODY_W/2, -HEIGHT/2-0.08, FRONT_Z), (-BODY_W/2, -HEIGHT/2-0.08, FRONT_Z)],
             tex["bottom"], (0.004, 0.004, 0.996, 0.996))

    # Front and screenshot-matched rear mounting flanges: separate real through-hole meshes.
    for front, label in ((True, "FRONT"), (False, "REAR")):
        for left, side in ((True, "L"), (False, "R")):
            mesh = ear_mesh(front, left)
            add(scene, mesh, f"{label}_Mounting_Flange_{side}_Two_Rounded_Holes")

    # Front bracket attachment screws (three per side).
    for side, x in (("L", -BODY_W/2-3.2), ("R", BODY_W/2+3.2)):
        for idx, y in enumerate((-15.0, 0.0, 15.0)):
            add_cylinder(scene, f"FRONT_Ear_{side}_Attachment_Screw_{idx}", 3.1, 1.4,
                         (x, y, FRONT_Z), (0, 0, 1), SILVER)

    # Front identity-bearing port relief. All blocks terminate at or behind the front plane.
    for i, x in enumerate((-155.0, -134.0, -113.0, -92.0)):
        add_box(scene, f"FRONT_QSFP28_Port_{i}", (16.0, 11.5, 4.0), (x, -6.0, FRONT_Z-5.0), BLACK)
    sfp_x = (-51.0, -34.0, -17.0, 0.0)
    number = 4
    for row, y in enumerate((4.8, -5.2)):
        for col, x in enumerate(sfp_x):
            add_box(scene, f"FRONT_SFPplus_Port_{number}", (13.5, 7.0, 4.0), (x, y, FRONT_Z-5.0), BLACK)
            number += 2
        number = 5
    for label, x in zip(("MGMT", "BITS", "CON", "ToD"), (72.0, 104.0, 135.0, 164.0)):
        add_box(scene, f"FRONT_RJ45_{label}", (14.0, 14.5, 4.0), (x, -2.0, FRONT_Z-5.0), BLACK)
    add_box(scene, "FRONT_USB_Type_A", (6.3, 17.0, 4.0), (181.0, -2.0, FRONT_Z-5.0), BLACK)
    for idx, (x, y) in enumerate(((194.0, 5.0), (205.0, 5.0), (194.0, -6.0), (205.0, -6.0))):
        add_cylinder(scene, f"FRONT_Timing_DIN_Connector_{idx}", 3.5, 3.0,
                     (x, y, FRONT_Z-4.0), (0, 0, 1), GOLD)
    add_box(scene, "FRONT_GM_PTP_Port", (15.0, 14.0, 4.0), (-197.0, -7.0, FRONT_Z-5.0), BLACK)
    add_cylinder(scene, "FRONT_ESD_Point", 2.2, 1.4, (-215.0, -7.0, FRONT_Z-4.0), (0, 0, 1), SILVER)
    for idx, x in enumerate(np.linspace(174.0, 217.0, 7)):
        add_cylinder(scene, f"FRONT_Status_LED_or_Button_{idx}", 1.25, 1.0,
                     (float(x), -13.5, FRONT_Z-4.0), (0, 0, 1), GREEN if idx < 5 else AMBER)

    # Rear grounding block, three fan modules, center panel, and two AC PSUs.
    add_box(scene, "REAR_Grounding_ESD_Panel", (90.0, 41.0, 3.0), (178.5, 0, REAR_Z+3.0), GRAY_DARK)
    for idx, x in enumerate((190.0, 175.0)):
        add_cylinder(scene, f"REAR_Grounding_Stud_{idx}", 3.0, 1.2, (x, 3.0, REAR_Z+2.0),
                     (0, 0, -1), SILVER)
    add_cylinder(scene, "REAR_ESD_Point", 2.2, 1.0, (146.0, -8.0, REAR_Z+2.0), (0, 0, -1), SILVER)

    for idx, x in enumerate((108.0, 58.0, 8.0)):
        add_box(scene, f"REAR_Fan_Module_{idx}_Housing", (48.0, 41.0, 4.0), (x, 0, REAR_Z+3.0), BLACK)
        z_handle = REAR_EXTREME_Z + 5.0
        add(scene, fan_frame_mesh(x, z_handle), f"REAR_Fan_{idx}_Rounded_Orange_Handle_Frame")
        arm_length = REAR_Z - z_handle
        arm_center = (REAR_Z + z_handle) / 2.0
        add_box(scene, f"REAR_Fan_{idx}_Handle_Connector_L", (4.0, 8.0, arm_length),
                (x-18.0, 0, arm_center), ORANGE)
        add_box(scene, f"REAR_Fan_{idx}_Handle_Connector_R", (4.0, 8.0, arm_length),
                (x+18.0, 0, arm_center), ORANGE)
        add_box(scene, f"REAR_Fan_{idx}_AIR_OUT_Latch", (26.0, 3.5, 8.0), (x, 0, z_handle+1.0), ORANGE)
        add_cylinder(scene, f"REAR_Fan_{idx}_Captive_Screw", 2.2, 2.0,
                     (x+18.0, 16.0, REAR_Z+2.0), (0, 0, -1), SILVER)

    add_box(scene, "REAR_Fixed_Central_Panel", (71.0, 41.0, 3.0), (-51.5, 0, REAR_Z+3.0), GRAY_DARK)

    for idx, x in enumerate((-137.2, -199.8)):
        add_box(scene, f"REAR_AC_PSU_{idx}_Housing", (56.6, 40.1, 4.0), (x, 0, REAR_Z+3.0), GRAY_DARK)
        add_box(scene, f"REAR_AC_PSU_{idx}_IEC_C14_Inlet", (18.0, 18.0, 2.0), (x-5.0, 0, REAR_Z+2.5), BLACK)
        add_box(scene, f"REAR_AC_PSU_{idx}_Status_Grille", (8.0, 31.0, 2.0), (x+21.0, 0, REAR_Z+2.5), BLACK)
        add_cylinder(scene, f"REAR_AC_PSU_{idx}_LED_Green", 1.5, 1.0,
                     (x+21.0, 6.0, REAR_Z+1.8), (0, 0, -1), GREEN)
        add_cylinder(scene, f"REAR_AC_PSU_{idx}_LED_Amber", 1.5, 1.0,
                     (x+21.0, -7.0, REAR_Z+1.8), (0, 0, -1), AMBER)
        z_handle = REAR_EXTREME_Z + 5.0
        add_box(scene, f"REAR_AC_PSU_{idx}_Orange_Handle", (5.2, 34.0, 10.0),
                (x+7.5, 0, z_handle), ORANGE)
        add_box(scene, f"REAR_AC_PSU_{idx}_Black_Ejector", (5.0, 29.0, 10.0),
                (x-21.0, -2.0, z_handle), BLACK)
        arm_length = REAR_Z - z_handle
        arm_center = (REAR_Z + z_handle) / 2.0
        for arm_idx, y in enumerate((-13.0, 13.0)):
            add_box(scene, f"REAR_AC_PSU_{idx}_Orange_Handle_Connector_{arm_idx}",
                    (5.2, 5.0, arm_length), (x+7.5, y, arm_center), ORANGE)
        for arm_idx, y in enumerate((-11.0, 9.0)):
            add_box(scene, f"REAR_AC_PSU_{idx}_Black_Ejector_Connector_{arm_idx}",
                    (5.0, 5.0, arm_length), (x-21.0, y, arm_center), BLACK)
        # Silver cord-retainer loop, visible and projecting.
        loop_z = REAR_EXTREME_Z + 1.6
        add_cylinder_between(scene, f"REAR_AC_PSU_{idx}_Cord_Loop_L", (x-9.5, -8.0, loop_z),
                             (x-9.5, 8.0, loop_z), 1.4, SILVER)
        add_cylinder_between(scene, f"REAR_AC_PSU_{idx}_Cord_Loop_R", (x+2.5, -8.0, loop_z),
                             (x+2.5, 8.0, loop_z), 1.4, SILVER)
        add_cylinder_between(scene, f"REAR_AC_PSU_{idx}_Cord_Loop_T", (x-9.5, 8.0, loop_z),
                             (x+2.5, 8.0, loop_z), 1.4, SILVER)

    # Paired three-section side mounting rails and relief.
    for side, x, outward in (("LEFT", -BODY_W/2-0.9, -1), ("RIGHT", BODY_W/2+0.9, 1)):
        add_box(scene, f"{side}_Mounting_Rail_Base", (1.8, 36.0, 410.0), (x, 0, 0), GRAY_LIGHT)
        for idx, z in enumerate((-137.0, 0.0, 137.0)):
            add_box(scene, f"{side}_Rail_Section_{idx}_Top", (2.1, 2.8, 116.0),
                    (x+outward*1.1, 13.0, z), GRAY_LIGHT)
            add_box(scene, f"{side}_Rail_Section_{idx}_Bottom", (2.1, 2.8, 116.0),
                    (x+outward*1.1, -13.0, z), GRAY_LIGHT)
            add_box(scene, f"{side}_Rail_Section_{idx}_Front_End", (2.1, 26.0, 2.8),
                    (x+outward*1.1, 0, z+58.0), GRAY_LIGHT)
            add_box(scene, f"{side}_Rail_Section_{idx}_Rear_End", (2.1, 26.0, 2.8),
                    (x+outward*1.1, 0, z-58.0), GRAY_LIGHT)
        for idx, (y, z) in enumerate(((10.0, -68.5), (-10.0, -68.5), (10.0, 68.5), (-10.0, 68.5))):
            add_cylinder(scene, f"{side}_Rail_Fastener_{idx}", 2.5, 1.5,
                         (x+outward*2.0, y, z), (outward, 0, 0), SILVER)

    # Top stamped channel, screw heads, and empty front-edge mounting holes.
    add_box(scene, "TOP_Long_Raised_Channel", (420.0, 0.7, 8.0), (0, HEIGHT/2-0.35, 185.0), GRAY)
    top_screws = []
    top_screws.extend((x, 219.0) for x in (-216.0, -108.0, 0.0, 108.0, 216.0))
    top_screws.extend((x, z) for z in (105.0, 55.0, 5.0) for x in (65.0, 140.0, 210.0))
    top_screws.extend((x, -222.0) for x in np.linspace(-215.0, 215.0, 12))
    assert len(top_screws) == 26
    for idx, (x, z) in enumerate(top_screws):
        add_cylinder(scene, f"TOP_Cover_Screw_{idx:02d}", 1.55, 0.7,
                     (float(x), HEIGHT/2-0.35, float(z)), (0, 1, 0), SILVER)
    for idx, x in enumerate(np.linspace(-190.0, 190.0, 9)):
        add_cylinder(scene, f"TOP_Front_Edge_Empty_Hole_{idx}", 1.7, 0.5,
                     (float(x), HEIGHT/2-0.25, 208.0), (0, 1, 0), BLACK)

    scene.metadata.update({
        "asset": "Juniper MX204 exact exterior AC configuration",
        "units": "meters",
        "coordinate_convention": "+X right, +Y up, +Z front",
        "bottom_mode": "GENERIC_BOTTOM_FALLBACK",
        "generator": "New construction by rack-device-3d-model-assets workflow",
    })
    return scene


def patch_unlit(path: Path) -> None:
    """Make the six baked photographic faces viewer-independent and opaque."""
    gltf = GLTF2().load(str(path))
    if "KHR_materials_unlit" not in (gltf.extensionsUsed or []):
        gltf.extensionsUsed = list(gltf.extensionsUsed or []) + ["KHR_materials_unlit"]
    for material in gltf.materials or []:
        if "photographic texture" not in (material.name or ""):
            continue
        material.extensions = dict(material.extensions or {})
        material.extensions["KHR_materials_unlit"] = {}
        material.alphaMode = "OPAQUE"
        material.doubleSided = False
        if material.pbrMetallicRoughness:
            material.pbrMetallicRoughness.baseColorFactor = [1.0, 1.0, 1.0, 1.0]
            material.pbrMetallicRoughness.metallicFactor = 0.0
            material.pbrMetallicRoughness.roughnessFactor = 0.76
    gltf.samplers = [Sampler(wrapS=33071, wrapT=33071)]
    for texture in gltf.textures or []:
        texture.sampler = 0
    gltf.asset.generator = "MX204 exact-exterior build / trimesh+pygltflib / opaque-unlit faces"
    gltf.save_binary(str(path))


def export() -> None:
    MODEL.mkdir(parents=True, exist_ok=True)
    outputs = ((False, MODEL / "Juniper-MX204.glb"),
               (True, MODEL / "Juniper-MX204-web.glb"))
    for web, path in outputs:
        scene = build_scene(web)
        payload = trimesh.exchange.gltf.export_glb(scene, include_normals=True)
        path.write_bytes(payload)
        patch_unlit(path)
        print(f"wrote {path} ({path.stat().st_size} bytes), geometries={len(scene.geometry)}")


if __name__ == "__main__":
    export()
