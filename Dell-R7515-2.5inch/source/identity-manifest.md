# Assembly identity manifest

- manufacturer: Dell Technologies / Dell EMC
- requested_product_id: PowerEdge R7515
- regulatory_model: E46S
- regulatory_type: E46S003
- delivery_subject: complete-appliance
- host_enclosure_model: PowerEdge R7515 2U rack chassis
- installed_module_model: not modular; one complete single-socket server
- installed_module_count: 1
- installed_module_positions: not applicable
- front_backplane_or_drive_configuration: 24 x 2.5-inch SFF front-accessible carriers, slots 0-23, one horizontal row of 24 vertically oriented carriers
- installed_front_drive_state: all 24 carrier/blank faces present; no missing opening
- bezel_and_blanking_panel_state: optional Dell 2U security bezel installed; black/graphite 13-cell staggered hexagonal grille, left key lock/release block, right fixed attachment block, centered factory `DELL EMC` emblem; underlying 24-SFF carriers remain installed
- front_control_state: narrow left status/health control strip; right control strip with power button, two USB 2.0 ports, iDRAC Direct Micro-AB USB, iDRAC Direct LED, VGA; slide-out information tag at lower right
- rear_drive_configuration: no rear drives and no rear-drive cage
- rear_io_or_controller_configuration: Riser 1B, slot 2 and slot 3 full-height/full-length x16 blanking plates; PCIe slot 4 and slot 5 blanking plates; optional LOM riser populated with two RJ45 ports; two onboard 1 GbE RJ45 ports; two USB 3.0; dedicated iDRAC RJ45; one DB-15 VGA; one DB-9 serial; CMA status port and system-ID button
- power_and_fan_configuration: two stacked hot-plug Dell EPP 750 W AC PSUs, both installed, IEC AC inputs and integral circular exhaust fans visible; internal six-fan row is present and represented wherever visible through exterior openings
- u_height: 2U
- front_configuration_lock: `source/originals/user-row11-front.png`
- rear_configuration_lock: `source/originals/user-row11-rear.png`
- primary_front_photo: `source/third-party/itcreations-r7515-front-bezel.png`
- primary_rear_photo: `source/third-party/bytestock-r7515-24sff-gallery-4.jpg`
- official_front_layout: `source/originals/official-front-24x2.5-manual.jpg`
- official_rear_layout: `source/originals/official-rear-no-rear-drives-manual.jpg`
- exclusions: PowerEdge R7525; every LFF/3.5-inch front; rear-drive configurations; DC/HVDC PSU faces; single-PSU blank; non-R7515 rear boards; bezel-removed final state
- evidence_urls:
  - https://www.dell.com/support/manuals/en-us/poweredge-r7515/per7515_ism_pub
  - https://dl.dell.com/content/manual22344309-dell-poweredge-r7515-installation-and-service-manual.pdf?language=en-us
  - https://dl.dell.com/content/manual23687584-dell-emc-poweredge-r7515-technical-specifications.pdf?language=en-us
  - https://i.dell.com/sites/csdocuments/product_docs/en/poweredge-r7515-technical-guide.pdf
  - https://blog.itcreations.com/dell-emc-poweredge-r7515-review/
  - https://shop.bytestock.com/dell-poweredge-r7515-24-x-2-5-2u-rack-server-configure-your-own-nvme
- status: VERIFIED

The screenshot row, exact-model manual, exact 24-SFF real-photo gallery, and exact review photograph agree on the installed front bezel and the no-rear-drive rear assembly. The rear is not borrowed from the R7525 or from an LFF record.
