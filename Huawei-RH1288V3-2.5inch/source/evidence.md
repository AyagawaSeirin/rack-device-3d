# Evidence, source matrix, search log, and inclusion rules

Access date: 2026-08-23

## Exact target

The eleventh readable row in the user-provided table is `Huawei RH1288V3/2.5-inch`. It is the Huawei FusionServer RH1288 V3, nameplate model `H12M-03`, not RH1288H V3, not any V5/V6/V7 successor and not the four-bay 3.5-inch chassis.

The official Issue 45 user guide identifies H12M-03 as a 1U two-socket server and lists two 8-bay 2.5-inch backplanes plus a separate 4-bay 3.5-inch backplane. The screenshot, direct front photograph and Huawei Figure 4-1 show eight standard carrier fronts in the exact asymmetric `3 upper / 5 lower` arrangement: three paired columns at left plus two additional lower-row carriers beneath the right service area. The requested visible build uses the ordinary SAS/SATA/SSD carrier appearance, not the NVMe-specific dual-indicator carrier mix.

## Rear configuration freeze

The screenshot rear shows four adjacent service RJ45 ports. Issue 45 identifies the only matching visible FlexIO face as SM210/SM212, both providing four GE electrical ports. The exact H12M-03 8-SFF listing at Khabtelecom identifies SM212 together with two 750 W Platinum AC PSUs. The rear is therefore frozen to:

- SM212-visible four-GE FlexIO face;
- one management RJ45, two USB 3.0, one VGA, one serial port and UID indicator;
- one full-height and one half-height PCIe position with factory perforated blanks;
- two 750 W AC hot-swap PSUs, side-by-side at physical rear right, 1+1 redundancy;
- no DC/HVDC inlet, no rear mounting ears and no alternate 10GE/IB face.

The five hot-swap fan modules described by Huawei remain inside the closed chassis. The two circular fans visible from the rear are PSU fans and are modeled as part of the two PSU modules.

## Official documents and gallery

### Huawei support and Issue 45 user guide

- Support product page: https://support.huawei.com/enterprise/en/intelligent-servers/rh1288-v3-pid-9901873
- Public PDF mirror used for visual/text access: https://device.report/m/7009a59d0542b27d0a93809307e88a251b2cc3ea1245bace9872a925196f6af3.pdf
- Document: `RH1288 V3 Server V100R003 User Guide`, Issue 45, 2023-10-30, 285 pages.
- Proves: H12M-03, 1U, 8-SFF and 4-LFF variant split, ports, SM210/SM212 four-GE topology, PCIe positions, AC PSU options, fan count, 43 x 436 x 708 mm for the 2.5-inch chassis.
- Download limitation: the mirror's raw PDF is protected by a Cloudflare challenge in this environment. No challenge or access control was bypassed. Its indexed PDF text and page references were used, while the locally retained Huawei whitepaper supplies the rendered authoritative figures.

### Huawei whitepaper Issue 03

- Source: https://katalog.vector.net/wp-content/uploads/import/Huawei%20FusionServer%20RH8100%20V3%20White%20Paper.pdf
- Local unchanged PDF: `source/originals/rh1288-v3-white-paper-issue03.pdf`
- Local extracted text: `source/originals/rh1288-v3-white-paper-issue03.txt`
- Relevant inspected pages: `source/pdf-pages/whitepaper-physical-011-front.png`, `whitepaper-physical-013-rear-10ge-electrical.png`, `whitepaper-physical-014-rear-optical-ge.png`, `whitepaper-physical-022-structure.png`, `whitepaper-physical-077-dimensions.png`.
- Proves: Figure 4-1 8-bay front; Figures 4-4 through 4-6 rear options; Figure 4-8 physical structure; Table 9-1 dimensions; two redundant PSUs; five hot-swap fans.
- The upstream filename says RH8100 V3, but the downloaded PDF contents, title, every page header and checksum identify the actual document as Huawei FusionServer RH1288 V3 White Paper Issue 03. The misleading upstream filename is recorded rather than hidden.

### Huawei data sheet

- URL: https://www.nforce.com/files/Huawei%20FusionServer%20RH1288%20V3%20Data%20Sheet.pdf
- Local unchanged PDF: `source/originals/huawei-rh1288-v3-data-sheet.pdf`
- Inspected renders: `source/pdf-pages/data-sheet-p001.png`, `data-sheet-p002.png`.
- Proves: 1U, eight 2.5-inch storage, three PCIe slots maximum, five N+1 fan modules, two redundant hot-swap PSUs and the same 436 x 708 x 43 mm 2.5-inch dimensions.

### Huawei official product gallery

- Page: https://info.support.huawei.com/computing/tools/gallery/enterprise/intelligent-server/detail?currentProduct=37&lang=en
- API record: `RH1288 V3 Rack Server`, directory `RH1288 V3`, update date 2025-08-14.
- Exact direct images: `source/originals/huawei-gallery-rh1288-v3-01.jpg`, `huawei-gallery-rh1288-v3-02.jpg`.
- Original official download-all archive: `source/originals/huawei-gallery-rh1288-v3.zip`, SHA-256 `013c4c967456d4bb2eb96d3008503a9f17be0eb06a3c04fb7cd3f93d8460d948`.
- The archive contains the same two images at 720p and 1080p. It is preserved unchanged.
- Proves exact shell, top, mounting ears, physical right and left side material/landmarks, 8-SFF front and the physical PSU module shape. The official rear photograph carries a two-port optical NIC and is intentionally excluded from the requested rear port identity.

## Third-party exact-device cross-checks

- CarrierOne exact 8-SFF page: https://store.carrierone.com/us/configure/huawei-rh1288-v3-8sff-new — direct straight front plus exact ISO/rear/interior references. The front is the primary binding real photograph.
- LNC exact product page: https://www.lnc.ru/catalog/huawei/rack/huawei-fusionserver-rh1288-v3 — straight four-GE rear photograph, primary rear identity/style reference.
- Khabtelecom H12M-03 package: https://khabtelecom.ru/server-huawei-rh1288-v3-h12m-03/ — specifies 8-SFF, SM212 four-GE FlexIO and 2x750 W Platinum AC; photo matches the official shell.
- QG rear copy: https://www.qgserver.com/fusionserver-rh1288-v3-is-a-standard-1u-2-socket-rack-server315 — independent rear-image cross-check.

## Dimension inclusion rule

Huawei calls 43 x 436 x 708 mm the 2.5-inch `chassis` envelope. The document does not state whether removable pull handles are included. The model therefore keeps the authoritative body ratio and reports visible projections separately rather than silently stretching the body. Front ears target the nominal 482.6 mm 19-inch mounting span and exist only at the front. The GLB audit reports both the published body and final visible bounds.

## Bottom fallback search log

Searches included official Huawei support, the product gallery, the retired exact 3D viewer, the whitepaper, Issue 45 user guide, hardware replacement video index, English and Chinese queries for `bottom`, `underside`, `底部`, `底面`, exact H12M-03 reseller pages, used-equipment listings, teardown pages, image search and same-family 1U searches. No exact RH1288 V3 underside photograph or mechanical bottom drawing was found. The only exact-device images show the top, sides, front, rear or open interior.

The bottom therefore uses `GENERIC_BOTTOM_FALLBACK`. `source/third-party/generic-bottom-dell-r610.jpeg` is inspected only for neutral galvanized sheet-metal texture and folded-edge photographic character. Its label, vents, feet, openings, ports and module arrangement are explicitly forbidden. The generated bottom must be a conservative opaque 436:708 sheet with no unsupported identifying feature, and the final status is `PASS_WITH_BOTTOM_FALLBACK` if all other gates pass.

## Official 3D discovery

The official gallery API returns the exact historic viewer URL:

`https://info.support.huawei.com/computing/server3D/res/server/rh1288v3/index.html?lang=en`

That route previously exposed RH1288 V3 original/exploded/component views. As of the access date it returns an HTTP 302 to Huawei's 3D-service maintenance/migration page; Huawei states the service has been restricted for an upgrade since 2026-01-30. Browser/network inspection found no public direct model file and no downloadable GLB/glTF/OBJ/FBX/STEP/CAD asset. No access control, internal environment or private API was bypassed. The exact official gallery ZIP was downloaded unchanged, but it contains PNG views only. Details are retained in `source/optional-3d/README.md`; no file is misrepresented as an official 3D model.

## PDF workflow note

No dedicated PDF skill/tool is installed in this session. The required fallback was used: Ghostscript text extraction, page rasterization to high-resolution PNG, and original-detail visual inspection with the image viewer. Every relevant local PDF page named above was inspected before generation.

## 2026-08-27 current reverse review

- Reopened Huawei's exact RH1288 V3 product gallery and legacy 3D viewer URL in a real browser. The gallery still identifies `RH1288 V3 Rack Server` and the historic exact viewer route still exists as an indexed Huawei visual source.
- The legacy route now redirects to Huawei's migrated product-3D landing page. That current landing page did not surface RH1288 V3 as a directly retrievable public model, and its public old-version link failed. No downloadable GLB/glTF/OBJ/FBX/STEP/CAD binary was exposed and no access control was bypassed.
- The preserved official gallery ZIP remains the only exact official downloadable visual archive found; it contains PNG product views, not 3D geometry.
- Original-detail re-inspection reconfirmed H12M-03, 1U, eight 2.5-inch carriers in the asymmetric 3-upper/5-lower layout, the SM212-visible four-GE rear, two installed 750 W AC PSUs, front-only ears and the 436 × 43 × 708 mm body.
