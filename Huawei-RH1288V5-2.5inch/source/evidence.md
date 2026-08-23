# Evidence ledger — Huawei FusionServer Pro 1288H V5 10SFF

Access date for web sources: 2026-08-23 (Asia/Singapore).

## Requested row and formal identity

The user-supplied table is preserved unchanged as `source/originals/user-request-table.png`. The ninth readable device row, enlarged in `qa/reference/user-row-09.png`, says `华为 RH1288V5/2.5英寸`. Pixel inspection shows five SFF columns by two rows and the narrow one-USB 10SFF control panel. The preceding eighth row is the 3.5-inch/LFF variant and the following rows are V3; neither is interchangeable.

Huawei's formal V5 name is **FusionServer Pro 1288H V5 Server**. `RH1288V5` is retained only as the user's catalog alias. Huawei support PID is `21872252`; the platform/nameplate family is `H12H-05`. Official support: <https://support.huawei.com/enterprise/en/intelligent-servers/1288h-v5-pid-21872252> and product API: <https://support.huawei.com/supportgateway/supproductservice/v1/enterprise/aggregation/init?pid=21872252>.

## Official documents

1. Huawei, *FusionServer Pro 1288H V5 Server User Guide*, Issue 13, 2020-06-05. Preserved unchanged as `source/originals/huawei-1288h-v5-user-guide-issue13.pdf` (SHA-256 `2d37b0d60f98412566b86a0c093ece8332ccaa0f8b232079e400c28df3a512dd`).
   - PDF p.10 / document p.2: exact 1288H V5 2.5-inch physical structure and closed cover family.
   - PDF p.14 / document p.6: Figure 2-3, 10 x 2.5-inch front; Figure 2-2 above it is the rejected 8SFF front.
   - PDF pp.15-19 / document pp.7-11: 10SFF controls and the only front connector, one USB 3.0.
   - PDF p.20 / document p.12: Figure 2-10 rear, PCIe slots 1, 2, 3, optional FlexIO, PSU 1 and PSU 2.
   - PDF pp.22-24 / document pp.14-16: Figure 2-12 and Table 2-4, fixed VGA, GE3, GE4, management, serial, two USB 3.0 and PSU sockets; optional LOM1/2 may be optical or electrical when installed.
   - PDF p.55 / document p.47: 2.5-inch chassis is 43 x 436 x 708 mm; 3.5-inch chassis is 43 x 436 x 748 mm and is rejected.
   - PDF p.56 / document p.48: 19-inch/482.6 mm cabinet constraint and maximum 10SFF server weight.
2. Huawei, *1288H V5 Server Quick Guide*, V100R005, revision 07. Preserved unchanged as `source/originals/huawei-1288h-v5-quick-start-v100r005-07.pdf` (SHA-256 `ea00018e8c0619d40e93021766000bf11fd5d0e300eae821fe0ff7c18b935cdd`).
   - PDF p.1 contains all 4LFF/8SFF/10SFF front diagrams, the three-slot rear diagram and both chassis depths.
   - PDF p.2 proves front-only mounting hardware and the closed top during installation.

The environment has no dedicated PDF skill/tool. Text extracted in the existing project evidence cache was copied alongside the unchanged PDFs; relevant pages were freshly rendered with Ghostscript to `source/pdf-pages/` and every rendered page was inspected at original detail. `source/image-inspection.csv` records what each page proves.

## Frozen front configuration

- 10 x 2.5-inch SFF carrier/filler faces, five columns by two rows.
- No security bezel, no open bay, no 8SFF DVD/VGA region.
- Ten black honeycomb carrier faces, ten right-side latch/handle blocks and ten lime-green vertical accents.
- Left ear carries Huawei flower/HUAWEI; right ear carries `1288H V5`.
- The narrow control area has the fault display/status/buttons and one USB 3.0 only.
- Internal disk capacity/population cannot be read from the user thumbnail. The model preserves ten externally closed faces and omits seller capacity stickers.

Exact real specimen source: ServerFlow, *Huawei FusionServer 1288H V5 1U 10SFF (4 x U.2, 2 x 900 W, 2 x LGA3647)*, <https://serverflow.ru/config/servernaya-platforma-huawei-fusionserver-1288h-v5-1u-10sff-4x-u-2-2x-900w-2x-lga3647/>. The dynamic gallery was inspected with Playwright. Fifteen original 3000 x 2252 WebPs are preserved in `source/third-party/serverflow/`; `10sff.webp` and `10sff-02.webp` bind the exact front/top appearance. `10sff-03` through `10sff-13` are open-cover/internal or component views and are supporting-only.

Independent 10SFF cross-check: Uonel/Huawei Telecom Equipment, BOM `02312DFL`, platform `H12H-05-S10AFF`, <https://www.huaweitelecomequipment.com/sale-13651281-02312dfl-h12h-05-s10aff-huawei-1288h-v5-server-10-sas-sata-hdd-chassis.html>. Original 790 x 592 image is `source/third-party/uonel/02312DFL-H12H-05-S10AFF-10SFF.jpg`; it confirms the 2 x 5 carrier front and one-USB control panel but is too oblique/low-resolution to be the primary style lock.

CompuWay, <https://www.compuway.ru/servers/huawei/huawei-fusionserver-rh1288h-v5-product-page/>, supplies the exact 10SFF elevation diagram `source/third-party/compuway/front-10sff.png` and shared rear diagram. Its `front.jpg` is the rejected 8SFF configuration.

## Frozen rear configuration

The enlarged requested thumbnail `qa/reference/user-row-09-rear-4x.png` matches the official default three-slot rear outline:

- three separate upper PCIe slot covers (slot 1, slot 2, slot 3), all closed;
- lower-left optional LOM1/2 area closed and **unpopulated**;
- fixed VGA, GE LOM3, GE LOM4, management RJ45, serial RJ45 and two stacked USB 3.0 ports;
- independent optional FlexIO position closed and **unpopulated**;
- two identical hot-swap AC PSU faces with IEC inlets; no DC/HVDC terminals and no unproven wattage marking.

`source/third-party/mydraw/mydraw-rear-3io.png` matches this requested silhouette. `mydraw-rear-2io.png` is retained only as a contrast/rejection source. The exact ServerFlow 10SFF rear photograph provides real galvanized metal, PSU, fan, handle and recess character, but its installed optional 10GE electrical LOM1/2 module is explicitly rejected. Huawei official gallery rear `_05` similarly has an installed optical LOM module and is not the requested port state.

Huawei documents multiple AC wattages. The thumbnail proves two same-type AC/IEC modules but not 550/900/1500 W; the final exterior therefore carries no wattage-specific label. This follows the user instruction to standardize on AC without inventing a rating.

## Dimensions and orientation

The controlling body is 436 W x 43 H x 708 D mm. A 482.6 mm outer front mounting span is treated separately from the 436 mm body and normalized against exact photos; it is not substituted for the body width. Small PSU handle/latch protrusion is listed separately in `source/dimension-ledger.csv`. Coordinate convention is +X device right as seen from front, +Y up, +Z front. A rear view naturally reverses screen-side physical left/right and is never mirrored to resemble the front.

## Side and top evidence

No complete orthogonal real left/right photo was found. The gap is closed by jointly using:

- exact 10SFF ServerFlow front-top, rear-top and open-cover angles for the real 708 mm chassis material/edge continuity;
- Huawei official gallery `_02` and `_03` for the two different side fronts and non-mirrored slot/fastener placement;
- the public xFusion successor-official 1288H V5 viewer, rotated and visually inspected in `qa/reference/xfusion-viewer-side-a.png` and `...side-b.png`, for full-length side geometry of the shared 2.5-inch/708 mm chassis.

The viewer/gallery has an incompatible 8SFF front and cannot supply front identity. Huawei's guide gives one 708 mm 2.5-inch chassis dimension for both 8SFF and 10SFF; the official side shell is used only where it does not depend on the front backplane. Left and right remain independent assets with different endpoint/fastener patterns.

Top is bound by exact 10SFF closed specimen photographs (`10sff.webp`, `10sff-02.webp`, `10sff-photo.webp`) and corroborated by the official viewer/gallery. It has a front fixed strip, two long vent bands, center latch, closed galvanized cover and asymmetric rear step/label zones.

## Official optional 3D/viewer evidence

xFusion successor-official public viewer: <https://support.xfusion.com/server-3d/res/server/1288hv5/index.html?lang=en>. The page openly loads <https://support.xfusion.com/server-3d/res/server/1288hv5/tree.json> and `res/model/obj0.bin` through `obj15.bin` plus six JPEG atlases. The resource set is a proprietary iV3D binary viewer, **not** Wavefront OBJ, GLB, glTF, STEP, FBX or standard CAD. All public original resources and the required public runtime scripts are preserved unchanged under `source/optional-3d/xfusion-1288hv5-viewer/` with `SHA256SUMS.txt`.

Inspection shows the viewer default front is 8SFF and has a DVD/VGA/two-USB area. It is therefore an optional chassis/top/side/bottom geometry source only, never the main build and never a substitute for the requested 10SFF GLBs. No public official GLB, glTF, STEP, FBX or standard CAD download was found. The viewer exposes no explicit redistribution license; the files are retained as source evidence and are not copied into the delivered model.

Huawei gallery product ID 59: <https://info.support.huawei.com/computing/tools/gallery/enterprise/intelligent-server/detail?currentProduct=59&lang=zh>. Five unchanged 1920 x 1080 official RGBA images and the ZIP are stored in `source/originals/official-gallery/`. They also depict 8SFF and are supporting-only for shared chassis geometry/material.

## Six-face production modes

- Front: `SOURCE_LOCKED_GENERATION` from exact 10SFF real photograph.
- Rear: `MULTI_REFERENCE_RECONSTRUCTION` because available real photographs install a different optional LOM module; requested empty-LOM/empty-FlexIO state is locked by the user row plus official diagrams.
- Left/right: `MULTI_REFERENCE_RECONSTRUCTION` from exact 10SFF real angles plus full-side official viewer geometry; generated independently, never mirrored.
- Top: `MULTI_REFERENCE_RECONSTRUCTION` from multiple exact closed 10SFF real photos.
- Bottom: `GENERIC_BOTTOM_FALLBACK`, with the public official 1288H V5 viewer underside as the closest same-model/2.5-inch chassis reference and exact 10SFF material/edge sources. See `source/bottom-search-log.md`.

## Explicit exclusions

RH1288 V3/1288H V3; 2288H V5; every 2U product; 4LFF/3.5-inch front and 748 mm chassis; 8SFF/DVD/VGA front; MyDraw 2-I/O rear; optional LOM1/2 modules; installed FlexIO; external add-in cards/cables; front security bezel; DC/HVDC PSUs; seller watermark, serials, barcodes, inventory labels and capacity stickers.
