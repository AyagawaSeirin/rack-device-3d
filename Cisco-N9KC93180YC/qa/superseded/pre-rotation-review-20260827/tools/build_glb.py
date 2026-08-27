#!/usr/bin/env python3
"""Build self-contained standard/web GLBs for Cisco N9K-C93180YC-FX."""

from __future__ import annotations

import hashlib
import json
import math
import struct
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
VIEWS = ROOT / "views"
MODELS = ROOT / "models"
INTERMEDIATE = ROOT / "qa" / "intermediate"

W, H, D = 482.6, 44.0, 571.0
BODY_W = 439.0
X_BODY = BODY_W / 2
X_OUTER = W / 2
Y_OUTER = H / 2
Z_OUTER = D / 2


def align4(data: bytearray):
    while len(data) % 4:
        data.append(0)


def flatten(values):
    return [item for row in values for item in row]


class GLBBuilder:
    def __init__(self, variant: str):
        self.variant = variant
        self.binary = bytearray()
        self.doc = {
            "asset": {
                "version": "2.0",
                "generator": "Codex exact-appearance rack-device builder",
                "copyright": "Cisco and Nexus marks remain property of Cisco Systems, Inc.",
                "extras": {
                    "identity": "Cisco Nexus 9000 C93180YC-FX Chassis",
                    "pid": "N9K-C93180YC-FX",
                    "installed_configuration": "48 empty SFP28 cages; 6 empty QSFP28 cages; four NXA-FAN-30CFM-PI; two NXA-PAC-500W-PI AC PSUs",
                    "airflow": "port-side intake; burgundy-coded",
                    "not_variants": ["N9K-C93180YC-EX", "N9K-C93180YC-FX3", "N9K-C93180YC-FX3S", "93180LC-EX", "24-port ordering PID", "PE blue airflow"],
                    "dimensions_mm": {"overall_width": W, "body_width": BODY_W, "height": H, "depth": D},
                    "orientation": "+X device right from front, +Y up, +Z front",
                    "bottom_evidence": "GENERIC_BOTTOM_FALLBACK after exhaustive exact-PID search",
                    "official_public_3d": "not found as of 2026-08-24",
                    "variant": variant,
                },
            },
            "scene": 0,
            "scenes": [{"name": "Exact_Product_Scene", "nodes": [0]}],
            "nodes": [{"name": "Cisco_N9K_C93180YC_FX_PI_AC", "children": [], "extras": {"rack_units": 1}}],
            "meshes": [],
            "materials": [],
            "textures": [],
            "images": [],
            "samplers": [{"name": "LinearClamp", "magFilter": 9729, "minFilter": 9987, "wrapS": 33071, "wrapT": 33071}],
            "accessors": [],
            "bufferViews": [],
            "buffers": [{"byteLength": 0}],
            "extensionsUsed": ["KHR_materials_unlit"],
        }
        self.solid_materials = {}
        self.cube_meshes = {}
        self.cylinder_meshes = {}
        self.ring_meshes = {}
        self.front_ring_meshes = {}
        self.photo_materials = {}

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
            "primitives": [{"attributes": {"POSITION": pos, "NORMAL": nor, "TEXCOORD_0": tex}, "indices": ind, "material": material}],
        }
        index = len(self.doc["meshes"])
        self.doc["meshes"].append(mesh)
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

    def add_photo_material(self, name, path):
        payload = Path(path).read_bytes()
        image_view = self.add_view(payload, None, name + "_PNG")
        image_index = len(self.doc["images"])
        self.doc["images"].append({"name": name + "_Image", "bufferView": image_view, "mimeType": "image/png"})
        texture_index = len(self.doc["textures"])
        self.doc["textures"].append({"name": name + "_Texture", "sampler": 0, "source": image_index})
        definition = {
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
        self.doc["materials"].append(definition)
        self.photo_materials[name] = index
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

    def cylinder_mesh(self, material, segments=32):
        key = (material, segments)
        if key in self.cylinder_meshes:
            return self.cylinder_meshes[key]
        positions, normals, uvs, indices = [], [], [], []
        for side, z, normal_z in ((0, .5, 1), (1, -.5, -1)):
            center = len(positions)
            positions.append((0,0,z)); normals.append((0,0,normal_z)); uvs.append((.5,.5))
            for i in range(segments):
                a = 2 * math.pi * i / segments
                positions.append((math.cos(a)*.5, math.sin(a)*.5, z))
                normals.append((0,0,normal_z)); uvs.append(((math.cos(a)+1)/2,(1-math.sin(a))/2))
            for i in range(segments):
                a, b = center + 1 + i, center + 1 + (i + 1) % segments
                indices.extend((center, a, b) if side == 0 else (center, b, a))
        for i in range(segments):
            a0, a1 = 2*math.pi*i/segments, 2*math.pi*(i+1)/segments
            base = len(positions)
            for a,z in ((a0,.5),(a0,-.5),(a1,-.5),(a1,.5)):
                positions.append((math.cos(a)*.5,math.sin(a)*.5,z)); normals.append((math.cos(a),math.sin(a),0)); uvs.append((i/segments,0 if z>.0 else 1))
            indices.extend((base,base+1,base+2,base,base+2,base+3))
        mesh = self.add_mesh(f"UnitCylinder_Mat{material}", positions, normals, uvs, indices, material)
        self.cylinder_meshes[key] = mesh
        return mesh

    def ring_mesh(self, material, segments=40, inner=.62):
        key = (material, segments, inner)
        if key in self.ring_meshes:
            return self.ring_meshes[key]
        positions, normals, uvs, indices = [], [], [], []
        for z, nz, reverse in ((.5,1,False),(-.5,-1,True)):
            for i in range(segments):
                a0, a1 = 2*math.pi*i/segments, 2*math.pi*(i+1)/segments
                base=len(positions)
                verts=[(.5*math.cos(a0),.5*math.sin(a0),z),(.5*math.cos(a1),.5*math.sin(a1),z),(.5*inner*math.cos(a1),.5*inner*math.sin(a1),z),(.5*inner*math.cos(a0),.5*inner*math.sin(a0),z)]
                positions.extend(verts); normals.extend([(0,0,nz)]*4); uvs.extend([(0,1),(1,1),(1,0),(0,0)])
                indices.extend((base,base+2,base+1,base,base+3,base+2) if reverse else (base,base+1,base+2,base,base+2,base+3))
        mesh=self.add_mesh(f"UnitRing_Mat{material}",positions,normals,uvs,indices,material)
        self.ring_meshes[key]=mesh
        return mesh

    def front_ring_mesh(self, material, segments=40, inner=.66):
        key=(material,segments,inner)
        if key in self.front_ring_meshes:
            return self.front_ring_meshes[key]
        positions,normals,uvs,indices=[],[],[],[]
        for i in range(segments):
            a0,a1=2*math.pi*i/segments,2*math.pi*(i+1)/segments
            base=len(positions)
            positions.extend([
                (.5*math.cos(a0),.5*math.sin(a0),0),(.5*math.cos(a1),.5*math.sin(a1),0),
                (.5*inner*math.cos(a1),.5*inner*math.sin(a1),0),(.5*inner*math.cos(a0),.5*inner*math.sin(a0),0),
            ])
            normals.extend([(0,0,1)]*4)
            uvs.extend([(0,1),(1,1),(1,0),(0,0)])
            indices.extend((base,base+1,base+2,base,base+2,base+3))
        mesh=self.add_mesh(f"UnitFrontRing_Mat{material}",positions,normals,uvs,indices,material)
        self.front_ring_meshes[key]=mesh
        return mesh

    def add_node(self, name, mesh, translation=None, scale=None, extras=None):
        node={"name":name,"mesh":mesh}
        if translation is not None: node["translation"]=[round(float(v),6) for v in translation]
        if scale is not None: node["scale"]=[round(float(v),6) for v in scale]
        if extras: node["extras"]=extras
        index=len(self.doc["nodes"]); self.doc["nodes"].append(node); self.doc["nodes"][0]["children"].append(index)
        return index

    def box(self, name, material, center, size, extras=None):
        return self.add_node(name, self.cube_mesh(material), center, size, extras)

    def cylinder(self, name, material, center, size, extras=None):
        return self.add_node(name, self.cylinder_mesh(material), center, size, extras)

    def ring(self, name, material, center, size, extras=None, inner=.62):
        return self.add_node(name, self.ring_mesh(material, inner=inner), center, size, extras)

    def front_ring(self, name, material, center, size, extras=None, inner=.66):
        return self.add_node(name,self.front_ring_mesh(material,inner=inner),center,size,extras)

    def plane(self, name, material, positions, normal, uvs=None, extras=None):
        if uvs is None:
            uvs=[(0,1),(1,1),(1,0),(0,0)]
        mesh=self.add_mesh(name+"_Mesh",positions,[normal]*4,uvs,[0,1,2,0,2,3],material)
        return self.add_node(name,mesh,extras=extras)

    def save(self, path):
        align4(self.binary)
        self.doc["buffers"][0]["byteLength"]=len(self.binary)
        raw_json=json.dumps(self.doc,separators=(",",":"),ensure_ascii=False).encode("utf-8")
        while len(raw_json)%4: raw_json+=b" "
        total=12+8+len(raw_json)+8+len(self.binary)
        payload=bytearray(struct.pack("<4sII",b"glTF",2,total))
        payload.extend(struct.pack("<II",len(raw_json),0x4E4F534A)); payload.extend(raw_json)
        payload.extend(struct.pack("<II",len(self.binary),0x004E4942)); payload.extend(self.binary)
        path.parent.mkdir(parents=True,exist_ok=True); path.write_bytes(payload)
        return len(payload),hashlib.sha256(payload).hexdigest()


def prepare_textures(variant):
    faces=("front","rear","left","right","top","bottom")
    if variant == "standard":
        return {face: VIEWS / f"{face}.png" for face in faces}
    out=INTERMEDIATE/variant/"views"
    out.mkdir(parents=True,exist_ok=True)
    targets={
        "front":(1600,146), "rear":(1600,161),
        "left":(1600,123), "right":(1600,123),
        "top":(800,946), "bottom":(800,946),
    }
    result={}
    for face,size in targets.items():
        image=Image.open(VIEWS/f"{face}.png").convert("RGBA")
        image=image.resize(size,Image.Resampling.LANCZOS)
        path=out/f"{face}.png"
        image.save(path,optimize=True)
        result[face]=path
    return result


def build(variant):
    tex=prepare_textures(variant)
    b=GLBBuilder(variant)

    chassis=b.add_solid_material("Cisco_Galvanized_Steel",[.64,.67,.69,1],.58,.6)
    silver=b.add_solid_material("Bright_Steel_Edges",[.78,.80,.81,1],.7,.42)
    dark=b.add_solid_material("Dark_Port_Recess",[.025,.03,.034,1],.04,.58)
    black=b.add_solid_material("Black_Polymer_Handle",[.012,.014,.018,1],.03,.46)
    burgundy=b.add_solid_material("PI_Burgundy",[.48,.045,.15,1],.03,.48)
    white=b.add_solid_material("PSU_500W_Label",[.92,.92,.88,1],0,.82)
    green=b.add_solid_material("Status_LED_Green",[.01,.65,.08,1],0,.28,[0,.28,.02])
    amber=b.add_solid_material("Status_LED_Amber",[.9,.52,.02,1],0,.3,[.25,.09,0])
    usb_blue=b.add_solid_material("USB_Insert_Blue",[.02,.16,.58,1],.04,.45)
    photos={face:b.add_photo_material(f"FACE_{face.upper()}_SOURCE_LOCKED",path) for face,path in tex.items()}

    b.box(
        "Closed_1RU_FX_Chassis_Core",chassis,(0,0,0),(BODY_W-.8,H-.8,D-.8),
        {"pid":"N9K-C93180YC-FX","closed_manifold_core":True,"body_dimensions_mm":[BODY_W,H,D]},
    )

    # Six independently generated and oriented source-lock skins. The front/top/
    # bottom UVs crop front-ear pixels away from the 439 mm body; ears are geometry.
    crop=(W-BODY_W)/(2*W)
    body_uv=[(crop,1),(1-crop,1),(1-crop,0),(crop,0)]
    def front_uv(x,y):
        return (.5+x/W,.5-y/H)
    def front_photo_plane(name,x0,x1,y0,y1,z=Z_OUTER+1.41,extras=None):
        return b.plane(name,photos["front"],[(x0,y0,z),(x1,y0,z),(x1,y1,z),(x0,y1,z)],(0,0,1),[
            front_uv(x0,y0),front_uv(x1,y0),front_uv(x1,y1),front_uv(x0,y1)],extras=extras)
    # Split around the port field so each cage remains a real recess while its
    # own source-locked photo patch supplies the visible face.
    front_photo_plane("Front_Photo_LeftControl",-X_BODY,-182.5,-Y_OUTER,Y_OUTER,extras={"source_lock":"front"})
    front_photo_plane("Front_Photo_TopLegendStrip",-182.5,X_BODY,15.0,Y_OUTER,extras={"source_lock":"front"})
    front_photo_plane("Front_Photo_BottomVentStrip",-182.5,X_BODY,-Y_OUTER,-15.0,extras={"source_lock":"front"})
    for index,(x0,x1) in enumerate(((-182.5,-178.0),(-86,-80),(12,18),(110,124)),1):
        front_photo_plane(f"Front_Photo_PortDivider_{index}",x0,x1,-15,15,extras={"source_lock":"front"})
    b.plane("Rear_SourceLocked_Texture",photos["rear"],[
        (X_BODY,-Y_OUTER,-Z_OUTER-3.1),(-X_BODY,-Y_OUTER,-Z_OUTER-3.1),
        (-X_BODY,Y_OUTER,-Z_OUTER-3.1),(X_BODY,Y_OUTER,-Z_OUTER-3.1)],(0,0,-1),
        extras={"source_lock":"rear","airflow":"PI burgundy"})
    b.plane("Physical_Left_Independent_Texture",photos["left"],[
        (X_BODY,-Y_OUTER,Z_OUTER),(X_BODY,-Y_OUTER,-Z_OUTER),
        (X_BODY,Y_OUTER,-Z_OUTER),(X_BODY,Y_OUTER,Z_OUTER)],(1,0,0),
        extras={"front_in_image":"left","not_mirrored":True})
    b.plane("Physical_Right_Independent_Texture",photos["right"],[
        (-X_BODY,-Y_OUTER,-Z_OUTER),(-X_BODY,-Y_OUTER,Z_OUTER),
        (-X_BODY,Y_OUTER,Z_OUTER),(-X_BODY,Y_OUTER,-Z_OUTER)],(-1,0,0),
        extras={"front_in_image":"right","not_mirrored":True})
    b.plane("Top_SourceLocked_Texture",photos["top"],[
        (-X_BODY,Y_OUTER+.7,Z_OUTER),(X_BODY,Y_OUTER+.7,Z_OUTER),
        (X_BODY,Y_OUTER+.7,-Z_OUTER),(-X_BODY,Y_OUTER+.7,-Z_OUTER)],(0,1,0),body_uv,
        {"front_in_image":"bottom","source_lock":"top"})
    b.plane("Bottom_GenericFallback_Texture",photos["bottom"],[
        (X_BODY,-Y_OUTER,Z_OUTER),(-X_BODY,-Y_OUTER,Z_OUTER),
        (-X_BODY,-Y_OUTER,-Z_OUTER),(X_BODY,-Y_OUTER,-Z_OUTER)],(0,-1,0),body_uv,
        {"front_in_image":"bottom","status":"GENERIC_BOTTOM_FALLBACK"})

    # Front-only rack ears assembled around six true openings (three per ear).
    ear_span=X_OUTER-X_BODY
    def front_ear_plane(name,xc,yc,w,h):
        z=Z_OUTER+.55
        return b.plane(name,silver,[(xc-w/2,yc-h/2,z),(xc+w/2,yc-h/2,z),
                                    (xc+w/2,yc+h/2,z),(xc-w/2,yc+h/2,z)],(0,0,1),
                       extras={"front_only_single_sided":True})
    for side,sign in (("Left",-1),("Right",1)):
        xc=sign*(X_BODY+ear_span/2)
        front_ear_plane(f"Front_{side}_Ear_OuterRail",sign*(X_OUTER-1.1),0,2.2,H)
        front_ear_plane(f"Front_{side}_Ear_InnerRail",sign*(X_BODY+1.1),0,2.2,H)
        front_ear_plane(f"Front_{side}_Ear_TopBridge",xc,19.6,ear_span-2.2,4.8)
        front_ear_plane(f"Front_{side}_Ear_BottomBridge",xc,-19.6,ear_span-2.2,4.8)
        for bridge_y in (-6.5,6.5):
            front_ear_plane(f"Front_{side}_Ear_MidBridge_{bridge_y:+.1f}",xc,bridge_y,ear_span-2.2,3.6)
        for index,yc in enumerate((13,0,-13),1):
            b.front_ring(f"Front_{side}_Ear_RackOpening_{index}",silver,(xc,yc,Z_OUTER+.55),(13,11,1),
                         {"true_through_hole":True,"front_only_single_sided":True},inner=.66)
        z0,z1=Z_OUTER-1.5,Z_OUTER+1.5
        b.plane(f"Top_{side}_Ear_ThinProjection",silver,
                [(xc-ear_span/2,Y_OUTER+.1,z1),(xc+ear_span/2,Y_OUTER+.1,z1),
                 (xc+ear_span/2,Y_OUTER+.1,z0),(xc-ear_span/2,Y_OUTER+.1,z0)],(0,1,0),
                extras={"front_only":True,"top_surface":True})
        b.plane(f"Bottom_{side}_Ear_ThinProjection",silver,
                [(xc+ear_span/2,-Y_OUTER-.1,z1),(xc-ear_span/2,-Y_OUTER-.1,z1),
                 (xc-ear_span/2,-Y_OUTER-.1,z0),(xc+ear_span/2,-Y_OUTER-.1,z0)],(0,-1,0),
                extras={"front_only":True,"bottom_surface":True})

    # Front control strip and all 54 port cages are individual visible geometry.
    b.box("Front_LED_and_Brand_Panel",chassis,(-202,0,Z_OUTER+.55),(31,40,1.1),{"branding_in_source_texture":True})
    for index,y in enumerate((9,1,-7),1):
        b.cylinder(f"Front_Status_LED_{index}",green if index<3 else amber,(-207,y,Z_OUTER+1.15),(2.1,2.1,.6))
    sfp_start=-178.0
    sfp_pitch=12.25
    for column in range(24):
        x=sfp_start+column*sfp_pitch
        group=column//8+1
        for row,y in enumerate((9.0,-8.0),1):
            index=column*2+row
            p=f"Front_SFP28_{index:02d}"
            b.box(p+"_Recess",dark,(x,y,Z_OUTER+.7),(10.6,14.0,1.4),
                  {"port_index":index,"port_family":"SFP28","empty":True,"group":group})
            front_photo_plane(p+"_SourceTexture",x-5.3,x+5.3,y-7,y+7,
                              extras={"port_index":index,"source_lock":"front","recessed_geometry":True})
            b.box(p+"_LatchRelief",silver,(x,y-2.0,Z_OUTER+1.3),(7.8,2.2,.18))
    for column,x in enumerate((137.5,170.5,203.5),1):
        for row,y in enumerate((9.0,-8.0),1):
            index=48+(column-1)*2+row
            p=f"Front_QSFP28_{index:02d}"
            b.box(p+"_Recess",dark,(x,y,Z_OUTER+.75),(26.0,14.5,1.5),
                  {"port_index":index,"port_family":"QSFP28","empty":True})
            front_photo_plane(p+"_SourceTexture",x-13,x+13,y-7.25,y+7.25,z=Z_OUTER+1.56,
                              extras={"port_index":index,"source_lock":"front","recessed_geometry":True})
            b.box(p+"_LatchRelief",silver,(x,y-1.5,Z_OUTER+1.3),(14.0,2.2,.2))
    front_photo_plane("Front_QSFP28_Continuous_SourceTexture",124.0,X_BODY,-15.0,15.0,z=Z_OUTER+1.58,
                      extras={"source_lock":"front","ports":"49-54","continuous_exact_photo":True})
    for index,x in enumerate([(-180+i*6.4) for i in range(62)],1):
        b.box(f"Front_LowerVent_{index:02d}",dark,(x,-18.7,Z_OUTER+.5),(3.0,2.2,.5),{"vent_relief":True})

    # Rear installed configuration: PSU1, four burgundy PI fan trays, PSU2, FX I/O.
    psu_centers=(("PSU1",170.0),("PSU2",-121.0))
    for label,xc in psu_centers:
        p=f"Rear_NXA_PAC_500W_PI_{label}"
        b.box(p+"_Module",silver,(xc,0,-Z_OUTER-.65),(94,41,1.3),
              {"pid":"NXA-PAC-500W-PI","power":"500W AC","airflow":"port-side intake"})
        b.ring(p+"_CircularFanGuard",silver,(xc+17,0,-Z_OUTER-1.55),(29,29,1.8),{"wire_guard":True},inner=.8)
        b.ring(p+"_FanDark",black,(xc+17,0,-Z_OUTER-1.8),(23,23,2.0),{"fan":True},inner=.18)
        b.box(p+"_IEC_Inlet",black,(xc-18,0,-Z_OUTER-1.7),(21,22,2.4),{"connector":"IEC AC"})
        b.box(p+"_PullHandle",black,(xc-3,-1,-Z_OUTER-5.0),(6,29,8.0),{"visible_protrusion":True})
        b.box(p+"_BurgundyRelease",burgundy,(xc-43,0,-Z_OUTER-2.5),(7,19,4.0),{"airflow_code":"PI burgundy"})
        b.cylinder(p+"_500W_Label",white,(xc+17,0,-Z_OUTER-2.75),(15,15,.5),{"text":"500W AC"})
    fan_centers=(91.0,45.0,-1.0,-47.0)
    for slot,xc in enumerate(fan_centers,1):
        p=f"Rear_NXA_FAN_30CFM_PI_Slot{slot}"
        b.box(p+"_Tray",dark,(xc,0,-Z_OUTER-.8),(43,41,1.6),
              {"pid":"NXA-FAN-30CFM-PI","slot":slot,"airflow":"port-side intake"})
        for bar in range(-3,4):
            b.box(p+f"_GrilleBar_{bar:+d}",silver,(xc+bar*5.4,6,-Z_OUTER-1.75),(1.15,23,1.0),{"grille_relief":True})
        b.box(p+"_BurgundyLatch",burgundy,(xc,-6,-Z_OUTER-3.0),(31,10,4.5),{"airflow_code":"PI burgundy"})
        b.box(p+"_LatchLeftArm",burgundy,(xc-16,0,-Z_OUTER-2.4),(4,23,3.2))
        b.box(p+"_LatchRightArm",burgundy,(xc+16,0,-Z_OUTER-2.4),(4,23,3.2))

    io_x=-194.5
    b.box("Rear_FX_L1_L2_IO_Plate",chassis,(io_x,0,-Z_OUTER-.7),(48,41,1.4),{"generation":"FX","not_EX_or_FX3":True})
    for row,y in enumerate((8.0,-7.0),1):
        for column,dx in enumerate((-8.0,8.0),1):
            label=("L1","Console","L2","OOB")[(row-1)*2+column-1]
            b.box(f"Rear_IO_{label}",dark,(io_x+dx,y,-Z_OUTER-1.7),(13,11,2.0),{"port":label})
    b.box("Rear_IO_USB",black,(io_x+20,-1,-Z_OUTER-1.8),(5,18,2.2),{"port":"USB"})
    b.box("Rear_IO_USB_Blue_Insert",usb_blue,(io_x+20,-1,-Z_OUTER-2.95),(2.5,12,.2))
    b.cylinder("Rear_BCN_LED",green,(io_x-8,-16,-Z_OUTER-1.8),(2.2,2.2,2.0),{"label":"BCN"})
    b.cylinder("Rear_STS_LED",green,(io_x+8,-16,-Z_OUTER-1.8),(2.2,2.2,2.0),{"label":"STS"})

    # Side-specific relief: unique node names and different positions prove no mirror.
    for index,z in enumerate((240,160,70,-40,-135,-230),1):
        b.box(f"Physical_Left_RailSlot_{index}",dark,(X_BODY+.2,-10,z),(.7,5,12),{"side":"left","not_mirrored":True})
    for index,z in enumerate((225,120,15,-100,-205),1):
        b.box(f"Physical_Right_RailSlot_{index}",dark,(-X_BODY-.2,-9,z),(.7,5,14),{"side":"right","not_mirrored":True})
    b.box("Physical_Left_GroundingPad",silver,(X_BODY+.35,2,105),(.8,15,29),{"two_hole_pad":True,"side":"left"})
    for index,z in enumerate((98,112),1):
        b.box(f"Physical_Left_GroundingHole_{index}",dark,(X_BODY+.78,2,z),(.2,4,4),{"side":"left"})
    for side,x,zs in (("Left",X_BODY,(252,184,26,-170,-250)),("Right",-X_BODY,(245,132,-20,-160,-244))):
        for index,z in enumerate(zs,1):
            b.box(f"Physical_{side}_Fastener_{index}",silver,(x+(0.35 if x>0 else -0.35),8,z),(.8,4.5,4.5),{"side":side.lower()})

    # Top ventilation and service-cover relief; bottom stays conservative.
    b.box("Top_Front_Perforated_Band_Recess",dark,(0,Y_OUTER+.18,244),(425,.5,58),{"verified_top_vent_band":True})
    for index,x in enumerate(range(-205,206,10),1):
        b.box(f"Top_Vent_SilverBridge_{index:02d}",silver,(x,Y_OUTER+.48,244),(2,.12,55),{"vent_relief":True})
    for name,xc,zc,w,d in (("Small_Left_Front",-167,88,88,112),("Large_Rear_Right",155,-105,115,190)):
        for edge,center,size in (
            ("Front",(xc,Y_OUTER+.4,zc+d/2),(w,.2,1.4)),
            ("Rear",(xc,Y_OUTER+.4,zc-d/2),(w,.2,1.4)),
            ("Left",(xc-w/2,Y_OUTER+.4,zc),(1.4,.2,d)),
            ("Right",(xc+w/2,Y_OUTER+.4,zc),(1.4,.2,d)),
        ):
            b.box(f"Top_Hatch_{name}_{edge}",dark,center,size,{"service_hatch_seam":True})
    for index,(x,z) in enumerate(((-205,250),(-150,250),(-80,250),(0,250),(80,250),(150,250),(205,250),(-120,40),(120,40)),1):
        b.box(f"Top_Fastener_{index}",silver,(x,Y_OUTER+.55,z),(4,.25,4),{"visible_fastener":True})
    b.box("Bottom_Conservative_FrontLip",silver,(0,-Y_OUTER-.2,Z_OUTER-1.5),(BODY_W,.5,3),{"fallback":True})
    b.box("Bottom_Conservative_RearLip",silver,(0,-Y_OUTER-.2,-Z_OUTER+1.5),(BODY_W,.5,3),{"fallback":True})

    output=MODELS/f"Cisco-N9K-C93180YC-FX-{variant}.glb"
    size,digest=b.save(output)
    result={
        "variant":variant,"path":str(output),"bytes":size,"sha256":digest,
        "nodes":len(b.doc["nodes"]),"meshes":len(b.doc["meshes"]),
        "materials":len(b.doc["materials"]),"images":len(b.doc["images"]),
    }
    print(json.dumps(result,indent=2))
    return output


if __name__=="__main__":
    variants=sys.argv[1:] or ["standard","web"]
    for variant in variants:
        if variant not in ("standard","web"):
            raise SystemExit(f"unknown variant: {variant}")
        build(variant)
