# Juniper MX204 evidence ledger

Access date for all online sources: 2026-08-23 (Asia/Singapore).

## PDF fallback disclosure

No `pdf` skill is installed in this environment. The required explicit fallback was used: the current official 199-page MX204 hardware guide was downloaded unchanged, text was extracted locally with Ghostscript `txtwrite`, relevant pages were rendered at 300 dpi with Ghostscript `png16m`, and every saved page render was inspected with the image viewer at original detail. The PDF is `source/originals/mx204-hardware-guide.pdf` (4,199,319 bytes; SHA-256 `81d9d2dd9550ecb6f54b6e46d6c00afc2bebac15314052e788998bde08749109`). Relevant saved PDF pages include 20-26 (overview, front, AC/DC rear, part numbers), 57 (physical dimensions), 60 (rear grounding), 66 (airflow/top schematic), and 90-92 (top/side rails and rear bracket installation).

## User screenshot inspection

- Local source: `source/originals/user-screenshot.png`
- SHA-256: `8ee991db9af36f19c3c3bff7a4c73dcd8df47f8a844e8e6febf5601dda095be1`
- Exact target row: third readable device row, after Juniper QFX5110 and Juniper MX304; label is `Juniper MX204`.
- What it proves: one 1U port-side front with the MX204 fixed I/O grouping and both front mounting flanges; one AC rear with three fan positions and two populated IEC-inlet power supplies; the rear thumbnail also shows mounting-flange ends.
- Limitations: 1042 x 1380 composite screenshot; target device thumbnails are only about 200 x 35 pixels. It cannot prove color, label text, fine connector shapes, fan latch color, side/top/bottom features, exact rail construction, or product-photo texture. It is a configuration clue, not a final texture or primary photographic-style source.

## Official sources

### Juniper MX204 media library

- URL: https://www.juniper.net/us/en/company/images/image-library-logos-and-product-photos/products/mx204.html
- Browser inspection: dynamic page was opened and inspected with Playwright; the rendered table exposed public original 1500-pixel JPEG URLs for front, front/top, left, right, and rear. Page footer states Juniper Networks copyright/all rights reserved; assets are retained for the user's stated internal-use workflow.
- Saved originals and SHA-256:
  - `mx204-front-high.jpg` — `41160618a6d21d36dd35d7776995504e39ece97d929dd88328fce9ff12c72ab9`
  - `mx204-frontwtop-high.jpg` — `a14e9aa3ee4112458edb143f9697babb2c817a0fdebc2e3862405e9c5977a55b`
  - `mx204-left-high.jpg` — `dbb9997ef2dd8b03871f9a226f998888379a45491d118c1605d5e150ce27914d`
  - `mx204-right-high.jpg` — `7f3a3a52a6dfe2074aab9c5177f8fdcf89e226550fbd051993d1e75791b966d3`
  - `mx204-rear-high.jpg` — `bf34896da6bc4a760f973083f6fc5df933c76236361bffe2e93b80a3f403b071`
- Inspection result: all five are exact MX204 real Nikon D800 product photographs. Front and rear are direct elevations. Left/right are three-quarter photographs, not direct orthographic sides; they bind material, top/side construction, ears, and silhouette. Rear is the fully populated AC configuration with three orange AIR OUT fan modules and two IEC-inlet AC PSUs.

### Current Juniper Hardware Compatibility Tool

- URL: https://apps.juniper.net/hct/product/MX204/hwspecs
- Proves: externally identical AC variants `MX204-HW-BASE (AC)` and `MX204-HWBASE-AC-FS`; fixed 1U chassis `JNP204-CHAS`; 17.6 in body width; 18.5 in body depth; 20.43 in depth with FRUs; front-to-back/AFO airflow; three `JNP-FAN-1RU` modules; AC PSU model `JPSU-650W-AC-AO`.
- Limitation: semantic specifications only; no bottom view.

### MX204 Universal Routing Platform Hardware Guide

- URL: https://www.juniper.net/documentation/us/en/hardware/mx204/mx204.pdf
- Title/version: `MX204 Universal Routing Platform Hardware Guide`, published 2026-07-30.
- Visual/text findings:
  - PDF page 21: fixed 1U system, four rate-selectable ports, eight SFP+ ports, two PSUs, three fans; exact front and top/side line art.
  - PDF page 23: exact front and AC rear line art; AC variant uses two AC power-supply modules.
  - PDF page 26: chassis `MX204`, fan `JNP-FAN-1RU`, AC PSU `JPSU-650W-AC-AO`, built-in `RE-S-1600x8`.
  - PDF page 57: AC fully loaded dimensions 19 in x 1.72 in x 18.5 in body depth and 20.43 in with fan/PSU handles.
  - PDF page 60: two threaded grounding points and rear-left location.
  - PDF page 66: exact top plan silhouette and front-to-back airflow.
  - PDF pages 90-92: factory side mounting rails, front brackets, movable rear brackets, and their visible relief/attachment.

### Juniper HTML documentation

- Chassis/configuration: https://www.juniper.net/documentation/us/en/hardware/mx204/topics/topic-map/mx204-chassis.html
- AC power system: https://www.juniper.net/documentation/us/en/hardware/mx204/topics/topic-map/mx204-ac-power-system.html
- Cooling: https://www.juniper.net/documentation/us/en/hardware/mx204/topics/topic-map/mx204-cooling-system.html
- Site/dimensions: https://www.juniper.net/documentation/us/en/hardware/mx204/topics/topic-map/mx204-site-guidelines-req.html
- Front ports: https://www.juniper.net/documentation/us/en/hardware/mx204/topics/topic-map/mx204-connecting-to-network.html
- Rack installation: https://www.juniper.net/documentation/us/en/hardware/mx204/topics/topic-map/mx204-installing.html
- Proves: component counts and part numbers, AC IEC inlet description, exact front connector types and timing ports, three fan slots 0-2, two PSU slots 0-1, AFO airflow, grounding studs, and side/rear rack-bracket mechanics.

## Exact-model third-party real photographs

Each image was downloaded unchanged and inspected at original detail. Seller backgrounds, cables, inventory stickers, serials, scratches, loose rails, and shipping props are excluded from the canonical assets.

- `source/third-party/ebay-356815936914-top.png`
  - Listing: https://www.ebay.com/itm/356815936914 (dynamic page returned a public 403 in Playwright; the publicly indexed original image URL remained accessible)
  - Image URL: https://image.pushauction.com/0/0/23ce7c1b-d0f9-4bb5-8b80-8d8f0b30d6d2/91ff3f3a-5272-462e-8824-70e5c4994d94.png
  - SHA-256: `de1380cb26923c81b303289306cfd3a6da4a60168303f526f5e61090a2552278`
  - Proves: near-direct top, embossed Juniper Networks wordmark, cover seam/fastener/stamping pattern, label zones, and exact MX204 identity label; AC rear handles are visible.
  - Limitations: used unit with scratches and serial-bearing seller photography; those unique serial values are not reproduced.
- `source/third-party/ebay-236254786705-rear-top.jpg`
  - Listing: https://www.ebay.com/itm/236254786705
  - Image URL: https://i.ebayimg.com/images/g/h1MAAeSwXbRoljJW/s-l1600.jpg
  - SHA-256: `4a90567d69fbcf08dac367096fb911f70a44fce80926ab136f28dc104151dd2b`
  - Proves: exact MX204 top and dual-AC rear relief, three fan latch protrusions, two PSU handle/cord-retainer assemblies.
- `source/third-party/ebay-226170261047-rear-top.jpg`
  - Listing: https://www.ebay.com/itm/226170261047
  - Image URL: https://i.ebayimg.com/images/g/e4cAAOSw9DBm~7yA/s-l1200.jpg
  - SHA-256: `93a5124c78e5f4e345029d1511fc26ad9b3a727251d5935d7d05047f905ba6bd`
  - Proves: second independent exact MX204 dual-AC rear/top photograph and real surface finish.
- `source/third-party/ebay-356014453430-rear.jpg`
  - Listing: https://www.ebay.com/itm/356014453430
  - Image URL: https://i.ebayimg.com/images/g/YhwAAOSw7dtnvQ81/s-l960.jpg
  - SHA-256: `80acb5d8d7565e2df8bb5e88c6f2404ff6c1f6787ee6bf7a9bbb410987d67383`
  - Proves: third exact MX204 dual-AC rear/top photograph; used only as corroboration because resolution is lower.
- `source/third-party/ebay-286102956961-top.jpg`
  - Listing: https://www.ebay.co.uk/itm/286102956961
  - Image URL: https://i.ebayimg.com/images/g/OL0AAOSwAIxnCUwO/s-l1200.jpg
  - SHA-256: `10e5d1bbf4e2d32b2d2dcbf50ec936fd2384f21e3a2e965b37e24aa0a463db18`
  - Proves: top/AC rear and separate Juniper side rail kit. The loose rail is supporting mechanical evidence, not installed-state texture.

### Rejected leads

- `source/third-party/uvation-Juniper_MX204_bottom.png`, SHA-256 `90c690e64b7c569d4e2bacb943a516512266fa8754992932d954f81583498cb4`, is not an MX204 and does not show a bottom; it was rejected after original-detail inspection and is never an imagegen identity input.
- `source/third-party/juniper-mx301-underside-fallback-g103372.png`, SHA-256 `cb1eb0e159251880506656b34f14910964d7819fb1cf5a7b008afb9820d4e103`, is an official MX301 top/side technical figure despite a misleading search-result description; it was rejected as a bottom reference and is not an imagegen input.

## Dimension ledger

- body_width_mm: 447 (17.6 in, current Hardware Compatibility Tool chassis-width field)
- overall_width_mm: 482.6 (19 in over front mounting brackets)
- height_mm: 43.7 (1.72 in, 1U)
- body_depth_mm: 470 (18.50 in)
- overall_depth_mm: 518.9 (20.43 in with fan and power handles)
- front_projection_mm: included in the 470 mm body-depth datum; no separate unsupported addition
- rear_projection_mm: 48.9 beyond body depth to fan/PSU handle extrema
- rack_ear_left_extension_mm: approximately 17.8, derived from (482.6 - 447) / 2
- rack_ear_right_extension_mm: approximately 17.8, derived from (482.6 - 447) / 2
- published_dimension_includes: 19-inch width includes front mounting brackets; 20.43-inch depth explicitly includes fan and power handles; body width and body depth are recorded separately
- tolerance: +/- 1 mm on documented dimensions; +/- 1.5 mm on small protrusions estimated from verified photographs

## Bottom search log and controlled fallback

Searches covered exact-model Juniper product/media pages, current hardware guide and its rendered figures, Hardware Compatibility Tool, official rack/maintenance/return documentation, public videos and teardown terms, reseller/used-equipment/auction/marketplace pages, and English/Japanese/Chinese terms for bottom/underside. Dynamic Juniper galleries were inspected in Playwright; an eBay listing returned a public 403 and was not bypassed. No exact MX204 underside photo or drawing was found. Searches for same-vendor 1U undersides also produced mislabeled top/rear images rather than a usable underside.

The required bottom mode is therefore `GENERIC_BOTTOM_FALLBACK`. The generated bottom must be a conservative, non-identifying, closed gray sheet-metal plane matching the verified 447:470 ratio and side edge material. It must contain no logo, label, vent, holes, feet, rails, seams, fasteners, ports, or protrusions not proven from adjacent faces, and it must not change any verified side silhouette. Final status can be no better than `PASS_WITH_BOTTOM_FALLBACK`.

## Official 3D/CAD/viewer search

Current official-domain searches covered MX204 plus `3D`, `CAD`, `GLB`, `glTF`, `STEP`, `OBJ`, `FBX`, `AR`, `interactive viewer`, and `Visio`. The dynamic product/media pages were inspected and expose only raster photographs and documentation. No public exact-PID official 3D/CAD/GLB/GLTF or interactive-model network asset was found. `source/optional-3d/` is intentionally empty; no access control, login, private API, or paywall was bypassed.
