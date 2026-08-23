# Assembly identity manifest

manufacturer: Huawei Technologies Co., Ltd.
product_line: FusionServer
requested_product_id: RH2288 V3
nameplate_model: H22M-03
delivery_subject: complete-appliance
host_enclosure_model: H22M-03 12-disk 3.5-inch chassis
installed_module_model: not applicable
installed_module_count: not applicable
installed_module_positions: not applicable
front_backplane_or_drive_configuration: 12 common SAS/SATA 3.5-inch LFF bays, non-NVMe, three rows by four columns; twelve factory carrier faces installed; no capacity-specific drive stickers
rear_io_or_controller_configuration: no rear disk module; I/O module 2 and I/O module 1 fitted with their photographed blank PCIe covers; onboard slots 4 and 5 blank; SM211 flexible NIC with two GE RJ45 ports; two USB 3.0, dedicated Mgmt RJ45, VGA, DB9 serial and UID; no installed PCIe cards, rails or cables
bezel_and_blanking_panel_state: no security bezel; all twelve front carrier faces present; rear expansion openings blanked exactly as in the no-rear-disk H22M-03 photographs
power_and_fan_configuration: two identical WEPW80015 460 W GOLD AC hot-swap PSUs in the vertically stacked PSU1/PSU2 positions on one rear side; four internal hot-swap fan modules; front-to-rear airflow
u_height: 2U
body_width_mm: 447
overall_front_width_mm: 482.6
height_mm: 86.1
body_depth_mm: 748
published_dimension_includes: Huawei data sheet states product W x D x H for the 3.5-inch model; it does not separately state whether the rear cord-retainer loops are included
front_projection_mm: carrier handles and front mounting/control ears are separate visible relief
rear_projection_mm: PSU fan/cord-retainer assemblies are separate visible relief; their final measured extension is reported separately from the 748 mm published chassis depth
visual_branding: real front Huawei logo and RH2288 V3 badge; no invented exterior FusionServer wordmark where the photographed chassis does not carry one; FusionServer retained in asset metadata and reports
evidence_urls:
  - https://support.huawei.com/enterprise/en/intelligent-servers/rh2288-v3-pid-9901877
  - https://info.support.huawei.com/computing/tools/gallery/enterprise/intelligent-server/detail?currentProduct=38&name=RH2288+V3+Rack+Server
  - https://a.storyblok.com/f/283550/11994287b0/huawei_fusionserver_rh2288_v3_data_sheet.pdf
  - https://www.ruten.com.tw/item/22632335258685/
  - https://server.zol.com.cn/726/7268120.html
  - https://pdfcoffee.com/user-manual-rh2288-v3-pdf-free.html
status: VERIFIED

## Frozen configuration decision

- The user table's sixth-row front is accepted only as the 12-LFF variant clue.
- The sixth-row rear thumbnail is a mismatched device and is excluded from all generation and QA targets by explicit user authorization.
- The delivered rear is the cross-checked H22M-03 no-rear-disk assembly in Ruten `content-15/22/23/24` and the straight ZOL photograph: dual AC PSUs stacked vertically on one side, SM211 two-port flexible NIC, blank onboard slots 4/5, blank I/O/riser panels and the documented management/console group.
- The current Huawei official product-gallery rear is a different legal RH2288 V3 option with a rear disk module and four-port NIC. It is retained only for exact chassis/material/side evidence; its rear-disk module and NIC count are explicitly forbidden in the requested build.
- Ruten `content-17` is an internal motherboard overview and `content-21` is a motherboard connector close-up. Neither is rear evidence.
- All six legacy AI faces and any legacy preview/model are defect examples only. They have no authority over this manifest or the source locks.
