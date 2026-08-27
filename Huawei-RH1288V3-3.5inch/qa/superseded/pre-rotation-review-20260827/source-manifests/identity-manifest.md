# Assembly identity manifest — frozen before generation

manufacturer: Huawei Technologies Co., Ltd.
requested_product_id: Huawei FusionServer RH1288 V3
official_nameplate_model: H12M-03
generation_suffix: V3
delivery_subject: complete-appliance
host_enclosure_model: RH1288 V3 1U 3.5-inch chassis
installed_module_model: not applicable
installed_module_count: not applicable
installed_module_positions: not applicable
front_backplane_or_drive_configuration: 4-disk configuration; four 3.5-inch LFF SAS/SATA bays in one row, slots 0-3 left to right
carrier_state: four factory LFF carrier fronts installed and closed; no open bay; the user screenshot does not prove internal media population, so seller disk labels are excluded
rear_io_or_controller_configuration: SM212-visible four-GE FlexIO face; four RJ45 service ports; one RJ45 management port; two USB 3.0 ports; one VGA port; one serial port; one UID indicator; one full-height and one half-height PCIe position, both with factory perforated blanks
bezel_and_blanking_panel_state: no optional security bezel; factory left/right front mounting ears present; no rear ears; both rear PCIe openings blanked
power_and_fan_configuration: two 460 W 80 Plus Platinum hot-swap AC PSUs, model family DPS-460DB-1 A / Huawei P/N 02130957, in 1+1 redundancy; five internal hot-swap fan modules in N+1 redundancy
u_height: 1U
body_width_mm: 436
overall_width_mm: 482.6 nominal 19-inch mounting span with front ears
height_mm: 43
published_chassis_depth_mm: 748
front_backplane_variant: 3.5-inch LFF, not 2.5-inch SFF
excluded_variants: RH1288H V3; RH2288/RH2288H; RH1288 V5/1288H V5 and later generations; RH1288 V3 8x2.5-inch and NVMe fronts; two-port 10GE/IB rear faces; two-GE rear face; DC/HVDC PSUs; rear mounting ears
evidence_urls:
  - https://support.huawei.com/enterprise/en/intelligent-servers/rh1288-v3-pid-9901873
  - https://info.support.huawei.com/computing/tools/gallery/enterprise/intelligent-server/detail?currentProduct=37&lang=en
  - https://www.router-switch.com/pdf2html/pdf/huawei-rh1288-v3-rack-server-datasheet.pdf
  - https://katalog.vector.net/wp-content/uploads/import/Huawei%20FusionServer%20RH8100%20V3%20White%20Paper.pdf
  - https://device.report/m/7009a59d0542b27d0a93809307e88a251b2cc3ea1245bace9872a925196f6af3.pdf
  - https://rozetka.com.ua/ua/596556760/p596556760/
  - https://www.lnc.ru/catalog/huawei/rack/huawei-fusionserver-rh1288-v3
status: VERIFIED
delivery_status: PASS_WITH_BOTTOM_FALLBACK
bottom_evidence_status: GENERIC_BOTTOM_FALLBACK after documented search exhaustion
completed_at: 2026-08-23

## Identity decision

The tenth readable device row in the supplied table is the Huawei RH1288 V3 3.5-inch row. It is the 1U H12M-03 appliance, not the 2U RH2288/RH2288H family and not the V5 successor. Huawei Issue 45 and the Issue 03 whitepaper separate the four-bay 3.5-inch face from the 8-bay 2.5-inch faces. The user row and exact 4LFF photographs show four closed LFF carrier fronts.

The screenshot rear has four adjacent service RJ45 ports, selecting the four-GE SM210/SM212 visible face. The frozen option is SM212 because exact H12M-03 package evidence ties SM212 to this generation; SM210 and SM212 share the same exterior four-RJ45 face. The requested visible identity is therefore four GE ports regardless of internal board revision.

The two externally visible circular rear fans are PSU fans. The five chassis cooling modules are internal to the closed appliance and are configuration evidence, not exterior openings. AC is frozen throughout; no DC or HVDC inlet is allowed.
