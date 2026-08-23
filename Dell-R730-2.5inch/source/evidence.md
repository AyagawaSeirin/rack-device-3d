# Evidence, provenance and inclusion rules

Access date for all web sources: 2026-08-23 (Asia/Singapore).

## User configuration lock

- Local original: `source/user-lock/row-13-context.png`, SHA-256 `7efb5b4ccf0095fee7977f6a95083306935b9e63a990fd83bb8883fc49fdfeb9`.
- Cropped target row: `source/user-lock/row-13-r730-sff.png`, SHA-256 `5095e7936db12a4b2577c656142b89f554c75f447958ef88bef35fee5dfd9e9a`.
- Visual finding: the target is the bottom row labeled `DELL R730/2.5英寸`, not the preceding R730/3.5 row. The front thumbnail is the no-bezel 16-carrier SFF chassis. The rear thumbnail is Dell's standard R730 rear with three riser groups, four-port NDC and two AC PSUs; it is not an R730xd rear.

## Official documents

1. Dell, *PowerEdge R730 and R730xd Technical Guide*, v1.7.
   - URL: https://i.dell.com/sites/doccontent/shared-content/data-sheets/en/Documents/Dell-PowerEdge-R730-and-R730xd-Technical-Guide-v1-7.pdf
   - Preserved unchanged: `source/originals/Dell-PowerEdge-R730-R730xd-Technical-Guide-v1.7.pdf`
   - SHA-256: `61b2092c53b217377f92b18ab11abe024058891c06fa67a7359c4532c8ebb1eb`
   - Page 13: R730 supports up to sixteen 2.5-inch drives; Figure 2 proves the exact no-bezel 16-SFF front.
   - Page 14: Figure 5 proves the standard R730 rear; Dell separately illustrates R730xd on page 15, so no rear flex drives are allowed.
   - Page 15: exact R730 open-chassis view supports installed fan/riser/PSU placement and confirms six hot-plug cooling fans inside.
   - Page 57: official dimension figure and values Xa 482.4, Xb 444.0, Y 87.3, Za without bezel 18.0, Zb 684.0, Zc 723.0 mm.
   - Page 58: 495/750/1100 W AC options and DC alternatives; the screenshot and selected photos lock two 750 W AC units.
   - Rendered/inspected page files: `source/pdf-pages/technical-guide-p01.png` through `p04.png`, `technical-guide-dimensions-p01.png` and `p02.png`.

2. Dell, *PowerEdge R730 Technical Specification*.
   - URL: https://i.dell.com/sites/doccontent/shared-content/data-sheets/en/documents/dell-poweredge-r730-spec-sheet.pdf
   - Preserved unchanged: `source/originals/Dell-PowerEdge-R730-Spec-Sheet.pdf`
   - SHA-256: `257ffff42ba59cafd3693b7b82cc2d14899b14c6d7e04b0fa0cbfdbc496be48b`
   - Proves 2U, 44.40 x 8.73 x 68.40 cm nominal body dimensions, up to sixteen 2.5-inch drives, seven PCIe slots plus PERC slot, four-port NDC options and AC PSU families.
   - Rendered/inspected pages: `source/pdf-pages/spec-sheet-p01.png`, `spec-sheet-p02.png`.

3. Dell, *PowerEdge R730 Owner's Manual*, Rev. A01 mirror of Dell publication.
   - Canonical Dell URL: https://dl.dell.com/topicspdf/poweredge-r730-dsms_owners-manual_en-us.pdf (public web index readable; direct CDN returned HTTP 403 in this environment).
   - Public mirror: https://2beshop.com/pdf/dell/dell-poweredge-r730.pdf
   - Preserved mirror file: `source/third-party/Dell-PowerEdge-R730-Owners-Manual-mirror.pdf`
   - SHA-256: `22416561f1ff20f367ce8e513c1c21cb25d6f214cc1c869458ea7ac5e3b68c9d`
   - Figure 2 and tables prove the 16-SFF control-area components; Figure 7 and table prove rear component families and order.
   - Rendered/inspected pages: `source/pdf-pages/owners-manual-v2-p01.png` through `p12.png`.

4. Dell live manual topics:
   - 2.5-inch chassis: https://www.dell.com/support/manuals/en-us/poweredge-r730/r730_ompublication/25-inch-hard-drive-chassis?guid=guid-d289ce54-d940-46a4-b22c-f4092f561b4e
   - Back panel: https://www.dell.com/support/manuals/en-us/poweredge-r730/r730_ompublication/back-panel?guid=guid-1dc323f8-8173-4723-8bac-b781cdb7fc9b
   - Riser specification: https://www.dell.com/support/manuals/en-us/poweredge-r730/r730_ompublication/expansion-bus-specifications?guid=guid-25fe748e-f8c6-463e-846d-d489758b0870
   - Chassis dimensions: https://www.dell.com/support/manuals/en-us/poweredge-r730/r730_ompublication/chassis-dimensions?guid=guid-9f567556-3e45-41f8-bece-bd67cb41383e

## Exact-configuration color photography

- ITinStock exact 16-SFF front: https://files.ekmcdn.com/itinstock/images/dell-poweredge-r730-16x-2.5-bay-cto-no-cpu-no-memory-2u-rack-server-58716-p.jpg — real photo, near-straight front; proves Dell/PowerEdge control strip, sixteen carrier style/count, ears and genuine used-material character. Local SHA-256 `d28712fbd5eeac47e1b857f839f1108a200d5402b011223c31de3737df678b7a`.
- Server Superstore exact standard blank rear: https://serversuperstore.com/cdn/shop/files/Pic8back_e578e964-f891-4b8b-bdda-810d7206a725.png?v=1726770370&width=1946 — real photo of R730 rear shared by the documented R730 front variants; all seven riser openings blank, four-port NDC, dual 750 W AC. Local SHA-256 `af0a1c29630dc7cfd29fe87fef28deff8da77c2cf6344ecd58d587405f18f1d9`.
- ITinStock exact 16-SFF top/front angles: `r730-16sff-itinstock-81022-1.jpg` and `-2.jpg`, URL family https://itinstock.com/dell-poweredge-r730-2x-14c-e5-2680v4-24ghz-256gb-ram-16x-25-hdd-bay-2u-server-81022-p.asp — exact 16-SFF chassis; rails in one photo are seller accessories and excluded. They prove the installed top cover, front label band, latch/ribs and cover edge.
- NewServerLife exact 16-SFF rear/top angle: https://newserverlife.com/upload/iblock/aae/r730_16sff-rear.jpeg — real exact-configuration angle; proves rear/top relationship and PSU protrusions; fitted rear card differs and is not used for the locked rear port inventory.
- ITinStock exact R730 direct side: https://files.ekmcdn.com/itinstock/images/trend-micro-dell-poweredge-r730-2x-10c-e5-2650v3-2.3ghz-ram-cto-2u-rack-server-2-83478-p.jpg — direct R730 left-side photograph; front drive module in that listing is a different documented R730 front option and is excluded from front evidence. The R730 side shell, cover tabs, stamped channel and regulatory-label placement are used only after cross-checking the exact 16-SFF top/front/rear sources and Dell's shared R730 chassis dimensions.
- HardwareDirect exact 16-SFF front/top angle: https://hardwaredirect.pl/media/catalog/product/cache/a1bf80813993b64aec2ee5a175f69572/s/e/serwer_dell_r730_16x2_5_z_2xe5_2640_v4_128gb_ram_h730p_2x_480gb_ssd_sata_2_5_4x1gbe_2xpsu_szyny_idrac_8_enterprise_7736_16720_0.jpg — real photo; proves top/front material and cover geometry.

The saved Server Superstore `Pic2Alltrays...png` was visually inspected and rejected: despite the R730 page context, it is visibly a different 1U product image. It is not referenced by any face lock, prompt or model feature.

## Optional official 3D/CAD/AR search

- Dell's official R730 3D Guides list is public and identifies 22 interactive service procedures: https://www.dell.com/support/product-details/en-nz/product/poweredge-r730/resources/3dguides
- Example exact R730 guide: https://www.dell.com/support/resources/en-ca/3dviewer/ic14000r730002401a/how-to-replace-the-power-supply-unit%C2%A0psu-on-a-poweredge-r730
- Browser and direct HTTP inspection both returned Dell/Akamai HTTP 403 in this environment. Search of Dell product resources, media/manual pages and exact-PID queries found no public direct GLB, glTF, STEP, STP, OBJ, FBX or downloadable CAD endpoint. The guide is an interactive service experience, not an exposed downloadable exterior asset.
- The untouched HTTP response and headers are retained under `source/optional-3d/`; no third-party or AI file is mislabeled as official.

## Six-face evidence and mode decision

- Front: direct exact real photograph exists -> `SOURCE_LOCKED_GENERATION`.
- Rear: direct real R730 blank-riser/four-RJ45/dual-AC photograph exists and Dell proves the shared R730 rear -> `SOURCE_LOCKED_GENERATION`.
- Left: direct exact-R730 side photograph exists; variant-specific front content is excluded -> `SOURCE_LOCKED_GENERATION` for the side shell only.
- Right: no usable direct right-side photograph found. Exact 16-SFF front/top and rear/top angles plus direct R730 opposite-side construction and Dell mechanical drawing jointly constrain the closed side silhouette, top seam, front ear, rear PSU protrusions and absence of vents; it is generated independently, without mirroring labels -> `MULTI_REFERENCE_RECONSTRUCTION`.
- Top: no perfectly orthographic direct top photo, but several exact 16-SFF top/front and top/rear photos jointly show every major top feature -> `MULTI_REFERENCE_RECONSTRUCTION`.
- Bottom: `GENERIC_BOTTOM_FALLBACK` after search exhaustion.

## Bottom search log

Searched exact-model Dell product manuals, technical guide, system-cover/rail/service topics, 3D Guides, videos, product media and regulatory identity (`E31S001`); then exact-model ITinStock, Server Superstore, NewServerLife, eBay, used-equipment, reseller, auction, review, teardown and Chinese-language sources using `underside`, `bottom`, `底部`, `机箱`, `E31S001 underside`, and local-language equivalents. No usable exact underside image was found. Search results repeatedly returned front, rear, top-cover or open-internal views. The fallback therefore uses only the official 444:684 body ratio and exact side/top galvanized material, and intentionally includes no identifying or unsupported bottom detail.

Final acceptance status must be `PASS_WITH_BOTTOM_FALLBACK`, not ordinary `PASS`.

