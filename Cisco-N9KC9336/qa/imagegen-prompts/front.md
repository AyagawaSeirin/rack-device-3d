# Front face generation record

Production mode: `SOURCE_LOCKED_GENERATION`

Method: built-in `image_gen`, two dedicated front-only calls; the first was rejected for incorrect port-number lettering and is preserved at `qa/rejected/imagegen/front-v1-wrong-port-labels.png`. The selected second call used the same source lock, followed by flat-`#00FF00` conservative border-connected removal. Exact photographed source pixels then restored the Cisco/Nexus/model control strip and numbering band without inventing text.

Input roles:

1. `source/third-party/serverlama-front.jpg` — PRIMARY BINDING REAL FACE PHOTOGRAPH; exact readable `N9K-C9336C-FX2`; binding identity, layout, material, color, surface texture, photographic character and style.
2. `source/third-party/etb-front.jpg` — BINDING exact-model front-left/top geometry and material reference.
3. `source/pdf-pages/fx2-hig/page-9.png` — OFFICIAL TECHNICAL DIAGRAM for 36-port arrangement, controls and side holes.

Final prompt:

```text
Use case: product-mockup
Asset type: exact Cisco rack-switch front orthographic texture for GLB
Production mode: SOURCE_LOCKED_GENERATION. Generation is required; changing the source photographic style is forbidden.
Input images: Image 1 is the PRIMARY BINDING REAL FACE PHOTOGRAPH and highest authority for identity, layout, materials, silver finish, real surface grain, color balance, highlight softness, recess shadows and photographic character. Image 2 is a binding exact-model three-quarter geometry/material reference. Image 3 is Cisco's official technical diagram for factual count and layout only.
Primary request: generate one new perfectly straight front orthographic view of the exact Cisco N9K-C9336C-FX2 chassis, with no rack ears installed. Rear configuration is 2x NXA-PAC-1100W-PI2 and 3x NXA-FAN-65CFM-PI, but no rear parts may appear.
Verified inventory: far-left Cisco logo and printed Cisco Nexus N9K-C9336C-FX2 marking; three chassis LEDs BCN/STS/ENV; four vertically arranged lane-selector LEDs numbered 1-4; one round LS lane-selection button; exactly 36 empty QSFP28 ports arranged as exactly 18 independent vertical two-port cages, odd port above following even port from 1/2 through 35/36; continuous narrow lower perforation strip; silver metal face; no rack ears.
Scene/backdrop: one perfectly flat uniform solid #00FF00 chroma-key background, no floor, no cast/contact shadow, no gradient, no texture, no reflections. Do not use #00FF00 anywhere in the device.
Style/medium: same real reseller product-photography style and imperfect real material character as Image 1; preserve metal grain, small wear, real cage depth and recess shadows. Not CGI, game art, illustration, vector, toon, flat shading, cleanup or beautification.
Composition/framing: one complete front face only, perfectly straight-on with no top or side visible, centered with crisp silhouette, physical ratio 439:44, long edge at least 2048 px.
Constraints: preserve exact counts/order/proportions and readable Cisco/Nexus/model branding in the real left position and orientation; all black ports and vents remain opaque; no cables, rails, brackets, watermark, reseller label, callouts, dimensions, detached fragments, pseudo-text, invented LEDs/ports/seams, repetition, mirroring, artificial symmetry, relighting, smoothing, denoising or color restyling.
```

Selected output: `views/front.png`

Selection note: the selected face remains an independently generated front. Only the small branding/numbering regions were corrected with pixels from the binding exact-model photograph; no other model, mirrored face, synthetic label or freehand text was used.
