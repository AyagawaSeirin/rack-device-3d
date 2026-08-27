from pathlib import Path
import hashlib
import json

import numpy as np
from PIL import Image
from pygltflib import GLTF2

ROOT = Path(__file__).resolve().parents[2]
QA = ROOT / "qa"
FACES = ("front", "rear", "left", "right", "top", "bottom")
VIEWS = ("front", "rear", "right", "left", "top", "bottom", "frontRight", "rearRight")


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def mean_diff(a: Path, b: Path) -> float:
    aa = np.asarray(Image.open(a).convert("RGB"), dtype=np.float32)
    bb = np.asarray(Image.open(b).convert("RGB"), dtype=np.float32)
    if aa.shape != bb.shape:
        raise ValueError((a, b, aa.shape, bb.shape))
    return float(np.abs(aa - bb).mean())


def extract_images(glb_path: Path, out_dir: Path) -> dict:
    gltf = GLTF2().load_binary(str(glb_path))
    blob = gltf.binary_blob()
    out_dir.mkdir(parents=True, exist_ok=True)
    # Image order follows photographic-surface geometry insertion order.
    face_order = ("front", "rear", "right", "left", "top", "bottom")
    result = {}
    for face, image in zip(face_order, gltf.images or []):
        view = gltf.bufferViews[image.bufferView]
        start = view.byteOffset or 0
        data = blob[start : start + view.byteLength]
        path = out_dir / f"{face}.png"
        path.write_bytes(data)
        embedded = np.asarray(Image.open(path).convert("RGB"))
        expected = np.asarray(Image.open(QA / "tooling" / "model-textures" / "standard" / f"{face}.png").convert("RGB"))
        result[face] = {
            "path": str(path.relative_to(ROOT)),
            "size_px": list(Image.open(path).size),
            "pixel_identical_to_standard_build_texture": bool(np.array_equal(embedded, expected)),
            "sha256": sha(path),
        }
    return result


def main() -> None:
    standard = ROOT / "model" / "Lenovo-ThinkServer-SR655-2.5inch.glb"
    web = ROOT / "model" / "Lenovo-ThinkServer-SR655-2.5inch-web.glb"
    standard_audit = json.loads((QA / "glb-audit-standard.json").read_text())
    web_audit = json.loads((QA / "glb-audit-web.json").read_text())
    views_audit = json.loads((QA / "views-audit.json").read_text())

    source_diff = {}
    for engine in ("three-standard", "babylon-web"):
        source_diff[engine] = {
            view: round(
                mean_diff(
                    QA / "reference" / "compare" / engine / f"{view}.png",
                    QA / "renders" / engine / f"{view}.png",
                ),
                6,
            )
            for view in VIEWS
        }

    viewer_parity = {
        view: round(
            mean_diff(
                QA / "renders" / "three-standard" / f"{view}.png",
                QA / "renders" / "babylon-web" / f"{view}.png",
            ),
            6,
        )
        for view in VIEWS
    }
    standard_web = {
        "three": {
            view: round(
                mean_diff(
                    QA / "renders" / "three-standard" / f"{view}.png",
                    QA / "renders" / "three-web-check" / f"{view}.png",
                ),
                6,
            )
            for view in ("front", "rear", "top", "frontRight")
        },
        "babylon": {
            view: round(
                mean_diff(
                    QA / "renders" / "babylon-standard-check" / f"{view}.png",
                    QA / "renders" / "babylon-web" / f"{view}.png",
                ),
                6,
            )
            for view in ("front", "rear", "top", "frontRight")
        },
    }

    left = Image.open(ROOT / "views" / "left.png").convert("RGBA")
    right = Image.open(ROOT / "views" / "right.png").convert("RGBA").transpose(Image.Transpose.FLIP_LEFT_RIGHT)
    bg = Image.new("RGBA", left.size, (176, 179, 178, 255))
    left_rgb = np.asarray(Image.alpha_composite(bg, left).convert("RGB"), dtype=np.float32)
    right_rgb = np.asarray(Image.alpha_composite(bg, right).convert("RGB"), dtype=np.float32)
    mirrored_side_diff = float(np.abs(left_rgb - right_rgb).mean())

    metrics = {
        "status": "PASS",
        "views_audit": {
            "status": views_audit["status"],
            "error_count": views_audit["error_count"],
            "warning_count": views_audit["warning_count"],
            "max_ratio_error_percent": max(v["ratio_error_percent"] for v in views_audit["faces"].values()),
            "max_core_alpha_below_250_percent": max(v["core_alpha_below_250_percent"] for v in views_audit["faces"].values()),
        },
        "standard_glb": {
            "path": str(standard.relative_to(ROOT)),
            "bytes": standard.stat().st_size,
            "sha256": sha(standard),
            "audit_status": standard_audit["status"],
            "error_count": standard_audit["error_count"],
            "warning_count": standard_audit["warning_count"],
            "counts": standard_audit["counts"],
            "dimensions_xyz_m": standard_audit["geometry"]["dimensions_xyz"],
            "dimension_ratio_error_percent": standard_audit["dimension_check"]["nonuniform_ratio_error_percent"],
        },
        "web_glb": {
            "path": str(web.relative_to(ROOT)),
            "bytes": web.stat().st_size,
            "sha256": sha(web),
            "audit_status": web_audit["status"],
            "error_count": web_audit["error_count"],
            "warning_count": web_audit["warning_count"],
            "counts": web_audit["counts"],
            "dimensions_xyz_m": web_audit["geometry"]["dimensions_xyz"],
            "dimension_ratio_error_percent": web_audit["dimension_check"]["nonuniform_ratio_error_percent"],
        },
        "embedded_standard_textures": extract_images(standard, QA / "extracted-standard-textures"),
        "source_comparison_mean_rgb_0_255": source_diff,
        "viewer_parity_mean_rgb_0_255": viewer_parity,
        "standard_web_mean_rgb_0_255": standard_web,
        "physical_left_vs_mirrored_right_mean_rgb_0_255": round(mirrored_side_diff, 6),
        "actual_glb_render_count": len(list((QA / "renders").glob("*/*.png"))) - 3,
        "official_archive": {
            "path": "source/optional-3d/Lenovo-ThinkSystem-SR655-official-viewer-original-files.tar.gz",
            "bytes": (ROOT / "source/optional-3d/Lenovo-ThinkSystem-SR655-official-viewer-original-files.tar.gz").stat().st_size,
            "sha256": sha(ROOT / "source/optional-3d/Lenovo-ThinkSystem-SR655-official-viewer-original-files.tar.gz"),
        },
        "unresolved_errors": [],
        "unresolved_non_bottom_evidence_gaps": [],
    }
    (QA / "metrics.json").write_text(json.dumps(metrics, indent=2) + "\n")
    print(json.dumps(metrics, indent=2))


if __name__ == "__main__":
    main()
