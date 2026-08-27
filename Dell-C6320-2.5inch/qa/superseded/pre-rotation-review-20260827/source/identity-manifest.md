# Assembly identity manifest

manufacturer: Dell
requested_product_id: PowerEdge C6320 / 2.5-inch
delivery_subject: enclosure-with-modules
host_enclosure_model: PowerEdge C6300 enclosure, regulatory model B08S
installed_module_model: PowerEdge C6320 two-socket compute sled (not C6320p)
installed_module_count: 4
installed_module_positions: rear 2 columns x 2 rows, positions 1-4 all populated
front_backplane_or_drive_configuration: 24 x 2.5-inch SFF hot-swap bays, one vertical row, six bays assigned to each of four system boards; 2.5-inch expander-capable backplane; all 24 carrier fronts present; one narrow non-usable drive cover at far right before the right control panel
rear_io_or_controller_configuration: four identical C6320 sled rears; each has one PCIe Gen3 x16 half-height blank/grille, one USB 3.0 port, two embedded 10GbE SFP+ ports, one dedicated iDRAC8 RJ45 management port, one USB-to-serial port, one VGA port, and one power/status button
bezel_and_blanking_panel_state: no front bezel; 24 vertical 2.5-inch carrier fronts installed; PCIe rear positions use the photographed vented/blank carrier style; no empty sled slot
power_and_fan_configuration: 2 x matching 1400 W AC hot-plug shared PSUs, stacked at rear physical right / screen left, each with round fan guard, IEC AC inlet and orange release/indicator part; no HVDC and no mixed 1400/1600 W pair; internal shared fan cage has four fans
factory_branding: preserve Dell mark on the left front control panel and POWEREDGE C6320/Dell factory markings on rear sled pull-label areas where visible; do not use C6320p branding
u_height: 2U (86.8 mm)
orientation: right-handed glTF; +X device right seen from front, +Y up, +Z front
dimension_subject: fully installed C6300 enclosure with four C6320 nodes
chosen_overall_dimensions_mm: 482.3 W x 86.8 H x 795.9 D
evidence_urls:
  - https://www.dell.com/support/manuals/en-us/poweredge-c6300/c6320_pub
  - https://www.dell.com/support/manuals/en-us/poweredge-c6320/c6320_pub/chassis-dimensions?guid=guid-1b6d8b76-78e6-4872-b103-de2c091cedf3&lang=en-us
  - https://dl.dell.com/topicspdf/poweredge-c6320_Owners-Manual_en-us.pdf
  - https://i.dell.com/sites/doccontent/shared-content/data-sheets/en/Documents/Dell-PowerEdge-C6320-Spec-Sheet.pdf
  - https://www.ebay.ca/itm/175404082673
  - https://itinstock.com/dell-poweredge-c6300-node-server-4x-c6320-w-2x10c-e5-2650v3-128gb-ram-12tb-hdd-61070-p.asp
user_row_source: source/originals/user-screenshot.png; C6320/2.5-inch row only
status: VERIFIED

## Assembly exclusions

- Do not deliver a standalone C6320 sled.
- Do not substitute a bare C6300 chassis, C6320p/Xeon Phi sled, C6400/C6420, C6200/C6220, or any other generation.
- Do not mix 3.5-inch front, 12-drive front, 1600 W PSU geometry, HVDC labeling, missing sleds, or differing rear adapters.
- Front mounting ears are modeled at the front plane. Their wider silhouette may be visible from the rear; no separate rear-ear geometry is inferred.

## Dimension decision

The current Dell online C6320 manual identifies the delivery host as the PowerEdge C6300 enclosure and gives Xa 482.3, Xb 448.0, Y 86.8, Za without bezel 41.4, Zb 762.1 and Zc 795.9 mm. An older downloadable C6320 manual revision gives 482.4, 448.0, 86.8, 28.2, 764.2 and 790.3 mm for the “C6320 system.” Because the delivery subject is explicitly the complete C6300 enclosure with installed C6320 sleds, the current host-enclosure row is the binding scale. The older row remains visual/history evidence only and is not blended into geometry.
