# Juniper MX304 repair v2 final QA report

Final status: REWORK

2026-08-24 forced revalidation revoked the prior pass: the accepted physical-right
face was a horizontal flip of its dedicated imagegen output. This is forbidden
by the exact-appearance contract. See `repair-v3/before/revalidation-detected/`.
The remainder of this file is the preserved prior repair-v2 report and is not a
current acceptance result while repair v3 is in progress.

## Rework cause and preservation

The prior final left face mirrored the right generation, which is an immediate REWORK condition. The full pre-repair state is preserved under repair-v2/before/ with 109 checksummed files. No historical source, view, GLB, report, render or comparison was silently overwritten without that archive.

## Independent physical-left lineage

The replacement uses MULTI_REFERENCE_RECONSTRUCTION from only real/official physical-left evidence:

- Official Juniper Left view photo for exact target identity, two-RE/two-LMIC16 configuration, material, color, style and front direction.
- Exact JNP304/MX304 used photograph for the complete physical-left panel, 2x4 recesses, front pad, screw/black-locator sequence, front ear, rear AC/fan projection and real wear.
- Exact target-configuration Juniper Community real photograph for target edge/material confirmation.
- Official Hardware Guide page 99 for slots, mounting holes and front/rear geometry.

right.png, the rejected mirrored left, prior AI faces, old GLBs and all renders/comparisons were forbidden as inputs. Three imagegen attempts were retained: r1 was factually correct; r2 still had the wrong physical ratio; r3 changed to 2x3 slots and exposed the top. The selected r1 was rectified without whole-face axis stretching: only feature-free gray metal gaps were lengthened, all mechanical feature spans retained original horizontal pixel scale, and the final 2409x321 content was uniformly resized to 3072x409.

The final left has front at screen-right and rear at screen-left, exactly 2 rows x 4 recesses, one front pad, two cyan front handle profiles and a left-specific black-locator/screw sequence. It is visibly and bytewise different from physical-right and from the rejected mirror.

## Structural results

- Six-view audit: PASS, 0 errors. Left physical-ratio error 0.0466%; maximum face error 0.0792%. Alpha warnings resolve to anti-aliased silhouettes/true ear holes; all cores have zero fully transparent pixels.
- Front/rear elevation audit: PASS, 0 errors, 0 warnings.
- Standard GLB: PASS, 0 errors, 0 warnings; 15,984,340 bytes; 120 nodes; 22 meshes/primitives; 19 materials; 6 embedded images; exact 482.6 x 88.9 x 667.2 mm proportions.
- Web GLB: PASS, 0 errors, 0 warnings; 2,405,508 bytes; identical geometry/counts/bounds.
- Non-mirror audit: PASS. Both side nodes use identity rotation, scale [1,1,1], positive determinant and no negative/mirrored parent. Left physical front +Z maps to image-right u=1; right physical front maps to image-left u=0.
- Extracted standard/web left textures match the selected repaired texture hashes exactly; left/right embedded textures are distinct.

## Viewer and comparison results

- Three.js and Babylon.js each rendered front, rear, left, right, top and bottom from the actual standard GLB; Three.js additionally rendered all four three-quarter views and front-top.
- Maximum cross-viewer mean RGB difference: 6.572205/255; repaired left difference: 1.578883/255. Orientation, opacity and feature counts agree.
- Standard/web eight-camera maximum mean RGB difference: 1.490990/255; repaired left: 0.713187/255.
- 42 repair renders and 30 repair comparison sheets are retained, including left evidence, before/after and asymmetric landmark sheets.
- Light/dark checkerboards confirm left black locator holes and recesses are opaque pixels rather than transparency.

## Remaining exception

Only the previously documented conservative bottom fallback remains. There are no unresolved non-bottom evidence items. No exact public official 3D/CAD asset was found.
