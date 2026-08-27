# Evidence and dimension ledger

Access date for web sources: 2026-08-23 (Asia/Singapore).

## PDF workflow fallback

No `pdf` skill or preinstalled PDF command-line tool was available in this environment. The explicit fallback was used: `pypdf` extracted the complete 228-page hardware-guide text to `source/pdf-text/qfx5110-hardware-guide.txt`; PyMuPDF rendered the relevant pages at 3× scale to `source/pdf-pages/`; every rendered page was then inspected with the image viewer at `detail: original`. This limitation and fallback are part of the evidence record.

Rendered and inspected hardware-guide PDF pages: 15, 24, 25, 27, 28, 29, 31, 41, 44, 48, 49, 51, 55, 56, 57, 74, and 75. Relevant printed pages/figures include the mounting-bracket diagrams, QFX5110-48S identity, hardware-only product table, redundancy, port panel, FRU/management panel, fan system, AFI airflow diagram, AC PSU, AC-AFI PSU ordering table, clearance drawing, and physical dimensions.

## Screenshot inspection

Source: `source/originals/user-screenshot.png`, SHA-256 `8ee991db9af36f19c3c3bff7a4c73dcd8df47f8a844e8e6febf5601dda095be1`.

The first readable device row says Juniper / QFX5110. At original detail it proves a 1U front with 48 small cages in two rows and four larger cages at device-right, plus a rear with one management block, five pale/azure fan modules, and two IEC-style AC PSUs. The light fan handles rule out gold/orange AFO, and IEC inlets rule out DC. The row therefore supports QFX5110-48S-AFI with dual AC. It also shows front mounting ears and empty front transceiver cages. Limitations: it is a small UI thumbnail, does not prove exact side/top/bottom detail, cannot prove small labels, and is not used as a final texture.

## Official sources

### Juniper image library

URL: https://www.juniper.net/us/en/company/images/image-library-logos-and-product-photos/products/qfx5110-48s.html

Authority/source class: official product-photo library. Visual origin: real product photography. The page explicitly labels 2100-pixel front, front-with-top, left, right, AFI AC rear, AFI DC rear, AFO AC rear, and AFO DC rear files. All eight originals were preserved unchanged and inspected at original detail.

- `qfx5110-48s-front-high.jpg`, 554003 bytes, SHA-256 `24ac6ee1ab5ef9b5f122814304729489d4ba2d689fb7e531565faeafc1382acb`: exact empty port panel, material, port counts/order, timing connectors, perforations, numbering. Primary front identity/style reference. No rack ears in the library shot.
- `qfx5110-48s-frontwtop-high.jpg`, 527793 bytes, SHA-256 `27c7e8ff2079570ba699e0b3d7874b241247a78e8e5a07820805cd8fc3942e0f`: exact front plus most of the top, real gray cover material, faint embossed Juniper mark, seams, and proportions. Primary top reconstruction source.
- `qfx5110-48s-left-high.jpg`, 507962 bytes, SHA-256 `8f21c1312fab6a3f94b4e11de0aa2125c19a758546a2e011916eb1a75d9a1530`: exact left-labeled three-quarter photo, side seam/slot/material evidence. Primary left reconstruction source.
- `qfx5110-48s-right-high.jpg`, 519192 bytes, SHA-256 `474907940a73be145c4b4b620ecd44d192c97cd927dd7e563565cba9151bee1f`: exact right-labeled three-quarter photo, side seam/slot/material evidence. Primary right reconstruction source.
- `qfx5110-48s-rear-high-afi-ac.jpg`, 506525 bytes, SHA-256 `08ceacb17ccbc78060f6664907eae5f5d4865f44130ee40f31564bf31ebb7942`: exact AFI AC rear, five blue AIR IN fans, two IEC AC PSUs, management panel and branding. Primary rear identity/style reference.
- AFI DC, AFO AC, and AFO DC official originals were also preserved only as rejected-variant controls; they prove why DC terminal blocks and gold/orange AIR OUT fans are excluded.

### Juniper QFX5110 Switch Hardware Guide

URL: https://www.juniper.net/documentation/us/en/hardware/qfx5110/qfx5110.pdf

Local: `source/originals/qfx5110-hardware-guide.pdf`, 5497497 bytes, SHA-256 `b47b985fde4056039deb89c1231ecffdfd575c431c1b2ad317fde4905f02df02`.

Authority/source class: official installation and maintenance manual; PDF metadata title `QFX5110 Switch Hardware Guide`, created 2026-02-25. It proves:

- QFX5110-48S has 48 SFP+ and four QSFP28 ports and is 1U;
- hardware-only PID `QFX5110-48S-AFI` means AC and Air In (FRUs-to-ports);
- default installed state is two power supplies and five fans;
- fan slots are 0–4 left-to-right, AFI is Juniper Azure Blue and labeled AIR IN;
- AC-AFI PSU model is `JPSU-650W-AC-AFI` and each unit is 650 W;
- the exact FRU management-panel component layout;
- rack-mounting bracket attachment and 19-inch rack compatibility;
- body dimensions and the explicit exclusion of fan/PSU handles from depth.

### Juniper system overview and hardware compatibility tool

- https://www.juniper.net/documentation/us/en/hardware/qfx5110/topics/topic-map/qfx5110-system-overview.html
- https://apps.juniper.net/hct/product/QFX5110/hwspecs

These current official pages cross-check the exact fixed chassis, 1U height, 48×SFP+ + 4×QSFP28 port set, AC/AFI ordering variant, and exact chassis dimensions.

### Dynamic page / public 3D search

The current Juniper QFX5110 product page was opened in a real browser with Playwright and its rendered gallery/requests inspected. It exposes six ordinary product-photo tabs and no `model-viewer`, 3D/AR tab, GLB, glTF, OBJ, FBX, STEP, or STP resource. Search queries also covered the exact PID plus `3D`, `AR`, `GLB`, `glTF`, `CAD`, `STEP`, `OBJ`, and `FBX` on Juniper and the public web. No publicly accessible exact-PID official 3D/CAD file or official interactive 3D viewer was found. Therefore `source/optional-3d/` intentionally contains only a search record, not a substituted model.

## Third-party exact-device photographs

### EveryChina exact QFX5110-48S-AFI gallery

URL: https://switches-networks.sell.everychina.com/p-116654966/showimage.html

Authority/source class: secondary marketplace/used-equipment gallery; visual origin real photographs. Four files were downloaded and inspected. The listing title explicitly claims QFX5110-48S-AFI. The photos cross-check the blue AFI fan set, dual AC rear, top cover/screw lines, and installed short galvanized front ears. One view has optics installed and one has packaging on top, so these images are supporting geometry/rack-hardware sources only, never front texture sources.

### NW工房 exact QFX5110-48S-AFI used listing

URL: https://nwkoubou.jp/SHOP/QFX5110-48S-AFI-2PWR-BK.html

Authority/source class: secondary used-equipment seller; visual origin real 2048×1536 camera photos. The listing states SFP+×48, QSFP28×4, back-to-front airflow, dual power, and no rack hardware included. The three images cross-check the unpopulated front, full top material/seam, five blue AFI fans, two AC PSUs, and real fan-handle relief. The photographed unit has a cracked fan and seller/asset labels; those are excluded.

### eBay exact AFI dual-AC listing

URL: https://www.ebay.com/itm/267628313967

Search index identified an exact `Juniper QFX5110-48S-AFI ... Dual AC` listing with eleven pictures. Browser access returned HTTP 403; no access control was bypassed and no image was used. This is recorded as a search attempt only.

## Dimension ledger

| Field | Value | Inclusion / basis |
|---|---:|---|
| body_width_mm | 440.944 | official HCT, 17.36 in |
| overall_width_mm | 482.600 | 19-inch rack span with installed front ears; official rack standard plus exact-model ear photos |
| height_mm | 43.688 | official HCT, 1.72 in; nominal 1U |
| body_depth_mm | 520.192 | official HCT, 20.48 in |
| overall_depth_mm | 551.992 | 520.192 body + 4.8 front connectors + 27.0 rear handles/retainers; rear value is inside image-derived 24 ± 4 mm tolerance |
| front_projection_mm | 4.8 | gold timing connectors at the port face |
| rear_projection_mm | 27.0 | fan/PSU handles and cord retainers; official depth explicitly excludes handles |
| rack_ear_left_extension_mm | 20.828 | half of 482.600 − 440.944 |
| rack_ear_right_extension_mm | 20.828 | half of 482.600 − 440.944 |
| published_dimension_includes | chassis body; excludes fan and power-supply handles | official hardware guide, printed p.66 / PDF p.75 |

The primary geometry uses exact body dimensions. Only the small rear projection is image-derived; its tolerance is recorded and does not alter the official body scale. Final GLB structural bounds are 482.600 × 43.848 × 551.992 mm; the 0.160 mm height delta is the two 0.08 mm anti-z-fighting face offsets, while the closed chassis body remains exactly 43.688 mm high.

## Bottom search and fallback

Searches covered exact-model official product pages, documentation, image library, dynamic gallery, hardware guide, product videos/teardown terms, exact-PID reseller and marketplace listings, eBay, used-equipment sellers, auction/gallery terms, and Japanese/Chinese queries for underside/bottom/disassembly. Same-family QFX5100 and same-vendor 1U searches also produced no usable underside photograph. Exact bottom identity is therefore unavailable, but every silhouette-affecting body edge is fixed by official front/top/side evidence.

The bottom is locked to `GENERIC_BOTTOM_FALLBACK`: an opaque flat gray sheet-metal underside matching the official 440.944:520.192 ratio, material grain, and folded edge character, with no logo, model label, vents, holes, feet, rails, seams, fasteners, or protrusions. This forces final status `PASS_WITH_BOTTOM_FALLBACK`.

## Source inclusion / exclusion rules

- Preserve all factory Juniper branding and the QFX5110-48S, AIR IN, AFI, port, and control markings established by real sources.
- Exclude seller stickers, QR/serial labels not readable in the primary official photo, cables, optics, rails, packaging, damage, and shadows/backgrounds.
- Do not use the AFI DC or AFO images except as negative variant controls.
- Do not add rear ears; the official rear elevation has none. Front ears are separate geometry based on screenshot plus exact-model real photos.
- No official 3D file is used or substituted because none was publicly found.
