# Assembly identity manifest

- manufacturer: Cisco Systems, Inc.
- requested_product_id: `Cisco Nexus9000 C93180YC-FX Chassis` (user clarification)
- exact_cisco_pid: `N9K-C93180YC-FX`
- delivery_subject: complete-appliance
- equipment_type: fixed-port data-center switch
- host_enclosure_model: not applicable
- installed_module_model: four `NXA-FAN-30CFM-PI` fan modules plus two `NXA-PAC-500W-PI` AC power supplies
- installed_module_count: 4 fans; 2 AC PSUs
- installed_module_positions: rear/power-supply side, two PSUs with four fan trays between them; I/O/control cluster at the device-right end in the screenshot
- front_backplane_or_drive_configuration: 48 SFP/SFP28 cages in two rows plus 6 QSFP/QSFP28 cages in two rows
- rear_io_or_controller_configuration: FX rear I/O cluster with L1 and L2 software-defined ports, BCN/STS LEDs, RS-232 console, USB, and RJ-45 out-of-band management
- bezel_and_blanking_panel_state: no front bezel; all fixed cages visible; no optics installed
- power_and_fan_configuration: port-side intake; 2 × 500W AC `NXA-PAC-500W-PI`; 4 × `NXA-FAN-30CFM-PI`; all burgundy-coded and direction-matched
- u_height: 1 RU
- evidence_urls:
  - https://www.cisco.com/c/en/us/td/docs/switches/datacenter/nexus9000/hw/n93180ycfx_hig/guide/b_n93180ycFX_nxos_hardware_installation_guide.pdf
  - https://www.cisco.com/c/en/us/support/switches/nexus-93180yc-fx-switch/model.html
  - https://www.cisco.com/c/en/us/td/docs/dcn/nx-os/nexus9000/106x/release-notes/cisco-nexus-9000-nxos-release-notes-1063F.html
- status: VERIFIED
- delivery_status: PASS_WITH_BOTTOM_FALLBACK

## Identity resolution

The user explicitly resolved the chassis as `N9K-C93180YC-FX`. The screenshot rear I/O pixel grid is compatible with the official FX L1/L2 layout and not the EX or FX3 rear layout.

The original rear thumbnail preserves burgundy/dark-magenta latch pixels on all four fan modules. The preserved legacy FX hardware guide calls the burgundy intake fan `NXA-FAN-30CFM-B`; the user's final configuration lock normalizes the installed fan ordering PID to `NXA-FAN-30CFM-PI`. The visible hardware invariant is the same port-side-intake burgundy module. Cisco also requires all installed fans and power supplies to use the same airflow direction. The user requires standard AC power; Cisco's current FX system specifications and release support table map that to two 500W `NXA-PAC-500W-PI` modules.

The exact installed configuration is therefore:

- chassis: `N9K-C93180YC-FX`, full 48-port base PID, 1 RU;
- front: 48 empty SFP28 cages plus 6 empty QSFP28 cages; no optics, no bezel;
- rear: four installed `NXA-FAN-30CFM-PI` fan trays;
- rear: two installed `NXA-PAC-500W-PI` standard AC power supplies;
- airflow: port-side intake, burgundy-coded throughout;
- rack hardware: front rack ears present; rear ears are not inferred.

## Conflicting reseller evidence rejected

A reseller page labels a photographed unit as FX with 650W PI modules, but the photographed rear has the EX-style RJ-45/SFP/USB management cluster rather than the official FX L1/L2 cluster. It is classified as a mismatched stock image and is not used to override the Cisco FX support matrix or the user screenshot.

The valid-FX build gate is cleared for six-face source locking, generation and
delivery. The only evidence exception is the documented generic bottom fallback.

## Task-12 scope clarification — corrected 2026-08-28

The common Task-12 requirement for all devices is AC power. The later exact-FRU
clarification for `NXA-PAC-1100W-PI2` and `NXA-FAN-65CFM-PI` applies only to
the separately scoped `N9K-C9336C-FX2`; it is not an installed-configuration
requirement for this chassis.

The active GLBs correctly retain the physically supported, source-locked FX
exterior: 4 x 30CFM PI intake fans and 2 x 500W PI AC PSUs. The incompatible
65CFM/1100W-PI2 modules are intentionally not installed because their size,
slot count and rear architecture belong to C9336C-FX2. This exclusion preserves
exactness rather than creating a blocker. With all non-bottom evidence and QA
gates resolved, the delivery status is `PASS_WITH_BOTTOM_FALLBACK`.
