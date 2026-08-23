# Juniper MX204 assembly identity manifest

- manufacturer: Juniper Networks (now HPE Juniper Networking)
- requested_product_id: MX204
- orderable_hardware_pid: MX204-HW-BASE (AC physical variant); the later license-bundle PID MX204-HWBASE-AC-FS has the same verified exterior hardware
- chassis_model: JNP204-CHAS
- delivery_subject: complete-appliance
- host_enclosure_model: not applicable; fixed-configuration MX204 chassis
- installed_module_model: built-in RE-S-1600x8 routing engine; three JNP-FAN-1RU fan modules; two JPSU-650W-AC-AO power-supply modules
- installed_module_count: 1 built-in routing engine; 3 fan modules; 2 AC PSUs
- installed_module_positions: fan slots 0, 1, 2 and PSU slots 0, 1, all populated
- front_backplane_or_drive_configuration: fixed front I/O; four QSFP28/QSFP+ rate-selectable ports (0-3), eight SFP+ ports (4-11), no transceivers installed, no bezel
- rear_io_or_controller_configuration: AC rear; three JNP-FAN-1RU AFO fan trays and two JPSU-650W-AC-AO IEC-inlet power supplies; no PSU blank
- bezel_and_blanking_panel_state: no front bezel; all network ports empty; fixed central rear chassis blank area present; no missing FRU blank
- power_and_fan_configuration: AC, 2 x 650 W JPSU-650W-AC-AO, 3 x JNP-FAN-1RU, front-to-back/AFO airflow
- rack_hardware: factory front mounting brackets/ears present; side mounting rails present; rear sliding brackets represented in the retracted/flush configuration evidenced by the user screenshot and official rack-installation figures
- u_height: 1U; actual chassis height 43.7 mm (1.72 in)
- body_dimensions: 447 mm wide x 43.7 mm high x 470 mm deep
- overall_dimensions: 482.6 mm wide over front mounting brackets x 43.7 mm high x 518.9 mm deep over fan/PSU handles
- evidence_urls:
  - https://apps.juniper.net/hct/product/MX204/hwspecs
  - https://www.juniper.net/documentation/us/en/hardware/mx204/mx204.pdf
  - https://www.juniper.net/documentation/us/en/hardware/mx204/topics/topic-map/mx204-chassis.html
  - https://www.juniper.net/us/en/company/images/image-library-logos-and-product-photos/products/mx204.html
- screenshot_target: `/root/Project/rack-device-3d/Juniper-MX204/source/originals/user-screenshot.png`, third readable device row (after QFX5110 and MX304)
- status: VERIFIED
- bottom_status: GENERIC_BOTTOM_FALLBACK required after documented search exhaustion; this does not alter the verified identity, silhouette, or any other face

## Frozen identity decision

The exterior target is the fully populated AC-powered MX204 appliance. The user explicitly selected AC for this batch. The screenshot shows the same fixed front-port arrangement, three rear fan positions, and two IEC-style AC inlets. It is too small to establish color, fine labels, fan-handle shape, or any side/top/bottom detail, so those details are bound to the current Juniper official photographs, hardware guide, Hardware Compatibility Tool, and cross-checked exact-model resale photography instead.
