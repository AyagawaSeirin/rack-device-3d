# Evidence and search record

Access date: 2026-08-24 (Asia/Singapore)

## Identity resolution

The requested normalized label `N9KC9336` is not itself a complete Cisco PID. The screenshot's final row was inspected at original resolution and isolated without modifying the original. It shows a 2U port side with 36 QSFP+ ports in two rows and a power side with two large central fan modules and two outer AC supplies. This is the exterior of the Cisco Nexus 9336PQ, PID `N9K-C9336PQ`, not any 1U Nexus 9336C/FX2 descendant.

The two PSU release-latch pixels in the screenshot are burgundy/red. Cisco's hardware guide maps burgundy to port-side intake, and exact-unit photographs show the same configuration with readable `N9K-PAC-1200W V01` PSU and `N9K-C9300-FAN3` fan labels. Cisco requires all fans and PSUs in the chassis to use the same airflow direction. The installed physical variant is therefore uniquely resolved as:

- chassis `N9K-C9336PQ V02`, 2U;
- 36 fixed 40-Gigabit QSFP+ ports, empty in the delivery state;
- two `N9K-C9300-FAN3` port-side-intake fan modules, burgundy identification stripes;
- two `N9K-PAC-1200W` 1200-W AC port-side-intake supplies, burgundy latches, 1+1 redundant;
- no blue `-B` exhaust modules, no DC/HVDC supplies, no rear ears.

## Official sources

### Hardware installation guide

URL: https://www.cisco.com/c/en/us/td/docs/switches/datacenter/nexus9000/hw/aci_9336pq_hig/guide/b_n9336PQ_hardware_install_guide.pdf

Preserved original: `source/originals/cisco-N9K-C9336PQ-hardware-installation-guide.pdf`

- size: 5,107,332 bytes
- SHA-256: `392bef2a7ce332ab6906a34cca0903e5d590ae444ecaf75021907b8b1e8e3e6d`
- document: Cisco Nexus 9336PQ ACI-Mode Switch Hardware Installation Guide, first published 2014-08-13, current public file last modified 2026-06-18, 78 pages.
- relevant rendered pages: PDF pages 11–13 (manual pages 1–3), 59 (manual page 49), 73 (manual page 63), preserved under `source/pdf-pages/` with hashes in `qa/reference/pdf-pages-sha256.txt`.
- proves: exact PID, 2U, fixed 36-QSFP port count, port numbering, two fan modules, exact intake/exhaust fan/PSU PIDs and colors, all-modules-same-airflow rule, AC PSU support, port-side and power-side geometry, separate rack-mount brackets, and published dimensions.

The dedicated `pdf` skill named by the workflow is not installed in this Codex session. The original PDF was still preserved unchanged; text was checked through the indexed official Cisco page/web PDF extraction, and every relevant page was rendered locally with Ghostscript at 220 dpi and visually inspected at original detail. This is recorded as a tooling substitution, not hidden.

### Online hardware guide and data sheet

- Overview: https://www.cisco.com/c/en/us/td/docs/switches/datacenter/nexus9000/hw/aci_9336pq_hig/guide/b_n9336PQ_hardware_install_guide/b_n9336PQ_hardware_install_guide_chapter_01010.html
- System specifications: https://www.cisco.com/c/en/us/td/docs/switches/datacenter/nexus9000/hw/aci_9336pq_hig/guide/b_n9336PQ_hardware_install_guide/b_n9336PQ_hardware_install_guide_appendix_0111.html
- Data sheet / ordering table: https://www.cisco.com/c/en/us/products/collateral/switches/nexus-9000-series-switches/datasheet-c78-731792.html

The ordering table lists chassis `N9K-C9336PQ`, intake fan `N9K-C9300-FAN3`, exhaust fan `N9K-C9300-FAN3-B`, intake AC supply `N9K-PAC-1200W`, and exhaust AC supply `N9K-PAC-1200W-B` as separate physical orderable parts.

### Official product diagrams

- Power-supply side JPEG: https://www.cisco.com/c/dam/en/us/td/i/300001-400000/300001-310000/304001-305000/304581.eps/_jcr_content/renditions/304581.jpg
- Port side JPEG: https://www.cisco.com/c/dam/en/us/td/i/300001-400000/300001-310000/304001-305000/304580.eps/_jcr_content/renditions/304580.jpg

Both are preserved unchanged under `source/originals/`. They prove the two fans/two PSU arrangement, front control grouping, 36 QSFP ports, chassis-side holes and rail-lock notch. They are technical diagrams and do not establish color/material by themselves.

## Exact official 3D model discovery

Official landing page: https://www.cisco.com/c/dam/assets/prod/switches/nexus-9000-series/nexus-9336pq-aci-spine-3d-model.html

The page embeds Cisco's public Kaon model at `https://apps.kaonadn.net/4357027/product.html`. The UI currently reports that the application is disabled, but Playwright network inspection found public, unauthenticated resources for the exact `Cisco Nexus 9336PQ ACI Spine Switch`. No authentication, private API, anti-bot bypass, or access-control circumvention was used.

The model is a Kaon/Lepton package, not GLB/GLTF/CAD. Its exact public source files were downloaded byte-for-byte into `source/optional-3d/`: `app.xml`, `lepton.xml`, four `u178b24aa-*.bin` geometry blocks, twelve face/quadrant JPEGs, two composite textures, auxiliary textures, public manifest, and official viewer page. Total preserved package size is 5,982,249 bytes. Per-file sizes and SHA-256 values are in `source/optional-3d/SOURCE.md` and `qa/reference/optional-3d-sha256.txt`.

`lepton.xml` declares the exact title, 36-port/front/rear scripted views, 14,778 visible mesh faces across four binary objects (5,588 + 2,950 + 3,180 + 3,060 faces), and exact model texture names. The official package is retained only as an optional backup and authoritative exterior reference. None of its binary mesh data is copied into the self-built standard/web GLBs.

The official package includes exact top, left, right and bottom photographic texture segments. Therefore the bottom is evidence-backed and the generic-bottom fallback is not invoked.

## Third-party exact-unit photography

Primary listing: https://www.ebay.com/itm/165588009864

Ten original 1600-pixel listing photographs were downloaded from the listing's public `i.ebayimg.com` gallery and inspected at original detail. They show one `N9K-C9336PQ V02` with readable factory PID, readable `N9K-PAC-1200W V01` PSU label, readable burgundy `N9K-C9300-FAN3` fan stripe, exact front, exact rear, both informative three-quarter angles, top labels, and side geometry. The listing states PID `N9K-C9336PQ` and dual power. Hashes are in `qa/reference/third-party-sha256.txt`; image-by-image findings and exclusions are in `source/image-inspection.csv`.

Seller barcode stickers and loose black retaining straps are not part of the user screenshot configuration and are excluded during source-locked generation. Factory Cisco/Nexus branding, model badge, module identity colors and factory warning/ground labels are retained. Unit-specific serial/barcode data is not reproduced.

Additional discovery pages reviewed:

- https://dedicatednetworksinc.com/product/new-open-box-cisco-n9k-c9336pq-nexus-9k-aci-spine-36p-40g-qsfp/
- https://www.icpnetworks.co.uk/cisco/n9k-c9336pq
- https://serverorbit.com/buy-cisco-n9k-c9336pq-36-ports-l3-switch-40g-ethernet-qsfp/ (page and direct full image returned 403 during preservation; result used only as a discovery lead)

## Search log

Official identity/configuration queries:

- `site:cisco.com N9K-C9336PQ hardware installation guide PDF dimensions airflow AC power supply`
- `site:cisco.com N9K-C9336PQ datasheet 36-port front rear airflow NXA-PAC`
- `site:cisco.com N9K-C9336PQ 3D model CAD STEP GLB Visio`
- `site:cisco.com/c/dam N9K-C9336PQ CAD OR STEP OR STL OR OBJ OR FBX OR GLB OR glTF`

Exact exterior and commerce queries:

- `"N9K-C9336PQ" front rear`
- `N9K-C9336PQ front rear real photo`
- `N9K-C9336PQ side top used`
- `N9K-C9336PQ rear burgundy N9K-PAC-1200W`
- `Cisco Nexus 9336PQ teardown bottom`

Official-model outcome: exact official interactive model found and preserved; no exact public GLB, glTF, STEP, OBJ or FBX download was found. The optional official format is Kaon/Lepton XML + binary mesh + JPEG textures.

Bottom outcome: no commerce underside photo was required for fallback because the exact official model package exposes all four bottom texture quadrants and matching side-edge evidence.

## Dimension interpretation

Cisco publishes 17.5 in width, 22.5 in depth and 3.5 in height. The self-built body uses exact inch conversions `444.5 × 571.5 × 88.9 mm`, while the ledger also records Cisco's rounded `445 × 571 × 89 mm` values.

The N9K-C9300-RMK front brackets are a separately documented kit. The user screenshot and exact-unit photographs include both front brackets. Their combined rack span is modeled as the nominal 19 in (482.6 mm), yielding 19.05 mm extension on each side of the 444.5 mm body. This is a documented engineering inference with ±1.5 mm tolerance rather than a Cisco-published chassis width. Brackets exist only at the port plane; there are no rear ears.
