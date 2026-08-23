# Assembly identity manifest

manufacturer: Dell
requested_product_id: PowerEdge R730
regulatory_model: E31S Series
regulatory_type: E31S001
delivery_subject: complete-appliance
host_enclosure_model: Dell PowerEdge R730 2U rack chassis
installed_module_model: not modular; complete R730 appliance
installed_module_count: not applicable
installed_module_positions: not applicable
front_backplane_or_drive_configuration: 16 x 2.5-inch SFF SAS/SATA hot-plug backplane; sixteen installed Dell 2.5-inch hot-plug carriers in slots 0-15
front_bezel_state: removable security bezel absent
front_control_area: Dell logo; round power button; NMI and system-ID controls; VGA; three LCD navigation buttons; blue LCD under the factory PowerEdge R730 wordmark; information tag; optical-drive slot; vFlash slot; two USB 2.0 ports including iDRAC Direct; large square-hole intake grille
rear_io_or_controller_configuration: screenshot-locked standard R730 rear; all seven PCIe/riser positions 1-7 fitted with vented blank covers; dedicated iDRAC8 RJ45; DB9 serial; DB15 VGA; two stacked USB; four-port 1GbE NDC; no rear flex-bay and no add-in-card external ports
bezel_and_blanking_panel_state: front bezel absent; sixteen carriers installed; all seven rear PCIe positions blanked
power_and_fan_configuration: two installed hot-plug Dell EPP 750 W AC PSUs, IEC C14 inlets, fan grilles, orange release latches and black pull handles; no DC PSU
u_height: 2U
branding_state: retain factory Dell and PowerEdge R730 marks; retain small factory port labels and PSU EPP 750W marks where readable; do not introduce Dell EMC branding on the front control strip
configuration_lock: /root/Project/rack-device-3d/Dell-R730-2.5inch/source/user-lock/row-13-r730-sff.png
configuration_lock_sha256: 5095e7936db12a4b2577c656142b89f554c75f447958ef88bef35fee5dfd9e9a
excluded_families_and_variants: R730xd; R720/R720xd; any 8x3.5 LFF front; any 8x2.5 front; any R730xd rear flex drives; any rear fitted add-in-card ports; any single PSU or DC PSU; any front bezel
primary_official_configuration_evidence:
  - https://i.dell.com/sites/doccontent/shared-content/data-sheets/en/Documents/Dell-PowerEdge-R730-and-R730xd-Technical-Guide-v1-7.pdf (pp. 13-15 and 57-58)
  - https://www.dell.com/support/manuals/en-us/poweredge-r730/r730_ompublication/25-inch-hard-drive-chassis?guid=guid-d289ce54-d940-46a4-b22c-f4092f561b4e
  - https://www.dell.com/support/manuals/en-us/poweredge-r730/r730_ompublication/back-panel?guid=guid-1dc323f8-8173-4723-8bac-b781cdb7fc9b
  - https://www.dell.com/support/manuals/en-us/poweredge-r730/r730_ompublication/expansion-bus-specifications?guid=guid-25fe748e-f8c6-463e-846d-d489758b0870
status: VERIFIED

## Lock rationale

The user screenshot row and Dell's technical guide agree on the no-bezel 16-SFF R730 front. The screenshot rear agrees feature-for-feature with Dell Figure 5: three half-height blanks (slots 1-3), two full-height blanks (4-5), two full-height blanks (6-7), four RJ45 NDC ports, standard management/video/USB cluster, upper-right perforated grille and two AC PSUs. Dell publishes one R730 rear view for the supported R730 front chassis choices and a separately different R730xd rear; the build therefore uses the R730 rear only and explicitly excludes the R730xd flex-bay rear.

