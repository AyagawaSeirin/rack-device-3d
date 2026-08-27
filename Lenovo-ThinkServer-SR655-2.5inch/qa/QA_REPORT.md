# Lenovo ThinkSystem SR655 24x2.5 final QA report

Status: PASS

2026-08-27 rotation re-review: **PASS**. Authoritative current hashes: standard `b34a0af03dcd28de63131f9e18494ac17cd4f960c18e0726c51d81da0ab2c677`; web `b2fd3bfbd4457318066a52bad42563d61f30fb7bf08d79a5a3a80512b4952011`. The rear elevation was corrected by byte-identical reuse of the validated physical-pair rear, and both GLBs completed 40/40 final-hash loads plus four 72-frame rotation gates. See `qa/rotation-review-20260827/final-report.md`. Older hashes/counts below are superseded.

Bottom status: exact official-viewer underside; no fallback.

## Identity

The delivered subject is the original-generation Lenovo ThinkSystem SR655, machine types 7Y00/7Z01, not SR655 V3. The physical front is the B5VJ 24x2.5-inch chassis with twenty-four visible carrier fronts in positions 0-23. The rear is PCIe-rich: eight covers in 3+3+2 banks, no rear drives, two-port OCP, management/VGA/USB/serial I/O, and two installed 750W hot-swap AC PSUs.

The user screenshot's ThinkServer wording is retained as a source-label discrepancy; official documentation names the product ThinkSystem SR655. Hidden media/protocol are not asserted because the documented 24-bay SAS/SATA, NVMe and mixed backplanes share the same requested carrier-level exterior.

Identity status: VERIFIED. Remaining non-bottom evidence gaps: none.

## Six generated view assets

Exactly six built-in imagegen calls were used, one per face. Front, rear and top use SOURCE_LOCKED_GENERATION; physical left, physical right and bottom use MULTI_REFERENCE_RECONSTRUCTION. The bottom has exact official viewer evidence and is not a generic fallback.

The final views audit is PASS with zero errors. Maximum physical-ratio error is 0.1029%. Every face has 0% core alpha below 250 and 0% transparent core. The six warnings are anti-aliased exterior silhouette pixels only; light and dark checkerboard inspection shows no opening through black ports, vents or chassis surfaces.

Left and right were generated in separate calls and were never mirrored or copied. The right side has the verified yellow warning label and its own boss/hole pattern; the left has no yellow label and a different pattern. The final physical-left versus mirrored-right mean RGB difference is 27.999523/255.

Unit-specific generated QR, serial and unsupported protocol microtext was blurred/deidentified. Legitimate ThinkSystem and SR655 branding, positions 0-23, real I/O, red accents and the verified 750W AC labels were retained.

## Newly constructed geometry

The official InfinityRT mesh was not imported or copied. Both new GLBs contain 261 nodes/meshes/primitives and 17 materials. Visible geometry includes:

- a closed outward-facing chassis body;
- separate front latch support assemblies;
- twenty-four independently framed SFF carrier recesses, handles and red accents;
- eight PCIe cover assemblies and rear dividers;
- two AC PSU bodies with fan rings, C14 inlets, orange handles and indicators;
- OCP/BMC/VGA/USB/serial/NMI relief;
- independently arranged left/right bosses, fasteners and upper lips;
- top cover, stampings, latch, vent and edge seams;
- bottom plate and verified stamped seam relief.

Main materials are OPAQUE/double-sided false; all six source-photo materials use KHR_materials_unlit. There are no external resources, negative/mirrored node transforms or missing UVs on textured primitives.

## Standard GLB

Path: model/Lenovo-ThinkServer-SR655-2.5inch.glb

Bytes: 11,964,408

SHA-256: 51e5d5a72fb4f4471d76cb24f16627d10e7ea12993ebeec220aa2da7f7f7bc25

Structural audit: PASS, zero errors and zero warnings.

Bounds: approximately 482.000 x 86.500 x 764.860 mm versus 482.0 x 86.5 x 764.7 mm. Non-uniform dimension-ratio error: 0.0139%.

All six standard embedded images were extracted and are pixel-identical to the approved RGB build textures.

## Web GLB

Path: model/Lenovo-ThinkServer-SR655-2.5inch-web.glb

Bytes: 8,382,752

SHA-256: 3a721b51d754151d01b5981391318b5d74b361ef8e9f980228167dc8846f1f09

Structural audit: PASS, zero errors and zero warnings. Geometry, node/material counts, bounds and orientation match the standard model; only texture resolution/file size is reduced.

## Independent viewer validation

Three.js 0.180 GLTFLoader rendered the standard GLB from front, rear, physical right, physical left, top, bottom, front-right and rear-right. Babylon.js independently rendered the web GLB from the same eight views. Each engine also loaded four check views of the opposite standard/web model, for 24 actual-GLB renders total.

Both engines agree on face assignment, text direction, physical left/right orientation, opacity, 24-carrier count, 8-slot rear, two AC PSUs and three-quarter geometry. The engine-to-engine raw pixel differences are lighting/antialiasing diagnostics, not feature discrepancies.

Standard versus web same-camera mean RGB difference is at most 0.520367/255 in Three.js and 0.494065/255 in Babylon.js.

## Source comparisons

Thirty-two comparison sheets cover:

- six orthographic and two authoritative three-quarter views in Three.js;
- the same eight in Babylon.js;
- eight engine-parity views;
- eight standard-versus-web checks.

Aligned source/render mean RGB differences are at most 7.621456/255 in Three.js and 15.388142/255 in Babylon.js. Manual feature review confirms all identity-bearing rows in feature-inventory.csv map one-to-one to the actual GLB renders.

## Official model backup

The public Lenovo InfinityRT viewer's original raw files are retained unchanged at source/optional-3d/Lenovo-ThinkSystem-SR655-official-viewer-original-files.tar.gz.

Archive size: 16,590,938 bytes

Archive SHA-256: 2d99c8fe4bc86f0ed28575421e76630a356cb69360e1dcb09b44c2c81af24a3e

The package is an optional official backup and evidence source only. It did not replace or supply mesh geometry to the newly constructed GLBs.

## Final decision

PASS. There are no unresolved QA errors or non-bottom evidence gaps, and the bottom is exact-model evidence-backed rather than a fallback.
