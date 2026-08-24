# Right face generation record

Production mode: `MULTI_REFERENCE_RECONSTRUCTION`

Method: built-in `image_gen`, one dedicated call; flat `#00FF00` chroma background followed by conservative border-connected removal.

Input roles:

1. `source/third-party/serverlama-angled-side.jpg` — PRIMARY BINDING exact-model REAL PHOTOGRAPH showing physical right from the front-right-top; highest authority for right-side material/style and hole layout.
2. `source/originals/cisco-N9K-C9336C-FX2-port-side.jpg` — OFFICIAL exact-PID oblique showing physical-right screw and grounding locations.
3. `source/originals/cisco-N9K-C9336C-FX2-power-side.jpg` — OFFICIAL exact-PID rear oblique confirming the same physical-right side.
4. `source/pdf-pages/fx2-hig/page-29.png` — OFFICIAL TECHNICAL diagram for rack-bracket holes and two-hole grounding pad.

Final prompt:

```text
Use case: product-mockup
Asset type: exact Cisco rack-switch physical RIGHT-side orthographic texture for GLB
Production mode: MULTI_REFERENCE_RECONSTRUCTION from inspected exact-model real photographs and official diagrams; never mirror the left.
Input images: Image 1 is the PRIMARY BINDING real N9K-C9336C-FX2 front-right-top photograph and highest authority for right-side material, color, grain, wear and photographic style. Images 2-4 are official exact-PID geometry references and confirm right-side-only grounding holes.
Primary request: generate one new perfectly straight physical-right orthographic face of bare Cisco N9K-C9336C-FX2 chassis, no rails or brackets installed.
Verified inventory: very long low 1RU silver sheet-metal side at body ratio 571.5:44; exactly six verified rack-bracket mounting locations in the independent right pattern; exactly two paired threaded grounding-lug holes on their outlined pad on the physical right only; front/top vent edge as a thin real boundary; no yellow left-side caution label; no ports, feet, handles, branding or rear modules projected onto the side.
Scene/backdrop: perfectly flat uniform #00FF00 chroma-key background, no floor, shadow, gradient, texture or reflection; do not use #00FF00 in the device.
Style/medium: same real photographic silver sheet metal, subtle grain, small wear and highlight softness as Image 1; not CGI, illustration, vector, toon, generic clean panel or game asset.
Composition/framing: one complete physical-right side only, perfectly straight orthographic, front edge on image right and rear edge on image left when viewed from the physical right, no adjacent face visible, long edge at least 1536 px.
Constraints: preserve the independent right pattern and two grounding holes; never mirror left; no rails, brackets, cables, watermark, seller mark, pseudo-text, invented holes/seams/vents/labels, artificial symmetry, smoothing, relighting or restyling.
```

Selected output: `views/right.png`

Post-generation evidence correction: the prompt's phrase “six verified rack-bracket mounting locations” was too compressed. The final source inventory resolves two independent six-slot rack-bracket zones, 12 slots total. `views/right.png` and the GLB geometry implement 12 plus the right-only two-hole grounding pad. The face was generated in its own right-side call and was never mirrored from the left.
