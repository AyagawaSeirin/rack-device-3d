# Assembly identity manifest

- manufacturer: Hewlett Packard Enterprise (HPE; period-correct front badge may show the HP roundel)
- requested_product_id: HPE ProLiant DL360 Gen9, 4 LFF / 3.5-inch chassis
- base_chassis_sku: 755259-B21 (HPE DL360 Gen9 4LFF Configure-to-Order chassis)
- delivery_subject: complete-appliance
- host_enclosure_model: HPE ProLiant DL360 Gen9 1U 4LFF chassis
- installed_module_model: not applicable
- installed_module_count: not applicable
- installed_module_positions: not applicable
- front_backplane_or_drive_configuration: four 3.5-inch LFF hot-plug SAS/SATA/SSD bays, one row of four; four HPE Smart Carrier-style carriers installed as locked by the user screenshot
- front_control_configuration: 4LFF universal media/control strip with optical slot, serial-label pull tab, optional front VGA, optional USB 2.0, Systems Insight Display/control area, USB 3.0, UID/NIC/health/power indicators; standard left/right front ears
- rear_io_or_controller_configuration: three PCIe blank/slot positions as shown by HPE; optional 4x1GbE FlexibleLOM installed; two rear USB 3.0; one optional DB9 serial installed; one dedicated iLO 4 RJ45; four embedded 1GbE RJ45; one VGA
- bezel_and_blanking_panel_state: no security bezel; PCIe positions and unused aperture areas closed by the screenshot/HPE-render-matched factory blanks
- power_and_fan_configuration: two HPE 500W Flex Slot hot-plug AC power supplies installed; two visible PSU fan/handle assemblies; seven internal hot-plug fan modules represented as separate geometry
- u_height: 1U
- coordinate_convention: right-handed glTF; +X device right from front, +Y up, +Z front
- user_configuration_lock: source/originals/user-config-lock-full.png, row 6 crop qa/reference/user-config-lock-row6.png
- front_variant_exclusion: do not use 8SFF/10SFF, Gen10, or any Gen9 front other than 4LFF
- rear_variant_exclusion: do not use the two-port QSFP/SFP FlexibleLOM rear, a missing-serial rear, a one-PSU rear, the alternate two-full-height-riser rear, or any Gen10 rear
- evidence_urls:
  - https://support.hpe.com/hpesc/public/docDisplay?docId=c04444501&docLocale=en_US
  - https://support.hpe.com/hpesc/public/docDisplay?docId=emr_na-c04443049
  - https://www.hpe.com/psnow/doc/c04346229.pdf
  - https://images10.newegg.com/User-Manual/User_Manual_59-108-646.pdf
  - https://newserverlife.com/configure/hp_proliant_dl360_gen9_4lff/
  - https://www.piospartslap.de/HP-Enterprise-ProLiant-DL360-G9-Server-2xE5-2690-V3-0GB-4-Bay-35-LFF-2x-25-Intern-SFF
- status: VERIFIED

The screenshot is the configuration authority. HPE documentation proves the 4LFF chassis identity, component names, physical compatibility and dimensions. Third-party photographs are used only where their visible configuration agrees with the screenshot and official diagrams.
