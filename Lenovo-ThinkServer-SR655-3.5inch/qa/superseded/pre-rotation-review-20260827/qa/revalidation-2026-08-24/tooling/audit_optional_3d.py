#!/usr/bin/env python3
import hashlib
import io
import json
import tarfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
OPTIONAL = ROOT / "source" / "optional-3d"
PUBLIC = OPTIONAL / "viewer-public"
ARCHIVE = OPTIONAL / "Lenovo-ThinkSystem-SR655-official-viewer-original-files.tar.gz"
OUTPUT = ROOT / "qa" / "revalidation-2026-08-24" / "optional-3d-audit.json"


def sha256_path(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


errors = []
current_files = sorted(path for path in PUBLIC.rglob("*") if path.is_file())
current_map = {path.relative_to(PUBLIC).as_posix(): path for path in current_files}

archive_map = {}
with tarfile.open(ARCHIVE, "r:gz") as archive:
    for member in archive.getmembers():
        if not member.isfile():
            continue
        name = member.name
        prefix = "viewer-public/"
        if not name.startswith(prefix):
            errors.append(f"unexpected archive file path: {name}")
            continue
        relative = name[len(prefix):]
        extracted = archive.extractfile(member)
        if extracted is None:
            errors.append(f"cannot read archive member: {name}")
            continue
        data = extracted.read()
        archive_map[relative] = {
            "size": len(data),
            "sha256": sha256_bytes(data),
        }

missing_from_archive = sorted(set(current_map) - set(archive_map))
missing_from_unpacked = sorted(set(archive_map) - set(current_map))
content_mismatches = []
for relative in sorted(set(current_map) & set(archive_map)):
    current_path = current_map[relative]
    current_size = current_path.stat().st_size
    current_sha = sha256_path(current_path)
    archived = archive_map[relative]
    if current_size != archived["size"] or current_sha != archived["sha256"]:
        content_mismatches.append({
            "path": relative,
            "unpacked_size": current_size,
            "archive_size": archived["size"],
            "unpacked_sha256": current_sha,
            "archive_sha256": archived["sha256"],
        })

if missing_from_archive:
    errors.append(f"{len(missing_from_archive)} unpacked files are absent from the archive")
if missing_from_unpacked:
    errors.append(f"{len(missing_from_unpacked)} archive files are absent from the unpacked directory")
if content_mismatches:
    errors.append(f"{len(content_mismatches)} archive/unpacked content mismatches")

manifest_path = PUBLIC / "MANIFEST.sha256"
manifest_lines = [line for line in manifest_path.read_text(encoding="utf-8").splitlines() if line.strip()]
manifest_errors = []
for line in manifest_lines:
    recorded, path_text = line.split("  ", 1)
    marker = "Lenovo-ThinkServer-SR655-3.5inch/source/optional-3d/viewer-public/"
    if marker not in path_text:
        manifest_errors.append(f"unexpected manifest path: {path_text}")
        continue
    relative = path_text.split(marker, 1)[1]
    path = PUBLIC / relative
    if not path.is_file():
        manifest_errors.append(f"manifest file missing: {relative}")
    elif sha256_path(path) != recorded:
        manifest_errors.append(f"manifest checksum mismatch: {relative}")
if manifest_errors:
    errors.append(f"{len(manifest_errors)} manifest verification errors")

model_extensions = {".glb", ".gltf", ".obj", ".fbx", ".step", ".stp"}
single_model_files = sorted(path.relative_to(PUBLIC).as_posix() for path in current_files if path.suffix.lower() in model_extensions)

report = {
    "status": "PASS" if not errors else "FAIL",
    "viewer_page": "https://lenovopress.lenovo.com/3dtours/sr655/",
    "accessed_at": "2026-08-24",
    "format": "InfinityRT public WebGL package (XML hierarchy, RAW/Draco mesh blocks, textures and runtime); no single GLB/GLTF download",
    "license_clue": "Lenovo copyright / All rights reserved; no public redistribution license located; retained for internal evidence/backup",
    "archive_path": str(ARCHIVE.relative_to(ROOT)),
    "archive_bytes": ARCHIVE.stat().st_size,
    "archive_sha256": sha256_path(ARCHIVE),
    "unpacked_file_count_including_manifest": len(current_files),
    "unpacked_bytes_including_manifest": sum(path.stat().st_size for path in current_files),
    "manifest_entry_count": len(manifest_lines),
    "manifest_excludes_itself": len(manifest_lines) == len(current_files) - 1 and "MANIFEST.sha256" not in {line.split("  ", 1)[1].rsplit("/", 1)[-1] for line in manifest_lines},
    "manifest_errors": manifest_errors,
    "archive_file_count": len(archive_map),
    "archive_matches_unpacked_byte_for_byte": not missing_from_archive and not missing_from_unpacked and not content_mismatches,
    "missing_from_archive": missing_from_archive,
    "missing_from_unpacked": missing_from_unpacked,
    "content_mismatches": content_mismatches,
    "single_file_3d_assets": single_model_files,
    "errors": errors,
}
OUTPUT.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
print(json.dumps(report, indent=2))
raise SystemExit(1 if errors else 0)
