# Evidence and dimension ledger

Initial access date: 2026-08-23
Forced-review refresh: 2026-08-24
Rotation-review official refresh: 2026-08-27

## PDF-tool fallback

No dedicated PDF skill was installed in this session. The Huawei PDF evidence was therefore processed with the required local fallback: text extraction, page-by-page raster rendering, and original-resolution visual inspection. Extracted text is retained beside the PDFs under `source/originals/`; inspected page renders and their checksums are under `source/pdf-pages/`. This fallback did not bypass document access control.

## Exact target confirmed

- Huawei official support identifies RH2288 V3 as nameplate model `H22M-03`, a 2U dual-socket rack server.
- Huawei whitepaper Issue 01 Figure 4-4 proves the 24-disk physical front: 24 x 2.5-inch slots numbered 0-23, left USB/Huawei ear, right diagnostics/VGA ear.
- User screenshot row 7 and the independent 24-SFF product photograph match that front.
- Huawei dimensions for a 2.5-inch chassis are 447 x 708 x 86.1 mm (body W x D x H). The 19-inch mounting span is separate from the 447 mm body.
- The 24-disk configuration does not support rear disks according to the Issue 32 user guide. The compatible rear therefore requires the standard I/O/riser layout and both AC PSUs stacked at one rear side.

## Historical rear conflict and user correction

The user screenshot row 7 rear cannot belong to RH2288 V3:

1. The screenshot has one black AC inlet/fan PSU assembly at each rear corner.
2. Huawei whitepaper Figure 4-6, the Issue 32 user-guide description, and two independent exact-model rear images all place both hot-swap PSUs together, stacked vertically at one rear side.
3. The screenshot uses a different expansion-slot and ventilation topology across the top half.
4. AC/DC choice cannot explain this: the physical PSU bay placement and entire rear sheet-metal cutout differ.
5. The official RH2288 V3 configuration matrix does not list a distributed-corner-PSU rear option.

Comparison: `qa/comparisons/rear-identity-conflict.png` (user rear above, compatible RH2288 V3 rear below).

This was an assembly-identity failure, so the initial run correctly stopped before generation. The user later explicitly classified the screenshot rear as a table-image error and authorized the official RH2288 V3 rear. The former BLOCKED records are preserved under `qa/repair-before-user-correction/`. The rejected rear is not an image-generation input and does not define any final feature.

The corrected identity is now VERIFIED: official 24-SFF front, no rear disks, standard RH2288 V3 I/O/PCIe/flexible-NIC arrangement, and two AC PSUs stacked vertically at the same rear side.

## Source records

### Huawei official support product page and image

- URL: https://support.huawei.com/enterprise/en/servers/rh2288-v3-pid-9901877
- Image URL: https://download.huawei.com/mdl/imgDownload/1ec24825533741b8a0e458d081ff371b
- Visual origin: official photograph, exact RH2288 V3, 8-SFF front variant.
- Proves: exact chassis/top material, two-cover seam, center latch, factory labels, front ears and product identity.
- Limitation: not the requested 24-SFF front and does not show an orthographic side/bottom.

### Huawei RH2288 V3 whitepaper Issue 01

- URL: https://www.doit.com.cn/subject/hcc2015/pdf/7.pdf
- Local: `source/originals/rh2288-v3-white-paper-cn-issue01.pdf`
- Visual origin: Huawei technical document.
- Relevant renders: `source/pdf-pages/whitepaper-p14-opaque.png`, `whitepaper-p15-opaque.png`, `whitepaper-p16-opaque.png`, `whitepaper-p20.png`.
- Proves: 24-SFF front, 25-SFF distinction, single official rear topology, ports, PSU placement, physical assembly, 2.5-inch dimensions, 24-disk weight and allowed power types.

### Huawei RH2288 V3 data sheet

- URL: https://www.nforce.com/files/Huawei%20FusionServer%20RH2288%20V3%20Data%20Sheet.pdf
- Local: `source/originals/huawei-rh2288-v3-data-sheet.pdf`
- Visual origin: Huawei data sheet.
- Proves: 2U, 16 DIMMs for base RH2288 V3, dual hot-swap PSUs, dimensions 447 x 708 x 86.1 mm for 2.5-inch chassis.
- Limitation: later summary omits the 24-SFF configuration even though the detailed whitepaper and Issue 32 guide retain it.

### Issue 32 user guide text

- URL: https://pdfcoffee.com/user-manual-rh2288-v3-pdf-free.html
- Official support item is account-restricted; the public mirror exposes the Huawei text but its full PDF download requires reCAPTCHA. No access control was bypassed.
- Proves: H22M-03 identity; six backplane types including 24 and 25; 24-disk configuration slots 0-23; 24-disk configurations do not support rear disks; official rear callout topology.

### Exact 24-SFF front photograph

- URL: https://kitairu.net/images/products/products_879314_bfa2953eae1c32f0bdaa5d235e62da0a.png
- Local: `source/third-party/kitairu-rh2288-v3-24sff.png`
- Visual origin: secondary product photograph/render, exact RH2288 V3 24-SFF claim.
- Proves: requested 24-carrier color/layout and left/right mounting-ear arrangement.

### Exact-model straight rear photograph

- URL: https://img2.zol.com.cn/product/146/150/cejpY66MME9Z2.jpg
- Local: `source/third-party/zol-rh2288-v3-rear.jpg`
- Visual origin: independent exact RH2288 V3 photograph.
- Proves: both PSUs stacked at the same rear side; slot banks, fixed port order and AC physical shape.
- Limitation: retailer watermark outside the product; it is a source only, not a final asset.

### Exact-model right-side and top references

- URL: https://www.qgserver.com/fusionserver-rh2288-v3-2u-rack-server
- Local accepted side/top evidence: `source/third-party/qgserver-rh2288v3-3.jpg`, `qgserver-rh2288v3-5.jpg`.
- Visual origin: secondary exact-model product photography/diagram.
- Proves: right side and top structure/material.

### Huawei V3 chassis left-side references

- URL: https://www.burrillandco.com/pz62d396d-cz5b0326a-used-huawei-fusion-server-rh2288-v3-2u-rack-server-750w.html
- Local: `source/third-party/burrill-rh2288-v3-2.jpg`, `burrill-rh2288-v3-4.jpg`.
- Visual origin: real used-equipment photography.
- Proves: physical-left panel and top on a Huawei 2.5-inch V3 chassis. Huawei comparison documentation records RH2288H differences as CPU/memory/GPU/power/display while both base/H 2.5-inch chassis share 447 x 708 x 86.1 mm bounds.
- Limitation: photographed front badge may be RH2288H V3, so it is supporting side-shell evidence only, never the front/rear identity source.

### Rejected sources

- `source/third-party/zhiding-eddc088f719295cf.jpg`: CPU heatsink only, no exterior proof.
- `source/third-party/mydraw-rh2288h-v3-diagram.png`: useful topology lead for the H variant, not color/style or base RH2288 V3 identity proof.
- `source/third-party/qgserver-rh2288v3-6.jpg`: seller illustration with two PSUs arranged horizontally; conflicts with Huawei Figure 4-6 and the exact ZOL rear photograph, so it is excluded from rear generation and identity proof.
- `source/originals/rh2288-v3-user-guide-issue32.pdf`: one-page public viewer placeholder saying the document cannot load; not the manual.
- `source/originals/fusionserver-rack-v100r003-product-doc-package.bin`: public Huawei link returned an ASCII PGP signature rather than the document package.
- `source/originals/rh2288-v3-white-paper-download-page.html`: anti-bot/download landing HTML, not a PDF.

## Bottom and official-3D search

Exact underside searches covered Huawei official support/documents/multimedia, dynamic Browser inspection, exact-model reseller/used/eBay/marketplace queries, Chinese and English bottom/underside/底部 queries, teardown/review pages and the available image galleries. No exact underside was found. After the user's rear correction resolved the only non-bottom conflict, the delivered bottom uses the documented conservative `GENERIC_BOTTOM_FALLBACK` only.

Searches for `RH2288 V3` plus 3D, CAD, STEP, GLB, glTF, OBJ, FBX, AR, Visio and interactive viewer found no public exact official model. No login, paywall, private API or access control was bypassed.

During the 2026-08-24 forced review, Huawei's current public Product Visuals entry was opened in real Chromium at `currentProduct=38`. The public response identifies `RH2288 V3 Rack Server` and exposes two official images plus an image ZIP, but returns `threeUrl: null` and the page has no `Visualize in 3D` button. This confirms that the neighboring gallery's 3D capability is not available for this exact PID. The captured page is under `qa/forced-review-2026-08-24/evidence-inspection/`; the public response is retained under `source/optional-3d/`.

The same Product Visuals entry and public JSON response were reopened in real Chromium on 2026-08-27. They still identify `RH2288 V3 Rack Server`, retain update date 2025-08-14, expose only the two raster images and ZIP, and return `threeUrl: null`; the current screenshots are under `qa/rotation-review-20260827/after/research/`. No public exact-PID official 3D became available.
