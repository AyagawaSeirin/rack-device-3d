# Assembly identity manifest

- manufacturer: Dell
- requested_product_id: PowerEdge R720
- delivery_subject: complete-appliance
- host_enclosure_model: PowerEdge R720 2U (not R720xd)
- installed_module_model: not applicable
- installed_module_count: not applicable
- installed_module_positions: not applicable
- front_backplane_or_drive_configuration: 8 x 3.5-inch LFF hot-plug positions, 2 rows x 4 columns, all eight factory carriers present
- rear_io_or_controller_configuration: standard R720 seven-slot rear; three low-profile PCIe blanks (1-3), four full-height PCIe blanks (4-7), dedicated iDRAC7 Enterprise RJ45, DB9 serial, VGA, two USB 2.0, four RJ45 Select Network Adapter ports
- bezel_and_blanking_panel_state: removable security bezel absent; all eight LFF carriers visible; all seven PCIe positions closed by factory perforated blanks
- power_and_fan_configuration: two installed hot-plug AC PSUs with IEC AC inlets and visible circular PSU fans; screenshot appearance matches 750 W modules
- u_height: 2U
- rack_hardware: front rack latches/ears only; no rear ears inferred
- branding: factory Dell and PowerEdge R720 markings retained
- configuration_lock: `source/originals/user-configuration-lock.png`, first row only
- exclusion_lock: no R720xd, no SFF, no R730, no rear flex-bay, no DC PSU, no bezel, no add-in card rear connectors
- evidence_urls:
  - https://downloads.dell.com/manuals/all-products/esuprt_ser_stor_net/esuprt_poweredge/poweredge-r720_reference-guide_en-us.pdf
  - https://dl.dell.com/topicspdf/poweredge-r720_owners-manual_en-us.pdf
- status: VERIFIED

## Configuration-lock reading

The user image first row explicitly labels `DELL R720/3.5英寸`. Its front crop shows the R720 LCD/control bar, optical bay and eight horizontally handled LFF carriers in a 2 x 4 arrangement with no security bezel. Its rear crop matches the Owner's Manual Figure 7 R720 rear, including the seven-slot arrangement and no R720xd rear flex-bay. It shows the quad-RJ45 network daughter card and two installed AC PSUs.

