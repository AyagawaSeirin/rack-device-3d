# Dell C6320 / 2.5-inch exact exterior model

Status: **PASS_WITH_BOTTOM_FALLBACK**

This directory delivers the complete Dell PowerEdge C6300 enclosure populated with four standard C6320 nodes, 24 × 2.5-inch carriers, and two matching 1400 W AC shared PSUs. It is not a standalone node, bare enclosure, C6320p, or mixed-power configuration.

Primary artifacts:

- `models/Dell-PowerEdge-C6300-4xC6320-24SFF-standard.glb`
- `models/Dell-PowerEdge-C6300-4xC6320-24SFF-web.glb`
- `views/front.png`, `rear.png`, `left.png`, `right.png`, `top.png`, `bottom.png`
- `source/identity-manifest.md`, `evidence.md`, `face-source-lock.csv`, `feature-inventory.csv`
- `qa/final-report.md`, `delivery-validation.json`, and `webgl-loads/load-events.json`

The only fallback is the explicitly disclosed conservative bottom face. No commit or push was made.

Audit note: the web GLB is `PASS` with one benign warning because its dedicated `TRUE_DELL_LOGO_Image` is `512 × 512 px`, below the 1024px recommendation. It remains clear at the target website distance; the standard GLB retains a 1024px logo. This does not affect identity, geometry, or the 40 successful real loads.
