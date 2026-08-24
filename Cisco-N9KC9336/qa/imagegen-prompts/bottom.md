# Bottom face generation record

Production mode: `GENERIC_BOTTOM_FALLBACK`

Method: built-in `image_gen`, one dedicated call; flat `#00FF00` chroma background followed by conservative border-connected removal.

Input roles:

1. `source/third-party/generic-bottom-cisco-catalyst3650.jpg` — INSPECTED generic same-vendor 1U underside MATERIAL reference only; every model-specific hole, boss, label, foot, latch and vent is forbidden from transfer.
2. `source/third-party/serverlama-angled-side.jpg` — exact-model verified right-side material and bottom-edge silhouette reference.
3. `source/third-party/ebay-lonestar-1.jpg` — exact-model verified left-side material and bottom-edge silhouette reference.

Final prompt:

```text
Use case: product-mockup
Asset type: conservative rack-device bottom texture for GLB
Production mode: GENERIC_BOTTOM_FALLBACK. Exact N9K-C9336C-FX2 underside imagery was not found after documented official, PDF, Browser-assisted, reseller, shopping, marketplace, used-equipment, video, English, Chinese and Japanese searches.
Input images: Image 1 is only a generic same-vendor 1U sheet-metal underside material reference; DO NOT transfer any of its labels, holes, stamped bosses, feet, vents, latch slots, fasteners or module shapes. Images 2 and 3 are exact N9K-C9336C-FX2 side photographs and bind the silver material and outer bottom-edge silhouette.
Primary request: generate one new perfectly straight bottom-up orthographic face: a conservative non-identifying plain closed silver sheet-metal underside matching the exact chassis body ratio 439:571.5 and verified edge treatment.
Scene/backdrop: perfectly flat uniform #00FF00 chroma-key background with no floor, cast/contact shadow, gradient, texture or reflection; do not use #00FF00 in the device.
Style/medium: real neutral product photography matching the exact side-source silver sheet metal, subtle grain, small natural wear and soft highlights; not CGI, illustration, vector, toon or polished game asset.
Composition/framing: one complete underside only, perfectly straight orthographic, front/port side at image bottom and rear/power side at image top, no adjacent face visible, long edge at least 1536 px.
Constraints: intentionally no branding, model labels, regulatory labels, vents, holes, feet, rails, seams, fasteners, stamped bosses, protrusions, ports or service markings; do not copy or mirror the top; preserve only the verified rectangular silhouette and silver material; all product pixels opaque; no watermark, pseudo-text, invented detail, relighting, beautification or smoothing.
```

Selected output: `views/bottom.png`

