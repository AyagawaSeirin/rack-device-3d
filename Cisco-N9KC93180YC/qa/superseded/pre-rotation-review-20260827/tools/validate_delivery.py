#!/usr/bin/env python3
"""Static GLB, texture, identity, non-mirror, and 40-load delivery audit."""

from __future__ import annotations

import csv
import hashlib
import io
import json
import struct
from datetime import datetime, timezone
from pathlib import Path

from PIL import Image, ImageChops, ImageOps, ImageStat

ROOT=Path(__file__).resolve().parents[1]
MODELS={
    "standard":ROOT/"models/Cisco-N9K-C93180YC-FX-standard.glb",
    "web":ROOT/"models/Cisco-N9K-C93180YC-FX-web.glb",
}
EXPECTED_HASHES={
    "standard":"0d6f8bbfd0993a33014b887ab6c4deabbb94b7a01c79abcecc9c57b04a3e740a",
    "web":"e15f5488d4c5eadfeebb00e2056fc49194fe755ff20524aa344d3bc44ab5ff7e",
}
EXPECTED_BYTES={"standard":9883884,"web":3492720}
EXPECTED_MTIME_NS={
    "standard":1787559291131000000,
    "web":1787559296689000000,
}
EXPECTED_LAST_MODIFIED_HTTP={
    "standard":"Mon, 24 Aug 2026 08:14:51 GMT",
    "web":"Mon, 24 Aug 2026 08:14:56 GMT",
}
FACES=("front","rear","left","right","top","bottom")


def sha(data:bytes)->str:
    return hashlib.sha256(data).hexdigest()


def parse_glb(path:Path):
    payload=path.read_bytes()
    magic,version,length=struct.unpack_from("<4sII",payload,0)
    assert magic==b"glTF" and version==2 and length==len(payload)
    offset,document,binary=12,None,b""
    while offset<len(payload):
        chunk_length,chunk_type=struct.unpack_from("<II",payload,offset)
        offset+=8
        chunk=payload[offset:offset+chunk_length]
        offset+=chunk_length
        if chunk_type==0x4E4F534A:
            document=json.loads(chunk.rstrip(b" \x00").decode())
        elif chunk_type==0x004E4942:
            binary=chunk
    assert document is not None
    return payload,document,binary


def view_bytes(document,binary,index):
    view=document["bufferViews"][index]
    start=view.get("byteOffset",0)
    return binary[start:start+view["byteLength"]]


def geometry_signature(document,binary):
    digest=hashlib.sha256()
    digest.update(json.dumps(document["nodes"],sort_keys=True,separators=(",",":")).encode())
    digest.update(json.dumps(document["meshes"],sort_keys=True,separators=(",",":")).encode())
    for accessor in document["accessors"]:
        definition={k:v for k,v in accessor.items() if k not in ("bufferView","byteOffset")}
        digest.update(json.dumps(definition,sort_keys=True,separators=(",",":")).encode())
        digest.update(view_bytes(document,binary,accessor["bufferView"]))
    return digest.hexdigest()


def embedded_images(document,binary):
    result={}
    for image_def in document["images"]:
        raw=view_bytes(document,binary,image_def["bufferView"])
        with Image.open(io.BytesIO(raw)) as image:
            result[image_def["name"]]={
                "bytes":len(raw),"sha256":sha(raw),"size_px":list(image.size),
                "mode":image.mode,"format":image.format,
            }
    return result


documents={}
geometry={}
model_reports={}
for flavor,path in MODELS.items():
    file_stat=path.stat()
    payload,document,binary=parse_glb(path)
    documents[flavor]=document
    geometry[flavor]=geometry_signature(document,binary)
    model_reports[flavor]={
        "path":str(path.relative_to(ROOT)),"bytes":len(payload),"sha256":sha(payload),
        "mtime_ns":file_stat.st_mtime_ns,
        "mtime_utc":datetime.fromtimestamp(file_stat.st_mtime,timezone.utc).isoformat(),
        "geometry_signature":geometry[flavor],"nodes":len(document["nodes"]),
        "meshes":len(document["meshes"]),"materials":len(document["materials"]),
        "images":len(document["images"]),"embedded_images":embedded_images(document,binary),
    }

names=[node.get("name","") for node in documents["standard"]["nodes"]]
feature_counts={
    "sfp28_recesses":sum(n.startswith("Front_SFP28_") and n.endswith("_Recess") for n in names),
    "qsfp28_recesses":sum(n.startswith("Front_QSFP28_") and n.endswith("_Recess") for n in names),
    "psu_modules":sum(n.startswith("Rear_NXA_PAC_500W_PI_") and n.endswith("_Module") for n in names),
    "iec_inlets":sum(n.startswith("Rear_NXA_PAC_500W_PI_") and n.endswith("_IEC_Inlet") for n in names),
    "pi_fan_trays":sum(n.startswith("Rear_NXA_FAN_30CFM_PI_Slot") and n.endswith("_Tray") for n in names),
    "pi_fan_latches":sum(n.startswith("Rear_NXA_FAN_30CFM_PI_Slot") and n.endswith("_BurgundyLatch") for n in names),
    "rear_fx_l1_l2_oob_console_ports":sum(n in ("Rear_IO_L1","Rear_IO_L2","Rear_IO_OOB","Rear_IO_Console") for n in names),
    "front_rack_openings":sum("_Ear_RackOpening_" in n for n in names),
    "rear_ear_nodes":sum(n.startswith("Rear_") and "Ear" in n for n in names),
    "independent_left_texture":sum(n=="Physical_Left_Independent_Texture" for n in names),
    "independent_right_texture":sum(n=="Physical_Right_Independent_Texture" for n in names),
}
expected_counts={
    "sfp28_recesses":48,"qsfp28_recesses":6,"psu_modules":2,"iec_inlets":2,
    "pi_fan_trays":4,"pi_fan_latches":4,"rear_fx_l1_l2_oob_console_ports":4,
    "front_rack_openings":6,"rear_ear_nodes":0,"independent_left_texture":1,
    "independent_right_texture":1,
}

standard_images=model_reports["standard"]["embedded_images"]
texture_identity={}
for face in FACES:
    raw=(ROOT/"views"/f"{face}.png").read_bytes()
    embedded=standard_images[f"FACE_{face.upper()}_SOURCE_LOCKED_Image"]
    texture_identity[face]={
        "view_sha256":sha(raw),"embedded_sha256":embedded["sha256"],
        "exact_byte_match":sha(raw)==embedded["sha256"],"size_px":embedded["size_px"],
    }

left=Image.open(ROOT/"views/left.png").convert("RGBA")
right=Image.open(ROOT/"views/right.png").convert("RGBA").resize(left.size,Image.Resampling.LANCZOS)
mirror_diff=ImageChops.difference(left,ImageOps.mirror(right))
mirror_mean=sum(ImageStat.Stat(mirror_diff).mean[:3])/3
non_mirror={
    "left_sha256":sha((ROOT/"views/left.png").read_bytes()),
    "right_sha256":sha((ROOT/"views/right.png").read_bytes()),
    "mirrored_rgb_mean_absolute_difference":round(mirror_mean,4),
    "pass":mirror_mean>4.0,
}

load_report=json.loads((ROOT/"qa/webgl-loads/load-events.json").read_text())
records=load_report["records"]
load_counts={
    "actual":len(records),
    "three":sum(r["viewer"]=="three" for r in records),
    "babylon":sum(r["viewer"]=="babylon" for r in records),
    "standard":sum(r["model"]=="standard" for r in records),
    "web":sum(r["model"]=="web" for r in records),
    "unique_urls":len({r["model_url"] for r in records}),
    "unique_screenshots":len({r["screenshot"] for r in records}),
    "hash_matches":sum(r["sha256"]==EXPECTED_HASHES[r["model"]] for r in records),
    "byte_matches":sum(r["proof_bytes"]==EXPECTED_BYTES[r["model"]] for r in records),
    "mtime_matches":sum(r["model_last_modified_http"]==EXPECTED_LAST_MODIFIED_HTTP[r["model"]] for r in records),
    "screenshots_exist":sum((ROOT/r["screenshot"]).is_file() for r in records),
}

with (ROOT/"qa/viewer-load-evidence.csv").open(newline="") as handle:
    load_csv_rows=list(csv.DictReader(handle))
viewer_load_csv_matches=len(load_csv_rows)==len(records)==40
if viewer_load_csv_matches:
    for record,row in zip(records,load_csv_rows):
        screenshot=ROOT/record["screenshot"]
        viewer_load_csv_matches=viewer_load_csv_matches and all((
            row["sequence"]==str(record["sequence"]),
            row["viewer"]==record["viewer"],
            row["model"]==record["model"],
            row["view"]==record["view"],
            row["sha256"]==record["sha256"],
            row["proof_bytes"]==str(record["proof_bytes"]),
            row["model_last_modified_http"]==record["model_last_modified_http"],
            row["screenshot"]==record["screenshot"],
            screenshot.is_file(),
            row["screenshot_sha256"]==sha(screenshot.read_bytes()) if screenshot.is_file() else False,
            row["status"]=="PASS",
        ))

views_audit=json.loads((ROOT/"qa/views-audit.json").read_text())
alpha_repair=json.loads((ROOT/"qa/rear-alpha-repair.json").read_text())
structural_audits={
    flavor:json.loads((ROOT/f"qa/glb-structural-{flavor}.json").read_text())
    for flavor in MODELS
}
final_report_text=(ROOT/"qa/final-report.md").read_text()
final_report_glb_metadata_exact=all(token in final_report_text for token in (
    EXPECTED_HASHES["standard"], EXPECTED_HASHES["web"],
    "9,883,884", "3,492,720",
    "2026-08-24T08:14:51.131000+00:00",
    "2026-08-24T08:14:56.689000+00:00",
    "40/40 PASS",
    "qa/webgl-loads/load-events.json",
    "qa/viewer-load-evidence.csv",
    "qa/webgl-loads/contact-sheets/all-40-hash-proven-loads.png",
))

all_materials=[m for d in documents.values() for m in d["materials"]]
asset_extras=documents["standard"]["asset"]["extras"]
checks={
    "model_hashes_exact":all(model_reports[k]["sha256"]==EXPECTED_HASHES[k] for k in MODELS),
    "model_bytes_exact":all(model_reports[k]["bytes"]==EXPECTED_BYTES[k] for k in MODELS),
    "model_mtimes_exact":all(model_reports[k]["mtime_ns"]==EXPECTED_MTIME_NS[k] for k in MODELS),
    "standard_web_geometry_identical":geometry["standard"]==geometry["web"],
    "self_contained_no_external_buffer_uri":all("uri" not in b for d in documents.values() for b in d["buffers"]),
    "all_materials_opaque":all(m.get("alphaMode","OPAQUE")=="OPAQUE" for m in all_materials),
    "all_materials_single_sided":all(not m.get("doubleSided",False) for m in all_materials),
    "six_embedded_images_each":all(len(d["images"])==6 for d in documents.values()),
    "standard_embeds_exact_six_views":all(x["exact_byte_match"] for x in texture_identity.values()),
    "feature_counts_exact":feature_counts==expected_counts,
    "left_right_not_mirrored":non_mirror["pass"],
    "exact_identity_metadata":asset_extras.get("pid")=="N9K-C93180YC-FX" and "NXA-FAN-30CFM-PI" in asset_extras.get("installed_configuration","") and "NXA-PAC-500W-PI" in asset_extras.get("installed_configuration",""),
    "official_body_dimensions_metadata":asset_extras.get("dimensions_mm")=={"overall_width":482.6,"body_width":439.0,"height":44.0,"depth":571.0},
    "forty_hash_proven_loads":load_counts=={
        "actual":40,"three":20,"babylon":20,"standard":20,"web":20,
        "unique_urls":40,"unique_screenshots":40,"hash_matches":40,
        "byte_matches":40,"mtime_matches":40,"screenshots_exist":40,
    },
    "load_report_pass":load_report.get("status")=="PASS" and load_report.get("fresh_transfer_proof_count")==40,
    "load_report_expected_glbs_exact":load_report.get("expected_hashes")==EXPECTED_HASHES and load_report.get("expected_bytes")==EXPECTED_BYTES and load_report.get("expected_last_modified_http")==EXPECTED_LAST_MODIFIED_HTTP,
    "viewer_load_csv_and_screenshot_hashes_exact":viewer_load_csv_matches,
    "standard_views_audit_zero_errors":views_audit.get("status")=="PASS" and views_audit.get("error_count")==0,
    "rear_alpha_only_repair_proven":alpha_repair.get("status")=="PASS" and alpha_repair.get("rgb_unchanged") is True and alpha_repair.get("changed_pixel_count")==336 and alpha_repair.get("remaining_non_opaque_core_pixels")==0,
    "glb_structural_audits_zero_errors":all(report.get("status")=="PASS" and report.get("error_count")==0 for report in structural_audits.values()),
    "final_report_glb_load_and_mtime_metadata_exact":final_report_glb_metadata_exact,
    "bottom_fallback_declared":"GENERIC_BOTTOM_FALLBACK" in (ROOT/"source/face-source-lock.csv").read_text(),
    "official_3d_negative_result_recorded":"NOT_FOUND" in (ROOT/"source/official-3d-search-log.md").read_text(),
}

status="PASS_WITH_BOTTOM_FALLBACK" if all(checks.values()) else "REWORK"
report={
    "status":status,"identity":"Cisco N9K-C93180YC-FX",
    "configuration":"2 x NXA-PAC-500W-PI AC; 4 x NXA-FAN-30CFM-PI; port-side intake",
    "models":model_reports,"geometry_parity":geometry,"feature_counts":feature_counts,
    "expected_feature_counts":expected_counts,"texture_identity":texture_identity,
    "left_right_non_mirror":non_mirror,"load_counts":load_counts,
    "views_audit":views_audit,"rear_alpha_repair":alpha_repair,
    "structural_audits":structural_audits,"checks":checks,
}
(ROOT/"qa/audit.json").write_text(json.dumps(report,indent=2)+"\n")
(ROOT/"qa/delivery-validation.json").write_text(json.dumps(report,indent=2)+"\n")
for flavor in MODELS:
    sub={"status":"PASS" if all(checks.values()) else "REWORK","model":model_reports[flavor],"checks":checks}
    (ROOT/f"qa/audit-{flavor}.json").write_text(json.dumps(sub,indent=2)+"\n")
print(json.dumps(report,indent=2))
raise SystemExit(0 if status=="PASS_WITH_BOTTOM_FALLBACK" else 1)
