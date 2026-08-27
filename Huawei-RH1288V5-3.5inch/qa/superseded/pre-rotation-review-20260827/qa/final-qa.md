# Final QA — Huawei FusionServer Pro 1288H V5 4LFF

## Decision

**PASS_WITH_BOTTOM_FALLBACK**

All mandatory identity, configuration, appearance, geometry, file-structure, transparency, GLB-structure, and independent-viewer gates pass. The bottom is the sole controlled fallback because no exact direct bottom evidence was found. No non-bottom face is accepted as a generic fallback.

## Frozen configuration

- Official model: Huawei FusionServer Pro 1288H V5 Server
- Huawei support product PID: 21872252
- User-list alias: RH1288V5/3.5-inch
- 1U; 436 × 43 × 748 mm 3.5-inch chassis; 482.6 mm front-ear span
- Four installed 3.5-inch LFF carrier fronts, no security bezel
- Three external rear PCIe/riser regions
- FlexIO/LOM and service-I/O family matching the exact rear specimen
- Two installed 900 W hot-swap AC PSU modules; no DC PSU geometry
- Huawei and 1288H V5 markings retained; unit serials, drive-capacity labels and reseller stickers omitted

## Source and face lock

| Face | Lock | Result |
|---|---|---|
| Front | exact 4LFF specimen, user row, CompuWay 4LFF, MyDraw/official diagram | PASS — four carriers, ears, service strip and markings retained |
| Rear | exact specimen, user row, CompuWay rear, official diagrams, MyDraw 3IO | PASS — three PCIe zones, service ports and dual AC PSUs retained |
| Top | exact closed-cover Serverflow photos plus official structure evidence | PASS — latch, two vent bands, seams and label zones retained |
| Left | independent multi-reference reconstruction | PASS — independent endpoint/rail/fastener pattern; no mirrored side asset |
| Right | independent multi-reference reconstruction | PASS — PSU-side rear endpoint and distinct pattern retained; no mirrored side asset |
| Bottom | controlled fallback | PASS_WITH_BOTTOM_FALLBACK — conservative closed base; no invented ports, labels or access panels |

The current Huawei Intelligent Servers 3D page returned no data, the linked old-version host did not resolve, and public searches found no exact downloadable 1288H V5 4LFF CAD/GLB/GLTF. A 2288H V5 3D presentation was explicitly rejected as an incompatible 2U product.

## Six PNG audit

`qa/views-audit.json`: **PASS**, zero errors.

- All six files are RGBA PNGs with transparent exterior backgrounds.
- Long edge: 2400 px content for every face.
- Physical-ratio error: 0.023% to 0.128%.
- No suspicious core transparency on front, rear, left, top or bottom.
- Right-side core alpha below 250 is 2.586%; manual review confirms it is limited to the independently generated edge/true-hole/anti-alias detail and is under the locked 3% limit.
- Final embedded GLB textures are composited to RGB and use `OPAQUE`; no BLEND/MASK material is present.

## GLB structural audit

Both reports are **PASS** with zero errors and zero warnings:

- `qa/glb-audit-standard.json`
- `qa/glb-audit-web.json`

| Property | Standard | Web |
|---|---:|---:|
| GLB bytes | 9,646,376 | 7,450,640 |
| Nodes / meshes / primitives | 424 / 424 / 424 | 328 / 328 / 328 |
| Materials | 14 | 14 |
| Embedded base-color images | 6 unique RGB PNGs | 6 unique RGB PNGs |
| Mirrored nodes | 0 | 0 |
| External buffers | 0 | 0 |
| Bounds (m) | 0.4826 × 0.0450 × 0.76775 | 0.4826 × 0.0450 × 0.76775 |

The visible bounds include shallow front/rear service relief and top/bottom fastener relief; the structural body remains locked to 436 × 43 × 748 mm. Proportion checks pass within the configured 8% tolerance.

`qa/feature-audit.json`: **PASS**. Named geometry verifies two rack ears, four carrier handles and release accents, three PCIe regions, four LOM sockets, two 900 W AC PSU bodies, two C14 inlets, two PSU fans, two top vent bands, independent left/right relief features, and six separately named appearance surfaces.

This is not a six-texture box. Carrier frames/handles, port cages, PCIe panel structure, PSU bodies/fans/C14 inlets/handles/latches, top latch/vents/seams, side relief, bottom plate and rack ears are separately visible geometry.

## Independent viewer QA

The web GLB was loaded, not mocked, in both engines:

- Three.js 0.180.0: front, rear, left, right, top, bottom, four three-quarter views
- Babylon.js: the same ten views
- Checkerboard screenshots: `qa/renders/three/` and `qa/renders/babylon/`
- Contact sheets: `qa/comparisons/three-orthographic-contact.png`, `three-three-quarter-contact.png`, `babylon-orthographic-contact.png`, `babylon-three-quarter-contact.png`

`qa/viewer-consistency.json`: **PASS**. Overall mean absolute RGB difference between matching engine captures is 4.43779/255. Orthographic views range from 1.64 to 3.63; three-quarter views range from 7.49 to 7.57 because the engines light PBR relief differently. Silhouette, orientation, topology, face assignment and texture direction match.

The standard GLB was additionally loaded in Three.js front view and Babylon.js rear view under `qa/renders/standard-load/`.

## Authority comparisons

The model render was compared against exact front/rear product elevations and exact closed-chassis Serverflow front/top/rear specimen photos:

- `qa/comparisons/authority-front.png`
- `qa/comparisons/authority-rear.png`
- `qa/comparisons/authority-top.png`
- `qa/comparisons/authority-frontRight.png`
- `qa/comparisons/authority-rearRight.png`

Manual feature review passes the invariant counts and ordering: four LFF bays; two rack ears; three rear PCIe zones; management/LOM/service group before the PSU area; exactly two AC PSU modules at the far right of the rear; correct closed-cover latch, seams and vent bands. Difference panels are diagnostic only because the authority photos have different perspective, lighting, labels and specimen wear.

## Known limitation

No exact bottom photograph or official bottom drawing was available. The bottom therefore remains a transparent PNG and modeled face, but its feature content is intentionally conservative and its provenance remains `CONTROLLED_FALLBACK`. This is the reason the final status is not plain `PASS`.

