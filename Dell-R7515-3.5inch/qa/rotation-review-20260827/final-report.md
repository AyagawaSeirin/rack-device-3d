# Dell PowerEdge R7515 3.5-inch rotation and exact-appearance re-review

Date: 2026-08-27 (Asia/Singapore)  
Final disposition: **PASS_WITH_BOTTOM_FALLBACK**

## Frozen delivery identity

Complete Dell PowerEdge R7515 (E46S/E46S003) 2U appliance: 12 × 3.5-inch LFF carriers in 3 × 4 layout, no security bezel, no rear-drive cage, Riser 1B plus slots 4/5, two stacked EPP 750 W AC PSUs, six internal system fans and visible PSU exhaust fans. The real Dell/PowerEdge R7515 marks remain in their verified physical locations. R7525, SFF, 8-LFF, rear-2-LFF and DC/HVDC configurations remain excluded.

Final bounds are 482 × 86.8 × 703.755 mm. Body width/depth and front/rear projections remain separately recorded in the dimension ledger.

## Frozen artifacts

| Artifact | Bytes | SHA-256 | Pre-review relation |
|---|---:|---|---|
| standard GLB | 18,850,044 | `06b20f03ccc702fddb0dec854f37f60f4a4c14761488b3b58591bc7824b90f55` | unchanged |
| web GLB | 10,604,860 | `692020e5444f1f071f340a6f3b4908d8e4eef60ee570471bd1f3103496ec1f76` | unchanged |
| Three.js viewer | — | `399fd9bf1986b29f205ea526dae84d302bbd4164b5e9f851f4c0c5b1add10328` | new independent harness |
| Babylon.js viewer | — | `8a4df2e3080fff783450aa60bab6daae446035ddb50a0aeffe7af69ef72272ad` | new independent harness |

The complete pre-review GLBs, builder, six views, QA tree, load evidence and report are checksum-preserved in `qa/superseded/pre-rotation-review-20260827/`.

## Reproduction and root-cause decision

The alleged rotation flicker, transparency jump, disappearing face, mirror, gray/white switch and checker leakage did not reproduce in either frozen GLB. Initial and final real-Chromium WebGL2 runs agreed in Three.js and Babylon.js. The generic first `audit_views` invocation incorrectly used body depth for side elevations that include the front wing and rear PSU projection; the face-specific dimension ledger resolves that audit-configuration cause. No model edit was justified, so the GLB hashes remain unchanged.

Viewer/capture causes were independently controlled: enforced hidden loading overlay, `qaReady` gate, explicit render settling, fixed orthographic frustum, right-handed Babylon coordinates, fixed near/far 0.01/10, fixed neutral lighting with no per-angle compensation, and serialized cache-busted capture. These controls prevent overlay mixture, per-angle scale jumps and premature capture without masking a model defect.

## Final gates

- `audit_views`: PASS, 0 errors, 0 unresolved; two reviewed side-silhouette antialias warnings.
- Standard/web `audit_glb`: PASS, 0 errors and 0 warnings each.
- Standard/web duplicate, reverse-duplicate, exterior coplanar, material-alpha, negative-transform, normal/winding and closed-core audit: PASS, 0 errors each.
- Six main face materials: `OPAQUE`, `[1,1,1,1]`, `doubleSided=false`; no main-chassis `BLEND`.
- Texture sampling: six independent embedded images, no atlas/bleed; glTF default LINEAR minification showed no orbit shimmer.
- Frozen-hash loads: 40/40 PASS, 40 unique nonces, 2 engines × 2 GLBs × 10 views; every run WebGL2, overlay absent.
- Frozen-hash rotation: 288 yaw frames (72 × 5° per combination), 128 multi-pitch light/dark-checker frames and 72 same-angle stability frames; 0 anomalies/failures.
- Inventory: 34/34 rows reviewed — 33 `PASS_EXACT`, one `PASS_BOTTOM_FALLBACK`; standard/web node names synchronize.
- Matched-camera source/render/overlay/difference sets exist for all six faces.

Machine-readable gate: `qa/rotation-review-20260827/final-gate.json`.  
Visual summaries: `qa/rotation-review-20260827/contact-sheets/`.  
Per-row inventory: `qa/rotation-review-20260827/feature-inventory-review.csv`.

## Official 3D and residual risk

Fresh official-domain and real-browser review found no public exact installed-configuration R7515 raw 3D asset. The 3D Guides endpoint returned Dell/Akamai HTTP 403; the result is preserved without bypass. No file is mislabeled official.

The sole remaining evidence exception is the conservative, non-identifying underside documented as `GENERIC_BOTTOM_FALLBACK`. There is no non-bottom identity/evidence gap. Therefore the correct status is **PASS_WITH_BOTTOM_FALLBACK**.
