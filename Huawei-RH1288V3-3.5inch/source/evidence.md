# Evidence ledger, source matrix, search log, and inclusion rules

Access date: 2026-08-23

## Exact target and screenshot row

The tenth readable equipment row is `Huawei RH1288V3/3.5-inch`. The exact delivery subject is a complete Huawei FusionServer RH1288 V3, nameplate model H12M-03, generation V3, 1U, with the four-bay 3.5-inch/LFF front. It is not RH1288H, RH2288/RH2288H, V5 or the 2.5-inch/SFF/NVMe front.

The screenshot front has four equal LFF carrier faces in one row, Huawei branding on the left ear, RH1288 V3/Intel marks on the right ear, the label slot and operator I/O in the documented 4-bay positions. The screenshot rear has four adjacent service RJ45 ports, two PCIe blank regions, management/USB/VGA/serial I/O and two AC PSU modules. This rear configuration selects the four-GE visible face, not the two-GE or 10GE/IB alternatives.

## Official Huawei sources

### Product support and user guide

- Product support: https://support.huawei.com/enterprise/en/intelligent-servers/rh1288-v3-pid-9901873
- Exact guide: `RH1288 V3 Server V100R003 User Guide`, Issue 45, 2023-10-30.
- Public indexed PDF mirror: https://device.report/m/7009a59d0542b27d0a93809307e88a251b2cc3ea1245bace9872a925196f6af3.pdf
- Proves: H12M-03; 1U; separate 4x3.5-inch and 8x2.5-inch fronts; slots 0-3 for the LFF face; rear I/O order; FlexIO choices; full-height and half-height PCIe positions; AC/DC PSU options; five fan modules; 436 x 748 x 43 mm for the 3.5-inch chassis.
- Access limitation: Huawei currently requires login for the full Issue 45 download, and the public mirror presents a Cloudflare challenge to direct raw-PDF download in this environment. Indexed PDF text and page references were used. No challenge or access control was bypassed.

### Huawei FusionServer RH1288 V3 White Paper, Issue 03

- URL: https://katalog.vector.net/wp-content/uploads/import/Huawei%20FusionServer%20RH8100%20V3%20White%20Paper.pdf
- Local unchanged PDF: `source/originals/Huawei-FusionServer-RH1288-V3-White-Paper-Issue03.pdf`
- The upstream filename incorrectly says RH8100 V3; the PDF title, every page header and content identify `Huawei FusionServer RH1288 V3 White Paper`, Issue 03, 2016-05-12.
- Text extraction: `source/pdf-pages/Huawei-FusionServer-RH1288-V3-White-Paper-Issue03.txt`.
- Inspected renders: physical PDF pages 11, 12, 13, 14, 22 and 77.
- Key figures: Figure 4-3 4-bay front; Figure 4-4/4-5 alternate 10GE rear faces; Figure 4-6 four-GE rear face; Figure 4-8 chassis/PSU/fan/backplane structure.
- Proves: exact 4-LFF front feature order; the selected four-GE rear topology; two PCIe blanks; two PSUs; five hot-swap fan modules; three PCIe capability; four front 3.5-inch SAS/SATA drives.

### Huawei RH1288 V3 rack-server datasheet

- URL: https://www.router-switch.com/pdf2html/pdf/huawei-rh1288-v3-rack-server-datasheet.pdf
- Local unchanged PDF: `source/originals/Huawei-RH1288-V3-Rack-Server-datasheet.pdf`
- Text extraction: `source/pdf-pages/Huawei-RH1288-V3-Rack-Server-datasheet.txt`
- Inspected renders: all five pages.
- Proves: standard 1U; three front configurations including 4-disk LFF; four 3.5-inch SAS/SATA disks; up to three PCIe slots; five N+1 hot-swap fans; two 1+1 hot-swap PSUs; dimensions 436 x 748 x 43 mm for LFF and 436 x 708 x 43 mm for SFF.
- Figure 2-1 is the clean four-LFF elevation. Figure 3 is the selected four-GE rear layout with dual PSUs.

### Huawei official product gallery

- Gallery: https://info.support.huawei.com/computing/tools/gallery/enterprise/intelligent-server/detail?currentProduct=37&lang=en
- API record: `RH1288 V3 Rack Server`, update date 2025-08-14.
- Direct JPEGs: `Huawei-product-gallery-RH1288-V3_01.jpg`, `_02.jpg`.
- Original official archive: `Huawei-product-gallery-RH1288-V3-official-download-all.zip`, SHA-256 `013c4c967456d4bb2eb96d3008503a9f17be0eb06a3c04fb7cd3f93d8460d948`.
- Archive contents: the same two views as 720p and 1080p PNGs.
- Important exclusion: both official gallery photos show the 8x2.5-inch/SFF front, and the rear photo shows a two-port FlexIO face. They are excluded from LFF front and selected four-GE rear identity. They remain supporting same-generation evidence for photographic material, top-cover construction, physical left/right side asymmetry and PSU geometry.

### Huawei hardware-replacement multimedia

- Document: https://support.huawei.com/enterprise/zh/doc/EDOC1000091057
- Local unchanged MP4s: official parts `o002`, `o003`, `o006`, `o007`, `o008`, `o00a`, `o00b`, `o00h`.
- Direct public pattern: `https://download.huawei.com/edownload/e/download.do?actionFlag=download&mid=SUPE_DOC&nid=EDOC1000091057&partNo=<PART>&play=1&_t=20180104103157000`.
- Inspected contact sheets under `qa/reference/video-frames/`.
- Proves: exact generation shell and side/rail construction; AC PSU removal and module shape; five fan positions; riser and PCIe construction; FlexIO card position.
- Limitation: the filmed server uses the 8-SFF front and two-GE rear. These videos are configuration-support evidence only, not LFF front or four-GE rear primary sources.

## Exact 4-LFF real photography

### Rozetka listing 596556760

- Page: https://rozetka.com.ua/ua/596556760/p596556760/
- Public product API: https://product-api.rozetka.com.ua/v4/goods/get-main?front-type=xl&country=UA&lang=ua&goodsId=596556760
- Preserved API JSON: `source/third-party/rozetka-596556760-product-api.json`.
- Fifteen original images preserved as `source/third-party/rozetka-596556760-*.jpg`; all were inspected at original detail.
- API identity: `Huawei RH1288 V3 4LFF 1U`, two 460 W Platinum PSUs, used grade.
- Proves: real 4-LFF carrier face; H12M-03/RH1288 V3 marks; exact top cover, labels, latch, vent rows, seams, 748 mm LFF shell; oblique side edges; open-chassis five-fan arrangement; two Delta DPS-460DB-1 A 460 W AC PSUs, Huawei P/N 02130957.
- Rear limitation: this photographed unit carries a two-GE FlexIO face. It is excluded from rear port identity and used only for metal/PSU realism.
- Seller changes excluded: NL SAS drive labels, inventory tape `2`, cable straps around PSU handles, cables and room background.

### Rozetka listings 596449957 and 595931176

- Pages: https://rozetka.com.ua/ua/596449957/p596449957/ and https://rozetka.com.ua/ua/595931176/p595931176/
- Public API JSON and 15 original photos per listing are preserved in matching directories.
- These are independent listings of the same exact 4-LFF platform and repeat the same source photo sequence with separately encoded originals. Every file was inspected.
- They cross-check the front, top, open chassis, five-fan row and 460 W AC PSU facts. They add no bottom view and do not change the selected four-GE rear.

### Other 4-LFF front sources

- Carrier One exact 4LFF page: https://store.carrierone.com/us/configure/huawei-rh1288-v3-4lff-new
- BS-OPT 4HDD page: https://bs-opt.ru/servers/stoechnye-servery/huawei/27513a0d-8903-11e8-80e1-002655dc0a1d/
- Both provide exact four-LFF front/top references. Carrier One's other gallery images are family/SFF material and are not treated as 4LFF configuration proof.

## Selected rear cross-checks

- LNC exact RH1288 V3 four-GE rear: https://www.lnc.ru/catalog/huawei/rack/huawei-fusionserver-rh1288-v3
- Local primary: `source/third-party/lnc-RH1288-V3-4GE-rear.jpg`, SHA-256 `0f75651dd26bd24abc4d1eb9716576dd319dbbb357755b32bf6f463a30e56b07`.
- QGserver independent copy: https://www.qgserver.com/fusionserver-rh1288-v3-is-a-standard-1u-2-socket-rack-server315
- The LNC/QG image, user row and Huawei Figure 4-6 agree on four GE ports, management RJ45, two USB 3.0, VGA, serial, two PCIe blanks and dual AC PSUs.

## Configuration freeze and inclusion rules

- Front: four factory LFF carriers installed and closed. Internal disks are not inferred; seller drive labels are removed.
- Rear FlexIO: SM212-visible four GE. The exact internal SM210 versus SM212 revision is not visually distinguishable, but SM212 is tied to H12M-03 package evidence and is the frozen board option.
- Rear PCIe: one full-height and one half-height position, both factory-perforated blanks. No added NIC/HBA bracket.
- PSU: two 460 W Platinum AC hot-swap modules, 1+1, same exterior form and lime-green release details; no DC/HVDC inlet and no mixed PSU type.
- Fans: five internal hot-swap modules in N+1. They do not become exterior openings in the closed model.
- Rack hardware: front ears only. A rear view of the front ears in perspective never creates rear-ear geometry.
- Published LFF chassis dimensions are 436 x 748 x 43 mm. Front ears are separate and target the nominal 482.6 mm rack span. No 708 mm SFF scaling is used.

## Six-face evidence status

- Front: `SOURCE_LOCKED_GENERATION` from a direct exact 4LFF real photograph, supported by Huawei Figure 4-3 and the user row.
- Rear: `SOURCE_LOCKED_GENERATION` from the direct four-GE rear photograph, supported by Huawei Figure 4-6 and the user row. Rozetka rear photography is PSU/material-only because it has two GE ports.
- Left: `MULTI_REFERENCE_RECONSTRUCTION`; exact 4LFF front/top/rear obliques and open-shell views jointly prove the 748 mm silhouette and side edges, while Huawei exact-model official photos prove the non-mirrored generation-specific side landmarks.
- Right: `MULTI_REFERENCE_RECONSTRUCTION`; exact 4LFF rear/top/right oblique directly reveals the right edge, supplemented by the official RH1288 V3 right-side photo and exact 4LFF open-shell views.
- Top: `MULTI_REFERENCE_RECONSTRUCTION`; three exact 4LFF real angles jointly prove the entire cover, labels, vent rows, latch and seams.
- Bottom: `GENERIC_BOTTOM_FALLBACK` after search exhaustion.

## Bottom fallback search log

Searches covered Huawei support, Issue 45, the whitepaper, the datasheet, current official gallery, retired official 3D viewer, official hardware videos, English/Russian/Ukrainian/Chinese queries for `bottom`, `underside`, `底部`, `底面`, exact H12M-03/4LFF reseller and used listings, three Rozetka listings with 45 original photographs, image search, teardown and same-family 1U references. No exact RH1288 V3 underside photograph or mechanical bottom drawing was found.

The inspected fallback is a Dell PowerEdge R610 underside photograph:

https://psauction.com/item/view/487098/dell-poweredge-r610-rackserver-med-raid

It supplies only neutral galvanized material and folded-edge photographic character. Its label, vent, openings, feet, holes and Dell-specific structure are forbidden. The generated bottom is a conservative opaque 436:748 sheet with no unsupported identifier and cannot alter the verified side silhouette. Final status is `PASS_WITH_BOTTOM_FALLBACK` if all other gates pass.

## Official 3D search

The official gallery API exposes the historic viewer URL:

`https://info.support.huawei.com/computing/server3D/res/server/rh1288v3/index.html?lang=en`

The route now returns HTTP 302 to Huawei's 3D-service migration/maintenance page. The archived official index is preserved under `source/optional-3d/`; it references `tree.json` and `./res/model/`, but public model payloads now redirect and were not present in the public archive. No current public raw GLB/glTF/OBJ/FBX/STEP/CAD file was discoverable. The exact official gallery ZIP was downloaded unchanged and contains only SFF PNG photos. See `source/optional-3d/README.md`.

## PDF workflow note

No dedicated PDF skill/tool is available in this session. The documented fallback was used: Ghostscript text extraction, high-resolution page rendering and original-detail inspection with the image viewer. All locally rendered pages named above were inspected before generation.
