# Assembly identity manifest

- manufacturer: Cisco Systems, Inc.
- requested_product_id: `N9KC93180YC` (parser-normalized text shown in the user screenshot)
- exact_cisco_pid: unresolved
- delivery_subject: complete-appliance
- equipment_type: fixed-port data-center switch
- host_enclosure_model: not applicable
- installed_module_model: four hot-swappable fan modules plus two hot-swappable AC power supplies
- installed_module_count: 4 fans; 2 AC PSUs
- installed_module_positions: rear/power-supply side, two PSUs with four fan trays between them; I/O/control cluster at the device-right end in the screenshot
- front_backplane_or_drive_configuration: 48 SFP/SFP28 cages in two rows plus 6 QSFP/QSFP28 cages in two rows
- rear_io_or_controller_configuration: unresolved; the screenshot is too small to distinguish the EX management/SFP cluster from the FX L1/L2 cluster reliably
- bezel_and_blanking_panel_state: no front bezel; all fixed cages visible; no optics installed
- power_and_fan_configuration: AC only; two PSUs and four fans; airflow direction and module PIDs unresolved
- u_height: 1 RU
- evidence_urls:
  - https://www.cisco.com/c/en/us/td/docs/switches/datacenter/nexus9000/hw/n93180ycex_hig/guide/b_n93180ycex_nxos_mode_hardware_install_guide.pdf
  - https://www.cisco.com/c/en/us/td/docs/switches/datacenter/nexus9000/hw/n93180ycfx_hig/guide/b_n93180ycFX_nxos_hardware_installation_guide.pdf
  - https://www.cisco.com/c/en/us/td/docs/dcn/hw/nx-os/nexus9000/93180yc-fx3/cisco-nexus-93180yc-fx3-nx-os-mode-switch-hardware-installation-guide.pdf
- status: BLOCKED

## Blocking ambiguity

The screenshot row uses `N9KC93180YC`, not a complete Cisco chassis PID. Cisco documents multiple materially different products that normalize to that shared stem:

| Candidate chassis | Body dimensions from Cisco | AC PSU choices shown by Cisco | Distinguishing exterior facts |
|---|---:|---|---|
| `N9K-C93180YC-EX` | 445 × 571 × 44 mm | `NXA-PAC-650W-PE` or `NXA-PAC-650W-PI` | EX rear management cluster; 30 CFM fan family |
| `N9K-C93180YC-FX` | 439 × 571 × 44 mm | `NXA-PAC-500W-PE` or `NXA-PAC-500W-PI` | L1/L2 rear I/O cluster; 30 CFM fan family |
| `N9K-C93180YC-FX3` | 439 × 496 × 44 mm | `NXA-PAC-650W-PE` or `NXA-PAC-650W-PI` | timing/GNSS front details, ToD rear port, different 496 mm-depth body; 35 CFM fan family |

The user crop contains only about 204 × 34 source pixels for each elevation. The chassis badge and PSU/fan labels are unreadable. Nearest-neighbor enlargement confirms that the rear I/O block is only a handful of source pixels per port. It appears more compatible with the EX/FX generation than FX3, but it cannot reliably distinguish EX from FX or prove the airflow color.

AC-only does not resolve the physical configuration. EX/FX/FX3 all support both port-side intake and port-side exhaust AC modules. The blue/burgundy color-coded handles and module labels are below reliable resolution in the screenshot. The 24-port licensed EX/FX ordering variants also retain the same fixed cage silhouette, so empty cages do not prove the license/PID.

## Required unblock input

Provide at least one of:

1. a readable chassis PID photograph (for example `N9K-C93180YC-EX`, `-FX`, `-FX3`, or `-FX3S`);
2. the exact ordered chassis PID plus both installed AC PSU PIDs and fan PID/airflow direction; or
3. original-resolution front and rear photographs in which the model badge, rear I/O labels, fan latch color, and PSU label are readable.

No image generation or mesh work is permitted until this manifest can be changed to `VERIFIED`.
