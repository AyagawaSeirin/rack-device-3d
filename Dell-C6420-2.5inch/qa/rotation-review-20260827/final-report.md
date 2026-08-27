# Dell PowerEdge C6420 2.5-inch rotation and exact-appearance re-review

Date: 2026-08-27 (Asia/Singapore)  
Final disposition: **PASS_WITH_BOTTOM_FALLBACK**

## Frozen delivery identity

Complete 2U Dell PowerEdge C6400 enclosure populated with four air-cooled C6420 sleds, 24 × 2.5-inch carriers, default blank rear PCIe/mezzanine regions, four blue sled handles and two shared EPP 1600 W AC PSUs in the center stack. Rear sled order remains 3/4 at screen-left and 1/2 at screen-right. Four internal 60 mm dual-rotor fans are documented. Dell EMC/C6400 and EPP marks remain source-locked; standalone sleds, partial populations, C6520/C6525, LFF, mixed NVMe, external add-in NICs, DC PSUs and liquid cooling remain excluded.

Final bounds are 482.6 × 86.8 × 797.3 mm.

## Frozen artifacts

| Artifact | Bytes | SHA-256 | Pre-review SHA-256 |
|---|---:|---|---|
| standard GLB | 16,380,516 | `88348a13c53b99c31408225b483cdf5c7adba612b9505ea9b7466d684ce60151` | `ecc0f7ff5b5cd595ae72e00af83f63e0857fefb079787c4737b61ef353d674f9` |
| web GLB | 6,890,888 | `7a8c3b7442786f723ec71bb21220d9a3d716a02a5ed3e72b66d5ca756186c680` | `b78c3c55807c96d9831ceb8da5e162684558f253135c438cd96a238ad1f61553` |
| Three.js viewer | — | `399fd9bf1986b29f205ea526dae84d302bbd4164b5e9f851f4c0c5b1add10328` | — |
| Babylon.js viewer | — | `8a4df2e3080fff783450aa60bab6daae446035ddb50a0aeffe7af69ef72272ad` | — |
| builder | — | `fb39666925ed5d1453288f4d0a7ecefc196fde58fd73eaf43ee8c6a2eacd38a1` | archived |

The complete pre-review state is checksum-preserved in `qa/superseded/pre-rotation-review-20260827/`. Pre-repair rotation evidence and the rejected first layer-repair evidence/GLBs are separately preserved under `qa/superseded/`.

## Reproduction, model cause and repair

The initial 2-engine/2-GLB orbit sequence did not show an abrupt frame jump, but independent structural analysis found **47 exterior same-facing coplanar overlaps in each GLB**. The risk concentrated on top photo card versus seams/fasteners, side cards versus ribs/fasteners, and rear module boundaries versus ports/fan relief. This was a genuine model/export z-fighting risk, not texture alpha.

The builder now maintains a mechanical depth ledger: closed body/module backing → source-locked photo card → boundary → port/fan grille → handle/fastener, with camera-correct sign on each face. Standard and web are rebuilt from the same corrected builder. The first repair placed the rear photo card behind dark module bodies; manual 40-load inspection caught the obscured rear despite automated stability passing. That frozen set was archived and invalidated. The final rear order was corrected, hashes refrozen, and the complete C6420 rotation/load suite rerun.

The independent viewers enforce hidden overlay, `qaReady`, render settling, fixed frustum, right-handed coordinates, near/far 0.01/10, fixed neutral lighting and serialized cache-busted capture. No viewer-specific residual defect remains.

## Final gates

- `audit_views`: PASS, 0 errors, 0 unresolved; six reviewed antialiased source/silhouette warnings, no fully transparent inset-core pixel.
- Standard/web `audit_glb`: PASS, 0 errors and 0 warnings each.
- Standard/web duplicate, reverse-duplicate, exterior coplanar, material-alpha, negative-transform, normal/winding and closed-core audit: PASS, 0 errors each; exterior same-facing coplanar count is 0.
- Six main face materials: `OPAQUE`, `[1,1,1,1]`, `doubleSided=false`; no main-chassis `BLEND`.
- Texture sampling: six independent embedded images, no atlas/bleed; glTF default LINEAR minification showed no final orbit shimmer.
- Final frozen-hash loads: 40/40 PASS, 40 unique nonces, 2 engines × 2 GLBs × 10 views; rear fully visible in all four combinations; every run WebGL2, overlay absent.
- Final frozen-hash rotation: 288 yaw frames, 128 multi-pitch light/dark-checker frames and 72 same-angle stability frames; 0 anomalies/failures.
- Inventory: 45/45 rows reviewed — 43 `PASS_EXACT`, two bottom-fallback rows; standard/web node names synchronize.
- Matched-camera source/render/overlay/difference sets exist for all six faces.

Machine-readable gate: `qa/rotation-review-20260827/final-gate.json`.  
Visual summaries: `qa/rotation-review-20260827/contact-sheets/`.  
Per-row inventory: `qa/rotation-review-20260827/feature-inventory-review.csv`.

## Official 3D and residual risk

Fresh official-domain and real-browser review found no public exact C6400 + four C6420 + 24-SFF installed-assembly raw 3D asset. The 3D Guides endpoint returned Dell/Akamai HTTP 403; evidence is preserved without bypass. No file is mislabeled official.

The sole remaining exception is the conservative, non-identifying underside fallback. No non-bottom identity/evidence gap remains. Therefore the correct status is **PASS_WITH_BOTTOM_FALLBACK**.
