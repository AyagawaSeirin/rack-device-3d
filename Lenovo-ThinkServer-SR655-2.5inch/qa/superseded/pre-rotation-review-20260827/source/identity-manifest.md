# Identity manifest

manufacturer: Lenovo
official_product_name: Lenovo ThinkSystem SR655
user_label: Lenovo ThinkServer SR655 / 2.5-inch
requested_product_id: SR655
generation: original SR655; machine types 7Y00 / 7Z01; SR655 V3 explicitly excluded
delivery_subject: complete-appliance
host_enclosure_model: B5VJ — ThinkSystem SR655 24x2.5-inch chassis
installed_module_model: not a modular rack enclosure
installed_module_count: not applicable
installed_module_positions: not applicable
front_backplane_or_drive_configuration: 24 visible 2.5-inch hot-swap carrier fronts in one horizontal row, positions 0-23; exterior locked to the official public viewer 24x2.5 state and the user screenshot; internal media/protocol are not asserted because SAS/SATA, NVMe, and mixed backplanes share this carrier-level exterior
rear_io_or_controller_configuration: PCIe-rich rear with eight slots in 3+3+2 banks; two-port OCP 3.0 area, BMC management RJ45, VGA, two USB, serial and NMI; no rear drives
bezel_and_blanking_panel_state: no security bezel; twenty-four visible black carriers/fillers with red upper latch accents; factory Lenovo/ThinkSystem and SR655 markings retained
power_and_fan_configuration: two installed Lenovo 750W hot-swap AC PSUs with IEC C14 inlets, fan grilles, green status indicators and orange ejector handles; six internal fans are documented but not externally visible in the closed delivery subject
airflow: ordinary closed SR655 airflow path; no separate exterior airflow SKU
u_height: 2U
body_width_mm: 444.6
overall_width_mm: 482.0
height_mm: 86.5
overall_depth_mm: 764.7
published_dimension_includes: overall width includes rack latches; depth includes rack latches and excludes security bezel
coordinate_convention: right-handed glTF; +X device right from front, +Y up, +Z front
status: VERIFIED

## Evidence lock

- User list screenshot row 5 directly shows the 24-carrier 2.5-inch front and PCIe-rich rear with two AC PSUs. The thumbnail is a configuration/style clue, not a final texture.
- Lenovo Quick Start figures 1-3 distinguish 8, 16 and 24 front 2.5-inch configurations; Figure 3 shows positions 0-23. Figure 6 proves the eight-slot rear.
- Lenovo Press Product Guide names B5VJ as the 24x2.5-inch physical chassis and documents the 24-bay SAS/SATA, NVMe and mixed backplane choices, all within the same front carrier envelope.
- The public Lenovo InfinityRT viewer contains an exact 24x2.5 model group. It was independently selected together with the PCIe-rich rear and two 750W AC PSUs.
- The official viewer proves distinct physical left/right panels, the top and bottom, and two authoritative three-quarter views.

There are no unresolved non-bottom identity or configuration gaps.
