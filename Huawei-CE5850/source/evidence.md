# Evidence and source-lineage record

Access and review date: 2026-08-23

## Locked delivery identity

- Manufacturer: Huawei Technologies Co., Ltd.
- Part number / bundle / chassis PID: `02359104` / `CE5850-EI-B00` / `CE5850-48T4S2Q-EI`
- Delivery subject: complete fixed 1U appliance
- Port side: 48 x GE RJ45, 4 x 10GE SFP+, 2 x 40GE QSFP+
- Power side: 2 x PAC-150WA AC and 2 x FAN-40EA-F, all installed
- Airflow: power-side intake, port-side exhaust
- Canonical orientation: the user-facing port side is `front` / `+Z`. Huawei's image package calls this face `rear`.

The exact identity was locked from the user table, public Huawei Info-Finder package for part number `02359104`, the exact EI product photographs, and Huawei ordering data. The exact EI power-side photograph reads `CE5850-48T4S2Q-EI`, `PAC-150WA`, and `FAN-40EA-F`; it is not the nearby HI chassis.

## Primary exact-model visual evidence

| Evidence | Local preserved file | What it proves |
|---|---|---|
| Huawei Info-Finder `rear.png` | `source/originals/huawei-infofinder-ce5850-48t4s2q-ei-rear.png` | Exact EI port face, Huawei/model marking, 48/4/2 port inventory and order |
| Huawei Info-Finder `front.png` | `source/originals/huawei-infofinder-ce5850-48t4s2q-ei-front.png` | Exact dual PAC-150WA / dual FAN-40EA-F power face and management block |
| Huawei Info-Finder `rear_left.png` | `source/originals/huawei-infofinder-ce5850-48t4s2q-ei-rear_left.png` | Port face, top cover, left-side silhouette and landmarks |
| Huawei Info-Finder `rear_right.png` | `source/originals/huawei-infofinder-ce5850-48t4s2q-ei-rear_right.png` | Port face, top cover, right-side grounding/fastener landmarks |
| Huawei Info-Finder `rear_top.png` | `source/originals/huawei-infofinder-ce5850-48t4s2q-ei-rear_top.png` | Top cover and continuous port-side perforated band |
| Huawei Info-Finder `front_top.png` | `source/originals/huawei-infofinder-ce5850-48t4s2q-ei-front_top.png` | Exact power face plus top-cover material |
| Huawei support appearance/airflow captures | `source/originals/huawei-official-ce5850-48t4s2q-ei-appearance.png`; `source/originals/huawei-official-ce5850-ei-airflow-port-exhaust.png` | EI versus HI identity and port-side-exhaust configuration |

Public preview endpoint used for the exact part package:

`https://info.support.huawei.com/info-finder/imagelib/getPreviewImages?domain=0&lang=en&partNumber=02359104`

Every selected raster above was inspected at original detail for PID, face/orientation, installed modules, port counts, crop, and seller alteration. Exact-image SHA-256 values and face roles are recorded in `source/face-source-lock.csv`.

## Documentation and dimensions

- Huawei support dimension page: `https://support.huawei.com/enterprise/zh/doc/EDOC1000019242/53f4bcaa`
- Preserved official datasheet: `source/originals/huawei-cloudengine-5800-datasheet.pdf`
- Extracted text: `source/originals/huawei-cloudengine-5800-datasheet.txt`
- Rendered inspected excerpts: `source/pdf-pages/huawei-cloudengine-5800-datasheet-p01.png` through `p05.png`

The official source gives `442.0 mm x 420.0 mm x 43.6 mm` for the chassis. The separate installed rack ears extend the overall width to the 19-inch envelope of `482.6 mm`; they do not stretch the 442 mm body textures. Final audited GLB bounds are exactly `482.6 x 43.6 x 420.0 mm`.

The same official datasheet identifies `CE5850-EI-B00` as the CE5850-48T4S2Q-EI switch with two 150 W AC power modules, two fan boxes, and port-side exhaust. It lists `FAN-40EA-F` as panel-side intake and `PAC-150WA` as the 150 W AC module.

## Third-party cross-checks

Exact-PID reseller datasheets and photos are preserved under `source/third-party/`. They were used only to cross-check the official identity/dimensions and to search for otherwise hidden faces. The unrelated-looking marketplace image `made-in-china-ce5850-48t4s2q-ei.jpg` was not used as binding evidence.

## Bottom search and controlled fallback

Official product pages, the public Info-Finder six-image package, official datasheet/manual material, exact-PID reseller datasheets/photos, marketplace/used-equipment image leads, and exact-model searches for underside/bottom/service/teardown views were reviewed. No usable exact-model underside photograph was found. The final `views/bottom.png` therefore remains the documented `GENERIC_BOTTOM_FALLBACK`:

- conservative blank 442:420 dark sheet metal;
- material and edge character constrained by exact left/right/top photographs;
- no copied top vent, branding, labels, feet, rails, holes, fasteners, ports, or unsupported protrusions;
- no change to any verified side silhouette.

Final model status is therefore `PASS_WITH_BOTTOM_FALLBACK`, not ordinary `PASS`.

## Public official 3D search

Huawei Info-Finder metadata for the exact EI photo package exposed `threeDUrl: null` and `customThreedUrl: null`. Official-domain searches for the exact EI/HI PIDs with 3D, GLB, glTF, CAD, STEP, AR, Visio, and VSS produced no public downloadable exact model. The Visio package is a stencil/diagram asset, not 3D. Details are retained in `source/optional-3d/README.md`.

## 2026-08-27 current reverse review

- Reopened Huawei Info-Finder Hardware Center PID `22460464`; it still resolves the exact `CE5850-48T4S2Q-EI` product rather than the nearby HI chassis.
- Rechecked the exact `02359104` photo package, current official product-3D surfaces, and public 3D/CAD/GLB/glTF searches. The exact package still exposes no public downloadable official 3D binary; the official six-photo package remains the primary visual authority.
- Re-inspection of the retained original-detail port and power faces reconfirmed 48 GE RJ45 + 4 SFP+ + 2 QSFP+, no HI breakout-lamp row, and the installed `PAC-150WA / FAN-40EA-F / management / FAN-40EA-F / PAC-150WA` power-side order.
- The final GLB preserves the user-facing port side as +Z/front, while retaining Huawei's opposite front/rear naming in the evidence notes. No current source contradicted the 442 × 43.6 × 420 mm appliance or the separate front-ear geometry.
