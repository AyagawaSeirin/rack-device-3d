# Assembly identity manifest

- manufacturer: Dell
- requested_product_id: PowerEdge R730, regulatory model E31S / type E31S001
- delivery_subject: complete-appliance
- host_enclosure_model: PowerEdge R730 2U rack chassis
- installed_module_model: not applicable
- installed_module_count: not applicable
- installed_module_positions: not applicable
- front_backplane_or_drive_configuration: 8 × 3.5-inch/LFF hot-swap SAS/SATA backplane; two rows × four columns; eight Dell LFF carriers installed
- rear_io_or_controller_configuration: standard R730 rear, no R730xd rear flex-bay; seven PCIe positions covered by factory perforated blanks; iDRAC8 Enterprise RJ45; DB9 serial; VGA; two USB 3.0; four RJ45 network daughter-card ports
- bezel_and_blanking_panel_state: front security bezel absent; all eight LFF carrier fronts present; optical drive present; PCIe positions blanked
- power_and_fan_configuration: two hot-swap 750 W AC PSUs installed, IEC AC inlets, orange release tabs, integral fans; six internal hot-swap fan modules represented where visible through the open front airflow path
- front_control_configuration: left control block with Dell and PowerEdge R730 markings, power/NMI/system-ID controls, VGA, LCD navigation and pull-out information tag; central iDRAC Direct/USB block; optical drive at upper right
- u_height: 2U
- body_width_mm: 444.0
- overall_width_mm: 482.4
- height_mm: 87.3
- body_depth_mm: 684.0
- overall_depth_mm: 723.0
- front_projection_mm_without_bezel: 18.0
- front_projection_mm_with_bezel: 32.0 (not installed; dimensional reference only)
- rear_projection_mm: 39.0 nominal difference between Zc and Zb, dominated by PSU/rear handles
- user_configuration_lock: `source/originals/user-row12-r730-lff.png`, extracted unchanged from row 12 of the supplied second screenshot
- evidence_urls:
  - https://www.dell.com/support/manuals/en-us/poweredge-r730/r730_ompublication/35-inch-hard-drive-chassis?guid=guid-cf7676b4-eb53-47a8-8ffb-34a74ca4f4a4&lang=en-us
  - https://www.dell.com/support/manuals/en-us/poweredge-r730/r730_ompublication/back-panel?guid=guid-1dc323f8-8173-4723-8bac-b781cdb7fc9b&lang=en-us
  - https://i.dell.com/sites/csdocuments/Shared-Content_data-Sheets_Documents/en/us/Dell-PowerEdge-R730-and-R730xd-Technical-Guide-v1-7.pdf
  - https://www.ebay.com/itm/387258968614
  - https://www.youtube.com/watch?v=OSV3PdYySjM
  - https://www.youtube.com/watch?v=CVg_X-OO9Kc
- excluded_lookalikes: PowerEdge R730xd; every SFF/2.5-inch R730; PowerEdge R720/R720xd; any rear with two rear drive bays; DC PSUs; single-PSU or PSU-blank configurations
- status: VERIFIED

## Configuration lock decision

The screenshot row shows the standard R730 8-LFF face: exactly eight large carriers in a 2 × 4 arrangement, no security bezel, and the standard R730 rear without R730xd rear drives. Its rear silhouette and group order match the official R730 back view and the real 8-LFF sources retained here. The build therefore freezes the photographed standard seven-slot rear, four-RJ45 NDC and two AC PSUs. No optional PCIe add-in card is invented.

