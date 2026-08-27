# Huawei FusionServer RH2288 V3 / H22M-03 24-SFF final QA

Final rotation-review status: **PASS_WITH_BOTTOM_FALLBACK** (2026-08-27)

Authoritative current hashes: standard `99784848fa3bc592b4273af59d79fc1d9e34586a92064f475693d980e32dd9ff`; web `26e40115ac095319ddbd3903e0a6e576e1172d854740eb39da3a90985969cf41`. Both completed 40/40 final-hash static loads and four 72-frame rotation gates with no flicker/gray/opacity failure. See `qa/rotation-review-20260827/final-report.md`; older hashes and counts below describe the superseded pre-rotation checkpoint.

## Delivered identity

- Huawei FusionServer RH2288 V3, official nameplate `H22M-03`, 2U.
- Exact 24 x 2.5-inch SFF front, modeled as 24 separately named carrier groups, indices 00-23.
- User-corrected official rear: no rear drives; two AC PSUs stacked vertically on the same rear side; two-port flexible NIC A1/A2; standard I/O, USB, Mgmt, LAN, VGA, serial and PCIe banks.
- Body dimensions: 447 x 708 x 86.1 mm; mounting-ear span: 482.6 mm.
- Real Huawei and RH2288 V3 identity marks are retained from exact evidence. No serial number or unsupported label was invented.

The original screenshot-rear conflict and all initial BLOCKED records remain unchanged under `qa/repair-before-user-correction/`. The corrected build never uses that mispaired rear as a generation or modeling source. The user-authorized VERIFIED rear transition is independently frozen under `repair-official-rear/`.

## Six face assets

`qa/audits/views.json` passes all six files with zero errors. Maximum physical-ratio error is 0.0555%; the inset chassis cores have 0% alpha below 250. The six warnings identify only anti-aliased/translucent pixels inside the outer content bounds and were visually checked as silhouette/key edges, not chassis holes.

All six final faces now have built-in ImageGen lineage. The repaired front is source-locked to the exact 24-SFF photograph and Huawei whitepaper Figure 4-4: exactly 24 carriers, one USB 2.0 and four Ethernet indicator groups on physical left, and diagnostic/health/UID/power/NMI/VGA controls on physical right. A 14-pixel extension of each feature-free top/bottom chassis rail restores the official silhouette without rescaling or repainting any carrier, ear, control, logo or text. The replaced photo-rectified front and its two prior GLBs/reports are preserved under `repair-imagegen-front/before/`. Left and right are byte-distinct, have separate evidence locks and were never mirrored. Prompt/input roles and accepted/rejected generations are recorded in `qa/imagegen-prompts/face-generation-log.md` and `repair-imagegen-front/README.md`.

## GLB structure

Both GLBs pass `audit_glb.py` with zero errors and zero warnings:

- `model/Huawei-RH2288V3-2.5inch.glb` — 26,207,588 bytes — SHA-256 `daa3ff261e7f7e40b9e3566ebff5430c8dafe78054bec673487cf9828a6e34ee`
- `model/Huawei-RH2288V3-2.5inch-web.glb` — 10,089,824 bytes — SHA-256 `10e11be59a635642e8f3ec289e12766b1a028384ab73edc0060792ff2ae9d570`

Each contains 453 nodes/meshes/primitives, 13 OPAQUE materials, six independent base-color textures, normals, a closed load-bearing shell and no mirrored nodes. Bounds are 482.600 x 86.300 x 715.350 mm; the 708 mm body plus modeled front/rear relief remains within the 3% structural tolerance. The additional eight geometry nodes encode the corrected asymmetric front controls.

`qa/audits/structure.json` independently verifies:

- carrier indices exactly 00-23;
- two AC PSU groups exactly 0-1;
- zero rear-drive geometry;
- two flexible-NIC port nodes;
- standard management I/O nodes;
- closed chassis node;
- independent left/right texture nodes and byte-distinct images;
- exactly one physical-left USB 2.0 node and exactly four physical-left Ethernet-indicator nodes;
- complete independent physical-right diagnostic/health/UID/power/NMI/VGA control group;
- zero mirror-named nodes.

## Browser and visual QA

Real Chromium loaded both the rebuilt standard and web GLBs in two independent engines:

- Three.js: six orthographic and four three-quarter views for standard and web;
- Babylon.js: the same ten views for standard and web;
- total post-repair capture set: 40 browser renders.

Atomic capture waited for the viewer ready state before every screenshot. Final review found no missing texture, loader overlay, CORS failure, duplicate top relief, duplicate side vent, orientation flip or open face. See `qa/browser-qa.md`, `repair-imagegen-front/renders/` and the post-repair contact sheets under `repair-imagegen-front/comparisons/`.

## Evidence fallback and official 3D

No public exact official CAD/GLB/glTF/OBJ/FBX/AR/interactive model was found; the search, formats and access limitations are recorded in `source/optional-3d/README.md`. No authentication or access control was bypassed.

Only the underside remains unsupported by direct photography. It uses the permitted `GENERIC_BOTTOM_FALLBACK`: a closed plain zinc-grey sheet at the verified footprint, with no invented screws, labels, vents or feet. There are no unresolved non-bottom evidence gaps.
