# Juniper MX204 final QA report

Final status: **PASS_WITH_BOTTOM_FALLBACK**

## Scope and identity

The completed asset is the exact AC exterior variant of Juniper MX204 / `MX204-HW-BASE`, chassis `JNP204-CHAS`: fixed 1U appliance, three `JNP-FAN-1RU` front-to-back/AFO fan modules, two `JPSU-650W-AC-AO` AC PSUs, no transceivers installed, no front bezel. The user screenshot's third readable row was treated as a configuration clue and was not used as a final texture.

## Face generation and alpha

- Six built-in `image_gen` calls were made, exactly one per face.
- Source modes: front/rear/top `SOURCE_LOCKED_GENERATION`; left/right `MULTI_REFERENCE_RECONSTRUCTION`; bottom `GENERIC_BOTTOM_FALLBACK`.
- All raw outputs used a uniform `#00ff00` key and the installed imagegen key-removal helper.
- `views-audit.json`: `PASS`, zero errors. Maximum physical-ratio error is 1.5576%.
- Every inset chassis core is fully opaque. Partial alpha is limited to real ear holes and anti-aliased external edges.
- Final face dimensions: front/rear 4112x387; left/right 4112x397; top/bottom 1964x2064.

## Model structure

The GLBs are newly constructed, not official-file substitutes and not six decorative planes on a box. They include a closed chassis plus 167 other named visible geometry nodes: four mounting flanges with true rounded through-holes, front bracket fasteners, front port recess groups, three rounded fan-handle assemblies with continuous depth arms, two AC PSU assemblies with handles/ejectors/cord loops and continuous connector arms, paired three-section side rails, top channel, 26 screw heads, and front-edge cover holes.

Both GLBs contain 168 nodes/meshes/primitives, 15 PBR materials, six embedded textures, normals, and UVs. They have no external buffers, no negative/mirrored node transform, and all materials are `OPAQUE`/`doubleSided=false`.

Measured GLB bounds are 482.600 x 43.860 x 519.600 mm versus the 482.6 x 43.7 x 518.9 mm ledger. The small residual is the antialiased/relief clearance of outward face planes and is within the audit tolerance; non-uniform ratio error is 0.3138%.

## Actual GLB viewer validation

Two independent glTF engines were used through real Playwright-driven browser renders:

1. Three.js 0.169 `GLTFLoader`: all six orthographic, four three-quarter, light/dark front/rear for the standard GLB; four check views for the web GLB.
2. Babylon.js glTF loader: all six orthographic, four three-quarter, light/dark front/rear for the web GLB; four check views for the standard GLB.

Both viewers agree on face orientation, normal logo/text direction, opacity, ear holes, AC rear order, and geometry. Standard-versus-web same-camera mean absolute RGB difference is 0.1624/255 in Three.js and 0.1558/255 in Babylon.js; maximum is below 0.335/255.

Twenty-four comparison sheets cover six orthographic views in each engine, four authoritative three-quarter references, and eight standard-versus-web checks. Direct front/rear comparisons retain exact feature counts and order. Three-quarter comparisons confirm the separate top cover, side rails, front brackets, rear fans, PSUs, handles, ejectors, and cord loops.

## Embedded texture verification

All six standard-GLB embedded images were extracted and compared pixel-for-pixel with `views/*.png`; every one is identical. Web textures are the same approved assets downscaled only to a maximum 2048-pixel edge. No generated preview, source thumbnail, or stale texture is embedded.

## Bottom exception

No exact MX204 underside photograph or technical drawing was found after the required official, PDF, dynamic-browser, third-party, marketplace, video/teardown, and multilingual escalation. The bottom is therefore the allowed conservative generic fallback: correct verified 447:470 body ratio and gray sheet-metal finish, with no logo, label, vent, hole, foot, rail, seam, screw, or unsupported protrusion. This is the sole reason the final status is `PASS_WITH_BOTTOM_FALLBACK` instead of `PASS`.

## Official 3D search

No public exact-PID official 3D/CAD/GLB/GLTF or interactive-viewer asset was found. `source/optional-3d/` is intentionally empty. No login, authentication, paywall, access control, or private API was bypassed.

## Final files

- `model/Juniper-MX204.glb` — 12,160,388 bytes — SHA-256 `d9a933eeefa4905c10b5256b0505e61fd9ecdd2237154132bf0cde64b59f79a2`
- `model/Juniper-MX204-web.glb` — 7,829,716 bytes — SHA-256 `a0f03859097b35021df2ca5436ae70404c62de849eb40b9a530a774cef3d759b`

There are no unresolved non-bottom evidence gaps and no unresolved QA errors.
