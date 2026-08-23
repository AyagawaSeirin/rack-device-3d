# Evidence, dimensions, configuration and search log

Access date for all web sources: 2026-08-23. The user screenshot is the highest-priority installed-configuration lock; HPE documentation is the product/compatibility/dimension authority.

## User configuration lock

- Local original: `source/originals/user-config-lock-full.png`
- SHA-256: `7efb5b4ccf0095fee7977f6a95083306935b9e63a990fd83bb8883fc49fdfeb9`
- Row-6 crop: `qa/reference/user-config-lock-row6.png`
- Proves: HPE DL360G9/3.5-inch row; 1U 4LFF front family; the exact rear layout used for this row; dual PSU state; no bezel.
- Limitations: thumbnail resolution cannot establish small label text, wattage or hidden surfaces. Those facts are resolved only from exact HPE documents and cross-checked exact-device photographs.

## Official HPE sources

### HPE ProLiant DL360 Gen9 — Identifying Components

- URL: https://support.hpe.com/hpesc/public/docDisplay?docId=c04444501&docLocale=en_US
- Authority/source class: official HPE dynamic support document
- Browser API response preserved: `qa/browser/hpe-identifying-components-api.txt`
- Exact attachments preserved unchanged:
  - `source/originals/a00020643.gif` — official 4LFF front diagram, SHA-256 `88e28352124ff8bf3e30d27f54022c2926e571d1265993b2c1e0e100d52525b5`
  - `source/originals/a00020644.gif` — official rear diagram, SHA-256 `2299aa77be57e4e57ecc5872908c732bf5a3eb2a9c2d7eb0b9fc74184b6e924d`
  - `source/originals/a00020645.gif` — system-board diagram, SHA-256 `58d2e2fe4a3c1f14c3c573cb65c35359990bf60b5808f847b3fabaa661d15e62`
  - `source/originals/c04444778.gif` — internal-layout photograph, SHA-256 `b07000cbc0ebb460c377993c23ba02c37042adab63fb07a0052a0eaec3c6aa94`
- Proves: four LFF bays; optional 4LFF optical/VGA/USB/SID positions; rear slot 1/2/3; PSU 2 and 1; VGA; embedded NIC 4/3/2/1; iLO4; optional serial; two USB3; FlexibleLOM bay; system/fan layout.
- Visual-origin classification: official technical diagrams plus official real internal photograph.

### HPE ProLiant DL360 Gen9 — Specifications

- URL: https://support.hpe.com/hpesc/public/docDisplay?docId=emr_na-c04443049
- Authority/source class: official HPE dynamic support document
- Browser response: `qa/browser/hpe-specifications-api.txt`, SHA-256 `a41c2bd551259025194b97e2c5254706b0ecb212d2e9d9b495dead0beb9ee7de`
- Browser page screenshot: `qa/browser/hpe-specifications-page.png`
- Quoted scope: dimensions H×W×D; 4LFF = 4.32 × 43.46 × 75.0 cm (1.7 × 17.1 × 29.5 in).
- Normalized: body height 43.2 mm, body width 434.6 mm, body depth 750.0 mm.
- Limitations: rack-ear width and small removable-part projections are not separately enumerated on this page; they are ledgered from the 19-inch rack span and exact photos with an explicit ±2 mm tolerance.

### HPE ProLiant DL360 Gen9 QuickSpecs

- URL: https://www.hpe.com/psnow/doc/c04346229.pdf
- Authority/source class: official HPE QuickSpecs
- Relevant pages: Overview/rear p.2; dimensions/form factor p.9; storage p.47; technical dimensions p.48 in the accessed version.
- Proves: 1U; 4LFF option; three PCIe positions with slot 3 optional; dual HPE Flexible Slot PSU layout; 4x1GbE FlexibleLOM example; dimensions without bezel; four LFF storage bays.
- Retrieval note: official text and PDF render were inspected through the web path. Direct file transfer from `www.hpe.com` repeatedly failed with `ERR_HTTP2_PROTOCOL_ERROR`, so no partial or corrupted file was retained.

### HP/HPE ProLiant DL360 Gen9 Maintenance and Service Guide

- Original HPE document mirrored unchanged from Newegg: https://images10.newegg.com/User-Manual/User_Manual_59-108-646.pdf
- Local: `source/originals/HPE-ProLiant-DL360-Gen9-Maintenance-Service-Guide-767928-006-mirror.pdf`
- SHA-256: `2b72d0f6c4ccdbb68f1810ddc51f2cfdcef18837189fc931134c34cb52bdefbf`
- Document identity: HP ProLiant DL360 Gen9 Server Maintenance and Service Guide, part 767928-001, Edition 1, September 2014.
- Text extraction: `source/pdf-pages/Maintenance-Service-Guide-text.txt` using Ghostscript `txtwrite` because the optional PDF skill was not installed in this session.
- Visually inspected renders include: p.15 access panel/chassis exploded view; p.16 exact left/right ears and LFF rail part IDs; p.19 system components/PSU; p.27 rear access; p.29 4LFF Systems Insight Display; p.32-33 AC PSU/access panel; p.45-46 ear/side bracket; p.48-49 4LFF backplane/FlexibleLOM; p.75 4LFF front components; p.77 4LFF controls; p.80 exact rear; p.81 PSU/rear LEDs; p.83 system board.
- Proves: independent ear parts; access-panel construction; top seam/latch; LFF-specific rail identities; AC PSU body/handle; four LFF backplane; side fastener/rail features; exact front/rear component order.

## Exact-device photographs and renders

### NewServerLife 4LFF front

- Page: https://newserverlife.com/configure/hp_proliant_dl360_gen9_4lff/
- Image: https://newserverlife.com/upload/iblock/d9e/dl360_g9_4lff.png
- Local: `source/third-party/newserverlife-dl360-g9-4lff.png`
- SHA-256: `ec72ebf08b5b1cd9622b484db6c1908dc30da5ba778f41e978711cc3c4e4c607`
- Authority/source class/visual origin: secondary refurbisher / real photograph.
- Proves: exact four-carrier LFF front, media/control strip, ears, period HP and ProLiant DL360 Gen9 badges, carrier handle and red release-tab form, photographic material/style.
- Limitations: elevated front angle; gray seller canvas; configuration labels are listing-specific and not treated as readable identity data.

### Piospartslap exact 4LFF chassis set

- Page: https://www.piospartslap.de/HP-Enterprise-ProLiant-DL360-G9-Server-2xE5-2690-V3-0GB-4-Bay-35-LFF-2x-25-Intern-SFF
- Local files: `source/third-party/pios-15304-1.jpg`, `pios-15304-2.jpg`, `pios-15304-3.jpg`
- SHA-256: `06f162...2eca`, `591984...7a7c`, `616299...7392`
- Authority/source class/visual origin: secondary used-equipment seller / real photographs.
- Proves: exact LFF 750 mm chassis depth; top cover/perforation/seam/latch; independent front and rear material character; rear 500W AC PSU fan/handle construction; side-edge and rail hardware evidence.
- Limitations: this unit's FlexibleLOM uses a different two-port adapter and its drive bays are empty. Those parts are not copied into the locked model; screenshot/HPE render controls them.

### Exact rear component render

- Page: https://www.hp-pro.net/Netshop/Servers-HP/Proliant-DL/360/795236-B21.html
- Image/local: `source/third-party/hp-pro-net-dl360g9-rear.jpg`
- SHA-256: `e2e44bb74f786f129b9c9574591f50021563b150ec92fb052b9b04afa3207362`
- Visual origin: HPE official rear product render reproduced by reseller.
- Proves: the screenshot-matched rear: three PCIe positions, 4x1GbE FlexibleLOM, two USB3, DB9 serial, iLO4, four embedded NICs, VGA and dual Flex Slot PSU.
- Supporting exact rear image: `source/third-party/maychuvina-dl360g9-rear-8rj45.png`, SHA-256 `7741539f...15c0f9`, same eight-network-port arrangement; seller watermark/background excluded.

### Servak/Pios exact chassis top and rear corroboration

- Servak page: https://servak.com.ua/servers/servera-hp-gen9/server-hp-proliant-dl360-gen9-4-lff.html
- Local: `source/third-party/servak-dl360g9-lff4.jpg`, SHA-256 `21882e7c...400d8`
- Proves: exact Gen9 top panel and rear material, two PSU state, rear-edge silhouette.
- Limitations: reseller sticker on top and a different FlexibleLOM. Sticker and differing adapter are excluded.

## Bottom evidence exhaustion and controlled fallback

Searches performed:

- Official: HPE support documents, QuickSpecs, maintenance/service guide, parts support, cabling, rail/access-panel material, HPE media/3D/AR/CAD terms.
- Browser: dynamic HPE Identifying Components and Specifications pages, their public API payloads and attachments.
- Third party in English, Chinese and German: exact-model reseller, used-equipment, marketplace, auction, teardown, rail-installation and underside/bottom queries; `DL360 Gen9 underside`, `DL360 G9 bottom`, `DL360 Gen9 底部`, `DL360 G9 4LFF side`, `DL360 Gen9 LFF rails`.
- Cross-check: a Reddit report confirms holes exist on an exact DL360 Gen9 bottom but supplies no usable orthographic image; no identity-bearing bottom pattern was accepted from text.

Result: no usable exact DL360 Gen9 4LFF underside photograph or drawing was found. `GENERIC_BOTTOM_FALLBACK` is therefore invoked. The inspected fallback material reference is an HPE DL120 Gen9 1U underside photograph, local `source/third-party/generic-bottom-fallback-hpe-dl120g9.jpg`, SHA-256 `512afea833fd331a9df9de6062a2d7da0100767fb1e4778b0125d2639e82ed7a`. It is used only for galvanized-sheet color/finish. Its holes, stampings, feet, labels and seams are explicitly forbidden from the DL360 output.

## Optional official 3D search

Queries covered exact model, SKU 755259-B21, `GLB`, `glTF`, `STEP`, `CAD`, `OBJ`, `FBX`, `AR`, HPE support/media and public 3D indexes. No exact public HPE 3D file was found. No community file is substituted or called official. See `source/optional-3d/README.md`.

## Inclusion rules and modeling tolerances

- Published 434.6 × 43.2 × 750.0 mm is treated as the bezel-free 4LFF body envelope.
- Standard rack-flange outer span is modeled at 482.6 mm; ears are separate front-only assemblies.
- Source-measured projections: carrier handles 8 mm forward, PSU handles/latches 12 mm rearward; tolerance ±2 mm.
- The resulting expected GLB envelope is 482.6 × 43.2 × 770.0 mm. Texture planes do not inflate bounds.
- Rails, cable-management arm, seller labels and cables are excluded. Installed drive carriers, control strip, ports, PCIe blanks, fan/PSU faces, HPE/ProLiant branding and front ears are included.
