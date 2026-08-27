#!/usr/bin/env python3
"""Cross-variant geometry, embedded texture, feature, and 40-load delivery gate."""

from __future__ import annotations

import hashlib
import io
import json
import struct
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
MODELS = {
    "standard": ROOT / "models/Dell-PowerEdge-C6300-4xC6320-24SFF-standard.glb",
    "web": ROOT / "models/Dell-PowerEdge-C6300-4xC6320-24SFF-web.glb",
}
FACES = ("front", "rear", "left", "right", "top", "bottom")


def sha(data):
    return hashlib.sha256(data).hexdigest()


def parse_glb(path):
    payload = path.read_bytes()
    magic, version, length = struct.unpack_from("<4sII", payload, 0)
    assert magic == b"glTF" and version == 2 and length == len(payload)
    offset, document, binary = 12, None, b""
    while offset < len(payload):
        chunk_length, chunk_type = struct.unpack_from("<II", payload, offset)
        offset += 8
        chunk = payload[offset:offset + chunk_length]
        offset += chunk_length
        if chunk_type == 0x4E4F534A:
            document = json.loads(chunk.rstrip(b" \x00").decode())
        elif chunk_type == 0x004E4942:
            binary = chunk
    assert document is not None
    return payload, document, binary


def view_bytes(document, binary, index):
    view = document["bufferViews"][index]
    start = view.get("byteOffset", 0)
    return binary[start:start + view["byteLength"]]


def geometry_signature(document, binary):
    digest = hashlib.sha256()
    digest.update(json.dumps(document["nodes"], sort_keys=True, separators=(",", ":")).encode())
    digest.update(json.dumps(document["meshes"], sort_keys=True, separators=(",", ":")).encode())
    for accessor in document["accessors"]:
        definition = {key: value for key, value in accessor.items() if key not in ("bufferView", "byteOffset")}
        digest.update(json.dumps(definition, sort_keys=True, separators=(",", ":")).encode())
        digest.update(view_bytes(document, binary, accessor["bufferView"]))
    return digest.hexdigest()


def embedded_images(document, binary):
    result = {}
    for image_def in document["images"]:
        raw = view_bytes(document, binary, image_def["bufferView"])
        with Image.open(io.BytesIO(raw)) as image:
            result[image_def["name"]] = {
                "sha256": sha(raw),
                "bytes": len(raw),
                "size_px": list(image.size),
                "mode": image.mode,
                "format": image.format,
            }
    return result


reports = {}
documents = {}
geometry = {}
for flavor, path in MODELS.items():
    payload, document, binary = parse_glb(path)
    documents[flavor] = document
    geometry[flavor] = geometry_signature(document, binary)
    reports[flavor] = {
        "path": str(path.relative_to(ROOT)),
        "bytes": len(payload),
        "sha256": sha(payload),
        "geometry_signature": geometry[flavor],
        "node_count": len(document["nodes"]),
        "mesh_count": len(document["meshes"]),
        "material_count": len(document["materials"]),
        "image_count": len(document["images"]),
        "embedded_images": embedded_images(document, binary),
    }

standard_images = reports["standard"]["embedded_images"]
face_texture_identity = {}
for face in FACES:
    source = (ROOT / "views" / f"{face}.png").read_bytes()
    embedded = standard_images[f"FACE_{face.upper()}_SOURCE_LOCKED_Image"]
    face_texture_identity[face] = {
        "approved_sha256": sha(source),
        "embedded_sha256": embedded["sha256"],
        "exact_byte_match": sha(source) == embedded["sha256"],
        "embedded_size_px": embedded["size_px"],
    }

names = [node["name"] for node in documents["standard"]["nodes"]]
feature_counts = {
    "sff_carrier_bodies": len([name for name in names if name.startswith("SFF_Carrier_") and name.endswith("_Body")]),
    "c6320_node_pull_tabs": len([name for name in names if name.startswith("C6320_Node_") and name.endswith("_PullTab")]),
    "sfp_plus_ports": len([name for name in names if "_SFPplus_" in name]),
    "idrac_rj45_ports": len([name for name in names if name.endswith("_iDRAC_RJ45")]),
    "vga_ports": len([name for name in names if name.endswith("_VGA")]),
    "shared_1400w_ac_psu_faces": len([name for name in names if name.startswith("Shared_AC_PSU_1400W_") and name.endswith("_Face")]),
    "iec_ac_inlets": len([name for name in names if name.endswith("_IEC_AC_Inlet")]),
    "psu_fan_guards": len([name for name in names if name.endswith("_FanGuard")]),
    "front_large_rack_holes": len([name for name in names if name.endswith("_LargeRackHole")]),
    "front_ear_fasteners": len([name for name in names if "_Ear_Fastener_" in name]),
    "major_side_key_slots": len([name for name in names if "_MajorKeySlot_" in name]),
    "right_only_vertical_access_slots": len([name for name in names if name == "Physical_Right_VerticalAccessSlot"]),
    "right_only_upper_recesses": len([name for name in names if name.startswith("Physical_Right_UpperRecess_")]),
    "true_poweredge_c6320_label_planes": len([name for name in names if name.endswith("_True_POWEREDGE_C6320_Label")]),
    "front_true_dell_brand_planes": len([name for name in names if name == "Front_True_DELL_Brand"]),
}
expected_counts = {
    "sff_carrier_bodies": 24, "c6320_node_pull_tabs": 4, "sfp_plus_ports": 8,
    "idrac_rj45_ports": 4, "vga_ports": 4, "shared_1400w_ac_psu_faces": 2,
    "iec_ac_inlets": 2, "psu_fan_guards": 2, "front_large_rack_holes": 2,
    "front_ear_fasteners": 8,
    "major_side_key_slots": 6, "right_only_vertical_access_slots": 1,
    "right_only_upper_recesses": 2, "true_poweredge_c6320_label_planes": 4,
    "front_true_dell_brand_planes": 1,
}

load_report = json.loads((ROOT / "qa/webgl-loads/load-events.json").read_text())
load_gate = {
    "status": load_report["status"],
    "actual_loads": load_report["actual_loads"],
    "fresh_transfer_proof_count": load_report["fresh_transfer_proof_count"],
    "unique_model_urls": len({record["model_url"] for record in load_report["records"]}),
    "pass_records": len([record for record in load_report["records"] if record["status"] == "PASS"]),
    "three_loads": len([record for record in load_report["records"] if record["viewer"] == "three"]),
    "babylon_loads": len([record for record in load_report["records"] if record["viewer"] == "babylon"]),
    "standard_loads": len([record for record in load_report["records"] if record["model"] == "standard"]),
    "web_loads": len([record for record in load_report["records"] if record["model"] == "web"]),
}

audit_files = {
    "standard": ROOT / "qa/audit-standard.json",
    "web": ROOT / "qa/audit-web.json",
}
structural_audits = {}
for flavor, path in audit_files.items():
    audit = json.loads(path.read_text())
    structural_audits[flavor] = {
        "path": str(path.relative_to(ROOT)),
        "status": audit["status"],
        "error_count": audit["error_count"],
        "warning_count": audit["warning_count"],
        "warnings": audit["warnings"],
    }

web_audit = json.loads(audit_files["web"].read_text())
web_logo_image_audit = next(
    image for image in web_audit["images"]
    if image.get("name") == "TRUE_DELL_LOGO_Image"
)
web_logo_resolution_warning = {
    "image": web_logo_image_audit["name"],
    "size_px": web_logo_image_audit["size_px"],
    "warnings": web_logo_image_audit["warnings"],
    "classification": "BENIGN_WEB_OPTIMIZATION_WARNING",
    "rationale": (
        "The 512 px web logo remains clear at the target website camera distance; "
        "the standard GLB retains the 1024 px logo. Identity, geometry, opacity, "
        "and both-viewer real-load gates are unaffected."
    ),
}

checks = {
    "standard_web_geometry_identical": geometry["standard"] == geometry["web"],
    "all_six_standard_face_textures_exact_byte_matches": all(item["exact_byte_match"] for item in face_texture_identity.values()),
    "feature_counts_exact": feature_counts == expected_counts,
    "all_materials_opaque": all(material.get("alphaMode", "OPAQUE") == "OPAQUE" for material in documents["standard"]["materials"] + documents["web"]["materials"]),
    "no_external_buffer_uri": all("uri" not in buffer for document in documents.values() for buffer in document["buffers"]),
    "forty_real_loads_complete": load_gate == {
        "status": "PASS", "actual_loads": 40, "fresh_transfer_proof_count": 40,
        "unique_model_urls": 40, "pass_records": 40, "three_loads": 20,
        "babylon_loads": 20, "standard_loads": 20, "web_loads": 20,
    },
    "official_3d_negative_result_recorded": (ROOT / "source/optional-3d/README.md").is_file(),
    "bottom_fallback_declared": "GENERIC_BOTTOM_FALLBACK" in (ROOT / "source/face-source-lock.csv").read_text(),
    "structural_audits_pass_without_errors": all(
        item["status"] == "PASS" and item["error_count"] == 0
        for item in structural_audits.values()
    ),
    "only_expected_web_logo_resolution_warning": (
        structural_audits["standard"]["warning_count"] == 0
        and structural_audits["web"]["warning_count"] == 1
        and structural_audits["web"]["warnings"] == ["long edge 512 px is below 1024 px"]
        and web_logo_image_audit["size_px"] == [512, 512]
        and web_logo_image_audit["warnings"] == ["long edge 512 px is below 1024 px"]
    ),
}

report = {
    "status": "PASS_WITH_BOTTOM_FALLBACK" if all(checks.values()) else "REWORK",
    "models": reports,
    "face_texture_identity": face_texture_identity,
    "geometry_parity": geometry,
    "feature_counts": feature_counts,
    "expected_feature_counts": expected_counts,
    "load_gate": load_gate,
    "structural_audits": structural_audits,
    "web_logo_resolution_warning": web_logo_resolution_warning,
    "checks": checks,
}
path = ROOT / "qa/delivery-validation.json"
path.write_text(json.dumps(report, indent=2) + "\n")
print(json.dumps(report, indent=2))
raise SystemExit(0 if report["status"] == "PASS_WITH_BOTTOM_FALLBACK" else 1)
