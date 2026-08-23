# Evidence and inclusion rules

Access date: 2026-08-23 to 2026-08-24 (Asia/Singapore)

## Resolved physical subject

The delivery subject is the fully visible 2U Dell EMC PowerEdge C6400 enclosure with four air-cooled PowerEdge C6420 sleds, a 24 x 2.5-inch SAS/SATA front, 24 installed drive carriers, and two shared EPP 1600 W AC PSUs. The user screenshot itself is the configuration authority. Dell's installation manual and technical guide prove the host/sled relationship, front mapping, rear sled enumeration and valid 24-SFF configuration. Inspected real photographs bind material and surface appearance.

The screenshot rear matches Dell's factory/default C6420 rear composition: empty low-profile PCIe and mezzanine/OCP openings with their vented blanks, four blue pull handles, and no visible add-in NIC/SFP/QSFP card. The chosen real rear photograph has the same four-node/default-I/O/1600-W-AC appearance.

## Dimension interpretation

Dell Figure 1 labels overall width `Xa=482.6 mm`, body width `Xb=448 mm`, height `Y=86.8 mm`, front projection `Za=26.8 mm`, body depth/datum span `Zb=763.2 mm`, and overall installed depth `Zc=797.3 mm`. The GLB uses overall bounds 482.6 x 86.8 x 797.3 mm. The body is 448 mm wide; front control/mounting housings and rear sled/PSU projections provide the larger overall bounds. No shipping dimension is used.

## Official document matrix

| Source | Preserved file | Relevant pages/figures | Proves |
|---|---|---|---|
| Dell EMC PowerEdge C6400 Installation and Service Manual | `source/originals/dell-poweredge-c6400-installation-service-manual.pdf` | PDF pages 6-10, 20, 32-35; Figures 1-7, 17, 30-34 | supported 24-SFF + C6420 assembly, front, control panels, rear, sled order, two PSUs, top covers and service geometry |
| Dell EMC PowerEdge C6400 Technical Specifications | `source/originals/dell-poweredge-c6400-technical-specifications.pdf` | PDF pages 4-6; Figure 1 and Tables 1-4 | dimensions, maximum installed weight, two AC PSUs, 24 drives and six drives per sled |
| Dell EMC PowerEdge C6400 and C6420 Technical Guide Rev A07 | `source/originals/dell-poweredge-c6400-c6420-technical-guide.pdf` | PDF pages 13-16; Figures 1-4, Table 4 | four-node chassis identity, front 24-SFF, rear sled anatomy and port names/order |

All three PDFs were preserved byte-for-byte, text-extracted, relevant pages rendered to PNG, and the page images inspected at original detail. The dedicated `pdf` skill was unavailable in this session, so PyPDF and PyMuPDF were used as the local extraction/render fallback while retaining the same textual-and-visual evidence process.

## Real-photograph matrix

| Group | URL | Local files | Inspection conclusion |
|---|---|---|---|
| User-linked Reddit/Imgur exact system | https://www.reddit.com/r/homelabsales/comments/10s2y93 and https://imgur.com/a/uec15Ij | `source/third-party/imgur-uec15Ij-cover.jpeg` | exact C6400 24-SFF with all 24 Dell 14G carriers; direct front three-quarter; binding front material/layout source |
| Techyparts exact four-node system | https://store.techyparts.com/products/dell-poweredge-c6400-24sff-4-node-c6420-dual-lga3647-h730p-x710-cto-2u-server | `techyparts-01.jpg` to `techyparts-09.jpg` | exact C6400/C6420 family; `02` is closed four-sled rear with two 1600 W AC PSUs and default blank slots; `01` shows top/front with drive blanks; `03-09` are open sled/internal detail and not face primaries |
| xByte/eBay exact four-node system | https://www.ebay.com/itm/384577208062 | `ebay-xbyte-01.jpg` to `ebay-xbyte-05.jpg` | exact closed C6400: front/top, direct right-side, top/rear, rear; `03` is binding right face and `02` binding top/left reconstruction reference; `05` is packaging context only |
| ITInStock/eBay exact chassis and sled gallery | https://www.ebay.co.uk/itm/204971395487 | `ebay-itinstock-01.jpg` to `ebay-itinstock-08.jpg` | exact chassis front/top/rear plus standalone sled internals; front has empty drive bays and is not final-config binding; confirms panel geometry and default four-sled rear |
| Bargain Hardware/eBay exact 24-SFF four-sled system | https://www.ebay.co.uk/itm/405204206396 | `ebay-bargainhardware-01.jpg` to `ebay-bargainhardware-06.jpg` | exact front/rear/open top/sled views; drive blanks or removed parts differ, so used only for supporting chassis/top/sled geometry |
| Abacus/eBay exact 24-SFF four-sled system | https://www.ebay.com/itm/126737099835 | `ebay-abacus-01.jpg` to `ebay-abacus-03.jpg` | exact front/top/rear warehouse photos; carrier count differs/empty positions present, so supporting geometry only |

Every listed local raster was opened at original detail. Seller backgrounds, inventory stickers, power-cable straps, missing drives, missing covers and open/removal states are classified as non-factory context and are excluded from canonical faces.

## Video escalation

- xByte `Dell PowerEdge C6400 Inside Look`, https://www.youtube.com/watch?v=cHwOED4bQpE, preserved as `source/third-party/xbyte-c6400-inside-look.mp4`; inspected through `video-frames/xbyte-contact-sheet.jpg`. It proves front/top/rear and internal fan/cover states but never provides a usable underside.
- IT Creations `Dell EMC PowerEdge C6420 Server REVIEW`, https://www.youtube.com/watch?v=7Uik0yhjZpE, preserved as `source/third-party/itcreations-c6420-review.mp4`; both five-minute contact sheets were inspected. It proves the four-node assembly, default rear anatomy and sled details but no exact underside.

## Browser/dynamic-page escalation

The Dell manual page was opened through a real browser after the Playwright skill prerequisite was satisfied. Dell's edge returned HTTP 403 `Access Denied`; the semantic web index and the public `dl.dell.com`/`i.dell.com` PDF endpoints remained accessible. Multiple dynamic eBay/Shopify galleries were opened through their gallery links and the underlying original images were preserved. No authentication, access control or private API was bypassed.

## Left-side reconstruction gate

No direct orthographic left photograph was found. The left face is therefore `MULTI_REFERENCE_RECONSTRUCTION`, not a mirrored right. Exact closed top/front/rear photographs jointly prove the left silhouette, galvanized material, edge seams, front Dell EMC control-housing projection and rear installed-sled projection. The direct right photograph constrains chassis manufacturing vocabulary only. The reconstruction explicitly omits the right-side QR label and uses an independently composed fastener layout; left and right PNG bytes and visual landmarks must differ.

## Bottom fallback search log

Searched official Dell documents, support pages, technical/service manuals, product media, Visio/CAD/AR/3D combinations, dynamic galleries, xByte, Techyparts, ITInStock, Bargain Hardware, Abacus, eBay, Reddit/Imgur, NewServerLife, ETB, auction/dealer pages, English queries (`underside`, `bottom`, `teardown`, `side`), Chinese queries (`底部`, `拆机`, `戴尔 C6400 C6420`) and the two full product videos above. No usable exact underside was found. The bottom is therefore the sole permitted `GENERIC_BOTTOM_FALLBACK`: an opaque plain galvanized 448 x 763.2-ratio panel with verified edge thickness and no unsupported identifying detail. Final status cannot exceed `PASS_WITH_BOTTOM_FALLBACK`.

## Official 3D result

No exact public official 3D file or viewer asset was found. See `source/optional-3d/README.md`. The new standard/web GLBs remain fully self-constructed.
