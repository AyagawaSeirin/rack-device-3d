# Dell PowerEdge R630 10×2.5-inch SFF identity manifest

- manufacturer: Dell
- requested_product_id: PowerEdge R630
- generation: 13G
- delivery_subject: complete-appliance
- host_enclosure_model: PowerEdge R630 long chassis for 10×2.5-inch / 24×1.8-inch variants
- installed_module_model: not applicable
- installed_module_count: not applicable
- installed_module_positions: not applicable
- front_backplane_or_drive_configuration: 10×2.5-inch SFF SAS/SATA hot-plug backplane, five columns by two rows; ten visible SFF carrier/handle assemblies; no optical bay
- rear_io_or_controller_configuration: three-riser chassis with three low-profile PCIe blanking plates; system-ID button/connector; iDRAC8 Enterprise RJ45; DB9 serial; VGA; two stacked USB 3.0; quad-RJ45 network daughter card; no add-in-card ports exposed
- bezel_and_blanking_panel_state: front bezel absent; all ten SFF carrier faces present; all three rear LP PCIe openings blanked
- power_and_fan_configuration: two matching Dell EPP AC hot-plug PSUs installed; IEC AC inlets, orange release tabs, pull handles, and rear fan geometry visible; no DC PSU and no PSU blank
- branding_state: retain physical Dell and PowerEdge R630 markings; retain the right-front Intel Xeon badge shown by the configuration lock and exact photos
- rack_hardware: separate front mounting ears/wing housings only; do not create rear ears; no external rails or cable-management arm
- u_height: 1U
- body_width_mm: 434.0
- overall_width_mm: 482.4
- height_mm: 42.8
- z_body_to_rear_outermost_mm: 731.0
- overall_depth_without_bezel_mm: 752.1
- front_projection_without_bezel_mm: 20.4
- coordinate_convention: right-handed glTF; +X device right as seen from front; +Y up; +Z front
- configuration_lock: `source/config-lock/row-3-r630-2.5inch.png`, SHA-256 `f16c31c90bcb9b26abacf665800525e5b83cff192a57a35821418b479270e2b5`
- evidence_urls:
  - https://i.dell.com/sites/doccontent/shared-content/data-sheets/en/Documents/Dell-PowerEdge-R630-Technical-Guide-v1-6.pdf
  - https://www.dell.com/support/manuals/en-us/poweredge-r630/r630_om_pub/three-riser-chassis?guid=guid-599100d8-eff9-4961-a285-accba372257d
  - https://www.dell.com/support/manuals/en-us/poweredge-r630/r630_om_pub/chassis-dimensions?guid=guid-60c95c46-c086-419b-8c1a-45a7e1b3d518&lang=en-us
  - https://techmikeny.com/products/dell-poweredge-r630-server-10-bay-sff-3-20ghz-16-core-128gb-ram-7-2tb-storage
  - https://www.ebay.com/itm/257483086393
- status: VERIFIED

## Configuration-lock interpretation

The user screenshot's third row is a bezel-less R630 10×2.5-inch face, not the 8-bay R630. The ten SFF faces form five vertical pairs. Its rear thumbnail matches the three-riser layout and dual-AC-PSU silhouette. The rear network block is locked to the quad-RJ45 option shown by the screenshot and corroborated by the exact-model manual/source set. Photos with two SFP+ plus two RJ45, empty PSU bays, installed add-in cards, a front bezel, rails, or seller cables are supporting evidence only and never override this manifest.
