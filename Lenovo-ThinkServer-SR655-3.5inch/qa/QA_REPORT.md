# Final QA report

status: PASS

2026-08-27 rotation re-review: **PASS**. The authoritative current hashes are standard `2a8925f1eb08f5fe67df99cac62bcfdcb823bc60ef152d710ab0dec0df59bb97` and web `632af251f3d568340933e357eb425cf7d1e94b5727dc3400c8dc83b9031f3868`; both completed 40/40 final-hash static loads and four 72-frame rotation gates. See `qa/rotation-review-20260827/final-report.md`. Hashes and counts in the older body below describe the preserved pre-rotation checkpoint and are superseded by that report.

bottom_status: exact official-viewer underside; no fallback

## Identity gate

- Lenovo ThinkSystem SR655 original generation, types 7Y00/7Z01; SR655 V3 excluded.
- Physical front variant B5VK with AUR9 12x3.5-inch SAS/SATA backplane.
- Requested PCIe-rich rear: eight slots in 3+3+2 banks, no rear drives.
- Two installed 750W AC hot-swap PSUs, C14 inlets, orange handles.
- No security bezel; front VGA present; two-port OCP 3.0 present.

Identity status: VERIFIED. Remaining non-bottom evidence gaps: none.

## Six-view asset audit

`qa/views-audit.json` status: PASS, zero errors.

- Front 2600x467; ratio error 0.086%; 12 LFF carriers and both front latches complete.
- Rear 2400x467; ratio error 0.014%; 8 slots, two OCP ports and two 750W AC PSUs complete.
- Left/right 3000x339; ratio error 0.103%; distinct non-mirrored hole/label/boss patterns.
- Top/bottom 1512x2600; ratio error 0.023%; top latch/vent/service-label layout and exact plain bottom seams retained.
- Six warnings are only anti-aliased external silhouette pixels. Every face has 0% core alpha below 250 and 0% transparent core.
- Light and dark checkerboard reviews: `qa/comparisons/alpha-checker-light.png` and `qa/comparisons/alpha-checker-dark.png`.

## Model structure

Both final GLBs contain:

- 189 nodes, meshes and primitives;
- 16 materials, including six opaque sRGB photographic materials with `KHR_materials_unlit`;
- six embedded textures and no external buffers/resources;
- no negative/mirrored transforms;
- closed main chassis body plus separate visible geometry for carrier frames/handles/latches, PCIe slot covers/dividers, PSU bodies/fans/C14 inlets/orange handles/LEDs, rear ports, side bosses/screws/lips, top cover/stampings/latch/vent and bottom plate/seams;
- front latch top/bottom mechanical supports only; no rear-plane ear geometry. Thin corner projections visible in a straight rear render are the physically front-mounted supports, not invented rear ears.

This is not a six-texture box. The official InfinityRT model package was never imported or copied into the build.

## Standard GLB

Path: `model/Lenovo-ThinkServer-SR655-3.5inch.glb`

Bytes: 11,101,288

SHA-256: `bc4abc301d051b8396943855464c941993854cde23c4a6ad74f140a7545446f6`

Audit: PASS, zero errors/warnings.

Bounds: 481.99999 x 86.499996 x 764.85997 mm. Maximum deviation from the 482.0 x 86.5 x 764.7 target is 0.16 mm.

## Web GLB

Path: `model/Lenovo-ThinkServer-SR655-3.5inch-web.glb`

Bytes: 7,904,740

SHA-256: `a7d9015d1a7a564acac7cab1ce497a1d1b11ca6f7053febeebc1a535916dbd3f`

Audit: PASS, zero errors/warnings. Geometry, node/material counts, orientation and bounds match the standard asset; only embedded texture resolution/file size is reduced.

## Independent viewer validation

Viewer path 1: Three.js 0.180 GLTFLoader, neutral background, no tone mapping.

Viewer path 2: Babylon.js public loader, neutral background, no tone mapping.

Each viewer rendered front, rear, right, left, top, bottom, front-right and rear-right for both standard and web GLBs: 32 final actual-GLB renders total under `qa/renders/`.

Both engines agree on front/rear text direction, side orientation, opacity, PSU/OCP placement and all six face assignments. Front/rear viewer-parity mean absolute RGB differences are below 0.65/255. Standard-vs-web front/rear differences are below 1.07/255. Three-quarter engine differences are lighting/camera-engine diagnostics; feature counts and orientation agree.

## Source comparisons

Six orthographic comparison sheets and two authoritative official-viewer three-quarter sheets are under `qa/comparisons/`.

Diagnostic mean absolute RGB differences, 0-255 scale:

- front 3.41
- rear 7.95 (principally the thin front-support corner projections and added true geometry)
- right 1.21
- left 1.18
- top 2.87
- bottom 1.81
- front-right 9.17
- rear-right 8.95

The three-quarter pixel differences include camera/crop and the real top service label absent from Lenovo's simplified official viewer. Manual feature review passes: silhouettes, 12 carriers, 8 rear slots, two OCP ports, two 750W AC PSUs, top latch/vent, right warning label, left/right asymmetry and bottom seam pattern all map one-to-one to the inventory.

## Final decision

PASS. The bottom has exact official-model evidence, so `PASS_WITH_BOTTOM_FALLBACK` is not applicable.
