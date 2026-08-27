# Fortinet FG1500D — final rotation review

Final result: **PASS_WITH_BOTTOM_FALLBACK**

## Frozen delivery identity

- Fortinet FortiGate FG-1500D AC, D generation, 2RU; FG-1500DT and FG-1500D-DC are excluded.
- Front: 16 × GE SFP, 16 × GE RJ45, 8 × 10GE SFP+/GE SFP, 2 × MGMT RJ45, console, USB-A and USB mini-B.
- Rear: the user's explicitly locked row-3 delivery appearance—four fan trays, service/blank panels, and two vertical AC PSUs.
- Independent non-mirrored sides and source-locked Fortinet top cover.
- Bottom remains a conservative closed ivory-white fallback with no invented features.
- A current official-public-3D recheck found no downloadable exact official mesh; the uncertified community USDZ remains excluded. See `official-3d-recheck-20260827.md`.

## Hashes and reproduction

| Variant | Before SHA-256 | Final SHA-256 |
|---|---|---|
| standard | `23db204ad7fe973ddcd007b01e6a05d4d62d2c206ea9f4e3c524b310f51602ee` | `b1ce643236d9515ca7221375bea026a7525fe0bd80e0df25f80bbe17fcd52987` |
| web | `2005bc62304731e6eb0c68dadb0ca4b799200a0d1afff0482afe84915d969d03` | `aebec4e41028be1a73dc52beba4d6bf98d445a5bcd7e6c172cdc83daf4c39d36` |

Before repair, both GLBs contained 192 exact duplicate triangle groups from redundant symmetric fan bars, unstable coplanar/near-coplanar relief, and a non-watertight core. Those model-side defects were common to both viewers and could produce angle-dependent shimmer or apparent transparency even though no gross whole-device disappearance occurred in the 5° sample.

## Root fix

- Replaced the core with a custom indexed 8-vertex/12-triangle watertight outward shell.
- Replaced eight redundant full fan bars with four bars while retaining eight visible spokes, eliminating all 192 duplicate groups.
- Removed perimeter and side seams already represented by the locked textures.
- Stabilized fan hubs, rear handle mounts, fasteners, and face/backing depth levels.
- Preserved the approved elevation PNGs; standard and web now contain identical visible mesh arrays and node transforms.

## Final gates

| Gate | Result |
|---|---|
| `audit_views` | PASS, 0 errors, 0 warnings |
| standard `audit_glb` | PASS, 0 errors, 0 warnings |
| web `audit_glb` | PASS, 0 errors, 0 warnings |
| material alpha | OPAQUE only; alpha 1; `doubleSided=false`; embedded alpha pixels 0 |
| transforms/core | 0 negative transforms; watertight, consistent, positive-volume core |
| duplicate/coplanar | 0 duplicate/opposite groups; 0 hazardous coplanar/near-coplanar pairs |
| standard/web geometry parity | PASS, 336 meshes and 336 bindings/transforms identical |
| static browser loads | PASS, 2 viewers × 2 GLBs × 10 views = 40 successful loads |
| rotation stress | PASS, 84 frames per combination = 336 final frames |

Every combination contains 72 yaw frames at 5° spacing plus 12 pitch keyframes, on light and dark checkerboards. Manual review found no surface flicker, transparency jump, checkerboard leak, disappearing face, mirror, texture switch, or sudden gray surface.

## Evidence and residual risk

- Before/after rotation evidence: `qa/rotation-review/{before,after}/{three,babylon}/{standard,web}/`
- Matched source/render/overlay/difference: `qa/rotation-review/after/matched-camera/contact-sheet.png`
- Feature inventory row review: `qa/rotation-review/after/feature-inventory-review.csv`
- Structural report: `qa/rotation-review/after/structural-rotation-audit.json`
- Machine-readable result: `qa/rotation-review/rotation-stress-report.json`

The bottom fallback is the only missing exact face. Fortinet catalog imagery shows a different factory rear; this asset intentionally follows the user's frozen row-3 delivery appearance and does not claim that rear as catalog-authoritative. Relative to that frozen subject there is no non-bottom gap. Twenty-four raw sub-1 mm² fan/handle/bar solid-junction contacts remain reported; all hazardous visible draw-order counts are zero.
