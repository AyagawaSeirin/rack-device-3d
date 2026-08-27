# Dell PowerEdge R730 2.5-inch rotation and exact-appearance re-review

Date: 2026-08-27 (Asia/Singapore)  
Final disposition: **PASS_WITH_BOTTOM_FALLBACK**

## Frozen delivery identity

Complete Dell PowerEdge R730 (E31S/E31S001) 2U appliance: 16 × 2.5-inch SFF carriers, no security bezel, Dell/PowerEdge R730 control strip, seven vented rear PCIe blanks, iDRAC8/serial/VGA/two USB/four-port 1GbE NDC, two EPP 750 W IEC-C14 AC PSUs and the documented six internal hot-plug cooling fans. Factory Dell, PowerEdge R730, Intel and PSU marks are retained. R730xd, flex-bay rear, LFF, 8-SFF, fitted rear cards, single PSU and DC PSU variants remain excluded.

Final bounds are 482.4 × 87.54 × 741.15 mm, within the 482.4 × 87.3 × 741.0 mm evidence ledger tolerance.

## Frozen artifacts

| Artifact | Bytes | SHA-256 | Pre-review relation |
|---|---:|---|---|
| standard GLB | 13,671,616 | `9c74ffddbb943bbfab7fe47955d2035c8869e4fa9e66eedf0304da6b30059e08` | unchanged |
| web GLB | 1,855,664 | `a86fe63f2e27d1f0cd251e5a69c94f71057ff5733f267e22cbed4bc49de8288e` | unchanged |
| Three.js viewer | — | `399fd9bf1986b29f205ea526dae84d302bbd4164b5e9f851f4c0c5b1add10328` | new independent harness |
| Babylon.js viewer | — | `8a4df2e3080fff783450aa60bab6daae446035ddb50a0aeffe7af69ef72272ad` | new independent harness |

The complete pre-review GLBs, builder, six views, QA tree, load evidence and reports are checksum-preserved in `qa/superseded/pre-rotation-review-20260827/`.

## Reproduction and root-cause decision

The alleged rotation flicker, transparency jump, disappearing face, mirror, gray/white switch and checker leakage did not reproduce in either frozen GLB. Both engines and both GLBs remained stable before and after hash freeze. Structural inspection found no model-layer repair target; changing a passing GLB would have added risk, so the standard/web hashes remain unchanged.

The independent viewers enforce a hidden loading overlay, `qaReady` and render-settle gates, fixed orthographic frustum, right-handed coordinates, near/far 0.01/10, fixed neutral lighting and a serialized cache-busted queue. This distinguishes capture/viewer hazards from the GLB and prevents false mixed/loading frames without lighting compensation.

## Final gates

- `audit_views`: PASS, 0 errors, 0 unresolved; six reviewed antialiased silhouette warnings and no fully transparent inset-core pixel.
- Standard/web `audit_glb`: PASS, 0 errors and 0 warnings each.
- Standard/web duplicate, reverse-duplicate, exterior coplanar, material-alpha, negative-transform, normal/winding and closed-core audit: PASS, 0 errors each.
- Six main face materials: `OPAQUE`, `[1,1,1,1]`, `doubleSided=false`; no main-chassis `BLEND`.
- Texture sampling: six independent embedded images, no atlas/bleed; explicit `LINEAR_MIPMAP_LINEAR` minification in standard and web.
- Frozen-hash loads: 40/40 PASS, 40 unique nonces, 2 engines × 2 GLBs × 10 views; every run WebGL2, overlay absent.
- Frozen-hash rotation: 288 yaw frames, 128 multi-pitch light/dark-checker frames and 72 same-angle stability frames; 0 anomalies/failures.
- Inventory: 50/50 rows reviewed — 48 `PASS_EXACT`, two bottom-fallback rows; standard/web node names synchronize.
- Matched-camera source/render/overlay/difference sets exist for all six faces.

Machine-readable gate: `qa/rotation-review-20260827/final-gate.json`.  
Visual summaries: `qa/rotation-review-20260827/contact-sheets/`.  
Per-row inventory: `qa/rotation-review-20260827/feature-inventory-review.csv`.

## Official 3D and residual risk

Dell currently lists 22 official R730 service 3D experiences, including PSU, fan, cover, risers, control panel and backplane. The exact-model service page exists, but it is not a downloadable proof of this fully installed 16-SFF exterior; fresh Chromium and direct HTTP requests returned Dell/Akamai HTTP 403. Screenshot, headers and untouched error body are preserved; access controls were not bypassed, so no raw official model could be retained.

The sole appearance exception is the documented conservative underside fallback. There is no non-bottom identity/evidence gap. Therefore the correct status is **PASS_WITH_BOTTOM_FALLBACK**.
