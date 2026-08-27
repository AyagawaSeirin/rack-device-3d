# Huawei RH2288 V3 3.5-inch — final rotation review

Final result: **PASS_WITH_BOTTOM_FALLBACK**

## Frozen delivery identity

- Huawei FusionServer RH2288 V3, nameplate H22M-03, 2U, 12 common 3.5-inch LFF carriers in 3 × 4, no bezel.
- No rear disks; SM211 2 × GE, photographed blank PCIe positions, standard management/console group, two vertically stacked WEPW80015 460 W AC PSUs.
- Left and right shells are independently source-locked and are not mirrored.
- Only the bottom is a controlled generic fallback: plain closed galvanized sheet with no invented identity-bearing detail.
- A current official-public-3D recheck found no downloadable exact official mesh; see `official-3d-recheck-20260827.md`.

## Hashes and reproduction

| Variant | Before SHA-256 | Final SHA-256 |
|---|---|---|
| standard | `274f7f7dc399c3dfc187c4c5b74d4c34fbbe76d93475ad8455fcfa4d68772e3c` | `acd512a706c8f546e6bab8e20884b3cafa7fef230a22047c2a0f764d90f900c2` |
| web | `0bf68be256a5e69ac79acd0c0411802519289c17be87852550dda0ec94f1398a` | `175eb3aadf23be5f50f38206ace84797cebe53a1743cb56d0016126c2051df71` |

Before repair, Three.js and Babylon.js both loaded the model, but source cards, procedural detail, and the full-size core used coplanar or sub-threshold parallel planes. This reproduced the model-side cause of edge/layer shimmer and apparent transparency; the sampled 5° frames did not show a gross whole-device disappearance.

## Root fix

- Inset the watertight core by 1 mm.
- Removed the duplicate front-ear cap and duplicate procedural rear face representation.
- Rebuilt the rear as seven non-overlapping source-locked regions with stable 0.7 mm backing.
- Stabilized carrier backing, top latch, and cord-loop relationships without moving identity-bearing exterior features.
- Kept all approved source-locked PNGs unchanged; standard and web use identical visible mesh arrays and node transforms.

## Final gates

| Gate | Result |
|---|---|
| `audit_views` | PASS, 0 errors; 6 silhouette anti-alias warnings only |
| standard `audit_glb` | PASS, 0 errors, 0 warnings |
| web `audit_glb` | PASS, 0 errors, 0 warnings |
| material alpha | OPAQUE only; alpha 1; `doubleSided=false`; embedded alpha pixels 0 |
| transforms/core | 0 negative transforms; watertight, consistent, positive-volume core |
| duplicate/coplanar | 0 duplicate/opposite groups; 0 hazardous coplanar/near-coplanar pairs |
| standard/web geometry parity | PASS, 64 meshes and 64 bindings/transforms identical |
| static browser loads | PASS, 2 viewers × 2 GLBs × 10 views = 40 successful loads |
| rotation stress | PASS, 84 frames per combination = 336 final frames |

Every combination contains 72 yaw frames at 5° spacing plus 12 pitch keyframes, on light and dark checkerboards. Manual contact-sheet review found no surface flicker, transparency jump, checkerboard leak, disappearing face, mirror, texture switch, or sudden gray surface.

## Evidence and residual risk

- Before/after rotation evidence: `qa/rotation-review/{before,after}/{three,babylon}/{standard,web}/`
- Matched source/render/overlay/difference: `qa/rotation-review/after/matched-camera/contact-sheet.png`
- Feature inventory row review: `qa/rotation-review/after/feature-inventory-review.csv`
- Structural report: `qa/rotation-review/after/structural-rotation-audit.json`
- Machine-readable result: `qa/rotation-review/rotation-stress-report.json`

The only residual authenticity limitation is the documented bottom fallback. Two raw sub-1 mm² cord-loop solid-junction contacts are reported for transparency but are below the hazard threshold and are not visible parallel draw surfaces. No non-bottom identity gap remains.

