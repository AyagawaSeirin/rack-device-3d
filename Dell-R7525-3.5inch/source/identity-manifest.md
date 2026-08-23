# Assembly identity manifest

manufacturer: Dell Technologies (Dell EMC)
requested_product_id: PowerEdge R7525
regulatory_model: E68S
regulatory_type: E68S001
delivery_subject: complete-appliance
host_enclosure_model: PowerEdge R7525 2U rack chassis
installed_module_model: not applicable
installed_module_count: not applicable
installed_module_positions: not applicable
front_backplane_or_drive_configuration: 12 x 3.5-inch/LFF hot-swappable SAS/SATA backplane; 4 columns x 3 rows; twelve Dell LFF carriers installed behind the bezel
front_bezel_state: installed; Dell EMC 2U honeycomb security bezel with LCD/navigation area and centered factory DELL EMC branding
front_control_configuration: left health/system-ID/Quick-Sync control strip; right power button, USB 2.0, iDRAC Direct Micro-AB, and front VGA control strip
rear_io_or_controller_configuration: no rear-drive module; four riser groups exposing eight PCIe slot positions; pictured BOSS S2 module/slot; rear handle; OCP 3.0 NIC area; two embedded NIC ports; dedicated iDRAC; one USB 2.0; one USB 3.0; rear VGA; system-ID button; optional DB9 serial card absent and its expansion filler retained
rear_storage_configuration: none
bezel_and_blanking_panel_state: bezel installed; all unused PCIe positions use the vented Dell filler pattern shown in the row-8 lock and Dell Figure 9
power_and_fan_configuration: two hot-plug 2400 W AC PSUs, redundant 1+1, one at each lower rear corner; each rear PSU fan and IEC C20 inlet visible; six internal hot-swap fan modules retained as modeled assemblies although hidden by the installed top cover
u_height: 2U
coordinate_convention: right-handed glTF; +X device right from front; +Y up; +Z front
configuration_lock: source/originals/user-row08-lock.png (user-provided screenshot, row 8)
evidence_urls:
  - https://www.dell.com/support/manuals/en-us/poweredge-r7525/r7525_ism_pub/front-view-of-the-system?guid=guid-6ee4302e-d12b-4757-8230-8a26b0a428ae&lang=en-us
  - https://www.dell.com/support/manuals/en-au/poweredge-r7525/r7525_ism_pub/rear-view-of-the-system?guid=guid-5ad00271-7f31-40ac-8491-663cd8b3c6ab&lang=en-us
  - https://www.dell.com/support/manuals/en-uk/poweredge-r7525/r7525_ts_pub/drives?guid=guid-bc918a74-5c23-4c92-b950-4d60a957acab&lang=en-us
  - https://dl.dell.com/topicspdf/poweredge-r7525_owners-manual_en-us.pdf
  - https://dl.dell.com/topicspdf/poweredge-r7525_owners-manual2_en-us.pdf
  - https://www.dell.com/support/contents/en-us/videos/videoplayer/how-to-replace-35x12-hdd-backplane-for-poweredge-r7525/6144984864001
status: VERIFIED

## Configuration exclusions

- Do not use the R7515 single-socket chassis or rear layout.
- Do not use any 2.5-inch/SFF front backplane or carrier grid.
- Do not use the XE9680 hex/honeycomb pattern.
- Do not add 2 x 2.5-inch or 4 x 2.5-inch rear-drive modules.
- Do not install the optional DB9 serial card because it is absent in the row-8 rear lock.
- Do not use DC PSUs or mix AC and DC.

