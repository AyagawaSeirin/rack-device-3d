#!/usr/bin/env python3
"""Build exact-appearance standard/web GLBs for HPE DL360 Gen9 8SFF."""

from __future__ import annotations

from pathlib import Path
from typing import Iterable

import numpy as np
from PIL import Image
from pygltflib import GLTF2
import trimesh
from trimesh.transformations import rotation_matrix
from trimesh.visual.material import PBRMaterial
from trimesh.visual.texture import TextureVisuals


ROOT = Path(__file__).resolve().parents[2]
VIEWS = ROOT / "views"
MODEL = ROOT / "model"
TEXTURES = ROOT / "qa" / "model-textures"

# HPE published 8/10SFF system-unit dimensions plus separately resolved protrusions.
BODY_W = 0.4347
OVERALL_W = 0.4826
HEIGHT = 0.0432
BODY_D = 0.6985
FRONT_PROTRUSION = 0.0040
REAR_PROTRUSION = 0.0210
OVERALL_D = BODY_D + FRONT_PROTRUSION + REAR_PROTRUSION
EAR_W = (OVERALL_W - BODY_W) / 2.0

# Keep the opaque source-locked appearance sheets far enough above the closed
# structural shell to avoid cross-viewer depth fighting. 10-20 micrometres was
# stable in Three.js but exposed large underlying-shell triangles in Babylon.js
# oblique views; 0.15 mm remains below all modeled feature relief.
FACE_TEXTURE_OFFSET = 0.00015

X_MIN, X_MAX = -BODY_W / 2.0, BODY_W / 2.0
Y_MIN, Y_MAX = -HEIGHT / 2.0, HEIGHT / 2.0
Z_REAR, Z_FRONT = -BODY_D / 2.0, BODY_D / 2.0

STANDARD_NAME = "HPE-DL360G9-2.5inch.glb"
WEB_NAME = "HPE-DL360G9-2.5inch-web.glb"


def pbr(
    name: str,
    rgba: tuple[int, int, int, int],
    *,
    metallic: float = 0.0,
    roughness: float = 0.75,
) -> PBRMaterial:
    return PBRMaterial(
        name=name,
        baseColorFactor=[channel / 255.0 for channel in rgba],
        metallicFactor=metallic,
        roughnessFactor=roughness,
        alphaMode="OPAQUE",
        doubleSided=False,
    )


MATERIALS = {
    "galvanized": pbr("HPE_GalvanizedSteel", (180, 183, 181, 255), metallic=0.34, roughness=0.70),
    "silver": pbr("HPE_LightStampedSteel", (205, 207, 204, 255), metallic=0.28, roughness=0.64),
    "dark_silver": pbr("HPE_DarkStampedSteel", (96, 101, 100, 255), metallic=0.18, roughness=0.72),
    "black": pbr("HPE_BlackPolymer", (18, 19, 19, 255), roughness=0.84),
    "deep_black": pbr("HPE_VentAndPortCavity", (3, 4, 4, 255), roughness=0.94),
    "blue": pbr("HPE_ServicePortBlue", (16, 91, 171, 255), roughness=0.74),
    "green": pbr("HPE_IndicatorGreen", (45, 190, 63, 255), roughness=0.62),
    "red": pbr("HPE_ReleaseRed", (144, 37, 48, 255), roughness=0.68),
    "psu_blue": pbr("HPE_500WBadgeBlue", (58, 169, 222, 255), roughness=0.70),
    "yellow": pbr("HPE_SafetyYellow", (242, 211, 18, 255), roughness=0.72),
    "white": pbr("HPE_LabelWhite", (229, 229, 224, 255), roughness=0.92),
}


def apply_material(mesh: trimesh.Trimesh, material: PBRMaterial) -> trimesh.Trimesh:
    mesh.visual = TextureVisuals(material=material)
    return mesh


def add_mesh(scene: trimesh.Scene, name: str, mesh: trimesh.Trimesh, material: str) -> None:
    apply_material(mesh, MATERIALS[material])
    scene.add_geometry(mesh, node_name=name, geom_name=name)


def add_box(
    scene: trimesh.Scene,
    name: str,
    extents: tuple[float, float, float],
    center: tuple[float, float, float],
    material: str,
    *,
    rotate_z: float = 0.0,
) -> None:
    transform = rotation_matrix(rotate_z, [0.0, 0.0, 1.0]) if rotate_z else np.eye(4)
    transform[:3, 3] = center
    mesh = trimesh.creation.box(extents=extents, transform=transform)
    add_mesh(scene, name, mesh, material)


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
    mesh = trimesh.creation.cylinder(
        radius=radius,
        height=height,
        sections=sections,
        transform=transform,
    )
    add_mesh(scene, name, mesh, material)


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


def opaque_rgb(face: str, web: bool) -> Image.Image:
    source = Image.open(VIEWS / f"{face}.png").convert("RGBA")
    fills = {
        "front": (13, 14, 14, 255),
        "rear": (184, 186, 184, 255),
        "left": (177, 180, 178, 255),
        "right": (177, 180, 178, 255),
        "top": (188, 191, 190, 255),
        "bottom": (177, 180, 179, 255),
    }
    image = Image.alpha_composite(Image.new("RGBA", source.size, fills[face]), source).convert("RGB")
    if web:
        limits = {
            "front": (2048, 2048),
            "rear": (2048, 2048),
            "left": (2048, 2048),
            "right": (2048, 2048),
            "top": (1536, 1536),
            "bottom": (1536, 1536),
        }
        image.thumbnail(limits[face], Image.Resampling.LANCZOS)
    target_dir = TEXTURES / ("web" if web else "standard")
    target_dir.mkdir(parents=True, exist_ok=True)
    image.save(target_dir / f"{face}.png", "PNG", optimize=True)
    return image


def front_body_texture(web: bool) -> Image.Image:
    source = Image.open(VIEWS / "front.png").convert("RGBA")
    alpha = source.getchannel("A")
    bbox = alpha.point(lambda value: 255 if value > 8 else 0).getbbox() or (0, 0, *source.size)
    content = source.crop(bbox)
    ear_pixels = max(1, round(content.width * EAR_W / OVERALL_W))
    body = content.crop((ear_pixels, 0, content.width - ear_pixels, content.height))
    body = Image.alpha_composite(Image.new("RGBA", body.size, (13, 14, 14, 255)), body).convert("RGB")
    if web:
        body.thumbnail((2048, 2048), Image.Resampling.LANCZOS)
    target_dir = TEXTURES / ("web" if web else "standard")
    target_dir.mkdir(parents=True, exist_ok=True)
    body.save(target_dir / "front-body.png", "PNG", optimize=True)
    return body


def front_ear_texture(side: str, web: bool) -> Image.Image:
    source = Image.open(VIEWS / "front.png").convert("RGBA")
    alpha = source.getchannel("A")
    bbox = alpha.point(lambda value: 255 if value > 8 else 0).getbbox() or (0, 0, *source.size)
    content = source.crop(bbox)
    ear_pixels = max(1, round(content.width * EAR_W / OVERALL_W))
    if side == "left":
        ear = content.crop((0, 0, ear_pixels, content.height))
    else:
        ear = content.crop((content.width - ear_pixels, 0, content.width, content.height))
    ear = Image.alpha_composite(Image.new("RGBA", ear.size, (207, 209, 206, 255)), ear).convert("RGB")
    # Keep the factory HP/HPE and ProLiant marks legible in both delivery GLBs.
    # Upscaling does not invent detail; it prevents the small dedicated ear map
    # from being minified below the web viewers' readable-label threshold.
    scale = 1024 / max(ear.size)
    if scale > 1.0:
        ear = ear.resize(
            (max(1, round(ear.width * scale)), max(1, round(ear.height * scale))),
            Image.Resampling.LANCZOS,
        )
    target_dir = TEXTURES / ("web" if web else "standard")
    target_dir.mkdir(parents=True, exist_ok=True)
    ear.save(target_dir / f"{side}-ear.png", "PNG", optimize=True)
    return ear


def add_chassis_and_ears(scene: trimesh.Scene, web: bool) -> None:
    # Closed body and access cover, kept inside the published 43.2 mm height.
    add_box(scene, "ChassisStructuralBody_434p7x43p2x698p5mm", (BODY_W, HEIGHT, BODY_D), (0, 0, 0), "galvanized")
    add_box(scene, "TopAccessCover_Closed", (BODY_W - 0.003, 0.0012, BODY_D - 0.006), (0, Y_MAX - 0.0006, 0), "silver")
    add_box(scene, "BottomBasePlate_GenericFallback", (BODY_W - 0.002, 0.0012, BODY_D - 0.004), (0, Y_MIN + 0.0006, 0), "galvanized")

    # Separate front-only HPE Quick Release ears. Exact photos show solid tool-less
    # ear faces, not generic rack flanges with large circular mounting holes.
    for side, sign in (("Left", -1.0), ("Right", 1.0)):
        add_box(
            scene,
            f"FrontHPEQuickReleaseEar_{side}_SolidToollessBody",
            (EAR_W, HEIGHT, 0.0060),
            (sign * (BODY_W / 2.0 + EAR_W / 2.0), 0.0, Z_FRONT - 0.0030),
            "silver",
        )
        add_box(
            scene,
            f"FrontQuickReleaseEar_{side}_InnerStep",
            (0.006, HEIGHT - 0.004, 0.018),
            (sign * (BODY_W / 2.0 + 0.003), 0, Z_FRONT - 0.009),
            "dark_silver",
        )
        texture = front_ear_texture(side.lower(), web)
        x0 = sign * BODY_W / 2.0
        x1 = sign * OVERALL_W / 2.0
        if x0 > x1:
            x0, x1 = x1, x0
        add_plane(
            scene,
            f"FrontHPEQuickReleaseEar_{side}_SourceLockedFace",
            [
                (x0, Y_MIN, Z_FRONT + FACE_TEXTURE_OFFSET),
                (x1, Y_MIN, Z_FRONT + FACE_TEXTURE_OFFSET),
                (x1, Y_MAX, Z_FRONT + FACE_TEXTURE_OFFSET),
                (x0, Y_MAX, Z_FRONT + FACE_TEXTURE_OFFSET),
            ],
            texture,
        )


def add_sff_carrier(
    scene: trimesh.Scene,
    index: int,
    x: float,
    y: float,
    *,
    web: bool,
) -> None:
    width, height = 0.068, 0.0172
    depth = 0.0040
    z = Z_FRONT + depth / 2.0
    rail = 0.00125
    # Open frame leaves the source-locked carrier texture visible while adding parallax.
    add_box(scene, f"SFFCarrier_{index:02d}_TopRail", (width, rail, depth), (x, y + height / 2 - rail / 2, z), "black")
    add_box(scene, f"SFFCarrier_{index:02d}_BottomRail", (width, rail, depth), (x, y - height / 2 + rail / 2, z), "black")
    add_box(scene, f"SFFCarrier_{index:02d}_LeftRail", (rail, height, depth), (x - width / 2 + rail / 2, y, z), "black")
    add_box(scene, f"SFFCarrier_{index:02d}_RightRail", (rail, height, depth), (x + width / 2 - rail / 2, y, z), "black")
    # Independent pull handle, circular activity/release detail and red latch.
    add_box(scene, f"SFFCarrier_{index:02d}_PullHandle", (0.012, height - 0.003, 0.0046), (x - width / 2 + 0.007, y, Z_FRONT + 0.0017), "dark_silver")
    add_cylinder(scene, f"SFFCarrier_{index:02d}_ReleaseRing", 0.0045, 0.0022, (x + 0.013, y, Z_FRONT + 0.0029), "black", axis="z", sections=24 if not web else 16)
    add_cylinder(scene, f"SFFCarrier_{index:02d}_ActivityGreen", 0.0026, 0.0025, (x + 0.013, y, Z_FRONT + 0.0030), "green", axis="z", sections=20 if not web else 14)
    add_box(scene, f"SFFCarrier_{index:02d}_RedReleaseLatch", (0.010, height - 0.004, 0.0046), (x + width / 2 - 0.0062, y, Z_FRONT + 0.0017), "red")
    # Handle/vent slots are opaque dark geometry, never transparent body pixels.
    slots = 5 if not web else 4
    for slot in range(slots):
        sx = x - 0.018 + slot * 0.006
        add_box(scene, f"SFFCarrier_{index:02d}_VentSlot_{slot+1}", (0.0036, 0.0013, 0.0048), (sx, y - 0.004, Z_FRONT + 0.0020), "deep_black")


def add_front(scene: trimesh.Scene, web: bool) -> None:
    top_y, bottom_y = 0.0100, -0.0100
    left_columns = (-0.168, -0.095, -0.022)
    index = 1
    for x in left_columns:
        for y in (top_y, bottom_y):
            add_sff_carrier(scene, index, x, y, web=web)
            index += 1
    for x in (0.061, 0.134):
        add_sff_carrier(scene, index, x, bottom_y, web=web)
        index += 1

    # Universal Media Bay above carriers 7-8: independent VGA, USB, optical slot and grille.
    add_box(scene, "FrontUniversalMediaBay_Frame", (0.142, 0.0175, 0.0020), (0.098, top_y, Z_FRONT + 0.0008), "black")
    add_box(scene, "FrontUniversalMediaBay_OpticalSlot", (0.064, 0.0040, 0.0042), (0.132, 0.0135, Z_FRONT + 0.0020), "deep_black")
    add_box(scene, "FrontUniversalMediaBay_USB2", (0.012, 0.0055, 0.0044), (0.089, 0.0150, Z_FRONT + 0.0021), "deep_black")
    add_box(scene, "FrontUniversalMediaBay_VGA_Shell", (0.023, 0.0090, 0.0044), (0.049, 0.0108, Z_FRONT + 0.0021), "silver")
    add_box(scene, "FrontUniversalMediaBay_VGA_Blue", (0.018, 0.0060, 0.0048), (0.049, 0.0108, Z_FRONT + 0.0023), "blue")
    grille_cols = 17 if not web else 12
    for col in range(grille_cols):
        gx = 0.083 + col * 0.0052
        add_box(scene, f"FrontMediaBay_GrilleSlot_{col+1}", (0.0032, 0.0016, 0.0045), (gx, 0.0060, Z_FRONT + 0.0022), "deep_black")

    # Far-right front control strip with separate controls and USB 3.0.
    add_box(scene, "FrontControlStrip_Backplate", (0.023, HEIGHT - 0.003, 0.0020), (0.200, 0, Z_FRONT + 0.0008), "black")
    for idx, (y, material) in enumerate(((0.014, "green"), (0.008, "green"), (0.002, "yellow"), (-0.004, "blue")), 1):
        add_box(scene, f"FrontControlStrip_LED_{idx}", (0.0033, 0.0033, 0.0044), (0.194, y, Z_FRONT + 0.0022), material)
    add_box(scene, "FrontControlStrip_SID", (0.006, 0.015, 0.0040), (0.205, 0.008, Z_FRONT + 0.0020), "dark_silver")
    add_box(scene, "FrontControlStrip_USB3", (0.0068, 0.013, 0.0046), (0.205, -0.011, Z_FRONT + 0.0023), "blue")

    # Long upper intake geometry, source-matched and opaque.
    intake_cols = 46 if not web else 34
    for col in range(intake_cols):
        x = -0.201 + col * 0.0080
        if x > 0.177:
            break
        add_box(scene, f"FrontUpperIntakeSlot_{col+1}", (0.0054, 0.0018, 0.0030), (x, 0.0185, Z_FRONT + 0.0014), "deep_black")


def add_pcie_blank(scene: trimesh.Scene, name: str, x: float, width: float, web: bool) -> None:
    y, height = 0.0102, 0.0190
    z = Z_REAR - 0.0020
    add_box(scene, f"{name}_Plate", (width, height, 0.0040), (x, y, z), "silver")
    add_box(scene, f"{name}_Recess", (width - 0.006, height - 0.007, 0.0045), (x, y, Z_REAR - 0.0024), "galvanized")
    ribs = max(3, round(width / (0.020 if web else 0.014)))
    for rib in range(ribs):
        rx = x - width * 0.38 + rib * width * 0.76 / max(1, ribs - 1)
        add_box(scene, f"{name}_Rib_{rib+1}", (0.0014, height - 0.008, 0.0048), (rx, y, Z_REAR - 0.0025), "dark_silver")


def add_rj45(scene: trimesh.Scene, name: str, x: float, y: float) -> None:
    add_box(scene, f"{name}_MetalCage", (0.017, 0.0125, 0.0050), (x, y, Z_REAR - 0.0025), "silver")
    add_box(scene, f"{name}_Socket", (0.0125, 0.0088, 0.0055), (x, y, Z_REAR - 0.0030), "deep_black")
    add_box(scene, f"{name}_GreenLED", (0.0020, 0.0015, 0.0058), (x + 0.0052, y + 0.0044, Z_REAR - 0.0032), "green")


def add_db9(scene: trimesh.Scene, name: str, x: float, y: float) -> None:
    add_box(scene, f"{name}_Shell", (0.024, 0.0105, 0.0050), (x, y, Z_REAR - 0.0026), "silver")
    add_box(scene, f"{name}_PinField", (0.017, 0.0064, 0.0054), (x, y, Z_REAR - 0.0030), "deep_black")
    for row in range(2):
        count = 5 if row == 0 else 4
        for col in range(count):
            px = x - 0.0065 + col * (0.013 / max(1, count - 1))
            py = y + (0.0016 if row == 0 else -0.0016)
            add_cylinder(scene, f"{name}_Pin_{row}_{col}", 0.00035, 0.0010, (px, py, Z_REAR - 0.0052), "yellow", axis="z", sections=8)


def add_fan_blades(scene: trimesh.Scene, prefix: str, x: float, y: float, z: float, web: bool) -> None:
    sections = 20 if web else 28
    add_cylinder(scene, f"{prefix}_FanFrame", 0.0150, 0.0040, (x, y, z), "dark_silver", axis="z", sections=sections)
    add_cylinder(scene, f"{prefix}_FanCavity", 0.0128, 0.0044, (x, y, z - 0.0005), "deep_black", axis="z", sections=sections)
    for blade in range(7):
        angle = blade * 2.0 * np.pi / 7.0 + 0.16
        radius = 0.0070
        bx = x + np.cos(angle) * radius
        by = y + np.sin(angle) * radius
        add_box(scene, f"{prefix}_FanBlade_{blade+1}", (0.0030, 0.0100, 0.0048), (bx, by, z - 0.0008), "dark_silver", rotate_z=angle - 0.35)
    add_cylinder(scene, f"{prefix}_FanHub", 0.0036, 0.0050, (x, y, z - 0.0010), "dark_silver", axis="z", sections=18)
    add_cylinder(scene, f"{prefix}_500WBadge", 0.0030, 0.0052, (x, y, z - 0.0013), "psu_blue", axis="z", sections=18)


def add_psu(scene: trimesh.Scene, index: int, x: float, web: bool) -> None:
    name = f"ACPSU_500W_{index}"
    add_box(scene, f"{name}_IndependentBody", (0.056, 0.039, 0.020), (x, 0, Z_REAR + 0.010), "dark_silver")
    add_box(scene, f"{name}_RearFace", (0.055, 0.038, 0.0050), (x, 0, Z_REAR - 0.0025), "black")
    fan_x = x - 0.010
    inlet_x = x + 0.015
    add_fan_blades(scene, name, fan_x, 0, Z_REAR - 0.0040, web)
    add_box(scene, f"{name}_IEC_C14", (0.017, 0.022, 0.0060), (inlet_x, 0, Z_REAR - 0.0040), "deep_black")
    # Source-proven pull handle reaches 21 mm behind the body plane.
    add_box(scene, f"{name}_PullHandle", (0.0060, 0.027, 0.0060), (fan_x, -0.001, Z_REAR - 0.0180), "black")
    add_box(scene, f"{name}_RedReleaseLatch", (0.012, 0.0060, 0.0070), (x + 0.023, 0.011, Z_REAR - 0.0070), "red")
    add_box(scene, f"{name}_StatusLED", (0.0025, 0.0025, 0.0065), (x + 0.023, 0.015, Z_REAR - 0.0055), "green")


def add_rear(scene: trimesh.Scene, web: bool) -> None:
    # Three explicit no-card PCIe blanking plates.
    add_pcie_blank(scene, "RearPCIeBlank_Slot1", 0.170, 0.072, web)
    add_pcie_blank(scene, "RearPCIeBlank_Slot2", 0.088, 0.070, web)
    add_pcie_blank(scene, "RearPCIeBlank_Slot3", 0.005, 0.082, web)

    # FlexibleLOM blank and its source-locked green release detail.
    add_box(scene, "RearFlexibleLOM_Blank", (0.086, 0.016, 0.0048), (0.171, -0.0125, Z_REAR - 0.0025), "silver")
    add_box(scene, "RearFlexibleLOM_Blank_Recess", (0.073, 0.010, 0.0052), (0.171, -0.0125, Z_REAR - 0.0029), "galvanized")
    add_box(scene, "RearFlexibleLOM_GreenRelease", (0.006, 0.0025, 0.0058), (0.205, -0.0060, Z_REAR - 0.0033), "green")

    # Two stacked USB 3.0 ports.
    for index, y in enumerate((-0.0080, -0.0160), 1):
        add_box(scene, f"RearUSB3_{index}_Shell", (0.014, 0.0060, 0.0050), (0.112, y, Z_REAR - 0.0025), "silver")
        add_box(scene, f"RearUSB3_{index}_BlueInsert", (0.010, 0.0035, 0.0055), (0.112, y, Z_REAR - 0.0030), "blue")

    add_db9(scene, "RearSerial_DB9", 0.075, -0.0120)
    add_rj45(scene, "Rear_iLO4_Dedicated", 0.039, -0.0125)
    for index, x in enumerate((0.010, -0.020, -0.050, -0.080), 1):
        add_rj45(scene, f"RearEmbedded331i_NIC{index}", x, -0.0125)
    add_box(scene, "RearVGA_DB15_Shell", (0.025, 0.011, 0.0050), (-0.117, -0.0125, Z_REAR - 0.0025), "silver")
    add_box(scene, "RearVGA_DB15_Blue", (0.019, 0.0065, 0.0055), (-0.117, -0.0125, Z_REAR - 0.0030), "blue")

    # Source-locked separator/vent between VGA and PSUs.
    vent_cols = 4
    for col in range(vent_cols):
        add_box(scene, f"RearPrePSU_Vent_{col+1}", (0.0030, 0.015, 0.0050), (-0.151 + col * 0.0050, -0.005, Z_REAR - 0.0028), "deep_black")

    add_psu(scene, 2, -0.188, web)
    add_psu(scene, 1, -0.129, web)


def add_top_side_geometry(scene: trimesh.Scene, web: bool) -> None:
    # Top cover: front is +Z. Relief remains within the published height envelope.
    groups = [
        (0.000, 0.290, 44),
        (-0.115, -0.255, 24),
        (0.070, -0.255, 30),
        (0.095, -0.070, 16),
    ]
    for group_index, (cx, cz, count) in enumerate(groups, 1):
        actual = max(8, count if not web else round(count * 0.72))
        columns = max(4, round(actual ** 0.5 * 2.0))
        rows = max(2, round(actual / columns))
        for row in range(rows):
            for col in range(columns):
                x = cx + (col - (columns - 1) / 2.0) * 0.0060
                z = cz + (row - (rows - 1) / 2.0) * 0.0060
                add_cylinder(scene, f"TopVentGroup{group_index}_Hole_{row}_{col}", 0.00155, 0.0008, (x, Y_MAX - 0.0004, z), "deep_black", axis="y", sections=8 if web else 12)
    add_box(scene, "TopCoverReleaseLatch_Recess", (0.030, 0.0009, 0.055), (0.082, Y_MAX - 0.00045, -0.070), "dark_silver")
    add_box(scene, "TopCoverReleaseLatch_Handle", (0.018, 0.0010, 0.032), (0.082, Y_MAX - 0.00050, -0.070), "black")
    for index, z in enumerate((0.225, 0.045, -0.150, -0.315), 1):
        add_box(scene, f"TopCoverSmallLatch_{index}", (0.008, 0.0009, 0.018), (0.050 if index % 2 else -0.050, Y_MAX - 0.0004, z), "dark_silver")

    # Independent non-mirrored physical side relief.
    left_points = [(-0.010, 0.300), (0.004, 0.150), (-0.006, -0.080), (0.002, -0.250), (-0.008, -0.325)]
    right_points = [(0.005, 0.305), (-0.006, 0.205), (0.004, 0.030), (-0.004, -0.130), (0.006, -0.290)]
    for side, x, points in (("Left", X_MIN, left_points), ("Right", X_MAX, right_points)):
        for index, (y, z) in enumerate(points, 1):
            add_cylinder(scene, f"{side}Side_RailHole_{index}", 0.0027, 0.0010, (x, y, z), "deep_black", axis="x", sections=18 if not web else 12)
    add_box(scene, "LeftSide_RearPerforationRelief", (0.0010, 0.012, 0.075), (X_MIN, -0.006, -0.285), "deep_black")
    add_box(scene, "RightSide_RearPerforationRelief", (0.0010, 0.010, 0.060), (X_MAX, -0.007, -0.295), "deep_black")
    add_box(scene, "RightSide_LongRailSlot", (0.0010, 0.005, 0.030), (X_MAX, 0.007, -0.305), "deep_black")
    # Bottom intentionally receives no unsupported feature geometry.


def add_textured_faces(scene: trimesh.Scene, web: bool) -> None:
    textures = {face: opaque_rgb(face, web) for face in ("rear", "left", "right", "top", "bottom")}
    front_body = front_body_texture(web)
    e = FACE_TEXTURE_OFFSET
    add_plane(
        scene,
        "FrontBody_SourceLockedAppearance",
        [
            (X_MIN, Y_MIN, Z_FRONT + e),
            (X_MAX, Y_MIN, Z_FRONT + e),
            (X_MAX, Y_MAX, Z_FRONT + e),
            (X_MIN, Y_MAX, Z_FRONT + e),
        ],
        front_body,
    )
    add_plane(
        scene,
        "Rear_SourceLockedAppearance",
        [
            (X_MAX, Y_MIN, Z_REAR - e),
            (X_MIN, Y_MIN, Z_REAR - e),
            (X_MIN, Y_MAX, Z_REAR - e),
            (X_MAX, Y_MAX, Z_REAR - e),
        ],
        textures["rear"],
    )
    add_plane(
        scene,
        "RightIndependentAppearance",
        [
            (X_MAX + e, Y_MIN, Z_FRONT),
            (X_MAX + e, Y_MIN, Z_REAR),
            (X_MAX + e, Y_MAX, Z_REAR),
            (X_MAX + e, Y_MAX, Z_FRONT),
        ],
        textures["right"],
    )
    add_plane(
        scene,
        "LeftIndependentAppearance",
        [
            (X_MIN - e, Y_MIN, Z_REAR),
            (X_MIN - e, Y_MIN, Z_FRONT),
            (X_MIN - e, Y_MAX, Z_FRONT),
            (X_MIN - e, Y_MAX, Z_REAR),
        ],
        textures["left"],
    )
    # Imagegen top/bottom orientation: front at image top.
    add_plane(
        scene,
        "Top_SourceLockedAppearance",
        [
            (X_MIN, Y_MAX + e, Z_FRONT),
            (X_MAX, Y_MAX + e, Z_FRONT),
            (X_MAX, Y_MAX + e, Z_REAR),
            (X_MIN, Y_MAX + e, Z_REAR),
        ],
        textures["top"],
    )
    add_plane(
        scene,
        "Bottom_GenericFallbackAppearance",
        [
            (X_MAX, Y_MIN - e, Z_FRONT),
            (X_MIN, Y_MIN - e, Z_FRONT),
            (X_MIN, Y_MIN - e, Z_REAR),
            (X_MAX, Y_MIN - e, Z_REAR),
        ],
        textures["bottom"],
    )


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
            if material.pbrMetallicRoughness:
                material.pbrMetallicRoughness.baseColorFactor = [1.0, 1.0, 1.0, 1.0]
                material.pbrMetallicRoughness.metallicFactor = 0.0
    document.save_binary(str(path))


def build(web: bool) -> Path:
    scene = trimesh.Scene(base_frame="HPE_DL360G9_Xright_Yup_Zfront")
    scene.metadata.update(
        {
            "manufacturer": "Hewlett Packard Enterprise",
            "product": "HPE ProLiant DL360 Gen9",
            "variant": "755258-B21 8SFF / 2.5-inch, 8 carriers, no bezel, blank PCIe/FlexibleLOM, dual 500W AC PSU",
            "dimensions_mm": "body 434.7 x 43.2 x 698.5; front-ear span 482.6; total depth with 4 mm front relief and 21 mm rear PSU handles 723.5",
            "coordinate_convention": "+X device right, +Y up, +Z front",
            "source_lock": "user screenshot row 7 + HPE maintenance guide c04441985 + exact-device real photos",
            "build_type": "new exact-appearance exterior replica; documented generic-bottom fallback only",
        }
    )
    add_chassis_and_ears(scene, web)
    add_front(scene, web)
    add_rear(scene, web)
    add_top_side_geometry(scene, web)
    add_textured_faces(scene, web)

    MODEL.mkdir(parents=True, exist_ok=True)
    output = MODEL / (WEB_NAME if web else STANDARD_NAME)
    output.write_bytes(scene.export(file_type="glb", include_normals=True))
    patch_unlit_textures(output)
    print(f"{output.name}: bytes={output.stat().st_size} geometry_nodes={len(scene.geometry)}")
    return output


def main() -> None:
    build(web=False)
    build(web=True)


if __name__ == "__main__":
    main()
