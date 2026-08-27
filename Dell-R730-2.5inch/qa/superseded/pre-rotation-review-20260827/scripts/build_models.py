#!/usr/bin/env python3
"""Build the self-authored exact-exterior Dell PowerEdge R730 16-SFF GLBs.

The script intentionally uses only the locked project views.  The body is closed,
front ears are separate, drives/slots/ports/PSUs/handles are separate visible
geometry, and all six photo materials are OPAQUE KHR_materials_unlit materials.
"""

from __future__ import annotations

import hashlib
import json
import math
import struct
from io import BytesIO
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
VIEWS = ROOT / "views"
MODEL = ROOT / "model"
QA = ROOT / "qa"
BUILD = QA / "build"


def align4(data: bytearray) -> None:
    while len(data) % 4:
        data.append(0)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def normalize(v):
    length = math.sqrt(sum(x * x for x in v)) or 1.0
    return tuple(x / length for x in v)


class GLBBuilder:
    def __init__(self, variant: str, texture_paths: dict[str, tuple[Path, str]]):
        self.variant = variant
        self.bin = bytearray()
        self.doc = {
            "asset": {
                "version": "2.0",
                "generator": "Dell-R730-2.5inch self-authored exterior builder",
                "copyright": "Factory Dell/PowerEdge marks retained as product appearance evidence",
                "extras": {
                    "manufacturer": "Dell",
                    "product": "PowerEdge R730",
                    "variant": "16 x 2.5-inch SFF, no bezel, seven blank PCIe covers, dual EPP 750W AC",
                    "coordinateConvention": "+X device right, +Y up, +Z front",
                    "bottomMode": "GENERIC_BOTTOM_FALLBACK",
                    "buildVariant": variant,
                },
            },
            "extensionsUsed": ["KHR_materials_unlit"],
            "extensionsRequired": ["KHR_materials_unlit"],
            "scene": 0,
            "scenes": [{"name": "Dell PowerEdge R730 16-SFF", "nodes": []}],
            "nodes": [],
            "meshes": [],
            "materials": [],
            "textures": [],
            "images": [],
            "samplers": [{"magFilter": 9729, "minFilter": 9987, "wrapS": 33071, "wrapT": 33071}],
            "buffers": [{"byteLength": 0}],
            "bufferViews": [],
            "accessors": [],
        }
        self.materials = {}
        for face, (path, mime) in texture_paths.items():
            self.materials[face] = self.add_texture_material(face, path, mime)
        self.materials.update(
            {
                "silver": self.add_color_material("galvanized silver", (0.64, 0.66, 0.66, 1.0), 0.72),
                "dark_silver": self.add_color_material("dark galvanized steel", (0.29, 0.31, 0.31, 1.0), 0.74),
                "black": self.add_color_material("black textured polymer", (0.018, 0.021, 0.024, 1.0), 0.78),
                "gray": self.add_color_material("handle gray", (0.22, 0.24, 0.25, 1.0), 0.66),
                "green": self.add_color_material("status green", (0.18, 0.88, 0.04, 1.0), 0.48),
                "blue": self.add_color_material("Dell blue LCD", (0.0, 0.35, 0.9, 1.0), 0.52),
                "orange": self.add_color_material("Dell PSU release orange", (0.94, 0.26, 0.015, 1.0), 0.58),
                "teal": self.add_color_material("serial teal", (0.03, 0.44, 0.46, 1.0), 0.68),
            }
        )

    def append_view(self, payload: bytes, target: int | None = None) -> int:
        align4(self.bin)
        offset = len(self.bin)
        self.bin.extend(payload)
        view = {"buffer": 0, "byteOffset": offset, "byteLength": len(payload)}
        if target is not None:
            view["target"] = target
        self.doc["bufferViews"].append(view)
        return len(self.doc["bufferViews"]) - 1

    def add_texture_material(self, face: str, path: Path, mime: str) -> int:
        image_view = self.append_view(path.read_bytes())
        self.doc["images"].append(
            {"name": f"{face}-{self.variant}", "bufferView": image_view, "mimeType": mime}
        )
        image_index = len(self.doc["images"]) - 1
        self.doc["textures"].append({"name": face, "sampler": 0, "source": image_index})
        texture_index = len(self.doc["textures"]) - 1
        self.doc["materials"].append(
            {
                "name": f"{face} source-locked photo",
                "pbrMetallicRoughness": {
                    "baseColorFactor": [1, 1, 1, 1],
                    "baseColorTexture": {"index": texture_index},
                    "metallicFactor": 0.0,
                    "roughnessFactor": 1.0,
                },
                "alphaMode": "OPAQUE",
                "doubleSided": False,
                "extensions": {"KHR_materials_unlit": {}},
            }
        )
        return len(self.doc["materials"]) - 1

    def add_color_material(self, name, rgba, roughness, unlit=False) -> int:
        material = {
            "name": name,
            "pbrMetallicRoughness": {
                "baseColorFactor": list(rgba),
                "metallicFactor": 0.0,
                "roughnessFactor": roughness,
            },
            "alphaMode": "OPAQUE",
            "doubleSided": False,
        }
        if unlit:
            material["extensions"] = {"KHR_materials_unlit": {}}
        self.doc["materials"].append(material)
        return len(self.doc["materials"]) - 1

    def accessor(self, values, components, component_type, type_name, target, minimum=None, maximum=None):
        if component_type == 5126:
            fmt = "<" + "f" * len(values)
        elif component_type == 5123:
            fmt = "<" + "H" * len(values)
        else:
            raise ValueError(component_type)
        view = self.append_view(struct.pack(fmt, *values), target)
        acc = {
            "bufferView": view,
            "byteOffset": 0,
            "componentType": component_type,
            "count": len(values) // components,
            "type": type_name,
        }
        if minimum is not None:
            acc["min"] = list(minimum)
        if maximum is not None:
            acc["max"] = list(maximum)
        self.doc["accessors"].append(acc)
        return len(self.doc["accessors"]) - 1

    def add_primitive(self, name, positions, normals, uvs, indices, material):
        flat_p = [x for v in positions for x in v]
        flat_n = [x for v in normals for x in v]
        flat_uv = [x for v in uvs for x in v]
        lo = [min(v[i] for v in positions) for i in range(3)]
        hi = [max(v[i] for v in positions) for i in range(3)]
        pa = self.accessor(flat_p, 3, 5126, "VEC3", 34962, lo, hi)
        na = self.accessor(flat_n, 3, 5126, "VEC3", 34962)
        ua = self.accessor(flat_uv, 2, 5126, "VEC2", 34962)
        ia = self.accessor(indices, 1, 5123, "SCALAR", 34963, [min(indices)], [max(indices)])
        self.doc["meshes"].append(
            {
                "name": name,
                "primitives": [
                    {
                        "attributes": {"POSITION": pa, "NORMAL": na, "TEXCOORD_0": ua},
                        "indices": ia,
                        "material": material,
                        "mode": 4,
                    }
                ],
            }
        )
        mesh = len(self.doc["meshes"]) - 1
        self.doc["nodes"].append({"name": name, "mesh": mesh})
        node = len(self.doc["nodes"]) - 1
        self.doc["scenes"][0]["nodes"].append(node)
        return node

    def quad(self, name, positions, normal, material, uv=(0.0, 0.0, 1.0, 1.0)):
        u0, v0, u1, v1 = uv
        tex = [(u0, v1), (u1, v1), (u1, v0), (u0, v0)]
        return self.add_primitive(name, positions, [normal] * 4, tex, [0, 1, 2, 0, 2, 3], material)

    def box(self, name, center, size, material, omit_normals=()):
        cx, cy, cz = center
        sx, sy, sz = (value / 2 for value in size)
        x0, x1 = cx - sx, cx + sx
        y0, y1 = cy - sy, cy + sy
        z0, z1 = cz - sz, cz + sz
        faces = [
            ([(x1,y0,z1),(x1,y0,z0),(x1,y1,z0),(x1,y1,z1)], (1,0,0)),
            ([(x0,y0,z0),(x0,y0,z1),(x0,y1,z1),(x0,y1,z0)], (-1,0,0)),
            ([(x0,y1,z1),(x1,y1,z1),(x1,y1,z0),(x0,y1,z0)], (0,1,0)),
            ([(x0,y0,z0),(x1,y0,z0),(x1,y0,z1),(x0,y0,z1)], (0,-1,0)),
            ([(x0,y0,z1),(x1,y0,z1),(x1,y1,z1),(x0,y1,z1)], (0,0,1)),
            ([(x1,y0,z0),(x0,y0,z0),(x0,y1,z0),(x1,y1,z0)], (0,0,-1)),
        ]
        positions=[]; normals=[]; uvs=[]; indices=[]
        for corners, normal in faces:
            if normal in omit_normals:
                continue
            base=len(positions); positions.extend(corners); normals.extend([normal]*4)
            uvs.extend([(0,1),(1,1),(1,0),(0,0)])
            indices.extend([base,base+1,base+2,base,base+2,base+3])
        return self.add_primitive(name, positions, normals, uvs, indices, material)

    def cylinder(self, name, center, radius, length, axis, material, segments=16):
        axis_vec={"x":(1,0,0),"y":(0,1,0),"z":(0,0,1)}[axis]
        basis={"x":((0,1,0),(0,0,1)),"y":((0,0,1),(1,0,0)),"z":((1,0,0),(0,1,0))}[axis]
        b,c=basis; a=axis_vec; half=length/2
        positions=[]; normals=[]; uvs=[]; indices=[]
        for end in (-1,1):
            for i in range(segments):
                t=2*math.pi*i/segments
                radial=tuple(math.cos(t)*b[k]+math.sin(t)*c[k] for k in range(3))
                positions.append(tuple(center[k]+end*half*a[k]+radius*radial[k] for k in range(3)))
                normals.append(radial); uvs.append((i/segments, 0 if end<0 else 1))
        for i in range(segments):
            j=(i+1)%segments
            indices.extend([i,j,segments+j,i,segments+j,segments+i])
        for end, normal in ((-1,tuple(-v for v in a)),(1,a)):
            center_index=len(positions)
            positions.append(tuple(center[k]+end*half*a[k] for k in range(3)))
            normals.append(normal); uvs.append((.5,.5))
            ring=[]
            for i in range(segments):
                t=2*math.pi*i/segments
                radial=tuple(math.cos(t)*b[k]+math.sin(t)*c[k] for k in range(3))
                ring.append(len(positions))
                positions.append(tuple(center[k]+end*half*a[k]+radius*radial[k] for k in range(3)))
                normals.append(normal); uvs.append((.5+.5*math.cos(t),.5+.5*math.sin(t)))
            for i in range(segments):
                j=(i+1)%segments
                if end<0: indices.extend([center_index,ring[j],ring[i]])
                else: indices.extend([center_index,ring[i],ring[j]])
        return self.add_primitive(name, positions, normals, uvs, indices, material)

    def build_geometry(self):
        m=self.materials
        body_w=0.4440; body_h=0.0873; body_d=0.6840
        x0=-body_w/2; x1=body_w/2; y0=-body_h/2; y1=body_h/2
        z_rear=-body_d/2; z_front=body_d/2
        z_frontmost=0.3600; z_rearmost=-0.3810

        # Closed structural shell.
        self.box("closed chassis body",(0,0,0),(body_w,body_h,body_d),m["silver"])
        # The full-width front elevation supplies both ear face skins.  The
        # outward depth planes provide the visible 18 mm projection in oblique
        # views without inventing rear-facing flanges in the rear elevation.
        self.quad("left front rack ear outer depth",[(-0.2412,y0,z_front),(-0.2412,y0,z_frontmost),(-0.2412,y1,z_frontmost),(-0.2412,y1,z_front)],(-1,0,0),m["black"])
        self.quad("right front rack ear outer depth",[(0.2412,y0,z_frontmost),(0.2412,y0,z_front),(0.2412,y1,z_front),(0.2412,y1,z_frontmost)],(1,0,0),m["black"])

        eps=0.00012
        # Six opaque canonical photographic faces.
        self.quad("front canonical photo",[( -0.2412,y0,z_frontmost+0.00005),(0.2412,y0,z_frontmost+0.00005),(0.2412,y1,z_frontmost+0.00005),(-0.2412,y1,z_frontmost+0.00005)],(0,0,1),m["front"])
        self.quad("rear canonical photo",[(x1,y0,z_rear-eps),(x0,y0,z_rear-eps),(x0,y1,z_rear-eps),(x1,y1,z_rear-eps)],(0,0,-1),m["rear"])
        self.quad("physical right canonical photo",[(x1+eps,y0,z_front),(x1+eps,y0,z_rear),(x1+eps,y1,z_rear),(x1+eps,y1,z_front)],(1,0,0),m["right"])
        self.quad("physical left canonical photo",[(x0-eps,y0,z_rear),(x0-eps,y0,z_front),(x0-eps,y1,z_front),(x0-eps,y1,z_rear)],(-1,0,0),m["left"])
        self.quad("top canonical photo",[(x0,y1+eps,z_front),(x1,y1+eps,z_front),(x1,y1+eps,z_rear),(x0,y1+eps,z_rear)],(0,1,0),m["top"])
        self.quad("bottom fallback photo",[(x0,y0-eps,z_rear),(x1,y0-eps,z_rear),(x1,y0-eps,z_front),(x0,y0-eps,z_front)],(0,-1,0),m["bottom"])

        # Front control depth, separate ears/latches and dense grille relief.
        self.box("front control assembly",(-0.157,0,(z_front+z_frontmost)/2),(0.130,0.084,z_frontmost-z_front),m["black"])
        self.box("front VGA recess",(-0.180,0.017,z_frontmost-0.0002),(0.018,0.011,0.0002),m["black"])
        self.box("front LCD recess",(-0.128,0.018,z_frontmost-0.0002),(0.034,0.009,0.0002),m["blue"])
        for i,y in enumerate((-0.013,-0.030)):
            self.box(f"front USB {i+1}",(-0.198,y,z_frontmost-0.0002),(0.008,0.013,0.0002),m["black"])
        for row in range(4):
            for col in range(14):
                self.box(f"front intake recess {row:02d}-{col:02d}",(-0.184+col*0.0073,-0.010-row*0.0076,z_frontmost-0.0002),(0.0048,0.0048,0.0002),m["black"])

        # Sixteen independently projecting 2.5-inch carriers, each with handle and two LEDs.
        drive_start=-0.089; drive_end=0.215; pitch=(drive_end-drive_start)/16
        for i in range(16):
            cx=drive_start+(i+.5)*pitch
            carrier_w=pitch*0.87; carrier_y0=-0.040; carrier_y1=0.036; carrier_z=0.3597
            self.box(f"drive carrier {i:02d}",(cx,-0.002,(z_front+carrier_z)/2),(carrier_w,0.076,carrier_z-z_front),m["dark_silver"])
            self.box(f"drive pull handle {i:02d}",(cx,-0.027,carrier_z-0.0002),(pitch*0.70,0.009,0.0002),m["gray"])
            self.box(f"drive activity LED {i:02d}",(cx-pitch*0.18,0.034,carrier_z+0.00018),(0.0026,0.0024,0.00025),m["green"])
            self.box(f"drive status LED {i:02d}",(cx+pitch*0.18,0.034,carrier_z+0.00018),(0.0026,0.0024,0.00025),m["green"])
            for row in range(3):
                self.box(f"carrier vent {i:02d}-{row:02d}",(cx,-0.001-row*0.009,carrier_z-0.00025),(pitch*0.46,0.005,0.0002),m["black"])
            xl=cx-carrier_w/2; xr=cx+carrier_w/2
            u0=(xl+0.2412)/0.4824;u1=(xr+0.2412)/0.4824
            v0=(y1-carrier_y1)/body_h;v1=(y1-carrier_y0)/body_h
            self.quad(f"drive carrier {i:02d} source-photo skin",[(xl,carrier_y0,carrier_z+0.00012),(xr,carrier_y0,carrier_z+0.00012),(xr,carrier_y1,carrier_z+0.00012),(xl,carrier_y1,carrier_z+0.00012)],(0,0,1),m["front"],(u0,v0,u1,v1))

        # Rear seven blank covers with explicit relief.
        blanks=[
            ("slot 1",0.175,0.027,0.066,0.018),("slot 2",0.175,0.006,0.066,0.018),("slot 3",0.175,-0.015,0.066,0.018),
            ("slot 4",0.073,0.025,0.100,0.020),("slot 5",0.073,0.001,0.100,0.020),
            ("slot 6",-0.055,0.025,0.100,0.020),("slot 7",-0.055,0.001,0.100,0.020),
        ]
        for label,cx,cy,w,h in blanks:
            self.box(f"rear PCIe blank {label}",(cx,cy,z_rear-0.003),(w,h,0.006),m["silver"])
            for j in range(max(4,int(w/0.008))):
                self.box(f"{label} vent {j:02d}",(cx-w*.42+j*(w*.84/max(1,int(w/0.008)-1)),cy,z_rear-0.0062),(0.0045,h*.30,0.001),m["black"])
            xl=cx-w/2;xr=cx+w/2;yb=cy-h/2;yt=cy+h/2
            u0=(x1-xr)/body_w;u1=(x1-xl)/body_w;v0=(y1-yt)/body_h;v1=(y1-yb)/body_h
            self.quad(f"rear PCIe blank {label} source-photo skin",[(xr,yb,z_rear-0.0069),(xl,yb,z_rear-0.0069),(xl,yt,z_rear-0.0069),(xr,yt,z_rear-0.0069)],(0,0,-1),m["rear"],(u0,v0,u1,v1))
        self.box("rear upper-right grille",(-0.171,0.023,z_rear-0.002),(0.078,0.038,0.004),m["silver"])
        for row in range(4):
            for col in range(8):
                self.box(f"rear grille opening {row:02d}-{col:02d}",(-0.197+col*0.0076,0.034-row*0.0075,z_rear-0.0045),(0.0044,0.0044,0.001),m["black"])
        gx0,gx1=-0.210,-0.132;gy0,gy1=0.004,0.042
        self.quad("rear upper-right grille source-photo skin",[(gx1,gy0,z_rear-0.0051),(gx0,gy0,z_rear-0.0051),(gx0,gy1,z_rear-0.0051),(gx1,gy1,z_rear-0.0051)],(0,0,-1),m["rear"],((x1-gx1)/body_w,(y1-gy1)/body_h,(x1-gx0)/body_w,(y1-gy0)/body_h))

        # Rear management/video/network port relief, screen order is preserved by physical coordinates.
        self.cylinder("rear system ID button",(0.211,-0.029,z_rear-0.006),0.0045,0.002,"z",m["blue"],12)
        self.box("rear iDRAC8 RJ45",(0.190,-0.028,z_rear-0.006),(0.015,0.017,0.004),m["black"])
        self.box("rear DB9 serial",(0.164,-0.028,z_rear-0.006),(0.020,0.013,0.004),m["teal"])
        self.box("rear DB15 VGA",(0.136,-0.028,z_rear-0.006),(0.022,0.013,0.004),m["blue"])
        for i,cy in enumerate((-0.020,-0.036)):
            self.box(f"rear USB 3.0 {i+1}",(0.112,cy,z_rear-0.006),(0.014,0.009,0.004),m["black"])
        for i in range(4):
            self.box(f"rear NDC RJ45 {i+1}",(0.086-i*0.023,-0.028,z_rear-0.006),(0.017,0.019,0.004),m["black"])
        px0,px1=0.000,0.222;py0,py1=-0.043,-0.010
        self.quad("rear I/O source-photo skin",[(px1,py0,z_rear-0.0085),(px0,py0,z_rear-0.0085),(px0,py1,z_rear-0.0085),(px1,py1,z_rear-0.0085)],(0,0,-1),m["rear"],((x1-px1)/body_w,(y1-py1)/body_h,(x1-px0)/body_w,(y1-py0)/body_h))
        self.cylinder("rear PCIe holder handle",(0.050,-0.004,z_rear-0.012),0.0034,0.150,"x",m["black"],16)
        hx0,hx1=-0.025,0.125;hy0,hy1=-0.014,0.007
        self.quad("rear PCIe handle source-photo skin",[(hx1,hy0,z_rear-0.0156),(hx0,hy0,z_rear-0.0156),(hx0,hy1,z_rear-0.0156),(hx1,hy1,z_rear-0.0156)],(0,0,-1),m["rear"],((x1-hx1)/body_w,(y1-hy1)/body_h,(x1-hx0)/body_w,(y1-hy0)/body_h))

        # Two separately modeled hot-plug EPP 750W AC modules reaching the official rear bound.
        # Centers/width follow the two source-locked module apertures in the
        # cropped rear elevation (not a symmetric generic PSU placement).
        psu_centers=(-0.076,-0.1665)
        psu_width=0.089
        for i,cx in enumerate(psu_centers,1):
            self.box(f"EPP 750W AC PSU {i}",(cx,-0.022,(z_rear+z_rearmost)/2),(psu_width,0.043,z_rear-z_rearmost),m["dark_silver"])
            self.box(f"PSU {i} IEC C14 inlet",(cx-0.023,-0.022,z_rearmost+0.0010),(0.022,0.027,0.002),m["black"])
            self.cylinder(f"PSU {i} cooling fan",(cx+0.018,-0.022,z_rearmost+0.0010),0.017,0.002,"z",m["black"],20)
            self.cylinder(f"PSU {i} fan hub",(cx+0.018,-0.022,z_rearmost+0.0010),0.005,0.002,"z",m["silver"],16)
            self.box(f"PSU {i} pull handle top",(cx+0.035,-0.005,z_rearmost+0.0010),(0.006,0.005,0.002),m["gray"])
            self.box(f"PSU {i} pull handle bottom",(cx+0.035,-0.039,z_rearmost+0.0010),(0.006,0.005,0.002),m["gray"])
            self.box(f"PSU {i} pull handle bridge",(cx+0.039,-0.022,z_rearmost+0.0010),(0.004,0.034,0.002),m["gray"])
            xl=cx-psu_width/2;xr=cx+psu_width/2;yb=-0.0435;yt=-0.0005
            self.quad(f"PSU {i} source-photo skin",[(xr,yb,z_rearmost-0.0001),(xl,yb,z_rearmost-0.0001),(xl,yt,z_rearmost-0.0001),(xr,yt,z_rearmost-0.0001)],(0,0,-1),m["rear"],((x1-xr)/body_w,(y1-yt)/body_h,(x1-xl)/body_w,(y1-yb)/body_h))

        # Top cover relief within the published 2U envelope.
        self.box("top cover latch",(0,0.04355,-0.010),(0.021,0.00018,0.038),m["black"])
        self.box("top forward stiffening rib",(0,0.04356,0.185),(0.370,0.00016,0.006),m["silver"])
        self.box("top rear stiffening rib",(0,0.04356,-0.185),(0.370,0.00016,0.006),m["silver"])
        for side,cx in (("left",x0+0.004),("right",x1-0.004)):
            self.box(f"{side} folded top lip",(cx,0.040,0),(0.008,0.006,0.63),m["silver"])
        for i,z in enumerate((-0.25,-0.12,0.02,0.16,0.28)):
            self.box(f"left top-cover catch tab {i+1}",(x0+0.0004,0.035,z),(0.002,0.010,0.018),m["dark_silver"])
            self.box(f"right top-cover catch tab {i+1}",(x1-0.0004,0.035,z),(0.002,0.010,0.018),m["dark_silver"])

    def write(self, path: Path):
        self.build_geometry()
        self.doc["buffers"][0]["byteLength"] = len(self.bin)
        raw = json.dumps(self.doc, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
        while len(raw)%4: raw += b" "
        align4(self.bin)
        total=12+8+len(raw)+8+len(self.bin)
        payload=bytearray(struct.pack("<4sII",b"glTF",2,total))
        payload.extend(struct.pack("<II",len(raw),0x4E4F534A)); payload.extend(raw)
        payload.extend(struct.pack("<II",len(self.bin),0x004E4942)); payload.extend(self.bin)
        path.parent.mkdir(parents=True,exist_ok=True); path.write_bytes(payload)


def prepare_textures(variant: str):
    out=BUILD/f"{variant}-textures"; out.mkdir(parents=True,exist_ok=True)
    fills={"front":(18,19,21),"rear":(166,168,166),"left":(182,184,182),"right":(182,184,182),"top":(188,190,188),"bottom":(188,190,188)}
    result={}
    for face in ("front","rear","left","right","top","bottom"):
        with Image.open(VIEWS/f"{face}.png") as src:
            rgba=src.convert("RGBA")
        alpha=rgba.getchannel("A"); bbox=alpha.getbbox() or (0,0,*rgba.size); rgba=rgba.crop(bbox)
        base=Image.new("RGBA",rgba.size,fills[face]+(255,)); base.alpha_composite(rgba)
        rgb=base.convert("RGB")
        if variant=="web":
            limit=2048 if face in {"front","rear"} else 1536
            if max(rgb.size)>limit:
                scale=limit/max(rgb.size); rgb=rgb.resize((round(rgb.width*scale),round(rgb.height*scale)),Image.Resampling.LANCZOS)
            path=out/f"{face}.jpg"; rgb.save(path,"JPEG",quality=90,optimize=True,progressive=True)
            result[face]=(path,"image/jpeg")
        else:
            path=out/f"{face}.png"; rgb.save(path,"PNG",optimize=True)
            result[face]=(path,"image/png")
    return result


def main():
    MODEL.mkdir(parents=True,exist_ok=True); BUILD.mkdir(parents=True,exist_ok=True)
    outputs=[]
    for variant,name in (("standard","Dell-R730-2.5inch.glb"),("web","Dell-R730-2.5inch-web.glb")):
        textures=prepare_textures(variant)
        path=MODEL/name; GLBBuilder(variant,textures).write(path)
        outputs.append({"variant":variant,"path":str(path.relative_to(ROOT)),"bytes":path.stat().st_size,"sha256":sha256(path),"textures":{f:{"path":str(p.relative_to(ROOT)),"sha256":sha256(p)} for f,(p,_) in textures.items()}})
    manifest={
        "identity":"Dell PowerEdge R730 16 x 2.5-inch SFF, no bezel, seven blank rear PCIe positions, 4x1GbE NDC, dual EPP 750W AC",
        "coordinateConvention":"+X right, +Y up, +Z front; glTF metres",
        "expectedBoundsM":[0.4824,0.0873,0.7410],
        "visibleGeometry":{"driveCarriers":16,"driveLEDs":32,"frontEars":2,"rearBlankCovers":7,"rearNdcRj45":4,"rearUsb":2,"acPsus":2,"psuFans":2,"psuPullHandles":2,"topRibs":2,"topLatch":1,"closedBody":True},
        "bottomMode":"GENERIC_BOTTOM_FALLBACK",
        "outputs":outputs,
    }
    (QA/"build-manifest.json").write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print(json.dumps(manifest,indent=2,ensure_ascii=False))


if __name__=="__main__": main()
