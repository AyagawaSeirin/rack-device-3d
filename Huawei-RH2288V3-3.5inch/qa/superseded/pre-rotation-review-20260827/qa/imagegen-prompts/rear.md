# Rear imagegen record

Production mode: `SOURCE_LOCKED_GENERATION`

Input roles:

1. `source/third-party/zol-rh2288-v3-rear.jpg`: PRIMARY BINDING REAL STRAIGHT REAR PHOTOGRAPH — identity, installed configuration, geometry, material and style.
2. `source/third-party/ruten/content-22`: BINDING EXACT USED-UNIT REAR THREE-QUARTER PHOTOGRAPH.
3. `source/third-party/ruten/content-15`: BINDING EXACT USED-UNIT NEAR-STRAIGHT REAR PHOTOGRAPH.
4. `source/third-party/ruten/content-23`: BINDING REAL PSU/CONSOLE/CORD-LOOP DETAIL.
5. `source/originals/huawei-official-rh2288-v3-02.jpg`: OFFICIAL SHELL/MATERIAL REFERENCE ONLY — its rear-disk module and four-port NIC are explicitly forbidden.

Final prompt:

```text
Use case: product-mockup
Asset type: exact rack-device REAR face texture for GLB
Production mode: SOURCE_LOCKED_GENERATION; Image 1 is the highest-authority binding identity/configuration/material/style reference; every input was inspected at original detail.
Input images: Image 1 PRIMARY BINDING REAL STRAIGHT REAR PHOTO; Image 2 BINDING EXACT USED-UNIT REAR GEOMETRY/MATERIAL; Image 3 BINDING EXACT USED-UNIT REAR ORDER; Image 4 BINDING PSU/CONSOLE/CORD-LOOP DETAIL; Image 5 OFFICIAL CHASSIS SHELL/MATERIAL ONLY—do not copy its rear disks or four-port NIC.
Primary request: generate a new exact perfectly straight orthographic rear view of Huawei FusionServer RH2288 V3 / H22M-03 with no rear disks, blank expansion covers, SM211 two-GE flexible NIC and two identical 460 W GOLD AC PSUs stacked vertically on the same far side.
Verified left-to-right inventory in the straight rear image: large I/O module 2 with three horizontal blank perforated PCIe covers above one SM211 bracket containing exactly two RJ45 GE ports; two narrow onboard blank covers labeled slot 4 and slot 5; large I/O module 1 with three horizontal blank perforated covers above two blue USB 3.0 ports, dedicated Mgmt RJ45, blue VGA, teal-backed DB9 serial and UID; far-side PSU1 above PSU2, each a separate removable module with IEC inlet, round fan recess, lime ejector and black cord-retainer loop. No rear mounting ears, no rear disks, no installed PCIe cards and no cables.
Scene/backdrop: perfectly flat solid #ff00ff chroma-key background for local removal; no shadow, gradient, floor, reflection or lighting variation; do not use #ff00ff on the product.
Style/medium: preserve Image 1's real product-photography character—galvanized steel grain, genuine stamping, dark perforation recesses, real connector colors, mild wear, neutral balance, soft highlights and port shadows; do not turn it into a cleaner CGI/product render.
Composition/framing: one complete rear face, perfectly straight-on, no top/side visible, no perspective, no crop; physical ratio 447:86.1; generous flat-key padding; text reads normally and is not mirrored.
Constraints: exactly two RJ45 flexible-NIC ports, exactly two stacked identical AC PSUs, zero rear disks, correct blank-panel order; equipment pixels fully opaque after key removal; only physically open holes may reveal background; remove only the outside ZOL watermark/seller surroundings.
Avoid: four-port NIC, rear-disk module, split/side-by-side PSUs, DC PSU, rear ears, copied official rear option, generic server layout, pseudo-text, fake LEDs/ports, repetition, mirroring, CGI cleanup, relighting, beautification, smoothing, vector/toon/flat shading.
```
