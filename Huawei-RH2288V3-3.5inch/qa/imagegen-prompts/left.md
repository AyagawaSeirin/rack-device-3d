# Left imagegen record

Production mode: `MULTI_REFERENCE_RECONSTRUCTION`

Input roles:

1. `source/originals/huawei-official-rh2288-v3-02.jpg`: PRIMARY OFFICIAL EXACT 12-LFF LEFT-SHELL GEOMETRY/MATERIAL REFERENCE.
2. `source/originals/huawei-official-rh2288-v3-01.jpg`: OFFICIAL OPPOSITE-ANGLE ORIENTATION/CROSS-CHECK.
3. `source/third-party/ruten/content-3`: BINDING EXACT REAL 12-LFF METAL/TOP/FRONT STYLE.
4. `source/third-party/ruten/content-22`: BINDING EXACT REAL REAR/TOP/SIDE-EDGE STYLE.
5. `source/third-party/ruten/content-23`: SUPPORTING REAL REAR-SIDE EDGE/PSU RELIEF.

Final prompt:

```text
Use case: product-mockup
Asset type: exact rack-device PHYSICAL-LEFT face texture for GLB
Production mode: MULTI_REFERENCE_RECONSTRUCTION; no direct straight side photo exists; all inputs were inspected at original detail and are exact RH2288 V3 12-LFF sources.
Input images: Image 1 PRIMARY OFFICIAL EXACT LEFT-SHELL GEOMETRY/MATERIAL; Image 2 OFFICIAL OPPOSITE-ANGLE ORIENTATION CROSS-CHECK; Image 3 BINDING REAL EXACT-UNIT GALVANIZED TEXTURE/WEAR; Image 4 BINDING REAL REAR/TOP/SIDE EDGE; Image 5 SUPPORTING REAL REAR EDGE/PSU RELIEF.
Primary request: generate a new exact physical-left orthographic side view of Huawei FusionServer RH2288 V3 / H22M-03 12-LFF chassis.
Verified inventory: closed galvanized 748 x 86.1 mm side shell; front is at screen-right and rear at screen-left; distinct stamped rail lip, exact sparse holes/bosses/fasteners and local vent pattern from the binding sources; front ear projects only at the front plane; rear PSU/cord-loop relief appears only at the rear edge; do not add a rear ear.
Scene/backdrop: perfectly flat solid #ff00ff chroma-key background for local removal; no shadow, gradient, floor, reflection or lighting variation; do not use #ff00ff on the product.
Style/medium: same real galvanized-sheet photographic character as Images 3-5—grain, mild wear, soft neutral highlights and stamped-edge shadows; not CGI or a vector illustration.
Composition/framing: one complete side only, perfectly straight orthographic, no top/front/rear face visible, no perspective, no crop; physical ratio 748:86.1; front at screen-right; generous flat-key padding.
Constraints: keep this physical side distinct from the right; no text mirroring, no copied right-side vent pattern, no unsupported rail, foot, label, vent, screw or hole; product pixels opaque after key removal except verified true openings.
Avoid: generic side panel, left-right mirror, SFF 708 mm shortening, QG mixed-gallery geometry, invented details, CGI cleanup, smoothing, denoising, artificial symmetry, vector/toon/flat shading.
```
