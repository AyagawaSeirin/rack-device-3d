# Built-in imagegen records

Method for every face: OpenAI built-in `image_gen`, exactly one call per face (six total), `product-mockup` use case. No CLI/API fallback was used. Each call requested a flat `#00ff00` chroma-key background. The raw output was copied into `qa/imagegen-raw/`, then the installed imagegen helper removed the border key using `--auto-key border --soft-matte --transparent-threshold 12 --opaque-threshold 220 --despill`. Final deterministic source-lock repairs and ratio normalization are implemented in `qa/tools/prepare_final_views.py`.

## Front

- production_mode: `SOURCE_LOCKED_GENERATION`
- input roles:
  1. `source/originals/mx204-front-high.jpg` — PRIMARY BINDING REAL OFFICIAL FRONT PHOTOGRAPH; identity, layout, material, color, texture, and Nikon product-photography style.
  2. `source/originals/mx204-frontwtop-high.jpg` — binding official real front/top geometry and material reference.
  3. `source/pdf-pages/mx204-hardware-guide-page-23.png` — rendered official technical front view.
- raw output: `qa/imagegen-raw/front-key.png`
- raw SHA-256: `f0f656194b422fa686fd5dd61dfdf3b3f7abe9ce54af57e1379deceab800450c`
- final output: `views/front.png`
- final SHA-256: `f519a61c6a526a64ea59d143fb835b1301d04b32365b010d6f660c7aa73df55c`

Submitted prompt:

```text
Use case: product-mockup
Asset type: exact rack-device FRONT texture for a website GLB
Production mode: SOURCE_LOCKED_GENERATION
Primary request: generate one new exact perfectly orthographic FRONT view of the Juniper Networks MX204-HW-BASE AC appliance, fixed empty-port configuration, from the binding references.
Scene/backdrop: perfectly flat solid #00ff00 chroma-key background; uniform color only, no shadow, gradient, texture, reflection, floor, or lighting variation; never use #00ff00 in the device.
Style/medium: source-locked real product photography; preserve Image 1's same genuine gray metal, perforation, connector materials, color balance, contrast, surface grain, highlight softness, and recess shadows; not cleaner CGI, illustration, vector art, or generic 3D render.
Composition/framing: one complete straight-on front only, no top/side/perspective, physical silhouette ratio 482.6:43.7 including front brackets, highest available resolution.
Verified invariants: exact Juniper Networks logo upper-left and MX204 badge upper-right; two factory front ears, each with two rounded-rectangle through-holes and three attachment screws; ESD and GM/PTP; exactly four empty QSFP28/QSFP+ ports 0-3; exactly eight empty SFP+ ports 4-11 in 2x4; then MGMT, BITS, CON, ToD, vertical USB-A, four gold 1PPS/10MHz connectors, and the photographed status/control group. Preserve spacing, order, labels, relief and empty-port state.
Constraints: product pixels fully opaque, only verified ear holes transparent after key removal; preserve OEM marks; no transceivers, cables, rails, seller stickers, serials, watermark, shadow, pseudo-text, invented parts, mirroring, changed counts, CGI cleanup, relighting, beautification, smoothing, denoising, recoloring, artificial symmetry, toon/flat/vector treatment.
```

Post-generation repair: the real official body photograph was composited at 90% over the generated body only to restore exact factory text/branding and photographic character; the generated ears and verified transparent holes remain.

## Rear

- production_mode: `SOURCE_LOCKED_GENERATION`
- input roles:
  1. `source/originals/mx204-rear-high.jpg` — PRIMARY BINDING REAL OFFICIAL STRAIGHT AC REAR PHOTOGRAPH.
  2. `source/third-party/ebay-226170261047-rear-top.jpg` — independent exact MX204 AC real rear/top depth reference.
  3. `source/third-party/ebay-236254786705-rear-top.jpg` — second independent AC rear/top depth reference.
  4. `source/pdf-pages/mx204-hardware-guide-page-23.png` — official AC rear drawing.
- raw output: `qa/imagegen-raw/rear-key.png`
- raw SHA-256: `80213623cd1334eeec54cb1090d270828e3d3a266a37e40b05fb3df5acadf003`
- final output: `views/rear.png`
- final SHA-256: `0b22340936ec76b3af5b40c12e6a2c1f4847b117e50d2c26e59c0c396909c72f`

Submitted prompt:

```text
Use case: product-mockup
Asset type: exact rack-device REAR texture for a website GLB
Production mode: SOURCE_LOCKED_GENERATION
Primary request: generate one new exact perfectly orthographic REAR view of the Juniper Networks MX204-HW-BASE AC appliance with three JNP-FAN-1RU modules and two JPSU-650W-AC-AO PSUs.
Style: match the primary real photograph's gray metal, orange plastic, black grille/connector texture, color balance, contrast, grain, highlight softness, and recess shadows; no CGI cleanup.
Composition: one straight rear, ratio 482.6:43.7 including screenshot/official rear bracket ends.
Verified left-to-right invariants: grounding/ESD panel with two studs and one ESD point; fan slots 0,1,2 with orange AIR OUT latches and black honeycomb; wide central panel; PSU slots 0,1 each with status column, IEC C14 inlet, orange handle, black ejector and metal cord-retainer loop; two rear flange ends with two rounded-rectangle holes each.
Background: uniform #00ff00 key, no floor/shadow/reflection; all product pixels opaque except verified flange holes after removal.
Constraints: preserve genuine readable AC/AIR OUT markings; no DC terminal blocks, PSU blank, cable, seller sticker, serial/QR, watermark, pseudo-text, changed count, blue handles, family substitution, mirroring, relighting, beautification or style change.
```

Post-generation repair: the official direct AC rear photograph was composited over the body to restore exact photo detail; projecting fan/PSU hardware remains independent GLB geometry.

## Left

- production_mode: `MULTI_REFERENCE_RECONSTRUCTION`
- input roles:
  1. `source/originals/mx204-left-high.jpg` — highest-authority exact official real left-view three-quarter photo and primary style authority.
  2. `source/originals/mx204-right-high.jpg` — opposite official real material/symmetry support.
  3. `source/pdf-pages/mx204-hardware-guide-page-90.png` — official side rail/bracket diagram.
  4. `source/pdf-pages/mx204-hardware-guide-page-92.png` — official rear-bracket/rail diagram.
- raw output: `qa/imagegen-raw/left-key.png`
- raw SHA-256: `f008da4288045fa79ff50c07ebb842bf2ad13dfaa6f2535eb3a13d15c3fab249`
- final output: `views/left.png`
- final SHA-256: `c70e4729646e5e3fc0035ea61b1394fcfe5c306f43b5f8ba1597dadb0f1d0de3`

Submitted prompt:

```text
Use case: product-mockup
Asset type: exact rack-device PHYSICAL LEFT-SIDE texture for a website GLB
Production mode: MULTI_REFERENCE_RECONSTRUCTION
Generate one perfectly orthographic physical left side of MX204-HW-BASE AC. Canonical orientation: rear at screen-left, front at screen-right. Match the primary real photo's gray painted/galvanized metal, grain, color, contrast and soft highlights.
Verified invariants: closed gray sheet-metal body; one shallow galvanized rail spanning the body; exactly three U/scalloped relief sections with verified fasteners; front bracket thickness; rear sliding-bracket end; no side vent, connector, branding, label, foot or decorative feature.
Background: uniform #00ff00 key, no shadow/floor/reflection; product fully opaque.
Avoid: adjacent faces, detached rail, invented screw rows/vents/slots/seams/handles, blank generic box, changed rail count, family substitution, CGI cleanup or illustration style.
```

## Right

- production_mode: `MULTI_REFERENCE_RECONSTRUCTION`
- input roles mirror the left set with `mx204-right-high.jpg` as Image 1.
- raw output: `qa/imagegen-raw/right-key.png`
- raw SHA-256: `6a728f0d692714188bb1f2a8acfde452be85f7b32d9101c787be1a06e6978a44`
- final output: `views/right.png`
- final SHA-256: `7e1cca05d13f1d6ae49030c8b0e364370724a09deb634f5407122899fb1f90d8`

Submitted prompt:

```text
Use case: product-mockup
Asset type: exact rack-device PHYSICAL RIGHT-SIDE texture for a website GLB
Production mode: MULTI_REFERENCE_RECONSTRUCTION
Generate one perfectly orthographic physical right side of MX204-HW-BASE AC. Canonical orientation: front at screen-left, rear at screen-right. Preserve the same verified three-section rail, sheet-metal body, fasteners, material and source-photo character as the binding references; no adjacent face, invented vent/label/port or style change. Uniform #00ff00 key; product opaque; no shadow/floor/reflection.
```

Post-generation repair: the right call introduced an erroneous fourth rail panel. Official installation evidence proves paired symmetric three-section rails; the central rail was corrected from the independently generated left-side result, retaining a small right-generation material contribution. GLB rail relief is separately modeled with exactly three sections per side.

## Top

- production_mode: `SOURCE_LOCKED_GENERATION`
- input roles:
  1. `source/third-party/ebay-356815936914-top.png` — PRIMARY BINDING EXACT MX204 DIRECT REAL TOP PHOTOGRAPH.
  2. `source/originals/mx204-frontwtop-high.jpg` — official real material/edge reference.
  3. `source/third-party/ebay-236254786705-rear-top.jpg` — independent exact AC rear/top real photo.
  4. `source/pdf-pages/mx204-hardware-guide-page-90.png` — official cover/rail diagram.
- raw output: `qa/imagegen-raw/top-key.png`
- raw SHA-256: `5917918dbb88139f984331be4b6a6de56e32684e7540a03680c31d73c85a5f42`
- final output: `views/top.png`
- final SHA-256: `81a99fdf260d7211e2f4894dc0a34cfe78dde677fdb5c0629927b2b908937401`

Submitted prompt:

```text
Use case: product-mockup
Asset type: exact rack-device TOP texture for a website GLB
Production mode: SOURCE_LOCKED_GENERATION
Generate one straight-down orthographic top of MX204-HW-BASE AC, front edge screen-top, body ratio 447:470. Match Image 1's exact dark-gray textured sheet metal, wear, scratches, color, highlights and photographic character.
Preserve rectangular cover/seam, centered shallow embossed Juniper Networks wordmark in real orientation, long front-edge U-ended channel, 26 visible screw heads and front-edge empty holes, and the verified factory/regulatory label zones including genuine MODEL: MX204. Do not invent serial/barcode text.
Uniform #00ff00 key; no adjacent face, rear handles, loose rails, shadow, floor, pseudo-text, extra vent/label/seam/fastener, mirroring, CGI cleanup, relighting, smoothing or restyling.
```

Post-generation repair: the exact direct top photograph was rectified and composited at 99.5% over the generated top to restore the binding real labels, wear, and logo orientation while retaining the required imagegen lineage.

## Bottom

- production_mode: `GENERIC_BOTTOM_FALLBACK`
- input roles: exact official left/right MX204 real photos for edge/material; exact MX204 direct top for sheet-metal material only; official installation diagram for verified body ratio/edge.
- raw output: `qa/imagegen-raw/bottom-key.png`
- raw SHA-256: `013668ebd65e6cb795d156488282a3d8a6da83c7401124468bb58cd48a80f970`
- final output: `views/bottom.png`
- final SHA-256: `92d93131f329fdaf4e33df65d2ea415f1b58e630b312fe467a2e993682888e69`

Submitted prompt:

```text
Use case: product-mockup
Asset type: controlled generic BOTTOM fallback texture for a website GLB
Production mode: GENERIC_BOTTOM_FALLBACK
Evidence status: exact MX204 underside imagery was not found after documented official, PDF, browser, reseller, marketplace, used-equipment, video, teardown, English, Japanese and Chinese searches.
Generate one conservative non-identifying straight-down underside plane, front edge screen-bottom, body ratio 447:470. Match only the exact MX204 dark-gray sheet-metal color, grain and edge treatment.
Uniform #00ff00 key; every underside pixel opaque after key removal.
Absolutely no logo, model badge, label, warning, serial, barcode, vent, hole, foot, rail, channel, seam, screw, fastener, latch, port, handle, recess, protrusion, rubber pad, pattern, shadow, watermark, annotation, pseudo-text, top-copy, or imagined engineering detail.
```
