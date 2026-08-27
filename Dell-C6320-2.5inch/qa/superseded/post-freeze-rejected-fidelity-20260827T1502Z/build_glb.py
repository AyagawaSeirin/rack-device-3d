#!/usr/bin/env python3
"""Deterministically build the exact-appearance Dell C6300 + 4x C6320 GLBs."""

from __future__ import annotations

import hashlib
import json
import math
import struct
import sys
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
VIEWS = ROOT / "views"
MODELS = ROOT / "models"
INTERMEDIATE = ROOT / "qa" / "intermediate"

W, H, D = 482.3, 86.8, 795.9
BODY_W = 448.0
MM = 0.001
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
                "generator": "Codex deterministic exact-appearance rack-device builder",
                "copyright": "Product marks remain property of Dell Technologies",
                "extras": {
                    "identity": "Dell PowerEdge C6300 enclosure with four standard C6320 sleds",
                    "installed_configuration": "24 x 2.5-inch front carriers; four dual-SFP+ C6320 nodes; two matching 1400 W AC shared PSUs",
                    "not_variants": ["C6320p", "bare C6300", "C4130", "HVDC PSU", "1600 W PSU"],
                    "dimensions_mm": {"overall_width": W, "body_width": BODY_W, "height": H, "depth": D},
                    "world_units": "metres",
                    "orientation": "+X device right from front, +Y up, +Z front",
                    "bottom_evidence": "GENERIC_BOTTOM_FALLBACK after exhaustive search",
                    "official_public_3d": "not found as of 2026-08-24",
                    "variant": variant,
                },
            },
            "scene": 0,
            "scenes": [{"name": "Exact_Product_Scene", "nodes": [0]}],
            "nodes": [{"name": "Dell_PowerEdge_C6300_4xC6320_24SFF", "children": [], "extras": {"rack_units": 2}}],
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

    def add_node(self, name, mesh, translation=None, scale=None, extras=None):
        node={"name":name,"mesh":mesh}
        # Builder dimensions are authored in millimetres; glTF world units are
        # metres. The pre-review file omitted this conversion and was 1000x too
        # large, degrading depth precision in both WebGL engines.
        if translation is not None: node["translation"]=[round(float(v)*MM,9) for v in translation]
        if scale is not None: node["scale"]=[round(float(v)*MM,9) for v in scale]
        if extras: node["extras"]=extras
        index=len(self.doc["nodes"]); self.doc["nodes"].append(node); self.doc["nodes"][0]["children"].append(index)
        return index

    def box(self, name, material, center, size, extras=None):
        return self.add_node(name, self.cube_mesh(material), center, size, extras)

    def cylinder(self, name, material, center, size, extras=None):
        return self.add_node(name, self.cylinder_mesh(material), center, size, extras)

    def ring(self, name, material, center, size, extras=None, inner=.62):
        return self.add_node(name, self.ring_mesh(material, inner=inner), center, size, extras)

    def plane(self, name, material, positions, normal, uvs=None, extras=None):
        if uvs is None:
            uvs=[(0,1),(1,1),(1,0),(0,0)]
        positions=[tuple(float(value)*MM for value in point) for point in positions]
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
    if variant=="standard":
        result={face:VIEWS/f"{face}.png" for face in ("front","rear","left","right","top","bottom")}
    else:
        out=INTERMEDIATE/variant/"views"; out.mkdir(parents=True,exist_ok=True); result={}
        targets={"front":(1536,277),"rear":(1536,277),"left":(1536,168),"right":(1536,168),"top":(865,1536),"bottom":(865,1536)}
        for face,size in targets.items():
            image=Image.open(VIEWS/f"{face}.png").convert("RGBA").resize(size,Image.Resampling.LANCZOS)
            path=out/f"{face}.png"; image.save(path,optimize=True); result[face]=path
    return result


def build(variant):
    tex=prepare_textures(variant)
    b=GLBBuilder(variant)
    chassis=b.add_solid_material("Galvanized_Steel",[.64,.67,.70,1],.58,.58)
    silver=b.add_solid_material("Bright_Steel",[.76,.79,.81,1],.72,.42)
    black=b.add_solid_material("Black_Handles",[.018,.022,.026,1],.08,.42)
    dark=b.add_solid_material("Dark_Recess",[.055,.065,.075,1],.05,.62)
    orange=b.add_solid_material("PSU_Orange_Release",[.95,.18,.015,1],0,.5)
    yellow=b.add_solid_material("Factory_Warning_Yellow",[.92,.74,.045,1],0,.72)
    blue=b.add_solid_material("Dell_Blue_IO",[.015,.16,.62,1],.05,.48)
    green=b.add_solid_material("Status_LED_Green",[.01,.75,.13,1],0,.3,[0,.35,.04])
    white=b.add_solid_material("Label_White",[.92,.94,.95,1],0,.85)
    photos={face:b.add_photo_material(f"FACE_{face.upper()}_SOURCE_LOCKED",path) for face,path in tex.items() if face in ("front","rear","left","right","top","bottom")}

    # The structural core sits just behind the six independently textured outer
    # skins and modeled relief, avoiding coplanar depth conflicts in WebGL.
    b.box("Closed_2U_Chassis_Core",chassis,(0,0,0),(BODY_W-1,H-.8,D-.9),{"evidence":"Dell enclosure dimensions","closed_manifold_core":True})
    crop=(W-BODY_W)/(2*W); uvs=[(crop,1),(1-crop,1),(1-crop,0),(crop,0)]
    # Deterministic card/core/relief spacing. Canonical photographs sit behind
    # their separately modelled relief instead of 0.01-0.05 mm from duplicate
    # photo cards. Side names now follow +X=device-right from the front.
    b.plane("Front_SourceLocked_Texture",photos["front"],[(-X_BODY,-Y_OUTER,Z_OUTER-.80),(X_BODY,-Y_OUTER,Z_OUTER-.80),(X_BODY,Y_OUTER,Z_OUTER-.80),(-X_BODY,Y_OUTER,Z_OUTER-.80)],(0,0,1),uvs,{"source_lock":"front","role":"gap and chassis backing texture","clearance_mm":.60})
    b.plane("Rear_SourceLocked_Texture",photos["rear"],[(X_BODY,-Y_OUTER,-Z_OUTER+.80),(-X_BODY,-Y_OUTER,-Z_OUTER+.80),(-X_BODY,Y_OUTER,-Z_OUTER+.80),(X_BODY,Y_OUTER,-Z_OUTER+.80)],(0,0,-1),uvs,{"source_lock":"rear","clearance_mm":.55})
    left_x=-X_BODY+.60; right_x=X_BODY-.60
    b.plane("Physical_Left_SourceLocked_Texture",photos["left"],[(left_x,-Y_OUTER,-Z_OUTER),(left_x,-Y_OUTER,Z_OUTER),(left_x,Y_OUTER,Z_OUTER),(left_x,Y_OUTER,-Z_OUTER)],(-1,0,0),extras={"image_left":"rear","image_right":"front","not_mirrored":True,"clearance_mm":.60})
    b.plane("Physical_Right_SourceLocked_Texture",photos["right"],[(right_x,-Y_OUTER,Z_OUTER),(right_x,-Y_OUTER,-Z_OUTER),(right_x,Y_OUTER,-Z_OUTER),(right_x,Y_OUTER,Z_OUTER)],(1,0,0),extras={"image_left":"front","image_right":"rear","not_mirrored":True,"clearance_mm":.60})
    b.plane("Top_SourceLocked_Texture",photos["top"],[(-X_BODY,Y_OUTER-.80,Z_OUTER),(X_BODY,Y_OUTER-.80,Z_OUTER),(X_BODY,Y_OUTER-.80,-Z_OUTER),(-X_BODY,Y_OUTER-.80,-Z_OUTER)],(0,1,0),extras={"front_in_image":"bottom","clearance_mm":.75})
    b.plane("Bottom_GenericFallback_Texture",photos["bottom"],[(X_BODY,-Y_OUTER+.50,Z_OUTER),(-X_BODY,-Y_OUTER+.50,Z_OUTER),(-X_BODY,-Y_OUTER+.50,-Z_OUTER),(X_BODY,-Y_OUTER+.50,-Z_OUTER)],(0,-1,0),extras={"status":"GENERIC_BOTTOM_FALLBACK","clearance_mm":.35})

    # Front ears with real open rack holes; ears exist only at the front.
    for side,sign in (("Left",-1),("Right",1)):
        x_outer=sign*(X_BODY+(X_OUTER-X_BODY)/2)
        b.box(f"Front_{side}_Ear_OuterRail",black,(sign*(X_OUTER-2),0,Z_OUTER-.35),(4,H,.3))
        b.box(f"Front_{side}_Ear_InnerRail",black,(sign*(X_BODY+2),0,Z_OUTER-.35),(4,H,.3))
        b.box(f"Front_{side}_Ear_TopBridge",black,(x_outer,Y_OUTER-5,Z_OUTER-.25),(X_OUTER-X_BODY-8,10,.3))
        b.box(f"Front_{side}_Ear_BottomBridge",black,(x_outer,-Y_OUTER+5,Z_OUTER-.25),(X_OUTER-X_BODY-8,10,.3))
        b.ring(f"Front_{side}_Ear_LargeRackHole",black,(sign*233.15,-27,Z_OUTER-.15),(16,16,.2),{"true_through_hole":True,"layered_clearance_mm":.05},inner=.64)
        b.ring(f"Front_{side}_Ear_SmallMechanicalHole",black,(sign*233.15,25,Z_OUTER-.15),(7,7,.2),{"true_through_hole":True,"layered_clearance_mm":.05},inner=.6)
        for index,(xf,yf) in enumerate(((230.0,35),(236.0,12),(230.0,-3),(236.0,-39)),1):
            b.cylinder(f"Front_{side}_Ear_Fastener_{index}",silver,(sign*xf,yf,Z_OUTER-.003),(3,3,.006),{"verified_ear_fastener":True})

    # Front control panels, non-usable cover, and 24 independently modeled SFF carriers.
    b.box("Front_Left_Control_Panel",dark,(-213,0,Z_OUTER-.25),(20,75,.44))
    b.box("Front_Right_Control_Panel",dark,(213,0,Z_OUTER-.25),(20,75,.44))
    b.box("Front_Nonusable_Drive_Cover",black,(193,0,Z_OUTER-.23),(11,75,.46),{"not_a_drive_bay":True})
    def front_u(x): return .5 + x / W
    def front_v(y): return .5 - y / H
    for label,x0,x1 in (("LeftControl",-223,-203),("RightControl",203,223)):
        b.plane(f"Front_{label}_SourceTexture",photos["front"],[(x0,-37,Z_OUTER-.20),(x1,-37,Z_OUTER-.20),(x1,37,Z_OUTER-.20),(x0,37,Z_OUTER-.20)],(0,0,1),[(front_u(x0),front_v(-37)),(front_u(x1),front_v(-37)),(front_u(x1),front_v(37)),(front_u(x0),front_v(37))])
    bay_w,gap,group_extra=14.2,1.0,2.5
    total=24*bay_w+23*gap+3*group_extra; start=-total/2
    for i in range(24):
        group=i//6; x=start+bay_w/2+i*(bay_w+gap)+group*group_extra
        prefix=f"SFF_Carrier_{i+1:02d}"
        b.box(prefix+"_Body",black,(x,-1,Z_OUTER-.25),(bay_w,74,.44),{"drive_form_factor_in":2.5,"bay_index":i+1})
        x0,x1=x-bay_w/2,x+bay_w/2
        b.plane(prefix+"_SourceTexture",photos["front"],[(x0,-38,Z_OUTER-.20),(x1,-38,Z_OUTER-.20),(x1,36,Z_OUTER-.20),(x0,36,Z_OUTER-.20)],(0,0,1),[(front_u(x0),front_v(-38)),(front_u(x1),front_v(-38)),(front_u(x1),front_v(36)),(front_u(x0),front_v(36))],{"bay_index":i+1,"source_lock":"front","clearance_mm":.18})
        b.box(prefix+"_TopLatch",silver,(x,25,Z_OUTER-.025),(9,11,.01))
        b.box(prefix+"_Handle",dark,(x,-7,Z_OUTER-.024),(3.2,32,.008))
        b.cylinder(prefix+"_LatchButton",silver,(x,24,Z_OUTER-.023),(6,6,.006))
        b.box(prefix+"_BottomTooth",silver,(x,-36.5,Z_OUTER-.024),(bay_w-2,2,.008))
    for i,x in enumerate((-213,213)):
        b.cylinder(f"Front_Control_PowerButton_{i+1}",silver,(x,9,Z_OUTER-.023),(6,6,.006))
        b.cylinder(f"Front_Control_StatusLED_{i+1}",green,(x,-4,Z_OUTER-.022),(2.2,2.2,.004))
    # The genuine photographed Dell logo stays in the source-locked control
    # crop. No programmatically redrawn or duplicate logo plane is added.

    # Rear: four standard C6320 nodes, each with the exact required visible I/O set.
    node_centers_x=(-132,53); row_centers=(21,-21)
    for row,yc in enumerate(row_centers,1):
        for col,xc in enumerate(node_centers_x,1):
            node=(row-1)*2+col; p=f"C6320_Node_{node}"
            b.box(p+"_PerimeterTop",silver,(xc,yc+18,-Z_OUTER+.25),(177,3,.2),{"node_model":"PowerEdge C6320","not_c6320p":True})
            b.box(p+"_PCIeCarrier",silver,(xc-22,yc+7,-Z_OUTER+.25),(128,18,.2),{"slot":"low-profile PCIe/blank"})
            b.box(p+"_PCIeVent",dark,(xc-35,yc+7,-Z_OUTER+.055),(86,12,.01))
            ports=[("USB3",-78,blue,(10,8,.6)),("SFPplus_A",-57,dark,(17,10,.6)),("SFPplus_B",-37,dark,(17,10,.6)),("iDRAC_RJ45",-10,black,(16,12,.6)),("USB_to_Serial",14,black,(10,9,.6)),("VGA",40,blue,(23,13,.6)),("Power_Status",72,black,(11,11,.6))]
            for label,dx,mat,size in ports:
                b.box(f"{p}_{label}",mat,(xc+dx,yc-11,-Z_OUTER+.25),(size[0],size[1],.2),{"node":node,"port":label})
            b.cylinder(p+"_PowerLED",green,(xc+72,yc-11,-Z_OUTER+.003),(3,3,.006))
            b.box(p+"_PullTab",black,(xc+82,yc+5,-Z_OUTER+.25),(13,25,.2),{"node":node,"label":"POWEREDGE C6320"})
            # Factory POWEREDGE C6320 markings remain in the binding rear photo;
            # a synthetic duplicate label plane would compete in depth.

    # Two matching 1400 W AC shared PSUs stacked at device right / rear viewer-left.
    for index,yc in enumerate((21,-21),1):
        p=f"Shared_AC_PSU_1400W_{index}"
        b.box(p+"_Face",silver,(190,yc,-Z_OUTER+.25),(66,39,.2),{"power_input":"AC","rating_w":1400,"matched_pair":True})
        b.ring(p+"_FanGuard",silver,(205,yc,-Z_OUTER+.20),(24,24,.10),{"fan":True,"wire_guard":True,"layer":"guard-ring"},inner=.82)
        b.ring(p+"_FanInner",black,(205,yc,-Z_OUTER+.35),(20,20,.10),{"fan":True,"layer":"recessed-fan"},inner=.22)
        for angle in (0,45,90,135):
            rad=math.radians(angle); sx=30 if angle%90==0 else 22; sy=3 if angle%90==0 else 2.5
            # Axis-aligned/crossed bars approximate the verified silver wire guard.
            if angle==0: b.box(p+"_GuardHorizontal",silver,(205,yc,-Z_OUTER+.08),(22,1.2,.06))
            elif angle==90: b.box(p+"_GuardVertical",silver,(205,yc,-Z_OUTER+.03),(1.2,22,.04))
        b.box(p+"_IEC_AC_Inlet",black,(174,yc,-Z_OUTER+.24),(19,16,.48),{"connector":"IEC AC inlet"})
        b.box(p+"_OrangeRelease",orange,(161,yc,-Z_OUTER+.08),(5,19,.16))
        b.box(p+"_HandleRecess",dark,(184,yc,-Z_OUTER+.18),(7,22,.1))

    # Side-specific rail slots and right-only access/recess features.
    for side,x,photo_name in (("Physical_Left",-X_BODY,photos["left"]),("Physical_Right",X_BODY,photos["right"])):
        inward=-.3 if x>0 else .3
        for index,z in enumerate((-245,0,245),1):
            b.box(f"{side}_MajorKeySlot_{index}",dark,(x+inward,-10,z),(.6,6,48),{"side_specific":side})
            b.box(f"{side}_KeySlotFlank_{index}_A",dark,(x+inward,-10,z-30),(.6,4,7))
            b.box(f"{side}_KeySlotFlank_{index}_B",dark,(x+inward,-10,z+30),(.6,4,7))
        for index,z in enumerate((-330,-180,-70,85,180,320),1):
            b.box(f"{side}_Fastener_{index}",silver,(x+inward,7,z),(.6,6,6))
    b.box("Physical_Right_VerticalAccessSlot",dark,(X_BODY-.3,-9,205),(.6,26,7),{"right_only":True})
    for index,z in enumerate((120,290),1):
        b.box(f"Physical_Right_UpperRecess_{index}",silver,(X_BODY-.3,19,z),(.6,11,46),{"right_only":True})

    # Four source-verified shared fan-cage rotors under the installed opaque
    # cover. They are configuration nodes and never leak through the closed core.
    for index,x in enumerate((-150,-50,50,150),1):
        b.box(f"Internal_Shared_Fan_{index}_Housing",black,(x,0,80),(44,70,55),{"internal":True,"installed":True})
        b.cylinder(f"Internal_Shared_Fan_{index}_Rotor",dark,(x,0,80),(34,34,20),{"internal":True,"installed":True})

    # Closed top lid relief, seams, pads, and conservative bottom perimeter only.
    b.box("Top_Cover_Stepped_Seam",silver,(0,Y_OUTER-.3,-240),(BODY_W,.1,2.5))
    for index,x in enumerate((-128,128),1):
        b.box(f"Top_Longitudinal_Seam_{index}",silver,(x,Y_OUTER-.3,0),(1.5,.1,620))
    b.box("Top_Black_Oval_Pad",black,(-150,Y_OUTER-.3,155),(54,.1,28),{"source":"exact service-angle photo"})
    b.box("Top_Blue_Pad_Center",blue,(-150,Y_OUTER-.24,155),(15,.02,15))
    b.box("Top_Blue_Rectangular_Pad",blue,(155,Y_OUTER-.3,140),(42,.1,52),{"source":"exact service-angle photo"})
    for label,mat,x,width,depth in (("Black",dark,-90,70,30),("Yellow",yellow,0,70,26),("White",white,90,50,26)):
        b.box(f"Top_Factory_Label_Block_{label}",mat,(x,Y_OUTER-.005,330),(width,.01,depth),{"factory_label_block":True,"no_pseudo_text":True})
    b.box("Bottom_Conservative_FrontLip",silver,(0,-Y_OUTER+.15,Z_OUTER-1.5),(BODY_W,.3,3),{"fallback":True})
    b.box("Bottom_Conservative_RearLip",silver,(0,-Y_OUTER+.15,-Z_OUTER+1.5),(BODY_W,.3,3),{"fallback":True})

    output=MODELS/f"Dell-PowerEdge-C6300-4xC6320-24SFF-{variant}.glb"
    size,digest=b.save(output)
    print(json.dumps({"variant":variant,"path":str(output),"bytes":size,"sha256":digest,"nodes":len(b.doc["nodes"]),"meshes":len(b.doc["meshes"]),"materials":len(b.doc["materials"]),"images":len(b.doc["images"])},indent=2))
    return output


if __name__=="__main__":
    variants=sys.argv[1:] or ["standard","web"]
    for variant in variants:
        if variant not in ("standard","web"): raise SystemExit(f"unknown variant: {variant}")
        build(variant)
