#!/usr/bin/env python3
"""Create a checksum-backed inspection ledger for every retained raster source."""

from __future__ import annotations

import csv
import hashlib
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "source"
OUT = SOURCE / "image-inspection-log.csv"


def classify(relative: str) -> tuple[str, str, str, str, str, str, str]:
    name = Path(relative).name.lower()
    if "user-configuration-lock" in name:
        return ("user-provided screenshot", "R7515 3.5-inch row lock", "front+rear row", "Original screenshot visually inspected at original detail; row 10 identifies Dell R7515/3.5-inch and excludes adjacent R7525/SFF rows.", "binding configuration lock", "accepted", "user screenshot")
    if "user-row10-lock" in name:
        return ("user-provided screenshot crop", "R7515 3.5-inch row lock", "front+rear elevation thumbnails", "Exact row-10 crop; 12 LFF exposed carriers, no bezel, no-rear-drive rear, four expansion positions and twin PSUs visible.", "binding configuration lock", "accepted", "user screenshot")
    if "user-row10-front" in name:
        return ("user-provided screenshot crop", "R7515 12 LFF", "front", "Upscaled discovery crop; low native resolution but exact carrier/control-wing silhouette and count are visible.", "supporting configuration lock", "accepted supporting", "user screenshot")
    if "user-row10-rear" in name:
        return ("user-provided screenshot crop", "R7515 no-rear-drive rear", "rear", "Upscaled discovery crop; low native resolution but no rear drives, port/riser arrangement and twin PSUs are visible.", "supporting configuration lock", "accepted supporting", "user screenshot")
    if "official-front-12lff" in name:
        return ("Dell official color figure", "R7515 12 x 3.5-inch", "front", "Straight official front figure; exact 3x4 carrier matrix and left/right control wings; callout numbers are outside the product and are not final-texture content.", "binding geometry/layout", "accepted", "official render")
    if "official-rear-no-rear-drives" in name:
        return ("Dell official color figure", "R7515 no rear drives", "rear", "Straight official rear figure; exact Riser 1B slots 2/3, slots 4/5, system I/O/LOM and dual PSU layout.", "binding geometry/layout", "accepted", "official render")
    if "official-rear-two-drives" in name:
        return ("Dell official color figure", "R7515 rear 2 x 3.5-inch", "rear rejected variant", "Exact R7515 but incompatible rear-drive cage/riser option; retained only to prevent accidental mixing.", "negative configuration reference", "rejected target variant", "official render")
    if "official-system-dimensions" in name:
        return ("Dell official technical diagram", "R7515", "top/side dimension envelope", "Official Xa/Xb/Y/Za/Zb/Zc diagram; proves proportions and depth inclusion, not surface detail.", "binding dimensions; bottom fallback envelope", "accepted", "technical diagram")
    if relative.startswith("pdf-pages/"):
        page = name.rsplit("-p", 1)[-1].split(".")[0]
        if "technical-guide" in name:
            note = "Rendered Dell Technical Guide page visually inspected in the other-PDF contact sheet; relevant chassis figure/text used only where it matches the locked variant."
        elif "technical-specifications" in name:
            note = "Rendered Dell Technical Specifications page visually inspected; proves dimensions, AC PSU options, six-fan requirement, risers, drive and port specifications."
        elif "spec-sheet" in name:
            note = "Rendered Dell R7515 spec-sheet page visually inspected; identity and port-count corroboration only."
        else:
            note = "Rendered Dell Installation and Service Manual page visually inspected in original/high detail and in manual contact sheets; exact-model component/cover/side evidence or rejected-variant context recorded by page."
        return ("Dell official PDF page render", "PowerEdge R7515", f"document page {page}", note, "supporting official evidence", "accepted with figure-level variant filtering", "official document render")
    if name.startswith("serverlama-r7515-front-diagonal"):
        return ("reseller real photograph", "R7515 12 LFF", "front/top three-quarter", "Exact 12-LFF no-bezel device; direct real top-cover material, label deck, latch, vent and carrier relief evidence.", "binding top/front geometry and photographic style", "accepted", "real photograph")
    if name.startswith("serverlama-r7515-front.jpg"):
        return ("reseller real photograph", "R7515 12 LFF", "front", "Exact straight 12-LFF no-bezel front on white; all carrier and control details visible without annotations.", "PRIMARY front identity/style", "accepted", "real photograph")
    if name.startswith("serverlama-r7515-back-diagonal"):
        return ("reseller real photograph", "R7515 no rear drives; dual 750W AC", "rear/top/right three-quarter", "Exact locked rear option and top/side relief; no seller modifications or cables.", "binding top/right/rear geometry", "accepted", "real photograph")
    if name.startswith("serverlama-r7515-back.jpg"):
        return ("reseller real photograph", "R7515 no rear drives; dual EPP 750W AC", "rear", "Exact straight rear matching row-10 layout; serial/VGA/USB/iDRAC/Gb/OCP, four PCIe positions and twin AC PSUs visible.", "PRIMARY rear identity/style", "accepted", "real photograph")
    if name.startswith("serversstorages-r7515-588"):
        return ("reseller real photograph", "R7515 common 2U chassis; optional bezel/1100W PSU", "front-right three-quarter", "Exact R7515 common side/top chassis; optional bezel and PSU wattage are excluded from target front/rear.", "PRIMARY right-side geometry/style", "accepted for right/top only", "real photograph")
    if name.startswith("serversstorages-r7515-591"):
        return ("reseller real photograph", "R7515 common 2U chassis; 1100W PSU", "rear-left three-quarter", "Exact opposite side wall and common top/chassis; 1100W hub label does not override locked 750W rear.", "binding left-side geometry", "accepted for left/side only", "real photograph")
    if name.startswith("serversstorages-r7515-view"):
        return ("reseller real photograph", "R7515 common 2U chassis", "left side orthographic", "Direct straight side view; front at screen-right/rear PSU handles at screen-left; exact independent holes, seams and stamped rail channel.", "PRIMARY left-side identity/style", "accepted", "real photograph")
    if name.startswith("serversstorages-r7515-589"):
        return ("reseller real photograph", "R7515 no-rear-drive; dual 1100W AC", "rear", "Exact R7515 rear arrangement but alternate PSU watt label and slightly different optional LOM population; used for geometry only.", "supporting rear geometry", "accepted supporting", "real photograph")
    if name.startswith("serversstorages-r7515-590"):
        return ("reseller real photograph", "R7515 common chassis with optional bezel", "front-left three-quarter", "Exact model and common chassis, but optional bezel is incompatible with target; side/top only.", "supporting opposite-side/top geometry", "accepted for side/top only", "real photograph")
    if "ecs-r7515-12bay" in name:
        return ("reseller product photograph", "R7515 12 LFF", "front", "Straight exact 12-LFF no-bezel front; white canvas; corroborates primary front.", "supporting front", "accepted supporting", "real photograph")
    if "ecs-r7515-rear-4pcie" in name:
        return ("reseller copy of Dell diagram", "R7515 no rear drives", "rear", "Annotated no-rear-drive rear diagram; layout proof only, annotations excluded.", "supporting rear geometry", "accepted supporting", "technical diagram")
    if "rear-drivebay" in name or name == "ecs-r7515-rear.jpg":
        return ("reseller product image", "R7515 rear-drive option", "rear rejected variant", "Exact model but incompatible rear drive cage; retained only as negative reference.", "negative configuration reference", "rejected target variant", "real photograph/diagram")
    if "ecs-r7515-internal-drivecage" in name:
        return ("reseller technical image", "R7515 rear-drive configuration", "interior/top rejected assembly", "Rear-drive cage option; used only to distinguish and reject it from target.", "negative assembly reference", "rejected target variant", "official/reseller render")
    if "ecs-r7515-internal-pcie" in name:
        return ("reseller technical image", "R7515 no-rear-drive common chassis", "interior/top", "Exact internal no-rear-drive riser layout and six-fan bank; external top material not established by this image.", "supporting assembly geometry", "accepted supporting", "official/reseller render")
    if "ecs-r7515-main" in name:
        return ("reseller product image", "R7515 optional bezel", "front three-quarter rejected bezel", "Optional honeycomb bezel incompatible with locked open front; common top/side silhouette only.", "negative bezel reference; top support", "rejected for front", "real photograph")
    if name.startswith("itc-front-bezel"):
        return ("review video frame", "R7515 optional bezel", "front", "Exact model but optional bezel plus watermark; bezel excluded, common materials/logo reference only.", "negative bezel/material support", "rejected for front", "real photograph")
    if name.startswith("itc-status-leds"):
        return ("review video frame", "R7515", "front left control close-up", "Exact five status icons; external annotation and watermark excluded.", "binding component close-up", "accepted supporting", "real photograph")
    if name.startswith("itc-front-control"):
        return ("review video frame", "R7515", "front right control close-up", "Exact power/USB/iDRAC-direct/VGA/control geometry; overlay and watermark excluded.", "binding component close-up", "accepted supporting", "real photograph")
    if name.startswith("itc-rear-ports"):
        return ("review video frame", "R7515 no rear drives", "rear close-up", "Exact serial/VGA/USB/iDRAC/Gb/riser/vent close-up; overlays and watermark excluded.", "binding rear component close-up", "accepted supporting", "real photograph")
    if name.startswith("itc-dual-psu"):
        return ("review video frame", "R7515 dual AC PSU", "rear PSU close-up", "Exact stacked PSU fan/inlet/latch construction; 1100W overlay/label is alternate wattage and does not override locked 750W hubs.", "binding PSU geometry/material", "accepted supporting", "real photograph")
    if "youtube-playback-error" in name:
        return ("browser screenshot", "R7515 video access attempt", "error screen", "Public YouTube player returned a playback error; no device evidence present.", "search-exhaustion record", "rejected as evidence", "browser screenshot")
    if name.startswith("itc-"):
        return ("review video frame", "R7515", "interior/component", "Exact-model real frame visually inspected; annotations/watermark and internal-only content are not final exterior texture.", "supporting assembly/material", "accepted supporting", "real photograph")
    return ("retained raster", "R7515 source set", "unclassified", "Visually inspected during source review; not selected as a binding primary face source.", "supporting or rejection record", "not primary", "unknown")


def main() -> None:
    paths = sorted(
        path for path in SOURCE.rglob("*")
        if path.is_file() and path.suffix.lower() in {".png", ".jpg", ".jpeg", ".webp"}
    )
    fields = [
        "path", "sha256", "pixel_width", "pixel_height", "inspected_at",
        "source_class", "claimed_model_configuration", "face_or_angle",
        "image_inspection_notes", "imagegen_input_role", "acceptance",
        "visual_origin",
    ]
    with OUT.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for path in paths:
            relative = path.relative_to(SOURCE).as_posix()
            with Image.open(path) as image:
                width, height = image.size
            source_class, config, face, notes, role, acceptance, origin = classify(relative)
            writer.writerow({
                "path": f"source/{relative}",
                "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                "pixel_width": width,
                "pixel_height": height,
                "inspected_at": "2026-08-23 original/high detail",
                "source_class": source_class,
                "claimed_model_configuration": config,
                "face_or_angle": face,
                "image_inspection_notes": notes,
                "imagegen_input_role": role,
                "acceptance": acceptance,
                "visual_origin": origin,
            })
    print(f"wrote {len(paths)} rows to {OUT}")


if __name__ == "__main__":
    main()
