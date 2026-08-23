# Juniper MX304 assembly identity manifest

- manufacturer: Juniper Networks (HPE Juniper Networking)
- requested_product_id: Juniper MX304, user screenshot second readable equipment row
- frozen_full_pid_and_variant: MX304-PREM-AC-FS physical configuration; chassis bundle MX304-PREM with AC rear
- delivery_subject: complete-appliance
- host_enclosure_model: JNP304/MX304 chassis (JNP304-CHAS physical enclosure)
- installed_module_model: JNP304-RE (standard Junos physical face) and MX304-LMIC16-BASE
- installed_module_count: 2 Routing Engines and 2 LMIC16 line cards
- installed_module_positions: RE0 top-left; RE1/LMIC2 occupied by RE1 top-right; LMIC0 bottom-left; LMIC1 bottom-right
- front_backplane_or_drive_configuration: four occupied front card positions; two JNP304-RE above two MX304-LMIC16-BASE; 32 empty QSFP-family port cages total; no installed transceivers; no blank panels
- rear_io_or_controller_configuration: AC rear; two JNP-PWR2200-AC power supplies in PSU0/PSU1 top-to-bottom; timing interface board between PSUs and Fan 0; three JNP-FAN-2RU modules in Fan 0/1/2
- bezel_and_blanking_panel_state: no optional cable-management brackets; no optional front air-filter cover/bezel; no blank card panels; factory rack ears installed
- power_and_fan_configuration: AC, 2 x JNP-PWR2200-AC, 2200 W class, 1+1 redundancy; 3 x JNP-FAN-2RU; front-to-back airflow with rear AIR OUT markings
- u_height: 2 U, 88.9 mm
- body_dimensions_mm: width 440.9; height 88.9; depth 610.0
- overall_dimensions_for_delivered_subject_mm: width 482.6 across front rack ears; height 88.9; depth 667.2 without optional cable-management brackets or optional air-filter cover
- optional_components_excluded: JNP-CABLEMGMT-2RU and JNP-FLTRDR-2RU external front cover assembly
- exact_bottom_evidence: not found after documented official, PDF, Browser, marketplace, video, teardown, and multilingual searches
- bottom_policy: GENERIC_BOTTOM_FALLBACK; conservative non-identifying opaque gray sheet metal; no unsupported holes, labels, vents, feet, rails, seams, fasteners, or branding
- evidence_urls:
  - https://www.juniper.net/us/en/company/images/image-library-logos-and-product-photos/products/mx304.html
  - https://www.juniper.net/documentation/us/en/hardware/mx304/mx304.pdf
  - https://www.juniper.net/documentation/us/en/hardware/mx304/topics/topic-map/mx304-system-overview.html
  - https://www.juniper.net/documentation/us/en/hardware/mx304/topics/topic-map/mx304-chassis.html
  - https://apps.juniper.net/hct/product/MX304/hwspecs
  - https://community.juniper.net/blogs/reema-ray/2023/03/28/mx304-deepdive
  - https://www.ebay.com/itm/357632213474
- identity_resolution: The screenshot front matches the official two-RE/two-LMIC16 product photo and therefore MX304-PREM rather than MX304-BASE. The screenshot rear matches the official AC rear, and the user separately mandated AC. The official support SKU MX304-PREM-AC-FS names this physical AC premium bundle; FS/software licensing is not visually modeled.
- status: VERIFIED

## Identity exclusions

- MX304-BASE is excluded because it contains one Routing Engine and the screenshot contains two.
- The one-RE/three-LMIC front option is excluded.
- MX304-LMIC20S is excluded because its SFP/QSFP face differs from the screenshot's two 16-port LMIC16 faces.
- DC and HVAC/HVDC rear variants are excluded. Their terminal/connector shapes differ from the screenshot and the task-wide AC decision.
- Seller cables, inventory stickers, serial-number labels, damage, and missing modules are not part of the delivery subject.
