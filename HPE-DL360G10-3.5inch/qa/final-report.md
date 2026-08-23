# HPE ProLiant DL360 Gen10 4LFF final QA report

Final status: **PASS_WITH_BOTTOM_FALLBACK**

The newly constructed standard and web GLBs pass identity, installed configuration, six-face lineage, dimensions, opaque-material, orientation, structural, and dual-viewer actual-load gates. The only exception is the documented bottom-only fallback after the recorded official, dynamic-page, reseller, marketplace, auction, used-equipment, video, and multilingual underside searches found no usable exact underside.

## Frozen identity and configuration

- HPE ProLiant DL360 Gen10, 1U, four 3.5-inch LFF Smart Carrier positions, no security bezel.
- 867958-B21 embedded-LOM generation rear: three PCIe positions; 331FLR four-RJ45 FlexibleLOM; embedded 331i four-RJ45; serial DB9; dedicated iLO 5; two USB 3.0; VGA; no rear drive cage.
- Two HPE 500W Flex Slot Platinum 94% hot-plug AC power supplies with IEC AC inputs; no DC or single-PSU substitution.
- HPE and ProLiant DL360 Gen10 factory branding remains visible and reads normally.
- Physical left and right assets and geometry are independent; no mirror transform is present.

## Final GLBs

| Profile | File | Bytes | SHA-256 |
|---|---|---:|---|
| standard | `model/HPE-DL360G10-3.5inch.glb` | 20,458,036 | `d6439e734fc85aaef0125f8c40cf0807bf9a147050d594026a3e4d8e1f3a2ac1` |
| web | `model/HPE-DL360G10-3.5inch-web.glb` | 8,165,268 | `ab529ee20cb9d295165bb47cdd0429ada6d44b48f87ba4fca315d0cde3cec4bc` |

Both are self-contained GLB 2.0 files with the same 159 named exterior/internal geometry groups, scene bounds, configuration metadata, and six independently embedded face images. Each has 159 nodes, meshes, and primitives; 17 materials; six textures/images; no mirrored nodes; no external buffers; and OPAQUE source-photo face materials using `KHR_materials_unlit`.

Actual world bounds are 482.6 x 43.2 x 751.75 mm. HPE's published body/system dimensions are 434.6 x 42.9 x 749.8 mm; the separate 482.6 mm rack-ear span and 1.95 mm rear handle relief are recorded in `source/dimension-ledger.csv`. The final normalized dimension-ratio error is 0.3783%, within the audit tolerance.

## Six faces and lineage

- `front.png`: MULTI_REFERENCE_RECONSTRUCTION from the user configuration lock, official 4LFF QuickSpecs view/diagram, and exact 4LFF real photographs.
- `rear.png`: SOURCE_LOCKED_GENERATION from the official shown embedded-LOM rear and the user's row-4 lock.
- `left.png` and `right.png`: independent MULTI_REFERENCE_RECONSTRUCTION; no mirrored image, UV, node, or negative scale.
- `top.png`: MULTI_REFERENCE_RECONSTRUCTION locked to an exact photographed 4LFF chassis top.
- `bottom.png`: documented GENERIC_BOTTOM_FALLBACK, conservative and non-identifying, with no copied top, logo, label, vent, foot, rail, or unsupported mechanism.

The final views audit is PASS. Its six automated warnings only report antialiased/transparent pixels somewhere inside each complete content rectangle; original-detail inspection confirms every face has 0% core pixels below alpha 250, and the GLBs composite all mapped chassis texels to opaque RGB.

## Actual-load validation

- Three.js 0.179.1: standard and web, six orthographic plus four three-quarter views each, plus one dark-background front check each: 22 screenshots.
- Babylon.js 8.22.2: the same 22 screenshots. The QA scene explicitly uses the glTF right-handed convention so physical left/right naming agrees with Three.js.
- Required actual-GLB render count: 40. Additional dark-background checks: 4. Total: 44.
- Final browser console result: zero errors and zero warnings in both viewer sessions.
- Standard/web mean pixel MAE across the same ten cameras is 0.0643% in Three.js and 0.0427% in Babylon.js; their scene bounds are identical.
- Twenty-four reference/render/overlay/difference sheets, four ten-view viewer sheets, two three-quarter source-review sheets, and one causal geometry-repair before/after sheet are stored in `qa/comparisons/`.

## Structural gates

- `qa/views-audit-final.json`: PASS, 0 errors.
- `qa/glb-standard-audit-final.json`: PASS, 0 errors, 0 warnings.
- `qa/glb-web-audit-final.json`: PASS, 0 errors, 0 warnings.
- Front has exactly four LFF carriers and two front-only ears; rear has no rear-ear geometry, exact port ordering, three PCIe positions, and two AC PSUs.
- Source-locked `500W`/`94%` labels and carrier details remain visible; approximate solid overlay disks were removed from the final geometry layer.
- Main equipment faces are opaque; no transparent ports, vents, grilles, labels, or empty interior are exposed.

## Official 3D search and residual risk

No exact public official HPE GLB/glTF/CAD/AR model was found. The reproducible search record is `source/optional-3d/README.md`; no unofficial model is described as official and none replaced either constructed GLB.

Remaining risk is limited to the exact underside, which is unavailable and is therefore disclosed as the controlled bottom-only fallback. The second residual uncertainty is the vendor's lack of a separately published rack-ear/handle envelope; those protrusions are recorded independently from the official body dimensions rather than silently folded into them.

No git commit or push was performed.
