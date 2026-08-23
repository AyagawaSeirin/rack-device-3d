# Fortinet FortiGate FG-1500D assembly identity

manufacturer: Fortinet, Inc.
requested_product_id: FortiGate FG-1500D (D generation; not FG-1500DT, FG-1500D-DC, FortiDDoS/FG-1500F, FG-1400 family, FG-1800F, or adjacent generations)
delivery_subject: complete-appliance
host_enclosure_model: FortiGate 1500D 2 RU appliance chassis
installed_module_model: integrated FG-1500D front I/O cage set plus the user-locked rear service-module arrangement visible in screenshot row 3
installed_module_count: front 5 port/cage groups after console and management; rear 4 fan trays + 2 AC PSUs + blank/service panels
installed_module_positions: front and rear positions are frozen in feature-inventory.csv
front_backplane_or_drive_configuration: no drive bays or bezel; 16x GE SFP (ports 1-16), 16x GE RJ45 (17-32), 8x 10GE SFP+/GE SFP (33-40), 2x GE RJ45 MGMT, console, USB-A and USB mini-B
rear_io_or_controller_configuration: user screenshot row 3, not the later/standard Fortinet diagram; upper-left four individually framed fan trays, upper center-right blank/service-panel area, far-right two vertical AC PSUs, lower row segmented vent/blank/service panels
bezel_and_blanking_panel_state: no front bezel; all front cages present; rear blank/service panels installed as seen in the user screenshot
power_and_fan_configuration: dual hot-swappable 100-240 V AC power supplies; four user-locked rear fan trays for the delivery appearance
u_height: 2 RU; official physical height 89 mm
body_dimensions_mm: 438 W x 89 H x 554 D
rack_brackets: supplied separately by Fortinet; not installed on the front delivery appearance because the locked row-3 front has no visible rack brackets. Do not infer rear ears from a perspective view.
hardware_revision: D-generation exterior delivery subject; internal Gen1/Gen2 CPU/disk revision is not externally selected and must not cause an F/E-generation exterior substitution
evidence_urls:
  - https://www.fortinet.com/content/dam/fortinet/assets/data-sheets/zh_cn/FortiGate_1500D.pdf
  - https://fortinetweb.s3.amazonaws.com/docs.fortinet.com/v2/attachments/c48097f0-1a12-11e9-9685-f8bc1258b856/FortiGate-1500D-Supplement.pdf
  - https://community.fortinet.com/fortigate-3/technical-tip-how-to-identify-a-fortigate-1500d-s-hardware-revision-between-generation-1-and-generation-2-221266
  - /root/Project/rack-device-3d/Fortinet-FG1500D/source/user-row/original-request-table.png
configuration_conflict: Fortinet QSG, datasheet, FIPS imagery, and the 2017 fan-redundancy note show the catalog FG-1500D AC rear as left dual PSU plus three chassis cooling-fan grilles (with additional PSU fans). The user explicitly requires the screenshot-row rear instead. The main model therefore implements the user-owned row-3 delivery appearance and does not claim that rear as the catalog factory rear.
status: VERIFIED

## Identity exclusions

- FG-1500DT has four 10GE RJ45 ports and only four SFP+ ports; it is excluded.
- FG-1500D-DC has DC terminal PSUs; it is excluded in favor of uniform AC.
- FortiDDoS/"1500F", FortiGate 1800F and later F/G platforms use different front I/O and rear thermal systems; excluded.
- FG-1200D/1400/3700D and other D-family layouts cannot donate identity-bearing port or rear-module geometry.
- The optional 3D Warehouse model is a non-certified community upload by Jesus Ruiz; it is not official Fortinet CAD and is not the main build.
