# Assembly identity manifest

manufacturer: Lenovo

user_label: Lenovo ThinkServer SR655 / 3.5-inch

resolved_official_product_id: Lenovo ThinkSystem SR655 (original generation, not SR655 V3)

machine_types: 7Y00, 7Z01

frozen_cto_base: 7Z01CTO1WW (3-year base warranty; warranty machine type does not change the documented exterior)

delivery_subject: complete-appliance

host_enclosure_model: ThinkSystem SR655 2U rack server

installed_module_model: not modular; complete single-socket server appliance

installed_module_count: 1 complete appliance

installed_module_positions: n/a

front_chassis_feature: B5VK — ThinkSystem SR655 12x3.5-inch chassis

front_backplane_or_drive_configuration: AUR9 — 12x3.5-inch SAS/SATA backplane; twelve visible 3.5-inch hot-swap carrier fronts in a 3-row x 4-column arrangement; internal drive capacities are not asserted

rear_io_or_controller_configuration: PCIe-rich rear, eight PCIe slots, no rear drive bays; two-port OCP 3.0 Ethernet adapter; BMC RJ45, VGA, two USB-A, serial, NMI and status LEDs

bezel_and_blanking_panel_state: no security bezel; all eight PCIe openings carry the factory perforated blanking/slot covers shown in the screenshot and official Figure 3

power_and_fan_configuration: two identical 750W AC hot-swap PSUs with C14 inlets and orange release handles; official candidate 7N67A00883 / B6XT Platinum; six internal hot-swap fans, externally hidden under the closed cover

front_io_state: optional front VGA present on left rack latch; right front I/O/control module and two USB-A ports present

u_height: 2U

airflow: front-to-rear; exterior fan subtype does not change the closed-chassis appearance and is not inferred beyond the six hot-swap fan positions proven by the official viewer

dimensions_mm: overall 482.0 W x 86.5 H x 764.7 D; body width 444.6 (published rounded value 445); detailed product-guide height 87 and depth 764

coordinate_convention: right-handed glTF; +X device right when seen from front, +Y up, +Z front

branding_policy: preserve authentic Lenovo, ThinkSystem and SR655 markings in their factory positions and readable orientation; do not invent serial numbers, QR content or unproven labels

evidence_urls:

- https://dcsc.lenovo.com/#/categories/STG%40Servers%40Rack%20Server%40ThinkSystem%20SR655
- https://pubs.lenovo.com/sr655/
- https://lenovopress.lenovo.com/lp1161-thinksystem-sr655-server
- https://lenovopress.lenovo.com/3dtours/sr655/
- https://www.ebay.com/itm/206238343567

identity_resolution_notes:

- The user screenshot says “ThinkServer”; Lenovo's authoritative name for SR655 types 7Y00/7Z01 is “ThinkSystem SR655”. “ThinkServer” is retained only as the requested folder/key label.
- The screenshot has no V3 suffix and matches the original-generation front latches and rear layout. SR655 V3 is excluded.
- DCSC's public original-generation page exposes 7Z01CTO1WW. The 7Y00/7Z01 distinction is warranty/base ordering, with no documented exterior difference. The physical exterior lock is therefore B5VK + AUR9 + the screenshot/official Figure 3 rear configuration.
- The official 3D viewer's PCIe-rich section explicitly states “12x 3.5-inch chassis” and “Up to 8x PCIe slots”.
- The official product-guide Figure 3 exactly matches the requested rear and visibly labels both installed PSUs “750W AC”. Product-guide page 81 confirms all supported AC PSU variants use C14 connectors.

status: VERIFIED

