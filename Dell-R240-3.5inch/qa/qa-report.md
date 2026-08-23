# Dell PowerEdge R240 4LFF exact-appearance QA report

Final status: **PASS_WITH_BOTTOM_FALLBACK**

## Identity and installed configuration

- Exact product: Dell EMC PowerEdge R240, regulatory model E57S / type E57S001.
- Form: 1U, 4 × 3.5-inch/LFF hot-swap front, bezel absent, all four Dell 14G carrier faces installed.
- Rear: standard onboard serial, VGA, dedicated iDRAC, two 1GbE, two USB 3.0, system ID/CMA, one half-height and one full-height PCIe blanking plate, lower vent field and one fixed/cabled AC PSU.
- Cooling: four individually represented single-rotor cabled fan assemblies below the installed opaque cover.
- Power correction: official R240 documentation proves a single non-redundant fixed/cabled PSU. A dual-PSU rear would be an impossible R240/R340 hybrid, so the final model contains exactly one installed AC PSU and an explicit `Second_AC_PSU_ABSENT` configuration marker.
- Factory Dell EMC / PowerEdge R240 markings remain visible on the source-locked front face. Reseller marks were excluded.

## Authoritative dimensions and coordinates

- Overall width: 482.0 mm.
- Body width: 434.0 mm.
- Height: 42.8 mm.
- Body depth: 534.496 mm.
- Overall no-bezel depth: 573.596 mm.
- Coordinate system: right-handed glTF, +X device-right from the front, +Y up, +Z front.

Both final GLBs report an audited world bounding box of exactly 0.482 × 0.0428 × 0.573596 m. Proportion error is 0.0%.

## Six-face source lock

All six canonical PNGs were independently generated/reconstructed and visually inspected at original detail. Physical left and right use different generations, different source bindings and different hashes; neither is a mirror of the other. Detailed prompts and source roles are in `qa/imagegen-prompts/`; selected chroma and final hashes are in `qa/imagegen-generation-record.csv`.

`qa/views-audit.json` status is PASS with zero errors. Its six warnings only flag intentional antialiased silhouette pixels; every chassis-core transparent-pixel measurement is 0.0%. Bottom uses only a plain central galvanized material crop and contains no unsupported holes, labels, feet, vents, seams or fasteners.

## GLB structural gates

Both GLBs are newly constructed self-contained files and use the same external geometry. The standard file embeds full-resolution six-face textures; the web file embeds proportional reduced textures.

- Six embedded base-color images; no external buffers or image URIs.
- All primary equipment-face materials are OPAQUE; no BLEND material.
- No negative-determinant/mirrored transforms.
- 132 nodes, 15 meshes/primitives and 13 materials.
- `qa/glb-standard-audit.json`: PASS, 0 errors, 0 warnings.
- `qa/glb-web-audit.json`: PASS, 0 errors, 0 warnings.
- `qa/feature-count-audit.json`: PASS: 4 carrier bodies, 4 handles, 4 release rings, 1 installed fixed AC PSU, 2 PCIe blanking plates, 4 cabled fans, 5 independent features per physical side and all required rear I/O nodes.

## Independent WebGL final gate

The final artifacts were fetched with `cache: no-store`, parsed and rendered in two independent engines:

- Three.js 0.170.0 / WebGL2.
- Babylon.js 7.44.0 / WebGL2.

Each engine loaded each GLB in ten views: front, rear, physical left, physical right, top, bottom, front-left, front-right, rear-left and rear-right. The accepted final set is exactly 40 post-repair loads, 40 screenshots at 1280 × 800 and zero browser errors. Every record includes actual byte length, GLB SHA-256, bounds, HTTP 200, screenshot SHA-256, parse/render booleans and the unique request URL in `qa/webgl-evidence/load-evidence.json` and `.ndjson`.

Four engine/model contact sheets were inspected at original detail. Thirty-two reference/render/overlay/difference sheets cover the six canonical orthographic sources plus the authoritative ETB front-right and TechMike rear-right photographs for every viewer/model pair. Earlier diagnostic screenshots that revealed a loading overlay, a 2 µm PSU depth overlap and false rear-view front-ear silhouettes were discarded; all 40 accepted screenshots were captured after those repairs.

## Official exact 3D search

No publicly downloadable official Dell exact R240 3D/AR/GLB/glTF/CAD asset was found. Dell product and support galleries exposed only 2D media. Therefore `source/optional-3d/` contains the reproducible search log only and no substitute model. The two delivered GLBs remain independent reconstructions.

## Bottom fallback and remaining risk

The exact R240 underside was not found after official manual, Dell product/support, exact-unit photography, full-video, marketplace and local-language searching. The bottom is therefore the skill-approved conservative fallback. A generic Dell 1U underside was used for sheet-metal material character only and no geometry was copied from it.

Remaining risk is limited to the unavailable underside, fine non-identity regulatory microprint, and sub-millimetre side/top stamping placement reconstructed from multiple oblique real photos rather than factory orthographic elevations. No non-bottom identity, port, bay, PSU, slot, branding or overall-dimension gate remains unresolved.

