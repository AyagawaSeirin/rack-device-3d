#!/usr/bin/env python3
"""Build exact-appearance standard/web GLBs for the locked R7515 assembly."""

from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont
from pygltflib import GLTF2
import trimesh
from trimesh.visual.material import PBRMaterial


ROOT = Path(__file__).resolve().parents[1]
VIEWS = ROOT / "views"
MODEL = ROOT / "model"
TEXTURES = ROOT / "qa" / "work" / "model-textures"
MANIFEST = ROOT / "qa" / "build-manifest.json"
FONT_REGULAR = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

# All dimensions are millimetres in evidence, metres in glTF.
BODY_WIDTH = 434.0
FRONT_WIDTH = 482.0
HEIGHT = 86.8
BODY_DEPTH = 647.07
FRONT_PROJECTION = 22.0
REAR_PROJECTION = 34.685
FULL_DEPTH = 703.755
FRONT_Z = BODY_DEPTH / 2.0
REAR_Z = -BODY_DEPTH / 2.0
FRONT_OUTER_Z = FRONT_Z + FRONT_PROJECTION
REAR_OUTER_Z = REAR_Z - REAR_PROJECTION


def m(value_mm: float) -> float:
    return value_mm / 1000.0


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def tight_crop(image: Image.Image) -> Image.Image:
    rgba = image.convert("RGBA")
    bbox = rgba.getchannel("A").point(lambda a: 255 if a > 8 else 0).getbbox()
    if bbox is None:
        raise ValueError("transparent source")
    return rgba.crop(bbox)


def crop_production_face(face: str) -> Image.Image:
    image = Image.open(VIEWS / f"{face}.png").convert("RGBA")
    if face == "left":
        # Full face has rear 34.685 mm and front 22 mm projections. The GLB
        # models those separately; this crop binds only the 647.07 mm wall.
        return image.crop((159, 8, 2977, 386))
    if face == "right":
        return image.crop((104, 8, 2922, 387))
    return tight_crop(image)


def flatten_opaque(image: Image.Image, fill: tuple[int, int, int]) -> Image.Image:
    rgba = image.convert("RGBA")
    background = Image.new("RGBA", rgba.size, (*fill, 255))
    background.alpha_composite(rgba)
    return background.convert("RGB")


def make_info_tag(size: tuple[int, int]) -> Image.Image:
    width, height = size
    image = Image.new("RGB", size, (22, 25, 27))
    draw = ImageDraw.Draw(image)
    draw.rounded_rectangle(
        (2, 2, width - 3, height - 3),
        radius=max(2, height // 12),
        outline=(112, 118, 121),
        width=max(1, height // 36),
    )

    # Use the exact official Dell information-tag wordmark as the logo mask.
    crop = Image.open(ROOT / "qa" / "work" / "dell-wordmark-crop.png").convert("RGB")
    mark = crop.crop((28, 72, 74, 158)).rotate(90, expand=True)
    data = np.array(mark)
    gray = data.mean(axis=2)
    mask = Image.fromarray(np.where(gray > 198, 255, 0).astype(np.uint8), mode="L")
    mark_rgba = Image.new("RGBA", mark.size, (238, 240, 241, 0))
    mark_rgba.putalpha(mask)
    logo_target_h = round(height * 0.50)
    logo_target_w = round(mark_rgba.width * logo_target_h / mark_rgba.height)
    mark_rgba = mark_rgba.resize((logo_target_w, logo_target_h), Image.Resampling.LANCZOS)
    image.paste(mark_rgba, (round(width * 0.035), round(height * 0.24)), mark_rgba)

    draw = ImageDraw.Draw(image)
    title_font = ImageFont.truetype(FONT_BOLD, round(height * 0.22))
    model_font = ImageFont.truetype(FONT_REGULAR, round(height * 0.17))
    text_x = round(width * 0.28)
    draw.text((text_x, round(height * 0.20)), "PowerEdge", font=title_font, fill=(236, 238, 239))
    draw.text((text_x, round(height * 0.52)), "R7515", font=model_font, fill=(210, 215, 217))
    return image


def prepare_textures(variant: str) -> dict[str, Path]:
    output = TEXTURES / variant
    output.mkdir(parents=True, exist_ok=True)
    long_edge = 3072 if variant == "standard" else 2048
    fill = {
        "front": (22, 25, 27),
        "rear": (156, 161, 162),
        "left": (149, 153, 154),
        "right": (149, 153, 154),
        "top": (179, 183, 184),
        "bottom": (170, 174, 175),
    }
    paths: dict[str, Path] = {}
    for face in ("front", "rear", "left", "right", "top", "bottom"):
        path = output / f"{face}.png"
        source_view = VIEWS / f"{face}.png"
        if path.exists() and path.stat().st_mtime_ns >= source_view.stat().st_mtime_ns:
            paths[face] = path
            continue
        image = flatten_opaque(crop_production_face(face), fill[face])
        scale = long_edge / max(image.size)
        size = tuple(max(1, round(dimension * scale)) for dimension in image.size)
        image = image.resize(size, Image.Resampling.LANCZOS)
        image.save(path, optimize=True)
        paths[face] = path
    tag_path = output / "info-tag.png"
    if not tag_path.exists():
        make_info_tag((1024, 256)).save(tag_path, optimize=True)
    paths["info_tag"] = tag_path
    return paths


def pbr_material(
    name: str,
    color: tuple[int, int, int, int],
    *,
    metallic: float = 0.0,
    roughness: float = 0.78,
) -> PBRMaterial:
    return PBRMaterial(
        name=name,
        baseColorFactor=np.array(color, dtype=np.uint8),
        metallicFactor=metallic,
        roughnessFactor=roughness,
        doubleSided=False,
        alphaMode="OPAQUE",
    )


def texture_material(name: str, path: Path) -> PBRMaterial:
    return PBRMaterial(
        name=f"Tex_{name}",
        baseColorFactor=np.array([255, 255, 255, 255], dtype=np.uint8),
        baseColorTexture=Image.open(path).convert("RGB"),
        metallicFactor=0.0,
        roughnessFactor=0.82,
        doubleSided=False,
        alphaMode="OPAQUE",
    )


def apply_material(mesh: trimesh.Trimesh, material: PBRMaterial) -> trimesh.Trimesh:
    mesh.visual = trimesh.visual.TextureVisuals(
        uv=np.zeros((len(mesh.vertices), 2), dtype=np.float64),
        material=material,
    )
    return mesh


def box_mesh(
    extents_mm: tuple[float, float, float],
    center_mm: tuple[float, float, float],
    material: PBRMaterial,
) -> trimesh.Trimesh:
    mesh = trimesh.creation.box(extents=[m(v) for v in extents_mm])
    mesh.apply_translation([m(v) for v in center_mm])
    return apply_material(mesh, material)


def cylinder_mesh(
    radius_mm: float,
    height_mm: float,
    center_mm: tuple[float, float, float],
    material: PBRMaterial,
    *,
    axis: str = "z",
    sections: int = 24,
) -> trimesh.Trimesh:
    mesh = trimesh.creation.cylinder(radius=m(radius_mm), height=m(height_mm), sections=sections)
    if axis == "x":
        mesh.apply_transform(trimesh.transformations.rotation_matrix(math.pi / 2, [0, 1, 0]))
    elif axis == "y":
        mesh.apply_transform(trimesh.transformations.rotation_matrix(math.pi / 2, [1, 0, 0]))
    mesh.apply_translation([m(v) for v in center_mm])
    return apply_material(mesh, material)


def torus_mesh(
    major_mm: float,
    minor_mm: float,
    center_mm: tuple[float, float, float],
    material: PBRMaterial,
) -> trimesh.Trimesh:
    mesh = trimesh.creation.torus(
        major_radius=m(major_mm),
        minor_radius=m(minor_mm),
        major_sections=28,
        minor_sections=10,
    )
    mesh.apply_translation([m(v) for v in center_mm])
    return apply_material(mesh, material)


class TextureBatch:
    """One material/image per face with disconnected source-locked quads."""

    def __init__(self, material: PBRMaterial):
        self.material = material
        self.vertices: list[list[float]] = []
        self.faces: list[list[int]] = []
        self.uv: list[list[float]] = []

    def _append(self, vertices: list[list[float]], uv: list[list[float]]) -> None:
        offset = len(self.vertices)
        self.vertices.extend(vertices)
        self.uv.extend(uv)
        self.faces.extend([[offset, offset + 1, offset + 2], [offset, offset + 2, offset + 3]])

    def front(
        self,
        x0: float,
        x1: float,
        y0: float,
        y1: float,
        z: float,
        uv_rect: tuple[float, float, float, float] = (0, 0, 1, 1),
    ) -> None:
        u0, v0, u1, v1 = uv_rect
        self._append(
            [[m(x0), m(y0), m(z)], [m(x1), m(y0), m(z)], [m(x1), m(y1), m(z)], [m(x0), m(y1), m(z)]],
            [[u0, 1.0 - v1], [u1, 1.0 - v1], [u1, 1.0 - v0], [u0, 1.0 - v0]],
        )

    def rear(
        self,
        x0: float,
        x1: float,
        y0: float,
        y1: float,
        z: float,
        uv_rect: tuple[float, float, float, float] = (0, 0, 1, 1),
    ) -> None:
        u0, v0, u1, v1 = uv_rect
        self._append(
            [[m(x1), m(y0), m(z)], [m(x0), m(y0), m(z)], [m(x0), m(y1), m(z)], [m(x1), m(y1), m(z)]],
            [[u0, 1.0 - v1], [u1, 1.0 - v1], [u1, 1.0 - v0], [u0, 1.0 - v0]],
        )

    def left(self, y0: float, y1: float, z0: float, z1: float, x: float) -> None:
        self._append(
            [[m(x), m(y0), m(z0)], [m(x), m(y0), m(z1)], [m(x), m(y1), m(z1)], [m(x), m(y1), m(z0)]],
            [[0, 0], [1, 0], [1, 1], [0, 1]],
        )

    def right(self, y0: float, y1: float, z0: float, z1: float, x: float) -> None:
        self._append(
            [[m(x), m(y0), m(z1)], [m(x), m(y0), m(z0)], [m(x), m(y1), m(z0)], [m(x), m(y1), m(z1)]],
            [[0, 0], [1, 0], [1, 1], [0, 1]],
        )

    def top(self, x0: float, x1: float, z0: float, z1: float, y: float) -> None:
        # z1 is front (+Z), z0 is rear (-Z); source front is screen bottom.
        self._append(
            [[m(x0), m(y), m(z1)], [m(x1), m(y), m(z1)], [m(x1), m(y), m(z0)], [m(x0), m(y), m(z0)]],
            [[0, 0], [1, 0], [1, 1], [0, 1]],
        )

    def bottom(self, x0: float, x1: float, z0: float, z1: float, y: float) -> None:
        self._append(
            [[m(x1), m(y), m(z1)], [m(x0), m(y), m(z1)], [m(x0), m(y), m(z0)], [m(x1), m(y), m(z0)]],
            [[0, 0], [1, 0], [1, 1], [0, 1]],
        )

    def mesh(self) -> trimesh.Trimesh:
        mesh = trimesh.Trimesh(
            vertices=np.array(self.vertices, dtype=np.float64),
            faces=np.array(self.faces, dtype=np.int64),
            process=False,
        )
        mesh.visual = trimesh.visual.TextureVisuals(
            uv=np.array(self.uv, dtype=np.float64), material=self.material
        )
        return mesh


def add(scene: trimesh.Scene, mesh: trimesh.Trimesh, name: str, names: list[str]) -> None:
    mesh.metadata["name"] = name
    scene.add_geometry(mesh, node_name=name, geom_name=name)
    names.append(name)


def build_scene(texture_paths: dict[str, Path]) -> tuple[trimesh.Scene, list[str]]:
    materials = {
        "silver": pbr_material("GalvanizedSteel", (156, 161, 162, 255), metallic=0.08, roughness=0.66),
        "silver_dark": pbr_material("GalvanizedSteelDark", (105, 111, 113, 255), metallic=0.06, roughness=0.72),
        "black": pbr_material("DellBlackPlastic", (21, 24, 26, 255), roughness=0.82),
        "deep": pbr_material("OpaqueVentDepth", (5, 7, 8, 255), roughness=0.93),
        "orange": pbr_material("DellOrangeLatch", (224, 82, 22, 255), roughness=0.58),
        "green": pbr_material("DellGreenIndicator", (40, 196, 75, 255), roughness=0.42),
        "blue": pbr_material("ConnectorBlue", (23, 83, 171, 255), metallic=0.0, roughness=0.56),
        "teal": pbr_material("SerialTeal", (24, 104, 103, 255), metallic=0.0, roughness=0.58),
    }
    tex = {name: texture_material(name, path) for name, path in texture_paths.items()}
    scene = trimesh.Scene(base_frame="R7515_Origin")
    names: list[str] = []

    # Closed core, full-dimensional front wings, and bottom folds.
    add(scene, box_mesh((BODY_WIDTH, 84.8, BODY_DEPTH), (0, 0, 0), materials["silver"]), "Chassis_Core_Closed", names)
    add(scene, box_mesh((38, HEIGHT, 20.8), (-222, 0, FRONT_Z + 10.4), materials["black"]), "Front_ControlWing_Left", names)
    add(scene, box_mesh((38, HEIGHT, 20.8), (222, 0, FRONT_Z + 10.4), materials["black"]), "Front_ControlWing_Right", names)
    add(scene, box_mesh((406, 82, 5), (0, 0, FRONT_Z + 2.5), materials["deep"]), "Front_Backplane_Recess", names)
    add(scene, box_mesh((BODY_WIDTH, 1.2, 6), (0, -42.8, 0), materials["silver_dark"]), "Bottom_Fold_Long", names)

    # Front source-locked texture surfaces and separate 12-carrier assemblies.
    front_batch = TextureBatch(tex["front"])
    front_batch.front(-241, -203, -43.3, 43.3, FRONT_OUTER_Z, (0.0, 0.0, 0.118, 1.0))
    front_batch.front(203, 241, -43.3, 43.3, FRONT_OUTER_Z, (0.935, 0.0, 1.0, 1.0))
    drive_x0, drive_x1 = -203.0, 203.0
    drive_u0, drive_u1 = 0.118, 0.935
    col_w = (drive_x1 - drive_x0) / 4.0
    row_h = HEIGHT / 3.0
    for row in range(3):
        y_top = HEIGHT / 2.0 - row * row_h
        y_bottom = y_top - row_h
        v0, v1 = row / 3.0, (row + 1) / 3.0
        for col in range(4):
            x0 = drive_x0 + col * col_w
            x1 = x0 + col_w
            u0 = drive_u0 + col * (drive_u1 - drive_u0) / 4.0
            u1 = drive_u0 + (col + 1) * (drive_u1 - drive_u0) / 4.0
            center_x = (x0 + x1) / 2.0
            center_y = (y_bottom + y_top) / 2.0
            add(scene, box_mesh((col_w - 1.6, row_h - 1.2, 17.5), (center_x, center_y, FRONT_Z + 11.7), materials["black"]), f"DriveCarrier_{row}_{col}", names)
            add(scene, box_mesh((55, 15.0, 2.0), (center_x + 15, center_y, FRONT_OUTER_Z - 1.2), materials["deep"]), f"DriveVentRecess_{row}_{col}", names)
            add(scene, box_mesh((col_w - 4.0, 2.2, 2.8), (center_x, y_bottom + 2.2, FRONT_OUTER_Z - 1.5), materials["silver_dark"]), f"DriveHandle_{row}_{col}", names)
            add(scene, box_mesh((19.0, row_h - 4.0, 2.4), (center_x - 34.0, center_y, FRONT_OUTER_Z - 1.4), materials["black"]), f"DriveLatchBlock_{row}_{col}", names)
            add(scene, torus_mesh(4.2, 1.15, (center_x - 34.0, center_y, FRONT_OUTER_Z - 1.25), materials["orange"]), f"DriveReleaseRing_{row}_{col}", names)
            add(scene, cylinder_mesh(1.15, 1.0, (center_x - 47.0, center_y + 4.3, FRONT_OUTER_Z - 0.6), materials["green"], sections=16), f"DriveLED_A_{row}_{col}", names)
            add(scene, cylinder_mesh(1.15, 1.0, (center_x - 47.0, center_y - 4.3, FRONT_OUTER_Z - 0.6), materials["green"], sections=16), f"DriveLED_B_{row}_{col}", names)
            front_batch.front(x0 + 0.8, x1 - 0.8, y_bottom + 0.6, y_top - 0.6, FRONT_OUTER_Z, (u0, v0, u1, v1))
    add(scene, front_batch.mesh(), "Front_SourceLocked_TextureSurfaces", names)

    # Front control detail relief, pull recesses, and authentic information tag.
    add(scene, box_mesh((28, 20, 3.0), (-222, -15, FRONT_OUTER_Z - 1.6), materials["deep"]), "Front_Left_PullRecess", names)
    add(scene, box_mesh((28, 20, 3.0), (222, -15, FRONT_OUTER_Z - 1.6), materials["deep"]), "Front_Right_PullRecess", names)
    for index, y in enumerate((27, 19, 11, 3, -5)):
        add(scene, cylinder_mesh(1.2, 1.0, (-210, y, FRONT_OUTER_Z - 0.6), materials["green"], sections=16), f"Front_StatusLED_{index + 1}", names)
    add(scene, box_mesh((2.8, 18, 1.5), (-216, 19, FRONT_OUTER_Z - 0.8), materials["blue"]), "Front_QuickSync_Bar", names)
    add(scene, cylinder_mesh(4.0, 1.4, (215, 30, FRONT_OUTER_Z - 0.8), materials["green"], sections=20), "Front_PowerButton", names)
    # The exact source-locked control-wing texture carries the flush USB/VGA/
    # iDRAC sockets and the authentic DELL/PowerEdge tag. Do not cover those
    # identity-bearing details with generic solid port blocks.

    # Opaque side/top/bottom source surfaces. Front/rear projections are geometry.
    left_batch = TextureBatch(tex["left"])
    left_batch.left(-43.3, 43.3, REAR_Z, FRONT_Z, -217.02)
    add(scene, left_batch.mesh(), "Left_SourceLocked_TextureSurface", names)
    right_batch = TextureBatch(tex["right"])
    right_batch.right(-43.3, 43.3, REAR_Z, FRONT_Z, 217.02)
    add(scene, right_batch.mesh(), "Right_SourceLocked_TextureSurface", names)
    top_batch = TextureBatch(tex["top"])
    top_batch.top(-217, 217, REAR_Z, FRONT_Z, 43.39)
    add(scene, top_batch.mesh(), "Top_SourceLocked_TextureSurface", names)
    bottom_batch = TextureBatch(tex["bottom"])
    bottom_batch.bottom(-217, 217, REAR_Z, FRONT_Z, -43.39)
    add(scene, bottom_batch.mesh(), "Bottom_GenericFallback_TextureSurface", names)

    # Independent side relief and hole depths; patterns intentionally differ.
    add(scene, box_mesh((2.0, 21, 260), (-217.7, 7, 70), materials["silver_dark"]), "Left_RailChannel_Relief", names)
    add(scene, box_mesh((2.0, 18, 245), (217.7, 5, -20), materials["silver_dark"]), "Right_RailChannel_Relief", names)
    left_holes = [(-270, 17, 4.0), (-180, -8, 5.0), (-70, 15, 3.8), (40, -7, 5.2), (150, 12, 3.7), (250, -10, 4.2)]
    right_holes = [(-250, -9, 4.2), (-140, 14, 4.8), (-35, -12, 3.7), (80, 11, 5.0), (190, -8, 4.0), (280, 14, 3.5)]
    for index, (z, y, radius) in enumerate(left_holes):
        add(scene, cylinder_mesh(radius, 1.6, (-217.9, y, z), materials["deep"], axis="x", sections=20), f"Left_SideHole_{index + 1}", names)
    for index, (z, y, radius) in enumerate(right_holes):
        add(scene, cylinder_mesh(radius, 1.6, (217.9, y, z), materials["deep"], axis="x", sections=20), f"Right_SideHole_{index + 1}", names)

    # Top cover, label deck, latch, rear ventilation depth, and seams.
    add(scene, box_mesh((430, 0.6, 514), (0, 42.5, -66.5), materials["silver"]), "Top_RemovableCover", names)
    add(scene, box_mesh((430, 0.6, 130), (0, 42.5, 258.5), materials["silver"]), "Top_FixedLabelDeck", names)
    add(scene, box_mesh((20, 1.0, 39), (0, 42.9, 68), materials["black"]), "Top_CoverReleaseLatch", names)
    add(scene, box_mesh((275, 0.8, 12), (35, 42.78, -300), materials["deep"]), "Top_RearVentStrip", names)
    add(scene, box_mesh((430, 0.6, 1.6), (0, 42.55, 193.5), materials["silver_dark"]), "Top_CoverFrontSeam", names)

    # Rear base source surface.
    rear_batch = TextureBatch(tex["rear"])
    rear_batch.rear(-217, 217, -43.3, 43.3, REAR_Z - 0.02)

    # Riser covers, central grille, vertical slots and I/O blocks.  The exact
    # source-locked rear photograph remains visible inside every feature: only
    # thin perimeter bars are added for relief.  Never remap/copy sub-regions or
    # cover the source ports with generic coloured blocks.
    rear_features = [
        ("Rear_Riser1B_Slot2", 135, 17, 135, 16),
        ("Rear_Riser1B_Slot3", 135, -2, 135, 16),
        ("Rear_CentralExhaust", 35, 17, 150, 52),
        ("Rear_PCIeSlot4", -58, 9, 17, 54),
        ("Rear_PCIeSlot5", -81, 9, 17, 54),
        ("Rear_SystemIO_Block", 145, -24, 145, 34),
        ("Rear_OCP_LOM_Block", 20, -27, 70, 18),
    ]
    frame_bar = 1.25
    frame_depth = 1.0
    frame_z = REAR_Z - 0.52
    for feature_name, x, y, width, height in rear_features:
        add(scene, box_mesh((width, frame_bar, frame_depth), (x, y - height / 2 + frame_bar / 2, frame_z), materials["silver_dark"]), f"{feature_name}_FrameBottom", names)
        add(scene, box_mesh((width, frame_bar, frame_depth), (x, y + height / 2 - frame_bar / 2, frame_z), materials["silver_dark"]), f"{feature_name}_FrameTop", names)
        add(scene, box_mesh((frame_bar, height, frame_depth), (x - width / 2 + frame_bar / 2, y, frame_z), materials["silver_dark"]), f"{feature_name}_FrameLeft", names)
        add(scene, box_mesh((frame_bar, height, frame_depth), (x + width / 2 - frame_bar / 2, y, frame_z), materials["silver_dark"]), f"{feature_name}_FrameRight", names)
    add(scene, rear_batch.mesh(), "Rear_SourceLocked_TextureSurfaces", names)

    # Dual AC EPP 750W PSU modules.  Their exact source photograph carries the
    # fan blades/hub text, C14 inlet, handle and label.  A narrow fan rim and the
    # orange release latch provide true visible relief without hiding them.
    psu_width, psu_height = 100.0, 40.0
    psu_depth = REAR_PROJECTION - 0.32
    for row, y in enumerate((21.0, -21.0), start=1):
        add(scene, box_mesh((psu_width, psu_height, psu_depth), (-167, y, REAR_Z - psu_depth / 2), materials["silver"]), f"Rear_AC_PSU_{row}_Module", names)
        v0, v1 = (0.0, 0.5) if row == 1 else (0.5, 1.0)
        psu_batch = TextureBatch(tex["rear"])
        psu_batch.rear(-217, -117, y - psu_height / 2, y + psu_height / 2, REAR_OUTER_Z + 0.02, (0.79, v0, 1.0, v1))
        add(scene, psu_batch.mesh(), f"Rear_AC_PSU_{row}_SourceSurface", names)
        add(scene, torus_mesh(15.0, 0.5, (-191, y, REAR_OUTER_Z + 0.50), materials["deep"]), f"Rear_AC_PSU_{row}_FanRim", names)
        add(scene, box_mesh((3.5, 25, 0.6), (-119.0, y, REAR_OUTER_Z + 0.30), materials["orange"]), f"Rear_AC_PSU_{row}_OrangeLatch", names)

    # Side-visible rear PSU handle loops, front-only wing silhouettes.
    for side_name, x in (("Left", -216.5), ("Right", 216.5)):
        for row, y in enumerate((21.0, -21.0), start=1):
            add(scene, box_mesh((2.0, 12, 31), (x, y, REAR_Z - 19), materials["black"]), f"{side_name}_PSU_HandleLoop_{row}", names)

    return scene, names


def patch_glb(path: Path, variant: str) -> None:
    gltf = GLTF2().load(str(path))
    used = set(gltf.extensionsUsed or [])
    for material in gltf.materials or []:
        if material.name and material.name.startswith("Tex_"):
            material.extensions = dict(material.extensions or {})
            material.extensions["KHR_materials_unlit"] = {}
            material.alphaMode = "OPAQUE"
            material.doubleSided = False
            used.add("KHR_materials_unlit")
    gltf.extensionsUsed = sorted(used)
    gltf.asset.generator = "Codex exact-appearance R7515 exterior builder (trimesh + pygltflib)"
    gltf.asset.extras = {
        "manufacturer": "Dell Technologies",
        "model": "PowerEdge R7515",
        "variant": "12 x 3.5-inch LFF, no bezel, no rear drives, dual EPP 750W AC",
        "build": variant,
        "coordinateConvention": "+X right from front, +Y up, +Z front",
        "bottomMode": "GENERIC_BOTTOM_FALLBACK",
    }
    gltf.save_binary(str(path))


def scene_bounds_mm(scene: trimesh.Scene) -> list[list[float]]:
    bounds = np.array(scene.bounds) * 1000.0
    return [[round(float(value), 6) for value in row] for row in bounds]


def main() -> None:
    MODEL.mkdir(parents=True, exist_ok=True)
    report: dict[str, object] = {
        "identity": "Dell PowerEdge R7515 12x3.5 LFF; no bezel; no rear drives; dual EPP 750W AC",
        "dimensions_mm": {
            "body_width": BODY_WIDTH,
            "front_overall_width": FRONT_WIDTH,
            "height": HEIGHT,
            "body_depth": BODY_DEPTH,
            "front_projection": FRONT_PROJECTION,
            "rear_projection": REAR_PROJECTION,
            "full_depth": FULL_DEPTH,
        },
        "outputs": {},
    }
    for variant, filename in (
        ("standard", "Dell-R7515-3.5inch.glb"),
        ("web", "Dell-R7515-3.5inch-web.glb"),
    ):
        texture_paths = prepare_textures(variant)
        scene, node_names = build_scene(texture_paths)
        output = MODEL / filename
        output.write_bytes(trimesh.exchange.gltf.export_glb(scene, include_normals=True))
        patch_glb(output, variant)
        report["outputs"][variant] = {
            "path": str(output.relative_to(ROOT)),
            "bytes": output.stat().st_size,
            "sha256": sha256(output),
            "bounds_mm": scene_bounds_mm(scene),
            "node_count": len(node_names),
            "node_names": node_names,
            "texture_sha256": {
                name: sha256(path) for name, path in texture_paths.items()
            },
        }
    MANIFEST.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
