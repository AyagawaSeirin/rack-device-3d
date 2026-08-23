# Assembly identity manifest

- manufacturer: Juniper Networks
- requested_product_id: QFX5110-48S-AFI
- family_model: QFX5110-48S
- ordering_variant: QFX5110-48S-AFI (AC, Airflow In / FRU-to-port)
- equipment_type: fixed-configuration Ethernet switch
- delivery_subject: complete-appliance
- host_enclosure_model: QFX5110-48S fixed chassis
- installed_module_model: not modular; fixed port panel plus field-replaceable fans and power supplies
- installed_module_count: 5 fan modules + 2 AC power supplies
- installed_module_positions: management panel at rear device-left; fan slots 0–4 left-to-right; PSU slots 0–1 at rear device-right
- front_backplane_or_drive_configuration: 48 empty SFP/SFP+ cages in two rows of 24 plus 4 empty QSFP+/QSFP28 cages in a 2×2 block; no transceivers or cables
- rear_io_or_controller_configuration: QFX5110 management panel, five QFX5110-48S-FANAFI modules, two JPSU-650W-AC-AFI modules
- bezel_and_blanking_panel_state: no bezel; no port blanks; no missing FRUs
- power_and_fan_configuration: AC; two 650 W JPSU-650W-AC-AFI PSUs; five azure-blue AIR IN QFX5110-48S-FANAFI fan modules
- airflow_direction: AFI, FRU-to-port (back-to-front)
- rack_hardware: screenshot configuration includes two short front mounting ears; exact-model third-party photographs prove the galvanized two-large-hole/one-small-hole ear pattern; no rear ears and no full rails in the delivered model
- factory_branding: preserve the Juniper logo, QFX5110-48S/RUNNING JUNOS badge, port numbering, AIR IN/AFI markings, and verified control labels in their real locations and readable orientations
- u_height: 1 U
- body_dimensions_mm: 440.944 W × 43.688 H × 520.192 D (published depth excludes fan and PSU handles)
- installed_overall_dimensions_mm: 482.600 W including front ears × 43.688 H body envelope × approximately 551.992 D including front connectors and rear handles/retainers
- overall_depth_basis: front connector projection 4.8 mm plus image-derived rear projection 27 mm (within the documented 24 ±4 mm estimate), added to the official 520.192 mm body depth; official published depth explicitly excludes fan/PSU handles
- evidence_urls:
  - https://www.juniper.net/documentation/us/en/hardware/qfx5110/topics/topic-map/qfx5110-system-overview.html
  - https://www.juniper.net/us/en/company/images/image-library-logos-and-product-photos/products/qfx5110-48s.html
  - https://www.juniper.net/documentation/us/en/hardware/qfx5110/qfx5110.pdf
  - https://apps.juniper.net/hct/product/QFX5110/hwspecs
  - https://switches-networks.sell.everychina.com/p-116654966/showimage.html
  - https://nwkoubou.jp/SHOP/QFX5110-48S-AFI-2PWR-BK.html
- screenshot_identity_result: first readable row is QFX5110-48S; light-blue fan handles and dual IEC AC inlets match the official AFI AC rear and rule out AFO and DC variants
- status: VERIFIED

## Frozen delivery target

- standard_glb: `model/Juniper-QFX5110.glb`
- web_glb: `model/Juniper-QFX5110-web.glb`
- coordinate_convention: right-handed glTF; +X device-right as seen from front, +Y up, +Z front
- bottom_policy: `GENERIC_BOTTOM_FALLBACK` after documented official, Browser-assisted, marketplace, auction, used-equipment, teardown, video, English, Japanese, and Chinese searches found no exact underside
- final_status_ceiling: PASS_WITH_BOTTOM_FALLBACK
