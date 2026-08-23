# Assembly identity manifest

manufacturer: Huawei Technologies Co., Ltd.
requested_product_id: CE6851 (user screenshot row 13)
resolved_chassis_pid: CE6851-48S6Q-HI
resolved_ordering_part_number: 02350JAS
resolved_part_model: CE6851-HI-B-B0A
delivery_subject: complete-appliance
host_enclosure_model: not applicable; fixed 1U switch chassis
installed_module_model: PAC-600WA-B AC power module; FAN-40EA-B fan module
installed_module_count: 2 AC power modules; 2 fan modules
installed_module_positions: both power slots populated; both fan slots populated
front_backplane_or_drive_configuration: port side; 48 x 10GE SFP+ plus 6 x 40GE QSFP+
rear_io_or_controller_configuration: power side; PSU1, FAN1, management/USB/barcode panel, FAN2, PSU2
bezel_and_blanking_panel_state: no bezel; no blank power or fan slots; port-side rack brackets fitted per exact-B reseller evidence and the user's explicit ear-geometry requirement
power_and_fan_configuration: 2 x PAC-600WA-B, 2 x FAN-40EA-B, back-to-front airflow, port-side intake, power-side exhaust
u_height: 1U (43.6 mm)
body_dimensions_mm: 442.0 W x 420.0 D x 43.6 H
front_definition_for_asset_pipeline: port side (+Z)
rear_definition_for_asset_pipeline: power supply side (-Z)
coordinate_convention: right-handed; +X device right as seen from the port side; +Y up; +Z port side/front
evidence_urls:
  - https://info.support.huawei.com/info-finder/imagelib/getPreviewImages?domain=0&lang=zh&partNumber=02350JAS
  - https://info.support.huawei.com/info-finder/imagelib/getImgByNames4web?package_name=CE6851-48S6Q-HI_pic.zip&picture_name=front.png
  - https://info.support.huawei.com/info-finder/imagelib/getImgByNames4web?package_name=CE6851-48S6Q-HI_pic.zip&picture_name=rear.png
  - https://support.huawei.com/enterprise/zh/doc/EDOC1000019242/a1d7e273
  - https://revodistribution.com/parts/huawei-ce6851-48s6q-hi
identity_resolution:
  - Screenshot row 13 port thumbnail is a resized copy of Huawei official rear.png (NCC 0.922144).
  - Screenshot row 13 power thumbnail is a resized copy of Huawei official front.png (NCC 0.889632).
  - The matched official power-side photograph visibly reads PAC-600WA-B twice and FAN-40EA-B twice.
  - Huawei defines the B modules as back-to-front/power-panel-side exhaust; the resulting chassis airflow is port-side intake.
  - Huawei ordering table maps this complete dual-AC, dual-fan, port-side-intake assembly uniquely to 02350JAS / CE6851-HI-B-B0A.
status: VERIFIED

