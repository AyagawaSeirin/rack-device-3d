# Dell PowerEdge R630 10×2.5-inch final report

## Result

**PASS_WITH_BOTTOM_FALLBACK**

The delivered subject is a self-built Dell PowerEdge R630 13G 1U long chassis with the exact bezel-absent 10×2.5-inch SFF front, three-riser rear, quad-RJ45 NDC and two matching Dell EPP 1100W hot-plug AC PSUs. Genuine visible DELL, PowerEdge R630, Intel and EPP identity marks are retained. Physical left and right faces are independent and correctly oriented; neither is mirrored.

The only exception is the documented `GENERIC_BOTTOM_FALLBACK`. No usable exact underside image was found after official, interactive-gallery, reseller, marketplace, auction, video and English/Chinese searches. The fallback is deliberately conservative and contains no invented underside hardware. This is the only reason the result is not plain `PASS`.

## Deliverables

| Profile | File | Bytes | SHA-256 |
|---|---|---:|---|
| standard | `model/Dell-R630-2.5inch.glb` | 5,038,912 | `7645e39ef922b86174f68b3ee36e1d5b40a34d104d58d3e2d1881d3e27587194` |
| web | `model/Dell-R630-2.5inch-web.glb` | 1,366,752 | `c6e68df3a4a4def8ae9db1f3773d802b445614e84933f2de454c6bb230f87214` |

Both files are self-contained GLB 2.0 models. Each has 119 nodes/meshes, 14 materials and six unique embedded RGB JPEG face images. The standard and web geometry payload SHA-256 is identically `6da4a6044103554c65f96560721882fc3f0595c267c26a540d70e451cd6c0f9d`; only texture resolution/compression differs.

## Identity and dimensions

- Manufacturer/model: Dell PowerEdge R630, 13G, 1U.
- Front: exactly 10 SFF carriers, 2 rows × 5 columns; no bezel or optical bay; two front-only wing housings.
- Rear: three LP PCIe blanks; ID/iDRAC8/DB9/VGA/2×USB; four RJ45 NDC ports; two matching EPP 1100W AC PSUs with two C14 inlets, two orange releases, two circular fans/EPP hubs and two rigid molded pull handles; no fabric straps, DC supply, blank PSU or rear ears.
- World bounds: exactly `0.4824 × 0.0428 × 0.7521 m` (`482.4 × 42.8 × 752.1 mm`). Width includes the front mounting wings; body width is 434.0 mm.
- Both structural audits: `PASS`, zero errors, zero warnings, no mirrored nodes, no external buffers and six unique base-color images.

The final rear geometry was specifically repaired so PSU/port relief no longer hides the source-locked photographic C14, fan, EPP 1100W hub, orange-release and connector detail. Source/photo comparisons show these details remain visible in both orthographic and oblique views.

## Six-face lineage

| Face | Mode | Accepted output | Status |
|---|---|---|---|
| front | `SOURCE_LOCKED_GENERATION` | `views/front.png` | exact 10-bay; DELL/PowerEdge and Intel identity retained |
| rear | `SOURCE_LOCKED_GENERATION` | `views/rear.png` | target quad-RJ45 and dual EPP 1100W AC; straps removed, rigid handles retained |
| physical left | `MULTI_REFERENCE_RECONSTRUCTION` | `views/left.png` | independent source set; canonical front at image right |
| physical right | `MULTI_REFERENCE_RECONSTRUCTION` | `views/right.png` | independent source set; canonical front at image left; Intel wing retained |
| top | `SOURCE_LOCKED_GENERATION` | `views/top.png` | exact cover/vents/latch/service hatch/labels |
| bottom | `GENERIC_BOTTOM_FALLBACK` | `views/bottom.png` | conservative plate; no invented details |

`source/face-source-lock.csv` records primary real sources, source/output SHA-256 values, support sets and locked traits. `source/image-inspection.csv` records 44 original-detail raster inspections. `qa/imagegen-generation-record.json` records each face's independent input roles, accepted raw image, correction history, prompt and final hash. Rejected wrong-direction sides remain under `qa/reference/rejected/` and were not used.

The six-view audit is `PASS` with zero errors. Its five warnings are confined to anti-aliased silhouette edges/verified holes; the inset chassis core of every face is 0% transparent.

## Visible-feature gate

All 29 visible-feature inventory rows have a corresponding GLB mesh, photographic relief, or explicit absence and pass the two-viewer render review. Major silhouette/parallax items are separate geometry: closed body, two front-only wings, ten carrier bodies and handles/releases/LEDs, independent side channels/lips/studs, top service-hatch frame and latch, three rear riser assemblies, named rear I/O recesses, two separated PSU bodies/frames, C14 rims, orange releases, rigid handles and screws. Fine printed/perforated appearance is preserved through the locked photographs rather than invented vector graphics.

Detailed results: `qa/feature-gate.csv`.

## Real WebGL acceptance

Two independent WebGL paths loaded the actual final files in real Chromium:

1. Viewer A: `<model-viewer>` 4.3.1.
2. Viewer B: Three.js 0.185.1 with `GLTFLoader` and an independent orthographic camera/bounds implementation.

For each viewer, both GLBs were loaded in front, rear, left, right, top, bottom, front-left, front-right, rear-left and rear-right views:

- expected/actual loads: **40 / 40**
- `window.__QA__.loaded === true`: **40**
- screenshots generated after final GLB build: **40**
- screenshots at 1400×900: **40**
- page/console errors captured by final batch listeners: **0**
- runtime dimensions: exact `0.4824 × 0.0428 × 0.7521 m` in all 40 rows
- Viewer B runtime scene nodes: 120 including its loaded scene root

The complete matrix with per-row GLB hash, engine, view, dimensions, screenshot path and screenshot SHA-256 is `qa/reports/webgl-load-matrix.json`. The 40 screenshot hashes are in `qa/reports/render-sha256.txt`; per-viewer summaries are in `viewer-a-load-log.txt` and `viewer-b-load-log.txt`.

Standard/web matched-view mean absolute RGB differences are only 0.076–0.503 on a 0–255 scale; all 20 pairs therefore retain the same visible form/appearance while the web file is smaller.

## Visual comparisons

- Four final 10-view contact sheets: `qa/comparisons/contact-viewer-{a,b}-{standard,web}.jpg`.
- Six same-camera reference/render/50%-overlay/difference sheets: `qa/comparisons/orthographic-{front,rear,left,right,top,bottom}.png`.
- Six-sheet overview: `qa/comparisons/contact-orthographic-comparisons.jpg`.
- Exact real front/top/side three-quarter review: `qa/comparisons/three-quarter-front-side-review.jpg`.
- Target rear and PSU-source-role review: `qa/comparisons/rear-source-review.jpg`.

Final visual inspection found no top/body z-fighting, diagonal slabs/triangles, gaps, false rear ears, left/right mirroring, black-alpha holes, hidden service hatch, missing carrier, alternate NDC, missing/mixed PSU or standard/web silhouette drift.

## Official model outcome

No official public Dell GLB/glTF/CAD/STEP/AR model matching this exact installed configuration was found after exhaustive official-domain and general searches. `source/optional-3d/README.md` records the result. Therefore there is no official binary to preserve; no third-party model was substituted, and both delivered GLBs are self-built.

## Residual risk

1. The underside is a documented conservative fallback, not a photographed exact underside.
2. Fine factory/compliance microtext is preserved as photographic print character and is not guaranteed to be semantically readable at arbitrary zoom; identity-bearing DELL/PowerEdge R630, Intel and EPP marks are visibly retained.
3. This is an exact exterior/web visualization, not engineering CAD or an internal-service model.

Aggregate machine-readable result: `qa/audit.json`. No Git commit or push was performed.
