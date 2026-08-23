# Evidence record — Cisco N9K-C9336C-FX2

Research date: 2026-08-24 (Asia/Singapore)

## Identity resolution

The screenshot labels the row only as `N9KC9336`, which is not a unique Cisco PID. Its front shows 36 QSFP-class ports as 18 vertical two-port groups, while its rear follows the sequence `PSU + three fan trays + RJ-45/RS-232/SFP/USB management cluster + PSU`. Feature-by-feature comparison with Cisco's official port-side and power-supply-side figures and hardware guide resolves the chassis to canonical PID `N9K-C9336C-FX2`.

Cisco's current hardware guide describes this PID as a 1-RU fixed-port switch with 36 40/100-Gigabit QSFP28 ports. The official port-side and power-supply-side figures match the screenshot's front 18-by-2 port presentation and rear sequence of PSU, three fans, management cluster, and PSU.

The earlier `N9K-C9336PQ` hypothesis is rejected. Its 2-RU/40-Gigabit identity and exterior layout conflict with the screenshot-to-official-figure comparison for C9336C-FX2. All earlier PQ-derived assets are quarantined under `qa/rejected/wrong-identity-9336PQ/` and are excluded from active source locks and deliverables.

## Binding local evidence

| File | Role | Size | SHA-256 |
|---|---|---:|---|
| `source/originals/user-screenshot.png` | User-supplied configuration lock | 289,852 bytes | `00861cf47eb85ee4f20fc3dc3fc850820368df4e3db7b2721b3226dfca8c1921` |
| `source/crops/user-row-N9KC9336.png` | Exact row crop preserving front/rear orientation | derived 1006 × 112 PNG | `99b3bae81c829654df8800880d79473078c69f6542c8f85cf0b5463552b73867` |
| `source/crops/user-rear-N9KC9336-4x.png` | Nearest-neighbor enlarged rear thumbnail; no new detail introduced | derived 840 × 220 PNG | `af16134e18c342dbfc3f18559321ba1085b6bf305967412497c0f67830467f94` |
| `source/originals/cisco-N9K-C9336C-FX2-port-side.jpg` | Official exact-PID port-side diagram | 29,850 bytes | `2b7374f065b7d8682ae88262c26d86b060ff260246a2c50ce898f399118ed166` |
| `source/originals/cisco-N9K-C9336C-FX2-power-side.jpg` | Official exact-PID power-side diagram | 28,324 bytes | `ead380a0df86f98af0573a95b2dc676cc002b2c21124b8b939de214a1244dba8` |
| `source/originals/cisco-N9K-C9336C-FX2-hardware-installation-guide.pdf` | Official exact-PID dimensions, topology, and supported-module matrix | 3,861,616 bytes | `082de2d988d805d8c5084c73cba8a73e21514bf31316a17289f41882b9c04134` |

Official figure URLs:

- Port side: https://www.cisco.com/c/dam/en/us/td/i/500001-600000/500001-510000/501001-502000/501590.jpg
- Power-supply side: https://www.cisco.com/c/dam/en/us/td/i/500001-600000/500001-510000/501001-502000/501591.jpg

## Inspected PDF pages

The official PDF was rendered locally with Ghostscript because a PDF-specific skill was unavailable. Each listed render was visually inspected at original detail.

| Render | Manual page | Verified content | SHA-256 |
|---|---:|---|---|
| `source/pdf-pages/fx2-hig/page-7.png` | 1 | Exact PID, 1-RU, 36 × 40/100G QSFP28; both PI fan families listed | `b3fa02a6486b49f87d1ae98e79f6f77f0c1b0845ea1500d6847f1e9fc5c5648b` |
| `source/pdf-pages/fx2-hig/page-8.png` | 2 | Supported AC PI PSU variants: 750W, 1100W PI2, and 1100W PI3 | `b98d2b639b5703f8d5c0ef5765fb8d49c9a8a6261b2236b63cf72f1b71608223` |
| `source/pdf-pages/fx2-hig/page-9.png` | 3 | Port-side feature diagram and 36-port arrangement | `1ba24cf263c2efb84e17d5cf52187514dd422235f28e030eb941bb459407d2d6` |
| `source/pdf-pages/fx2-hig/page-10.png` | 4 | Rear component order, two PSUs, three fans, management ports, same-airflow requirement | `bfa42af64226c3e60edd993fb5b5fd5feda0320137a26c521241eb683ee6d12b` |
| `source/pdf-pages/fx2-hig/page-55.png` | 49 | Official dimensions, including 1.72-inch / 1-RU height | `2bce34af7732e7e5fead9f282c31be6427873f90a27017814a09c0522ba52f0e` |

## Configuration facts proven by the screenshot

- Front: 36 QSFP28 ports are visible as 18 vertical two-port groups; cages appear empty.
- Rear: two PSU modules and three fan modules are populated.
- Both PSU faces show IEC AC inlets, consistent with the user's all-AC instruction.
- Both PSU pull tabs are burgundy/red, which Cisco defines as port-side-intake airflow. Cisco requires all installed PSUs and fan modules to use the same airflow direction, so the assembly is PI.
- The rear thumbnail is only 210 × 55 pixels. Upscaling does not recover labels, wattage, efficiency generation, or fan PID.

## Official variant matrix causing the block

Cisco's exact-model guide supports all of the following visible PI configurations:

- AC PSU: `NXA-PAC-750W-PI`
- AC PSU: `NXA-PAC-1100W-PI2`
- AC PSU: `NXA-PAC-1100W-PI3`
- Fan: `NXA-FAN-65CFM-PI`
- Fan: `NXA-SFAN-65CFM-PI`

The screenshot shorthand and unreadable module labels do not distinguish among these PIDs. A reseller bundle was found with 2 × 750W PI, while a separate exact-model intake listing described 2 × 1100W, confirming that more than one real AC intake assembly exists. Those reseller statements are corroborative only; the official Cisco compatibility list is the binding reason that no default can be assumed.

Primary official sources:

- Hardware overview and supported modules: https://www.cisco.com/c/en/us/td/docs/switches/datacenter/nexus9000/hw/n9336cfx2_hig/guide/b_n9336cFX2_nxos_hardware_installation_guide/b_n9336cFX2_nxos_hardware_installation_guide_chapter_01.html
- Dimensions: https://www.cisco.com/c/en/us/td/docs/switches/datacenter/nexus9000/hw/n9336cfx2_hig/guide/b_n9336cFX2_nxos_hardware_installation_guide/b_n9336cFX2_nxos_hardware_installation_guide_appendix_0111.html
- Current FX2 data sheet and ordering table: https://www.cisco.com/c/en/us/products/collateral/switches/nexus-9000-series-switches/datasheet-c78-742282.html
- Cisco model support page: https://www.cisco.com/c/en/us/support/switches/nexus-9336c-fx2-switch/model.html

## Decision

Status is `BLOCKED` at the assembly-identity gate. No face image generation, mesh construction, GLB export, or WebGL acceptance loading is permitted until the exact installed PSU and fan PIDs are supplied.
