# Huawei RH1288 V3 3.5-inch independent rotation and exact-appearance review

Date: 2026-08-27 (Asia/Singapore)  
Final disposition: **PASS_WITH_BOTTOM_FALLBACK**

## Scope and frozen identity

The delivered subject is the complete Huawei FusionServer RH1288 V3 / nameplate model **H12M-03**, 1U **4LFF / 3.5-inch** chassis, not RH1288H, RH2288, V5, 8SFF/NVMe or another rear-network variant. The final configuration is frozen as:

- four closed LFF carrier fronts, slots 0–3 left to right, no security bezel;
- authentic Huawei, RH1288 V3 and Intel factory marks on independent front ears;
- SM212-visible four-GE rear face, management RJ45, two USB 3.0, VGA, serial and UID; full-height and half-height PCIe blanks installed;
- two 460 W Platinum hot-swap **AC** PSUs in 1+1 redundancy and five internal N+1 fan modules;
- 482.6 × 43 × 748 mm final envelope, including the nominal rack-ear span.

The identity manifest, dimension ledger, face-source lock, whitepaper/datasheet figures, official gallery, exact Rozetka 4LFF photographs and exact LNC four-GE rear photograph were re-read. Port order, PSU order, rack ears and left/right orientation were checked from the viewer's real rear/front viewpoints. No non-bottom identity gap remains.

## Preservation and official 3D search

The pre-review GLBs, build script, six views, audits, loading evidence and reports were copied before changes to `qa/superseded/pre-rotation-review-20260827/`. The preserved official Huawei viewer index was not overwritten.

A fresh real-Chromium check confirmed that Huawei's current RH1288 V3 gallery still shows `查看3D`, but it redirects to the historic `/computing/server3D/res/server/rh1288v3/index.html` service. The viewer URL, `tree.json` and model resources return HTTP 302 to Huawei's migration page; the migrated catalogue has no RH1288 V3 entry, and public archive checks yielded no payload. The archived index also exposes an 8SFF/DVD component tree and does not prove a 4LFF exterior. Therefore no exact official 4LFF model file was available to preserve, and the independent GLBs are not claimed to be Huawei's official payload.

## Exact-appearance reverse review

All 37 feature-inventory rows were reviewed against locked sources and matched-camera renders: **36 PASS_EXACT and one PASS_BOTTOM_FALLBACK**. The four carrier/grille faces, ears and branding, ESN slot, diagnostic/operator group, USB/VGA, full/half-height rear blanks, four-GE FlexIO face, management/serial/UID, dual AC PSU fans/inlets/handles, cover seams, vents, labels and non-mirrored side treatment match in count, order, scale, position, relief, material and handedness.

The bottom is the only fallback. It is explicitly `GENERIC_BOTTOM_FALLBACK`, introduces no identity-bearing claim and passes dimension, opacity and rotation checks.

Detailed row results: `qa/rotation-review-20260827/feature-inventory-review.csv`.  
Matched-camera source/render/overlay/difference sets: `qa/rotation-review-20260827/comparisons/`.

## Flicker/transparency reproduction and attribution

The pre-review standard/web GLBs were loaded in real WebGL2 Three.js 0.179.1 and Babylon.js 8.22.2 viewers and orbited through complete 360° yaw at 5° increments plus shallow/deep checkerboard pitch frames. The alleged model flicker, transparent jump, face disappearance, mirrored texture, gray/white switching and checker leakage **did not reproduce**.

The same independent viewer/evidence defects were reproduced and corrected: CSS kept the loading overlay visible despite `hidden`, per-angle camera refitting produced an apparent scale jump, and Babylon's background render loop impeded deterministic capture. Final viewers use an enforced hidden overlay, right-handed coordinates, a frozen orthographic frustum, 0.01/10 near/far and explicit rendering. All invalid affected evidence was moved to model-local superseded storage and rerun. These were viewer/evidence factors, not GLB alpha failures.

## Model/material/structure review

No GLB edit was required; old and final hashes are identical. Standard and web are synchronized. All six source-locked photo materials are `OPAQUE`, `baseColorFactor=[1,1,1,1]`, `doubleSided=false` and unlit. All remaining colored relief is opaque with alpha 1. There is no `BLEND`, negative transform, mirrored scale, exact/reversed duplicate triangle or exterior same-facing coplanar overlap.

Recorded same-plane contacts are buried solid/relief relationships with `exteriorRisk=false`. After topology is evaluated from welded positions rather than UV seam splits, the closed chassis shell is watertight, winding-consistent and positive-volume. The six open photographic planes remain backed by the opaque closed shell, with no interior/checker leakage.

## Frozen hashes

| Artifact | Pre-review SHA-256 | Final SHA-256 |
|---|---|---|
| standard GLB | `c21ff62d34ee592364bd4fd8634a6bc2f8fb30e099985fa8b10540bc3ffb35bc` | same |
| web GLB | `af81151cbcb35e22161b351ba783b3b86cc426d4a3fa20b31c1510f855518cb6` | same |
| Three.js final viewer | n/a (new independent harness) | `d6ac8c05c9162fc403b459eec373e61cdbb1a192dbed50578493536e7f742681` |
| Babylon.js final viewer | n/a (new independent harness) | `dee3e02e93a3ceee0b2151da9ee77d6b0effe8577bb3c7e705a64a859ef6055b` |

## Final gates

| Gate | Result |
|---|---|
| `audit_views` | PASS, 0 errors, 3 reviewed anti-aliased silhouette warnings; opaque core alpha defects = 0 |
| standard `audit_glb` | PASS, 0 errors, 1 reviewed warning |
| web `audit_glb` | PASS, 0 errors, 1 reviewed warning |
| duplicate/coplanar/material-alpha/negative-transform/closed-core, standard + web | PASS, 0 errors |
| independent loads | 40/40 PASS; 40 unique nonces; 2 viewers × 2 GLBs × 10 views; WebGL2 true; overlay absent |
| orbit evidence | 288 yaw frames (72 per combination) + 64 shallow/deep pitch frames; anomaly count 0 |
| visual result | no flicker, transparency jump, checker leakage, disappearing/mirrored face, texture switch, gray/white flash, overlay mixture or clipping |

Machine-readable result: `qa/rotation-review-20260827/final-gate.json`.  
40-load summary/contact sheet: `qa/rotation-review-20260827/static-40-loads/summary.json` and `all-40-contact-sheet.png`.  
Rotation manifests/contact sheets: `qa/rotation-review-20260827/final-rotation/`.

## Warnings and residual risk

- The one GLB warning per variant is the auditor's generic warning for an untextured unlit colored relief material. It does not apply to any photographic face; all textured faces use neutral `[1,1,1,1]`, and the custom material-alpha audit records no violation.
- The three `audit_views` warnings are reviewed silhouette anti-aliasing, not transparent product-core pixels.
- Huawei's currently inaccessible official 3D payload prevents an official-file comparison; exact appearance is instead locked to current official dimensions/documentation plus exact 4LFF/front and four-GE/rear photographs.
- The underside remains the declared bottom-only fallback.

Final conclusion: all non-bottom exact-appearance, structural and cross-engine rotation-stability requirements pass. The only downgrade is the explicitly documented underside source gap; therefore the correct final status is **PASS_WITH_BOTTOM_FALLBACK**.
