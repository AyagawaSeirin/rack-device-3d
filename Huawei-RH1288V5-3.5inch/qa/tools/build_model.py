#!/usr/bin/env python3
"""Build exact-appearance standard and web GLBs for Huawei 1288H V5 4LFF."""

from __future__ import annotations

from pathlib import Path
from typing import Iterable

import numpy as np
from PIL import Image
import trimesh
from pygltflib import GLTF2
from trimesh.transformations import rotation_matrix
from trimesh.visual.material import PBRMaterial
from trimesh.visual.texture import TextureVisuals


ROOT = Path(__file__).resolve().parents[2]
VIEWS = ROOT / "views"
MODEL = ROOT / "model"
TEXTURES = ROOT / "qa" / "model-textures"

# Huawei user-guide dimensions for the 3.5-inch chassis, in metres.
BODY_W = 0.436
OVERALL_W = 0.4826
HEIGHT = 0.043
DEPTH = 0.748
X_MIN, X_MAX = -BODY_W / 2.0, BODY_W / 2.0
Y_MIN, Y_MAX = -HEIGHT / 2.0, HEIGHT / 2.0
Z_REAR, Z_FRONT = -DEPTH / 2.0, DEPTH / 2.0
EAR_W = (OVERALL_W - BODY_W) / 2.0

STANDARD_NAME = "Huawei-RH1288V5-3.5inch.glb"
WEB_NAME = "Huawei-RH1288V5-3.5inch-web.glb"


def pbr(
    name: str,
    rgba: tuple[int, int, int, int],
    *,
    metallic: float = 0.0,
    roughness: float = 0.72,
) -> PBRMaterial:
    return PBRMaterial(
        name=name,
        baseColorFactor=[v / 255.0 for v in rgba],
        metallicFactor=metallic,
        roughnessFactor=roughness,
        alphaMode="OPAQUE",
        doubleSided=False,
    )


MATERIALS = {
    "galvanized": pbr("GalvanizedSteel", (178, 181, 179, 255), metallic=0.38, roughness=0.68),
    "light_silver": pbr("LightStampedSteel", (205, 207, 204, 255), metallic=0.30, roughness=0.62),
    "dark_silver": pbr("DarkStampedSteel", (104, 109, 108, 255), metallic=0.24, roughness=0.70),
    "black": pbr("BlackPolymer", (17, 18, 18, 255), roughness=0.80),
    "deep_black": pbr("VentCavity", (4, 5, 5, 255), roughness=0.92),
    "blue": pbr("ServicePortBlue", (18, 91, 165, 255), roughness=0.72),
    "yellow": pbr("HuaweiReleaseYellow", (216, 225, 47, 255), roughness=0.72),
    "green": pbr("IndicatorGreen", (123, 181, 44, 255), roughness=0.65),
    "white": pbr("LabelWhite", (226, 226, 219, 255), roughness=0.90),
}


def apply_material(mesh: trimesh.Trimesh, material: PBRMaterial) -> trimesh.Trimesh:
    mesh.visual = TextureVisuals(material=material)
    return mesh


def add_box(
    scene: trimesh.Scene,
    name: str,
    extents: tuple[float, float, float],
    center: tuple[float, float, float],
    material: str,
) -> None:
    transform = np.eye(4)
    transform[:3, 3] = center
    mesh = trimesh.creation.box(extents=extents, transform=transform)
    apply_material(mesh, MATERIALS[material])
    scene.add_geometry(mesh, node_name=name, geom_name=name)


def add_cylinder(
    scene: trimesh.Scene,
    name: str,
    radius: float,
    height: float,
    center: tuple[float, float, float],
    material: str,
    *,
    axis: str = "z",
    sections: int = 24,
) -> None:
    transform = np.eye(4)
    if axis == "x":
        transform = rotation_matrix(np.pi / 2.0, [0.0, 1.0, 0.0])
    elif axis == "y":
        transform = rotation_matrix(np.pi / 2.0, [1.0, 0.0, 0.0])
    transform[:3, 3] = center
    mesh = trimesh.creation.cylinder(radius=radius, height=height, sections=sections, transform=transform)
    apply_material(mesh, MATERIALS[material])
    scene.add_geometry(mesh, node_name=name, geom_name=name)


def add_plane(
    scene: trimesh.Scene,
    name: str,
    vertices: Iterable[Iterable[float]],
    texture: Image.Image,
) -> None:
    vertices_np = np.asarray(list(vertices), dtype=np.float32)
    faces = np.asarray([[0, 1, 2], [0, 2, 3]], dtype=np.int64)
    uv = np.asarray([[0.0, 0.0], [1.0, 0.0], [1.0, 1.0], [0.0, 1.0]], dtype=np.float32)
    material = PBRMaterial(
        name=f"{name}_opaque_texture",
        baseColorTexture=texture,
        baseColorFactor=[1.0, 1.0, 1.0, 1.0],
        metallicFactor=0.0,
        roughnessFactor=0.82,
        alphaMode="OPAQUE",
        doubleSided=False,
    )
    mesh = trimesh.Trimesh(vertices=vertices_np, faces=faces, process=False)
    mesh.visual = TextureVisuals(uv=uv, image=texture, material=material)
    scene.add_geometry(mesh, node_name=name, geom_name=name)


def rgb_texture(face: str, web: bool) -> Image.Image:
    source = Image.open(VIEWS / f"{face}.png").convert("RGBA")
    fills = {
        "front": (15, 16, 16, 255),
        "rear": (181, 184, 182, 255),
        "left": (178, 181, 179, 255),
        "right": (178, 181, 179, 255),
        "top": (183, 186, 184, 255),
        "bottom": (174, 177, 175, 255),
    }
    image = Image.alpha_composite(Image.new("RGBA", source.size, fills[face]), source).convert("RGB")
    if web:
        image.thumbnail((2048, 2048), Image.Resampling.LANCZOS)
    out = TEXTURES / ("web" if web else "standard")
    out.mkdir(parents=True, exist_ok=True)
    image.save(out / f"{face}.png", optimize=True)
    return image


def add_chassis(scene: trimesh.Scene) -> None:
    # Closed structural shell with separately visible top, bottom, side lips and ears.
    add_box(scene, "ChassisStructuralBody_436x43x748mm", (BODY_W, HEIGHT - 0.0010, DEPTH), (0, 0, 0), "galvanized")
    add_box(scene, "TopCoverClosed", (BODY_W - 0.0030, 0.0015, DEPTH - 0.006), (0, Y_MAX - 0.00075, -0.001), "light_silver")
    add_box(scene, "BottomBasePlate_Fallback", (BODY_W - 0.0025, 0.0014, DEPTH - 0.004), (0, Y_MIN + 0.00070, 0), "galvanized")
    add_box(scene, "LeftTopFold", (0.0040, 0.0040, DEPTH - 0.010), (X_MIN + 0.0017, Y_MAX - 0.0020, 0), "light_silver")
    add_box(scene, "RightTopFold", (0.0040, 0.0040, DEPTH - 0.010), (X_MAX - 0.0017, Y_MAX - 0.0020, 0), "light_silver")

    # Rack ears exist only at the front plane and produce the documented 482.6 mm span.
    for side, sign in (("Left", -1.0), ("Right", 1.0)):
        x = sign * (BODY_W / 2.0 + EAR_W / 2.0)
        add_box(scene, f"FrontRackEar_{side}", (EAR_W, HEIGHT, 0.018), (x, 0, Z_FRONT - 0.009), "black")
        add_box(scene, f"FrontRackEar_{side}_InnerStep", (0.006, HEIGHT - 0.004, 0.025), (sign * (BODY_W / 2.0 + 0.003), 0, Z_FRONT - 0.0125), "dark_silver")
        for j, y in enumerate((-0.012, 0.012), 1):
            add_cylinder(scene, f"FrontRackEar_{side}_MountHole{j}", 0.0043, 0.0030, (x, y, Z_FRONT + 0.0012), "deep_black", axis="z", sections=24)


def add_front(scene: trimesh.Scene, web: bool) -> None:
    # Evidence-matched upper service strip and lower 4LFF bay row.
    # The exact upper strip artwork remains visible on the approved texture;
    # only real shallow controls are added above it as geometry.

    bay_min, bay_max = -0.209, 0.209
    gap = 0.0030
    bay_w = (bay_max - bay_min - 3 * gap) / 4.0
    bay_h = 0.0280
    for i in range(4):
        x = bay_min + bay_w / 2.0 + i * (bay_w + gap)
        # Do not cover the exact honeycomb/carrier artwork with a solid box.
        # Thin carrier rails, handles and vent relief below provide the depth.
        # Four separate carrier frames/handles give real parallax and bay depth.
        bar = 0.0016
        frame_w, frame_h = bay_w - 0.0010, bay_h
        z = Z_FRONT + 0.0038
        add_box(scene, f"LFFCarrier{i+1}_Top", (frame_w, bar, 0.0050), (x, -0.0060 + frame_h / 2 - bar / 2, z), "black")
        add_box(scene, f"LFFCarrier{i+1}_Bottom", (frame_w, bar, 0.0050), (x, -0.0060 - frame_h / 2 + bar / 2, z), "black")
        add_box(scene, f"LFFCarrier{i+1}_LeftRail", (bar, frame_h, 0.0050), (x - frame_w / 2 + bar / 2, -0.0060, z), "black")
        add_box(scene, f"LFFCarrier{i+1}_RightLatchRail", (0.0070, frame_h - 0.0010, 0.0070), (x + frame_w / 2 - 0.0042, -0.0060, Z_FRONT + 0.0048), "black")
        add_box(scene, f"LFFCarrier{i+1}_Handle", (0.0120, frame_h - 0.0040, 0.0080), (x - frame_w / 2 + 0.0072, -0.0060, Z_FRONT + 0.0052), "dark_silver")
        add_box(scene, f"LFFCarrier{i+1}_ReleaseAccent", (0.0018, frame_h - 0.0060, 0.0085), (x + frame_w / 2 - 0.0084, -0.0060, Z_FRONT + 0.0054), "yellow")
        # Recessed ventilation field: a dark cavity plus repeated geometry.
        cols = 9 if not web else 6
        rows = 2
        usable_w = frame_w - 0.026
        for row in range(rows):
            for col in range(cols):
                vx = x - usable_w / 2 + col * usable_w / max(1, cols - 1)
                vy = -0.0060 + (row - 0.5) * 0.0065
                add_cylinder(scene, f"LFFCarrier{i+1}_Vent_{row}_{col}", 0.00125, 0.0010, (vx, vy, Z_FRONT + 0.0059), "deep_black", axis="z", sections=6)

    # Upper controls: real protrusions are shallow; exact marking stays in texture.
    add_box(scene, "FrontOpticalSlimSlot", (0.039, 0.0050, 0.0042), (-0.035, 0.015, Z_FRONT + 0.0045), "deep_black")
    add_box(scene, "FrontStatusDisplay", (0.055, 0.0070, 0.0042), (0.035, 0.015, Z_FRONT + 0.0045), "dark_silver")
    add_cylinder(scene, "FrontPowerButton", 0.0030, 0.0048, (0.090, 0.015, Z_FRONT + 0.0048), "dark_silver", axis="z", sections=20)
    add_box(scene, "FrontUSB1", (0.012, 0.0055, 0.0045), (0.121, 0.015, Z_FRONT + 0.0047), "deep_black")
    add_box(scene, "FrontUSB2", (0.012, 0.0055, 0.0045), (0.151, 0.015, Z_FRONT + 0.0047), "deep_black")
    add_box(scene, "FrontVGA", (0.021, 0.0065, 0.0046), (0.185, 0.015, Z_FRONT + 0.0048), "blue")


def add_perforated_panel(
    scene: trimesh.Scene,
    name: str,
    x: float,
    y: float,
    width: float,
    height: float,
    web: bool,
) -> None:
    z = Z_REAR - 0.0022
    add_box(scene, f"{name}_Frame", (width, height, 0.0042), (x, y, z), "light_silver")
    add_box(scene, f"{name}_Cavity", (width - 0.004, height - 0.003, 0.0048), (x, y, z - 0.0020), "deep_black")
    cols = max(4, int(width / (0.008 if web else 0.006)))
    rows = max(2, int(height / 0.006))
    for row in range(rows):
        for col in range(cols):
            px = x - width * 0.43 + col * (width * 0.86) / max(1, cols - 1)
            py = y - height * 0.32 + row * (height * 0.64) / max(1, rows - 1)
            add_box(scene, f"{name}_Perforation_{row}_{col}", (0.0026, 0.0022, 0.0010), (px, py, z - 0.0046), "deep_black")


def add_rj45(scene: trimesh.Scene, name: str, x: float, y: float) -> None:
    z = Z_REAR - 0.0042
    add_box(scene, f"{name}_MetalCage", (0.016, 0.012, 0.006), (x, y, z), "light_silver")
    add_box(scene, f"{name}_Socket", (0.012, 0.0085, 0.0065), (x, y, z - 0.002), "deep_black")
    add_box(scene, f"{name}_LED", (0.0022, 0.0015, 0.0068), (x + 0.005, y + 0.004, z - 0.0025), "green")


def add_rear(scene: trimesh.Scene, web: bool) -> None:
    # Three exact external PCIe/riser regions above the service I/O.
    add_perforated_panel(scene, "RearPCIeBlank_1", 0.166, 0.0105, 0.074, 0.021, web)
    add_perforated_panel(scene, "RearPCIeBlank_2", 0.073, 0.0105, 0.096, 0.021, web)
    add_perforated_panel(scene, "RearPCIeBlank_3", -0.038, 0.0105, 0.109, 0.021, web)

    # Management/service I/O (rear screen-left = physical +X).
    add_rj45(scene, "RearGE_A1", 0.197, -0.0135)
    add_rj45(scene, "RearGE_A2", 0.176, -0.0135)
    add_box(scene, "RearVGA_DB15", (0.022, 0.011, 0.0065), (0.145, -0.0135, Z_REAR - 0.0044), "blue")
    for i, x in enumerate((0.113, 0.094, 0.075, 0.056), 1):
        add_rj45(scene, f"RearLOM_RJ45_{i}", x, -0.0135)
    add_box(scene, "RearUSB_1", (0.014, 0.0065, 0.006), (0.034, -0.0085, Z_REAR - 0.0042), "blue")
    add_box(scene, "RearUSB_2", (0.014, 0.0065, 0.006), (0.034, -0.0175, Z_REAR - 0.0042), "blue")
    add_box(scene, "RearFlexIOBlank", (0.080, 0.016, 0.005), (-0.025, -0.0130, Z_REAR - 0.0030), "light_silver")
    add_box(scene, "RearFlexIOVent", (0.065, 0.008, 0.0058), (-0.025, -0.0130, Z_REAR - 0.0048), "deep_black")
    add_cylinder(scene, "RearPSUFaultIndicator", 0.0021, 0.0050, (-0.085, -0.002, Z_REAR - 0.0040), "green", axis="z", sections=16)

    # Two separately modeled exact-specimen 900 W hot-swap AC PSU modules.
    module_w = 0.058
    for i, x in enumerate((-0.129, -0.188), 1):
        add_box(scene, f"ACPSU_900W_{i}_Body", (module_w, 0.039, 0.020), (x, -0.0005, Z_REAR + 0.0060), "dark_silver")
        add_box(scene, f"ACPSU_900W_{i}_Face", (module_w - 0.002, 0.037, 0.0050), (x, -0.0005, Z_REAR - 0.0020), "black")
        fan_x = x + 0.012
        inlet_x = x - 0.014
        add_cylinder(scene, f"ACPSU_900W_{i}_FanOuter", 0.0145, 0.0055, (fan_x, -0.0005, Z_REAR - 0.0040), "dark_silver", axis="z", sections=32 if not web else 20)
        add_cylinder(scene, f"ACPSU_900W_{i}_FanCavity", 0.0118, 0.0060, (fan_x, -0.0005, Z_REAR - 0.0048), "deep_black", axis="z", sections=32 if not web else 20)
        add_cylinder(scene, f"ACPSU_900W_{i}_FanHub", 0.0035, 0.0065, (fan_x, -0.0005, Z_REAR - 0.0052), "dark_silver", axis="z", sections=20)
        add_box(scene, f"ACPSU_900W_{i}_IEC_C14", (0.017, 0.022, 0.0064), (inlet_x, -0.0005, Z_REAR - 0.0049), "deep_black")
        add_box(scene, f"ACPSU_900W_{i}_Handle", (0.0045, 0.027, 0.0080), (x + 0.024, -0.0005, Z_REAR - 0.0055), "black")
        add_box(scene, f"ACPSU_900W_{i}_ReleaseLatch", (0.0040, 0.012, 0.0085), (x - 0.026, 0.0100, Z_REAR - 0.0058), "yellow")


def add_top_bottom_and_sides(scene: trimesh.Scene, web: bool) -> None:
    # Top cover seams and evidence-matched latch.
    add_box(scene, "TopFrontPanelSeam", (BODY_W - 0.012, 0.0008, 0.0020), (0, Y_MAX + 0.0001, 0.272), "dark_silver")
    add_box(scene, "TopRearPanelSeam", (BODY_W - 0.012, 0.0008, 0.0020), (0, Y_MAX + 0.0001, -0.302), "dark_silver")
    # The published 43 mm height is the controlling envelope. Latch relief is
    # shallow and mostly recessed, as on the exact closed-cover photographs.
    add_box(scene, "TopCoverLatchBase", (0.047, 0.0014, 0.025), (0, Y_MAX - 0.0004, 0.055), "light_silver")
    add_box(scene, "TopCoverLatchHandle", (0.028, 0.0018, 0.014), (0, Y_MAX + 0.0003, 0.055), "dark_silver")
    add_box(scene, "TopCoverLatchYellowMark", (0.010, 0.0016, 0.0035), (0, Y_MAX + 0.0004, 0.061), "yellow")

    # Two independent slot bands, visible as real geometry in grazing views.
    cols = 46 if not web else 28
    for band_name, z in (("Front", 0.155), ("Rear", -0.255)):
        add_box(scene, f"TopVentBand{band_name}_Recess", (0.330, 0.0008, 0.013), (0, Y_MAX + 0.0001, z), "deep_black")
        for col in range(cols):
            x = -0.160 + col * 0.320 / max(1, cols - 1)
            add_box(scene, f"TopVentBand{band_name}_Slot_{col}", (0.0038, 0.0010, 0.0080), (x, Y_MAX + 0.0002, z), "deep_black")

    # Conservative bottom fallback: closed base, one manufacturing seam and screws.
    add_box(scene, "BottomManufacturingSeam", (BODY_W - 0.018, 0.0008, 0.0020), (0, Y_MIN - 0.0001, -0.292), "dark_silver")
    bottom_screws = [(-0.190, 0.320), (0.190, 0.320), (-0.190, 0.050), (0.190, 0.050), (-0.190, -0.250), (0.190, -0.250)]
    for i, (x, z) in enumerate(bottom_screws, 1):
        add_cylinder(scene, f"BottomFallbackScrew_{i}", 0.0022, 0.0010, (x, Y_MIN - 0.0003, z), "dark_silver", axis="y", sections=16)

    # Independent side construction. Patterns deliberately differ; no mirrored side asset.
    add_box(scene, "LeftSideUpperRailRelief", (0.0035, 0.0060, 0.565), (X_MIN - 0.0010, 0.012, 0.015), "light_silver")
    add_box(scene, "RightSideUpperRailRelief", (0.0035, 0.0050, 0.610), (X_MAX + 0.0010, 0.013, -0.008), "light_silver")
    left_points = [(0.009, 0.304), (-0.006, 0.160), (0.002, -0.010), (-0.005, -0.205), (0.007, -0.335)]
    right_points = [(0.006, 0.315), (0.004, 0.120), (-0.003, -0.075), (0.006, -0.280)]
    for side, x, points in (("Left", X_MIN - 0.0018, left_points), ("Right", X_MAX + 0.0018, right_points)):
        for i, (y, z) in enumerate(points, 1):
            add_cylinder(scene, f"{side}SideFastener_{i}", 0.0021, 0.0030, (x, y, z), "dark_silver", axis="x", sections=16)
    add_box(scene, "LeftRearRailCutout", (0.0040, 0.0070, 0.025), (X_MIN - 0.0015, -0.010, Z_REAR + 0.040), "deep_black")
    add_box(scene, "RightFrontVentRelief", (0.0040, 0.021, 0.018), (X_MAX + 0.0015, 0.000, Z_FRONT - 0.035), "deep_black")


def add_textured_faces(scene: trimesh.Scene, textures: dict[str, Image.Image]) -> None:
    e = 0.00010
    add_plane(scene, "FrontExactAppearanceSurface", [
        (-OVERALL_W / 2, Y_MIN, Z_FRONT + e),
        (OVERALL_W / 2, Y_MIN, Z_FRONT + e),
        (OVERALL_W / 2, Y_MAX, Z_FRONT + e),
        (-OVERALL_W / 2, Y_MAX, Z_FRONT + e),
    ], textures["front"])
    add_plane(scene, "RearExactAppearanceSurface", [
        (X_MAX, Y_MIN, Z_REAR - e),
        (X_MIN, Y_MIN, Z_REAR - e),
        (X_MIN, Y_MAX, Z_REAR - e),
        (X_MAX, Y_MAX, Z_REAR - e),
    ], textures["rear"])
    add_plane(scene, "RightIndependentAppearanceSurface", [
        (X_MAX + e, Y_MIN, Z_FRONT),
        (X_MAX + e, Y_MIN, Z_REAR),
        (X_MAX + e, Y_MAX, Z_REAR),
        (X_MAX + e, Y_MAX, Z_FRONT),
    ], textures["right"])
    add_plane(scene, "LeftIndependentAppearanceSurface", [
        (X_MIN - e, Y_MIN, Z_REAR),
        (X_MIN - e, Y_MIN, Z_FRONT),
        (X_MIN - e, Y_MAX, Z_FRONT),
        (X_MIN - e, Y_MAX, Z_REAR),
    ], textures["left"])
    # PNG prompt orientation: front at image bottom. UV ordering compensates for glTF image origin.
    add_plane(scene, "TopExactAppearanceSurface", [
        (X_MAX, Y_MAX + e, Z_REAR),
        (X_MIN, Y_MAX + e, Z_REAR),
        (X_MIN, Y_MAX + e, Z_FRONT),
        (X_MAX, Y_MAX + e, Z_FRONT),
    ], textures["top"])
    add_plane(scene, "BottomFallbackAppearanceSurface", [
        (X_MIN, Y_MIN - e, Z_REAR),
        (X_MAX, Y_MIN - e, Z_REAR),
        (X_MAX, Y_MIN - e, Z_FRONT),
        (X_MIN, Y_MIN - e, Z_FRONT),
    ], textures["bottom"])


def patch_unlit_textures(path: Path) -> None:
    document = GLTF2().load_binary(str(path))
    used = list(document.extensionsUsed or [])
    if "KHR_materials_unlit" not in used:
        used.append("KHR_materials_unlit")
    document.extensionsUsed = used
    for material in document.materials or []:
        if material.name and material.name.endswith("_opaque_texture"):
            extensions = dict(material.extensions or {})
            extensions["KHR_materials_unlit"] = {}
            material.extensions = extensions
            material.alphaMode = "OPAQUE"
            material.doubleSided = False
    document.save_binary(str(path))


def build(web: bool) -> Path:
    scene = trimesh.Scene(base_frame="Huawei1288HV5_Xright_Yup_Zfront")
    scene.metadata.update({
        "manufacturer": "Huawei Technologies Co., Ltd.",
        "product": "FusionServer Pro 1288H V5 Server",
        "source_list_alias": "RH1288V5/3.5-inch",
        "variant": "1U, four 3.5-inch LFF carriers, three-I/O rear family, 2 x 900 W AC PSU",
        "dimensions_mm": "body 436 x 43 x 748; rack-ear span 482.6",
        "coordinate_convention": "+X right, +Y up, +Z front",
        "build_type": "new exact-appearance exterior replica; bottom controlled fallback",
    })
    add_chassis(scene)
    add_front(scene, web)
    add_rear(scene, web)
    add_top_bottom_and_sides(scene, web)
    textures = {face: rgb_texture(face, web) for face in ("front", "rear", "left", "right", "top", "bottom")}
    add_textured_faces(scene, textures)

    MODEL.mkdir(parents=True, exist_ok=True)
    output = MODEL / (WEB_NAME if web else STANDARD_NAME)
    output.write_bytes(scene.export(file_type="glb", include_normals=True))
    patch_unlit_textures(output)
    print(f"{output} bytes={output.stat().st_size} geometry={len(scene.geometry)}")
    return output


def main() -> None:
    build(web=False)
    build(web=True)


if __name__ == "__main__":
    main()
