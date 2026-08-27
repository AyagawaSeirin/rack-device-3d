# Rotation and exact-appearance review — Huawei FusionServer Pro 1288H V5 4LFF

Final status: **PASS_WITH_BOTTOM_FALLBACK**

## Frozen identity and authenticity

- Exact subject: Huawei FusionServer Pro `1288H V5`, Huawei PID `21872252`, 1U, four 3.5-inch LFF carriers, no bezel.
- Rear/configuration: three-I/O/riser family, exact service/FlexIO order, two installed 900 W hot-swap AC PSUs; no V3/V6, 2.5-inch, 2-I/O or DC substitution.
- Body: 436 × 43 × 748 mm; front-ear span 482.6 mm; final visible envelope 482.6 × 43.8 × 767.75 mm including sourced relief/projections.
- Current Huawei/public 3D recheck found no exact public downloadable 1288H V5 binary. The authoritative new build remains the required standard/web pair.
- Every one of the 27 feature-inventory rows is mapped to final actual-GLB evidence in `feature-inventory-verification.csv` and the 12 matched-camera source/render/overlay/difference sets under `matched-camera/`.

## Before/after hashes

| GLB | Pre-review SHA-256 | Final SHA-256 | Final bytes |
|---|---|---|---:|
| standard | `2da2a955a2a6eeedd455e8a698d63aef4e912ad59a1c9ccd3f2be2b414b9d845` | `acdbcd17c394d9f16952edc8855be3f9e35d7babe56db826dea25cf33890aa59` | 10,469,568 |
| web | `d811bb2d41af0c4f98d11e61884fcc9143b2de4f2403e3ce61f3e85dfd2f3933` | `c209a024784f953e2d6643fca8883c621aa67b12c54c202c683c0acf02a43dc0` | 8,147,936 |

The complete pre-rotation GLBs, build script, views, audits, load evidence and reports were copied before repair to `qa/superseded/pre-rotation-review-20260827/`. Existing 2026-08-24 user checkpoints were preserved and incorporated.

## Reproduction and root cause

- Reproduced: **yes**, in Babylon.js/WebGL2 for both standard and web at yaw 290°, pitch 18°. The source-locked top card disappeared for one frame and exposed the pale PBR backing. The affected ROI bright-pixel fraction was 31.35% (standard) / 31.37% (web).
- Root cause: six broad texture cards were only 0.1 mm from backing surfaces; Babylon's oblique depth precision selected the backing at one orbit angle. The V5 top/right canonical PNGs also contained transparent chassis-core symbols/holes, and large solid rear relief panels obscured exact source-photo detail.
- This was not a lighting-only defect. Three.js did not reproduce the single-frame dropout, while Babylon did, proving a cross-viewer depth/export stability problem.

## Repair

- Restored 8,441 top and 8,064 right core alpha pixels to 255 without changing RGB; dark labels/holes now remain opaque on both checkerboards.
- Inset the hidden closed body/top/bottom backing to provide at least 0.5 mm broad-card separation without moving the external envelope.
- Removed all exact card/relief tangencies; rear perforated panels and ports now use intersecting thin rails instead of identity-obscuring solid rectangles.
- Kept exact photo cards OPAQUE, `[1,1,1,1]`, single-sided and unlit; retained handles, latches, ears, carrier relief, PSU relief and sourced protrusions.
- Applied the same visible geometry, orientation, materials and configuration to standard/web; web only reduces non-identifying repeated detail/texture budget.

## Final gates

- `audit_views`: PASS, 0 errors. Six warnings are limited to anti-aliased external silhouettes/verified ear edges; every chassis core reports 0% alpha below 250.
- `audit_glb`: standard PASS and web PASS, 0 errors / 0 warnings.
- Extra structure: 0 duplicate triangle groups, 0 opposite duplicate pairs, 0 negative transforms, 0 material-alpha violations, 0 exact critical coplanar pairs, 0 textured-card/backing risks, one watertight closed core in each GLB.
- Static loads: 40/40 READY, 40/40 WebGL2, 40 screenshots present, 0 loader errors (`static-40-loads/static-40-load-manifest.json`).
- Rotation stress: Three standard 88, Three web 88, Babylon standard 88, Babylon web 88 = 352 final frames. Every combination includes 72 yaw frames at 5° plus 16 multi-pitch dark-checker frames.
- The former yaw-290 bright fraction is now 0.113% for both standard/web; contact-sheet review found no flicker, opacity jump, checkerboard leak, face disappearance, mirror, texture switch or sudden gray/white exposure.
- Standard/web parity over 88 corresponding frames per viewer: max normalized RMSE 0.006641 (Three) and 0.003913 (Babylon).

## Warning / residual risk

The only evidence exception is the documented conservative `GENERIC_BOTTOM_FALLBACK`; it contains no unsupported identity detail and changes no verified silhouette. No non-bottom identity gap or unresolved rotation risk remains.
