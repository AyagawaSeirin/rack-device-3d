# Evidence, source matrix and dimension ledger

Access date: 2026-08-23 (Asia/Singapore)

## Frozen delivery subject

One complete Huawei FusionServer RH2288 V3 / H22M-03 2U server with the 12-common-3.5-inch LFF non-NVMe front, no security bezel, no rear disk module, blank expansion covers, SM211 two-GE flexible NIC, the documented management/console group, and two identical 460 W GOLD AC hot-swap PSUs stacked vertically on the same rear side.

The user's row-6 table front is accepted only as a 12-LFF variant clue. The row-6 table rear is a mismatched device with split PSUs and is forbidden as target evidence by explicit user authorization. No imagegen call, geometry decision or comparison may use that thumbnail as the rear target.

## Official Huawei support page

- URL: https://support.huawei.com/enterprise/en/intelligent-servers/rh2288-v3-pid-9901877
- authority/source class: official dynamic support page
- rendered-browser findings: the page names `RH2288 V3`, states that the nameplate model is `H22M-03`, describes it as a 2U dual-socket server, exposes documentation/multimedia/tools tabs and links the official visual tools.
- current RH2288 V3 User Guide 44 is marked available only to customer or partner accounts. No authentication or access control was bypassed.
- the official Multimedia tab contains hardware installation video material but no downloadable exact mesh.

## Huawei Computing Products Visuals: exact official entry

- detail page: https://info.support.huawei.com/computing/tools/gallery/enterprise/intelligent-server/detail?currentProduct=38&name=RH2288+V3+Rack+Server
- API: https://info.support.huawei.com/computing/infogateway/gallery/v1/pic/pics?id=38&lang=en
- local API record: `source/optional-3d/official-gallery-api.json`
- official image 1: `source/originals/huawei-official-rh2288-v3-01.jpg`
- image 1 SHA-256: `2c38632f611f69469442e7682e06d69ef79817aaa00010d4cf8a0094578bf75a`
- official image 2: `source/originals/huawei-official-rh2288-v3-02.jpg`
- image 2 SHA-256: `8cc66c4522285a0e6528b17f91563a502f7841ff1ba2dbdd5cc34554b7e084ef`
- inspection: both are 1280×720 official renders and were inspected at original detail. Image 1 proves the 12-LFF front, top cover and one side shell. Image 2 proves the opposite side/top/rear shell and the stacked-PSU architecture.
- configuration limitation: image 2 has a rear disk module and four-port flexible NIC. Those are a different legal RH2288 V3 rear option. Only shell/material/side facts are reused; rear disks and the four-port NIC are forbidden in this no-rear-disk/SM211 build.
- official 3D result: the exact API entry returns `threeUrl: null`. The current official Interactive Product Display Intelligent Servers route returns no data, and the published old-version hostname did not resolve. No exact official GLB/glTF/CAD mesh could be downloaded.

## Official Huawei data sheet

- URL: https://a.storyblok.com/f/283550/11994287b0/huawei_fusionserver_rh2288_v3_data_sheet.pdf
- local unchanged original: `source/originals/huawei-fusionserver-rh2288-v3-datasheet.pdf`
- original SHA-256: `8d65c314723ee9751217b80bc481afd1bd99a33637174926c889ca7d3cda2ca3`
- source class: Huawei-branded official data sheet on a public mirror
- PDF-skill availability: unavailable in this runtime. The preserved original was text-extracted with Ghostscript and both pages were rendered at 200 dpi; the two page renders were inspected at original detail.
- text: `source/pdf-pages/datasheet.txt`
- page 1 render: `source/pdf-pages/datasheet-p001.png`, SHA-256 `314f684a597ffb066b2f6dfb47405d7b4a40b0bb1e326b6840c17f420e85646e`
- page 2 render: `source/pdf-pages/datasheet-p002.png`, SHA-256 `fa121833b358f1387bea621ca5bd4a1e5ff171e7c950fe9402bf3964e21bd94f`
- proves: 2U; 12-front-3.5-inch SAS/SATA option; two hot-swap PSUs; two-or-four GE NIC options; maximum six PCIe slots; 447 × 748 × 86.1 mm for the 3.5-inch model.

## Huawei RH2288 V3 guide/white-paper text evidence

- official support document identity: RH2288 V3 Server V100R003 User Guide 44 (guest-restricted on the current official site).
- public text mirrors used without bypassing access controls:
  - https://pdfcoffee.com/user-manual-rh2288-v3-pdf-free.html
  - https://device.report/m/6268d2a6d387f2527a75d4cef1d45f05a974b0cebb2da70599832f09eb42f0ce.pdf
- device.report PDF was text-indexed by the web retrieval service but its file endpoint returned a Cloudflare 403 to direct/browser download; it is not claimed as a preserved local original.
- proves in text: the 12-front-disk figure; rear component order; PSU1/PSU2; I/O modules; onboard slots 4/5; flexible NIC; two USB 3.0/Mgmt/VGA/serial; the rule that a no-rear-disk configuration supports the standard I/O layout; SM211 two-GE versus SM212 four-GE options; identical PSU BOM requirement.

## Exact 12-LFF front color evidence

### Router-switch product photograph

- page: https://www.router-switch.com/huawei-rh2288-v3-e5-2620-v4-16gb-ddr4-600gb-sas-sr130-460w.html
- image: https://media.router-switch.com/media/catalog/product/cache/e314645ec1c2b12980a7d398d456075b/h/u/huawei-rh2288-server.jpg
- local: `source/third-party/router-switch-12lff-front.jpg`
- SHA-256: `01edeb6b3785a23854ea8cb832485e505aff83dc02ec17defc02857669a52573`
- classification: real exact-model 12-LFF product photograph, near-front with top visible; primary real style reference for the front multi-reference reconstruction.
- proves: 3×4 carrier structure, black honeycomb, lime accents, left Huawei control ear, right RH2288 V3 ear and no security bezel.

### Ruten/Alibaba exact used-unit photographs

- page: https://www.ruten.com.tw/item/22632335258685/
- the current rendered page still publicly loads the retained `img.alicdn.com/imgextra/...` originals.
- local originals: `source/third-party/ruten/content-3` through `content-24`.
- complete original-detail classification: `source/ruten-image-audit.csv`.
- title limitation: the seller title says RH2288H V3, but exact photographed content shows the RH2288 V3 front badge and H22M-03 model text. Seller title metadata is not used as identity authority.
- front/top exterior evidence: `content-3/4/5/6/7/8/11`.
- correct rear evidence: `content-15/22/23/24`.
- explicit correction: `content-17` is an internal motherboard overview and `content-21` is a motherboard connector close-up. Neither is rear evidence.
- identity-label correction: `content-10` is a Huawei qualification card close-up, not the H22M-03 nameplate. H22M-03 text is visible in the top-label area of the exterior set, most clearly in `content-8`.
- seller overlays, capacity stickers, detached parts, annotations and non-factory surroundings are excluded by imagegen prompts; genuine metal/plastic grain, wear and exterior structure remain binding.

## Exact no-rear-disk rear color evidence

### ZOL straight rear photograph

- page: https://server.zol.com.cn/726/7268120.html
- image: https://img2.zol.com.cn/product/146/150/cejpY66MME9Z2.jpg
- local: `source/third-party/zol-rh2288-v3-rear.jpg`
- SHA-256: `ef0ab9535cd1809badc3658af8986bc57fe57693607df16e054b223934a30d9f`
- classification: real exact RH2288 V3 straight-rear product photograph; watermark lies outside the equipment.
- proves: no rear disks; SM211 two-RJ45 flexible NIC; blank I/O module 2, onboard slot 4/5 and I/O module 1 covers; USB/Mgmt/VGA/serial group; two vertically stacked PSUs on one side; no rear ears.
- Ruten `content-15/22/23/24` independently cross-check the same installed rear assembly and provide real used-unit material/relief/cord-loop detail.

## Left/right/top evidence

- Both official gallery images are exact 12-LFF RH2288 V3 catalog views and jointly expose both side shells, top cover, rail lips, vents, stamped bosses, fasteners, body length and end relationships.
- Ruten `content-3/4/7/22/23` are exact 12-LFF real photographs that cross-check color/material, top cover/latch/vent/seam, rear PSU relief and visible side edges.
- no direct straight-on real side photograph exists, so both sides are `MULTI_REFERENCE_RECONSTRUCTION` and must remain distinct.
- QG `qg-2/3/4` are retained only as rejected leads because the QG gallery mixes a rear with a side-by-side PSU layout. `qg-5` is explicitly incompatible with the target. No QG geometry is in a final source lock.

## Rejected and exclusion evidence

- `source/third-party/rejected-mismatched/suning-*`: gallery front is 8-SFF/other variants rather than the requested 12-LFF configuration.
- `source/third-party/rejected-mismatched/rh2288h-v3-lff.jpg`: RH2288H V3/H22H-03 exclusion example.
- user row-6 rear thumbnail: split-PSU non-H22M-03 table mismatch.
- Huawei official gallery image 2 rear option: exact RH2288 V3 but incompatible rear-disk/four-port configuration; shell-only evidence.
- QG rear `qg-5`: incompatible side-by-side PSU layout.
- Ruten `content-12/13/14/17/18/19/20/21`: internal views, not exterior face evidence.
- all prior AI-generated faces, prepared views, preview renders and any prior GLB: defect examples only, never primary evidence.

## Dimension ledger

| subject | body/overall width mm | height mm | body depth mm | protrusions | inclusion notes | source |
|---|---:|---:|---:|---|---|---|
| H22M-03 12-LFF chassis body | 447 | 86.1 | 748 | none in published row | Huawei states product W×D×H for 3.5-inch model; rack span/cord loops not itemized | official data sheet |
| front mounting span | 482.6 | 86.1 | n/a | front control ears and carrier relief | standard 19-inch span; ears modeled separately from 447 mm body | 19-inch rack standard + official/Ruten photos |
| front carriers/ear relief | within 482.6 width | within 86.1 height | measured from source proportions | shallow positive relief | recorded separately in model generator and QA | official/Ruten photos |
| rear PSU cord-retainer/fan relief | within 447 body width | within 86.1 height | extends beyond rear plane | separately measured/modelled | published 748 mm inclusion is not explicit; report body and final world bounds separately | ZOL/Ruten photos |

Normalized face ratios:

- front: `482.6 : 86.1 = 5.605110...`
- rear body: `447 : 86.1 = 5.191638...`
- left/right: `748 : 86.1 = 8.687573...`
- top/bottom: `447 : 748 = 0.597593...`

## Bottom search and controlled fallback

Searches attempted and recorded:

- official support Documentation/Multimedia/Tools tabs;
- exact Huawei Product Visuals and Interactive Product Display;
- official data sheet and public guide/white-paper text mirrors;
- Ruten complete gallery, ZOL, router-switch, QG, used-equipment/marketplace/auction results;
- English queries for `RH2288 V3 underside`, `bottom`, `H22M-03 bottom chassis`;
- Chinese queries for `华为 RH2288 V3 底部/底板/机箱`;
- same-family/same-vendor 2U underside leads and teardown/video results.

No usable exact RH2288 V3 underside photograph or mechanical drawing was found. `source/third-party/generic-bottom-reference-dell-r610.jpg` was inspected at original detail and is retained only for neutral galvanized-sheet photographic character. None of its vents, labels, holes, ports, feet or PSU structure may transfer. The generated bottom is a conservative opaque 447:748 plate with only exact side-proven edge lips. Final status is therefore `PASS_WITH_BOTTOM_FALLBACK` if every other gate passes.

## Correction and preservation lineage

- The first attempt ended with a tool-level `Bad Request`; its preserved state is under `repair-official-rear/before/`.
- The second attempt also ended incomplete after image generation; it produced no GLB and left a REWORK views audit.
- Before this repair, the entire then-current 211-file/172 MB state was copied to `repair-official-rear/retry-before/` and verified against `_snapshot-manifest.sha256`: 211/211 SHA-256 checks passed.
- This repair supersedes every old source lock that cited the wrong Ruten roles, SM212 four-port rear, or QG mixed-gallery side authority.
