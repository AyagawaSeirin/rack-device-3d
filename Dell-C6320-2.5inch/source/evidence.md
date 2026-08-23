# Evidence, source matrix, and inclusion rules

Access date: 2026-08-24 (Asia/Singapore)

## Target row and assembly decision

The user screenshot row reads `DELL C6320/2.5英寸` and supplies a complete front/rear pair. The front shows a 2U chassis with one row of 24 vertical 2.5-inch carriers, Dell control panels and front rack flanges. The rear shows two stacked shared PSUs plus four identical C6320 sled rears in a 2 x 2 layout. This is the complete PowerEdge C6300 enclosure populated with four PowerEdge C6320 two-socket sleds, not a standalone sled.

The exact screenshot layout agrees with Dell Owner's Manual figures 1/3 (supported/front configuration) and 6 (back panel with four system boards), and with two independent exact-model photo sets. The target rear has dual embedded 10GbE SFP+ cages, so the C6320p one-port/Mellanox layout is excluded. The screenshot PSU geometry agrees with Dell's 1400 W AC/HVDC outline and exact real photographs. Because the user requires unified AC power, the build fixes both modules to 1400 W AC; it does not use HVDC or a mixed 1400/1600 pair.

## Official sources

### Dell PowerEdge C6320 Owner's Manual

- URL: https://dl.dell.com/topicspdf/poweredge-c6320_Owners-Manual_en-us.pdf
- Local original: `source/originals/PowerEdge-C6320-Owners-Manual.pdf`
- SHA-256: `ac143bbbbe3bbf0ed1842a67b6fd6b97ffc38d4b540d3f8cc490b1eaaac2bd50`
- Authority/source class/visual origin: official / owner manual / technical diagram
- Relevant inspected pages:
  - p9: complete supported C6320 layout; four dual-socket nodes, 24 x 2.5 option, two matched PSU options.
  - p10: exact 24 x 2.5 one-row carrier map MB1-1 through MB4-6; non-usable drive cover.
  - p13: exact four-sled rear and port order.
  - p16: 1400 W AC/HVDC PSU external geometry; AC inlet and fan.
  - p17: 1600 W shape inspected only to reject it.
  - p26-p27: older C6320-system dimension revision and explicit no-mixed-PSU rule.
  - p59-p62: exact cover/side/fan-cage service geometry.
  - p136-p140: exact 24 x 2.5 expander backplane and drive-cage geometry.
- Proves: assembly identity, carrier count/order, rear I/O order, PSU count/shape, cover and side features, internal shared fan count.
- Limitation: mostly line art; color/material must come from exact photographs.

### Current Dell online chassis-dimension topic

- URL: https://www.dell.com/support/manuals/en-us/poweredge-c6320/c6320_pub/chassis-dimensions?guid=guid-1b6d8b76-78e6-4872-b103-de2c091cedf3&lang=en-us
- Authority/source class: official / current online owner manual topic
- Quoted facts: PowerEdge C6300 enclosure Xa 482.3 mm, Xb 448.0 mm, Y 86.8 mm, Za without bezel 41.4 mm, Zb 762.1 mm, Zc 795.9 mm.
- Proves: binding fully installed host-enclosure scale.
- Limitation: drawing reference spans do not support simply adding Za + Zb; Zc alone is used as total depth.

### Official 24 x 2.5 front diagram

- URL: https://dl.dell.com/topics//c6320_pub/images/GUID-C64FBEEF-F8AD-4949-9EAE-50D79A50B12D-low.png
- Local: `source/originals/official-front-2.5-low.png`
- SHA-256: `a426f23a7d013444a67dee7875b88c1e923f7e581b049a9cad5d8a328f268f5a`
- Proves: 24 vertical carriers, four six-drive board groups, left/right control locations, narrow non-usable cover and front ears.
- Limitation: line art, 660 x 169; not a material/style reference.

### Dell PowerEdge C6320 specification sheet

- URL: https://i.dell.com/sites/doccontent/shared-content/data-sheets/en/Documents/Dell-PowerEdge-C6320-Spec-Sheet.pdf
- Local: `source/originals/Dell-PowerEdge-C6320-Spec-Sheet.pdf`
- SHA-256: `16cf469ff540de7342e683375733c25379ea9522e32877dfc7627ff66b708c2a`
- Proves: 2U shared platform, up to four independent two-socket servers, flexible 24 x 2.5 or 12 x 3.5 storage.
- Limitation: marketing sheet, not a six-face mechanical source.

### Dell HPC 13G architecture white paper

- URL: https://downloads.dell.com/manuals/all-products/esuprt_solutions_int/esuprt_solutions_int_solutions_resources/high-computing-solution-resources_white-papers28_en-us.pdf
- Local: `source/originals/Dell-HPC-General-Computing-13G.pdf`
- SHA-256: `7b33a2e3bbafa400d2222900d170885fc61ae1bd8bb95bfb2f353b938740facc`
- Proves: C6320 is a half-height sled in a 2U chassis; chassis supports up to four sleds; maximum 24 x 2.5; default six 2.5 drives per sled.
- Limitation: architecture summary, not detailed face photography.

### Dell dynamic pages and video escalation

- Manual page: https://www.dell.com/support/manuals/en-us/poweredge-c6300/c6320_pub
- Top-cover video: https://www.dell.com/support/contents/en-uk/videos/videoplayer/how-to-replace-top-cover-for-poweredge-c6300-series/6079817769001
- Real-browser result: the Dell dynamic manual request returned HTTP 403; browser snapshot is retained under `.playwright-cli/`. Public static Dell PDF and image assets were then retrieved without bypassing access controls.
- Video transcript confirms securing screw, cover release latch lock, two-side traction handling, sliding direction and complete top-cover removal.

## Exact-model real photographs

### Maravi/eBay exact C6300 + four C6320 + 24 SFF gallery

- Listing: https://www.ebay.ca/itm/175404082673
- Configuration evidence: title states C6300, four C6320 nodes, 24 x 2.5, dual-port 10GbE SFP+; rear photos visually agree with Dell C6320 manual.
- `source/third-party/ebay-maravi-c6300-1.webp`, SHA `fc76b4d1e5369760489b65787905dd1d478a88a9cf5ebfc5bc112517a6f900fd`: near-orthogonal front three-quarter, all 24 carriers, correct control panels/ears, exact steel/plastic photography; black seller backdrop only.
- `source/third-party/ebay-maravi-c6300-2.webp`, SHA `498adec201b44eba4a630e33fcb4c9f9c2a9149c518af064fd87804f41c57bd6`: stacked exact fronts; confirms repeated carrier/control layout; warehouse background and barcode sticker excluded.
- `source/third-party/ebay-maravi-c6300-3.webp`, SHA `90580587d2878fac55cfdf5ce0530db08490c8db76da4830936d35492e50457c`: stacked exact rears; confirms four C6320 sleds, two orange-release 1400 W AC PSUs, SFP+/iDRAC/VGA order and real perforation/material.
- `source/third-party/ebay-maravi-c6300-4.webp`, SHA `e4002e8d36c38656626166edb601c257c58625162f0aa5bea7c5a49e01bb3942`: top/rear service angle; confirms galvanized cover, asymmetric black/blue traction pads, stepped seam, screw dimples, rear slot groups and factory warning labels. Sleds are partially pulled/open, so it is top evidence only and is not a rear-configuration primary.

### ITinStock exact four-C6320 photograph

- Listing: https://itinstock.com/dell-poweredge-c6300-node-server-4x-c6320-w-2x10c-e5-2650v3-128gb-ram-12tb-hdd-61070-p.asp
- Local: `source/third-party/itinstock-c6300-4xc6320.jpg`
- SHA-256: `66814d562a898a13fe5a8fb7c4e589ebe22c15a999f989e88b2989b802fcd9ed`
- Visual origin: real photograph; straight/near-straight complete rear on white.
- Proves: exact four-node C6320 rear, two stacked 1400 W AC PSUs, one PCIe vented carrier and complete I/O order per sled, no C6320p mixing.
- Limitations: 1200 x 800 padded canvas; mild elevated perspective; no direct side/bottom.

### Express Computer Systems C6320 rear/top angle

- Listing: https://expresscomputersystems.com/products/dell-poweredge-c6320-node-server-configurable
- Local: `source/third-party/express-c6320-rear.jpg`
- SHA-256: `8ef272a1584dfcf94a9bc705c5f3abc88eea77c1bc216585c103a72eb7f74cb3`
- Proves: exact complete C6300 host with four C6320 sleds and two AC PSUs; full top cover material and rear-left/right boundaries.
- Limitations: 800 x 800, rear perspective, white seller canvas.

### User screenshot

- Local original: `source/originals/user-screenshot.png`
- SHA-256: `00861cf47eb85ee4f20fc3dc3fc850820368df4e3db7b2721b3226dfca8c1921`
- Crops: `qa/reference/user-front-thumb.png`, SHA `79230f5b2c1a83c8a1cac2c5a92cdf142835319ab34120a3f8a3f5a96758c84f`; `qa/reference/user-rear-thumb.png`, SHA `127ca5a6d68dc868879aa32d5dc0ebde272e0c3f9739f7a1cbc9f9955466a46f`.
- Proves: the requested row and exact delivery appearance; user row matches 24 SFF/full four-C6320/dual AC photograph set.
- Limitation: thumbnail resolution; it locks target selection but does not replace higher-resolution exact photographs.

## Excluded or limited sources

- `source/third-party/ebay-c6300-24sff-front.png` and `source/third-party/ebay-c6300-24sff-rear-or-side.webp` came from a listing whose MPN includes `C6320PX4`; they show the common C6300 host but may contain C6320p sled hardware. They are excluded from all identity-bearing face inputs and final feature decisions.
- C6400/C6420, C6200/C6220 and C6320p results were discovery noise only and are excluded.
- Seller watermarks, warehouse backgrounds, serial/barcode stickers, loose rails, cables, missing sleds and pulled-node service states are not factory delivery features.

## Side-face reconstruction evidence

No exact straight side elevation was found. Left/right are therefore `MULTI_REFERENCE_RECONSTRUCTION`, not source-locked direct photographs. Official pages 59, 61 and 138 visibly establish the 2U side wall, folded edges, rail key slots, round fasteners, vertical access slot and upper shallow rectangular recesses. Exact front/top/rear photographs establish the real galvanized-steel finish and both side boundaries. The two calls use different source order and distinct non-mirrored locked traits. No side label, vent, foot or rail is added without evidence.

## Bottom exhaustive-search log and fallback decision

Exact underside searches attempted after official/PDF review:

- Dell manual/media/driver/video pages for C6300/C6320 plus `bottom`, `underside`, `rail`, `feet`, `mechanical`, `service`, `teardown` and `3D`.
- Dell top-cover and component-replacement videos; no underside view.
- Exact-model resellers: ITinStock, Express Computer Systems, Mojo Systems, TekBoost/Bargain Hardware leads, eBay/Maravi/Northland, ICT-spareparts.
- Marketplace/auction/used-equipment and image searches in English plus Chinese/Japanese terms: `底部`, `底面`, `侧面`, `側面`, `中古`.
- Exact C6300/C6320 Reddit/homelab listings and teardown leads.
- Public official 3D/CAD/AR/Visio searches.

No usable exact C6300 underside was found. Front, rear, left, right, top, dimensions and every silhouette-affecting edge are otherwise verified. `bottom.png` is therefore the sole controlled `GENERIC_BOTTOM_FALLBACK`: a conservative, opaque, unbranded galvanized sheet at 448.0:795.9 with no unsupported hole, vent, foot, rail, label, seam, fastener or protrusion. Final status can be no better than `PASS_WITH_BOTTOM_FALLBACK`.

## Inclusion rules for the build

- Main GLBs are newly modeled; no third-party or official mesh is copied.
- Preserve exact 2U proportions, 24-carrier front, 4-sled rear, 8 SFP+ cages, 4 iDRAC ports, 4 VGA ports, 2 matching 1400 W AC PSUs and front-only rack ears.
- Geometry is required for carriers, latches, ears/holes, sled boundaries, PSU blocks/fans/inlets/handles, ports, rear pull labels, cover pads, cover seam, side slots/recesses and all silhouette/parallax features.
- Dense grille/perforation may use depth-backed repeated geometry or opaque texture at web camera distance; it must never use transparent chassis pixels.
- Preserve Dell and PowerEdge C6320 factory markings; remove seller identity and serial/QR pseudo-text.
