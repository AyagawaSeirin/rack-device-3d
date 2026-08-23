# Final QA report — Huawei FusionServer RH2288 V3 / H22M-03 12×3.5-inch LFF

## Result

**PASS_WITH_BOTTOM_FALLBACK**

The standard and web GLBs complete the frozen H22M-03 configuration: 12 LFF carriers in a 3×4 front, no rear disks, SM211 two-port flexible NIC, standard management/VGA/serial/USB group, blank PCIe/riser areas and two identical AC PSUs vertically stacked on one rear side. Huawei and `RH2288 V3` front markings remain visible. `FusionServer` is retained in asset metadata and evidence records without inventing an exterior wordmark.

The only fallback is the underside. Exact-model underside evidence remained unavailable after the documented official, dynamic-gallery, PDF, reseller, marketplace, used-equipment, video and Chinese/English searches. The delivered bottom is intentionally plain, opaque and non-identifying.

## Deliverables

- Standard GLB: `model/Huawei-RH2288V3-3.5inch.glb`
- Web GLB: `model/Huawei-RH2288V3-3.5inch-web.glb`
- Reproducible builder: `model/build_model.py`
- Six approved transparent views: `views/front.png`, `rear.png`, `left.png`, `right.png`, `top.png`, `bottom.png`
- Identity/source records: `source/identity-manifest.md`, `face-source-lock.csv`, `feature-inventory.csv`, `evidence.md`
- Structural and browser audits: `qa/audits/`
- Two independent WebGL viewers: `qa/viewers/three.html`, `qa/viewers/babylon.html`
- Forty final screenshots: `qa/renders/`
- Orthographic comparisons and contact sheets: `qa/comparisons/`
- Comparison table: `qa/COMPARISON-TABLE.md`
- Asset manifest: `qa/asset-manifest.json`

## Model audit

| Item | Standard | Web |
|---|---:|---:|
| File size | 21,086,136 bytes | 10,019,496 bytes |
| Scene / nodes / meshes / primitives | 1 / 220 / 220 / 220 | 1 / 220 / 220 / 220 |
| Materials / textures / embedded images | 14 / 6 / 6 | 14 / 6 / 6 |
| World bounds (m) | 0.482600 × 0.086420 × 0.756520 | identical |
| Mirrored nodes | 0 | 0 |
| External buffers | 0 | 0 |
| GLB structural audit | PASS, 0 errors, 0 warnings | PASS, 0 errors, 0 warnings |

The 447 × 86.1 × 748 mm published chassis body remains the authored body. Overall depth grows only through verified front-carrier and rear PSU cord-loop relief. Six source-photographic face materials are RGB, opaque, sRGB base color and `KHR_materials_unlit`, stabilizing color across viewers.

`qa/audits/texture-lineage.json` directly extracts the embedded images from both binary GLBs. All twelve decoded standard/web face images are pixel-identical to the current approved `views/` assets after the builder's documented alpha removal and web resize; no old or rejected image is packaged.

## Configuration structure audit

- Twelve carrier indices `00`–`11`, exactly three rows × four columns.
- Separate front-only ear parts; no rear-ear nodes.
- Zero rear-drive nodes.
- Exactly two SM211 GE RJ45 nodes.
- Two vertically stacked AC PSU groups with fan and cord-loop geometry.
- Two USB 3.0, Mgmt RJ45, VGA, DB9 and UID nodes.
- Blank I/O module 2, onboard slot 4/5 and I/O module 1 groups.
- Independent, byte-distinct left and right textures; no mirror-named or negative-transform nodes.
- Source-locked top-latch relief and conservative generic bottom.

Result: `qa/audits/structure.json` = **PASS** for both GLBs.

## View and alpha audit

`qa/audits/views.json` = **PASS** with zero errors. Maximum physical-ratio error is 0.1015%. The six automated warnings are expected silhouette anti-aliasing/open-edge notices; original-detail inspection confirms no core chassis transparency, black-port deletion or interior leak. The GLB audit confirms all six embedded textures are RGB with 0% transparent and semi-transparent pixels and all materials use `alphaMode: OPAQUE`.

## WebGL acceptance

Real Chromium loaded both GLBs through two independent glTF renderers:

- Three.js: standard + web × front, rear, left, right, top, bottom, front-left, front-right, rear-left, rear-right.
- Babylon.js: the same 20-view matrix.

All 40 screenshots are present, non-empty and 1200×800. The maximum standard-versus-web normalized RMSE is 0.00967004 (0.967004%), below the 0.015 acceptance threshold. Both engines agree on face orientation, opacity, the 12-LFF count, no-rear-disk topology, stacked-PSU side and visible branding; expected PBR lighting differences remain only on untextured mechanical edges.

Result: `qa/audits/browser.json` = **PASS**.

## Source comparison and repairs closed

- Front: replaced duplicated procedural green/latch overlays with twelve same-source textured relief parts. The final straight view retains exactly one photographed release/status strip per carrier.
- Rear: replaced flat color blocks with seven non-overlapping same-source relief regions. The exact SM211, port labels, PCIe blanks, fans and PSU layout remain photographic, while module depth and cord loops stay geometric.
- Top: corrected the 180° UV orientation and replaced the synthetic latch block with same-source relief.
- Rear-ear symptom: removed rear-facing control geometry; final rear contains no rear-ear part.
- Material consistency: applied `KHR_materials_unlit` only to six photo-derived face materials, eliminating the viewer-dependent dark underside without flattening mechanical edge materials.

The final front/rear/top comparison sheets show one-to-one feature correspondence. Perspective contact sheets show a closed chassis, no visible empty interior, distinct sides, carrier/PSU relief and the correct front/rear relationship.

## Optional official 3D result

Huawei's exact product-gallery entry was recorded, but its API returns `threeUrl: null`; no downloadable official GLB/glTF/CAD model was available. The two official 1280×720 images remain evidence only. The official rear image is a different legal rear-disk/four-port option and was never used as the target rear configuration.
