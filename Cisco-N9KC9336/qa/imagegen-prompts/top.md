# Top face generation record

Production mode: `MULTI_REFERENCE_RECONSTRUCTION`

Method: built-in `image_gen`, one dedicated call; flat `#00FF00` chroma background followed by conservative border-connected removal.

Input roles:

1. `source/third-party/serverlama-angled-top.jpg` — PRIMARY BINDING exact-model REAL PHOTOGRAPH; highest authority for top layout, sheet-metal material, label placement and photographic style.
2. `source/third-party/itinstock-angle.jpg` — BINDING exact-model elevated front photo covering the vent band and label cluster.
3. `source/third-party/ebay-lonestar-1.jpg` — BINDING exact-model front-left-top photo covering the opposite top edge.
4. `source/third-party/etb-front.jpg` — SUPPORTING exact-model front-left-top material and seam reference.

Final prompt:

```text
Use case: product-mockup
Asset type: exact Cisco rack-switch top orthographic texture for GLB
Production mode: MULTI_REFERENCE_RECONSTRUCTION from multiple inspected exact-model real photographs.
Input images: Image 1 is the PRIMARY BINDING real N9K-C9336C-FX2 top photograph and highest authority for cover layout, silver material, surface grain, real wear, color balance and photographic style. Images 2-4 independently prove both top edges, the vent band, seams and label placement.
Primary request: generate one new perfectly straight top-down orthographic face of exact Cisco N9K-C9336C-FX2 chassis.
Verified inventory: rectangular silver sheet-metal cover at body ratio 439:571.5; one full-width narrow perforated ventilation band close to the front/port-side edge; real shallow cover seams/embossed lines and flush fasteners exactly as jointly shown; grouped factory labels on the left half near the port-side region consisting of a white regulatory block, yellow caution block and small blue-white inventory block. Preserve label shapes and genuine factory character but do not fabricate serial numbers, QR codes or unreadable compliance prose.
Scene/backdrop: perfectly flat uniform #00FF00 chroma-key background with no floor, shadow, gradient, texture or reflection; do not use #00FF00 in the device.
Style/medium: same real neutral reseller product photography, silver sheet-metal grain, small scuffs, imperfect real label surfaces and soft highlights as Image 1; no CGI cleanup, game art, illustration, vector, toon, relighting, beautification or smoothing.
Composition/framing: one complete top face only, perfectly straight top-down, front/port side at image bottom and rear/power side at image top, no side/front/rear adjacent face visible, long edge at least 1536 px.
Constraints: exact vent location and cover proportions; no Cisco logo invented on top; no rack rails, cables, seller stickers, watermark, pseudo-text, invented vents/holes/feet/ports, mirrored layout, artificial symmetry, denoising or color restyling.
```

Selected output: `views/top.png`

Post-generation source correction: any generated label-like marks were replaced only with rectified pixels from the binding exact-model top photograph. The resulting top remains the independently generated top face, with exact-model photographed label character and no fabricated serial or QR content.
