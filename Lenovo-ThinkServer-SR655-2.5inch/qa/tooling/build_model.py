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
TEXTURES = ROOT / "qa/tooling/model-textures"

BODY_W = 0.4446
OVERALL_W = 0.4820
HEIGHT = 0.0865
OVERALL_D = 0.7647
FRONT_PROJECTION = 0.0340
Z_MAX = OVERALL_D / 2.0
Z_MIN = -OVERALL_D / 2.0
FLANGE_Z = Z_MAX - FRONT_PROJECTION
CORE_SHELL_INSET = 0.0024
PHOTO_SKIN_INSET = 0.0012
FACE_PHOTO_INSET = 0.0016
FRAME_FACE_INSET = 0.0008
BODY_REAR_Z = Z_MIN + CORE_SHELL_INSET
BODY_D = FLANGE_Z - BODY_REAR_Z
BODY_Z = (FLANGE_Z + BODY_REAR_Z) / 2.0
EAR_W = (OVERALL_W - BODY_W) / 2.0


STANDARD_NAME = "Lenovo-ThinkServer-SR655-2.5inch.glb"
WEB_NAME = "Lenovo-ThinkServer-SR655-2.5inch-web.glb"


COLORS = {
    "silver": (172, 176, 176, 255),
    "light_silver": (205, 207, 205, 255),
    "dark_silver": (107, 112, 113, 255),
    "black": (18, 19, 20, 255),
    "dark": (32, 34, 35, 255),
    "vent": (6, 7, 8, 255),
    "red": (173, 12, 21, 255),
    "blue": (8, 91, 183, 255),
    "orange": (236, 94, 8, 255),
    "green": (58, 150, 52, 255),
    "yellow": (229, 199, 10, 255),
}


def pbr_color(name: str, rgba: tuple[int, int, int, int], roughness: float = 0.72) -> PBRMaterial:
    factor = [v / 255.0 for v in rgba]
    return PBRMaterial(
        name=name,
        baseColorFactor=factor,
        metallicFactor=0.0,
        roughnessFactor=roughness,
        alphaMode="OPAQUE",
        doubleSided=False,
    )


MATERIALS = {name: pbr_color(name, rgba) for name, rgba in COLORS.items()}


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


def make_rgb_texture(face: str, web: bool) -> Image.Image:
    source = Image.open(VIEWS / f"{face}.png").convert("RGBA")
    fills = {
        "front": (16, 17, 18, 255),
        "rear": (184, 187, 186, 255),
        "left": (175, 178, 177, 255),
        "right": (175, 178, 177, 255),
        "top": (177, 180, 179, 255),
        "bottom": (166, 168, 167, 255),
    }
    background = Image.new("RGBA", source.size, fills[face])
    composed = Image.alpha_composite(background, source).convert("RGB")
    if web:
        composed.thumbnail((2048, 2048), Image.Resampling.LANCZOS)
    out_dir = TEXTURES / ("web" if web else "standard")
    out_dir.mkdir(parents=True, exist_ok=True)
    composed.save(out_dir / f"{face}.png", optimize=True)
    return composed


def add_chassis_geometry(scene: trimesh.Scene) -> None:
    # Keep the watertight core behind the evidence-locked photographic skins.
    # The former 0.08 mm separation was not stable under orbit depth precision.
    add_box(
        scene,
        "ChassisBody",
        (BODY_W - 2 * CORE_SHELL_INSET, HEIGHT - 2 * CORE_SHELL_INSET, BODY_D),
        (0.0, 0.0, BODY_Z),
        "silver",
    )
    # Separate black front latch/ear assemblies, present only at the front plane.
    for side, sign in (("Left", -1.0), ("Right", 1.0)):
        x = sign * (BODY_W / 2.0 + EAR_W / 2.0)
        # The full-height black face is carried by the exact front photograph.
        # Only its top/bottom mechanical depth is solid geometry. A full-height
        # block would project as a false rear ear in an orthographic rear view.
        add_box(scene, f"Front{side}LatchTopCap", (EAR_W * 0.86, 0.012, 0.038), (x, HEIGHT / 2.0 - 0.006, FLANGE_Z + 0.015), "dark")
        add_box(scene, f"Front{side}LatchBottomCap", (EAR_W * 0.86, 0.012, 0.038), (x, -HEIGHT / 2.0 + 0.006, FLANGE_Z + 0.015), "dark")
    # Chassis corner folds and long side lips are visible in three-quarter views.
    add_box(scene, "TopRightSideLip", (0.006, 0.006, 0.705), (BODY_W / 2.0 + 0.001, HEIGHT / 2.0 - 0.003, BODY_Z), "light_silver")
    add_box(scene, "TopLeftSideLip", (0.006, 0.006, 0.705), (-BODY_W / 2.0 - 0.001, HEIGHT / 2.0 - 0.003, BODY_Z), "light_silver")


def add_front_geometry(scene: trimesh.Scene) -> None:
    # B5VJ front: one row of twenty-four narrow SFF carriers, positions 0-23.
    region_min, region_max = -0.205, 0.205
    gap_x = 0.0008
    cell_w = (region_max - region_min - 23 * gap_x) / 24.0
    cell_h = 0.066
    z_face = Z_MAX
    for idx in range(24):
        x = region_min + cell_w / 2.0 + idx * (cell_w + gap_x)
        y = 0.0
        frame_w = cell_w * 0.95
        frame_h = cell_h
        side_bar = min(0.0012, frame_w * 0.10)
        top_bar = 0.0020
        depth = 0.010
        center_z = z_face - FRAME_FACE_INSET - depth / 2.0
        name = f"SFFCarrier_{idx:02d}"
        # Open frame, handle and top accent provide real recess/parallax while
        # the exact photographic texture retains the dense perforation.
        add_box(scene, f"{name}_Top", (frame_w, top_bar, depth), (x, frame_h / 2.0 - top_bar / 2.0, center_z), "black")
        add_box(scene, f"{name}_Bottom", (frame_w, top_bar, depth), (x, -frame_h / 2.0 + top_bar / 2.0, center_z), "black")
        side_h = frame_h - 2 * top_bar
        add_box(scene, f"{name}_Left", (side_bar, side_h, depth), (x - frame_w / 2.0 + side_bar / 2.0, y, center_z), "black")
        add_box(scene, f"{name}_Right", (side_bar, side_h, depth), (x + frame_w / 2.0 - side_bar / 2.0, y, center_z), "black")
        add_box(scene, f"{name}_Handle", (frame_w * 0.56, 0.0020, 0.014), (x, -frame_h * 0.27, z_face - 0.007), "dark")
        add_box(scene, f"{name}_RedAccent", (frame_w * 0.88, 0.0015, 0.012), (x, frame_h * 0.42, z_face - 0.006), "red")

    # VGA, USB and status controls are flush, sub-centimetre face details. Keep
    # them in the approved high-resolution front texture; protruding boxes here
    # would expose false blue/metal side walls in a straight rear projection.


def add_rear_geometry(scene: trimesh.Scene) -> None:
    z_face = Z_MIN
    # Screen-left to right at the rear maps to physical +X to -X.
    banks = [
        ("BankA", 0.157, 3, 0.102),
        ("BankB", 0.022, 3, 0.098),
        ("BankC", -0.105, 2, 0.098),
    ]
    row_y = [0.027, 0.007, -0.013]
    for bank, x, rows, slot_w in banks:
        for row in range(rows):
            y = row_y[row]
            slot_h = 0.014
            depth = 0.010
            center_z = z_face + FRAME_FACE_INSET + depth / 2.0
            bar = 0.0016
            name = f"RearPCIe_{bank}_{row+1}"
            add_box(scene, f"{name}_Top", (slot_w, bar, depth), (x, y + slot_h / 2.0, center_z), "light_silver")
            add_box(scene, f"{name}_Bottom", (slot_w, bar, depth), (x, y - slot_h / 2.0, center_z), "light_silver")
            side_h = slot_h - 2 * bar
            add_box(scene, f"{name}_Left", (bar, side_h, depth), (x + slot_w / 2.0, y, center_z), "dark_silver")
            add_box(scene, f"{name}_Right", (bar, side_h, depth), (x - slot_w / 2.0, y, center_z), "dark_silver")
            add_box(scene, f"{name}_HandleLip", (slot_w * 0.80, 0.0012, 0.013), (x, y - slot_h * 0.30, z_face + 0.0065), "dark_silver")
    for i, x in enumerate((0.096, -0.045, -0.165), 1):
        add_box(scene, f"RearBankDivider{i}", (0.013, 0.060, 0.014), (x, 0.010, z_face + 0.007), "silver")

    # Two identical 750W AC hot-swap PSU modules, each with fan, C14 and handle.
    for i, x in enumerate((-0.120, -0.191), 1):
        add_box(scene, f"PSU{i}_Body", (0.064, 0.039, 0.024), (x, -0.023, z_face + 0.012), "light_silver")
        add_cylinder(scene, f"PSU{i}_FanRing", 0.0160, 0.010, (x - 0.012, -0.023, z_face + 0.005), "black", axis="z", sections=32)
        add_cylinder(scene, f"PSU{i}_FanHub", 0.0070, 0.011, (x - 0.012, -0.023, z_face + 0.0055), "dark_silver", axis="z", sections=32)
        add_box(scene, f"PSU{i}_C14Inlet", (0.020, 0.023, 0.012), (x + 0.019, -0.021, z_face + 0.006), "vent")
        add_box(scene, f"PSU{i}_OrangeHandle", (0.006, 0.027, 0.013), (x + 0.029, -0.024, z_face + 0.0065), "orange")
        for led, yy in enumerate((-0.013, -0.020, -0.027), 1):
            add_cylinder(scene, f"PSU{i}_LED{led}", 0.0018, 0.006, (x + 0.031, yy, z_face + 0.003), "green", axis="z", sections=12)

    # Exact lower I/O order.
    io_y = -0.031
    for idx, x in enumerate((0.205, 0.189), 1):
        add_box(scene, f"OCPPort{idx}", (0.013, 0.011, 0.010), (x, io_y, z_face + 0.005), "vent")
    add_cylinder(scene, "RearErrorLED", 0.0023, 0.006, (0.168, io_y, z_face + 0.003), "dark", axis="z", sections=12)
    add_box(scene, "RearBMC_RJ45", (0.015, 0.012, 0.010), (0.145, io_y, z_face + 0.005), "vent")
    add_cylinder(scene, "RearLocatorLED", 0.0018, 0.006, (0.128, io_y, z_face + 0.003), "blue", axis="z", sections=12)
    add_box(scene, "RearVGA", (0.021, 0.011, 0.010), (0.104, io_y, z_face + 0.005), "blue")
    for idx, y in enumerate((-0.026, -0.036), 1):
        add_box(scene, f"RearUSB{idx}", (0.013, 0.007, 0.010), (0.078, y, z_face + 0.005), "blue")
    add_box(scene, "RearSerialDB9", (0.022, 0.011, 0.010), (0.050, io_y, z_face + 0.005), "vent")
    add_cylinder(scene, "RearNMI", 0.0018, 0.006, (0.031, io_y, z_face + 0.003), "dark", axis="z", sections=12)


def add_side_top_bottom_geometry(scene: trimesh.Scene) -> None:
    right_x = BODY_W / 2.0
    left_x = -BODY_W / 2.0
    # Independently documented right side; it carries the yellow warning label.
    add_box(scene, "RightUpperRailLip", (0.005, 0.007, 0.590), (right_x, 0.031, -0.015), "light_silver")
    for idx, z in enumerate((0.255, 0.070, -0.110, -0.285), 1):
        add_cylinder(scene, f"RightRaisedBoss{idx}", 0.0040, 0.004, (right_x, -0.010, z), "light_silver", axis="x", sections=24)
    for idx, (y, z) in enumerate(((0.026, 0.300), (0.015, 0.220), (0.022, 0.010), (0.018, -0.180), (-0.018, -0.310)), 1):
        add_cylinder(scene, f"RightScrew{idx}", 0.00125, 0.0044, (right_x, y, z), "dark_silver", axis="x", sections=16)
    add_box(scene, "RightWarningLabelRelief", (0.0020, 0.012, 0.034), (right_x + 0.0003, 0.004, 0.205), "yellow")

    # Independently documented left side. Its boss/hole spacing is not mirrored
    # from the right and it has no yellow warning label.
    add_box(scene, "LeftUpperRailLip", (0.005, 0.007, 0.590), (left_x, 0.031, -0.015), "light_silver")
    for idx, z in enumerate((0.285, 0.145, -0.055, -0.245), 1):
        add_cylinder(scene, f"LeftRaisedBoss{idx}", 0.0040, 0.004, (left_x, -0.010, z), "light_silver", axis="x", sections=24)
    for idx, (y, z) in enumerate(((0.025, 0.315), (0.014, 0.260), (0.021, 0.180), (0.016, 0.090), (0.020, -0.020), (0.018, -0.135), (-0.016, -0.235), (-0.020, -0.300)), 1):
        add_cylinder(scene, f"LeftScrew{idx}", 0.00125, 0.0044, (left_x, y, z), "dark_silver", axis="x", sections=16)
    # Two small left-side rectangular slots near the rear.
    add_box(scene, "LeftSideSlot1", (0.004, 0.004, 0.010), (left_x, -0.020, -0.300), "vent")
    add_box(scene, "LeftSideSlot2", (0.004, 0.004, 0.010), (left_x, -0.028, -0.300), "vent")

    # The photographed cover already carries the shallow stamped seams. They do
    # not change silhouette at the target web distance; geometry rims obscured
    # label pixels and looked like synthetic outlines. Keep the projecting latch.
    top_y = HEIGHT / 2.0
    # Keep the dense rear vent in the exact opaque texture; do not cover it
    # with a flat generic plate.
    add_box(scene, "TopReleaseLatch", (0.052, 0.006, 0.016), (0.072, top_y - 0.0033, -0.215), "black")
    add_box(scene, "TopReleaseLatchBlueTab", (0.010, 0.007, 0.012), (0.050, top_y - 0.00355, -0.215), "blue")

    # The bottom skin and core close the body; avoid a duplicate full plate.
    bottom_y = -HEIGHT / 2.0
    add_box(scene, "BottomStampedSeamFront", (BODY_W - 0.012, 0.0016, 0.004), (0.0, bottom_y + 0.0009, 0.160), "dark_silver")
    add_box(scene, "BottomStampedSeamRear", (BODY_W - 0.012, 0.0016, 0.004), (0.0, bottom_y + 0.0009, -0.120), "dark_silver")


def add_textured_faces(scene: trimesh.Scene, textures: dict[str, Image.Image]) -> None:
    side_x = BODY_W / 2.0 - PHOTO_SKIN_INSET
    top_y = HEIGHT / 2.0 - PHOTO_SKIN_INSET
    bottom_y = -HEIGHT / 2.0 + PHOTO_SKIN_INSET
    front_z = Z_MAX - FACE_PHOTO_INSET
    rear_z = Z_MIN + FACE_PHOTO_INSET
    # Front (+Z), image left is physical -X.
    add_plane(scene, "FrontPhotographicSurface", [
        (-OVERALL_W / 2, -HEIGHT / 2, front_z),
        (OVERALL_W / 2, -HEIGHT / 2, front_z),
        (OVERALL_W / 2, HEIGHT / 2, front_z),
        (-OVERALL_W / 2, HEIGHT / 2, front_z),
    ], textures["front"])
    # Rear (-Z): natural rear screen-left is physical +X.
    add_plane(scene, "RearPhotographicSurface", [
        (BODY_W / 2, -HEIGHT / 2, rear_z),
        (-BODY_W / 2, -HEIGHT / 2, rear_z),
        (-BODY_W / 2, HEIGHT / 2, rear_z),
        (BODY_W / 2, HEIGHT / 2, rear_z),
    ], textures["rear"])
    # Right (+X), front edge at image left.
    add_plane(scene, "RightPhotographicSurface", [
        (side_x, -HEIGHT / 2, Z_MAX),
        (side_x, -HEIGHT / 2, Z_MIN),
        (side_x, HEIGHT / 2, Z_MIN),
        (side_x, HEIGHT / 2, Z_MAX),
    ], textures["right"])
    # Left (-X), rear edge at image left and front edge at image right.
    add_plane(scene, "LeftPhotographicSurface", [
        (-side_x, -HEIGHT / 2, Z_MIN),
        (-side_x, -HEIGHT / 2, Z_MAX),
        (-side_x, HEIGHT / 2, Z_MAX),
        (-side_x, HEIGHT / 2, Z_MIN),
    ], textures["left"])
    # Top (+Y), front edge at image top.
    add_plane(scene, "TopPhotographicSurface", [
        (BODY_W / 2, top_y, Z_MIN),
        (-BODY_W / 2, top_y, Z_MIN),
        (-BODY_W / 2, top_y, Z_MAX),
        (BODY_W / 2, top_y, Z_MAX),
    ], textures["top"])
    # Bottom (-Y), front edge at image top with natural bottom left/right reversal.
    add_plane(scene, "BottomPhotographicSurface", [
        (-BODY_W / 2, bottom_y, Z_MIN),
        (BODY_W / 2, bottom_y, Z_MIN),
        (BODY_W / 2, bottom_y, Z_MAX),
        (-BODY_W / 2, bottom_y, Z_MAX),
    ], textures["bottom"])


def build(web: bool) -> Path:
    scene = trimesh.Scene(base_frame="SR655_RH_Xright_Yup_Zfront")
    scene.metadata.update({
        "manufacturer": "Lenovo",
        "product": "ThinkSystem SR655",
        "variant": "B5VJ 24x2.5 SFF carrier exterior, 8-slot PCIe-rich rear, 2x750W AC",
        "coordinate_convention": "+X device right, +Y up, +Z front",
        "build_type": "newly constructed exact exterior replica; rotation-stable layered skins; official viewer mesh not copied",
    })
    add_chassis_geometry(scene)
    add_front_geometry(scene)
    add_rear_geometry(scene)
    add_side_top_bottom_geometry(scene)
    textures = {face: make_rgb_texture(face, web) for face in ("front", "rear", "left", "right", "top", "bottom")}
    add_textured_faces(scene, textures)
    MODEL.mkdir(parents=True, exist_ok=True)
    out = MODEL / (WEB_NAME if web else STANDARD_NAME)
    glb = scene.export(file_type="glb", include_normals=True)
    out.write_bytes(glb)
    # Photo-derived surfaces should match the approved sRGB face assets in
    # neutral website viewers. Keep all structural/relief materials PBR, while
    # making only the six embedded photographic materials unlit.
    document = GLTF2().load_binary(str(out))
    used = list(document.extensionsUsed or [])
    if "KHR_materials_unlit" not in used:
        used.append("KHR_materials_unlit")
    document.extensionsUsed = used
    for material in document.materials or []:
        if material.name and material.name.endswith("_opaque_texture"):
            extensions = dict(material.extensions or {})
            extensions["KHR_materials_unlit"] = {}
            material.extensions = extensions
    document.save_binary(str(out))
    print(out, out.stat().st_size, "geometry", len(scene.geometry))
    return out


def main() -> None:
    build(web=False)
    build(web=True)


if __name__ == "__main__":
    main()
