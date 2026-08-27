# Rotation and exact-appearance re-review — Huawei FusionServer RH2288 V3 24-SFF

Final status: **PASS_WITH_BOTTOM_FALLBACK**  
Review date: 2026-08-27  
Delivery subject: Huawei FusionServer RH2288 V3, nameplate H22M-03, 2U, 24x2.5-inch carriers 00-23, no rear drives, official same-side vertically stacked dual AC PSU rear.

## Hash transition

| GLB | Pre-review SHA-256 | Final SHA-256 | Final bytes |
|---|---|---|---:|
| standard | `daa3ff261e7f7e40b9e3566ebff5430c8dafe78054bec673487cf9828a6e34ee` | `99784848fa3bc592b4273af59d79fc1d9e34586a92064f475693d980e32dd9ff` | 26,217,524 |
| web | `10e11be59a635642e8f3ec289e12766b1a028384ab73edc0060792ff2ae9d570` | `26e40115ac095319ddbd3903e0a6e576e1172d854740eb39da3a90985969cf41` | 10,099,756 |

The pre-review checkpoint is preserved under `qa/superseded/pre-rotation-review-20260827/`.

## Reproduction and root cause

The pre-review GLBs each contained **190** photographic-surface/geometry pairs separated by at most 0.25 mm. In addition, all six photo-derived faces were ordinary PBR materials. The same angles rendered dark gray in Three.js and near-white in Babylon.js, directly reproducing the reported sudden-gray/transparent-looking cross-viewer state.

Root causes: near-coplanar photographic skins/core/relief and double application of viewer-dependent PBR lighting to already lit product photographs. No alpha blend was present; the visual symptom was depth and lighting instability, not genuine product transparency.

## Repair

- Inset the watertight core and place all six photographic skins in a stable evidence-preserving layer, separated from relief.
- Mark only the six photo-derived face materials `KHR_materials_unlit`; structural relief remains ordinary PBR.
- Preserve `alphaMode=OPAQUE`, `[1,1,1,1]`, `doubleSided=false`, RGB embedded images, existing source-locked views and exact configuration.
- Standard/web have identical visible geometry signature `50edebfda4b4a58afed01c019e423e3db4033d621a0f0545cac16dc5f071a854`.

## Structural gates

- `audit_views.py`: PASS, 0 errors; warnings are silhouette anti-aliasing only, with no transparent core pixels.
- `audit_glb.py`: standard/web PASS, 0 errors and 0 warnings.
- Final bounds: 482.6 x 86.1 x 715.35 mm (447 x 708 x 86.1 mm body plus documented front/rear relief and mounting span).
- 453 nodes/meshes/primitives, 13 materials, six independent embedded RGB textures.
- Exact duplicate triangles: 0; near-coplanar photographic pairs <=0.25 mm: 190 -> 0; negative transforms: 0; material-alpha errors: 0.
- Closed core: watertight, winding-consistent, positive volume.

## Real-browser gates

| Viewer / GLB | 5-degree yaw frames | Continuous animation frames | Dark-checker pitch frames | Result |
|---|---:|---:|---:|---|
| Three / standard | 72 | 58 | 8 | PASS |
| Three / web | 72 | 57 | 8 | PASS |
| Babylon / standard | 72 | 23 | 8 | PASS |
| Babylon / web | 72 | 22 | 8 | PASS |

Both paths are real Chromium WebGL2. Final-hash HTTP evidence proves 40/40 static loads and four rotation loads. Final visual review shows no flicker, opacity jump, checkerboard leakage, face loss, mirroring, texture switch or sudden gray state; Three/Babylon photographic color is now stable.

## Exact appearance and source status

The 2026-08-27 live Huawei Product Visuals check still identifies `RH2288 V3 Rack Server`, exposes two raster images/ZIP and returns `threeUrl: null`; no exact public official 3D became available. The corrected official rear remains proven by Huawei Figure 4-6 and exact-model photography: two PSUs stacked at one side, no rear drives, two flexible-NIC ports and standard I/O. All 12 feature-inventory rows pass against 24 matched-camera sheets.

Only the underside lacks direct exact-model imagery after documented official, browser-assisted and third-party search. It remains the permitted conservative `GENERIC_BOTTOM_FALLBACK`, so the result is not ordinary PASS.

Evidence entry points:

- `after/browser-gate-summary.json`
- `after/rotation-stress-report.json`
- `after/http-final-hash-audit.json`
- `after/structural-extra-standard.json` and `after/structural-extra-web.json`
- `after/matched-camera/comparison-manifest.json`
- `after/feature-inventory-verification.json`
- `after/rotation/<viewer>/<variant>/rotation-manifest.json`
- `after/research/`

Warnings/residual risk: exact underside detail remains unavailable; the fallback is closed, plain, non-identifying and does not alter any verified silhouette.
