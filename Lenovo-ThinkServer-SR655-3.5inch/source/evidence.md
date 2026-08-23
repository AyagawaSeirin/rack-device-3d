# Evidence and dimension ledger

Access date for web sources: 2026-08-23 (Asia/Singapore).

## PDF workflow fallback

The environment did not expose a `pdf` skill and did not include `pdftotext`, `pdftoppm` or `pdfinfo`. The explicit fallback was used:

- downloaded official PDFs unchanged;
- extracted every page's text with locally installed `pypdf` under `/tmp/sr655-python-libs`;
- rendered relevant pages at 3.5x scale with locally installed PyMuPDF;
- inspected every rendered page at original/high detail with the image-viewing tool;
- retained the extracted text beside each PDF and the inspected page renders under `source/pdf-pages/`.

No PDF evidence was accepted from filenames or extracted text alone.

## User screenshot inspection

Local source: `source/originals/user-screenshot-row-list.png`

SHA-256: `8ee991db9af36f19c3c3bff7a4c73dcd8df47f8a844e8e6febf5601dda095be1`

The fourth readable device row proves a label of “Lenovo / ThinkServer / SR655 / 3.5-inch”, a 12-bay LFF front in a 3x4 carrier arrangement, left and right front latches, a right-side front I/O module, the 8-PCIe-slot rear silhouette, two hot-swap PSU faces, lower rear I/O and no rear drives. Its 1042x1388 whole-table resolution leaves the device thumbnails too small to prove machine type, OCP adapter subtype, PSU wattage text, exact labels, side/top/bottom features, or whether internal media are present. It is a configuration clue and target-lock source, not a final texture.

## Official identity and configuration sources

### Lenovo Docs — SR655 types 7Y00/7Z01

URL: https://pubs.lenovo.com/sr655/

Authority: official.

Proves: original-generation ThinkSystem SR655, types 7Y00 and 7Z01, single-socket 2U identity; excludes SR655 V3.

### DCSC dynamic product page

URL: https://dcsc.lenovo.com/#/categories/STG%40Servers%40Rack%20Server%40ThinkSystem%20SR655

Authority/source class: official dynamic configurator.

Browser inspection: opened with an isolated Playwright session; selected Servers > Rack Server > ThinkSystem SR655. The page identifies the original SR655, exposes 7Z01CTO1WW, and links the official 3D catalog. No login or restricted endpoint was used.

Proves: official product naming, original generation, CTO base and public 3D viewer route.

### Lenovo Press Product Guide LP1161

HTML: https://lenovopress.lenovo.com/lp1161-thinksystem-sr655-server

PDF: https://lenovopress.lenovo.com/lp1161.pdf

Local original: `source/originals/lp1161-thinksystem-sr655-product-guide.pdf`

SHA-256: `9b76f2971e7eb4def7aa4cd062a46e9da367c8c8462aaea754084f37ad2b2c5b`

Inspected pages:

- PDF page 5 / Figure 3: exact 8-PCIe-slot rear, no rear drives, two-port OCP 3.0, lower I/O order, and two visibly labeled 750W AC PSUs.
- PDF page 27 / Figure 6: 12x3.5 SAS/SATA front configuration and AUR9 12-bay backplane; distinguishes it from 8+4 AnyBay AUR8.
- PDF page 81 / Table 70: supported AC and DC PSU choices; two identical PSUs; 7N67A00883/B6XT 750W Platinum; all supported AC PSUs use C14, while -48V DC uses a different Positronic connector.
- PDF page 97 / Table 79 and Figure 15: detailed width, height, front projection and rear depth inclusion rules.

Visual origin: official product render/photo and technical diagram.

### Setup Guide

URL: https://pubs.lenovo.com/sr655/SR655_setup_guide.pdf

Local original: `source/originals/SR655-setup-guide.pdf`

SHA-256: `312fad6ee0f961aa63abe58fd197445dacc88da67cd8eaddacb047bae12968d7`

Inspected pages: PDF pages 21, 23 and 28. They prove the front component families and the exact 8-slot rear callout numbering. The setup guide line art is geometry evidence, not color/style evidence.

### Quick Start

URL: https://pubs.lenovo.com/sr655/sr655_quick_start.pdf

Local original: `source/originals/SR655-quick-start.pdf`

SHA-256: `046e2707a56843848d7dfb960e9d3e3027a9c22311a9525b4df5658777674cd9`

Inspected pages: 1-2. They prove 12x3.5 front, 8-slot rear and the 482.0 x 86.5 x 764.7 mm overall envelope with latches and without a security bezel.

## Official interactive 3D viewer

Viewer page: https://lenovopress.lenovo.com/3dtours/sr655/

Lenovo Press document page: https://lenovopress.lenovo.com/lp1183-3d-tour-thinksystem-sr655

DCSC legacy link observed: https://www.lenovofiles.com/3dtours/products/superblaze/sr655/index.html (DNS no longer resolves; not used for downloads).

Authority/source class: official public interactive viewer.

Browser findings:

- the viewer is explicitly titled ThinkSystem SR655 and marked withdrawn;
- the PCIe-rich section states “12x 3.5-inch chassis” and “Up to 8x PCIe slots”;
- ordinary public network requests reveal `model_gl/hierarchy.xml`, 1,086 public mesh blocks, 59 textures and public Draco/runtime resources;
- no authentication, private API, access-control bypass or paid resource was used;
- the official model was used only as evidence and optional backup, never as the main-build mesh.

Exact exterior views captured from the public viewer after selecting the 12x3.5 chassis and PCIe-rich rear and stopping auto-rotation:

- `qa/reference/official-viewer-front-full.png`
- `qa/reference/official-viewer-rear-8pcie-full.png`
- `qa/reference/official-viewer-left-full.png`
- `qa/reference/official-viewer-right-full.png`
- `qa/reference/official-viewer-top-full.png`
- `qa/reference/official-viewer-bottom-full.png`
- `qa/reference/official-viewer-front-right-full.png`
- `qa/reference/official-viewer-rear-right-full.png`

These prove exact left/right asymmetry, top vent/latch/stampings, the exact plain bottom seam pattern, silhouette, rear PSU count and three-quarter relief. They are official renders, not real photographs.

## Optional official 3D backup

Directory: `source/optional-3d/viewer-public/`

Portable archive: `source/optional-3d/Lenovo-ThinkSystem-SR655-official-viewer-original-files.tar.gz`

Archive bytes: 16,590,938

Archive SHA-256: `2d99c8fe4bc86f0ed28575421e76630a356cb69360e1dcb09b44c2c81af24a3e`

Unpacked public files: 1,170 files, 39,986,840 bytes including checksum manifest.

Format: InfinityRT public WebGL viewer package; XML hierarchy, RAW/Draco mesh blocks, JPG/PNG textures, JavaScript and WASM runtime. It is not GLB/GLTF.

License/terms clue: viewer and Lenovo Press page display Lenovo copyright / “All rights reserved”; no public model-download or redistribution license was found. Files are retained for internal evidence/backup exactly as served. The archive is only a deterministic container around the unchanged public files.

## Third-party exact-model real photography

### eBay item 206238343567

URL: https://www.ebay.com/itm/206238343567

Claimed configuration: Lenovo SR655 12x3.5, EPYC 7502, AC PSU, 10G NIC.

Inspected unchanged files:

- `source/third-party/ebay-206238343567-1.jpg` — multiple exact SR655 12xLFF units; complete front carrier material, red accents, latches and top edge; seller plastic/tape and stacked devices are limitations.
- `source/third-party/ebay-206238343567-2.jpg` — exact internal chassis; six hot-swap fans and single-socket board; not an exterior face texture.
- `source/third-party/ebay-206238343567-3.jpg` — exact closed top cover, factory service label, latch, vent, stampings and sheet-metal grain; straight elevated view; strongest top real-photo source.
- `source/third-party/ebay-206238343567-4.jpg` — exact 8-slot rear and lower I/O material; only one 1100W AC PSU is installed, so it is material/style evidence only and cannot define the requested two-PSU rear configuration.

Cross-check: front, top, I/O and slot geometry match the official viewer, product guide and setup guide. Seller plastic, inventory labels, stacked neighboring units and missing second PSU are excluded through imagegen prompts.

### Other eBay listings

URLs:

- https://www.ebay.com/itm/365062520652
- https://www.ebay.com/itm/336575181717
- https://www.ebay.com/itm/127799443104

These current listings independently claim original SR655 12x3.5 configurations and 1100W/2x1100W AC variants. Their galleries reuse some of the same seller photography, so they corroborate provenance and configuration availability but are not counted as independent photographic views.

## Dimension ledger

body_width_mm: 444.6 (Quick Start); 445 rounded (Product Guide)

overall_width_mm: 482.0 to outside of front rack latches/EIA flanges

height_mm: 86.5 (Quick Start); 87 rounded (Product Guide)

body_depth_mm: 730 from front rack-flange mating surface to rearmost body/PSU-handle feature

overall_depth_mm: 764.7 (Quick Start); 764 rounded (Product Guide)

front_projection_mm: 34 from forwardmost front feature to rack-flange mating surface

rear_io_surface_from_flange_mm: 698

rear_projection_to_body_or_psu_handle_mm: 730

rack_ear_left_extension_mm: approximately 18.7 from 444.6 body width to 482 overall span, anchored symmetrically to official front views

rack_ear_right_extension_mm: approximately 18.7 from 444.6 body width to 482 overall span, anchored symmetrically to official front views

published_dimension_includes: Quick Start depth includes front rack latches and excludes the optional security bezel; Product Guide detailed depth separates front projection and rear body/PSU-handle extent. Width 482 includes front latches/EIA flanges; 444.6/445 is the chassis body.

model_bounds_target_mm: 482.0 W x 86.5 H x 764.7 D

tolerance: +/- 1.0 mm on overall exported bounds; small relief positions derived from the official viewer and photos within visual comparison tolerance

## Bottom status

The bottom is not a fallback. The exact-model official interactive viewer exposes a complete underside with a plain opaque galvanized plate and two long stamped seam paths. Bottom production mode is `MULTI_REFERENCE_RECONSTRUCTION`, not `GENERIC_BOTTOM_FALLBACK`.

## Stop-condition review

- Exact PID/generation: verified.
- 12x3.5 physical variant: verified.
- Front/rear pairing: verified by user row, official Figure 3 and official viewer PCIe-rich text.
- AC PSU quantity/wattage/inlet: verified as two 750W AC/C14 modules.
- Front/rear/left/right/top evidence: verified.
- Bottom evidence: verified from exact official viewer.
- Remaining non-bottom evidence gaps: none.
