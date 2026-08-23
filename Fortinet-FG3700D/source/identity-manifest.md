# Assembly identity manifest

- manufacturer: Fortinet, Inc.
- product_family_marking: FortiGate
- requested_product_id: FortiGate 3700D / FG-3700D
- generation_suffix: D
- delivery_subject: complete-appliance
- host_enclosure_model: FG-3700D chassis
- installed_module_model: none; fixed appliance interfaces plus field-replaceable fan/PSU assemblies
- installed_module_count: 0 user I/O modules installed
- installed_module_positions: n/a
- front_backplane_or_drive_configuration: four empty QSFP+ cages (ports 1-4), twenty-eight empty SFP/SFP+ cages (ports 5-32), two RJ45 management ports, one RJ45 console, one USB-A and one USB mini-B; factory rack-mount brackets and handles installed; no NEBS air-filter cover
- rear_io_or_controller_configuration: no rear I/O/controller option; three central fan-grille trays with three visible rear rotor openings, six documented fan positions/indicators, and a ground terminal pair near device-right
- bezel_and_blanking_panel_state: no bezel; factory white sheet-metal/caution panels retained; no adjacent-model rear module or display panel
- power_and_fan_configuration: AC only, two 100-240 Vac hot-swappable redundant 1+1 PSUs; six documented fan positions with three rear-visible rotor openings
- supplied_but_not_installed: two SFP+ SR transceivers, six rubber feet, rail kit, middle brackets, cables
- u_height: 3U (133 mm)
- body_dimensions_mm: 437 W x 133 H x 579 D
- rack_mount_overall_width_mm: 482.6 nominal 19-inch rack span with installed brackets
- airflow: front-to-rear
- excluded_variants: FG-3700D-DC, FG-3700D-NEBS filter cover, FG-3700DX, FG-3800D, FG-3700F, FG-1500D, and the non-binding low-resolution mixed rear thumbnail in the request table
- evidence_urls:
  - https://docs.fortinet.com/document/fortigate/hardware/fortigate-3700d-qsg-supplement
  - https://fortinetweb.s3.amazonaws.com/docs.fortinet.com/v2/attachments/a8cceba0-1a0a-11e9-9685-f8bc1258b856/FG-3700D-Supplement.pdf
  - https://www.fortinet.com/content/dam/fortinet/assets/data-sheets/ja_jp/FGT3700DDS.pdf
  - https://fccid.io/ANATEL/00228-15-08867/FortiGate-3700D-manual/C91A7ACF-EABF-42DE-A7A2-2875B299D103
  - https://www.ebay.com/itm/236708345684
  - https://www.ebay.com/itm/236755802715
- status: VERIFIED

## Thumbnail reconciliation

The request table row correctly identifies the front as FG-3700D. Its rear thumbnail is too small to establish fan count or panel boundaries and does not agree one-for-one with the Fortinet QSG/FIPS diagrams, ANATEL exact-PID photographs, and two independent FG-3700D AC listings. It is retained only as request context. The build freezes the cross-verified D-generation rear: two AC PSUs at the extremes, three square-perforated central fan trays, six fan positions/indicators, and the right-side grounding posts. This avoids creating a hybrid with an adjacent FortiGate generation.
