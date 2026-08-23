# Bottom imagegen record

Production mode: `GENERIC_BOTTOM_FALLBACK`

Input roles:

1. `source/third-party/generic-bottom-reference-dell-r610.jpg`: INSPECTED GENERIC REAL UNDERSIDE MATERIAL REFERENCE ONLY — transfer no features.
2. `source/originals/huawei-official-rh2288-v3-01.jpg`: VERIFIED EXACT SIDE/TOP GALVANIZED MATERIAL AND EDGE REFERENCE.
3. `source/originals/huawei-official-rh2288-v3-02.jpg`: VERIFIED EXACT OPPOSITE-SIDE/TOP MATERIAL AND EDGE REFERENCE.
4. `source/third-party/ruten/content-3`: VERIFIED EXACT REAL RH2288 V3 METAL GRAIN/WEAR REFERENCE.

Final prompt:

```text
Use case: product-mockup
Asset type: controlled generic-bottom fallback texture for exact rack-device GLB pipeline
Production mode: GENERIC_BOTTOM_FALLBACK; exact RH2288 V3 underside imagery was not found after documented official, PDF, dynamic-browser, reseller, marketplace, auction, used-equipment, video and English/Chinese searches.
Input images: Image 1 INSPECTED GENERIC REAL UNDERSIDE MATERIAL ONLY—do not transfer any Dell feature; Images 2-3 VERIFIED EXACT RH2288 V3 SIDE/TOP GALVANIZED MATERIAL AND EDGE TREATMENT; Image 4 VERIFIED EXACT REAL RH2288 V3 METAL GRAIN/WEAR.
Primary request: generate one conservative non-identifying perfectly orthographic bottom face for Huawei FusionServer RH2288 V3 / H22M-03 at physical ratio 447:748.
Verified inventory: one closed plain opaque galvanized sheet-metal underside, front edge at screen-bottom, preserving only simple edge lips already proven by the exact side references.
Scene/backdrop: perfectly flat solid #ff00ff chroma-key background for local removal; no shadow, gradient, floor, reflection or lighting variation; do not use #ff00ff on the product.
Style/medium: real neutral galvanized sheet matching the exact Huawei material—fine grain, mild natural variation, soft neutral highlights; not CGI or illustration.
Composition/framing: one complete bottom face, perfectly overhead/orthographic, no side/front/rear face visible, no perspective, no crop; physical ratio 447:748; generous flat-key padding.
Constraints: all product pixels opaque after key removal; do not copy or mirror the top; transfer none of Image 1's labels, vents, holes, feet, ports or PSU shapes.
Avoid: logo, model label, service label, vent, hole, foot, rail, seam, screw, fastener, protrusion, port, branding, pseudo-text, invented detail, top duplication, CGI cleanup, vector/toon/flat shading.
```
