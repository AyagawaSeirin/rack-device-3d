# HPE DL360 Gen9 2.5-inch independent rotation and exact-appearance review

Date: 2026-08-27 (Asia/Singapore)  
Final disposition: **PASS_WITH_BOTTOM_FALLBACK**

## Scope and frozen identity

The delivered subject is the complete HPE ProLiant DL360 Gen9 1U **8SFF / 2.5-inch** appliance, CTO chassis `755258-B21`, not Gen10 or a 10SFF/NVMe variant. The final configuration is frozen as:

- eight HPE SFF Smart Carrier faces in the correct 6+2 arrangement and a Universal Media Bay with optical drive, VGA and USB;
- independent HPE Quick Release ears with authentic chassis-era HP/HPE / ProLiant DL360 Gen9 factory marks;
- three PCIe blanks, FlexibleLOM blank, stacked USB 3.0, serial, iLO 4, embedded four-port 331i and rear VGA;
- two matched 500 W Flex Slot Platinum hot-plug **AC** PSUs with IEC C14, red latch, pull handle and visible fan geometry;
- 482.6 × 43.2 × 723.5 mm final envelope around the authoritative 434.7 × 43.2 × 698.5 mm body.

The identity manifest, dimension ledger, face-source lock, HPE QuickSpecs/service figures, exact ECS front photograph, exact dual-AC rear photograph and remaining six-face sources were re-read. Drive numbering/order, PSU order, rack ears, port groups, labels and left/right orientation were checked without mirroring. No non-bottom identity gap remains.

## Preservation and public official 3D search

The pre-review GLBs, build script, six views, audits, loading evidence and reports were copied before changes to `qa/superseded/pre-rotation-review-20260827/`. Existing source files were preserved.

The public HPE product/support, current QuickSpecs, exact-PID and GLB/glTF/CAD/STEP/OBJ/FBX/AR searches were repeated. No public exact 8SFF official 3D payload was found. The HPE exploded-view resource is video, and the Visio asset is 2D; neither was promoted as an official 3D deliverable.

## Exact-appearance reverse review and repairs

All 23 feature-inventory rows were reviewed against locked sources and matched-camera renders: **22 PASS_EXACT and one PASS_BOTTOM_FALLBACK**. The 8 SFF carrier faces, three intake regions, Universal Media Bay/control strip, ears/branding, three rear expansion blanks, FlexibleLOM blank, serial/USB/VGA/iLO/331i order, dual AC PSU modules, fans, inlets, handles, seams, labels and side/top treatment match in count, order, scale, position, relief and handedness.

The fresh pre-review `audit_views` found real source-view defects that old PASS reports had missed:

- `rear.png` and `right.png` contained sub-opaque pixels in the main product core;
- `front.png` included 29-pixel transparent side strips, leaving the exact face ratio 1.9565% off target.

The repair preserved all RGB product pixels, ports, labels and branding. Border-connected exterior alpha was retained, internal/main-core alpha was made opaque, and the front was cropped/rescaled to the metric 3072 × 275 face. Standard and web GLBs were then rebuilt from the repaired source-locked views. The legacy Babylon viewer was also corrected to right-handed coordinates; that viewer change is separate from the GLB repair.

Changed source-view hashes:

| View | Pre-review SHA-256 | Final SHA-256 |
|---|---|---|
| front | `3c6bdaf703ba1282dc9ba0b3b5353d5d46fd72ac135e29fabb3b36e13b84101a` | `ca7d9971589938f4ecc979d4613ecf3a42058f433f4a7910bef498b92a288b45` |
| rear | `5a1a3d0b0f6c4aba795fd350993b40f88a5b2106e90383d10dd6c00d49bf951d` | `77f302fa3b82d08d60940ab2be271811cd845316ca2af3a61aa5039539ef4b29` |
| right | `e3ea5602e1573fe5112218546723b0787ae69b5141f0db285929767509f423f6` | `24ff188fe0e604d34797d8deb571f68614033a0586a64c05ca7352abc96facd8` |

The bottom is the only fallback. It is explicitly `GENERIC_BOTTOM_FALLBACK`, introduces no identity-bearing claim and passes dimensions, opacity and rotation checks.

Detailed row results: `qa/rotation-review-20260827/feature-inventory-review.csv`.  
Matched-camera source/render/overlay/difference sets: `qa/rotation-review-20260827/comparisons/`.

## Flicker/transparency reproduction and attribution

The pre-repair and final standard/web GLBs were each loaded in real WebGL2 Three.js 0.179.1 and Babylon.js 8.22.2 viewers and orbited through complete 360° yaw at 5° increments plus shallow/deep checkerboard pitches. The source alpha defects were confirmed by file/audit inspection, but the builder's opaque photographic material path meant the alleged on-orbit flicker/transparent jump itself **did not reproduce** in the pre-repair GLBs. Pre-repair rotation evidence is retained under `qa/superseded/pre-repair-rotation-evidence-20260827/`.

Independent viewer/evidence defects were also reproduced: CSS mixed the loading overlay into frames, per-angle camera refitting created an apparent scale jump, and Babylon's continuous background render loop could stall deterministic capture. Final viewers use enforced overlay hiding, right-handed coordinates, a frozen orthographic frustum, 0.01/10 near/far and explicit rendering. Invalid evidence was moved to model-local superseded storage and fully rerun. These viewer factors are not reported as model-alpha causes.

## Model/material/structure review

Standard and web were rebuilt together and remain synchronized. All six photographic face materials are `OPAQUE`, `baseColorFactor=[1,1,1,1]`, `doubleSided=false` and unlit; all chassis/relief materials are opaque with alpha 1. There is no `BLEND`, negative transform, mirrored scale, exact/reversed duplicate triangle or exterior same-facing coplanar overlap.

Recorded coplanar relationships are buried solid contacts or source-locked relief with `exteriorRisk=false`. After welding UV seams for topology evaluation, the structural chassis core is watertight, winding-consistent and positive-volume. Open photographic face planes are backed by the closed opaque chassis core and do not leak the checkerboard/interior.

## Frozen hashes

| Artifact | Pre-review SHA-256 | Final SHA-256 |
|---|---|---|
| standard GLB | `3360da73d2f1471d49960bcb8d260a82801b502129230c1190d582ae6f0c1271` | `91315cddd57bf7e16b2d784414dc3410fb119eaf993f48e3f05f643681d28281` |
| web GLB | `31ef838553e8d91759057fe32eb974a4324dc263b4d38bcd7a5375b180f67559` | `bea25286f06a1a4bbee803299e318ef696683c3c51fe86a900ac36f1ad10fc8e` |
| Three.js final viewer | n/a (new independent harness) | `d6ac8c05c9162fc403b459eec373e61cdbb1a192dbed50578493536e7f742681` |
| Babylon.js final viewer | n/a (new independent harness) | `dee3e02e93a3ceee0b2151da9ee77d6b0effe8577bb3c7e705a64a859ef6055b` |

## Final gates

| Gate | Result |
|---|---|
| `audit_views` | PASS, 0 errors, 6 reviewed anti-aliased silhouette warnings; opaque core alpha defects = 0 |
| standard `audit_glb` | PASS, 0 errors, 0 warnings |
| web `audit_glb` | PASS, 0 errors, 0 warnings |
| duplicate/coplanar/material-alpha/negative-transform/closed-core, standard + web | PASS, 0 errors |
| independent loads | 40/40 PASS; 40 unique nonces; 2 viewers × 2 GLBs × 10 views; WebGL2 true; overlay absent |
| orbit evidence | 288 yaw frames (72 per combination) + 64 shallow/deep pitch frames; anomaly count 0 |
| visual result | no flicker, transparency jump, checker leakage, disappearing/mirrored face, texture switch, gray/white flash, overlay mixture or clipping |

Machine-readable result: `qa/rotation-review-20260827/final-gate.json`.  
40-load summary/contact sheet: `qa/rotation-review-20260827/static-40-loads/summary.json` and `all-40-contact-sheet.png`.  
Rotation manifests/contact sheets: `qa/rotation-review-20260827/final-rotation/`.

## Warnings and residual risk

- The six final `audit_views` warnings are reviewed silhouette anti-aliasing only; main product cores are opaque and GLB main-face materials do not blend.
- The nominal rack-ear span and external PSU-handle depth combine official body dimensions with exact-device imagery; this is dimension provenance, not an unresolved visible identity feature.
- The underside remains the declared bottom-only fallback.

Final conclusion: the source alpha/ratio defects were repaired and both GLBs rebuilt; all non-bottom exact-appearance, structural and cross-engine rotation-stability requirements pass. The only downgrade is the explicitly documented underside source gap; therefore the correct final status is **PASS_WITH_BOTTOM_FALLBACK**.
