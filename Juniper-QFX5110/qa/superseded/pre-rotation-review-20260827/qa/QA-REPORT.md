# Juniper QFX5110 exact-exterior QA report

## Final status

`PASS_WITH_BOTTOM_FALLBACK`

The exact installed subject is verified as **Juniper QFX5110-48S-AFI**, fixed 1U chassis, 48 empty SFP/SFP+ cages plus four empty QSFP28 cages, five azure `AIR IN` AFI fan modules, two 650 W AC-AFI PSUs, and two short front rack ears. All non-bottom faces are evidence-backed. Exact underside imagery was unavailable after the required search escalation, so the sole allowed conservative bottom fallback is disclosed.

## Pre-build gates

- identity manifest: VERIFIED
- power: AC, explicitly frozen from the user's batch decision
- airflow: AFI / FRU-to-port, proven by screenshot fan color and official AFI AC rear
- fan/PSU state: five `QFX5110-48S-FANAFI` plus two `JPSU-650W-AC-AFI`
- port state: empty, no optics/cables
- rack hardware: two front-only ears with true holes; no rear-ear geometry and no full rails
- body dimensions: 440.944 × 43.688 × 520.192 mm
- installed GLB bounds: 482.600 × 43.848 × 551.992 mm; the 0.160 mm height delta is the two 0.08 mm anti-z-fighting photo-face offsets, while the closed chassis remains exactly 43.688 mm

## Face assets

| Face | Mode | Final pixels | Key feature result |
|---|---|---:|---|
| front | SOURCE_LOCKED_GENERATION | 4096×371 | 48 SFP/SFP+ in 2×24, 4 QSFP28 in 2×2, timing ports, dual vent bands, front ears |
| rear | SOURCE_LOCKED_GENERATION | 4096×406 | management panel, 5 blue AFI fans, 2 AC AFI PSUs, Juniper/QFX5110 branding |
| left | MULTI_REFERENCE_RECONSTRUCTION | 4096×344 | distinct left body panel/seams/slots; protrusions are separate geometry |
| right | MULTI_REFERENCE_RECONSTRUCTION | 4096×344 | distinct right body panel/seams/slots; not mirrored |
| top | MULTI_REFERENCE_RECONSTRUCTION | 2604×3072 | real gray cover, seam/screws, faint embossed Juniper mark |
| bottom | GENERIC_BOTTOM_FALLBACK | 2604×3072 | conservative plain opaque gray sheet; no unsupported detail |

Exactly six built-in `image_gen` calls were made, one per face. Each prompt and labeled input-role record is in `qa/imagegen-prompts/`. Flat magenta key backgrounds were removed with the installed imagegen helper; all six final files are RGBA with transparent external canvases. The automated view audit reports PASS, zero errors. Its six generic alpha warnings were visually resolved: inset core alpha below 250 is 0% on five faces and 0.00221% on the rear (anti-aliased edge only); checkerboard renders show no transparency through opaque chassis surfaces. Front-ear holes are genuine mesh openings.

## New geometry and GLBs

The model is newly constructed. No official or third-party mesh was used. Visible geometry includes the closed body, source-locked six face surfaces, separate perforated front ears, 48 SFP cage reliefs, four QSFP cage reliefs, timing connectors, rear management block, five independently projecting fan modules/handles, two independently projecting AC PSUs/handles/retainers, asymmetric side-slot relief, and top seams/fasteners.

### Standard GLB

- file: `model/Juniper-QFX5110.glb`
- size: 19,683,332 bytes
- SHA-256: `774c9a74d4cb2c9f831cba63acb685d0b22227724b3eb53cc45516ce9527d47b`
- structural audit: PASS, 0 errors, 0 warnings

### Web GLB

- file: `model/Juniper-QFX5110-web.glb`
- size: 7,335,712 bytes
- SHA-256: `bc26e58f3c7f2308fb596802abd0da43ff96b67dae81d686cd52beef6b4b8801`
- structural audit: PASS, 0 errors, 0 warnings

Both final GLBs contain 1 scene, 54 nodes, 54 meshes/primitives, 14 materials, and seven embedded RGB base-color images. All main face materials are `OPAQUE`, `doubleSided:false`, neutral factor `[1,1,1,1]`, with `KHR_materials_unlit` on the source-photo materials. No external buffers, missing UVs, negative/mirrored transforms, partial-alpha textures, or required unsupported extensions were found. Standard and web geometry/bounds are identical.

## Actual-GLB viewer validation

Two independent glTF engines loaded the exported files:

1. Three.js `GLTFLoader` — standard GLB
2. Babylon.js `SceneLoader` — web GLB

Each path captured front, rear, left, right, top, bottom, front-left, front-right, rear-left, and rear-right. The two engines agree on orientation, opacity, silhouette and installed component counts. Viewer-consistency comparison sheets are under `qa/comparisons/viewer-consistency/`; any small differences are lighting/antialiasing only.

Light and dark checkerboard renders confirm that checkerboard appears only outside the appliance and through the real ear holes. Close-ups confirm two large and one small hole per front ear, normal readable rear Juniper/QFX5110 branding, and no global alpha damage. A rear orthographic view can see the laterally extending **front** ears through line-of-sight; node inspection confirms there are no rear-ear nodes.

## Source comparisons and repair history

- six orthographic source/render/overlay/difference sheets: `qa/comparisons/orthographic/`
- authoritative shallow front-top, left-angle, right-angle and rear-top comparisons: `qa/comparisons/three-quarter/`
- two-engine consistency sheets: `qa/comparisons/viewer-consistency/`

Initial render inspection found two causal geometry issues: over-wide side-slot relief and flat-color rear modules obscuring the source-locked photo. Version 1 was preserved under `qa/work/repair-v1/`; version 2 was preserved under `qa/work/repair-v2/`. The final build narrows the slots and projects the locked real rear photograph onto the independent management/fan/PSU outer planes while retaining their depth. A final bounds repair moved top seam/fastener detail inside the official chassis-height envelope.

Feature review confirms exact counts and left-to-right groups: 48+4 front cages, one management group, fans 0–4, two AC-AFI PSUs, no DC terminal blocks, no AFO orange fans, no absent FRU, no rear ears, and no copied top-to-bottom texture.

## PDF and official-model notes

No PDF skill was installed. The required explicit fallback was completed: full text extraction with pypdf, relevant page rendering with PyMuPDF at 3×, and original-detail visual inspection of every used page. The evidence log lists pages and figures.

Current official searches plus Playwright inspection of the rendered Juniper product gallery found no public exact-PID official GLB/glTF/CAD/AR/3D viewer resource. `source/optional-3d/README.md` records the search. No authentication, access control, paywall or private API was bypassed.

## Bottom exception

Exact underside imagery remained unavailable after official, dynamic-browser, reseller, marketplace, auction, used-equipment, teardown, video, English, Japanese, Chinese, same-family and same-vendor searches. `bottom.png` is intentionally non-identifying: verified footprint/material only, with no logo, label, vents, holes, feet, rails, seams, fasteners or protrusions. This is the only reason the final status is `PASS_WITH_BOTTOM_FALLBACK` rather than ordinary `PASS`.
