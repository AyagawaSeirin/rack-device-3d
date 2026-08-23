# Assembly identity manifest — frozen before generation

manufacturer: Huawei Technologies Co., Ltd.
requested_product_id: Huawei FusionServer RH1288 V3
official_nameplate_model: H12M-03
generation_suffix: V3
delivery_subject: complete-appliance
host_enclosure_model: RH1288 V3 1U 2.5-inch chassis
installed_module_model: not applicable
installed_module_count: not applicable
installed_module_positions: not applicable
front_backplane_or_drive_configuration: 8-disk configuration 1, eight 2.5-inch SFF SAS/SATA/SSD bays, slots 0-7; exact asymmetric 3-over-5 layout (three paired columns at left plus two additional lower-row bays beneath the right service area); eight closed carrier fronts; no NVMe-specific orange/green dual-indicator carrier substitution
carrier_state: all eight visible carrier fronts installed and closed; no open bay; the photographs do not prove the internal media population
rear_io_or_controller_configuration: SM212-visible four-GE FlexIO face (four RJ45 service ports), one RJ45 management port, two USB 3.0 ports, one VGA port, one serial port, one UID indicator, one full-height PCIe slot with factory perforated blank and one half-height PCIe slot with factory perforated blank
bezel_and_blanking_panel_state: no optional security bezel; factory left/right mounting ears present; both rear PCIe openings use perforated factory blanks
power_and_fan_configuration: two 750 W hot-swap AC PSUs in 1+1 redundancy, side-by-side at physical rear right; each exposes an IEC AC inlet, PSU fan grille, indicator and lime-green release feature; five internal hot-swap fan modules in N+1 redundancy are frozen but are not externally exposed with the cover installed
u_height: 1U
body_width_mm: 436
overall_width_mm: 482.6 nominal 19-inch rack mounting span, with mounting ears modeled separately
height_mm: 43
published_chassis_depth_mm: 708
front_backplane_variant: 2.5-inch, not 3.5-inch
excluded_variants: RH1288H V3; RH1288 V5; FusionServer 1288H V5/V6/V7; RH1288 V3 4x3.5-inch; RH1288 V3 NVMe-specific carrier mix; 10GE electrical FlexIO; 10GE optical FlexIO; DC or HVDC PSUs; any incompatible rear panel
evidence_urls:
  - https://support.huawei.com/enterprise/en/intelligent-servers/rh1288-v3-pid-9901873
  - https://info.support.huawei.com/computing/tools/gallery/enterprise/intelligent-server/detail?currentProduct=37&lang=en
  - https://www.nforce.com/files/Huawei%20FusionServer%20RH1288%20V3%20Data%20Sheet.pdf
  - https://device.report/m/7009a59d0542b27d0a93809307e88a251b2cc3ea1245bace9872a925196f6af3.pdf
  - https://katalog.vector.net/wp-content/uploads/import/Huawei%20FusionServer%20RH8100%20V3%20White%20Paper.pdf
  - https://www.lnc.ru/catalog/huawei/rack/huawei-fusionserver-rh1288-v3
  - https://khabtelecom.ru/server-huawei-rh1288-v3-h12m-03/
status: VERIFIED
delivery_status: PASS_WITH_BOTTOM_FALLBACK
bottom_evidence_status: GENERIC_BOTTOM_FALLBACK after documented search exhaustion

## Identity decisions

The user screenshot's eleventh readable device row is the RH1288 V3 2.5-inch row. Its front has eight SFF carrier faces in the Huawei-specific asymmetric 3-over-5 layout and its rear has four adjacent RJ45 service ports. The latter selects the four-GE SM210/SM212 physical FlexIO face rather than the two-port 10GE electrical, two-port 10GE optical or 56G IB faces. The exact H12M-03 package listing used as a configuration cross-check identifies SM212, two 750 W Platinum AC PSUs and the 8-SFF chassis; the visible face is therefore frozen as SM212.

The delivery includes only the externally visible closed appliance. The five internal fan modules are configuration evidence, not visible website geometry. The two large externally visible circular fans are the two PSU fan grilles and are modeled.
