# Evidence and source-lineage record

Access date: 2026-08-23

## Authoritative identity and dimensions

- Fortinet QSG page: https://docs.fortinet.com/document/fortigate/hardware/fortigate-3700d-qsg-supplement
- Preserved QSG PDF: `source/originals/FG-3700D-Supplement.pdf`; SHA-256 `d2e49206584d9d9b760aec52231f6f056b7649c4f06be040d348e9f554efe7be`.
- Fortinet data sheet: https://www.fortinet.com/content/dam/fortinet/assets/data-sheets/ja_jp/FGT3700DDS.pdf. It states 133 x 437 x 579 mm, 3 RU, 21.3 kg, 4 QSFP+, 20 SFP/SFP+, 8 ULL SFP+, 2 RJ45 management, 1 USB-A/1 USB-B, 1 serial console, and redundant hot-swappable power.
- NIST-hosted Fortinet FIPS security policy: https://csrc.nist.rip/groups/STM/cmvp/documents/140-1/140sp/140sp2369.pdf; SHA-256 `01134bde8a0b34f0cd6184d27b791c5a0cb0d5e2e988b9250e6b4a597b037f26`. Figure 2 and tables identify the FG-3700D front/rear connectors, six FAN indicators, two power supplies, and ground point.

The environment did not expose a PDF skill or Poppler. All relevant PDF pages were instead rendered with Ghostscript at 180 dpi to `source/pdf-pages/` and visually inspected at original detail. Textual claims were cross-checked against the Fortinet Document Library's indexed PDF text.

## Exact external photographs

- ANATEL external-photo record: https://fccid.io/ANATEL/00228-15-08867/FortiGate-3700D-manual/C91A7ACF-EABF-42DE-A7A2-2875B299D103, related document `EXT / Fotos Externas`. Preserved PDF `source/third-party/anatel-external-photos.pdf`; SHA-256 `6b31ff394e96f1d433c6011adf3d8cf9bca2010f879844294ff7c6c5679c559d`. Pages prove exact AC badge, front, rear, both non-mirrored sides, top, and bottom.
- eBay listing 236708345684: https://www.ebay.com/itm/236708345684. Listing claims model and MPN FG-3700D and dual AC PSU. Seven preserved 1600 px images show front ports, model badge, rear six-fan/dual-AC configuration, top, and bottom.
- eBay listing 236755802715: https://www.ebay.com/itm/236755802715. Listing claims MPN FG-3700D and model FG-3700D-USG. Nine preserved 1600 px images show full front, both sides, top, exact side regulatory badge, rear and included cables. Seller QR/inventory stickers and loose cables are excluded.
- EnBITCon FG-3700D page: https://www.enbitcon.de/shop/fortinet/fortigate-firewall/high-end/fortinet-fortigate-3700d-dc-firewall-end-of-sale-life-fg-3700d-dc. Its front is shared between AC/DC; its `FG-3700D-Bk...jpg` rear photograph is the AC layout and is used only after cross-checking against QSG/FIPS/ANATEL/eBay AC evidence.

## Request image

- Original request table: `source/originals/request-table.png`; SHA-256 `7efb5b4ccf0095fee7977f6a95083306935b9e63a990fd83bb8883fc49fdfeb9`.
- `qa/reference/request-row2.png` is a convenience crop, not a primary source.
- The second-row front is consistent with FG-3700D. The rear thumbnail is too low-resolution and visually inconsistent with all exact-PID sources, so it is not allowed to override the verified assembly.

## Source classification and exclusions

- Primary face locks are real exact-device photographs or exact-PID regulatory photographs.
- QSG/FIPS diagrams are supporting geometry references only.
- The NetBox front elevation and all AI outputs are derivatives/supporting material, never primary identity/style sources.
- FG-3700D-DC is excluded by AC requirement. FG-3700DX/3800D/3700F/1500D are excluded by generation, height, port count, or rear arrangement.

## Browser escalation note

The eBay galleries were opened through the rendered web channel and all image links were enumerated. A Playwright CLI attempt was also made under the required skill, but Chromium sandboxing rejected root execution even after a local no-sandbox configuration attempt; no private or access-controlled resources were bypassed. Public gallery URLs were downloaded directly and preserved unchanged.
