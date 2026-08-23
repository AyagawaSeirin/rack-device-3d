#!/usr/bin/env python3
"""Build exact-exterior Dell PowerEdge R720 8LFF website GLBs.

This is a newly constructed exterior model; no official or third-party mesh is
copied. Coordinates are metres in a right-handed glTF frame:
+X device right from the front, +Y up, +Z front.
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

import numpy as np
from PIL import Image
from pygltflib import GLTF2
import trimesh
from trimesh.visual import TextureVisuals
from trimesh.visual.material import PBRMaterial


ROOT = Path(__file__).resolve().parents[1]
VIEWS = ROOT / "views"
MODEL = ROOT / "model"

BODY_W = 0.4440
BODY_H = 0.0873
BODY_D = 0.7020
RACK_W = 0.4824
EAR_EXT = (RACK_W - BODY_W) / 2.0
FRONT_Z = 0.3510
REAR_Z = -0.3510
REAR_MOST_Z = -0.3900
REAR_PROJECTION = REAR_Z - REAR_MOST_Z


def pbr(name: str, rgba, metallic: float = 0.0, roughness: float = 0.78) -> PBRMaterial:
    return PBRMaterial(
        name=name,
        baseColorFactor=list(rgba),
        metallicFactor=metallic,
        roughnessFactor=roughness,
        alphaMode="OPAQUE",
        doubleSided=False,
    )


MAT_BODY = pbr("Dell galvanized chassis steel", (188, 191, 189, 255), 0.46, 0.55)
MAT_SILVER = pbr("Dell plated carrier and connector steel", (176, 179, 177, 255), 0.56, 0.42)
MAT_DARK_SILVER = pbr("Dell dark galvanized relief", (102, 106, 105, 255), 0.36, 0.59)
MAT_BLACK = pbr("Dell black polymer and connector cavities", (13, 15, 16, 255), 0.0, 0.86)
MAT_DARK = pbr("Deep fan vent and port cavity", (23, 26, 27, 255), 0.0, 0.92)
MAT_ORANGE = pbr("Dell carrier and PSU release orange", (202, 80, 24, 255), 0.0, 0.56)
MAT_GREEN = pbr("Dell status lens green", (39, 188, 74, 255), 0.0, 0.31)
MAT_BLUE = pbr("Dell VGA and LCD blue", (24, 118, 177, 255), 0.0, 0.44)
MAT_TEAL = pbr("Dell serial port teal", (35, 148, 145, 255), 0.0, 0.48)
MAT_GOLD = pbr("Connector pin gold", (190, 143, 53, 255), 0.62, 0.34)
MAT_LABEL = pbr("Dell factory label neutral", (218, 219, 215, 255), 0.0, 0.84)


def set_material(mesh: trimesh.Trimesh, material: PBRMaterial) -> trimesh.Trimesh:
    mesh.visual = TextureVisuals(
        uv=np.zeros((len(mesh.vertices), 2), dtype=np.float32), material=material
    )
    return mesh


def make_box(extents, center, material=MAT_BODY) -> trimesh.Trimesh:
    mesh = trimesh.creation.box(extents=np.asarray(extents, dtype=float))
    mesh.apply_translation(np.asarray(center, dtype=float))
    return set_material(mesh, material)


def make_cylinder(radius, height, center, material, sections=24, axis=(0, 0, 1)):
    mesh = trimesh.creation.cylinder(radius=radius, height=height, sections=sections)
    axis = np.asarray(axis, dtype=float)
    axis /= np.linalg.norm(axis)
    transform = trimesh.geometry.align_vectors([0.0, 0.0, 1.0], axis)
    mesh.apply_transform(transform)
    mesh.apply_translation(np.asarray(center, dtype=float))
    return set_material(mesh, material)


def cylinder_between(a, b, radius, material, sections=24):
    a = np.asarray(a, dtype=float)
    b = np.asarray(b, dtype=float)
    delta = b - a
    return make_cylinder(radius, np.linalg.norm(delta), (a + b) / 2.0,
                         material, sections, delta)


def add(scene: trimesh.Scene, name: str, mesh: trimesh.Trimesh) -> None:
    mesh.metadata["name"] = name
    scene.add_geometry(mesh, node_name=name, geom_name=name)


def add_group(scene: trimesh.Scene, name: str, meshes, material: PBRMaterial) -> None:
    if not meshes:
        return
    merged = trimesh.util.concatenate(meshes)
    set_material(merged, material)
    add(scene, name, merged)


def opaque_texture(image: Image.Image) -> Image.Image:
    return image.convert("RGB")


def profile_texture(face: str, profile: str) -> Image.Image:
    image = opaque_texture(Image.open(VIEWS / f"{face}.png"))
    if profile == "web":
        targets = {
            "front": (2048, 371),
            "rear": (2048, 403),
            "left": (2048, 253),
            "right": (2048, 255),
            "top": (1294, 2048),
            "bottom": (1295, 2048),
        }
        image = image.resize(targets[face], Image.Resampling.LANCZOS)
    return image


def texture_material(face: str, image: Image.Image) -> PBRMaterial:
    mode = "GENERIC_BOTTOM_FALLBACK" if face == "bottom" else "SOURCE_LOCKED"
    return PBRMaterial(
        name=f"FACE_{face.upper()}_{mode}_IMAGEGEN_PHOTOGRAPHIC",
        baseColorFactor=[255, 255, 255, 255],
        baseColorTexture=image,
        metallicFactor=0.0,
        roughnessFactor=0.90,
        alphaMode="OPAQUE",
        doubleSided=False,
    )


def textured_quad(face: str, image: Image.Image) -> trimesh.Trimesh:
    x0, x1 = -BODY_W / 2.0, BODY_W / 2.0
    y0, y1 = -BODY_H / 2.0, BODY_H / 2.0
    z0, z1 = REAR_Z, FRONT_Z
    eps = 0.00005
    if face == "front":
        x0, x1 = -RACK_W / 2.0, RACK_W / 2.0
        # The photographic skin is the recessed front substrate. Independent
        # carriers, controls and rack latches sit in front of it up to FRONT_Z.
        skin_z = z1 - 0.0055
        vertices = [[x0, y0, skin_z], [x1, y0, skin_z],
                    [x1, y1, skin_z], [x0, y1, skin_z]]
    elif face == "rear":
        vertices = [[x1, y0, z0 - eps], [x0, y0, z0 - eps],
                    [x0, y1, z0 - eps], [x1, y1, z0 - eps]]
    elif face == "left":
        vertices = [[x0 - eps, y0, z0], [x0 - eps, y0, z1],
                    [x0 - eps, y1, z1], [x0 - eps, y1, z0]]
    elif face == "right":
        vertices = [[x1 + eps, y0, z1], [x1 + eps, y0, z0],
                    [x1 + eps, y1, z0], [x1 + eps, y1, z1]]
    elif face == "top":
        vertices = [[x0, y1, z1], [x1, y1, z1],
                    [x1, y1, z0], [x0, y1, z0]]
    elif face == "bottom":
        vertices = [[x1, y0, z1], [x0, y0, z1],
                    [x0, y0, z0], [x1, y0, z0]]
    else:
        raise ValueError(face)
    mesh = trimesh.Trimesh(
        vertices=np.asarray(vertices, dtype=float),
        faces=np.asarray([[0, 1, 2], [0, 2, 3]], dtype=np.int64),
        process=False,
    )
    mesh.visual = TextureVisuals(
        uv=np.asarray([[0, 0], [1, 0], [1, 1], [0, 1]], dtype=np.float32),
        material=texture_material(face, image),
    )
    return mesh


def add_frame(scene: trimesh.Scene, prefix: str, cx: float, cy: float,
              width: float, height: float, depth: float, z: float,
              rail: float, material: PBRMaterial) -> None:
    add(scene, f"{prefix}_Top", make_box([width, rail, depth],
        [cx, cy + (height - rail) / 2.0, z], material))
    add(scene, f"{prefix}_Bottom", make_box([width, rail, depth],
        [cx, cy - (height - rail) / 2.0, z], material))
    add(scene, f"{prefix}_Left", make_box([rail, height - 2 * rail, depth],
        [cx - (width - rail) / 2.0, cy, z], material))
    add(scene, f"{prefix}_Right", make_box([rail, height - 2 * rail, depth],
        [cx + (width - rail) / 2.0, cy, z], material))


def add_front(scene: trimesh.Scene, sections: int) -> None:
    # Front-only rack latch/ear assemblies. They do not continue to the rear.
    for sign, side in ((-1, "Left"), (1, "Right")):
        x = sign * (BODY_W / 2.0 + EAR_EXT / 2.0)
        add_frame(scene, f"Front_Rack_Latch_Ear_{side}_Independent",
                  x, 0, EAR_EXT, BODY_H, 0.008,
                  FRONT_Z - 0.004, 0.0010, MAT_BLACK)
        # Close the ear from behind so a rear camera sees a real black flange,
        # while the front source texture remains visible on the forward face.
        add(scene, f"Front_Rack_Latch_Ear_{side}_Rear_Closure",
            make_box([EAR_EXT, BODY_H, 0.0010],
                     [x, 0, FRONT_Z - 0.0075], MAT_BLACK))

    x_centers = (-0.1600, -0.0534, 0.0534, 0.1600)
    y_centers = (0.0010, -0.0270)
    for row, cy in enumerate(y_centers, start=1):
        for col, cx in enumerate(x_centers, start=1):
            index = (row - 1) * 4 + col
            # The imagegen photograph supplies the exact carrier surface and
            # four-aperture handle texture. Thin perimeter geometry supplies
            # the real separate-carrier seam and oblique-view parallax.
            add_frame(scene, f"Front_LFF_{index}_Carrier_Perimeter",
                      cx, cy, 0.102, 0.025, 0.0030,
                      FRONT_Z - 0.0030, 0.0013, MAT_DARK_SILVER)

    # VGA, USB, vFlash, LCD controls, factory text and the optical-tray face
    # are flush details and remain exclusively in the exact source texture.


def add_perforated_blank(scene, name, center, width, height, z, material, rows, cols):
    # Keep the exact source-locked photographic plate visible; geometry adds
    # only the real perimeter relief and perforation depth instead of laying a
    # generic solid rectangle over the photo.
    add_frame(scene, name, center[0], center[1], width, height, 0.0010,
              z, 0.0005, material)


def rear_psu_photo_quad(name: str, image: Image.Image, cx: float, cy: float,
                        width: float, height: float, z: float) -> trimesh.Trimesh:
    """Map the matching exact rear-photo region to the protruding PSU face."""
    iw, ih = image.size
    screen_x = (BODY_W / 2.0 - cx) / BODY_W * iw
    screen_y = (BODY_H / 2.0 - cy) / BODY_H * ih
    crop_w = width / BODY_W * iw
    crop_h = height / BODY_H * ih
    left = max(0, round(screen_x - crop_w / 2.0))
    right = min(iw, round(screen_x + crop_w / 2.0))
    top = max(0, round(screen_y - crop_h / 2.0))
    bottom = min(ih, round(screen_y + crop_h / 2.0))
    crop = image.crop((left, top, right, bottom))
    if crop.width < 1024:
        target_h = max(1, round(crop.height * 1024 / crop.width))
        crop = crop.resize((1024, target_h), Image.Resampling.LANCZOS)
    material = PBRMaterial(
        name=f"FACE_REAR_{name}_SOURCE_LOCKED_PHOTOGRAPHIC",
        baseColorFactor=[255, 255, 255, 255],
        baseColorTexture=crop,
        metallicFactor=0.0,
        roughnessFactor=0.90,
        alphaMode="OPAQUE",
        doubleSided=False,
    )
    x0, x1 = cx - width / 2.0, cx + width / 2.0
    y0, y1 = cy - height / 2.0, cy + height / 2.0
    vertices = [[x1, y0, z], [x0, y0, z], [x0, y1, z], [x1, y1, z]]
    mesh = trimesh.Trimesh(
        vertices=np.asarray(vertices, dtype=float),
        faces=np.asarray([[0, 1, 2], [0, 2, 3]], dtype=np.int64),
        process=False,
    )
    mesh.visual = TextureVisuals(
        uv=np.asarray([[0, 0], [1, 0], [1, 1], [0, 1]], dtype=np.float32),
        material=material,
    )
    return mesh


def add_rear_fan(scene: trimesh.Scene, name: str, cx: float, cy: float,
                 z: float, radius: float, sections: int) -> None:
    add(scene, f"{name}_Dark_Cavity",
        make_cylinder(radius, 0.0020, [cx, cy, z], MAT_DARK, sections, (0, 0, 1)))
    blades = []
    for angle in np.linspace(0, 2 * math.pi, 7, endpoint=False):
        blade = make_box([radius * 0.95, radius * 0.15, 0.0014],
                         [cx, cy, z - 0.0003], MAT_BLACK)
        blade.apply_transform(trimesh.transformations.rotation_matrix(
            angle, [0, 0, 1], [cx, cy, z]))
        blades.append(blade)
    add_group(scene, f"{name}_Seven_Blades", blades, MAT_BLACK)
    add(scene, f"{name}_Hub",
        make_cylinder(radius * 0.31, 0.0018, [cx, cy, z - 0.0003],
                      MAT_DARK_SILVER, sections, (0, 0, 1)))


def add_rear(scene: trimesh.Scene, sections: int, rear_image: Image.Image) -> None:
    zface = REAR_Z - 0.0025
    # Rear camera reverses world X. Screen-left low-profile slots use +X.
    for idx, cy in enumerate((0.028, 0.005, -0.018), start=1):
        add_perforated_blank(scene, f"Rear_PCIe_LowProfile_Blank_{idx}",
            [0.170, cy, zface], 0.084, 0.019, zface, MAT_SILVER, 1, 11)
    for idx, (cx, cy) in enumerate(((0.067, 0.026), (0.067, 0.002),
                                     (-0.054, 0.026), (-0.054, 0.002)), start=4):
        add_perforated_blank(scene, f"Rear_PCIe_FullHeight_Blank_{idx}",
            [cx, cy, zface], 0.105, 0.020, zface, MAT_SILVER, 1, 13)

    # The exact upper-right vent field remains in the source-locked photo;
    # adding a repeated coarse grid here would obscure its real perforations.

    # Black carrying handle and two mounts, mechanically raised.
    handle_z = REAR_Z - 0.011
    add(scene, "Rear_Carry_Handle_Bar",
        cylinder_between([0.112, -0.020, handle_z], [-0.024, -0.020, handle_z],
                         0.0040, MAT_BLACK, sections))
    for idx, x in enumerate((0.112, -0.024), start=1):
        add(scene, f"Rear_Carry_Handle_Mount_{idx}",
            cylinder_between([x, -0.020, REAR_Z - 0.002],
                             [x, -0.020, handle_z], 0.0036, MAT_BLACK, sections))

    # System-ID, iDRAC7, DB9, VGA, USB and four RJ45 ports are flush/recessed
    # details and remain exclusively in the exact rear photograph.

    # Two complete 750W AC PSUs with true rear projection to 741 mm bounds.
    for idx, cx in enumerate((-0.120, -0.190), start=1):
        psu_cy, psu_w, psu_h = -0.021, 0.064, 0.044
        add_frame(scene, f"Rear_AC_PSU_{idx}_HotPlug_Extruded_Frame",
                  cx, psu_cy, psu_w, psu_h, REAR_PROJECTION,
                  (REAR_Z + REAR_MOST_Z) / 2.0, 0.0012, MAT_DARK_SILVER)
        add(scene, f"Rear_AC_PSU_{idx}_SourceLocked_OuterFace",
            rear_psu_photo_quad(f"PSU_{idx}", rear_image, cx, psu_cy,
                                psu_w - 0.0024, psu_h - 0.0024,
                                REAR_MOST_Z + 0.00005))


def add_sides(scene: trimesh.Scene, sections: int) -> None:
    patterns = {
        "Left": {"x": -BODY_W / 2.0, "axis": (-1, 0, 0),
                 "pins": [(0.010, 0.286), (-0.005, 0.167), (0.006, -0.010),
                          (-0.006, -0.206), (0.006, -0.317)],
                 "slots": [(0.028, 0.312), (0.027, 0.157), (0.027, -0.055),
                           (0.027, -0.265)]},
        "Right": {"x": BODY_W / 2.0, "axis": (1, 0, 0),
                  "pins": [(0.011, 0.300), (-0.006, 0.194), (0.007, 0.012),
                           (-0.004, -0.180), (0.005, -0.325)],
                  "slots": [(0.029, 0.300), (0.029, 0.090), (0.029, -0.120),
                            (0.029, -0.302)]},
    }
    for side, data in patterns.items():
        sign = -1 if side == "Left" else 1
        for idx, (y, z) in enumerate(data["pins"], start=1):
            add(scene, f"Side_{side}_Rail_Mount_Pin_{idx}",
                make_cylinder(0.0027, 0.0028,
                    [data["x"] + sign * 0.0014, y, z], MAT_SILVER,
                    sections, data["axis"]))
        for idx, (y, z) in enumerate(data["slots"], start=1):
            add(scene, f"Side_{side}_Independent_Cover_Hook_{idx}",
                make_box([0.0015, 0.0050, 0.018],
                    [data["x"] + sign * 0.0008, y, z], MAT_DARK))
        add(scene, f"Side_{side}_Upper_Cover_Seam",
            make_box([0.0010, 0.0014, BODY_D - 0.030],
                [data["x"] + sign * 0.0006, 0.029, 0.0], MAT_DARK_SILVER))
        add(scene, f"Side_{side}_Stamped_Rail_Interface",
            make_box([0.0012, 0.0020, BODY_D - 0.060],
                [data["x"] + sign * 0.0007, 0.012, 0.0], MAT_SILVER))


def add_top(scene: trimesh.Scene, sections: int) -> None:
    y = BODY_H / 2.0 - 0.0018
    add(scene, "Top_Removable_Cover_Perimeter_Seam_Front",
        make_box([BODY_W - 0.004, 0.0010, 0.0015], [0, y, 0.302], MAT_DARK_SILVER))
    add(scene, "Top_Removable_Cover_Perimeter_Seam_Rear",
        make_box([BODY_W - 0.004, 0.0010, 0.0015], [0, y, -0.333], MAT_DARK_SILVER))
    # The shallow top latch is fully resolved in the source-locked top photo;
    # duplicate geometry would create a second false latch.
    for idx, (x, z) in enumerate(((-0.145, 0.185), (0.020, 0.165),
                                  (0.155, 0.120), (-0.135, -0.240),
                                  (0.040, -0.210), (0.155, -0.285)), start=1):
        add(scene, f"Top_Cover_Fastener_{idx}",
            make_cylinder(0.0021, 0.0012, [x, y + 0.0005, z],
                          MAT_DARK_SILVER, 16, (0, 1, 0)))
    holes = []
    for row in range(3):
        for col in range(32):
            holes.append(make_cylinder(0.00145, 0.0010,
                [-0.205 + col * 0.0132, y + 0.0002, 0.316 + row * 0.0070],
                MAT_DARK, 12, (0, 1, 0)))
    add_group(scene, "Top_Front_Transverse_Vent_Relief_3x32", holes, MAT_DARK)


def build_scene(profile: str) -> trimesh.Scene:
    textures = {face: profile_texture(face, profile)
                for face in ("front", "rear", "left", "right", "top", "bottom")}
    sections = 30 if profile == "standard" else 20
    scene = trimesh.Scene(base_frame="Dell-R720-3.5inch_ROOT")
    scene.metadata.update({
        "manufacturer": "Dell",
        "product_id": "PowerEdge R720",
        "variant": "8LFF / 3.5-inch / 2U / no bezel",
        "configuration": "8 installed LFF carriers; 7 blanked PCIe positions; iDRAC7; serial; VGA; 2 USB2; quad RJ45 NDC; 2x750W AC PSU",
        "coordinate_convention": "+X device right from front; +Y up; +Z front",
        "units": "metres",
        "source_model_used": False,
        "bottom_mode": "GENERIC_BOTTOM_FALLBACK",
        "profile": profile,
    })
    add(scene, "Closed_Chassis_Core",
        make_box([BODY_W - 0.003, BODY_H - 0.003, BODY_D - 0.006],
                 [0, 0, -0.003], MAT_BODY))
    for face in ("front", "rear", "left", "right", "top", "bottom"):
        add(scene, f"Face_{face.title()}_Approved_Imagegen",
            textured_quad(face, textures[face]))
    add_front(scene, sections)
    add_rear(scene, sections, textures["rear"])
    add_sides(scene, sections)
    add_top(scene, sections)
    return scene


def add_unlit_and_metadata(path: Path, profile: str) -> None:
    gltf = GLTF2().load_binary(str(path))
    extensions = list(gltf.extensionsUsed or [])
    if "KHR_materials_unlit" not in extensions:
        extensions.append("KHR_materials_unlit")
    gltf.extensionsUsed = extensions
    for material in gltf.materials or []:
        if material.name and material.name.startswith("FACE_"):
            material.extensions = dict(material.extensions or {})
            material.extensions["KHR_materials_unlit"] = {}
        material.alphaMode = "OPAQUE"
        material.doubleSided = False
    gltf.asset.generator = "Trimesh exact-exterior construction + pygltflib face-unlit pass"
    gltf.asset.extras = {
        "manufacturer": "Dell",
        "product_id": "PowerEdge R720",
        "variant": "8LFF 3.5-inch no bezel",
        "profile": profile,
        "body_dimensions_mm": [444.0, 87.3, 702.0],
        "installed_bounds_mm": [482.4, 87.3, 741.0],
        "coordinate_convention": "+X device right from front; +Y up; +Z front",
        "source_model_used": False,
        "bottom_mode": "GENERIC_BOTTOM_FALLBACK",
        "visible_counts": {
            "LFF_carriers": 8,
            "front_rack_latches": 2,
            "PCIe_low_profile_blanks": 3,
            "PCIe_full_height_blanks": 4,
            "iDRAC7_RJ45": 1,
            "DB9_serial": 1,
            "rear_VGA": 1,
            "rear_USB2": 2,
            "network_adapter_RJ45": 4,
            "AC_PSU_750W": 2,
            "IEC_AC_inlets": 2,
            "PSU_visible_fans": 2,
        },
    }
    gltf.save_binary(str(path))


def export_profile(profile: str) -> Path:
    MODEL.mkdir(parents=True, exist_ok=True)
    scene = build_scene(profile)
    filename = "Dell-R720-3.5inch.glb" if profile == "standard" else "Dell-R720-3.5inch-web.glb"
    output = MODEL / filename
    output.write_bytes(scene.export(file_type="glb", include_normals=True))
    add_unlit_and_metadata(output, profile)
    return output


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--profile", choices=("standard", "web", "both"), default="both")
    args = parser.parse_args()
    profiles = ("standard", "web") if args.profile == "both" else (args.profile,)
    results = []
    for profile in profiles:
        output = export_profile(profile)
        results.append({"profile": profile, "path": str(output), "bytes": output.stat().st_size})
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
