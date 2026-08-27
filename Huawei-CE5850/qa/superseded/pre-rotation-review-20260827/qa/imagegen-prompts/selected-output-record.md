# Selected face-generation record

No face was regenerated during the final WebGL continuation. The six approved PNGs and their source locks were preserved byte-for-byte.

Provenance note: this file was added after an authorized context-migration handoff. It normalizes the binding inputs, production modes, and selected-output constraints from `source/face-source-lock.csv` and `source/feature-inventory.csv`; it is not represented as a byte-for-byte transcript of the earlier tool-call text.

## Common generation contract used for selected outputs

- Method: built-in image generation, one dedicated face call per selected output.
- Asset type: exact orthographic transparent rack-device face for Huawei `02359104 / CE5850-EI-B00 / CE5850-48T4S2Q-EI`.
- Style: the same real product-photography character, metal/plastic texture, color balance, contrast, highlight softness, edge character, and recess shadows as the primary binding real photograph; no CGI cleanup, relighting, beautification, smoothing, vector/toon treatment, or generic redesign.
- Composition: one complete face, perfectly straight, no adjacent face, floor, cast shadow, cable, rail, watermark, seller label, or detached fragment.
- Alpha: transparent external canvas; every visible device pixel opaque; only verified real through-holes may be transparent.
- Identity: preserve normal Huawei/model text, installed configuration, exact component counts/order, asymmetric side landmarks, physical ratio, and material character; no mirroring, pseudo-text, invented ports, LEDs, seams, feet, labels, or repeated patterns.

## Per-face records

### Front / port side

- Mode: `SOURCE_LOCKED_GENERATION`
- Primary binding real photograph: `source/originals/huawei-infofinder-ce5850-48t4s2q-ei-rear.png`
- Supporting exact photographs: `rear_top.png`, `rear_left.png`, `rear_right.png`, and the user table
- Locked prompt facts: Huawei/model column at left; four 2x6 RJ45 blocks (48 total); 4 SFP+ in 2x2; 2 QSFP+ vertically; EI has no HI breakout-LED row; silver face, blue numbering strips, yellow uplink strips
- Selected output: `views/front.png`

### Rear / power side

- Mode: `SOURCE_LOCKED_GENERATION`
- Primary binding real photograph: `source/originals/huawei-infofinder-ce5850-48t4s2q-ei-front.png`
- Supporting exact photographs: `front_top.png`, official EI appearance capture, and the user table
- Locked prompt facts: PAC-150WA / FAN-40EA-F / Console+ETH+USB management / FAN-40EA-F / PAC-150WA; black removable modules, real honeycomb fields and chrome handles
- Selected output: `views/rear.png`

### Left

- Mode: `MULTI_REFERENCE_RECONSTRUCTION`
- Primary binding angle: `source/originals/huawei-infofinder-ce5850-48t4s2q-ei-rear_left.png`
- Supporting exact sources: `rear_top.png` and official side diagram/appearance capture
- Locked prompt facts: dark gray sheet metal, three port-side and four power-side attachment landmarks, warning label and fasteners; not mirrored from right
- Rejected grounding-drift attempt retained as `qa/imagegen-raw/left-rejected-grounding.png`
- Selected output: `views/left.png`

### Right

- Mode: `MULTI_REFERENCE_RECONSTRUCTION`
- Primary binding angle: `source/originals/huawei-infofinder-ce5850-48t4s2q-ei-rear_right.png`
- Supporting exact sources: `rear_top.png` and official side diagram/appearance capture
- Locked prompt facts: right-only grounding symbol/screw, distinct fastener and attachment-hole layout; not mirrored from left
- Selected output: `views/right.png`

### Top

- Mode: `MULTI_REFERENCE_RECONSTRUCTION`
- Primary binding angle: `source/originals/huawei-infofinder-ce5850-48t4s2q-ei-rear_top.png`
- Supporting exact sources: `front_top.png`, `rear_left.png`, and `rear_right.png`
- Locked prompt facts: plain medium-gray cover, perimeter/cover seam, continuous port-side perforated band; no logo, label, or invented structure
- Selected output: `views/top.png`

### Bottom

- Mode: `GENERIC_BOTTOM_FALLBACK`
- Material references: exact `rear_left.png`, `rear_right.png`, and `front_top.png`
- Locked prompt facts: conservative blank 442:420 dark sheet-metal underside; no copied top vent, branding, labels, feet, rails, holes, fasteners, seams, ports, or unsupported protrusions
- Selected output: `views/bottom.png`
