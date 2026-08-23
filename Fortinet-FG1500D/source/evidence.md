# Evidence and source log

Access date for web sources: 2026-08-23 (Asia/Singapore).

## User-provided target row

URL/local path: `/root/.codex/attachments/5b35003e-f694-4867-9ec2-064ed79bae34/codex-clipboard-adb83d36-d04a-4b31-ba4c-78fd9865fae8.png`
claimed_model: row 3, vendor 飞塔 / model FG1500D
variant: D generation, AC, 2U; user explicitly freezes front and rear visible configuration
view_or_dimension: front and rear elevations in a comparison table
authority: user-owned delivery specification
source_class: user-provided screenshot
visual_origin: rendered/elevation imagery embedded in a UI table
primary_identity_style_reference: yes for requested row appearance
image_inspection_notes: original 1034x1320 image was inspected at original detail; the row-3 front is a white/pale-green FG-1500D face with the documented 16 SFP, 16 RJ45 and 8 SFP+ groups. The row-3 rear shows four individually framed upper fan trays, a central/right blank-panel field, dual vertical AC PSUs at far right, and segmented lower vent/blank panels.
proves: requested delivery row and the explicit rear configuration to reproduce
limitations: the rear conflicts with Fortinet catalog documents and does not visually match the standard production rear documented below.

## Fortinet Chinese datasheet

URL: https://www.fortinet.com/content/dam/fortinet/assets/data-sheets/zh_cn/FortiGate_1500D.pdf
local original: `source/originals/FortiGate-1500D-Datasheet-ZH.pdf`
SHA-256: d7c282c4709efc040c934a9d263afcdba8ffa1cd21d8d9c6332090255e2de003
document: FortiGate 1500D 技术参数表, 6 pages
pdf_page_or_figure: PDF page 3 hardware diagram; PDF page 5 specifications
claimed_model: FG-1500D / FG-1500D-DC and FG-1500DT
variant: use FG-1500D AC column only
authority: official
source_class: datasheet
visual_origin: technical diagram and official product render
primary_identity_style_reference: supporting
image_inspection_notes: rendered pages inspected at original detail. Page 3 proves the exact D front port groups and the distinction from 1500DT. Page 5 quotes 89 x 438 x 554 mm, 2 RU, 14.70 kg, 100-240 V AC and redundant hot-swap power.
proves: exact PID, D front configuration, AC power, U height and body dimensions
limitations: the official rear image is the standard rear, not the user-locked row rear; no full side/top/bottom elevation.

## Fortinet QSG supplement 2020-07-28

URL: https://fortinetweb.s3.amazonaws.com/docs.fortinet.com/v2/attachments/c48097f0-1a12-11e9-9685-f8bc1258b856/FortiGate-1500D-Supplement.pdf
local original: `source/originals/FortiGate-1500D-QSG-20200728.pdf`
SHA-256: e9a14901ff13340288e94de464ecfc9c979e7a45d4bcc7f1079aacab7eefec99
document: FortiGate 1500D Information / QuickStart Guide, 11 pages
pdf_page_or_figure: pages 1-4 rendered to `source/pdf-pages/QSG-p01..04.png`
authority: official
source_class: quick-start guide
visual_origin: official product photograph/render and technical diagram
primary_identity_style_reference: yes for front material/color; supporting-only for rear because user locked a different rear
image_inspection_notes: pages inspected at original detail. Page 1 shows top/front material and wordmark. Page 2 shows the standalone rack brackets and confirms they are boxed accessories. Page 3 enumerates all front connectors and shows the catalog AC/DC rear. Page 4 gives LED meanings.
proves: front layout, logo, top wordmark, accessory rack brackets, factory paint, standard PSU shape
limitations: standard rear conflicts with requested row rear; no direct left/right/bottom elevations.

## Fortinet 2017 cooling-fan technical note

URL: https://community.fortinet.com/fortigate-3/technical-note-redundancy-of-fortigate-1500d-cooling-fans-97527
local images: `source/originals/Fortinet-community-FG1500D-fan-note-1.png`, `...-2.png`
authority: official Fortinet community technical note
source_class: technical note
visual_origin: official rear diagram and airflow diagram
primary_identity_style_reference: no
image_inspection_notes: exact-model rear diagram inspected. Text says three chassis cooling fans plus one fan in each PSU.
proves: catalog FG-1500D rear is two PSUs plus three chassis cooling fans
limitations: contradicts the user-provided rear; retained to prevent accidental claims that the row rear is the catalog rear.

## NIST/Fortinet FIPS security policy

URL: https://csrc.nist.gov/CSRC/media/projects/cryptographic-module-validation-program/documents/security-policies/140sp4612.pdf
local original: `source/originals/FortiOS-6x-FIPS-Security-Policy.pdf`
SHA-256: 97c21a6e4b4d3887746c7951dc67553c41b09bdd883756e270fe281d3ec5e7d5
document: FortiOS 6.x FortiGate FIPS 140-2 Level 2 Non-Proprietary Security Policy, 54 pages
pdf_page_or_figure: p22 Figure 7; p35 Figure 16; p36 Figure 17
authority: official/government-hosted
source_class: security policy
visual_origin: technical diagrams and real photographs
primary_identity_style_reference: material/geometry support
image_inspection_notes: p22 shows the standard FG-1500D front/rear. p35 is a real bottom/rear power-supply corner for the shared 1200D/1500D enclosure. p36 is a real top/left-side enclosure-seal view for 1200D/1500D. All rendered pages were inspected at original detail.
proves: D-generation body material, standard rear conflict, side/top seam and bottom/rear edge treatment
limitations: photos are shared 1200D/1500D enclosure evidence and do not prove a full underside.

## Exact-model real and reseller images

- `source/third-party/amazon-renewed-front.jpg`, URL https://m.media-amazon.com/images/I/71NYSg1eNrL._AC_SL1500_.jpg, SHA-256 2abafad900b4911a518edf960d114f90b4949bf6a455601287950e1396b56840. Exact front/top product photograph/render; no rack ears; inspected; proves top wordmark, front materials and complete ports.
- `source/third-party/melbourne-2181487.jpg`, URL https://cdn11.bigcommerce.com/s-2kqswvsy80/images/stencil/1280x1280/products/42961/2181487/2181487__11815.1689583091.jpg. Exact front/top product render; inspected; supports front and top.
- `source/third-party/melbourne-2181489.jpg`, URL https://cdn11.bigcommerce.com/s-2kqswvsy80/images/stencil/1280x1280/products/42961/2181489/2181489__49351.1689583097.jpg, SHA-256 420a3f5b42182997300c8565bf28e12eeab91c951e55d850741025032d83ebd6. Exact front-left/top angle; inspected; proves physical-left side is mostly blank and lacks the right-side regulatory label.
- `source/third-party/melbourne-2181491.jpg`, URL https://cdn11.bigcommerce.com/s-2kqswvsy80/images/stencil/1280x1280/products/42961/2181491/2181491__44731.1689583102.jpg, SHA-256 410953fcce1e90839972ce1623f7dfb59b72f3e0c177fab50d118f437af70730. Exact front-right/top angle; inspected; proves physical-right regulatory label and different fastener layout.
- `source/third-party/ebay-front.png`, URL https://i.ebayimg.com/images/g/42oAAOSwbfBoFRA5/s-l1200.png, SHA-256 54474169d465ba8568a9d39274e8a32cbf2be25e2e5bd664ce0ed0ea3fa83f83. Real used exact FG-1500D front/left/top photo; missing right SFP+ cage/module and one rack bracket; material-only supporting source, never a complete configuration authority.
- `source/third-party/ebay-358014739037-front.jpg`, URL https://i.ebayimg.com/images/g/0nIAAeSwTGppPcXO/s-l1200.jpg, SHA-256 b535293b0db8a04cc215de80254154ae742574d34a02779904a1ecc7626445b3. Real used exact FG-1500D front/top photo; inspected; supports wear and metal texture but not a straight elevation.

## Bottom search log and fallback decision

Searched official datasheet/QSG/FIPS material, Fortinet documentation, public 3D/CAD/viewer resources, exact-model reseller and eBay listings, ANATEL external-photo record, local-language queries, and web/image queries for `FG-1500D underside`, `bottom`, `top side`, `used`, and `rear bottom`. The ANATEL record identifies external photos but its legacy object is unavailable (`skipped_missing_object`). No usable full exact-model underside was recovered. Therefore bottom is the only controlled fallback: a conservative opaque ivory-white sheet-metal underside at 438:554 with only the verified edge treatment; no logo, labels, vents, holes, feet, rails, seams, fasteners or protrusions are invented.

## Public optional 3D search

Fortinet official pages, support downloads, media, CAD/STEP/OBJ/FBX/GLB/glTF and viewer queries produced no exact publicly downloadable official 3D asset. A community SketchUp model was found at https://3dwarehouse.sketchup.com/model/a6f5e5e7-ed33-483d-a95c-1f9baa8ef976/Fortigate-1500D. The entity metadata names creator `Jesus Ruiz`, `isVerified: false`, `isCertified: false`, bounds 421 x 442 x 150 mm, 2,320 polygons and 17 materials; it is not Fortinet official CAD and has incorrect proportions. Its public USDZ conversion is preserved unchanged as `source/optional-3d/3D-Warehouse-Fortigate-1500D.usdz` (SHA-256 e90da2985a23cbbe7e9c79d699a27534e6ad1c813b5232904a32713760d26c69) solely as an optional non-authoritative reference. Inspection found generic/incorrect content including a texture named `Dell_S4048_Front_01.png`; it is excluded from the main build.

### Final official-3D recheck

On 2026-08-23 after the model and WebGL audits, official-domain searches were repeated for `FortiGate 1500D` with `3D`, `GLB`, `glTF`, `CAD`, `STEP`, `OBJ`, and `FBX`. Fortinet results still exposed only the hardware-document library, the FG-1500D QSG supplement, datasheets, and architecture documentation; no exact publicly downloadable official 3D asset or public official viewer resource was found. The community 3D Warehouse USDZ remains the only preserved optional model and remains excluded as non-official and dimensionally/content incorrect.
