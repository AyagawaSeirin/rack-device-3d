# Dell PowerEdge R240 3.5-inch/LFF assembly identity

- manufacturer: Dell EMC
- requested_product_id: PowerEdge R240, regulatory model E57S Series, regulatory type E57S001
- delivery_subject: complete-appliance
- host_enclosure_model: PowerEdge R240 1U rack chassis
- installed_module_model: not applicable
- installed_module_count: not applicable
- installed_module_positions: not applicable
- front_backplane_or_drive_configuration: 4 x 3.5-inch/LFF hot-swappable SAS/SATA/SSD backplane; one row of four installed Dell 14G LFF carrier fronts; no security bezel; optional optical-drive position present as the factory blank/closed panel shown by the locked configuration
- rear_io_or_controller_configuration: onboard serial, VGA, dedicated iDRAC RJ45, two onboard 1GbE RJ45, two USB 3.0, system ID and CMA/status ports; one half-height and one full-height PCIe opening, both with factory blanking plates; no added rear NIC/HBA face
- bezel_and_blanking_panel_state: security bezel absent; four hot-swap carrier faces present; both PCIe openings blanked
- power_and_fan_configuration: four single-rotor cabled cooling fans; one installed fixed/cabled AC PSU in the factory rear-right position. The R240 is non-redundant and does not support dual PSUs. Official evidence permits 250 W Bronze or 450 W Platinum; the user screenshot and cross-locked review unit match the 250 W Bronze exterior, whose externally visible rear structure is one IEC inlet, BIST LED/button and twin exhaust fields.
- u_height: 1U
- body_dimensions_mm: 434.0 W x 42.8 H x 534.496 D from Dell's chassis ledger
- overall_dimensions_mm: 482.0 W x 42.8 H x 573.596 D without security bezel; 22.0 mm verified front projection and approximately 17.1 mm residual rear projection
- coordinate_convention: right-handed glTF; +X device right seen from front, +Y up, +Z front
- evidence_urls:
  - https://www.delltechnologies.com/asset/en-us/products/servers/technical-support/poweredge-r240-technical-guide.pdf
  - https://www.dell.com/en-au/shop/dell-poweredge-servers/poweredge-r240-rack-server/spd/poweredge-r240/4er2400301auoo
  - https://www.etb-tech.com/dell-poweredge-r240-1x4-3-5-1-x-e-2224-3-4ghz-quad-core-32gb-4-x-12tb-7-2k-sata-perc-h330-idrac9-basic-svr-r240-005.html
  - https://techmikeny.com/products/dell-poweredge-r240-server-4-bay-lff-4-00ghz-6-core-24gb-ram-40tb-hdds-rails
  - https://www.servethehome.com/dell-emc-poweredge-r240-review-1u-entry-server/
  - https://www.youtube.com/watch?v=FGw0nzLS6rU
- user_configuration_lock: source/originals/user-configuration-lock.png, fifth readable equipment row
- status: VERIFIED

## Variant exclusion

The screenshot row is visually consistent with Dell's Figure 2 hot-swappable 4 x 3.5-inch system and with ETB/NewServerLife/Cloud Ninjas photographs. It is not the Figure 3 cabled-carrier face, the 2 x 3.5-inch cabled face, a 2.5-inch/SFF face, or a PowerEdge R340. R340 dual-redundant PSU geometry is explicitly excluded. “Dual PSU” cannot be represented without making a mechanically impossible hybrid.
