# Dell PowerEdge R630 2.5-inch rotation review — task 11

Final status: **PASS_WITH_BOTTOM_FALLBACK**

## Frozen deliverables

| Deliverable | SHA-256 |
|---|---|
| `model/Dell-R630-2.5inch.glb` | `ef889b24b442408367577ccfc4b3d44839da2dd2c58cafb542471a4fec5ee6d5` |
| `model/Dell-R630-2.5inch-web.glb` | `0afb1b6a3afeafdfdad2f675b9a6957fe98bc160bce616f26faae07d45c4a600` |
| `tools/build_glb.py` | `52d4606c40d9609fe327b32f0442279571ce5347b986643731d8d90d001da1fd` |
| Three.js orbit viewer | `09397e305ac39f3a87af77d253a848eed6f0be8d163fa75d2b3580fc665a116a` |
| Babylon.js orbit viewer | `37ee630ebd49c0c28fb2a62c98f549b6112d099a41196d881f84e12a07347ca6` |

Freeze and final hash verification are in `final/frozen-hashes.json` and `final/freeze-verification.json`; all five records match.

## Identity and authenticity

- Exact product: Dell PowerEdge R630, 13G, 1U long chassis, bezel absent, 10 × 2.5-inch SFF in five columns × two rows.
- Rear: three-riser chassis with three LP blanks; iDRAC8/DB9/VGA/2×USB; quad-RJ45 NDC; two matching EPP 1100 W hot-plug AC PSUs. DC, mixed, missing, 750 W and SFP+/RJ45 alternate configurations remain excluded.
- Cooling: seven source-verified internal hot-swap fan housings/rotors under the opaque cover; two rear PSU fans remain source-photo details.
- Rack hardware: two front-only wing housings; no rear ears, rails or cable-management arm.
- Genuine Dell/PowerEdge R630 and configuration-locked Intel Xeon markings remain in source-locked textures.
- Bounds: 482.4 × 42.8 × 752.2 mm versus 482.4 × 42.8 × 752.1 mm ledger; audit has zero dimension errors/warnings.

Inventory verification: `final/inventory-verification/inventory-verification.json`, 29/29 rows plus 4/4 hard gates PASS in standard and web.

## Reproduction and root cause

The archived GLBs did not produce a nondeterministic same-angle pop under the new stable renderer, but the actual model was still structurally REWORK: four top service-hatch frame overlaps, fourteen C14/handle coplanar junction risks after full rear-surface inspection, and a negative-volume Y-axis latch cylinder caused by a handedness-changing coordinate permutation.

The defect was in the **model/export layer**, not engine lighting or alpha. Both engines read identical opaque materials. Repair shortened intersecting frame/rim members into non-overlapping joints, separated release/handle parts, restored Y-axis cylinder winding, and added seven verified internal fan configuration nodes. The viewer now uses dynamic near/far ratio 120, NoToneMapping, no post-processing and no overlay capture; source-photo face materials remain unlit.

## Final WebGL2 evidence

- Four combinations; each has 72 × 5° yaw, 16 pitch and 16 stability frames over light/dark checkerboards.
- Total 416 rotation/stability frames. Same-angle maximum MAE: 0.0. Maximum adjacent luma delta: 2.61; maximum adjacent area delta: 0.00198.
- Forty cache-busted independent new-page loads all used WebGL2, matched frozen hashes, and had zero overlay/console errors.
- `final/frame-analysis/summary.json`: 4/4 PASS. `final/static-40-loads/load-run.json`: 40/40 PASS.
- `final/matched-camera/`: 24 actual-GLB captures and 24 source/render/overlay/difference sets across both engines, both levels and all six faces.

No final evidence shows flicker, transparency variation, leakage, disappearance, mirroring, gray/white switching or mixed loading frames.

## Audits

- Views audit: PASS, zero errors. Five alpha warnings were visually resolved as transparent canvas/anti-aliased boundary pixels; all six inset equipment cores are 0% transparent.
- Standard/web GLB audits: PASS, zero errors/warnings.
- Enhanced standard/web audits: zero duplicate, coplanar, material-alpha, negative-transform, normal/winding or closed-core errors.
- Main face materials are `OPAQUE`, `[1,1,1,1]`, `doubleSided=false`; no main chassis `BLEND`; closed core is watertight and positive-volume.

## Official model search and residual risk

No exact official public R630 10×2.5, three-riser, quad-RJ45, dual-AC 3D file was found in the 2026-08-27 recheck. The Playwright CLI Dell route returned HTTP 403 and no model resource; evidence is under `research/playwright-dell/`. No third-party mesh was substituted.

The only residual gap is the documented exact underside. The conservative `GENERIC_BOTTOM_FALLBACK` contains no invented branding/mechanical detail, so the correct final status is `PASS_WITH_BOTTOM_FALLBACK`.

All pre-repair GLBs, builder, six views, audits, load evidence and reports are preserved under `qa/superseded/pre-rotation-review-20260827/`.
