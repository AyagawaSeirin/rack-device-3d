# Juniper MX304 evidence and source ledger

Access date: 2026-08-23, Asia/Singapore

## Frozen result

The delivered physical assembly is the AC premium configuration represented by the user screenshot and the Juniper official image set: MX304-PREM-AC-FS physical configuration, comprising an MX304-PREM chassis, two JNP304-RE Routing Engines, two MX304-LMIC16-BASE line cards, two JNP-PWR2200-AC power supplies, and three JNP-FAN-2RU fan modules. The front has no installed optics, blank card panels, cable-management brackets, or optional front air-filter cover. All non-bottom identity and configuration fields are verified. The bottom uses the documented controlled fallback, so the target completion status is PASS_WITH_BOTTOM_FALLBACK if model QA passes.

## User screenshot inspection

Local original: source/originals/user-device-list.png, SHA-256 8ee991db9af36f19c3c3bff7a4c73dcd8df47f8a844e8e6febf5601dda095be1, 1042 x 1380 RGB PNG.

The second readable device row says Juniper and MX304 and shows both a front and rear thumbnail. Original-detail inspection proves the intended row and the broad two-by-two front card arrangement plus AC-style rear with three orange fan blocks. The row crop is retained as qa/reference/user-mx304-row.png. Its very small device thumbnails cannot prove component PIDs, port labels, exact side/top/bottom details, dimensions, or serial markings. It is a target-selection clue only and is not a final texture or primary style source.

## Identity and configuration chain

1. Juniper MX304 System Overview distinguishes MX304-BASE from MX304-PREM. MX304-PREM has two Routing Engines, two power supplies, and three fan trays. URL: https://www.juniper.net/documentation/us/en/hardware/mx304/topics/topic-map/mx304-system-overview.html
2. The official front photo and Hardware Guide printed pages 17-18 show the exact two-RE/two-LMIC16 front seen in the screenshot: RE0 and RE1/LMIC2 above LMIC0 and LMIC1. URLs: https://www.juniper.net/us/en/company/images/image-library-logos-and-product-photos/products/mx304.html and https://www.juniper.net/documentation/us/en/hardware/mx304/mx304.pdf
3. The official Hardware Guide printed page 13 states MX304-PREM has two Routing Engines, two power supplies, and three fan trays. Printed page 14 lists MX304-LMIC16-BASE and JNP304-RE variants. Printed page 44 identifies the 16-port LMIC face.
4. The user-mandated AC decision and the screenshot rear both match the official AC rear photo and Hardware Guide printed page 19. The DC rear has visibly different transparent terminal shields and diagonal orange handles and is excluded.
5. The current HPE/Juniper datasheet result lists MX304-PREM, JNP304-RE, JNP-PWR2200-AC, and MX304-LMIC16-BASE. Current PDF viewer/download page: https://www.hpe.com/psnow/doc/a00150831enw
6. Juniper Support Insights publicly lists MX304-PREM-AC-FS as an MX304 supported device SKU. URL: https://www.juniper.net/documentation/us/en/software/jsi/juniper-support-insights-user-guide/jsi-jcloud-user-guide/topics/concept/jsi-supported-devices.html
7. The Juniper Community MX304 Deepdive independently shows and labels the two-RE/two-LMIC configuration and reports AC AFO 2200 W PSUs plus three front-to-back fan trays. URL: https://community.juniper.net/blogs/reema-ray/2023/03/28/mx304-deepdive

The FS suffix is a bundle/software designation rather than a separately visible chassis shape. Exterior geometry is frozen by MX304-PREM plus the installed FRUs above; no unobservable license-specific mark is invented.

## Dimension ledger and conflict resolution

| field | frozen value | source and inclusion rule |
|---|---:|---|
| body_width_mm | 440.9 | HCT and Hardware Guide Figure 32/Table 23: 17.36 in / 44.09 cm |
| overall_width_mm | 482.6 | 19 in rack span across the two confirmed front ears |
| height_mm | 88.9 | 3.5 in, 2 U |
| body_depth_mm | 610.0 | 24.01 in bare chassis/body depth; no optional cable manager/filter cover |
| overall_depth_mm | 667.2 | Hardware Guide Figure 35: 26.27 in without air-filter cover; includes visible front/rear FRU projections |
| front_projection_mm | 16.7 derived | 667.2 minus 610.0 minus proven 40.5 mm rear projection; tolerance plus/minus 2 mm |
| rear_projection_mm | 40.5 | Hardware Guide Figure 35 labels 1.59 in rear FRU projection |
| rack_ear_left_extension_mm | 20.85 | half of 482.6 minus 440.9 |
| rack_ear_right_extension_mm | 20.85 | half of 482.6 minus 440.9 |
| maximum_installation_depth_mm | 782.0, excluded | Table 23 value with optional cable management and handles; not the photographed delivery subject |

The Hardware Guide printed page 17 prose says 17.63 in / 44.8 cm, while Figure 32, Table 23, current HCT, and Juniper Community dimensions consistently say about 17.36 in / 44.09 cm or rounded 440 mm. The 17.63 figure is treated as a transposition typo. The model uses the four-way corroborated 440.9 mm body width.

## PDF fallback and visual inspection

No PDF skill was available. The environment also lacked pdfinfo and pdftotext. The explicit fallback used Ghostscript 10.02.1 txtwrite for searchable text and Ghostscript pngalpha at 200 dpi for page rendering. Every retained page image was inspected with original-detail image viewing. The untouched official 266-page PDF is source/originals/mx304.pdf, SHA-256 8585166142102d94a529191446cadd51fbe48ce9e86a50849c5cf45c15789532.

Rendered/inspected actual PDF pages and printed-page meanings:

- mx304-actual-p023.png, printed 13: MX304-PREM, JNP-FAN-2RU, and JNP-PWR2200-AC identity table.
- mx304-actual-p024.png, printed 14: MX304-LMIC16-BASE and JNP304-RE model table.
- mx304-actual-p025.png, printed 15: 1+1 AC redundancy and three-fan requirement.
- mx304-actual-p027.png, printed 17: exact two-RE/two-LMIC front photo and chassis description.
- mx304-actual-p028.png, printed 18: exact slot positions for two-RE/two-LMIC and rejected one-RE/three-LMIC alternative.
- mx304-actual-p029.png, printed 19: exact AC rear photo/diagram and rejected DC rear photo.
- mx304-actual-p030.png, printed 20: DC/HVAC diagrams used only to exclude those variants.
- mx304-actual-p034.png, printed 24: optional cable manager, confirmed absent from screenshot target.
- mx304-actual-p049.png, printed 39: JNP304-RE identity.
- mx304-actual-p054.png, printed 44: MX304-LMIC16-BASE geometry and 16-port count.
- mx304-actual-p070.png, printed 60: top/plan dimension drawing and rack/body relationships.
- mx304-actual-p072.png, printed 62: no-air-filter plan view, 26.27 in overall depth, and physical table start.
- mx304-actual-p073.png, printed 63: body, FRU, PSU, and optional component dimensions.
- mx304-actual-p106.png, printed 96: exact top/right-side installation drawing, rail-slot pattern, and optional cable manager.
- mx304-actual-p107.png, printed 97: both side shells, rear brackets, and front-only rack-ear/rack attachment evidence.
- mx304-actual-p108.png, printed 98: optional external air-filter cover, confirmed excluded.
- mx304-actual-p109.png, printed 99: both left/right side panels and matching rail-slot/screw patterns.
- mx304-actual-p110.png, printed 100: exact side/top shell with rack placement and optional cover.

The extracted text is source/pdf-pages/mx304.txt. Page-render SHA-256 values are in source/checksums.sha256.

## Downloaded raster inspection ledger

### Official Juniper image library

- source/originals/mx304-front-high.jpg, 2100 x 691, real photograph, exact target front, primary identity/style source. It proves two JNP304-RE, two MX304-LMIC16 faces, 32 empty cages, eight cyan handles, right badge, ears, materials, and lighting. It has a white studio background and soft product shadow that imagegen must remove without restyling.
- source/originals/mx304-frontwtop-high.jpg, 2100 x 603, real photograph, exact target front/top three-quarter. It proves top color, front edge, panel height, and no optional filter cover; top far/rear detail remains partially hidden.
- source/originals/mx304-left-high.jpg, 2100 x 756, real photograph labeled Left view, exact target installed front with partial left-side/top exposure. It is not orthographic, so it is a binding left reconstruction source rather than a direct side texture.
- source/originals/mx304-right-high.jpg, 2100 x 750, real photograph labeled Right view, exact target installed front with partial right-side/top exposure. It is not orthographic, so it is a binding right reconstruction source rather than a direct side texture.
- source/originals/mx304-rear-ac-high.jpg, 2100 x 675, real photograph, exact AC rear and primary identity/style source. It proves two AC PSUs, timing board, three fan trays, ground panel, materials, and orange color.
- source/originals/mx304-rear-dc-high.jpg, 2100 x 675, real photograph, rejected DC variant used only for negative comparison. Its terminal covers and diagonal handles must not enter the model.

Official image-library URL: https://www.juniper.net/us/en/company/images/image-library-logos-and-product-photos/products/mx304.html

### Juniper Community exact-model material

- source/originals/community-mx304-01.png, 1260 x 351 RGBA, real-product three-quarter, exact two-RE/two-LMIC front/top. Supports top color, seam, rack ears, and target configuration; not a direct face.
- source/originals/community-mx304-02.png, 2276 x 670 RGBA, annotated official-style product view. Supports rounded 440 x 88.9 x 610 mm dimensions; annotations are not texture content.
- source/originals/community-mx304-06.png, 741 x 212 RGBA, annotated exact two-RE/two-LMIC front. Supports slot labels RE0, RE1, LMIC0, LMIC1; annotation text is not texture content.
- source/originals/community-mx304-08.png, 1029 x 527 RGBA, annotated exact AC rear. Supports PSU0/1, Fan0/1/2, and timing-interface names; crops/callouts are not texture content.

Source URL: https://community.juniper.net/blogs/reema-ray/2023/03/28/mx304-deepdive

### Exact-model used-equipment listing

Listing: https://www.ebay.com/itm/357632213474. The public rendered page exposes seven images but real-browser and direct page requests returned HTTP 403. Public image resources were downloaded without bypassing authentication or access controls.

- ebay-357632213474-01.webp: exact JNP304/MX304 top and one side, real used photo; primary top chassis source. Proves two top panels, seam, embossed Juniper logo, service hatch, labels, two rows of side rail slots, screws, gray material, and front/rear protrusions. Installed front cards differ and are excluded.
- ebay-357632213474-02.webp: close-up real photo of top regulatory/serial area. Proves model JNP304/MX304 and service hatch; serial/barcodes are unit-specific and excluded from generated textures.
- ebay-357632213474-03.webp: front-left close-up of a partially populated unit. Proves JNP304-RE face depth and internal slot recess, but is not target front configuration.
- ebay-357632213474-04.webp: close-up of empty/blanked front slot faces and MX304 badge. Proves badge position and chassis frame; card occupancy differs and is excluded.
- ebay-357632213474-05.webp: rear/right/top three-quarter real photo. Proves three fan-tray depth, side rail slots, rear ground end panel, top finish, and AC chassis silhouette.
- ebay-357632213474-06.webp: AC PSU/timing close-up with seller cable. Proves AC inlet/fan/handle depth and timing ports. Cable and seller condition are excluded.
- ebay-357632213474-07.webp: fan close-up. Proves orange frame relief, honeycomb recess, AIR OUT badges, and Fan 0/1/2 separators.

### Bottom fallback input

- source/third-party/generic-2u-underside-bkhd.jpg, 1500 x 1500, secondary product render, not MX304. It is used only for neutral gray sheet-metal underside character. Its holes, feet, handles, hatch, and layout are explicitly non-binding and must be omitted. URL: https://www.bkipc.com/Uploads/17627777296911d60e5fb57.jpg

## Six-face evidence conclusion

- Front: direct exact official real photo; SOURCE_LOCKED_GENERATION.
- Rear: direct exact official AC real photo; SOURCE_LOCKED_GENERATION.
- Left: official left three-quarter plus exact side real photo and installation diagrams jointly prove all visible traits; MULTI_REFERENCE_RECONSTRUCTION.
- Right: official right three-quarter plus exact side real photo and diagrams; documentation shows the matching side rail system on both sides; MULTI_REFERENCE_RECONSTRUCTION.
- Top: exact-model real top/side used photo, official front-top photo, plan drawing, and additional real rear/top photo; MULTI_REFERENCE_RECONSTRUCTION.
- Bottom: no exact view after required escalation; GENERIC_BOTTOM_FALLBACK.

## Bottom search log

Searched official MX304 product pages, image library, hardware guide, datasheet result, current HCT, installation/clearance diagrams, community deep-dive, public official videos/quick-start results, exact-model reseller/refurbisher pages, eBay used listing and all seven public images, BrightStar Systems, HPE Store, English terms underside/bottom/teardown/unboxing/used/auction, Chinese terms 底面/底部/机箱, and Japanese terms 底面/シャーシ/写真. Dynamic HCT and eBay pages returned public 403 in a real browser; no control was bypassed. No exact MX304 underside was found. Side/plan evidence proves no silhouette-changing bottom foot or rail. The fallback therefore uses a plain opaque sheet and cannot affect verified side or three-quarter silhouettes.

## Optional official 3D/CAD result

No public exact official 3D/CAD/GLB/GLTF/STEP/OBJ/FBX or interactive 3D model was found. Searches covered official Juniper/HPE pages, media HTML/resource-extension scans, HCT, HPE Store, and current web queries. The HCT real-browser request returned 403. No asset file is available to download; details are in source/optional-3d/README.md.

## Inclusion and exclusion rules

Include the factory Juniper Networks MX304 front badge, JNP304-RE and MX304-LMIC16 factory markings where readable, correct physical location/orientation, embossed top Juniper mark, AC PSU markings, and AIR OUT fan badges. Do not invent or copy a unit serial number, barcode, QR code, seller inventory sticker, cable, scratch pattern, shipping damage, pseudo-text, lit LED state, transceiver, blank panel, air-filter cover, or cable manager. Preserve real surface grain and photographic character rather than cleaning the device into a generic CGI render.

## Repair v2 — independent physical-left replacement

The previous final left face is rejected because it was produced by mirroring the right generation. The complete pre-repair state, including that invalid left PNG, both GLBs, reports, renders and comparisons, is preserved under repair-v2/before/ with checksums. No prior AI face, right.png, GLB or render was used as a source for the replacement.

The repaired left lineage uses MULTI_REFERENCE_RECONSTRUCTION from independent evidence:

1. Official mx304-left-high.jpg, currently listed by Juniper as Left view photo, is the primary real identity/material/style source for the exact 2xRE/2xLMIC16 target.
2. Exact JNP304/MX304 used-equipment photo ebay-357632213474-01.webp is the binding complete physical-left geometry/material source. Rear orange fan handles are at image-left and front cyan handles/front ear at image-right. It proves 2 rows x 4 long rail recesses, one larger front pad, and the real nonuniform screw/black-locator sequence.
3. community-mx304-01.png independently proves the exact target front configuration and front/top edge material.
4. Official Hardware Guide printed pages 96–99 constrain the physical-left front/rear direction, slot count, pad and mounting-hole geometry. Diagrams do not establish color/style.

Three built-in imagegen repair attempts were made from the same real/official inputs only. The first is selected for factual fidelity; the second is rejected because its tightly cropped ratio remained 6.06:1; the third is rejected for 2x3 slots and visible top perspective. The selected first call has correct 2x4 slots, front-right/rear-left direction, one front pad and nonuniform fasteners. Its initial tight ratio was 5.86:1. To avoid forbidden whole-face axis stretching, repair-v2/source/rectify-left.py lengthens only visually inspected feature-free gray sheet-metal gaps by 2.5x; all feature segments remain at original horizontal pixel scale. The rectified 2409x321 content is then resized uniformly to 3072x409, producing 0.0792% physical-ratio error without mirroring, flipping or using right-side pixels.

The accepted repaired left output is views/left.png, SHA-256 11a6d4c632cddea4b677730f5173aefbb240f7e1201fb930cd4047bd32b6ce64. Full input classification, orientation proof and forbidden lineage are recorded in repair-v2/source/left-evidence.md and repair-v2/source/left-source-lock.csv.
