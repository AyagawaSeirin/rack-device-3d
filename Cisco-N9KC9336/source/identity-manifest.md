# Assembly identity manifest

manufacturer: Cisco Systems, Inc.
requested_product_id: `N9KC9336` (screenshot shorthand)
identity_resolution_method: The screenshot's 36-port front face and rear `PSU + 3 fan trays + management cluster + PSU` sequence were compared feature-by-feature with Cisco's official N9336C-FX2 figures and hardware guide, resolving the chassis to `N9K-C9336C-FX2`.
delivery_subject: enclosure-with-modules
host_enclosure_model: `N9K-C9336C-FX2`
installed_module_model: 2 × `NXA-PAC-1100W-PI2` AC PSU; 3 × `NXA-FAN-65CFM-PI` fan tray
installed_module_count: 2 power-supply modules; 3 fan modules
installed_module_positions: PSU slot 1 at rear left; fan slots 1–3 across the rear center-left; management/console cluster at rear center-right; PSU slot 2 at rear right
front_backplane_or_drive_configuration: 36 fixed 40/100-Gigabit QSFP28 ports, arranged as 18 vertical two-port cages; no transceivers or cables installed in the screenshot
rear_io_or_controller_configuration: one RJ-45 out-of-band management port, one RS-232 console port, one SFP out-of-band management port, one USB port, BCN/STS LEDs, two PSUs, and three fan modules
bezel_and_blanking_panel_state: no front bezel; all 36 QSFP28 cages visible and empty; both PSU slots and all three fan slots populated
power_and_fan_configuration: 2 × `NXA-PAC-1100W-PI2` 1100-W AC PSU and 3 × `NXA-FAN-65CFM-PI` fan tray, all port-side intake with burgundy handles/latches; 1+1 PSU redundancy
u_height: 1 RU (official physical height 1.72 in / 4.4 cm)
published_dimensions: 17.3 in (43.9 cm) wide; 24.5 in (62.3 cm) deep with handles; 1.72 in (4.4 cm) high
evidence_urls:
  - https://www.cisco.com/c/en/us/td/docs/switches/datacenter/nexus9000/hw/n9336cfx2_hig/guide/b_n9336cFX2_nxos_hardware_installation_guide/b_n9336cFX2_nxos_hardware_installation_guide_chapter_01.html
  - https://www.cisco.com/c/en/us/td/docs/switches/datacenter/nexus9000/hw/n9336cfx2_hig/guide/b_n9336cFX2_nxos_hardware_installation_guide/b_n9336cFX2_nxos_hardware_installation_guide_appendix_0111.html
  - https://www.cisco.com/c/en/us/products/collateral/switches/nexus-9000-series-switches/datasheet-c78-742282.html
  - /root/.codex/attachments/6a010f6b-ae9b-41fb-95ff-f3eb06548688/codex-clipboard-125b3551-b9d1-4a93-ac51-15efd4ea24e5.png
status: VERIFIED

## Configuration lock

The original screenshot proves the chassis layout, installed counts, AC inlets, and port-side-intake color but not the module labels. The current task explicitly resolves the remaining BOM to two `NXA-PAC-1100W-PI2` PSUs and three `NXA-FAN-65CFM-PI` fan trays. An exact-configuration reseller listing independently states the same BOM, and an inspected high-resolution intake rear photograph shows the three `NXA-FAN-65CFM-PI` labels and burgundy hardware.

## Delivery state

The assembly-identity gate is satisfied. Six-face generation and exterior modeling may proceed. Exact underside imagery remains unavailable after required search escalation, so only the documented bottom-only fallback is permitted; this changes the maximum final status to `PASS_WITH_BOTTOM_FALLBACK` without relaxing any other face.
