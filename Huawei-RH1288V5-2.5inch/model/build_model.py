#!/usr/bin/env python3
"""Build exact-configuration Huawei 1288H V5 10SFF standard/web GLBs.

The optional xFusion iV3D resource is not imported.  Geometry and texture crops
are newly built from the approved six canonical views and feature inventory.
"""

from __future__ import annotations

import argparse
import io
import json
import math
import struct
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable

import mapbox_earcut
import numpy as np
from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
VIEWS = ROOT / "views"
MODEL = ROOT / "model"
TEXTURES = MODEL / "textures"

# Millimetres.  Export converts to metres, the normal glTF unit.
BODY_W = 436.0
BODY_H = 43.0
BODY_D = 708.0
FRONT_SPAN = 482.6
REAR_PROJECTION = 6.0
EAR_EXT = (FRONT_SPAN - BODY_W) / 2.0
Z_FRONT = BODY_D / 2.0
Z_REAR = -BODY_D / 2.0
Z_REAR_OUT = Z_REAR - REAR_PROJECTION


def align4(value: int) -> int:
    return (value + 3) & ~3


def rgba_crop(path: Path) -> Image.Image:
    image = Image.open(path).convert("RGBA")
    bbox = image.getchannel("A").point(lambda v: 255 if v > 8 else 0).getbbox()
    if not bbox:
        raise RuntimeError(f"empty alpha mask: {path}")
    return image.crop(bbox)


def opaque_rgb(image: Image.Image) -> Image.Image:
    rgba = np.asarray(image.convert("RGBA"), dtype=np.uint8)
    alpha = rgba[..., 3]
    opaque = alpha >= 128
    if np.any(opaque):
        fill = np.median(rgba[..., :3][opaque], axis=0).astype(np.uint8)
    else:
        fill = np.array([128, 128, 128], dtype=np.uint8)
    a = rgba[..., 3:4].astype(np.float32) / 255.0
    rgb = (rgba[..., :3].astype(np.float32) * a + fill * (1.0 - a)).round().astype(np.uint8)
    return Image.fromarray(rgb, "RGB")


def fit_long_edge(image: Image.Image, long_edge: int, *, upscale: bool = False) -> Image.Image:
    current = max(image.size)
    if current == long_edge or (current < long_edge and not upscale):
        return image
    scale = long_edge / current
    size = (max(1, round(image.width * scale)), max(1, round(image.height * scale)))
    return image.resize(size, Image.Resampling.LANCZOS)


def prepare_textures() -> dict[str, dict[str, Path]]:
    front = rgba_crop(VIEWS / "front.png")
    ear_px = round(front.width * EAR_EXT / FRONT_SPAN)
    source = {
        "front-left-ear": opaque_rgb(front.crop((0, 0, ear_px, front.height))),
        "front-body": opaque_rgb(front.crop((ear_px, 0, front.width - ear_px, front.height))),
        "front-right-ear": opaque_rgb(front.crop((front.width - ear_px, 0, front.width, front.height))),
        "rear": opaque_rgb(rgba_crop(VIEWS / "rear.png")),
        "left": opaque_rgb(rgba_crop(VIEWS / "left.png")),
        "right": opaque_rgb(rgba_crop(VIEWS / "right.png")),
        "top": opaque_rgb(rgba_crop(VIEWS / "top.png")),
        "bottom": opaque_rgb(rgba_crop(VIEWS / "bottom.png")),
    }
    outputs: dict[str, dict[str, Path]] = {"standard": {}, "web": {}}
    for flavor in outputs:
        directory = TEXTURES / flavor
        directory.mkdir(parents=True, exist_ok=True)
        for name, image in source.items():
            if flavor == "standard":
                if "ear" in name:
                    prepared = fit_long_edge(image, 1024, upscale=True)
                else:
                    prepared = image
            else:
                target = 1536 if name in {"top", "bottom"} else 2048
                if "ear" in name:
                    target = 1024
                prepared = fit_long_edge(image, target, upscale=True)
            path = directory / f"{name}.png"
            prepared.save(path, optimize=True)
            outputs[flavor][name] = path
    return outputs


@dataclass
class Geometry:
    positions: list[tuple[float, float, float]] = field(default_factory=list)
    normals: list[tuple[float, float, float]] = field(default_factory=list)
    uvs: list[tuple[float, float]] = field(default_factory=list)
    indices: list[int] = field(default_factory=list)

    def quad(
        self,
        vertices: Iterable[tuple[float, float, float]],
        normal: tuple[float, float, float],
        uvs: Iterable[tuple[float, float]] | None = None,
    ) -> None:
        base = len(self.positions)
        vertices = list(vertices)
        self.positions.extend(vertices)
        self.normals.extend([normal] * 4)
        self.uvs.extend(list(uvs) if uvs is not None else [(0.0, 0.0)] * 4)
        self.indices.extend([base, base + 1, base + 2, base, base + 2, base + 3])

    def triangle(
        self,
        vertices: Iterable[tuple[float, float, float]],
        normal: tuple[float, float, float],
        uvs: Iterable[tuple[float, float]] | None = None,
    ) -> None:
        base = len(self.positions)
        vertices = list(vertices)
        self.positions.extend(vertices)
        self.normals.extend([normal] * 3)
        self.uvs.extend(list(uvs) if uvs is not None else [(0.0, 0.0)] * 3)
        self.indices.extend([base, base + 1, base + 2])


def add_box(group: Geometry, center: tuple[float, float, float], size: tuple[float, float, float]) -> None:
    cx, cy, cz = center
    sx, sy, sz = (value / 2.0 for value in size)
    x0, x1 = cx - sx, cx + sx
    y0, y1 = cy - sy, cy + sy
    z0, z1 = cz - sz, cz + sz
    group.quad([(x1, y0, z0), (x1, y1, z0), (x1, y1, z1), (x1, y0, z1)], (1, 0, 0))
    group.quad([(x0, y0, z1), (x0, y1, z1), (x0, y1, z0), (x0, y0, z0)], (-1, 0, 0))
    group.quad([(x0, y1, z0), (x0, y1, z1), (x1, y1, z1), (x1, y1, z0)], (0, 1, 0))
    group.quad([(x0, y0, z1), (x0, y0, z0), (x1, y0, z0), (x1, y0, z1)], (0, -1, 0))
    group.quad([(x0, y0, z1), (x1, y0, z1), (x1, y1, z1), (x0, y1, z1)], (0, 0, 1))
    group.quad([(x1, y0, z0), (x0, y0, z0), (x0, y1, z0), (x1, y1, z0)], (0, 0, -1))


def add_cylinder_z(
    group: Geometry,
    cx: float,
    cy: float,
    z0: float,
    z1: float,
    radius: float,
    segments: int = 32,
) -> None:
    # Caps and walls; z0 is rearward, z1 is frontward.
    for i in range(segments):
        a0 = 2 * math.pi * i / segments
        a1 = 2 * math.pi * (i + 1) / segments
        p0 = (cx + radius * math.cos(a0), cy + radius * math.sin(a0), z0)
        p1 = (cx + radius * math.cos(a1), cy + radius * math.sin(a1), z0)
        q0 = (p0[0], p0[1], z1)
        q1 = (p1[0], p1[1], z1)
        group.triangle([(cx, cy, z0), p1, p0], (0, 0, -1))
        group.triangle([(cx, cy, z1), q0, q1], (0, 0, 1))
        mid = (a0 + a1) / 2
        normal = (math.cos(mid), math.sin(mid), 0)
        group.quad([p0, q0, q1, p1], normal)


def add_cylinder_x(
    group: Geometry,
    x0: float,
    x1: float,
    cy: float,
    cz: float,
    radius: float,
    segments: int = 24,
) -> None:
    for i in range(segments):
        a0 = 2 * math.pi * i / segments
        a1 = 2 * math.pi * (i + 1) / segments
        p0 = (x0, cy + radius * math.cos(a0), cz + radius * math.sin(a0))
        p1 = (x0, cy + radius * math.cos(a1), cz + radius * math.sin(a1))
        q0 = (x1, p0[1], p0[2])
        q1 = (x1, p1[1], p1[2])
        group.triangle([(x0, cy, cz), p0, p1], (-1, 0, 0))
        group.triangle([(x1, cy, cz), q1, q0], (1, 0, 0))
        mid = (a0 + a1) / 2
        normal = (0, math.cos(mid), math.sin(mid))
        group.quad([p0, q0, q1, p1], normal)


def uv_front(x: float, y: float) -> tuple[float, float]:
    return ((x + BODY_W / 2) / BODY_W, 1.0 - (y + BODY_H / 2) / BODY_H)


def rear_x(screen_u: float) -> float:
    return BODY_W / 2 - BODY_W * screen_u


def add_front_texture_quad(group: Geometry, x0: float, x1: float, y0: float, y1: float, z: float) -> None:
    group.quad(
        [(x0, y0, z), (x1, y0, z), (x1, y1, z), (x0, y1, z)],
        (0, 0, 1),
        [uv_front(x0, y0), uv_front(x1, y0), uv_front(x1, y1), uv_front(x0, y1)],
    )


def add_rear_texture_quad(
    group: Geometry, u0: float, u1: float, y0: float, y1: float, z: float
) -> None:
    x0, x1 = rear_x(u0), rear_x(u1)
    v0 = 1.0 - (y0 + BODY_H / 2) / BODY_H
    v1 = 1.0 - (y1 + BODY_H / 2) / BODY_H
    group.quad(
        [(x0, y0, z), (x1, y0, z), (x1, y1, z), (x0, y1, z)],
        (0, 0, -1),
        [(u0, v0), (u1, v0), (u1, v1), (u0, v1)],
    )


def add_rear_texture_with_holes(
    group: Geometry,
    u0: float,
    u1: float,
    y0: float,
    y1: float,
    z: float,
    *,
    circle_holes: list[tuple[float, float, float, float]] | None = None,
    rect_holes: list[tuple[float, float, float, float]] | None = None,
) -> None:
    """Add a rear-facing textured panel with actual circular/rectangular openings."""
    rings: list[list[tuple[float, float]]] = [[(u0, y0), (u1, y0), (u1, y1), (u0, y1)]]
    for cu, cy, ru, ry in circle_holes or []:
        rings.append([
            (cu + ru * math.cos(-2 * math.pi * i / 40), cy + ry * math.sin(-2 * math.pi * i / 40))
            for i in range(40)
        ])
    for hu0, hu1, hy0, hy1 in rect_holes or []:
        rings.append([(hu0, hy0), (hu0, hy1), (hu1, hy1), (hu1, hy0)])
    vertices_2d = np.asarray([point for ring in rings for point in ring], dtype=np.float64)
    ends = np.cumsum([len(ring) for ring in rings], dtype=np.uint32)
    triangles = np.asarray(mapbox_earcut.triangulate_float64(vertices_2d, ends), dtype=np.int64).reshape(-1, 3)
    for tri in triangles:
        points = [tuple(vertices_2d[index]) for index in tri]
        vertices = [(rear_x(u), y, z) for u, y in points]
        cross_z = float(np.cross(np.subtract(vertices[1], vertices[0]), np.subtract(vertices[2], vertices[0]))[2])
        if cross_z > 0:
            points[1], points[2] = points[2], points[1]
            vertices[1], vertices[2] = vertices[2], vertices[1]
        uvs = [(u, 1.0 - (y + BODY_H / 2) / BODY_H) for u, y in points]
        group.triangle(vertices, (0, 0, -1), uvs)


def add_rear_bar(
    group: Geometry,
    cx: float,
    cy: float,
    z: float,
    length: float,
    width: float,
    angle: float,
) -> None:
    dx, dy = math.cos(angle) * length / 2, math.sin(angle) * length / 2
    px, py = -math.sin(angle) * width / 2, math.cos(angle) * width / 2
    p0 = (cx - dx - px, cy - dy - py, z)
    p1 = (cx + dx - px, cy + dy - py, z)
    p2 = (cx + dx + px, cy + dy + py, z)
    p3 = (cx - dx + px, cy - dy + py, z)
    group.quad([p0, p3, p2, p1], (0, 0, -1))


def ear_meshes(
    xmin: float,
    xmax: float,
    holes: list[tuple[float, float, float]],
) -> tuple[Geometry, Geometry]:
    ymin, ymax = -BODY_H / 2, BODY_H / 2
    outer = [(xmin, ymin), (xmax, ymin), (xmax, ymax), (xmin, ymax)]
    rings: list[list[tuple[float, float]]] = [outer]
    for cx, cy, radius in holes:
        rings.append(
            [
                (cx + radius * math.cos(-2 * math.pi * i / 32), cy + radius * math.sin(-2 * math.pi * i / 32))
                for i in range(32)
            ]
        )
    vertices_2d = np.asarray([p for ring in rings for p in ring], dtype=np.float64)
    ends = np.cumsum([len(ring) for ring in rings], dtype=np.uint32)
    triangles = np.asarray(mapbox_earcut.triangulate_float64(vertices_2d, ends), dtype=np.int64).reshape(-1, 3)
    front = Geometry()
    side = Geometry()
    zf, zb = Z_FRONT, Z_FRONT - 3.0

    def uv(p: tuple[float, float]) -> tuple[float, float]:
        return ((p[0] - xmin) / (xmax - xmin), 1.0 - (p[1] - ymin) / (ymax - ymin))

    for tri in triangles:
        pts = [tuple(vertices_2d[index]) for index in tri]
        cross = (pts[1][0] - pts[0][0]) * (pts[2][1] - pts[0][1]) - (pts[1][1] - pts[0][1]) * (pts[2][0] - pts[0][0])
        if cross < 0:
            pts[1], pts[2] = pts[2], pts[1]
        front.triangle([(x, y, zf) for x, y in pts], (0, 0, 1), [uv(p) for p in pts])
        side.triangle([(pts[0][0], pts[0][1], zb), (pts[2][0], pts[2][1], zb), (pts[1][0], pts[1][1], zb)], (0, 0, -1))

    # Outer walls and hole walls.  Use geometric normals and winding.
    for ring_index, ring in enumerate(rings):
        hole_center = holes[ring_index - 1][:2] if ring_index else None
        for i, a in enumerate(ring):
            b = ring[(i + 1) % len(ring)]
            dx, dy = b[0] - a[0], b[1] - a[1]
            if hole_center is None:
                nx, ny = dy, -dx
            else:
                mx, my = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2
                nx, ny = hole_center[0] - mx, hole_center[1] - my
            length = math.hypot(nx, ny) or 1.0
            normal = (nx / length, ny / length, 0)
            verts = [(b[0], b[1], zf), (a[0], a[1], zf), (a[0], a[1], zb), (b[0], b[1], zb)]
            # Ensure the first triangle points roughly toward the chosen normal.
            e1 = np.subtract(verts[1], verts[0])
            e2 = np.subtract(verts[2], verts[0])
            if float(np.dot(np.cross(e1, e2), normal)) < 0:
                verts = [verts[1], verts[0], verts[3], verts[2]]
            side.quad(verts, normal)
    return front, side


class GLBBuilder:
    def __init__(self, name: str) -> None:
        self.name = name
        self.binary = bytearray()
        self.buffer_views: list[dict] = []
        self.accessors: list[dict] = []
        self.images: list[dict] = []
        self.textures: list[dict] = []
        self.materials: list[dict] = []
        self.meshes: list[dict] = []
        self.nodes: list[dict] = []
        self.triangle_count = 0

    def blob(self, payload: bytes, *, target: int | None = None, name: str | None = None) -> int:
        offset = align4(len(self.binary))
        self.binary.extend(b"\0" * (offset - len(self.binary)))
        self.binary.extend(payload)
        view = {"buffer": 0, "byteOffset": offset, "byteLength": len(payload)}
        if target:
            view["target"] = target
        if name:
            view["name"] = name
        self.buffer_views.append(view)
        return len(self.buffer_views) - 1

    def accessor(self, array: np.ndarray, component_type: int, kind: str, *, target: int, name: str) -> int:
        array = np.ascontiguousarray(array)
        view = self.blob(array.tobytes(), target=target, name=f"{name} buffer")
        count = int(array.shape[0])
        item = {
            "bufferView": view,
            "byteOffset": 0,
            "componentType": component_type,
            "count": count,
            "type": kind,
            "name": name,
        }
        if kind == "VEC3":
            item["min"] = [float(value) for value in array.min(axis=0)]
            item["max"] = [float(value) for value in array.max(axis=0)]
        self.accessors.append(item)
        return len(self.accessors) - 1

    def texture_material(self, name: str, path: Path) -> int:
        view = self.blob(path.read_bytes(), name=f"{name} PNG")
        self.images.append({"name": name, "bufferView": view, "mimeType": "image/png"})
        image_index = len(self.images) - 1
        self.textures.append({"name": name, "sampler": 0, "source": image_index})
        texture_index = len(self.textures) - 1
        self.materials.append(
            {
                "name": name,
                "pbrMetallicRoughness": {
                    "baseColorFactor": [1, 1, 1, 1],
                    "baseColorTexture": {"index": texture_index},
                    "metallicFactor": 0,
                    "roughnessFactor": 1,
                },
                "alphaMode": "OPAQUE",
                "doubleSided": False,
                "extensions": {"KHR_materials_unlit": {}},
            }
        )
        return len(self.materials) - 1

    def color_material(self, name: str, rgba: tuple[float, float, float, float]) -> int:
        rgb = tuple(max(0, min(255, round(channel * 255))) for channel in rgba[:3])
        stream = io.BytesIO()
        Image.new("RGB", (1024, 1024), rgb).save(stream, format="PNG", optimize=True)
        view = self.blob(stream.getvalue(), name=f"{name} solid-color PNG")
        self.images.append({"name": f"{name} solid color", "bufferView": view, "mimeType": "image/png"})
        image_index = len(self.images) - 1
        self.textures.append({"name": f"{name} solid color", "sampler": 0, "source": image_index})
        texture_index = len(self.textures) - 1
        self.materials.append(
            {
                "name": name,
                "pbrMetallicRoughness": {
                    "baseColorFactor": [1, 1, 1, 1],
                    "baseColorTexture": {"index": texture_index},
                    "metallicFactor": 0,
                    "roughnessFactor": 1,
                },
                "alphaMode": "OPAQUE",
                "doubleSided": False,
                "extensions": {"KHR_materials_unlit": {}},
            }
        )
        return len(self.materials) - 1

    def mesh(self, name: str, geometry: Geometry, material: int) -> int:
        if not geometry.indices:
            raise RuntimeError(f"empty geometry: {name}")
        positions = np.asarray(geometry.positions, dtype=np.float32) / 1000.0
        normals = np.asarray(geometry.normals, dtype=np.float32)
        uvs = np.asarray(geometry.uvs, dtype=np.float32)
        indices = np.asarray(geometry.indices, dtype=np.uint32)
        self.triangle_count += len(indices) // 3
        pos = self.accessor(positions, 5126, "VEC3", target=34962, name=f"{name} POSITION")
        nor = self.accessor(normals, 5126, "VEC3", target=34962, name=f"{name} NORMAL")
        uv = self.accessor(uvs, 5126, "VEC2", target=34962, name=f"{name} TEXCOORD_0")
        ind = self.accessor(indices, 5125, "SCALAR", target=34963, name=f"{name} indices")
        self.meshes.append(
            {
                "name": name,
                "primitives": [
                    {
                        "attributes": {"POSITION": pos, "NORMAL": nor, "TEXCOORD_0": uv},
                        "indices": ind,
                        "material": material,
                        "mode": 4,
                    }
                ],
            }
        )
        mesh_index = len(self.meshes) - 1
        self.nodes.append({"name": name, "mesh": mesh_index})
        return len(self.nodes) - 1

    def write(self, path: Path, extras: dict) -> dict:
        document = {
            "asset": {
                "version": "2.0",
                "generator": "OpenAI Codex exact-appearance GLB builder",
                "copyright": "Newly constructed project model; Huawei marks retained as factual product detail",
            },
            "extensionsUsed": ["KHR_materials_unlit"],
            "scene": 0,
            "scenes": [{"name": "Huawei 1288H V5 10SFF", "nodes": list(range(len(self.nodes)))}],
            "nodes": self.nodes,
            "meshes": self.meshes,
            "materials": self.materials,
            "samplers": [{"magFilter": 9729, "minFilter": 9987, "wrapS": 33071, "wrapT": 33071}],
            "textures": self.textures,
            "images": self.images,
            "accessors": self.accessors,
            "bufferViews": self.buffer_views,
            "buffers": [{"byteLength": len(self.binary)}],
            "extras": extras,
        }
        json_bytes = json.dumps(document, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
        json_bytes += b" " * (align4(len(json_bytes)) - len(json_bytes))
        binary = bytes(self.binary)
        binary += b"\0" * (align4(len(binary)) - len(binary))
        total = 12 + 8 + len(json_bytes) + 8 + len(binary)
        payload = bytearray(struct.pack("<4sII", b"glTF", 2, total))
        payload.extend(struct.pack("<II", len(json_bytes), 0x4E4F534A))
        payload.extend(json_bytes)
        payload.extend(struct.pack("<II", len(binary), 0x004E4942))
        payload.extend(binary)
        path.write_bytes(payload)
        return {
            "path": str(path),
            "bytes": len(payload),
            "nodes": len(self.nodes),
            "meshes": len(self.meshes),
            "primitives": len(self.meshes),
            "materials": len(self.materials),
            "textures": len(self.textures),
            "images": len(self.images),
            "triangles": self.triangle_count,
        }


def build(flavor: str, texture_paths: dict[str, Path], output: Path) -> dict:
    glb = GLBBuilder(f"Huawei 1288H V5 10SFF {flavor}")
    tex = {name: glb.texture_material(name, path) for name, path in texture_paths.items()}
    mat = {
        "metal": glb.color_material("galvanized metal relief", (0.57, 0.59, 0.60, 1)),
        "silver": glb.color_material("bright metal", (0.76, 0.78, 0.79, 1)),
        "dark": glb.color_material("dark metal", (0.08, 0.09, 0.095, 1)),
        "black": glb.color_material("black polymer", (0.018, 0.02, 0.022, 1)),
        "green": glb.color_material("Huawei lime release accent", (0.74, 0.88, 0.08, 1)),
        "blue": glb.color_material("connector blue", (0.02, 0.25, 0.62, 1)),
        "smoke": glb.color_material("smoked display", (0.03, 0.035, 0.038, 1)),
    }

    # Closed opaque core.
    core = Geometry()
    # Keep the hidden closed core well behind every photographic/relief layer.
    # The previous +/-353 mm Z caps were exactly coplanar with several front
    # relief caps and could win/lose the depth test while orbiting.
    add_box(core, (0, 0, 0), (BODY_W - 2.0, BODY_H - 2.0, BODY_D - 12.0))
    glb.mesh("Closed chassis shell", core, mat["metal"])

    # Six canonical opaque faces.  The front base is recessed so modeled bays/controls carry relief.
    front_base = Geometry()
    add_front_texture_quad(front_base, -BODY_W / 2, BODY_W / 2, -BODY_H / 2, BODY_H / 2, Z_FRONT - 5.0)
    glb.mesh("Front body source-locked base", front_base, tex["front-body"])

    rear_base = Geometry()
    add_rear_texture_quad(rear_base, 0, 1, -BODY_H / 2, BODY_H / 2, Z_REAR)
    glb.mesh("Rear source-locked base", rear_base, tex["rear"])

    left_face = Geometry()
    left_face.quad(
        [(-BODY_W / 2, -BODY_H / 2, Z_REAR), (-BODY_W / 2, -BODY_H / 2, Z_FRONT),
         (-BODY_W / 2, BODY_H / 2, Z_FRONT), (-BODY_W / 2, BODY_H / 2, Z_REAR)],
        (-1, 0, 0), [(0, 1), (1, 1), (1, 0), (0, 0)],
    )
    glb.mesh("Physical left non-mirrored face", left_face, tex["left"])

    right_face = Geometry()
    right_face.quad(
        [(BODY_W / 2, -BODY_H / 2, Z_FRONT), (BODY_W / 2, -BODY_H / 2, Z_REAR),
         (BODY_W / 2, BODY_H / 2, Z_REAR), (BODY_W / 2, BODY_H / 2, Z_FRONT)],
        (1, 0, 0), [(0, 1), (1, 1), (1, 0), (0, 0)],
    )
    glb.mesh("Physical right non-mirrored face", right_face, tex["right"])

    top_face = Geometry()
    top_face.quad(
        [(-BODY_W / 2, BODY_H / 2, Z_FRONT), (BODY_W / 2, BODY_H / 2, Z_FRONT),
         (BODY_W / 2, BODY_H / 2, Z_REAR), (-BODY_W / 2, BODY_H / 2, Z_REAR)],
        (0, 1, 0), [(0, 1), (1, 1), (1, 0), (0, 0)],
    )
    glb.mesh("Top closed cover face", top_face, tex["top"])

    bottom_face = Geometry()
    bottom_face.quad(
        [(BODY_W / 2, -BODY_H / 2, Z_FRONT), (-BODY_W / 2, -BODY_H / 2, Z_FRONT),
         (-BODY_W / 2, -BODY_H / 2, Z_REAR), (BODY_W / 2, -BODY_H / 2, Z_REAR)],
        (0, -1, 0), [(0, 1), (1, 1), (1, 0), (0, 0)],
    )
    glb.mesh("Conservative generic-bottom fallback face", bottom_face, tex["bottom"])

    # Front rack ears with actual circular through-holes, no rear ears.
    left_ear_front, left_ear_side = ear_meshes(
        -FRONT_SPAN / 2, -BODY_W / 2, [(-FRONT_SPAN / 2 + 7.1, 11.8, 3.8)]
    )
    right_ear_front, right_ear_side = ear_meshes(
        BODY_W / 2, FRONT_SPAN / 2,
        [(FRONT_SPAN / 2 - 7.1, 11.8, 3.8), (FRONT_SPAN / 2 - 7.2, -7.2, 2.1)],
    )
    glb.mesh("Front left Huawei branded rack ear true-hole face", left_ear_front, tex["front-left-ear"])
    glb.mesh("Front left rack ear extrusion", left_ear_side, mat["dark"])
    glb.mesh("Front right 1288H V5 rack ear true-hole face", right_ear_front, tex["front-right-ear"])
    glb.mesh("Front right rack ear extrusion", right_ear_side, mat["dark"])

    # Ten separately relieved 2.5-inch carrier/filler faces: 5 columns x 2 rows.
    carriers = Geometry()
    carrier_faces = Geometry()
    handles = Geometry()
    handle_faces = Geometry()
    accents = Geometry()
    x_start, x_end, gap = -207.0, 143.0, 2.0
    carrier_w = (x_end - x_start - 4 * gap) / 5
    rows = [(-18.5, -0.75), (0.75, 18.5)]
    for row_y0, row_y1 in rows:
        for column in range(5):
            x0 = x_start + column * (carrier_w + gap)
            x1 = x0 + carrier_w
            add_box(carriers, ((x0 + x1) / 2, (row_y0 + row_y1) / 2, Z_FRONT - 2.65),
                    (x1 - x0, row_y1 - row_y0, 4.5))
            add_front_texture_quad(carrier_faces, x0, x1, row_y0, row_y1, Z_FRONT - 0.1)
            add_box(handles, (x1 - 6.2, (row_y0 + row_y1) / 2, Z_FRONT),
                    (10.0, row_y1 - row_y0 - 1.1, 0.4))
            add_front_texture_quad(handle_faces, x1 - 11.2, x1 - 1.2,
                                   row_y0 + 0.55, row_y1 - 0.55, Z_FRONT + 0.45)
            add_box(accents, (x1 - 12.0, (row_y0 + row_y1) / 2, Z_FRONT - 0.35),
                    (1.35, row_y1 - row_y0 - 0.8, 0.6))
    glb.mesh("Ten SFF carrier recessed bodies", carriers, mat["black"])
    glb.mesh("Ten SFF carrier source-matched fronts", carrier_faces, tex["front-body"])
    glb.mesh("Ten carrier handle and latch reliefs", handles, mat["dark"])
    glb.mesh("Ten carrier source-matched handle fronts", handle_faces, tex["front-body"])
    glb.mesh("Ten carrier lime release accents", accents, mat["green"])

    control_body = Geometry()
    add_box(control_body, (177.0, 0, Z_FRONT - 3.0), (58.0, 39.0, 4.0))
    glb.mesh("Front control panel recessed body", control_body, mat["black"])
    control_face = Geometry()
    add_front_texture_quad(control_face, 148.0, 206.0, -19.5, 19.5, Z_FRONT)
    glb.mesh("Front control panel source-matched face", control_face, tex["front-body"])

    # Rear stamped covers and requested blank option state.
    rear_relief = Geometry(); rear_relief_faces = Geometry()
    rear_rects = [
        (0.035, 0.208, 2.0, 18.0, -356.2, "PCIe slot 1"),
        (0.235, 0.374, 2.0, 18.0, -356.2, "PCIe slot 2"),
        (0.405, 0.681, 2.0, 18.0, -356.2, "PCIe slot 3"),
        (0.025, 0.205, -18.0, -2.2, -355.5, "optional LOM1/2 blank"),
        (0.435, 0.701, -18.0, -2.2, -355.5, "FlexIO blank"),
    ]
    for u0, u1, y0, y1, z, _ in rear_rects:
        x0, x1 = rear_x(u0), rear_x(u1)
        add_box(rear_relief, ((x0 + x1) / 2, (y0 + y1) / 2, (Z_REAR + z) / 2),
                (abs(x1 - x0), y1 - y0, abs(z - Z_REAR)))
        # A 0.30 mm evidence-neutral stand-off keeps the source-locked cover
        # skin in front of the stamped solid instead of nearly coplanar.
        add_rear_texture_quad(rear_relief_faces, u0, u1, y0, y1, z - 0.30)
    glb.mesh("Three PCIe covers plus empty LOM and FlexIO geometry", rear_relief, mat["metal"])
    glb.mesh("Rear cover source-matched faces", rear_relief_faces, tex["rear"])

    # Fixed service I/O: VGA, four RJ45, two stacked USB.
    service_panel = Geometry(); service_dark = Geometry(); service_blue = Geometry()
    service_holes: list[tuple[float, float, float, float]] = []
    # VGA blue insert behind a source-textured metal strip opening.
    vx = rear_x(0.175)
    service_holes.append((0.175 - 7.0 / BODY_W, 0.175 + 7.0 / BODY_W, -13.8, -6.2))
    add_box(service_blue, (vx, -10.0, -357.6), (12.0, 6.5, 0.8))
    # Four sockets, left-to-right in the rear image.
    for u in (0.245, 0.278, 0.311, 0.344):
        x = rear_x(u)
        service_holes.append((u - 5.0 / BODY_W, u + 5.0 / BODY_W, -14.2, -4.8))
        add_box(service_dark, (x, -9.5, -357.6), (8.5, 8.0, 0.8))
    # USB stacked pair.
    ux = rear_x(0.397)
    for y in (-14.2, -5.8):
        service_holes.append((0.397 - 4.2 / BODY_W, 0.397 + 4.2 / BODY_W, y - 2.2, y + 2.2))
        add_box(service_dark, (ux, y, -357.5), (8.0, 4.4, 0.8))
        add_box(service_blue, (ux, y, -357.95), (6.5, 2.7, 0.4))
    add_rear_texture_with_holes(service_panel, 0.135, 0.415, -18.2, -3.2, -358.5,
                                rect_holes=service_holes)
    glb.mesh("Rear source-matched service strip with true connector openings", service_panel, tex["rear"])
    glb.mesh("Rear RJ45 and USB recesses", service_dark, mat["black"])
    glb.mesh("Rear VGA and USB blue inserts", service_blue, mat["blue"])

    # Two identical hot-swap AC PSU modules with textured faces and physical fan/inlet/handle relief.
    psu_bodies = Geometry(); psu_faces = Geometry(); fans = Geometry(); grilles = Geometry(); inlets = Geometry()
    psu_ranges = [(0.713, 0.852), (0.858, 0.997)]
    for u0, u1 in psu_ranges:
        x0, x1 = rear_x(u0), rear_x(u1)
        psu_body_back = Z_REAR_OUT + 1.0
        add_box(psu_bodies, ((x0 + x1) / 2, 0, (Z_REAR + psu_body_back) / 2),
                (abs(x1 - x0), 41.0, abs(psu_body_back - Z_REAR)))
        fan_u = u0 + (u1 - u0) * 0.32
        inlet_u = u0 + (u1 - u0) * 0.76
        fan_x = rear_x(fan_u)
        inlet_x = rear_x(inlet_u)
        inlet_u_half = 9.0 / BODY_W
        add_rear_texture_with_holes(
            psu_faces, u0, u1, -20.0, 20.0, Z_REAR_OUT,
            circle_holes=[(fan_u, 0.0, 15.0 / BODY_W, 15.0)],
            rect_holes=[(inlet_u - inlet_u_half, inlet_u + inlet_u_half, -13.0, 7.5)],
        )
        add_box(fans, (fan_x, 0, Z_REAR_OUT + 0.55), (29.2, 29.2, 0.6))
        for angle in (0, math.pi / 2, math.pi / 4, -math.pi / 4):
            add_rear_bar(grilles, fan_x, 0, Z_REAR_OUT + 0.25, 27.0, 1.2, angle)
        add_box(inlets, (inlet_x, -2.75, Z_REAR_OUT + 0.55), (19.0, 22.0, 0.6))
    glb.mesh("Two identical hot-swap AC PSU module bodies", psu_bodies, mat["metal"])
    glb.mesh("Two AC PSU source-matched faces", psu_faces, tex["rear"])
    glb.mesh("Two recessed PSU fan cavities", fans, mat["black"])
    glb.mesh("Two PSU fan grille relief groups", grilles, mat["silver"])
    glb.mesh("Two IEC C14 inlet recesses", inlets, mat["black"])

    # The two dense vent bands remain in the approved opaque high-resolution
    # top texture.  Their old solid caps ended exactly on the same plane as the
    # texture and were a deterministic z-fighting source; dense flush slots are
    # permitted texture detail and do not need a second coincident mesh layer.
    top_relief = Geometry()
    add_box(top_relief, (0, BODY_H / 2 - 0.20, 90.0), (25.0, 0.9, 34.0))
    add_box(top_relief, (0, BODY_H / 2 + 0.10, 90.0), (10.0, 0.3, 24.0))
    add_box(top_relief, (0, BODY_H / 2 - 0.15, 298.0), (BODY_W - 4.0, 0.8, 1.4))
    add_box(top_relief, (-138.0, BODY_H / 2 - 0.20, -340.0), (110.0, 0.9, 26.0))
    add_box(top_relief, (75.0, BODY_H / 2 - 0.20, -338.0), (150.0, 0.9, 30.0))
    glb.mesh("Top latch seam and stepped rear cover relief", top_relief, mat["metal"])

    # Distinct physical-left and physical-right wall relief; patterns are intentionally not mirrored.
    side_fasteners = Geometry(); side_slots = Geometry(); side_lips = Geometry()
    for z, radius in [(-250, 3.0), (-90, 2.6), (80, 3.0), (245, 2.7)]:
        add_cylinder_x(side_fasteners, -BODY_W / 2 - 0.25, -BODY_W / 2 + 0.8, 0, z, radius)
    for z, radius in [(-300, 2.5), (-150, 3.0), (15, 2.6), (165, 3.0), (300, 2.5)]:
        add_cylinder_x(side_fasteners, BODY_W / 2 - 0.8, BODY_W / 2 + 0.25, 0, z, radius)
    for x, z in [(-BODY_W / 2 + 0.10, -315), (-BODY_W / 2 + 0.10, 270),
                 (BODY_W / 2 - 0.10, -275), (BODY_W / 2 - 0.10, -30), (BODY_W / 2 - 0.10, 285)]:
        add_box(side_slots, (x, 0, z), (0.7, 4.0, 18.0))
    add_box(side_lips, (-BODY_W / 2 + 0.10, BODY_H / 2 - 0.9, 0), (0.7, 1.5, BODY_D - 1.0))
    add_box(side_lips, (BODY_W / 2 - 0.10, BODY_H / 2 - 0.9, 0), (0.7, 1.5, BODY_D - 1.0))
    glb.mesh("Independent left and right wall fastener relief", side_fasteners, mat["metal"])
    glb.mesh("Independent left and right wall rail-slot relief", side_slots, mat["dark"])
    glb.mesh("Black top lips on both side walls", side_lips, mat["dark"])

    extras = {
        "exactProduct": "Huawei FusionServer Pro 1288H V5 Server",
        "catalogAlias": "Huawei RH1288V5/2.5-inch",
        "installedConfiguration": "1U 10 x 2.5-inch; 3-I/O rear; FlexIO and optional LOM unpopulated; two identical AC PSUs",
        "coordinateConvention": "+X device right from front, +Y up, +Z front",
        "bodyDimensionsMm": [BODY_W, BODY_H, BODY_D],
        "overallBoundsMm": [FRONT_SPAN, BODY_H, BODY_D + REAR_PROJECTION],
        "bottomProductionMode": "GENERIC_BOTTOM_FALLBACK",
        "optionalOfficialAssetImported": False,
        "geometryPolicy": "closed shell plus separately relieved identity-bearing exterior assemblies",
    }
    return glb.write(output, extras)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--flavor", choices=("standard", "web", "both"), default="both")
    args = parser.parse_args()
    MODEL.mkdir(parents=True, exist_ok=True)
    textures = prepare_textures()
    flavors = ("standard", "web") if args.flavor == "both" else (args.flavor,)
    reports = []
    for flavor in flavors:
        suffix = "" if flavor == "standard" else "-web"
        output = MODEL / f"Huawei-RH1288V5-2.5inch{suffix}.glb"
        reports.append(build(flavor, textures[flavor], output))
    report = {
        "identity": "Huawei FusionServer Pro 1288H V5 1U 10SFF",
        "configuration": "3-I/O rear; LOM/FlexIO empty; dual same-type AC",
        "body_mm": [BODY_W, BODY_H, BODY_D],
        "overall_mm": [FRONT_SPAN, BODY_H, BODY_D + REAR_PROJECTION],
        "models": reports,
        "visible_geometry_groups": [
            "closed chassis shell", "six distinct opaque face surfaces", "two front-only rack ears with true holes",
            "ten SFF carriers with handle/latch/accent relief", "front control panel relief with source-matched flush display/buttons/USB",
            "three PCIe covers", "empty LOM and FlexIO covers", "VGA/four RJ45/two USB",
            "two identical AC PSU bodies/fan cavities/grilles/C14 inlets/releases",
            "opaque source-locked top vent bands plus separated latch/seam/rear-step relief", "independent non-mirrored side fasteners/slots/lips",
        ],
        "bottom_status": "GENERIC_BOTTOM_FALLBACK",
        "official_iv3d_imported": False,
    }
    (MODEL / "build-report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
