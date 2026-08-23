# Evidence and source log

Access date: 2026-08-23 (Asia/Singapore)

## Identity lock

The thirteenth readable equipment row in `source/originals/user-device-list.png` is Huawei `CE6851`. Its port-side thumbnail is a browser-resized copy of Huawei `rear.png` (best normalized cross-correlation 0.922144), and its power-side thumbnail is a resized copy of Huawei `front.png` (0.889632). Match diagnostics are retained in `qa/reference/front-match-scores.txt` and `qa/reference/match-scores.txt`.

The matched Huawei power-side source visibly reads `PAC-600WA-B` on both AC power modules and `FAN-40EA-B` on both fan modules. Huawei's hardware description defines the B modules as back-to-front/power-panel-side exhaust. The complete assembly therefore takes air in at the port side. Huawei ordering page 100 uniquely maps the complete two-AC/two-fan/port-side-intake configuration to part number `02350JAS`, part model `CE6851-HI-B-B0A`.

## Official sources

- Huawei Info-Finder image library, exact part pages:
  - https://info.support.huawei.com/info-finder/imagelib/getPreviewImages?domain=0&lang=zh&partNumber=02350JAS
  - https://info.support.huawei.com/info-finder/imagelib/getPreviewImages?domain=0&lang=zh&partNumber=02350JAR
  - Both pages point to the shared exact-model image package. The F page also serves the B-module photographs, so page title alone was not used for airflow; readable module labels in the screenshot-matched photograph and the ordering table were used.
- Exact public image endpoints, unchanged under `source/official/`: `front.png`, `front_top.png`, `rear.png`, `rear_left.png`, `rear_right.png`, `rear_top.png`.
- Huawei CloudEngine 7800&6800&5800 Series Switches Hardware Description, Issue 16, 2015-08-26, local file `source/official/huawei-hardware-description-issue16.pdf`:
  - print p36 / PDF p46: appearance and independent left/right side diagrams;
  - print p37 / PDF p47: exact slot/port/mounting-hole inventory;
  - print p54 / PDF p64: front-to-back and back-to-front airflow diagrams;
  - print p82 / PDF p92: 442.0 x 420.0 x 43.6 mm physical dimensions;
  - print p100 / PDF p110: 02350JAS / CE6851-HI-B-B0A complete dual-AC, dual-fan, port-side-intake ordering row.
- Huawei CloudEngine 6800 Switch Datasheet, local `source/official/huawei-cloudengine-6800-datasheet.pdf`, pages 8-9: independent dimensions and B/F module direction definitions.
- Current online hardware description:
  - https://support.huawei.com/enterprise/zh/doc/EDOC1000019242/a1d7e273

## Exact-B third-party photography

REVO gallery: https://revodistribution.com/parts/huawei-ce6851-48s6q-hi

The seven photographs are a single physical CE6851-48S6Q-HI unit. Power-side image 4 visibly carries B-suffix PAC/FAN modules; label close-up image 7 reads CE6851-48S6Q-HI. The set supplies direct top, bottom, right, left, port, power, and label views. Seller background and watermark are outside the product; the unit has wear and attached rack brackets. Files are preserved unchanged as `source/third-party/revo-ce6851-1.webp` through `-7.webp`.

## Rejected variant sources

`piospartslap-ce6851.jpg` and `linknewnet-ce6851-rear.jpg` show the same chassis with F-suffix airflow modules. They are retained only to demonstrate why family-name matching is insufficient and are excluded from all target face locks.

## Six-face decision

All six faces have direct exact-device real photographs and use `SOURCE_LOCKED_GENERATION`. Bottom fallback is not used. Left and right are not mirrored: the right side has the ground stud/yellow earth mark; the left side does not.

## Dimension interpretation

Huawei publishes 442.0 mm body width, 420.0 mm device depth, and 43.6 mm height. The documentation does not explicitly state whether removable rack brackets are included; official body photographs have no brackets. The user explicitly required rack-ear geometry, and the exact-B REVO unit proves the port-side bracket shape and installed position. Brackets are therefore separate geometry at a 482.6 mm standard rack span and do not redefine the quoted Huawei body width.

