# Evidence and identity audit

Audit date: 2026-08-24 (Asia/Singapore)

Final identity gate: **BLOCKED**

## Requested subject and screenshot lock

The user-provided table row is preserved unchanged at `source/originals/user-screenshot.png` (SHA-256 `00861cf47eb85ee4f20fc3dc3fc850820368df4e3db7b2721b3226dfca8c1921`). The extracted row is `source/originals/user-screenshot-N9KC93180YC-row.png` (SHA-256 `dc4f35b16756256b9c9768a3ca2ed59bf0cc064a315ea53a39795a0fd7e01e32`).

The row proves these common visible facts:

- Cisco/思科 branding and normalized display name `N9KC93180YC`;
- 1 RU fixed switch silhouette;
- 48 small front cages in two rows and 6 larger cages in two rows at device right;
- rear/power-supply side with two IEC AC power inputs, four fan trays, and a right-side control/I/O cluster;
- no front optics and no bezel.

It does **not** prove a complete Cisco PID, airflow direction, AC PSU wattage/PID, fan PID, or exact rear management-port configuration. The extracted device face is only about 204 × 34 source pixels. Nearest-neighbor crops are preserved in `qa/reference/` and were visually inspected. No amount of upscaling restores the missing badge/label information.

The rear cluster looks more compatible with EX/FX than the materially different FX3 rear, and its pixel pattern may be compatible with FX L1/L2 ports. This is only a likelihood. It is not reliable exact-PID evidence and cannot satisfy the assembly-identity gate.

## Official Cisco evidence

### Candidate `N9K-C93180YC-EX`

Official hardware guide:
https://www.cisco.com/c/en/us/td/docs/switches/datacenter/nexus9000/hw/n93180ycex_hig/guide/b_n93180ycex_nxos_mode_hardware_install_guide.pdf

- Cisco identifies a 1-RU `N9K-C93180YC-EX` with 48 × 1/10/25G SFP28 and 6 × 40/100G QSFP28 ports.
- Published switch dimensions: 17.5 × 22.5 × 1.72 inches (44.5 × 57.1 × 4.4 cm).
- Four fans: `NXA-FAN-30CFM-F` blue port-side exhaust or `NXA-FAN-30CFM-B` burgundy port-side intake.
- Two AC PSUs: `NXA-PAC-650W-PE` blue exhaust or `NXA-PAC-650W-PI` burgundy intake.
- Cisco also documents a 24-port ordering configuration `N9K-C93180YC-EX-24`, which retains the fixed front cage silhouette.
- Visual PDF pages inspected: printed pages 3, 45, and 46 in `source/pdf-pages/`.

### Candidate `N9K-C93180YC-FX`

Official hardware guide:
https://www.cisco.com/c/en/us/td/docs/switches/datacenter/nexus9000/hw/n93180ycfx_hig/guide/b_n93180ycFX_nxos_hardware_installation_guide.pdf

- Cisco identifies a 1-RU `N9K-C93180YC-FX` with the same 48 + 6 front cage pattern.
- Published switch dimensions: 17.3 × 22.5 × 1.72 inches (43.9 × 57.1 × 4.4 cm).
- Four fans: `NXA-FAN-30CFM-F` blue port-side exhaust or `NXA-FAN-30CFM-B` burgundy port-side intake.
- Two AC PSUs: `NXA-PAC-500W-PE` blue exhaust or `NXA-PAC-500W-PI` burgundy intake.
- The rear I/O cluster includes L1 and L2 software-defined ports, console, USB, and out-of-band RJ45; this differs from EX but is below reliable screenshot resolution.
- Cisco also documents 24-port ordering variants whose cage silhouette does not disambiguate the screenshot.
- Visual PDF pages inspected: printed pages 3, 4, 61, and 62 in `source/pdf-pages/`.

### Candidate `N9K-C93180YC-FX3`

Official hardware guide:
https://www.cisco.com/c/en/us/td/docs/dcn/hw/nx-os/nexus9000/93180yc-fx3/cisco-nexus-93180yc-fx3-nx-os-mode-switch-hardware-installation-guide.pdf

- Cisco identifies a 1-RU `N9K-C93180YC-FX3` with 48 × SFP28 and 6 × QSFP28 cages.
- Published switch dimensions: 17.3 × 19.5 × 1.72 inches (43.9 × 49.6 × 4.4 cm), 75 mm shorter than EX/FX.
- Four `NXA-FAN-35CFM-PE` blue exhaust or `NXA-FAN-35CFM-PI` burgundy intake fan modules.
- Two `NXA-PAC-650W-PE` blue exhaust or `NXA-PAC-650W-PI` burgundy intake AC PSUs.
- Front timing/GNSS connectors and rear ToD port are visible differentiators. The screenshot seems less compatible but is not readable enough for a formal exclusion.
- Visual PDF pages inspected: printed pages 3, 4, 49, and 50 in `source/pdf-pages/`.

## PDF processing note

The workflow-requested `pdf` skill is not installed in this session. The three official PDFs were still preserved unchanged, text-extracted with Ghostscript `txtwrite`, and the relevant pages rendered at 150 dpi with Ghostscript `png16m`. Every selected page render was inspected at original detail. The extraction warning `finalizing subclassing device while child refcount > 1` occurred after output generation; the text files were created and the cited dimension/module rows were verified against the page renders.

## Dynamic page and third-party escalation

Playwright headless browser inspection was used because Cisco pages and the reseller gallery are script-rendered:

- Cisco EX guide: extracted official front/rear figure URLs and verified current content. `qa/browser/cisco-ex-overview-snapshot.yml`.
- Cisco FX guide: extracted distinct FX figure URLs and rear L1/L2 inventory. `qa/browser/cisco-fx-overview-snapshot.yml`.
- Cisco FX3 support page: found only the 2D Visio stencil, no 3D/CAD asset. `qa/browser/cisco-fx3-support-snapshot.yml`.
- Piospartslap EX gallery: verified exact `N9K-C93180YC-EX`, blue 650W AC PSUs, blue fan latches, top cover, and rear management cluster across five 2000 × 2000 photos. `qa/browser/pios-ex-product-snapshot.yml`.

Third-party FX/FX3 photos were cross-checked against the official diagrams:

- exact FX rear photograph shows 500W AC labels and an L1/L2 2×2 rear cluster;
- exact FX3 rear photograph shows the ToD/control cluster between the fan bank and PSU2 and a shorter top;
- one FX3S marketplace image was rejected because it visibly shows the wrong port family;
- one FX3 reseller composite was rejected because it shows detached components, bags, and a watermark rather than a complete device face.

Failed public image fetches are recorded as limitations: the Northsoar host presented a certificate-name mismatch, ServerOrbit returned HTTP 403, CloudAppliances returned HTTP 403, and one NetworkOutlet CDN URL returned HTTP 404. No authentication, certificate bypass, or anti-bot bypass was attempted.

## Exactness decision

Selecting EX, FX, FX3, a 24-port ordering PID, or a PI/PE airflow bundle would change body width/depth, rear I/O, top/service-cover geometry, fan/PDU colors, and PSU labels. Those are identity-bearing exterior facts. Therefore:

- `source/identity-manifest.md` remains `BLOCKED`;
- all six rows in `source/face-source-lock.csv` remain unselected;
- built-in image generation was not invoked;
- no bottom fallback search was started because the non-bottom assembly identity failed first;
- no standard or web GLB was created;
- no viewer-load or comparison evidence was fabricated.

The exact unblock requirements are listed in `source/identity-manifest.md`.
