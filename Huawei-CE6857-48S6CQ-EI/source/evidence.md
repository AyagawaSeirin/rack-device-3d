# Evidence and build decisions

## Frozen result

The twelfth readable device row is Huawei `CE6857-48S6CQ-EI`. The delivered installed configuration is the screenshot-matched `02352CHS / CE6857-EI-F-B0B`: 1U, 48 empty SFP+ cages, 6 empty QSFP28 cages, four blue `FAN-031A-F` modules, and two airflow-matched 600 W AC modules. Blue `AIR IN` on the power/fan face means that face is the intake and the port face is the exhaust. Huawei calls this front-to-back airflow / port-side exhaust.

No CE6855, CE6856, CE6857 without `EI`, CE6857E, CE6870, or red `FAN-031A-B` configuration is used as identity evidence.

## Official public 3D

- Info-Finder page: https://info.support.huawei.com/info-finder/search-center/en/enterprise/Switches/ce6857-48s6cq-ei-pid-23152997/web3d
- Viewer: https://ar.ipd.huawei.com/3d-model/?product=CE6857-48S6CQ-EI&modelNumber=PARM6039&language=en_US
- Viewer asset key: `39bfcb9e8939f8c61e8e6a26fbcf2ad2d25fbf29ce952d5621106849211fedc4`
- Metadata: `PARM6039`, model `CE6857-48S6CQ-EI_Web_AR`, GLB version `D.3`, public time `2025-07-11 15:11:35`
- Preserved unchanged: `source/optional-3d/CE6857-48S6CQ-EI-PARM6039-official.glb`
- SHA-256: `028500da34c65d5a2004b3b72d8ca2dde733778952c71d4afb028c431fa1992c`

The public download was captured from the browser's successful public request. The product-gallery ZIP button redirected to Huawei login, so the ZIP was not bypassed; the six public preview originals were downloaded individually from their public image endpoints.

The official file is retained only as an optional original and geometry/color reference. Its mesh is not copied into the newly authored standard or web GLB. `qa/official-glb-audit.json` records the original file's own structural warnings (including broad BLEND materials and a 5.03% raw-bounds proportion mismatch); it remains byte-for-byte unchanged.

## Official Huawei manual pages

Document: *CloudEngine 8800, 7800, 6800, and 5800 Series Switches Hardware Description (Versions earlier than V200R020C00)*, Issue 36, 2021-03-10, Huawei Technologies. Public copy: https://iq-terra.ru/upload/iblock/402/vmx06ym2910bngs6bigw73vmzok95kjj.pdf

- rendered PDF page 285 / printed page 287: exact power face, port face, left/right sides, ground, CONSOLE, ETH, USB, four fan slots, two power slots;
- rendered page 286 / printed page 288: 48 SFP+, 6 QSFP28, port/middle/power-side mounting holes;
- rendered page 288 / printed page 290: blue `FAN-031A-F` plus blue PSU `AIR IN` diagram for port-side exhaust; red `FAN-031A-B` diagram is explicitly excluded;
- rendered pages 289-290 / printed pages 291-292: port families and management/USB functions;
- rendered page 291 / printed page 293: 442.0 x 420.0 x 43.6 mm, AC, 1U-equivalent chassis height;
- rendered page 292 / printed page 294: 1+1 power and 3+1 fan redundancy;
- rendered page 293 / printed page 295: `02352CHS`, 2 AC, 4 fans, port-side exhaust.

PDF text was extracted to `source/originals/*.txt`; each listed page was rendered to `source/pdf-pages/` and visually inspected at original detail. A dedicated PDF skill was not installed in this session, so the same required extraction/render/inspection sequence was performed with local PyMuPDF.

## Dimensions and inclusion

Authoritative bare/installed chassis dimensions are `442.0 W x 420.0 D x 43.6 H mm`. The official CAD's X scale is anchored to 442 mm. The power-side U brackets extend the model depth to approximately 457.9 mm; they do not increase width. No unsupported lateral 482.6 mm front flanges are installed in the locked product photographs, so the delivered model keeps the verified 442 mm visible width while the two rear mounting ears are separate geometry.

## Face modes

- Front (port side): `SOURCE_LOCKED_GENERATION`, binding real official straight photo.
- Rear (power/fan side): `SOURCE_LOCKED_GENERATION`, binding real official straight photo.
- Left/right/top: `MULTI_REFERENCE_RECONSTRUCTION`, binding exact real official three-quarter photos plus exact official CAD orthographic renders. Left and right remain separate and are never mirrored.
- Bottom: `MULTI_REFERENCE_RECONSTRUCTION`, because the exact official public CAD provides a complete exact underside. `GENERIC_BOTTOM_FALLBACK` is not used.

## Image inspection notes

All six Huawei gallery originals are exact PID images, RGBA, uncropped product views with no reseller background. The port and power photos are near-orthographic. The three-quarter images prove top finish and the distinct side patterns. The user screenshot proves row identity and the requested installed rear. `source/third-party/opticaltransceiver-ce6857-front.jpg` is rejected because its visible RJ45 layout contradicts the exact PID despite the seller title. The MF-Telecom and Made-in-China images merely corroborate the 48+6 service face and do not outrank Huawei's originals.

## Canonical orientation landmarks

- Front: `HUAWEI CE6857-48S6CQ-EI` below the left port banks; 6 QSFP28 cages at the right.
- Rear: management/USB cluster at the far left, then four blue fans, then two AC PSUs at the right.
- Left: no right-side regulatory/equipotential duplication; U bracket only at the power side.
- Right: regulatory label/equipotential features remain on the verified side; no mirroring.
- Top: Huawei white mark on the port-side black fascia and a single red stripe.
- Bottom: exact official CAD stamping, never a copy of the top.
