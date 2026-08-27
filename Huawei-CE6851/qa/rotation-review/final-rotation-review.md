# Huawei CE6851 — final rotation review

Final result: **PASS**

## Frozen delivery identity

- Huawei CE6851-48S6Q-HI, ordering part 02350JAS, complete CE6851-HI-B-B0A 1U appliance.
- Port side: 48 × 10GE SFP+ and 6 × 40GE QSFP+, fitted two-hole rack brackets.
- Power side: PAC-600WA-B, FAN-40EA-B, management/USB/barcode panel, FAN-40EA-B, PAC-600WA-B.
- Back-to-front airflow; independent non-mirrored sides; exact photographed top and underside.
- No bottom fallback. A current official-public-3D recheck found no downloadable exact official mesh; see `official-3d-recheck-20260827.md`.

## Hashes and reproduction

| Variant | Before SHA-256 | Final SHA-256 |
|---|---|---|
| standard | `8fb2e08ad9937d8d8bbdb524f6a83ca6c1d2882c19299289b9e28282e556531f` | `1558860afd7f3f036593fe22bcf16bc3407bd05e936b79eb7651e58c33b447a1` |
| web | `f3ab68606febe15ed6be49147e58590f58f7537bfcb012629a261ec3e63519a8` | `ed3b60003d5771eeca43364910e6e51eb7b648abe0ad4925543e86967be6d7aa` |

Before repair, the six evidence cards were only about 0.08 mm from the full-size core, and rear/top relief added further coplanar or near-coplanar planes. Both viewers therefore shared a model-side source of subpixel shimmer/draw-order instability, although no gross whole-device disappearance occurred in the sampled 5° frames.

## Root fix

- Inset the watertight core while retaining the authored official exterior bounds.
- Inset rear module bodies behind the source-locked rear face.
- Separated top vent/seam layers; the final two vent dividers sit on the outer vent surface as non-intersecting 0.6 mm relief.
- Preserved all six approved source-locked PNGs unchanged.
- Regenerated standard/web from the same scene; an intermediate 0.35 mm divider-risk checkpoint is preserved under `qa/superseded/post-repair-divider-rework-20260827/` and excluded from final evidence.

## Final gates

| Gate | Result |
|---|---|
| `audit_views` | PASS, 0 errors; 6 silhouette anti-alias warnings only |
| standard `audit_glb` | PASS, 0 errors, 0 warnings |
| web `audit_glb` | PASS, 0 errors, 0 warnings |
| material alpha | OPAQUE only; alpha 1; `doubleSided=false`; embedded alpha pixels 0 |
| transforms/core | 0 negative transforms; watertight, consistent, positive-volume core |
| duplicate/coplanar | 0 duplicate/opposite groups; 0 hazardous coplanar/near-coplanar pairs |
| standard/web geometry parity | PASS, 49 meshes and 49 bindings/transforms identical |
| static browser loads | PASS, 2 viewers × 2 GLBs × 10 views = 40 successful loads |
| rotation stress | PASS, 84 frames per combination = 336 final frames |

The final browser evidence is explicitly cache-bound to hash prefixes `1558860a` and `ed3b6000`. Every combination contains 72 yaw frames at 5° spacing plus 12 pitch keyframes, on light and dark checkerboards. Manual review found no surface flicker, transparency jump, checkerboard leak, disappearing face, mirror, texture switch, or sudden gray surface.

## Evidence and warnings

- Before/after rotation evidence: `qa/rotation-review/{before,after}/{three,babylon}/{standard,web}/`
- Matched source/render/overlay/difference: `qa/rotation-review/after/matched-camera/contact-sheet.png`
- Feature inventory row review: `qa/rotation-review/after/feature-inventory-review.csv`
- Structural report: `qa/rotation-review/after/structural-rotation-audit.json`
- Machine-readable result: `qa/rotation-review/rotation-stress-report.json`

The locked physical-left silhouette ratio differs from the pure 420:43.6 body ratio by 3.873%, inside the recorded 4% source-lock tolerance because it contains proven protrusions. The GLB dimensions audit independently. The 1 raw coplanar and 18 raw near pairs are internal-core or sub-1 mm² solid-junction contacts; the explicit hazardous visible-surface count is zero. No identity gap remains.

