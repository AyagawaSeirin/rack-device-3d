# Assembly identity manifest

- manufacturer: Hewlett Packard Enterprise (HPE; chassis-era factory marks may use the HP roundel)
- requested_product_id: HPE ProLiant DL360 Gen9, 8 SFF / 2.5-inch physical chassis variant
- configure_to_order_chassis: 755258-B21
- delivery_subject: complete-appliance
- host_enclosure_model: HPE ProLiant DL360 Gen9 1U 8SFF chassis
- installed_module_model: HPE SFF Smart Carrier drive carriers; Universal Media Bay; HPE Flex Slot AC PSUs
- installed_module_count: 8 SFF carrier fronts; 1 Universal Media Bay; 2 AC PSUs
- installed_module_positions: drive bays 1-6 in a 2-row x 3-column block at device-left; bays 7-8 in a 2-row x 1-column block below/right of the Universal Media Bay; PSU 2 then PSU 1 from rear-view left to right
- front_backplane_or_drive_configuration: 8 SFF SAS/SATA/SSD hot-plug backplane, all eight carrier faces present; optional 2-SFF/10-SFF kit absent
- front_control_configuration: no security bezel; Universal Media Bay with slim optical drive, front VGA and USB; right status/control strip with power/health/NIC/UID indicators, Systems Insight Display treatment and one USB 3.0
- rear_io_or_controller_configuration: three PCIe blanking plates; FlexibleLOM blank; two stacked rear USB 3.0; optional DB9 serial installed; dedicated iLO 4 RJ45; embedded 4-port 1GbE 331i; rear VGA
- bezel_and_blanking_panel_state: no front security bezel; three rear PCIe blanks installed; FlexibleLOM blank installed; no empty PSU bay
- power_and_fan_configuration: two matched HPE 500W Flex Slot Platinum hot-plug AC PSUs, each with IEC C14 inlet, red release latch, pull handle and visible fan geometry; no DC PSU
- exterior_fan_configuration: system fan cage is internal and is not exposed; the two PSU rear fans are externally visible and must be modeled
- rack_hardware: separate HPE Quick Release left and right front ears; no inferred rear rack ears
- u_height: 1U
- body_dimensions_mm: 434.7 W x 43.2 H x 698.5 D
- rack_mounting_overall_width_mm: 482.6 nominal 19-inch span across front mounting ears
- configuration_lock: qa/reference/user-config-lock-row7.png from the user screenshot, row 7 (`HPE / DL360G9/2.5英寸`)
- evidence_urls:
  - https://www.hpe.com/psnow/downloadDoc/HPE%20ProLiant%20DL360%20Gen9%20Server-c04346229.pdf?form=false&hf=slim&id=c04346229.pdf&isFutureVersion=true&preview=false&servePdfFile=true&ver=44
  - https://support.hpe.com/hpesc/public/api/document/c04441985?v=1771326120000
  - https://support.hpe.com/hpesc/public/docDisplay?docId=c04444501&docLocale=en_US
  - https://visiocafe.info/downloads/hp/documents/VSD-DL360Gen9.pdf
- configuration_resolution: The tiny user thumbnail is visibly resampled and cannot determine carrier aspect. The official HPE maintenance figure and exact-device real photographs jointly prove the Gen9 8SFF 6+2 arrangement and override thumbnail interpolation artifacts while preserving the requested row's 8SFF/double-AC configuration.
- status: VERIFIED

