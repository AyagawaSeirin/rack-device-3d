# Assembly identity manifest — Cisco Nexus 9336PQ

manufacturer: Cisco Systems, Inc.
requested_product_id: N9KC9336 (normalized/truncated screenshot label)
resolved_product_id: N9K-C9336PQ
hardware_revision_visible_in_exact-unit_photos: V02
equipment_type: fixed ACI spine switch
delivery_subject: complete-appliance
host_enclosure_model: N9K-C9336PQ
installed_module_model: not modular; fixed 36-port chassis
installed_module_count: not applicable
installed_module_positions: not applicable
front_backplane_or_drive_configuration: 36 fixed 40-Gigabit QSFP+ ports; empty cages; ports 1–36 left-to-right in 18 vertical pairs
rear_io_or_controller_configuration: power-supply side with PS1 left, two fan modules center, PS2 right; no rear network I/O
bezel_and_blanking_panel_state: no bezel; no port transceivers; both fan bays and both PSU bays populated; no blanking plates
power_and_fan_configuration: 2 × N9K-PAC-1200W V01 1200-W AC port-side-intake PSUs with burgundy latches; 2 × N9K-C9300-FAN3 port-side-intake fan modules with burgundy stripes; homogeneous port-side-intake airflow; 1+1 power redundancy
airflow: port-side intake, power-supply-side exhaust
u_height: 2U
body_dimensions: 445 mm W × 89 mm H × 571 mm D (official rounded metric values; source states 17.5 × 3.5 × 22.5 in)
rack_hardware: two N9K-C9300-RMK front-mount brackets attached at the port side, as shown by the user row and exact-unit photos; no rear ears
branding: factory Cisco logo and CISCO NEXUS C9336PQ badge retained
user_configuration_lock: source/originals/user-screenshot.png, final row; exact front/rear thumbnails show the 2U 36-QSFP layout and burgundy PSU latches
evidence_urls:
  - https://www.cisco.com/c/en/us/td/docs/switches/datacenter/nexus9000/hw/aci_9336pq_hig/guide/b_n9336PQ_hardware_install_guide/b_n9336PQ_hardware_install_guide_chapter_01010.html
  - https://www.cisco.com/c/en/us/td/docs/switches/datacenter/nexus9000/hw/aci_9336pq_hig/guide/b_n9336PQ_hardware_install_guide.pdf
  - https://www.cisco.com/c/en/us/products/collateral/switches/nexus-9000-series-switches/datasheet-c78-731792.html
  - https://www.cisco.com/c/dam/assets/prod/switches/nexus-9000-series/nexus-9336pq-aci-spine-3d-model.html
  - https://www.ebay.com/itm/165588009864
identity_reasoning: The screenshot abbreviation omits PQ, but its 2U two-row 36-QSFP port side and power side with two central large fan modules match N9K-C9336PQ and conflict with the 1U 9336C/FX2 family. The screenshot's two burgundy PSU latches match N9K-PAC-1200W. Exact-unit photos expose N9K-C9336PQ V02, N9K-PAC-1200W V01 and N9K-C9300-FAN3 labels. Cisco specifies burgundy as port-side intake and requires PSU/fan airflow to match. This makes the physical installed variant uniquely resolvable.
status: VERIFIED

## Explicit exclusions

- N9K-C9336C-FX2 / -FX2-E / later 9336C variants: 1U and materially different exterior.
- N9K-PAC-1200W-B and N9K-C9300-FAN3-B: blue port-side-exhaust modules; colors do not match the screenshot lock.
- N9K-PUV-1200W or DC supplies: wrong input type/color and excluded by the user's AC requirement.
- Any transceiver-populated or cabled port configuration: not present in the screenshot.

