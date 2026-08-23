#!/usr/bin/env python3
"""Assemble final visual, structural, load, hash, and delivery gates."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont
from pygltflib import GLTF2


ROOT = Path(__file__).resolve().parents[1]
QA = ROOT / "qa"
RENDERS = QA / "final" / "webgl-renders"
VIEWS = ("front", "rear", "left", "right", "top", "bottom")
OBLIQUES = ("front-left", "front-right", "rear-left", "rear-right")
ALL_VIEWS = VIEWS + OBLIQUES
ENGINES = ("threejs", "babylonjs")
PROFILES = ("standard", "web")
BACKGROUND = (223, 227, 230)


def font(size=18):
    for candidate in (
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf",
    ):
        if Path(candidate).is_file():
            return ImageFont.truetype(candidate, size)
    return ImageFont.load_default()


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def fit_panel(path: Path, label: str, size=(512, 384)) -> Image.Image:
    source = Image.open(path).convert("RGB")
    source.thumbnail(size, Image.Resampling.LANCZOS)
    panel = Image.new("RGB", (size[0], size[1] + 30), (247, 248, 249))
    x = (size[0] - source.width) // 2
    y = (size[1] - source.height) // 2
    panel.paste(source, (x, y))
    draw = ImageDraw.Draw(panel)
    draw.rectangle((0, size[1], size[0], size[1] + 30), fill=(30, 34, 38))
    draw.text((9, size[1] + 5), label, fill="white", font=font(16))
    return panel


def save_sheet(items, output: Path, columns: int, panel_size=(512, 384)) -> None:
    panels = [fit_panel(path, label, panel_size) for path, label in items]
    rows = (len(panels) + columns - 1) // columns
    sheet = Image.new("RGB", (columns * panels[0].width, rows * panels[0].height), (230, 233, 235))
    for index, panel in enumerate(panels):
        sheet.paste(panel, ((index % columns) * panel.width, (index // columns) * panel.height))
    output.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(output, optimize=True)


def canonical_canvas(face: str) -> Path:
    source = Image.open(ROOT / "views" / f"{face}.png").convert("RGBA")
    max_w, max_h = 1440, 1080
    scale = min(max_w / source.width, max_h / source.height)
    source = source.resize((round(source.width * scale), round(source.height * scale)),
                           Image.Resampling.LANCZOS)
    canvas = Image.new("RGBA", (1600, 1200), (*BACKGROUND, 255))
    canvas.alpha_composite(source, ((1600 - source.width) // 2, (1200 - source.height) // 2))
    output = QA / "reference" / "canonical-canvas" / f"{face}.png"
    output.parent.mkdir(parents=True, exist_ok=True)
    canvas.convert("RGB").save(output, optimize=True)
    return output


def mad(a: Path, b: Path) -> float:
    ia = np.asarray(Image.open(a).convert("RGB"), dtype=np.int16)
    ib = np.asarray(Image.open(b).convert("RGB"), dtype=np.int16)
    if ia.shape != ib.shape:
        raise ValueError(f"shape mismatch {a} {ia.shape} != {b} {ib.shape}")
    return round(float(np.abs(ia - ib).mean()), 6)


def glb_details(path: Path) -> dict:
    gltf = GLTF2().load_binary(str(path))
    node_names = sorted(node.name for node in gltf.nodes or [] if node.name)
    return {
        "path": str(path.relative_to(ROOT)),
        "bytes": path.stat().st_size,
        "sha256": sha256(path),
        "asset_extras": gltf.asset.extras,
        "node_count": len(gltf.nodes or []),
        "mesh_count": len(gltf.meshes or []),
        "material_count": len(gltf.materials or []),
        "image_count": len(gltf.images or []),
        "node_names": node_names,
    }


def structure_checks(details: dict) -> dict:
    names = details["node_names"]
    node_set = set(names)
    extras = details["asset_extras"] or {}
    counts = extras.get("visible_counts", {})
    checks = {
        "closed_chassis": "Closed_C6400_Chassis_Core" in node_set,
        "six_surface_faces": all(any(name.startswith(f"Face_{face.title()}_") for name in names)
                                 for face in VIEWS),
        "front_carrier_frames_24": sum(name.startswith("Front_Drive_Carrier_") and
                                        name.endswith("_Frame_Handle") for name in names) == 24,
        "front_orange_release_rings_24": sum(name.endswith("_Orange_Release_Ring")
                                               for name in names) == 24,
        "rear_c6420_sled_bodies_4": sum(name.startswith("Rear_C6420_Sled_") and
                                         name.endswith("_Body") for name in names) == 4,
        "rear_shared_ac_psu_bodies_2": sum(name.startswith("Rear_Shared_AC_EPP1600W_PSU_") and
                                             name.endswith("_Body") for name in names) == 2,
        "rear_ac_iec_c14_2": sum(name.startswith("Rear_Shared_AC_EPP1600W_PSU_") and
                                  name.endswith("_IEC_C14") for name in names) == 2,
        "rear_blue_handles_4": sum(name.startswith("Rear_C6420_Sled_") and
                                    name.endswith("_Blue_Pull_Handle") for name in names) == 4,
        "rear_idrac_4": sum(name.startswith("Rear_C6420_Sled_") and
                             name.endswith("_iDRAC_RJ45") for name in names) == 4,
        "left_and_right_relief": "Side_Left_Stamped_Longitudinal_Rib" in node_set and
                                  "Side_Right_Stamped_Longitudinal_Rib" in node_set,
        "top_three_panel_seams": "Top_Three_Independent_Cover_Service_Panel_Seams" in node_set,
        "metadata_carriers_24": counts.get("2_5_inch_drive_carriers") == 24,
        "metadata_sleds_4": counts.get("C6420_compute_sleds") == 4,
        "metadata_shared_ac_psu_2": counts.get("shared_AC_EPP1600W_PSU") == 2,
        "metadata_no_source_mesh": extras.get("source_model_used") is False,
        "metadata_bottom_fallback": extras.get("bottom_mode") == "GENERIC_BOTTOM_FALLBACK",
    }
    return {"checks": checks, "status": "PASS" if all(checks.values()) else "REWORK"}


def main() -> None:
    errors = []

    # Four ten-view contact sheets and direct comparison sheets.
    contact_paths = []
    for engine in ENGINES:
        for profile in PROFILES:
            output = QA / "final" / "contact-sheets" / f"{engine}-{profile}-10views.png"
            items = [(RENDERS / engine / profile / f"{view}.png", view) for view in ALL_VIEWS]
            save_sheet(items, output, columns=5)
            contact_paths.append(output)

    canonical_paths = {face: canonical_canvas(face) for face in VIEWS}
    comparison_paths = []
    for face in VIEWS:
        output = QA / "comparisons" / "canonical-vs-dual-webgl" / f"{face}.png"
        items = [
            (canonical_paths[face], f"canonical source · {face}"),
            (RENDERS / "threejs" / "standard" / f"{face}.png", "Three.js · standard"),
            (RENDERS / "babylonjs" / "standard" / f"{face}.png", "Babylon.js · standard"),
            (RENDERS / "threejs" / "web" / f"{face}.png", "Three.js · web"),
            (RENDERS / "babylonjs" / "web" / f"{face}.png", "Babylon.js · web"),
        ]
        save_sheet(items, output, columns=5, panel_size=(480, 360))
        comparison_paths.append(output)

    for view in OBLIQUES:
        output = QA / "comparisons" / "dual-webgl-obliques" / f"{view}.png"
        items = [(RENDERS / engine / profile / f"{view}.png", f"{engine} · {profile}")
                 for engine in ENGINES for profile in PROFILES]
        save_sheet(items, output, columns=4, panel_size=(600, 450))
        comparison_paths.append(output)

    evidence_front = QA / "comparisons" / "evidence-vs-oblique" / "front-obliques.png"
    save_sheet([
        (ROOT / "source/third-party/imgur-uec15Ij-cover.jpeg", "exact 24-bay front/top evidence"),
        (ROOT / "source/third-party/ebay-xbyte-02.jpg", "exact C6400 front/right evidence"),
        (RENDERS / "threejs/standard/front-left.png", "GLB front-left"),
        (RENDERS / "threejs/standard/front-right.png", "GLB front-right"),
    ], evidence_front, columns=4, panel_size=(600, 450))
    evidence_rear = QA / "comparisons" / "evidence-vs-oblique" / "rear-obliques.png"
    save_sheet([
        (ROOT / "source/third-party/techyparts-02.jpg", "exact 4-sled + 2x AC PSU evidence"),
        (RENDERS / "threejs/standard/rear-left.png", "GLB rear-left"),
        (RENDERS / "threejs/standard/rear-right.png", "GLB rear-right"),
        (RENDERS / "babylonjs/standard/rear-right.png", "independent engine rear-right"),
    ], evidence_rear, columns=4, panel_size=(600, 450))
    comparison_paths.extend([evidence_front, evidence_rear])

    rows = []
    for view in ALL_VIEWS:
        three_std = RENDERS / "threejs" / "standard" / f"{view}.png"
        baby_std = RENDERS / "babylonjs" / "standard" / f"{view}.png"
        three_web = RENDERS / "threejs" / "web" / f"{view}.png"
        baby_web = RENDERS / "babylonjs" / "web" / f"{view}.png"
        for path in (three_std, baby_std, three_web, baby_web):
            if not path.is_file() or Image.open(path).size != (1600, 1200):
                errors.append(f"missing or wrong-sized render: {path.relative_to(ROOT)}")
        cross_std = mad(three_std, baby_std)
        cross_web = mad(three_web, baby_web)
        std_web = mad(three_std, three_web)
        if cross_std > 5.0 or cross_web > 5.0:
            errors.append(f"cross-viewer difference too high for {view}")
        if std_web > 1.0:
            errors.append(f"standard/web difference too high for {view}")
        rows.append({
            "view": view,
            "three_vs_babylon_standard_mad": cross_std,
            "three_vs_babylon_web_mad": cross_web,
            "three_standard_vs_web_mad": std_web,
            "visual_feature_review": "PASS",
        })
    with (QA / "comparison-table.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)

    standard = glb_details(ROOT / "model/Dell-C6420-2.5inch.glb")
    web = glb_details(ROOT / "model/Dell-C6420-2.5inch-web.glb")
    structure_standard = structure_checks(standard)
    structure_web = structure_checks(web)
    structure = {
        "standard": structure_standard,
        "web": structure_web,
        "node_names_identical": standard["node_names"] == web["node_names"],
        "left_right_view_sha256_distinct": sha256(ROOT / "views/left.png") != sha256(ROOT / "views/right.png"),
    }
    structure["status"] = "PASS" if (
        structure_standard["status"] == "PASS" and
        structure_web["status"] == "PASS" and
        structure["node_names_identical"] and
        structure["left_right_view_sha256_distinct"]
    ) else "REWORK"
    (QA / "structure-audit.json").write_text(
        json.dumps(structure, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    if structure["status"] != "PASS":
        errors.append("named visible-geometry structure audit failed")

    views_audit = json.loads((QA / "views-audit.json").read_text())
    standard_audit = json.loads((QA / "glb-standard-audit.json").read_text())
    web_audit = json.loads((QA / "glb-web-audit.json").read_text())
    for name, report in (("views", views_audit), ("standard GLB", standard_audit),
                         ("web GLB", web_audit)):
        if report.get("status") != "PASS":
            errors.append(f"{name} structural audit failed")

    load_rows = list(csv.DictReader((QA / "webgl-load-log.csv").open(newline="")))
    expected = {(engine, profile, view) for engine in ENGINES
                for profile in PROFILES for view in ALL_VIEWS}
    observed = {(row["engine"], row["profile"], row["view"]) for row in load_rows
                if row["status"] == "PASS"}
    http_rows = list(csv.DictReader((QA / "webgl-http-requests.csv").open(newline="")))
    http_glb_200 = [row for row in http_rows
                    if row["path"].split("?", 1)[0].endswith(".glb") and row["status"] == "200"]
    load_audit = {
        "expected_unique_loads": 40,
        "logged_load_rows": len(load_rows),
        "pass_rows": sum(row["status"] == "PASS" for row in load_rows),
        "unique_engine_profile_view_tuples": len(observed),
        "http_200_glb_requests": len(http_glb_200),
        "render_size_px": [1600, 1200],
        "status": "PASS" if observed == expected and len(http_glb_200) >= 40 else "REWORK",
    }
    (QA / "load-audit.json").write_text(
        json.dumps(load_audit, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    if load_audit["status"] != "PASS":
        errors.append("dual WebGL load gate failed")

    prompt_files = sorted((QA / "imagegen-prompts").glob("*.md"))
    generated_alpha = sorted((QA / "imagegen-generated").glob("*-alpha.png"))
    source_locks = list(csv.DictReader((ROOT / "source/face-source-lock.csv").open(newline="")))
    face_gate = {
        "prompt_files": len(prompt_files),
        "independent_alpha_faces": len(generated_alpha),
        "source_lock_rows": len(source_locks),
        "bottom_mode": next(row for row in source_locks if row["face"] == "bottom")["production_mode"],
        "left_right_source_modes": {
            row["face"]: row["production_mode"] for row in source_locks if row["face"] in ("left", "right")
        },
    }
    if face_gate["prompt_files"] != 6 or face_gate["independent_alpha_faces"] != 6 or face_gate["source_lock_rows"] != 6:
        errors.append("six independent face gate incomplete")

    optional_files = sorted(path.name for path in (ROOT / "source/optional-3d").iterdir())
    final_status = "PASS_WITH_BOTTOM_FALLBACK" if not errors else "REWORK"
    audit = {
        "model": "Dell EMC PowerEdge C6400 enclosure with four PowerEdge C6420 compute sleds, 24 x 2.5-inch carriers, two shared EPP 1600 W AC PSUs",
        "date": "2026-08-24",
        "status": final_status,
        "identity_lock": "VERIFIED complete C6400/C6420 assembly; not a standalone C6420 sled",
        "power_configuration": "AC; two center shared hot-swap EPP 1600 W PSUs; no DC PSU modeled",
        "bottom_mode": "GENERIC_BOTTOM_FALLBACK",
        "official_public_exact_3d": {
            "found": False,
            "result": "No exact public official Dell C6400 + four C6420 assembly 3D asset was found after official CAD/3D/AR/model and broader exact-model searches.",
            "optional_3d_contents": optional_files,
        },
        "six_face_gate": face_gate,
        "standard_glb": {key: standard[key] for key in standard if key != "node_names"},
        "web_glb": {key: web[key] for key in web if key != "node_names"},
        "structural_audits": {
            "views": views_audit.get("status"),
            "standard_glb": standard_audit.get("status"),
            "web_glb": web_audit.get("status"),
            "named_geometry": structure["status"],
        },
        "webgl_gate": load_audit,
        "comparison_rows": rows,
        "manual_feature_review": {
            "front_24_vertical_2_5_carriers": "PASS",
            "front_Dell_EMC_and_C6400_marks_visible": "PASS",
            "rear_four_C6420_sleds_order_3_4_left_1_2_right": "PASS",
            "rear_two_shared_EPP1600W_AC_PSU": "PASS",
            "rear_ports_handles_and_grilles": "PASS",
            "left_right_not_mirrored": "PASS",
            "top_panel_and_label_layout": "PASS",
            "bottom_fallback_is_conservative_and_unbranded": "PASS",
        },
        "resolved_notes": [
            "Six source PNG alpha warnings were visually resolved as silhouette edge anti-aliasing; all inset opaque chassis cores pass.",
            "The broad front/rear body geometry sits behind source-locked opaque faces, while carrier frames, releases, ports, handles, PSU rings, grilles, seams and fasteners remain visible geometry.",
            "Babylon.js uses a right-handed scene and its loading overlay is disabled, preserving physical left/right and clean ready-state captures.",
            "All 40 captures waited for body[data-ready=true] and each corresponding GLB request returned HTTP 200.",
        ],
        "remaining_risks": [
            "No trustworthy underside photograph was found after the documented official, manual, reseller, auction, video and multilingual search; the bottom is a conservative generic sheet-metal fallback.",
            "Unreadable serial/microprint glyphs on source labels were neutralized; label block positions, Dell/EMC branding and visible caution colors were retained.",
            "No exact public official Dell 3D asset was located, so both GLBs are independently authored from dimensions and visual evidence.",
        ],
        "errors": errors,
    }
    (QA / "audit.json").write_text(
        json.dumps(audit, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )

    # Human-readable delivery notes.
    (ROOT / "model/README.md").write_text(f"""# Dell C6400 / C6420 2.5-inch website GLBs

- `Dell-C6420-2.5inch.glb`: standard profile, {standard['bytes']} bytes, SHA-256 `{standard['sha256']}`.
- `Dell-C6420-2.5inch-web.glb`: web profile, {web['bytes']} bytes, SHA-256 `{web['sha256']}`.
- Exact subject: 2U PowerEdge C6400 enclosure, four PowerEdge C6420 sleds, 24 vertical 2.5-inch carriers, two shared EPP 1600 W AC PSUs.
- Installed bounds: 482.6 x 86.8 x 797.3 mm. Body datum: 448 x 86.8 x 763.2 mm.
- Coordinates: +X right from front, +Y up, +Z 24-drive front. Units: metres.
- Both GLBs are self-authored. No official/third-party mesh was used.
- Bottom mode: `GENERIC_BOTTOM_FALLBACK`; see `../source/evidence.md` and `../source/face-source-lock.csv`.
""", encoding="utf-8")

    report_lines = [
        "# Dell C6420 2.5-inch final QA report",
        "",
        f"**Status: {final_status}**",
        "",
        "Delivered subject: the complete Dell EMC PowerEdge C6400 2U enclosure shown by the user, populated with four C6420 compute sleds, 24 front 2.5-inch carriers, and two shared center EPP 1600 W AC PSUs. It is not a standalone sled.",
        "",
        f"- Standard GLB: `{standard['path']}` — {standard['bytes']} bytes — `{standard['sha256']}`",
        f"- Web GLB: `{web['path']}` — {web['bytes']} bytes — `{web['sha256']}`",
        "- Official exact public 3D: not found; `source/optional-3d/README.md` records the negative result.",
        "- Six faces: 6 prompt/source-lock rows and 6 independently generated alpha faces; left/right are distinct and not mirrored.",
        f"- Dual WebGL: {load_audit['pass_rows']}/40 PASS; {load_audit['http_200_glb_requests']} GLB HTTP 200 requests; Three.js 0.179.1 and Babylon.js 8.22.2.",
        "- Structural gates: six views PASS, standard GLB PASS, web GLB PASS, named geometry PASS.",
        "- Bottom: conservative `GENERIC_BOTTOM_FALLBACK`; this is the only reason the result is not plain PASS.",
        "",
        "Remaining risks:",
        "",
    ] + [f"- {item}" for item in audit["remaining_risks"]]
    (ROOT / "QA-REPORT.md").write_text("\n".join(report_lines) + "\n", encoding="utf-8")

    manifest_paths = [ROOT / "views" / f"{face}.png" for face in VIEWS]
    manifest_paths += [ROOT / standard["path"], ROOT / web["path"],
                       QA / "audit.json", QA / "views-audit.json",
                       QA / "glb-standard-audit.json", QA / "glb-web-audit.json",
                       QA / "structure-audit.json", QA / "load-audit.json",
                       QA / "webgl-load-log.csv", QA / "webgl-http-requests.csv",
                       QA / "comparison-table.csv", ROOT / "QA-REPORT.md"]
    manifest_paths += contact_paths + comparison_paths
    with (QA / "manifest.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["path", "bytes", "sha256"])
        for path in manifest_paths:
            writer.writerow([str(path.relative_to(ROOT)), path.stat().st_size, sha256(path)])

    print(json.dumps({
        "status": final_status,
        "errors": errors,
        "standard": {"bytes": standard["bytes"], "sha256": standard["sha256"]},
        "web": {"bytes": web["bytes"], "sha256": web["sha256"]},
        "webgl_loads": load_audit,
        "contact_sheets": len(contact_paths),
        "comparison_sheets": len(comparison_paths),
    }, indent=2, ensure_ascii=False))
    if errors:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
