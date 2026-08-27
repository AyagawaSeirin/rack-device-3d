# Assembly identity manifest

- manufacturer: Hewlett Packard Enterprise (HPE)
- requested_product_id: HPE ProLiant DL360 Gen10, 4LFF / 3.5-inch physical chassis variant
- configuration_basis_pid: 867958-B21 (HPE DL360 Gen10 4-LFF CTO Server, embedded-LOM generation)
- delivery_subject: complete-appliance
- host_enclosure_model: HPE ProLiant DL360 Gen10 1U 4LFF chassis
- installed_module_model: not applicable
- installed_module_count: not applicable
- installed_module_positions: not applicable
- front_backplane_or_drive_configuration: four 3.5-inch LFF SAS/SATA hot-plug positions in one row; four HPE LFF Smart Carrier fronts installed; no front security bezel; optical-drive bay blank; display-port/USB-2.0 option blank; standard Systems Insight Display/control cluster and front iLO Service/USB 3.0 areas preserved
- rear_io_or_controller_configuration: no rear SFF/uFF drive option; primary PCIe riser with slot 1 FH x16 and slot 2 LP x8 plus installed secondary slot 3 x16 riser, all visible slot openings closed by correct blanking plates; HPE Ethernet 1Gb 4-port 331i embedded NIC; HPE Ethernet 1Gb 4-port 331FLR FlexibleLOM; dedicated iLO 5 RJ45 management; optional serial DB9 installed; two rear USB 3.0; rear VGA
- smart_array_configuration: HPE Smart Array P408i-a SR Gen10 type-a controller, frozen as the HPE-documented 4LFF hardware RAID path; controller is internal and has no rear-facing connector
- bezel_and_blanking_panel_state: front bezel absent; four LFF carriers present; front ODD and display/USB option positions blank; rear PCIe openings blanked; no rear-drive cage
- power_and_fan_configuration: two HPE 500W Flex Slot Platinum Hot Plug Low Halogen power supplies, 94% efficiency, IEC AC input, 100-240 VAC; two-processor/secondary-riser build with seven standard hot-plug fans
- u_height: 1U
- canonical_dimensions_mm: height 42.9; body_width 434.6; front_rack_ear_span 482.6; body_depth_lff 749.8; final_handle_relief_depth 751.75
- front_rack_hardware: left and right front ears/control endcaps are separate mechanical parts; preserve HPE and ProLiant DL360 Gen10 factory branding; do not add rear ears
- user_configuration_lock: `source/originals/user-config-lock-screenshot.png`, row 4, SHA-256 `7efb5b4ccf0095fee7977f6a95083306935b9e63a990fd83bb8883fc49fdfeb9`
- generation_exclusions: Gen9, Gen10 Plus, Gen11, 8SFF, 10SFF/NVMe, rear-drive riser/cage, DC PSU, single-PSU, empty/blank FlexibleLOM, SFP/SFP28 FlexibleLOM, security bezel
- evidence_urls:
  - https://www.hpe.com/psnow/doc/a00008159enw
  - https://support.hpe.com/hpesc/public/docDisplay?docId=a00105399en_us&docLocale=en_US
  - https://support.hpe.com/hpesc/public/docDisplay?docId=a00018806en_us&docLocale=en_US
  - https://support.hpe.com/hpesc/public/docDisplay?docId=a00105399en_us&docLocale=en_US&page=GUID-F62BAF36-F686-4739-B014-C59E4D72641C.html
  - https://retail.era.ca/products/hpe-proliant-dl360-gen10-1u-3-5-1x-gold-6138-32gb-ddr4-ram-e208i-a-sr-gen10-10g-2x500w
- status: VERIFIED

## Lock interpretation

The user screenshot uses the same front and rear configuration shown in HPE QuickSpecs overview pages 4 and 6: 4LFF, the embedded four-port NIC, a four-port RJ45 FlexibleLOM, the optional serial port, the optional third PCIe slot, and two 500W/94% Flex Slot AC supplies. `867958-B21` is the CTO identity that includes the embedded 331i generation and therefore matches that rear; Network Choice `P19765-B21/P19776-B21` is retained only as exact 4LFF chassis/top photographic evidence because its NC rear lacks the embedded ports.

The QuickSpecs internal view identifies a type-a Smart Array and the official user guide provides the dedicated 4LFF-to-P408i-a cabling path. P408i-a is therefore frozen as the valid installed controller. It is fully internal, so this choice does not create an unverified exterior feature.
