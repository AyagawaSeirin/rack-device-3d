# Dell PowerEdge R620 10×2.5 SFF identity manifest

- manufacturer: Dell
- requested_product_id: PowerEdge R620
- delivery_subject: complete-appliance
- host_enclosure_model: PowerEdge R620 10-drive-bay chassis (not R620 8-drive chassis; not R620xd; not R720)
- installed_module_model: N/A
- installed_module_count: N/A
- installed_module_positions: N/A
- front_backplane_or_drive_configuration: fixed 10×2.5-inch SAS/SATA SFF backplane; two rows × five columns; ten Dell 2.5-inch carriers installed; no front bezel
- rear_io_or_controller_configuration: mandatory three-low-profile-PCIe-slot rear; iDRAC7 Enterprise RJ45; DB9 serial; DB15 VGA; two USB 2.0; Intel I350/Broadcom 5720 class quad 1GbE Base-T RNDC rendered as four RJ45 ports; no SFP+; three perforated low-profile slot blanks
- bezel_and_blanking_panel_state: front bezel absent; all ten carriers present; three PCIe slots closed by ventilated factory blanks
- power_and_fan_configuration: two matching 750 W hot-plug AC PSUs, IEC C14 inlets, translucent handles, orange release latches, rear fans; no DC terminal block; seven internal fans are not externally exposed
- rack_hardware: separate front latch/ear assemblies only; no invented rear ears
- u_height: 1U
- generation: Dell PowerEdge 12th generation
- coordinate_convention: right-handed glTF; +X device right as seen from front, +Y up, +Z front
- user_screenshot_lock: source/originals/user-config-lock-screenshot.png, row 4; enlarged crops in source/user-lock/
- evidence_urls:
  - https://i.dell.com/sites/content/shared-content/data-sheets/en/documents/dell-poweredge-r620-technical-guide.pdf
  - https://dl.dell.com/topicspdf/poweredge-r620_owners-manual_en-us.pdf
  - https://www.dell.com/support/manuals/en-us/poweredge-r620/r620systemownersmanual-v1/back-panel-features-and-indicators
  - https://cloudninjas.com/products/dell-poweredge-r620-server
  - https://pcserverandparts.com/dell-poweredge-r620-10-bay-sff-server-2x-intel-xeon-e5-2670-2-60-ghz-8c-32gb-ddr3-4x-600gb-hdd-i350-h710-refurbished/
  - https://www.itcreations.com/product/144161
- status: VERIFIED

## Screenshot resolution decision

The enlarged front crop proves ten drive carriers: top row 0/2/4/6/8 and bottom row 1/3/5/7/9. The narrow control strip at device-left has the Dell/PowerEdge R620 marks, diagnostic LEDs, power controls, and mini-USB. It lacks the optical drive, horizontal LCD control strip, front VGA, dual full-size USB, and vFlash layout unique to the shorter eight-drive chassis.

The enlarged rear crop proves the three-low-profile-PCIe layout required by the ten-drive chassis, four same-family RJ45 apertures rather than a 2×SFP+ hybrid, and two AC-style IEC/fan PSU faces. The exact target is therefore the 10-drive R620 chassis despite the user-facing folder key remaining `Dell-R620-2.5inch`.

## Explicit exclusions

- R620 8×2.5 chassis: shorter (Zc 701.3 mm), different front control/optical/VGA layout; excluded.
- R620 2×SFP+ + 2×RJ45 RNDC: excluded; target is quad Base-T RJ45.
- R620 two-PCIe-slot rear: excluded; ten-drive target requires the three-slot rear.
- R620 DC PSU: excluded; target is matching dual AC.
- R720/R720xd and any 2U chassis: excluded.
- R620xd: no such delivery subject is used here.
