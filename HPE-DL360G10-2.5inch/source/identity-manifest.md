# Assembly identity manifest

manufacturer: Hewlett Packard Enterprise (HPE)
requested_product_id: HPE ProLiant DL360 Gen10 8SFF 2.5-inch CTO appearance, product-family anchor 867959-B21
delivery_subject: complete-appliance
host_enclosure_model: HPE ProLiant DL360 Gen10 1U SFF chassis (HSTNS-2154 family)
installed_module_model: not modular; complete rack server
installed_module_count: n/a
installed_module_positions: n/a
front_backplane_or_drive_configuration: standard 8 SFF SAS/SATA cage only; six carriers in the left 3-column x 2-row block plus two lower-row carriers under the Universal Media Bay optical/display blank; no +2SFF/NVMe/uFF conversion and no upper-row UMB carriers
installed_front_carriers: eight visible HPE SFF Smart Carrier-style fronts in the official standard 6+2 arrangement, matching the user row-5 count
rear_io_or_controller_configuration: no rear drive; three PCIe apertures present and blanked; FlexibleLOM aperture blanked; embedded 4x1GbE RJ45 group; dedicated iLO RJ45; optional serial DB9 present; two USB 3.0; VGA; dual AC power modules
bezel_and_blanking_panel_state: no security bezel; front 8SFF carrier faces exposed; Universal Media Bay blank/grille exposed; PCIe and FlexibleLOM blanking panels installed
power_and_fan_configuration: two HPE 500W Flex Slot Platinum AC hot-plug PSUs visible at rear; seven internal fan positions are not exterior delivery geometry except where rear/top evidence proves vents
u_height: 1U
body_dimensions_mm: 434.6 W x 42.9 H x 707 D (SFF chassis)
overall_front_width_mm: 482.6 nominal 19-inch rack span including the two front ears
coordinate_convention: right-handed glTF; +X device right from front; +Y up; +Z front
user_configuration_lock: source/originals/user-row5-config.png (row 5 of supplied screenshot)
excluded_variants: 4LFF/3.5-inch; 8+2SFF; 10SFF NVMe Premium; rear +1SFF/uFF; DL360 Gen9; DL360 Gen10 Plus; DL360 Gen11/Gen12; DC power-supply variants; alternate NIC/PCIe card populations
evidence_urls:
  - https://support.hpe.com/hpesc/public/docDisplay?docId=a00115362en_us&page=GUID-A907F1AD-6041-4CD5-9C29-47DF3AC366A9.html
  - https://support.hpe.com/hpesc/public/docDisplay?docId=a00115362en_us&page=GUID-CCF447DF-671D-4F37-9C1A-B88D67163C92.html
  - https://www.hpe.com/psnow/doc/a00008159enw.pdf
  - https://www.itpro.com/server/29565/hpe-proliant-dl360-gen10-review
  - https://www.piospartslap.de/?a=22257&lang=eng
status: VERIFIED

## Configuration lock rationale

The user image is the authority for the physical variant and installed exterior. It shows eight, not ten, SFF positions; a right-side Universal Media Bay/control region; no rear drive; blank PCIe/FlexibleLOM regions; embedded four-port Ethernet; dedicated iLO; serial/USB/VGA; and two AC PSUs. HPE QuickSpecs and Maintenance Edition 19 independently prove the 8SFF layout, port identities, standard rear order, 1U form factor, and SFF dimensions. IT Pro's reviewed 867963-B21 8SFF system provides a straight rear photograph matching the user rear, including blank expansion areas and dual 500W AC PSUs. No incompatible front/rear options are combined.
