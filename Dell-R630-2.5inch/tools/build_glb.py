#!/usr/bin/env python3
"""Construct the source-locked Dell PowerEdge R630 10x2.5 exterior GLBs.

The writer is dependency-light and emits self-contained glTF 2.0 binary files.
Geometry is in metres with +X device-right, +Y up, +Z front.
"""

from __future__ import annotations

import hashlib
import json
import math
import struct
from pathlib import Path
from typing import Iterable, Sequence

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
VIEWS = ROOT / "views"
MODEL = ROOT / "model"


def align4(data: bytearray) -> None:
    while len(data) % 4:
        data.append(0)


class GLBBuilder:
    def __init__(self, profile: str):
        self.profile = profile
        self.bin = bytearray()
        self.doc = {
            "asset": {
                "version": "2.0",
                "generator": "Codex exact-exterior GLB builder",
                "extras": {
                    "manufacturer": "Dell",
                    "model": "PowerEdge R630",
                    "variant": "10x2.5-inch SFF, bezel absent",
                    "rear": "three-riser, quad RJ45, dual matching EPP 1100W AC PSU",
                    "status": "PASS_WITH_BOTTOM_FALLBACK",
                    "coordinateConvention": "+X right, +Y up, +Z front",
                    "dimensionsMm": {"width": 482.4, "height": 42.8, "depth": 752.1},
                    "profile": profile,
                },
            },
            "extensionsUsed": ["KHR_materials_unlit"],
            "scene": 0,
            "scenes": [{"name": "Dell PowerEdge R630 10x2.5", "nodes": []}],
            "nodes": [],
            "meshes": [],
            "materials": [],
            "textures": [],
            "images": [],
            "samplers": [{"magFilter": 9729, "minFilter": 9987, "wrapS": 33071, "wrapT": 33071}],
            "bufferViews": [],
            "accessors": [],
            "buffers": [{"byteLength": 0}],
        }

    def blob(self, data: bytes, target: int | None = None) -> int:
        align4(self.bin)
        off = len(self.bin)
        self.bin.extend(data)
        view = {"buffer": 0, "byteOffset": off, "byteLength": len(data)}
        if target is not None:
            view["target"] = target
        self.doc["bufferViews"].append(view)
        return len(self.doc["bufferViews"]) - 1

    def accessor(self, values: Sequence, component: int, kind: str, target: int) -> int:
        if component == 5126:
            flat = [float(v) for row in values for v in (row if isinstance(row, (list, tuple)) else [row])]
            raw = struct.pack("<" + "f" * len(flat), *flat)
        elif component == 5123:
            flat = [int(v) for v in values]
            raw = struct.pack("<" + "H" * len(flat), *flat)
        else:
            raise ValueError(component)
        view = self.blob(raw, target)
        acc = {"bufferView": view, "componentType": component, "count": len(values), "type": kind}
        if kind == "VEC3" and component == 5126:
            acc["min"] = [min(v[i] for v in values) for i in range(3)]
            acc["max"] = [max(v[i] for v in values) for i in range(3)]
        self.doc["accessors"].append(acc)
        return len(self.doc["accessors"]) - 1

    def material_texture(self, name: str, texture_index: int) -> int:
        mat = {
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
        self.doc["materials"].append(mat)
        return len(self.doc["materials"]) - 1

    def material_solid(self, name: str, rgba: Sequence[float], metallic: float, roughness: float) -> int:
        mat = {
            "name": name,
            "pbrMetallicRoughness": {
                "baseColorFactor": list(rgba),
                "metallicFactor": metallic,
                "roughnessFactor": roughness,
            },
            "alphaMode": "OPAQUE",
            "doubleSided": False,
        }
        self.doc["materials"].append(mat)
        return len(self.doc["materials"]) - 1

    def image_texture(self, name: str, path: Path) -> int:
        raw = path.read_bytes()
        view = self.blob(raw)
        self.doc["images"].append({"name": name, "bufferView": view, "mimeType": "image/jpeg"})
        image_index = len(self.doc["images"]) - 1
        self.doc["textures"].append({"name": name, "sampler": 0, "source": image_index})
        return len(self.doc["textures"]) - 1

    def primitive(
        self,
        name: str,
        positions: Sequence[Sequence[float]],
        normals: Sequence[Sequence[float]],
        uvs: Sequence[Sequence[float]],
        indices: Sequence[int],
        material: int,
    ) -> None:
        p = self.accessor(positions, 5126, "VEC3", 34962)
        n = self.accessor(normals, 5126, "VEC3", 34962)
        t = self.accessor(uvs, 5126, "VEC2", 34962)
        i = self.accessor(indices, 5123, "SCALAR", 34963)
        mesh = {
            "name": name,
            "primitives": [{"attributes": {"POSITION": p, "NORMAL": n, "TEXCOORD_0": t}, "indices": i, "material": material}],
        }
        self.doc["meshes"].append(mesh)
        node = {"name": name, "mesh": len(self.doc["meshes"]) - 1}
        self.doc["nodes"].append(node)
        self.doc["scenes"][0]["nodes"].append(len(self.doc["nodes"]) - 1)

    def box(self, name: str, c: Sequence[float], s: Sequence[float], material: int) -> None:
        cx, cy, cz = c
        hx, hy, hz = (v / 2 for v in s)
        faces = [
            ((0, 0, 1), [(-hx, -hy, hz), (hx, -hy, hz), (hx, hy, hz), (-hx, hy, hz)]),
            ((0, 0, -1), [(hx, -hy, -hz), (-hx, -hy, -hz), (-hx, hy, -hz), (hx, hy, -hz)]),
            ((1, 0, 0), [(hx, -hy, hz), (hx, -hy, -hz), (hx, hy, -hz), (hx, hy, hz)]),
            ((-1, 0, 0), [(-hx, -hy, -hz), (-hx, -hy, hz), (-hx, hy, hz), (-hx, hy, -hz)]),
            ((0, 1, 0), [(-hx, hy, hz), (hx, hy, hz), (hx, hy, -hz), (-hx, hy, -hz)]),
            ((0, -1, 0), [(-hx, -hy, -hz), (hx, -hy, -hz), (hx, -hy, hz), (-hx, -hy, hz)]),
        ]
        pos, nor, uv, idx = [], [], [], []
        for normal, verts in faces:
            base = len(pos)
            pos.extend([(cx + x, cy + y, cz + z) for x, y, z in verts])
            nor.extend([normal] * 4)
            uv.extend([(0, 1), (1, 1), (1, 0), (0, 0)])
            idx.extend([base, base + 1, base + 2, base, base + 2, base + 3])
        self.primitive(name, pos, nor, uv, idx, material)

    def cylinder(self, name: str, c: Sequence[float], radius: float, length: float, axis: str, material: int, segments: int = 20) -> None:
        def m(u: float, v: float, w: float) -> tuple[float, float, float]:
            if axis == "x":
                return c[0] + w, c[1] + u, c[2] + v
            if axis == "y":
                return c[0] + u, c[1] + w, c[2] + v
            return c[0] + u, c[1] + v, c[2] + w

        def mn(u: float, v: float, w: float) -> tuple[float, float, float]:
            if axis == "x":
                return w, u, v
            if axis == "y":
                return u, w, v
            return u, v, w

        pos, nor, uv, idx = [], [], [], []
        half = length / 2
        for k in range(segments):
            a0, a1 = 2 * math.pi * k / segments, 2 * math.pi * (k + 1) / segments
            u0, v0 = radius * math.cos(a0), radius * math.sin(a0)
            u1, v1 = radius * math.cos(a1), radius * math.sin(a1)
            base = len(pos)
            pos.extend([m(u0, v0, -half), m(u1, v1, -half), m(u1, v1, half), m(u0, v0, half)])
            nor.extend([mn(math.cos(a0), math.sin(a0), 0), mn(math.cos(a1), math.sin(a1), 0), mn(math.cos(a1), math.sin(a1), 0), mn(math.cos(a0), math.sin(a0), 0)])
            uv.extend([(0, 1), (1, 1), (1, 0), (0, 0)])
            idx.extend([base, base + 1, base + 2, base, base + 2, base + 3])
        for sign in (-1, 1):
            center = len(pos)
            pos.append(m(0, 0, sign * half))
            nor.append(mn(0, 0, sign))
            uv.append((0.5, 0.5))
            ring = []
            for k in range(segments):
                a = 2 * math.pi * k / segments
                ring.append(len(pos))
                pos.append(m(radius * math.cos(a), radius * math.sin(a), sign * half))
                nor.append(mn(0, 0, sign))
                uv.append(((math.cos(a) + 1) / 2, (math.sin(a) + 1) / 2))
            for k in range(segments):
                a, b = ring[k], ring[(k + 1) % segments]
                idx.extend([center, b, a] if sign < 0 else [center, a, b])
        # Mapping local (u,v,w) to world (x,w,v) for a Y-axis cylinder is an
        # odd permutation and reverses handedness. Restore outward winding for
        # every triangle while retaining the explicitly transformed normals.
        if axis == "y":
            for offset in range(0, len(idx), 3):
                idx[offset + 1], idx[offset + 2] = idx[offset + 2], idx[offset + 1]
        self.primitive(name, pos, nor, uv, idx, material)

    def card(self, name: str, face: str, center: Sequence[float], size: Sequence[float], material: int, uv_rect=(0, 0, 1, 1)) -> None:
        cx, cy, cz = center
        a, b = size[0] / 2, size[1] / 2
        u0, v0, u1, v1 = uv_rect
        uv = [(u0, v1), (u1, v1), (u1, v0), (u0, v0)]
        if face == "front":
            pos = [(cx - a, cy - b, cz), (cx + a, cy - b, cz), (cx + a, cy + b, cz), (cx - a, cy + b, cz)]; n = (0, 0, 1)
        elif face == "rear":
            pos = [(cx + a, cy - b, cz), (cx - a, cy - b, cz), (cx - a, cy + b, cz), (cx + a, cy + b, cz)]; n = (0, 0, -1)
        elif face == "right":
            # Image left is physical front (+Z); image right is rear (-Z).
            pos = [(cx, cy - b, cz + a), (cx, cy - b, cz - a), (cx, cy + b, cz - a), (cx, cy + b, cz + a)]; n = (1, 0, 0)
        elif face == "left":
            # Image left is rear (-Z); image right is physical front (+Z).
            pos = [(cx, cy - b, cz - a), (cx, cy - b, cz + a), (cx, cy + b, cz + a), (cx, cy + b, cz - a)]; n = (-1, 0, 0)
        elif face == "top":
            # Image top is rear (-Z), image bottom is front (+Z).
            pos = [(cx - a, cy, cz + b), (cx + a, cy, cz + b), (cx + a, cy, cz - b), (cx - a, cy, cz - b)]; n = (0, 1, 0)
            uv = [(u0, v1), (u1, v1), (u1, v0), (u0, v0)]
        elif face == "bottom":
            pos = [(cx - a, cy, cz - b), (cx + a, cy, cz - b), (cx + a, cy, cz + b), (cx - a, cy, cz + b)]; n = (0, -1, 0)
            uv = [(u0, v0), (u1, v0), (u1, v1), (u0, v1)]
        else:
            raise ValueError(face)
        self.primitive(name, pos, [n] * 4, uv, [0, 1, 2, 0, 2, 3], material)

    def write(self, path: Path) -> None:
        self.doc["buffers"][0]["byteLength"] = len(self.bin)
        raw_json = json.dumps(self.doc, separators=(",", ":"), ensure_ascii=True).encode("utf-8")
        while len(raw_json) % 4:
            raw_json += b" "
        align4(self.bin)
        total = 12 + 8 + len(raw_json) + 8 + len(self.bin)
        glb = bytearray(struct.pack("<4sII", b"glTF", 2, total))
        glb.extend(struct.pack("<I4s", len(raw_json), b"JSON")); glb.extend(raw_json)
        glb.extend(struct.pack("<I4s", len(self.bin), b"BIN\x00")); glb.extend(self.bin)
        path.write_bytes(glb)


def make_textures(profile: str) -> dict[str, Path]:
    out = MODEL / f"textures-{profile}"
    out.mkdir(parents=True, exist_ok=True)
    bg = {
        "front": (19, 20, 21, 255), "rear": (109, 112, 111, 255),
        "left": (151, 155, 154, 255), "right": (151, 155, 154, 255),
        "top": (170, 173, 171, 255), "bottom": (174, 178, 177, 255),
    }
    paths = {}
    for face in ("front", "rear", "left", "right", "top", "bottom"):
        im = Image.open(VIEWS / f"{face}.png").convert("RGBA")
        base = Image.new("RGBA", im.size, bg[face]); base.alpha_composite(im); rgb = base.convert("RGB")
        if profile == "web":
            limit = 2048
            scale = min(1.0, limit / max(rgb.size))
            if scale < 1:
                rgb = rgb.resize((max(1, round(rgb.width * scale)), max(1, round(rgb.height * scale))), Image.Resampling.LANCZOS)
            quality, subsampling = 88, 2
        else:
            quality, subsampling = 95, 0
        p = out / f"{face}.jpg"
        rgb.save(p, "JPEG", quality=quality, subsampling=subsampling, optimize=True, progressive=True)
        paths[face] = p
    return paths


def build(profile: str, output: Path) -> dict:
    tex_paths = make_textures(profile)
    g = GLBBuilder(profile)
    tex = {f: g.image_texture(f"{f}-{profile}", p) for f, p in tex_paths.items()}
    face_mat = {f: g.material_texture(f"{f}-source-locked", tex[f]) for f in tex}
    metal = g.material_solid("galvanized steel", (0.56, 0.58, 0.58, 1), 0.28, 0.72)
    dark = g.material_solid("Dell black textured plastic", (0.035, 0.038, 0.041, 1), 0.02, 0.82)
    black = g.material_solid("recess black", (0.006, 0.008, 0.009, 1), 0.0, 0.95)
    orange = g.material_solid("hot-swap orange", (0.92, 0.20, 0.025, 1), 0.0, 0.6)
    green = g.material_solid("activity green", (0.10, 0.72, 0.16, 1), 0.0, 0.65)
    blue = g.material_solid("connector blue", (0.04, 0.22, 0.78, 1), 0.0, 0.55)
    teal = g.material_solid("serial teal", (0.10, 0.48, 0.48, 1), 0.1, 0.55)
    handle = g.material_solid("rigid PSU pull handle", (0.67, 0.69, 0.68, 1), 0.2, 0.42)

    # Verified exact overall bounds (metres).
    x_body, x_overall, y_h, z_overall = 0.4340, 0.4824, 0.0428, 0.7521
    xh, yh, zh = x_body / 2, y_h / 2, z_overall / 2
    z_front_body, z_rear_body = 0.35565, -0.3560
    # Recess the invisible closed shell slightly to prevent z-fighting with canonical face cards.
    g.box("closed chassis body", (0, 0, (z_front_body + z_rear_body) / 2), (x_body, y_h - 0.0016, z_front_body - z_rear_body), metal)

    # Six independent source-locked faces. Cards are slightly proud of the closed shell.
    g.card("front canonical face", "front", (0, 0, zh - 0.00050), (x_overall, y_h), face_mat["front"])
    g.card("rear canonical face", "rear", (0, 0, -zh + 0.00055), (x_body, y_h), face_mat["rear"])
    g.card("physical left canonical face", "left", (-xh - 0.00025, 0, 0), (z_overall, y_h), face_mat["left"])
    g.card("physical right canonical face", "right", (xh + 0.00025, 0, 0), (z_overall, y_h), face_mat["right"])
    top_depth = z_front_body - (-zh + 0.0007)
    top_cz = (z_front_body + (-zh + 0.0007)) / 2
    g.card("top canonical face", "top", (0, yh - 0.0006, top_cz), (x_body, top_depth), face_mat["top"])
    g.card("bottom fallback canonical face", "bottom", (0, -yh, top_cz), (x_body, top_depth), face_mat["bottom"])

    # Front-only integrated rack wing housings; no rear ears.
    ear_w = (x_overall - x_body) / 2
    for side, sx in (("left", -1), ("right", 1)):
        # Keep the solid wing depth behind the canonical front photograph so it
        # supplies real quarter-view parallax without hiding the left controls or
        # the source-locked right Intel badge.
        g.box(f"front {side} wing housing", (sx * (xh + ear_w / 2), 0, zh - 0.0090), (ear_w, y_h, 0.018), dark)

    # Ten real 2.5-inch carriers, two rows by five columns, with separate handles/releases/LEDs.
    col_centres = [-0.1472, -0.0736, 0.0, 0.0736, 0.1472]
    row_centres = [0.0104, -0.0104]
    for col, x in enumerate(col_centres):
        for row, y in enumerate(row_centres):
            bay = col * 2 + row
            g.box(f"SFF carrier {bay}", (x, y, z_front_body + 0.0084), (0.0686, 0.0182, 0.0166), dark)
            g.box(f"carrier {bay} pull handle", (x + 0.0300, y, zh - 0.00012), (0.0040, 0.0120, 0.00020), dark)
            g.cylinder(f"carrier {bay} orange release", (x - 0.0260, y + 0.0042, zh - 0.00008), 0.0015, 0.00012, "z", orange, 16)
            g.box(f"carrier {bay} activity LED", (x - 0.0260, y - 0.0045, zh - 0.00006), (0.0009, 0.0025, 0.00010), green)

    # Front control strip relief without covering the source-locked DELL/PowerEdge printing.
    g.box("left front control strip body", (-0.202, 0, z_front_body + 0.0065), (0.018, 0.037, 0.013), dark)
    for j, yy in enumerate((0.009, 0.002, -0.005)):
        g.cylinder(f"front control button {j+1}", (-0.202, yy, zh - 0.00008), 0.0018, 0.00012, "z", black, 14)
    g.box("iDRAC Direct micro USB recess", (-0.202, -0.014, zh - 0.00010), (0.005, 0.005, 0.00014), black)

    # Seven source-verified internal hot-swap cooling fans. They remain under
    # the opaque installed cover but are explicit configuration nodes.
    for j, x in enumerate((-0.150, -0.100, -0.050, 0.0, 0.050, 0.100, 0.150), 1):
        g.box(f"internal cooling fan {j} housing", (x, 0, 0.245), (0.043, 0.033, 0.052), black)
        g.cylinder(f"internal cooling fan {j} rotor", (x, 0, 0.245), 0.015, 0.018, "z", metal, 20)

    # Side rail channels and independent stud layouts.
    for side, sx, zs in (
        ("left", -1, (0.279, 0.061, -0.154, -0.319)),
        ("right", 1, (0.272, 0.041, -0.205, -0.331)),
    ):
        g.box(f"{side} recessed rail channel", (sx * (xh + 0.0015), -0.002, -0.015), (0.0030, 0.012, 0.650), metal)
        g.box(f"{side} upper folded rail lip", (sx * (xh + 0.0012), 0.014, -0.006), (0.0024, 0.006, 0.690), metal)
        for j, z in enumerate(zs):
            g.cylinder(f"{side} rail mounting stud {j+1}", (sx * (xh + 0.0030), -0.003, z), 0.0030, 0.0036, "x", metal, 18)

    # Raised top features with source-proven placement.
    # Raised service-hatch frame leaves the source-locked DELL embossing/label visible.
    hatch_x, hatch_z, hatch_w, hatch_d = -0.134, 0.273, 0.086, 0.073
    g.box("top DELL service hatch left frame", (hatch_x - hatch_w / 2, yh - 0.0003, hatch_z), (0.0022, 0.0006, hatch_d), metal)
    g.box("top DELL service hatch right frame", (hatch_x + hatch_w / 2, yh - 0.0003, hatch_z), (0.0022, 0.0006, hatch_d), metal)
    # Horizontal rails terminate between the vertical rails instead of
    # overlapping their top faces at all four corners.
    g.box("top DELL service hatch front frame", (hatch_x, yh - 0.0003, hatch_z + hatch_d / 2), (hatch_w - 0.0044, 0.0006, 0.0022), metal)
    g.box("top DELL service hatch rear frame", (hatch_x, yh - 0.0003, hatch_z - hatch_d / 2), (hatch_w - 0.0044, 0.0006, 0.0022), metal)
    g.box("top cover latch spine", (0.071, yh - 0.0014, 0.164), (0.015, 0.0028, 0.052), dark)
    g.cylinder("top cover latch finger recess", (0.071, yh - 0.0010, 0.188), 0.0080, 0.0012, "y", dark, 22)

    # Rear three-riser blocks.
    for j, x in enumerate((0.171, 0.101, 0.031), 1):
        g.box(f"rear LP PCIe blanking assembly {j}", (x, 0.0105, z_rear_body - 0.009), (0.062, 0.017, 0.018), metal)

    # Rear I/O cavities in physical +X to -X order (screen left to right from rear).
    # Recess meshes stay behind the canonical photographic face: these connectors
    # are cavities, not proud black blocks. The source-locked face retains their
    # exact shells, pins, labels and colours while the named meshes preserve the
    # structural inventory for inspection.
    zr = -zh + 0.00155
    g.cylinder("rear system ID button", (0.201, -0.010, zr), 0.0020, 0.0004, "z", blue, 14)
    g.box("rear iDRAC8 Enterprise RJ45 recess", (0.172, -0.010, zr), (0.013, 0.010, 0.0004), black)
    g.box("rear DB9 serial recess", (0.143, -0.010, zr), (0.020, 0.008, 0.0004), teal)
    g.box("rear VGA HD15 recess", (0.112, -0.010, zr), (0.020, 0.008, 0.0004), blue)
    for j, yy in enumerate((-0.0045, -0.0150), 1):
        g.box(f"rear USB 3.0 port {j} recess", (0.084, yy, zr), (0.011, 0.0055, 0.0004), black)
    for j, x in enumerate((0.058, 0.038, 0.018, -0.002), 1):
        g.box(f"quad RJ45 NDC port {j} recess", (x, -0.010, zr), (0.013, 0.009, 0.0004), black)

    # Dual matching EPP 1100W AC hot-plug PSUs. All protrusions remain inside Dell Zc.
    for j, x in enumerate((-0.066, -0.158), 1):
        # The module body stops behind the photographic rear plane. Four thin
        # perimeter rails provide real separation/parallax without painting over
        # the exact C14, fan guard, EPP 1100W hub label or factory screw detail.
        g.box(f"EPP 1100W AC PSU {j} body", (x, 0, z_rear_body - 0.008), (0.086, 0.039, 0.016), metal)
        zf = -zh + 0.00035
        g.box(f"PSU {j} top frame", (x, 0.0187, zf), (0.086, 0.0014, 0.0007), metal)
        g.box(f"PSU {j} bottom frame", (x, -0.0187, zf), (0.086, 0.0014, 0.0007), metal)
        g.box(f"PSU {j} left frame", (x - 0.0423, 0, zf), (0.0014, 0.036, 0.0007), metal)
        g.box(f"PSU {j} right frame", (x + 0.0423, 0, zf), (0.0014, 0.036, 0.0007), metal)

        # C14 is recessed in the locked texture; a narrow four-sided rim supplies
        # relief while leaving the real inlet interior visible.
        ix, iy, iw, ih, rim = x + 0.022, -0.001, 0.024, 0.024, 0.0012
        g.box(f"PSU {j} IEC C14 top rim", (ix, iy + ih / 2, zf - 0.0001), (iw - 2 * rim, rim, 0.0007), black)
        g.box(f"PSU {j} IEC C14 bottom rim", (ix, iy - ih / 2, zf - 0.0001), (iw - 2 * rim, rim, 0.0007), black)
        g.box(f"PSU {j} IEC C14 left rim", (ix - iw / 2, iy, zf - 0.0001), (rim, ih, 0.0007), black)
        g.box(f"PSU {j} IEC C14 right rim", (ix + iw / 2, iy, zf - 0.0001), (rim, ih, 0.0007), black)
        g.box(f"PSU {j} orange release tab", (x + 0.039, 0.001, zf - 0.0001), (0.0040, 0.018, 0.0007), orange)

        # Rigid molded pull handle only—no black fabric retention strap. Keep the
        # members narrow so the source-locked fan guard and EPP hub remain legible.
        g.box(f"PSU {j} rigid handle upper mount", (x + 0.002, 0.0148, zf - 0.0001), (0.016, 0.0024, 0.0007), handle)
        g.box(f"PSU {j} rigid handle lower mount", (x + 0.002, -0.0148, zf - 0.0001), (0.016, 0.0024, 0.0007), handle)
        g.box(f"PSU {j} rigid handle grasp", (x - 0.006, 0, zf - 0.0001), (0.0026, 0.0270, 0.0007), handle)
        for sx in (-1, 1):
            for sy in (-1, 1):
                g.cylinder(f"PSU {j} screw {sx} {sy}", (x + sx * 0.036, sy * 0.016, zf - 0.00015), 0.0012, 0.0005, "z", metal, 12)

    g.write(output)
    return {
        "file": str(output.relative_to(ROOT)),
        "bytes": output.stat().st_size,
        "sha256": hashlib.sha256(output.read_bytes()).hexdigest(),
        "nodes": len(g.doc["nodes"]), "meshes": len(g.doc["meshes"]),
        "materials": len(g.doc["materials"]), "images": len(g.doc["images"]),
    }


def main() -> None:
    MODEL.mkdir(parents=True, exist_ok=True)
    results = [
        build("standard", MODEL / "Dell-R630-2.5inch.glb"),
        build("web", MODEL / "Dell-R630-2.5inch-web.glb"),
    ]
    (MODEL / "build-report.json").write_text(json.dumps({"models": results}, indent=2) + "\n")
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
