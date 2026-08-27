# Top imagegen record

Production mode: `MULTI_REFERENCE_RECONSTRUCTION`

Input roles:

1. `source/third-party/ruten/content-3`: PRIMARY BINDING EXACT REAL TOP/FRONT PHOTOGRAPH — geometry, material, factory labels and photographic style.
2. `source/originals/huawei-official-rh2288-v3-01.jpg`: OFFICIAL EXACT TOP/FRONT/SIDE GEOMETRY.
3. `source/originals/huawei-official-rh2288-v3-02.jpg`: OFFICIAL EXACT TOP/REAR/OPPOSITE-SIDE GEOMETRY.
4. `source/third-party/ruten/content-4`: BINDING REAL COVER GRAIN/SEAM/LATCH SUPPORT.
5. `source/third-party/ruten/content-22`: BINDING REAL REAR-TOP/VENT/SAFETY-LABEL SUPPORT.

Final prompt:

```text
Use case: product-mockup
Asset type: exact rack-device TOP face texture for GLB
Production mode: MULTI_REFERENCE_RECONSTRUCTION; all inputs were inspected at original detail; no AI derivative is an input.
Input images: Image 1 PRIMARY BINDING EXACT REAL TOP PHOTO—geometry, galvanized material, factory labels, mild wear and photographic style; Images 2-3 OFFICIAL EXACT TOP/EDGE GEOMETRY; Image 4 BINDING REAL COVER GRAIN/SEAM/LATCH; Image 5 BINDING REAL REAR-TOP/VENT/SAFETY-LABEL SUPPORT.
Primary request: generate a new exact perfectly orthographic top view of Huawei FusionServer RH2288 V3 / H22M-03 12-LFF chassis.
Verified inventory: 447 x 748 mm galvanized cover; front edge at screen-bottom; front cover section with genuine H22M-03/Huawei factory identity and qualification label areas; transverse square-vent row; straight cover seam; one centered service latch with lime accent; exact fastener/boss pattern; rear safety-label group at the verified side. Remove only the large yellow/orange seller overlay. Preserve real factory label shapes and readable H22M-03/Huawei identity without inventing serials or pseudo-text.
Scene/backdrop: perfectly flat solid #ff00ff chroma-key background for local removal; no shadow, gradient, floor, reflection or lighting variation; do not use #ff00ff on the product.
Style/medium: Image 1 source-locked real galvanized product photography—real grain, slight scratches/wear, neutral color, soft highlights and recess shadows; do not clean into CGI.
Composition/framing: one complete top face, perfectly overhead orthographic, no side/front/rear face visible, no perspective, no crop; physical ratio 447:748; front at screen-bottom; generous flat-key padding.
Constraints: no mirrored text; no copied bottom; no seller text/phone/watermark; product pixels fully opaque after key removal except verified vent holes; no invented vent, latch, label, seam, handle, rail, foot or fastener.
Avoid: pseudo-text, beautification, CGI cleanup, relighting, smoothing, denoising, vector/toon/flat shading, artificial symmetry and repeated AI texture.
```
