# Front imagegen record

Production mode: `MULTI_REFERENCE_RECONSTRUCTION`

Input roles:

1. `source/third-party/router-switch-12lff-front.jpg`: PRIMARY BINDING REAL PRODUCT PHOTOGRAPH — exact 12-LFF front structure and real photographic material/style.
2. `source/originals/huawei-official-rh2288-v3-01.jpg`: OFFICIAL EXACT 12-LFF GEOMETRY/BRANDING REFERENCE.
3. `source/third-party/ruten/content-4`: BINDING EXACT USED-UNIT FRONT/TOP PHOTOGRAPH — wear, metal/plastic texture and carrier count.
4. `source/third-party/ruten/content-6`: BINDING REAL LEFT-EAR/USB/HUAWEI/CARRIER DETAIL.
5. `source/third-party/ruten/content-11`: BINDING REAL RIGHT-EAR/RH2288 V3/CONTROL DETAIL.

Final prompt:

```text
Use case: product-mockup
Asset type: exact rack-device FRONT face texture for GLB
Production mode: MULTI_REFERENCE_RECONSTRUCTION; every input was inspected at original detail; no AI derivative is an input.
Input images: Image 1 PRIMARY BINDING REAL PRODUCT PHOTOGRAPH—identity, 12-LFF layout, metal/plastic material and photographic style; Image 2 OFFICIAL EXACT 12-LFF GEOMETRY/BRANDING; Image 3 BINDING REAL USED-UNIT TEXTURE/WEAR/COUNT; Image 4 BINDING REAL LEFT-EAR DETAIL; Image 5 BINDING REAL RIGHT-EAR DETAIL.
Primary request: generate a new exact perfectly straight orthographic front view of Huawei FusionServer RH2288 V3 / H22M-03, 2U, twelve common 3.5-inch LFF carrier faces in exactly 3 rows x 4 columns, non-NVMe, no security bezel.
Verified inventory: far-left separate black control/mounting ear with two vertical USB 2.0 ports, four small network-link indicators, white Huawei flower/logo and lime bottom accent; center twelve black honeycomb carrier faces with lime vertical release accents and exact seams/handles; far-right separate black control/mounting ear with three-digit fault display, controls, pull-label recess, readable RH2288 V3 badge and lime bottom accent. Use carrier faces without capacity-specific stickers. Preserve factory HUAWEI and RH2288 V3 text normally oriented.
Scene/backdrop: perfectly flat solid #ff00ff chroma-key background for local removal; no shadow, gradient, floor, reflection or lighting variation; do not use #ff00ff on the product.
Style/medium: source-locked real product photography matching Image 1 and Image 3—real black molded plastic, honeycomb depth, galvanized edges, surface grain, mild wear, neutral color balance, soft highlights and dark recess shadows; not a cleaner CGI render.
Composition/framing: one complete face only, centered, perfectly straight-on, no top/side visible, no perspective, no crop; physical ratio 482.6:86.1; generous flat-key padding.
Constraints: exact 12 count and 3x4 order; all product pixels opaque after key removal; only verified front-ear through-holes may open; no seller overlay, drive-capacity label, cable, rail, watermark, pseudo-text, invented display/LED/port, mirroring, repetition, redesign or style change.
Avoid: family substitution, RH2288H V3, 8-SFF/10-LFF/25-SFF layouts, CGI cleanup, beautification, relighting, smoothing, denoising, artificial symmetry, vector/toon/flat shading and changed component counts.
```
