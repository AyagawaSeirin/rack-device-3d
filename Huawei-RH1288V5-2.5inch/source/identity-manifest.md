# Assembly identity manifest — Huawei FusionServer Pro 1288H V5 10SFF

manufacturer: Huawei Technologies Co., Ltd.
requested_product_id: Huawei RH1288V5/2.5-inch (user-list alias), officially FusionServer Pro 1288H V5 Server
delivery_subject: complete-appliance
host_enclosure_model: Huawei FusionServer Pro 1288H V5, regulatory/platform family H12H-05
installed_module_model: not applicable; this is a complete 1U rack server
installed_module_count: not applicable
installed_module_positions: not applicable
front_backplane_or_drive_configuration: 10 x 2.5-inch SFF, five columns by two rows; ten externally closed Huawei carrier/filler faces; no front security bezel; no open bay
rear_io_or_controller_configuration: 3-I/O rear family with three external PCIe slot covers; optional LOM1/2 position unpopulated and closed; separate optional FlexIO position unpopulated and closed; fixed 2 x GE LOM, one management RJ45, one serial RJ45, VGA and 2 x USB 3.0
bezel_and_blanking_panel_state: no security bezel; ten front carrier/filler faces installed; all three PCIe external positions and FlexIO position closed; no external add-in-card connector or cable
power_and_fan_configuration: 2 x identical Huawei hot-swap AC PSU, 1+1-capable, IEC/C14 inlets; no DC/HVDC terminals; no unproven wattage label; seven internal fan modules remain behind the closed cover
u_height: 1U
body_dimensions_mm: 436 W x 43 H x 708 D for the 2.5-inch chassis
overall_front_rack_span_mm: 482.6 target across the two front mounting ears
coordinate_convention: right-handed; +X device right as seen from front, +Y up, +Z front
branding_state: retain Huawei flower mark, HUAWEI wordmark, and readable 1288H V5 marking; omit unit serials, barcodes, reseller watermark/stickers, and drive-capacity labels
evidence_urls:
  - https://support.huawei.com/enterprise/zh/server/1288h-v5-pid-21872252
  - https://serverflow.ru/config/servernaya-platforma-huawei-fusionserver-1288h-v5-1u-10sff-4x-u-2-2x-900w-2x-lga3647/
  - https://www.compuway.ru/servers/huawei/huawei-fusionserver-rh1288h-v5-product-page/
evidence_local:
  - source/originals/huawei-1288h-v5-user-guide-issue13.pdf, PDF pages 10, 14-24, 55-56
  - source/originals/huawei-1288h-v5-quick-start-v100r005-07.pdf, PDF pages 1-2
  - source/third-party/serverflow/10sff.webp and 10sff-photo.webp
  - source/third-party/compuway/front-10sff.png and rear.jpg
  - source/originals/user-request-table.png, ninth readable device row
excluded_incompatible_variants:
  - Huawei RH1288 V3 / 1288H V3
  - Huawei 2288H V5 and all 2U products
  - 1288H V5 4 x 3.5-inch / LFF, including its 748 mm chassis depth
  - 1288H V5 8 x 2.5-inch front, optional DVD/VGA front, and its different control-panel layout
  - MyDraw 2-I/O rear; the requested thumbnail and official guide expose the three-PCIe-slot rear
  - DC or HVDC PSU faces; front bezel; cable-populated/add-in-card rear
status: VERIFIED

## Installed-state interpretation

The user thumbnail proves the 10SFF silhouette but is too small to prove the internal disk population. Official Figure 2-3 calls all ten positions drives, while the exact ServerFlow specimen visibly has ten closed carrier/filler faces and only one seller-applied capacity label. The exterior model therefore keeps all ten Huawei carrier/filler faces installed, removes the specimen-specific capacity sticker, and does not claim a disk capacity or internal population. This preserves every visible bay, handle, grille, latch and green accent without inventing unit-specific data.

## Rear-family decision

The official user guide and quick guide label PCIe slots 1, 2 and 3 plus a distinct optional FlexIO card position. The enlarged user-row thumbnail has three separate upper slot-cover bands, an empty optional LOM1/2 area at lower left, VGA, four fixed RJ45 sockets, two stacked USB ports, an empty FlexIO cover and dual AC PSUs. `mydraw-rear-2io.png` is retained only as contrast evidence. The ServerFlow 10SFF photograph is a material/PSU/chassis reference but its installed optional 10GE electrical LOM1/2 module is explicitly rejected for this requested rear.
