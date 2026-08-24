# Left face generation record

Production mode: `MULTI_REFERENCE_RECONSTRUCTION`

Method: built-in `image_gen`, one dedicated call; flat `#00FF00` chroma background followed by conservative border-connected removal.

Input roles:

1. `source/third-party/ebay-lonestar-1.jpg` — PRIMARY BINDING exact-model REAL PHOTOGRAPH showing the physical left side from the front-left-top; highest authority for left-side hole pattern, label placement, material and photographic style.
2. `source/third-party/etb-front.jpg` — BINDING second exact-model front-left/top photo.
3. `source/third-party/serverlama-angled-top.jpg` — SUPPORTING exact-model top/material reference.
4. `source/pdf-pages/fx2-hig/page-29.png` — OFFICIAL TECHNICAL bracket-hole reference; the grounding pad shown in official figures belongs to the physical right and must not be copied.

Final prompt:

```text
Use case: product-mockup
Asset type: exact Cisco rack-switch physical LEFT-side orthographic texture for GLB
Production mode: MULTI_REFERENCE_RECONSTRUCTION from inspected exact-model real photographs; never mirror the right.
Input images: Image 1 is the PRIMARY BINDING exact N9K-C9336C-FX2 real front-left-top photograph and highest authority for physical-left layout, silver material, grain, wear, color and photographic style. Image 2 independently confirms the same physical left. Image 3 supports cover material. Image 4 constrains bracket-hole geometry but its grounding pad is right-side-only and forbidden here.
Primary request: generate one new perfectly straight physical-left orthographic face of bare Cisco N9K-C9336C-FX2 chassis, no rack rails or brackets installed.
Verified inventory: very long low 1RU silver sheet-metal side at body ratio 571.5:44; independent left front-to-rear rack-bracket screw/slot pattern with six verified mounting locations; small yellow factory caution label in the rear half as shown; front/top perforated vent edge visible only as the real thin boundary detail; no two-hole grounding-lug pad on the left; no ports, feet, handles, branding or rear modules projected onto the side.
Scene/backdrop: perfectly flat uniform #00FF00 chroma-key background with no floor, shadow, gradient, texture or reflection; do not use #00FF00 in the device.
Style/medium: same real photographic silver sheet metal, subtle grain, small wear and soft highlight character as Image 1; not CGI, illustration, vector, toon, clean game asset or artificially smooth panel.
Composition/framing: one complete physical-left side only, perfectly straight orthographic, front edge on image left and rear edge on image right, no top/front/rear adjacent face visible, long edge at least 1536 px.
Constraints: preserve the independent left-side pattern; do not mirror the right; no grounding pad; no rails, brackets, cables, watermark, seller mark, pseudo-text, invented holes/seams/vents/labels, artificial symmetry, relighting, beautification, smoothing or restyling. The yellow label may remain a small real factory caution block without fabricated serial/QR text.
```

Selected output: `views/left.png`

Post-generation evidence correction: the prompt's phrase “six verified mounting locations” was too compressed. The final source inventory resolves two independent six-slot rack-bracket zones, 12 slots total. `views/left.png` and the GLB geometry implement 12; the left remains independently generated, retains its single caution label and has no grounding pad. Unsupported pseudo-microtext inside the generated yellow block was replaced with a clean `CAUTION` block rather than preserved as invented text.
