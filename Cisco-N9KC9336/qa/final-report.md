# Cisco N9K-C9336C-FX2 final asset report

Final status: **PASS_WITH_BOTTOM_FALLBACK**  
Completed: 2026-08-24 (Asia/Singapore)

## Accepted identity and installed configuration

The user screenshot contains only the shorthand `N9KC9336`. The chassis identity was not taken from a user-supplied full product name: the screenshot's 36-port front (18 vertical two-port cages) and rear `PSU + 3 fan trays + management cluster + PSU` sequence were compared feature-by-feature with Cisco's exact official figures and hardware guide, resolving the chassis to `N9K-C9336C-FX2`.

The installed configuration was subsequently locked explicitly to:

- 2 × `NXA-PAC-1100W-PI2` 1100-W AC PSU
- 3 × `NXA-FAN-65CFM-PI` fan tray
- port-side intake, with burgundy/red PI latches and handles
- 36 empty QSFP28 ports in 18 vertical two-port cages
- no rack ears installed

`source/identity-manifest.md` is `VERIFIED`. The exact-config public BOM and inspected real rear photograph independently support the module set. Cisco/Nexus/model branding is retained from exact-model photographed pixels; it was not replaced with a generic mark.

## Six-face production and source locks

All six directions were produced in separate built-in image-generation calls using the face-specific source locks in `source/face-source-lock.csv` and the recorded prompts in `qa/imagegen-prompts/`. Front, rear, left, right, top and bottom each have their own raw output and de-keyed intermediate. The front required one additional rejected retry; the rejected output remains under `qa/rejected/imagegen/` and does not participate in delivery.

Face outcome:

| Face | Mode | Binding outcome |
|---|---|---|
| Front | `SOURCE_LOCKED_GENERATION` | Exact 36-port C9336C-FX2 face; photographed Cisco/Nexus/model strip restored with source pixels |
| Rear | `SOURCE_LOCKED_GENERATION` | 2 × PI2 AC PSU, 3 × 65CFM PI fan, exact management order and burgundy PI hardware |
| Physical left | `MULTI_REFERENCE_RECONSTRUCTION` | 12 mounting slots in two zones, one caution label, no grounding pad |
| Physical right | `MULTI_REFERENCE_RECONSTRUCTION` | Independent 12-slot pattern and right-only two-hole grounding pad; never mirrored |
| Top | `MULTI_REFERENCE_RECONSTRUCTION` | Port-side ventilation band, cover fasteners and exact-photo label character |
| Bottom | `GENERIC_BOTTOM_FALLBACK` | Plain closed silver underside only; no unsupported holes, labels, feet or vents |

`qa/views-audit.json` reports `PASS`, 0 errors and 0 warnings. All faces meet physical aspect ratios, minimum resolution and opaque-core checks. The left and right PNG SHA-256 values differ (`a5896c…a157` versus `1d174f…6db7`), and the rendered views visibly preserve their non-mirrored feature differences.

## Self-built GLBs

Both GLBs are original self-built assets. Neither is derived from, nor replaced by, an official or third-party 3D model.

| Attribute | Standard | Web |
|---|---:|---:|
| File | `models/Cisco-N9K-C9336C-FX2-standard.glb` | `models/Cisco-N9K-C9336C-FX2-web.glb` |
| Bytes | 25,463,576 | 1,282,004 |
| MiB | 24.284 | 1.223 |
| SHA-256 | `80dc0f2030145a0b2320c2d4fbc76a5144d1af62ceb0ad0be91974d6b3043c66` | `18f0cb525689dfea1df6dd5ee4c18a1ffa34b0ff0d95df97f980b32beb5a4d1b` |
| Embedded face images | 6 full-resolution PNG | 6 long-edge-2048 JPEG |
| World bounds | 439 × 44 × 623 mm | 439 × 44 × 623 mm |
| Nodes / rendered mesh nodes | 655 / 654 | 655 / 654 |
| Unique meshes / materials | 18 / 15 | 18 / 15 |
| Mirrored nodes / external buffers | 0 / 0 | 0 / 0 |
| Structural audit | PASS, 0 errors, 0 warnings | PASS, 0 errors, 0 warnings |

The web asset is 94.9653% smaller while retaining identical geometry, node names, materials, dimensions and visible configuration. `qa/comparison/standard-vs-web-keyviews.png` shows the matched standard/web front, rear and oblique views.

Visible geometry is not a six-texture box. It includes 18 independent front cage frames with 36 lower port recess surfaces and latch relief; lower ventilation relief and controls; two independent AC PSU assemblies with IEC inlets, latches and protruding handles; three independent fan trays with grille relief, paired burgundy latches and protruding black handles; the RJ-45/console/SFP/USB/LED management cluster; two six-slot bracket zones on each physical side; a right-only grounding pad; and top intake perforation relief. The bottom intentionally has no inferred geometry.

The deterministic GLB audits are:

- `qa/standard-glb-audit.json`: `PASS`, 0 errors, 0 warnings
- `qa/web-glb-audit.json`: `PASS`, 0 errors, 0 warnings
- exact world bounds in both: 439 × 44 × 623 mm
- six embedded source-lock face images, opaque materials, valid normals/UVs/accessor bounds, no negative-determinant transform and no external buffer

## Two-engine WebGL gate: 40 actual loads

Two independent WebGL implementations loaded the current final hashes:

- Three.js r180: 20 loads
- Babylon.js 9.22.0: 20 loads

Each engine loaded each GLB in ten separate page navigations: front, rear, left, right, top, bottom, front-left, front-right, rear-left and rear-right. This is 2 engines × 2 GLBs × 10 views = **40 actual GLB loads**. Every URL used a unique gate token, every record reports WebGL2 and the full decoded body size, and every load generated its own screenshot.

Results:

- required / actual: 40 / 40
- current-hash matches: 40 / 40
- full-body transfer proofs: 40 / 40
- exact bounds matches: 40 / 40
- visual screenshots: 40
- rendered mesh nodes per load: 654
- load duration range: 286–1,197 ms
- total model bytes transferred: 534,923,600 bytes (510.143 MiB)

Evidence is preserved in `qa/webgl-loads/load-events.json`, `qa/viewer-load-evidence.csv`, and the 40 PNGs below `qa/webgl-loads/`. Visual contact sheets are:

- `qa/comparison/three-standard-10views.png`
- `qa/comparison/babylon-web-10views.png`
- `qa/comparison/standard-vs-web-keyviews.png`

Manual image audit of those renders confirms 36 front port recesses, the exact rear PSU/fan/management order, burgundy PI hardware, independent physical sides, the top port-side vent band, and the deliberately plain fallback bottom.

## Official public 3D search

No exact-PID public official 3D model was found after searching Cisco exact-model support/product/document surfaces and public indexing for `3D`, `CAD`, `GLB`, `glTF`, `OBJ`, `FBX`, `STEP` and `STP`. Cisco exposes a Visio stencil, but it is 2D and was not treated as an official 3D asset. `source/optional-3d/` therefore contains only `SEARCH-LOG.md`; there is no exact official file size or hash to report.

An official viewer package for the wrong `N9K-C9336PQ` identity exists only under `qa/rejected/wrong-identity-9336PQ/`. All PQ files, including the former official texture PNG set, are quarantined there and do not participate in active source locks, face textures, GLBs or QA renders. No active `source/`, `qa/`, `views/` or `models/` asset has a PQ filename.

## Residual risks and acceptance rationale

The sole status downgrade is the underside. No exact C9336C-FX2 underside image was found after the documented official, PDF, reseller, marketplace, used-equipment, video and multilingual search. The skill-defined conservative fallback is therefore used: a plain silver closed sheet with the verified silhouette and no invented model detail.

Exterior relief placement is scaled from authoritative dimensions and inspected photographs rather than manufacturing CAD. This is a web-ready exact-appearance exterior replica, not engineering CAD and not an internal-component model. Fine label legibility is naturally reduced in the web texture and at whole-device zoom, although the real Cisco/Nexus identity, exact module metadata, source evidence and full-resolution standard texture remain preserved.

All other gates pass. Final disposition: **PASS_WITH_BOTTOM_FALLBACK**.

Browser runtime caches, Python bytecode and the three pre-gate smoke screenshots were removed from the project tree after the formal evidence was captured. They were moved to the recoverable temporary quarantine `/tmp/n9kc9336-runtime-cleanup-20260824-1542/`; the 40 formal load screenshots and all final evidence remain in the model directory. No `BATCH-STATUS.md` change, git commit or push was performed.
