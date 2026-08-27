# Final QA — Huawei FusionServer RH1288 V3 / H12M-03 / 8-SFF

> Superseded for the current GLB hashes by `qa/rotation-review-20260827/final-report.md`.

Final status: **PASS_WITH_BOTTOM_FALLBACK**

The standard and web GLBs pass the identity, structure, orientation, opacity, feature-count, two-viewer and matched-camera gates. The status is not ordinary `PASS` only because no exact RH1288 V3 underside evidence was publicly available after the documented search; the bottom uses the permitted conservative fallback.

## Frozen assembly

- Huawei FusionServer RH1288 V3, nameplate H12M-03, 1U.
- Front: eight closed 2.5-inch SFF carriers in the real asymmetric arrangement: three upper and five lower. No security bezel and no NVMe-orange carrier substitution.
- Rear: four GE service RJ45 ports, one management RJ45, two USB 3.0, VGA, serial, UID, one full-height and one half-height perforated PCIe blank.
- Power: two installed 750 W hot-swap AC PSUs. No DC or HVDC variant.
- Excluded: RH1288H, V5/V6/V7, 3.5-inch, 10GE/IB and incompatible rear options.

## Final model files

| Deliverable | Size | SHA-256 | Result |
|---|---:|---|---|
| `model/Huawei-RH1288V3-2.5inch.glb` | 18,455,732 B | `e46479d199d482ca6bb2e0d0b48dc93776198e057ee17ab61c20d60894bee6ca` | PASS |
| `model/Huawei-RH1288V3-2.5inch-web.glb` | 7,037,964 B | `3a975b224eea0ea9f957b3c3ccc3289dd38dcf507b4eea04db2cdebb80cca5ba` | PASS |

Both are self-contained GLB 2.0 files with the same 284 nodes, 284 meshes/primitives, 14 materials, six textures and six embedded images. They use no external buffers, mirrored node transforms or required extensions. All six main face materials are `OPAQUE`.

The published body is 436 × 43 × 708 mm. Final visible GLB bounds, including front mounting span and verified relief, are **482.6 × 43.53 × 715.7 mm**. The repaired visible height is inside the required 43–44 mm envelope.

## Structural audit

| Audit | Errors | Warnings | Result |
|---|---:|---:|---|
| Six transparent face assets | 0 | 0 | PASS |
| Standard GLB | 0 | 0 | PASS |
| Web GLB | 0 | 0 | PASS |

The six face assets preserve their physical ratios, have no transparent chassis core and meet the long-edge resolution gate. Standard GLB textures retain up to 4000 px; web textures retain a 2048 px long edge while preserving the same exterior.

## Actual WebGL loading

Two independent loaders were used: Three.js and Babylon.js/WebGL2. Each engine loaded both the standard and web GLB and captured six orthographic plus four three-quarter views, yielding **40 READY captures and zero load errors**. The full index is `qa/viewer-matrix.csv`; contact sheets are in `qa/contact-sheets/`.

Final front/rear alpha behavior was also inspected over light and dark checkerboards in `qa/renders/alpha-check/`. High-resolution crops of the two rack ears, Huawei logo, service area and model badge are retained in `qa/renders/details/`.

Standard/web render parity was checked for all ten cameras in both engines. The maximum normalized RMSE was **0.00655894** (Babylon rear), so web optimization did not change silhouette, orientation or identifying layout. Individual values are in `qa/viewer-parity.csv`.

Babylon renders are brighter than Three because the viewers use independent lighting implementations. This is a viewer-lighting difference: both agree on UV orientation, feature order, relief, opacity and silhouette.

## Matched-camera comparisons

Six physical-ratio reference canvases were matched to the exact QA cameras. For both engines, each orthographic face has reference/render/50%-overlay/difference sheets under:

- `qa/comparisons/three-standard/`
- `qa/comparisons/babylon-standard/`

The four three-quarter views were checked against the exact official Huawei gallery angles and exact-device rear/ISO supporting photographs. The complete mapping and locked observations are in `qa/comparison-matrix.csv`.

## Repair closure

- The front carrier/service frames now remain behind the source-locked photo; only real handles/latches/accents protrude, removing the false horizontal bars.
- The front VGA was recalibrated to the approved elevation and recessed; the former blue plug-like overhang is gone.
- Small status/control/fastener placeholders were recessed so high-resolution photo detail is no longer covered by colored blocks in close-up.
- Rear port/fan recess geometry was moved to the interior side of the rear plane; the former large black occluders are gone.
- Front-only ears are separate single-sided planes, so a rear orthographic camera no longer sees broad false rear ears.
- The top latch was narrowed and recessed to match the approved top view without a duplicate square frame.
- Visible height is 43.53 mm, down from the rejected 50 mm and intermediate 44.145 mm candidates.

## Feature checklist

Every identity-bearing row in `source/feature-inventory.csv` has a matching final render/geometry result. The machine-readable verdicts are in `qa/feature-verification.csv`. Highlights:

- front carrier count/layout: 3 upper + 5 lower = 8 — PASS;
- front logo/model/Intel markings and front-only ears — PASS;
- rear 4 GE + management + 2 USB + VGA + serial — PASS;
- two PCIe blanks and two AC PSUs — PASS;
- independent, non-mirrored left/right sides — PASS;
- closed top with two seams and near-flush latch — PASS;
- no negative/mirrored transforms, face swap, transparent chassis or visible empty interior — PASS.

## Bottom disclosure

`views/bottom.png` is `GENERIC_BOTTOM_FALLBACK`. It is a plain opaque 436:708 galvanized underside based only on permitted material/edge evidence. It does not copy the top and contains no unsupported Huawei/Dell logo, label, vent, foot, hole, rail, port or service detail. This is the sole reason for the `PASS_WITH_BOTTOM_FALLBACK` result.

## Official 3D status

Huawei's exact historic RH1288 V3 3D viewer URL was found, but on 2026-08-23 it redirected to a service maintenance/migration notice and exposed no lawful public GLB/glTF/OBJ/FBX/STEP binary. No access control was bypassed. The exact official gallery ZIP of two images is preserved unchanged; details are in `source/optional-3d/README.md`.

## Reproducibility and retained history

- `model/build_model.py` is the deterministic build script.
- `qa/scripts/capture_viewer_matrix.js` captures the 40-view validation matrix.
- `qa/scripts/make_reference_canvases.py` reconstructs matched camera references.
- Exact selected image-generation prompts and original task item IDs were recovered from the authorized prior task and stored in `qa/imagegen-prompts/`.
- Rejected front/left generations and the pre-final GLB pair remain outside final `views/` and `model/` outputs under `qa/work/`.
