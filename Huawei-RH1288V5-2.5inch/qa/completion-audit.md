# Completion audit — Huawei RH1288V5/2.5-inch

Status: **PASS_WITH_BOTTOM_FALLBACK**

| Objective requirement | Authoritative current-state evidence | Result |
|---|---|---|
| Work is confined to this model and inherits prior research | All authored/build/QA files are under `Huawei-RH1288V5-2.5inch/`; `source/identity-manifest.md`, `source/evidence.md`, `source/face-source-lock.csv`, and `source/feature-inventory.csv` remain the controlling evidence | PASS |
| Exact delivery identity | `source/identity-manifest.md`: FusionServer Pro 1288H V5, 1U, 10×2.5-inch, 3-I/O, LOM/FlexIO unpopulated, dual same-type AC, status VERIFIED | PASS |
| Preserve brand and standardize to AC | `views/front.png` and the ear textures retain Huawei/HUAWEI and `1288H V5`; `qa/feature-audit.csv` verifies two IEC C14/AC PSU modules and no DC/HVDC face | PASS |
| Preserve optional official 3D but do not substitute it | `source/optional-3d/xfusion-1288hv5-viewer/` retains 49 public iV3D resources; every entry in `SHA256SUMS.txt` verifies; GLB extras and `model/build-report.json` record `official_iv3d_imported: false` | PASS |
| Re-key the bottom from the original generation | `qa/imagegen-raw/bottom.png` → `qa/imagegen-keyed/bottom-full.png` → `views/bottom.png`; the final core is fully opaque and keeps only the conservative base plate | PASS_WITH_BOTTOM_FALLBACK |
| Six canonical views and QA | `views/` contains front/rear/left/right/top/bottom; `qa/views-audit.json` is PASS with 0 errors; every opaque core has 0% transparent pixels | PASS |
| Newly constructed standard and web GLBs | `model/Huawei-RH1288V5-2.5inch.glb` and `model/Huawei-RH1288V5-2.5inch-web.glb`; both are self-contained newly generated files | PASS |
| Real visible exterior geometry | `qa/feature-audit.csv` checks all 32 inventory rows; 33 named GLB mesh groups cover ears/true holes, 10 carriers, rear panels/ports, dual PSUs, top relief and independent side relief | PASS |
| Correct dimensions, materials, transforms and packaging | `qa/glb-standard-audit.json` and `qa/glb-web-audit.json`: PASS, 0 errors, 0 warnings, exact 482.6×43×714 mm proportional bounds, 15 embedded OPAQUE materials/textures, no mirrored transforms | PASS |
| Same exterior in standard/web variants | `qa/embedded-assets-audit.json`: identical geometry hash `27ffad72d7f61e9640d21c5ac25eb2efa909c443d5618c4e8cc60738b8f7e06d`; `qa/render-consistency.json`: 40 render-pair checks PASS | PASS |
| Two independent WebGL viewers, six orthographic plus four oblique | `qa/webgl-load-audit.json`: Three.js r180 and Babylon.js 8.26.0 each loaded both GLBs, 40/40 required screenshots and 8 alpha-background screenshots, 0 loader/page errors; contact sheets under `qa/contact-sheets/` | PASS |
| Source/render comparisons | 12 comparison sheets under `qa/comparisons/`; `qa/comparison-matrix.csv` records feature review and diagnostic MAE, maximum 3.552878/255 | PASS_WITH_BOTTOM_FALLBACK |
| Delivery manifest and final QA | `delivery-manifest.json` hashes 92 deliverables with no verification failure; `qa/audit.json` and `qa/final-qa.md` record the final gate | PASS_WITH_BOTTOM_FALLBACK |

The bottom is the only controlled evidence exception. No non-bottom identity, configuration, face, geometry, viewer, audit, or packaging requirement remains unresolved.
