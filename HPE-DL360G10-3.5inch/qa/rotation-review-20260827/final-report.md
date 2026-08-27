# HPE DL360 Gen10 3.5-inch independent rotation and exact-appearance review

Date: 2026-08-27 (Asia/Singapore)  
Final disposition: **PASS_WITH_BOTTOM_FALLBACK**

## Scope and frozen identity

The delivered subject is the complete HPE ProLiant DL360 Gen10 1U **4LFF / 3.5-inch** appliance, configuration basis PID `867958-B21`, not the shallower 8SFF, Network Choice rear, Gen9, Gen10 Plus, or Gen11 variant. The final exterior configuration is frozen as:

- four installed LFF Smart Carrier fronts in one row, no security bezel;
- independent front rack ears with authentic HPE / ProLiant DL360 Gen10 branding;
- installed third PCIe riser, 331FLR four-RJ45 FlexibleLOM, embedded 331i four-RJ45 ports, iLO 5, serial, two USB 3.0 and VGA;
- two 500 W Flex Slot Platinum hot-plug **AC** PSUs and seven internal fan modules;
- 482.6 × 43.2 × 751.75 mm actual final GLB bounds, with the authoritative 434.6 × 42.9 × 749.8 mm LFF body dimensions preserved.

The identity manifest, dimension ledger, face-source lock, six face sources, official QuickSpecs/user guide and exact-device photographs were re-read. Left/right and rear-view port order were checked as viewed, not mirrored. No non-bottom identity gap remains.

## Preservation and public official 3D search

The pre-review GLBs, build script, six views, audits, loading evidence and reports were copied before changes to `qa/superseded/pre-rotation-review-20260827/`. Existing official/source files were not overwritten.

The public HPE support/product, current QuickSpecs, exact-PID and GLB/glTF/CAD/STEP/OBJ/FBX/AR searches were repeated. No public exact-configuration official 3D payload was found, so no third-party model was represented as official. The independent standard and web GLBs remain the deliverables.

## Exact-appearance reverse review

All 26 feature-inventory rows were reviewed against locked sources and matched-camera renders: **25 PASS_EXACT and one PASS_BOTTOM_FALLBACK**. The four LFF carriers, five upper grille divisions, ODD/display option blanks, SID/iLO/USB control areas, three PCIe blank groups, 331FLR and embedded 331i port order, serial/USB/VGA/iLO, two independent PSU modules, IEC C14 inlets, fan/handle relief, chassis seams, ears, labels and factory branding match the frozen configuration in count, order, scale, position, relief and handedness.

The bottom is the only fallback. It is explicitly `GENERIC_BOTTOM_FALLBACK`, contains no invented identity-bearing feature and matches the authoritative outline, opacity and dimensions. This is not an exact-source claim for the underside.

Detailed row results: `qa/rotation-review-20260827/feature-inventory-review.csv`.  
Matched-camera source/render/overlay/difference sets: `qa/rotation-review-20260827/comparisons/`.

## Flicker/transparency reproduction and attribution

The pre-review standard/web GLBs were independently loaded in real WebGL2 Three.js 0.179.1 and Babylon.js 8.22.2 viewers, then orbited through 360° yaw at 5° increments with shallow/deep checkerboard pitches. The alleged GLB flicker, transparency jump, face disappearance, mirrored texture, sudden gray/white switch and checker leakage **did not reproduce**.

Three viewer/evidence defects were reproduced and kept separate from the model:

1. author CSS `display:grid` overrode the loading element's `hidden` state and mixed the overlay into frames;
2. per-angle camera refitting caused an apparent scale jump near front/rear transitions;
3. Babylon's continuous background render loop could stall deterministic capture under load.

The final harness forces `#loading[hidden]{display:none!important}`, freezes one orthographic frustum for the complete orbit, uses 0.01/10 near/far planes, right-handed coordinates and explicit deterministic rendering. Invalid evidence was moved into model-local superseded directories and all affected captures were rerun. These were viewer/evidence causes, not GLB transparency.

## Model/material/structure review

No model edit was required after reverse review; old and final hashes are identical. Both variants already use stable, synchronized geometry. The six photographic face materials are `OPAQUE`, `baseColorFactor=[1,1,1,1]`, `doubleSided=false` and unlit; the chassis and relief materials are also opaque with alpha 1. There is no `BLEND`, negative transform, mirrored scale, exact/reversed duplicate triangle or exterior same-facing coplanar overlap.

The custom duplicate/coplanar audit records only buried solid contacts and independently modeled relief with no exterior same-plane risk. After welding UV seams for topology evaluation, the closed chassis core is watertight, winding-consistent and positive-volume. The six source-locked surface cards are intentionally open planes in front of that opaque closed core and do not expose the interior.

## Frozen hashes

| Artifact | Pre-review SHA-256 | Final SHA-256 |
|---|---|---|
| standard GLB | `d6439e734fc85aaef0125f8c40cf0807bf9a147050d594026a3e4d8e1f3a2ac1` | same |
| web GLB | `ab529ee20cb9d295165bb47cdd0429ada6d44b48f87ba4fca315d0cde3cec4bc` | same |
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

- The six `audit_views` warnings are reviewed edge anti-aliasing in source PNG content bounds; no main-face GLB material uses alpha blending and no checkerboard is visible through the product.
- The rack-ear span is constrained by the nominal 19-inch mounting span plus exact imagery while HPE publishes the bare body width separately; this is a measurement provenance limitation, not an unresolved visible identity feature.
- The underside remains the declared bottom-only fallback.

Final conclusion: all non-bottom exact-appearance, structural and cross-engine rotation-stability requirements pass. The only downgrade is the explicitly documented underside source gap; therefore the correct final status is **PASS_WITH_BOTTOM_FALLBACK**.
