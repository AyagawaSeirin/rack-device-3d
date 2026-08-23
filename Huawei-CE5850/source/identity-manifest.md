# Assembly identity manifest

manufacturer: Huawei Technologies Co., Ltd.
requested_product_id: CloudEngine CE5850 (user table row 1)
resolved_chassis_pid: CE5850-48T4S2Q-EI
resolved_complete_bundle: CE5850-EI-B00
bundle_part_number: 02359104
delivery_subject: complete-appliance
host_enclosure_model: CE5850-48T4S2Q-EI fixed 1U chassis
installed_module_model: 2 x PAC-150WA AC PSU; 2 x FAN-40EA-F fan module
installed_module_count: 4 removable rear/power-side modules total
installed_module_positions: PAC-150WA / FAN-40EA-F / central management area / FAN-40EA-F / PAC-150WA, left-to-right when viewing the power side
front_backplane_or_drive_configuration: user-facing front is the port side; 48 x 10/100/1000BASE-T RJ45, then 4 x 10GE SFP+, then 2 x 40GE QSFP+
rear_io_or_controller_configuration: user-facing rear is the power side; Console RJ45 above ETH management RJ45, pull-out serial label, USB, system/module LEDs
bezel_and_blanking_panel_state: no bezel; all 48 RJ45, 4 SFP+, and 2 QSFP+ cages empty; both fan slots and both PSU slots populated
power_and_fan_configuration: dual PAC-150WA AC, dual FAN-40EA-F, power-side intake and port-side exhaust (Huawei bundle wording: port-side exhaust)
u_height: 1U; actual height 43.6 mm
body_dimensions_mm: 442.0 W x 420.0 D x 43.6 H
rack_hardware: two separate port-side mounting ears/brackets, built as independent nodes; official manual records three port-side chassis attachment holes per side
orientation_note: Huawei documentation calls the power side "front" and port side "rear"; the user screenshot calls the port side front. Final canonical +Z/front follows the user screenshot and is the port side.
evidence_urls:
  - https://support.huawei.com/enterprise/zh/doc/EDOC1000019242/53f4bcaa
  - https://info.support.huawei.com/info-finder/imagelib/getPreviewImages?domain=0&lang=en&partNumber=02359104
  - https://carrier.huawei.com/~/media/CNBG/Downloads/Product/Fixed%20Network/carrierip-dcswitches/HUAWEI%20CloudEngine%205800%20Switch%20Datasheet.pdf
identity_resolution:
  - The screenshot power-side thumbnail has normalized cross-correlation 0.986153 against the exact Huawei Info-Finder CE5850-48T4S2Q-EI power-side photo; the HI match is 0.537702.
  - The screenshot port-side card has normalized cross-correlation 0.822625 against the exact EI photo and 0.693214 against HI.
  - The exact EI source reads CE5850-48T4S2Q-EI and shows FAN-40EA-F twice plus PAC-150WA twice.
  - Huawei ordering data maps that complete installed configuration to 02359104 / CE5850-EI-B00.
status: VERIFIED

