# Rotation and exact-appearance review — Huawei FusionServer RH1288 V3 / H12M-03 / 8-SFF

Final status: **PASS_WITH_BOTTOM_FALLBACK**

## Frozen identity and authenticity

- Exact subject: Huawei FusionServer `RH1288 V3`, nameplate `H12M-03`, 1U, eight 2.5-inch carriers in the real 3-upper/5-lower arrangement, no bezel.
- Rear: SM212-visible four GE service ports, management RJ45, 2×USB 3.0, VGA, serial, UID, one full-height and one half-height PCIe blank, two installed 750 W AC PSUs.
- Excludes RH1288H, V5/V6/V7, 3.5-inch, 10GE/IB, DC/HVDC and rear ears.
- Published body: 436 × 43 × 708 mm; final sourced visible envelope 482.6 × 43.53 × 715.7 mm.
- Huawei's historic exact interactive viewer route remains known, but the 2026-08-27 migrated page exposed no public downloadable exact 3D binary. The preserved official archive contains PNGs only.
- All 32 inventory rows are mapped to final actual-GLB evidence in `feature-inventory-verification.csv`; 12 matched-camera source/render/overlay/difference sets are under `matched-camera/`.

## Before/after hashes

| GLB | Pre-review SHA-256 | Final SHA-256 | Final bytes |
|---|---|---|---:|
| standard | `e46479d199d482ca6bb2e0d0b48dc93776198e057ee17ab61c20d60894bee6ca` | `eec6b1d8766e2da42aa9d042753ed99196876c8a0003bf983c2056cd9bbde6ea` | 18,463,300 |
| web | `3a975b224eea0ea9f957b3c3ccc3289dd38dcf507b4eea04db2cdebb80cca5ba` | `e562c63eafe5eea0896823be28b0d332e47405f2e14c2ab393f4203206cae1e8` | 7,045,532 |

The original GLBs, build script, views and full QA/load/report evidence were copied first to `qa/superseded/pre-rotation-review-20260827/`.

## Reproduction and root cause

- No abrupt face dropout was visible in the valid baseline 4×88 frame rotation matrix.
- The latent export defect was nevertheless present: all six cards sat only 0.1 mm from the closed chassis, and the PBR photo materials produced strong viewer-dependent brightness divergence. This was below the required cross-viewer depth margin and could become the same failure at another camera/driver precision.

## Repair

- Placed the six source cards on the authoritative body planes and inset the watertight core by 1.0 mm overall, producing 0.5 mm separation without changing external relief or final bounds.
- Converted the six source-photo materials to KHR_materials_unlit while enforcing OPAQUE, `[1,1,1,1]` and `doubleSided=false`; exact colors and labels now remain stable across Three/Babylon.
- Preserved the existing exact carrier, service-port, PCIe, PSU, handle, ear, side and top geometry; no source PNG was regenerated or restyled.

## Final gates

- `audit_views`: PASS, 0 errors / 0 warnings.
- `audit_glb`: standard/web PASS, 0 errors / 0 warnings; visible bounds unchanged at 482.6 × 43.53 × 715.7 mm.
- Extra structure: 0 duplicate triangle groups, 0 opposite duplicate pairs, 0 negative transforms, 0 material-alpha violations, 0 exact critical coplanar pairs, 0 textured-card/backing risks, one watertight closed core per GLB.
- Static loads: 40/40 READY and WebGL2, 40 screenshots present, 0 loader errors.
- Rotation stress: Three standard 88, Three web 88, Babylon standard 88, Babylon web 88 = 352 frames; no flicker, transparency jump, checkerboard leak, face loss, mirror, texture switch or sudden gray/white exposure.
- Standard/web parity max normalized RMSE: 0.006207 (Three), 0.002836 (Babylon).

## Warning / residual risk

The only exception is the documented conservative `GENERIC_BOTTOM_FALLBACK`; it carries no unsupported identity feature and does not alter any verified side silhouette. No non-bottom identity gap remains.
