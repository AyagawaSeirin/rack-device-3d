#!/usr/bin/env python3
"""Build self-contained standard/web GLBs for the verified Cisco N9K-C9336C-FX2."""

from __future__ import annotations

import hashlib
import io
import json
import math
import struct
import sys
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
VIEWS = ROOT / "views"
MODELS = ROOT / "models"
WEB_TEXTURES = ROOT / "qa" / "intermediate" / "web-textures"
STANDARD_TEXTURES = ROOT / "qa" / "intermediate" / "standard-textures"

# Cisco Hardware Installation Guide: 17.3 x 1.73 x 24.5 in overall.
# The 22.5 in body is source-locked separately from the 24.5 in handle depth.
W, H, BODY_D, OVERALL_D = 439.0, 44.0, 571.5, 623.0
X, Y, Z_BODY = W / 2.0, H / 2.0, BODY_D / 2.0
Z_HANDLE_REAR = Z_BODY - OVERALL_D  # front plane +285.75 to handle rear -337.25

# Photo-derived source locks are the primary visible exterior.  Coarse support
# volumes stay behind them; only narrow, source-aligned relief may sit in front.
# Every skin/support and skin/relief gap is at least 0.25 mm.
FRONT_SKIN_Z = Z_BODY - 0.55
FRONT_SUPPORT_Z = FRONT_SKIN_Z - 0.65
FRONT_RELIEF_Z = FRONT_SKIN_Z + 0.40
REAR_SKIN_Z = -Z_BODY - 0.55
REAR_SUPPORT_Z = REAR_SKIN_Z + 0.65
REAR_RELIEF_Z = REAR_SKIN_Z - 0.40


def align4(data: bytearray) -> None:
    while len(data) % 4:
        data.append(0)


def flatten(values):
    return [item for row in values for item in row]


class GLBBuilder:
    def __init__(self, variant: str):
        self.variant = variant
        self.binary = bytearray()
        self.vertex_count = 0
        self.triangle_count = 0
        self.doc = {
            "asset": {
                "version": "2.0",
                "generator": "Codex exact-appearance rack-device builder",
                "copyright": "Cisco and Nexus marks remain property of Cisco Systems, Inc.",
                "extras": {
                    "identity": "Cisco Nexus 9000 C9336C-FX2 Chassis",
                    "pid": "N9K-C9336C-FX2",
                    "identity_status": "VERIFIED",
                    "installed_configuration": "2 x NXA-PAC-1100W-PI2 AC PSU; 3 x NXA-FAN-65CFM-PI",
                    "airflow": "port-side intake; burgundy PI hardware",
                    "front_ports": "36 empty QSFP28 ports in 18 vertical two-port cages",
                    "not_variants": ["N9K-C9336PQ", "N9K-C9336-FX2", "N9K-C9336C-FX2-E"],
                    "dimensions_mm": {
                        "width": W,
                        "height": H,
                        "body_depth": BODY_D,
                        "overall_depth_with_handles": OVERALL_D,
                    },
                    "orientation": "+X device right from front, +Y up, +Z port/front side",
                    "bottom_evidence": "GENERIC_BOTTOM_FALLBACK after documented search escalation",
                    "official_public_3d": "not found in documented public-source search",
                    "variant": variant,
                },
            },
            "scene": 0,
            "scenes": [{"name": "N9K_C9336C_FX2_Scene", "nodes": [0]}],
            "nodes": [{
                "name": "Cisco_N9K_C9336C_FX2_PI2_AC",
                "children": [],
                "extras": {"rack_units": 1, "configuration_verified": True},
            }],
            "meshes": [],
            "materials": [],
            "textures": [],
            "images": [],
            "samplers": [{
                "name": "LinearClamp",
                "magFilter": 9729,
                "minFilter": 9987,
                "wrapS": 33071,
                "wrapT": 33071,
            }],
            "accessors": [],
            "bufferViews": [],
            "buffers": [{"byteLength": 0}],
            "extensionsUsed": ["KHR_materials_unlit"],
        }
        self.solid_materials = {}
        self.cube_meshes = {}
        self.cylinder_meshes = {}

    def add_view(self, payload: bytes, target=None, name=None):
        align4(self.binary)
        offset = len(self.binary)
        self.binary.extend(payload)
        definition = {"buffer": 0, "byteOffset": offset, "byteLength": len(payload)}
        if target is not None:
            definition["target"] = target
        if name:
            definition["name"] = name
        index = len(self.doc["bufferViews"])
        self.doc["bufferViews"].append(definition)
        return index

    def add_accessor(self, values, components, component_type, kind, target, name):
        flat = flatten(values) if values and isinstance(values[0], (tuple, list)) else list(values)
        if component_type == 5126:
            payload = struct.pack("<" + "f" * len(flat), *flat)
        elif component_type == 5123:
            payload = struct.pack("<" + "H" * len(flat), *flat)
        else:
            raise ValueError(component_type)
        view = self.add_view(payload, target, name + "_buffer")
        accessor = {
            "bufferView": view,
            "byteOffset": 0,
            "componentType": component_type,
            "count": len(flat) // components,
            "type": kind,
            "name": name,
        }
        if kind == "VEC3" and component_type == 5126:
            accessor["min"] = [min(row[i] for row in values) for i in range(3)]
            accessor["max"] = [max(row[i] for row in values) for i in range(3)]
        index = len(self.doc["accessors"])
        self.doc["accessors"].append(accessor)
        return index

    def add_mesh(self, name, positions, normals, uvs, indices, material):
        pos = self.add_accessor(positions, 3, 5126, "VEC3", 34962, name + "_POSITION")
        nor = self.add_accessor(normals, 3, 5126, "VEC3", 34962, name + "_NORMAL")
        tex = self.add_accessor(uvs, 2, 5126, "VEC2", 34962, name + "_TEXCOORD_0")
        ind = self.add_accessor(indices, 1, 5123, "SCALAR", 34963, name + "_INDICES")
        mesh = {
            "name": name,
            "primitives": [{
                "attributes": {"POSITION": pos, "NORMAL": nor, "TEXCOORD_0": tex},
                "indices": ind,
                "material": material,
            }],
        }
        index = len(self.doc["meshes"])
        self.doc["meshes"].append(mesh)
        self.vertex_count += len(positions)
        self.triangle_count += len(indices) // 3
        return index

    def add_solid_material(self, name, rgba, metallic=0.0, roughness=0.65, emissive=None):
        if name in self.solid_materials:
            return self.solid_materials[name]
        definition = {
            "name": name,
            "pbrMetallicRoughness": {
                "baseColorFactor": rgba,
                "metallicFactor": metallic,
                "roughnessFactor": roughness,
            },
            "alphaMode": "OPAQUE",
            "doubleSided": False,
        }
        if emissive:
            definition["emissiveFactor"] = emissive
        index = len(self.doc["materials"])
        self.doc["materials"].append(definition)
        self.solid_materials[name] = index
        return index

    def add_photo_material(self, name: str, path: Path):
        payload = path.read_bytes()
        mime = "image/jpeg" if path.suffix.lower() in (".jpg", ".jpeg") else "image/png"
        view = self.add_view(payload, None, name + "_image_buffer")
        image_index = len(self.doc["images"])
        self.doc["images"].append({
            "name": name + "_Image",
            "bufferView": view,
            "mimeType": mime,
        })
        texture_index = len(self.doc["textures"])
        self.doc["textures"].append({
            "name": name + "_Texture",
            "sampler": 0,
            "source": image_index,
        })
        material = {
            "name": name,
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
        index = len(self.doc["materials"])
        self.doc["materials"].append(material)
        return index

    def cube_mesh(self, material):
        if material in self.cube_meshes:
            return self.cube_meshes[material]
        faces = [
            ((0, 0, 1), [(-.5,-.5,.5),(.5,-.5,.5),(.5,.5,.5),(-.5,.5,.5)]),
            ((0, 0,-1), [( .5,-.5,-.5),(-.5,-.5,-.5),(-.5,.5,-.5),( .5,.5,-.5)]),
            ((1, 0, 0), [(.5,-.5,.5),(.5,-.5,-.5),(.5,.5,-.5),(.5,.5,.5)]),
            ((-1,0, 0), [(-.5,-.5,-.5),(-.5,-.5,.5),(-.5,.5,.5),(-.5,.5,-.5)]),
            ((0, 1, 0), [(-.5,.5,.5),(.5,.5,.5),(.5,.5,-.5),(-.5,.5,-.5)]),
            ((0,-1, 0), [(-.5,-.5,-.5),(.5,-.5,-.5),(.5,-.5,.5),(-.5,-.5,.5)]),
        ]
        positions, normals, uvs, indices = [], [], [], []
        for normal, vertices in faces:
            base = len(positions)
            positions.extend(vertices)
            normals.extend([normal] * 4)
            uvs.extend([(0,1),(1,1),(1,0),(0,0)])
            indices.extend([base,base+1,base+2,base,base+2,base+3])
        mesh = self.add_mesh(f"UnitBox_Mat{material}", positions, normals, uvs, indices, material)
        self.cube_meshes[material] = mesh
        return mesh

    def cylinder_mesh(self, material, segments=24):
        key = (material, segments)
        if key in self.cylinder_meshes:
            return self.cylinder_meshes[key]
        positions, normals, uvs, indices = [], [], [], []
        for side, z, normal_z in ((0, .5, 1), (1, -.5, -1)):
            center = len(positions)
            positions.append((0,0,z)); normals.append((0,0,normal_z)); uvs.append((.5,.5))
            for i in range(segments):
                angle = 2 * math.pi * i / segments
                positions.append((math.cos(angle)*.5, math.sin(angle)*.5, z))
                normals.append((0,0,normal_z))
                uvs.append(((math.cos(angle)+1)/2, (1-math.sin(angle))/2))
            for i in range(segments):
                a = center + 1 + i
                c = center + 1 + (i + 1) % segments
                indices.extend((center, a, c) if side == 0 else (center, c, a))
        for i in range(segments):
            a0, a1 = 2*math.pi*i/segments, 2*math.pi*(i+1)/segments
            base = len(positions)
            for angle, z in ((a0,.5),(a0,-.5),(a1,-.5),(a1,.5)):
                positions.append((math.cos(angle)*.5, math.sin(angle)*.5, z))
                normals.append((math.cos(angle),math.sin(angle),0))
                uvs.append((i/segments, 0 if z > 0 else 1))
            indices.extend((base,base+1,base+2,base,base+2,base+3))
        mesh = self.add_mesh(f"UnitCylinder_Mat{material}", positions, normals, uvs, indices, material)
        self.cylinder_meshes[key] = mesh
        return mesh

    def add_node(self, name, mesh, translation=None, scale=None, rotation=None, extras=None):
        node = {"name": name, "mesh": mesh}
        if translation is not None:
            node["translation"] = [round(float(v), 6) for v in translation]
        if scale is not None:
            node["scale"] = [round(float(v), 6) for v in scale]
        if rotation is not None:
            node["rotation"] = [round(float(v), 8) for v in rotation]
        if extras:
            node["extras"] = extras
        index = len(self.doc["nodes"])
        self.doc["nodes"].append(node)
        self.doc["nodes"][0]["children"].append(index)
        return index

    def box(self, name, material, center, size, extras=None):
        return self.add_node(name, self.cube_mesh(material), center, size, extras=extras)

    def cylinder(self, name, material, center, size, rotation=None, extras=None):
        return self.add_node(
            name, self.cylinder_mesh(material), center, size, rotation=rotation, extras=extras
        )

    def plane(self, name, material, positions, normal, uvs=None, extras=None):
        if uvs is None:
            uvs = [(0,1),(1,1),(1,0),(0,0)]
        mesh = self.add_mesh(name + "_Mesh", positions, [normal]*4, uvs, [0,1,2,0,2,3], material)
        return self.add_node(name, mesh, extras=extras)

    def save(self, path: Path):
        align4(self.binary)
        self.doc["buffers"][0]["byteLength"] = len(self.binary)
        raw_json = json.dumps(self.doc, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
        while len(raw_json) % 4:
            raw_json += b" "
        total = 12 + 8 + len(raw_json) + 8 + len(self.binary)
        payload = bytearray(struct.pack("<4sII", b"glTF", 2, total))
        payload.extend(struct.pack("<II", len(raw_json), 0x4E4F534A)); payload.extend(raw_json)
        payload.extend(struct.pack("<II", len(self.binary), 0x004E4942)); payload.extend(self.binary)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(payload)
        return len(payload), hashlib.sha256(payload).hexdigest()


def prepare_textures(variant: str):
    faces = ("front", "rear", "left", "right", "top", "bottom")
    if variant == "standard":
        # Keep the canonical RGBA elevations unchanged, but embed RGB-only
        # base-color images in the GLB.  OPAQUE already requires alpha to be
        # ignored; removing the unused channel also prevents viewer-specific
        # alpha heuristics from entering the upload path.
        STANDARD_TEXTURES.mkdir(parents=True, exist_ok=True)
        result = {}
        for face in faces:
            with Image.open(VIEWS / f"{face}.png") as original:
                target = STANDARD_TEXTURES / f"{face}.png"
                temporary = target.with_suffix(".tmp.png")
                original.convert("RGB").save(temporary, format="PNG", compress_level=6)
                temporary.replace(target)
            result[face] = target
        return result
    WEB_TEXTURES.mkdir(parents=True, exist_ok=True)
    result = {}
    for face in faces:
        with Image.open(VIEWS / f"{face}.png") as original:
            image = original.convert("RGB")
            scale = min(1.0, 2048.0 / max(image.size))
            size = tuple(max(1, round(value * scale)) for value in image.size)
            image = image.resize(size, Image.Resampling.LANCZOS)
            target = WEB_TEXTURES / f"{face}.jpg"
            temporary = target.with_suffix(".tmp.jpg")
            image.save(temporary, format="JPEG", quality=90, optimize=True, progressive=True)
            temporary.replace(target)
        result[face] = target
    return result


def build(variant: str):
    textures = prepare_textures(variant)
    b = GLBBuilder(variant)

    steel = b.add_solid_material("Cisco_Galvanized_Steel", [.68,.70,.70,1], .55, .58)
    silver = b.add_solid_material("Bright_Module_Edges", [.82,.83,.81,1], .65, .43)
    photo_edge = b.add_solid_material("Source_Aligned_Narrow_Relief", [.47,.48,.47,1], .30, .62)
    dark = b.add_solid_material("Dark_Recess", [.018,.022,.026,1], .02, .6)
    black = b.add_solid_material("Black_Polymer", [.009,.011,.014,1], .01, .48)
    burgundy = b.add_solid_material("Port_Intake_Burgundy", [.50,.025,.12,1], .02, .46)
    beige = b.add_solid_material("RJ45_Shield", [.68,.62,.52,1], .25, .55)
    green = b.add_solid_material("Status_LED_Green", [.01,.70,.08,1], 0, .25, [0,.3,.02])
    amber = b.add_solid_material("Status_LED_Amber", [.95,.50,.01,1], 0, .25, [.3,.08,0])
    blue = b.add_solid_material("USB_Blue_Insert", [.02,.14,.58,1], .02, .4)
    photos = {
        face: b.add_photo_material(f"FACE_{face.upper()}_SOURCE_LOCKED", path)
        for face, path in textures.items()
    }

    b.box(
        "Closed_1RU_C9336C_FX2_Chassis_Core", steel, (0,0,-1.5), (W-.8,H-.8,BODY_D-3.5),
        {"pid":"N9K-C9336C-FX2", "body_dimensions_mm":[W,H,BODY_D], "closed_core":True},
    )

    # Six independently generated faces: all explicit winding and positive transforms.
    b.plane("Front_SourceLocked_Texture", photos["front"], [
        (-X,-Y,FRONT_SKIN_Z),(X,-Y,FRONT_SKIN_Z),(X,Y,FRONT_SKIN_Z),(-X,Y,FRONT_SKIN_Z)
    ], (0,0,1), extras={"source_lock":"front", "ports":"1-36", "not_mirrored":True})
    b.plane("Rear_SourceLocked_Texture", photos["rear"], [
        (X,-Y,REAR_SKIN_Z),(-X,-Y,REAR_SKIN_Z),(-X,Y,REAR_SKIN_Z),(X,Y,REAR_SKIN_Z)
    ], (0,0,-1), extras={"source_lock":"rear", "bom":"2x PI2 PSU + 3x PI fan", "not_mirrored":True})
    b.plane("Physical_Left_Independent_Texture", photos["left"], [
        (-X,-Y,-Z_BODY),(-X,-Y,Z_BODY),(-X,Y,Z_BODY),(-X,Y,-Z_BODY)
    ], (-1,0,0), extras={"side":"physical-left", "grounding_pad":False, "not_mirrored":True})
    b.plane("Physical_Right_Independent_Texture", photos["right"], [
        (X,-Y,Z_BODY),(X,-Y,-Z_BODY),(X,Y,-Z_BODY),(X,Y,Z_BODY)
    ], (1,0,0), extras={"side":"physical-right", "grounding_pad":True, "not_mirrored":True})
    b.plane("Top_SourceLocked_Texture", photos["top"], [
        (-X,Y-.20,Z_BODY),(X,Y-.20,Z_BODY),(X,Y-.20,-Z_BODY),(-X,Y-.20,-Z_BODY)
    ], (0,1,0), extras={"front_in_image":"bottom", "source_lock":"top"})
    b.plane("Bottom_GenericFallback_Texture", photos["bottom"], [
        (X,-Y,Z_BODY),(-X,-Y,Z_BODY),(-X,-Y,-Z_BODY),(X,-Y,-Z_BODY)
    ], (0,-1,0), extras={"status":"GENERIC_BOTTOM_FALLBACK", "unsupported_detail_added":False})

    # Front: the exact two-row port photograph is the appearance layer.  Broad
    # cage/support/recess geometry is retained only behind that opaque skin.
    # Narrow source-aligned rims and latch openings provide parallax without
    # replacing the photographed cages with synthetic gray rectangles.
    port_start = -188.0
    pitch = 22.35
    for cage in range(18):
        x = port_start + cage * pitch
        cage_name = f"Front_QSFP28_Cage_{cage+1:02d}"
        for edge, center, size in (
            ("Left",(x-9.6,1.2,FRONT_SUPPORT_Z),(1.4,35.0,.60)),
            ("Right",(x+9.6,1.2,FRONT_SUPPORT_Z),(1.4,35.0,.60)),
            ("Top",(x,17.7,FRONT_SUPPORT_Z),(20.6,2.0,.60)),
            ("Bottom",(x,-15.3,FRONT_SUPPORT_Z),(20.6,2.0,.60)),
        ):
            b.box(cage_name + "_SupportFrame_" + edge, steel, center, size,
                  {"ports":[cage*2+1,cage*2+2], "behind_photo_skin":True})
        for edge, center, size in (
            ("Left",(x-9.6,1.2,FRONT_RELIEF_Z),(.35,33.0,.30)),
            ("Right",(x+9.6,1.2,FRONT_RELIEF_Z),(.35,33.0,.30)),
            ("Top",(x,17.35,FRONT_RELIEF_Z),(19.5,.40,.30)),
            ("Bottom",(x,-14.95,FRONT_RELIEF_Z),(19.5,.40,.30)),
        ):
            b.box(cage_name + "_SourceAlignedFineRim_" + edge, photo_edge, center, size,
                  {"ports":[cage*2+1,cage*2+2], "narrow_relief":True, "skin_clearance_mm":.25})
        for row, y in enumerate((9.4,-7.2)):
            port = cage*2 + row + 1
            b.box(f"Front_QSFP28_Port_{port:02d}_SupportRecess", dark,
                  (x,y,FRONT_SUPPORT_Z), (17.8,12.6,.50),
                  {"port_index":port, "port_family":"QSFP28", "empty":True, "behind_photo_skin":True})
        b.box(cage_name + "_CenterLatchSupport", steel, (x,1.0,FRONT_SUPPORT_Z), (17.0,5.0,.50),
              {"behind_photo_skin":True})
        b.box(cage_name + "_SourceAlignedCenterLip", photo_edge,
              (x,1.0,FRONT_RELIEF_Z), (16.0,.42,.30),
              {"narrow_relief":True, "skin_clearance_mm":.25})
        for aperture in range(4):
            ax = x - 5.4 + aperture * 3.6
            b.box(cage_name + f"_LatchAperture_{aperture+1}", dark,
                  (ax,1.0,FRONT_RELIEF_Z), (.8,.65,.30),
                  {"visible_opening":True, "skin_clearance_mm":.25})

    # Left front status/button zone and the full lower ventilation strip.
    for index, (x,y,material,label) in enumerate((
        (-210,10,green,"BCN"),(-210,3,green,"STS"),(-210,-4,amber,"ENV"),
        (-201,10,green,"Lane1"),(-201,4,green,"Lane2"),(-201,-2,green,"Lane3"),(-201,-8,green,"Lane4"),
    ), 1):
        b.cylinder(f"Front_Status_{index}_{label}", material, (x,y,FRONT_RELIEF_Z), (1.5,1.5,.30),
                   extras={"label":label, "skin_clearance_mm":.25})
    b.cylinder("Front_Lane_Select_Button", black, (-208,-13,FRONT_RELIEF_Z), (3.6,3.6,.30),
               extras={"label":"LS", "push_button":True, "skin_clearance_mm":.25})
    for index, x in enumerate(range(-213,214,7), 1):
        for row, y in enumerate((-17.2,-20.0), 1):
            b.box(f"Front_LowerVentSupport_{index:02d}_{row}", dark, (x,y,FRONT_SUPPORT_Z),
                  (3.4,1.45,.50), {"perforation_in_photo_skin":True, "behind_photo_skin":True})
    for index, y in enumerate((14,7,0,-7,-14), 1):
        b.cylinder(f"Front_RightFastener_{index}", dark, (214,y,FRONT_RELIEF_Z), (1.3,1.3,.30),
                   extras={"skin_clearance_mm":.25})

    # Rear canonical screen order maps to world +X -> -X when viewed from behind.
    psu_centers = (("PSU1_RearLeft", 189.0), ("PSU2_RearRight", -189.0))
    for label, x in psu_centers:
        prefix = f"Rear_NXA_PAC_1100W_PI2_{label}"
        b.box(prefix + "_InstalledVolume", steel, (x,0,-Z_BODY+1.0), (59.0,40.0,2.0),
              {"pid":"NXA-PAC-1100W-PI2", "power":"1100W AC", "airflow":"port-side intake", "behind_photo_skin":True})
        for edge, center, size in (
            ("Top",(x,19.5,REAR_SUPPORT_Z),(59,2.0,.50)),
            ("Bottom",(x,-19.5,REAR_SUPPORT_Z),(59,2.0,.50)),
            ("Left",(x-28.5,0,REAR_SUPPORT_Z),(2.0,39,.50)),
            ("Right",(x+28.5,0,REAR_SUPPORT_Z),(2.0,39,.50)),
        ):
            b.box(prefix + "_SupportFrame_" + edge, steel, center, size, {"behind_photo_skin":True})
        for edge, center, size in (
            ("Top",(x,19.1,REAR_RELIEF_Z),(58,.40,.30)),
            ("Bottom",(x,-19.1,REAR_RELIEF_Z),(58,.40,.30)),
            ("Left",(x-28.1,0,REAR_RELIEF_Z),(.40,38,.30)),
            ("Right",(x+28.1,0,REAR_RELIEF_Z),(.40,38,.30)),
        ):
            b.box(prefix + "_SourceAlignedFineRim_" + edge, photo_edge, center, size,
                  {"narrow_relief":True, "skin_clearance_mm":.25})
        inlet_x = x + (9 if x > 0 else -9)
        b.box(prefix + "_IEC_C14_Support", black, (inlet_x,0,REAR_SUPPORT_Z), (24,22,.50),
              {"connector":"IEC C14 AC", "behind_photo_skin":True})
        latch_x = x - (26 if x > 0 else -26)
        b.box(prefix + "_BurgundyRelease", burgundy, (latch_x,-3,REAR_SKIN_Z-.55), (2.5,10,.60),
              {"airflow_code":"PI burgundy", "skin_clearance_mm":.25})
        handle_x = x - (13 if x > 0 else -13)
        handle_near_z = REAR_SKIN_Z - 1.0
        handle_far_inner_z = Z_HANDLE_REAR + 6.0
        handle_mid = (handle_near_z + handle_far_inner_z) / 2
        handle_depth = handle_near_z - handle_far_inner_z
        b.box(prefix + "_HandleVertical", silver, (handle_x,0,Z_HANDLE_REAR+3.0), (2.0,20,6),
              {"visible_protrusion":True})
        for side_y in (-9,9):
            b.box(prefix + f"_HandleStem_{side_y:+d}", silver, (handle_x,side_y,handle_mid),
                  (2.0,2.0,handle_depth), {"visible_protrusion":True})
        b.cylinder(prefix + "_FAIL_LED", amber, (x+23,7,REAR_RELIEF_Z), (1.5,1.5,.30), extras={"label":"FAIL", "skin_clearance_mm":.25})
        b.cylinder(prefix + "_OK_LED", green, (x+23,-6,REAR_RELIEF_Z), (1.5,1.5,.30), extras={"label":"OK", "skin_clearance_mm":.25})

    fan_centers = (115.5, 32.5, -50.5)
    for slot, x in enumerate(fan_centers, 1):
        prefix = f"Rear_NXA_FAN_65CFM_PI_Slot{slot}"
        b.box(prefix + "_InstalledVolume", steel, (x,0,-Z_BODY+1.0), (79.0,40.0,2.0),
              {"pid":"NXA-FAN-65CFM-PI", "slot":slot, "airflow":"port-side intake", "behind_photo_skin":True})
        b.box(prefix + "_HoneycombSupport", dark, (x,-1,REAR_SUPPORT_Z), (72,27,.50),
              {"grille_in_photo_skin":True, "behind_photo_skin":True})
        b.box(prefix + "_PIDPlateSupport", black, (x,15,REAR_SUPPORT_Z), (72,6,.50),
              {"visible_pid_in_source_texture":"NXA-FAN-65CFM-PI", "behind_photo_skin":True})
        for side_x in (-34,34):
            b.box(prefix + f"_BurgundyLatch_{side_x:+d}", burgundy,
                  (x+side_x,0,REAR_SKIN_Z-.55), (3.0,10,.60),
                  {"airflow_code":"PI burgundy", "skin_clearance_mm":.25})
        b.box(prefix + "_HandleCrossbar", black, (x,0,Z_HANDLE_REAR+3.0), (46,3.0,6),
              {"visible_protrusion":True})
        handle_near_z = REAR_SKIN_Z - 1.0
        handle_far_inner_z = Z_HANDLE_REAR + 6.0
        stem_mid = (handle_near_z + handle_far_inner_z) / 2
        stem_depth = handle_near_z - handle_far_inner_z
        for side_x in (-22,22):
            b.box(prefix + f"_HandleStem_{side_x:+d}", black, (x+side_x,0,stem_mid),
                  (2.0,3.5,stem_depth), {"visible_protrusion":True})
        # The exact honeycomb and PID typography stay in the photo skin.  These
        # former grille bridges are support-only so they cannot overwrite it.
        for bar in range(-5,6):
            b.box(prefix + f"_GrilleBridgeSupport_{bar:+d}", steel,
                  (x+bar*6.0,-1,REAR_SUPPORT_Z), (.8,24,.40), {"behind_photo_skin":True})

    io_x = -125.5
    b.box("Rear_Management_IO_Support", steel, (io_x,0,REAR_SUPPORT_Z), (62,40,.50),
          {"order":"RJ45 management; RJ45 console; SFP; USB; BCN/STS", "behind_photo_skin":True})
    for row, (y,label) in enumerate(((9,"OOB_Management_RJ45"),(-5,"RS232_Console_RJ45")), 1):
        b.box("Rear_" + label + "_ShieldSupport", beige, (io_x-10,y,REAR_SUPPORT_Z), (15,12,.50),
              {"behind_photo_skin":True})
        b.box("Rear_" + label + "_RecessSupport", dark, (io_x-10,y,REAR_SUPPORT_Z), (11,8,.40),
              {"behind_photo_skin":True})
    b.box("Rear_OOB_Management_SFP_Support", dark, (io_x+9,-6,REAR_SUPPORT_Z), (14,10,.50),
          {"port":"SFP", "behind_photo_skin":True})
    b.box("Rear_USB_Port_Support", black, (io_x+23,-4,REAR_SUPPORT_Z), (6,17,.50),
          {"port":"USB", "behind_photo_skin":True})
    b.box("Rear_USB_Blue_InsertSupport", blue, (io_x+23,-4,REAR_SUPPORT_Z), (3,12,.30),
          {"behind_photo_skin":True})
    b.cylinder("Rear_BCN_LED", green, (io_x+7,-16,REAR_RELIEF_Z), (1.5,1.5,.30), extras={"label":"BCN", "skin_clearance_mm":.25})
    b.cylinder("Rear_STS_LED", green, (io_x+20,-16,REAR_RELIEF_Z), (1.5,1.5,.30), extras={"label":"STS", "skin_clearance_mm":.25})

    # The stamped side slots and right-side grounding pad are shallow/flush
    # features already locked pixel-for-pixel in the two independent side
    # elevations.  Earlier duplicate boxes ended exactly on the texture planes,
    # producing same-normal coplanar surfaces during orbit.  They add no verified
    # silhouette or parallax, so the source-locked side textures are the causal
    # representation and the redundant overpaint geometry is intentionally gone.

    # Top port-side intake band and flush fasteners are real visible relief.
    for column, x in enumerate(range(-210,211,7), 1):
        for row, z in enumerate((238,246,254), 1):
            b.box(f"Top_PortSideVent_{column:02d}_{row}", dark, (x,Y-.175,z),
                  (3.2,.35,3.2), {"verified_port_side_vent":True, "recessed":True})
    for index, (x,z) in enumerate((
        (-194,-248),(-150,-248),(-66,-170),(0,-170),(82,-170),(173,-170),
        (-170,50),(-58,50),(60,50),(170,50),(-172,245),(0,245),(174,245)
    ), 1):
        b.cylinder(f"Top_FlushFastener_{index:02d}", silver, (x,Y-.15,z), (4.3,4.3,.3),
                   rotation=(-math.sin(math.pi/4),0,0,math.cos(math.pi/4)),
                   extras={"flush_fastener":True})

    # Bottom remains a verified silhouette only: no inferred holes, labels, feet or vents.
    output = MODELS / f"Cisco-N9K-C9336C-FX2-{variant}.glb"
    size, digest = b.save(output)
    return {
        "variant": variant,
        "path": str(output.relative_to(ROOT)),
        "bytes": size,
        "sha256": digest,
        "nodes": len(b.doc["nodes"]),
        "meshes": len(b.doc["meshes"]),
        "materials": len(b.doc["materials"]),
        "images": len(b.doc["images"]),
        "unique_mesh_vertices": b.vertex_count,
        "unique_mesh_triangles": b.triangle_count,
        "source_face_hashes": {
            face: hashlib.sha256((VIEWS / f"{face}.png").read_bytes()).hexdigest()
            for face in ("front","rear","left","right","top","bottom")
        },
    }


def main():
    variants = sys.argv[1:] or ["standard", "web"]
    if any(variant not in ("standard", "web") for variant in variants):
        raise SystemExit("variants must be 'standard' and/or 'web'")
    results = [build(variant) for variant in variants]
    manifest_path = ROOT / "qa" / "build-manifest.json"
    existing = {}
    if manifest_path.exists():
        existing = json.loads(manifest_path.read_text(encoding="utf-8"))
    for result in results:
        existing[result["variant"]] = result
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(json.dumps(existing, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(results, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
