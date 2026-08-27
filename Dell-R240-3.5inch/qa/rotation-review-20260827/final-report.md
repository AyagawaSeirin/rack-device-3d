# Dell PowerEdge R240 3.5-inch rotation review — task 11

Final status: **PASS_WITH_BOTTOM_FALLBACK**

## Frozen deliverables

| Deliverable | SHA-256 |
|---|---|
| `model/Dell-R240-3.5inch.glb` | `f3593d8c33703b3975c428499f7f0d28e9f44e949a625a9d95d05841da40c863` |
| `model/Dell-R240-3.5inch-web.glb` | `7308ddf9ff281d039390ad09559b892dc8da5237f28667da05ae303742a15ef1` |
| `model/build-model.js` | `a4f91977253a5f12665b39f00bf1672da473fede04aa3d090b8eba8b42cc4955` |
| Three.js orbit viewer | `09397e305ac39f3a87af77d253a848eed6f0be8d163fa75d2b3580fc665a116a` |
| Babylon.js orbit viewer | `37ee630ebd49c0c28fb2a62c98f549b6112d099a41196d881f84e12a07347ca6` |

Freeze: `final/frozen-hashes.json`; post-evidence verification: `final/freeze-verification.json`, all five records match.

## Identity and authenticity

- Exact product: Dell EMC PowerEdge R240, E57S/E57S001, 1U, 4 × 3.5-inch hot-swap LFF, bezel absent.
- Rear: standard onboard I/O, both PCIe openings blanked, one fixed/cabled non-redundant AC PSU. A dual-PSU/R340-style rear remains explicitly excluded.
- Cooling: four source-verified single-rotor cabled fans, retained as four internal configuration nodes under the opaque cover.
- Rack hardware: two front-only ear/control assemblies; no rear ears.
- Factory Dell EMC / PowerEdge R240 markings remain in the source-locked real-photo textures. No synthetic logo plane was added.
- Bounds: 482.0 × 42.8 × 573.2 mm actual versus 482.0 × 42.8 × 573.596 mm ledger; dimension audit has zero errors/warnings.

Inventory verification: `final/inventory-verification/inventory-verification.json`, 22/22 rows plus 4/4 hard configuration gates PASS for both standard and web.

## Reproduction and root cause

The archived pre-repair GLBs reproduced a top-face switch between the real source texture and flat gray cover at different yaw/pitch combinations. Structural inspection found exact top/bottom card-to-solid coplanarity, two duplicate same-facing bottom triangles, 43 exterior coplanar overlaps, a PSU strap/body overlap, and inward/negative cylinder side winding affecting release rings, buttons and fan rotors.

This was primarily a **model/export defect**, because both Three.js and Babylon.js loaded the same frozen bytes and exposed the same risky surfaces. The prior viewer's broad fixed clipping range made depth competition harder to diagnose, but lighting or alpha was not the cause: all main materials were already OPAQUE.

Repair: inset closed core/deck surfaces; establish deterministic card/core/relief clearances; keep dense top perforation appearance in the exact source texture rather than covering it with coarse blocks; remove remaining PSU coplanarity; correct cylinder winding. The final viewer uses dynamic near/far with ratio 120, NoToneMapping, no post-processing, no loading-overlay capture, and only neutral light for solid relief; face textures are unlit.

## Final WebGL2 evidence

- Four combinations: Three.js/Babylon.js × standard/web.
- Per combination: 72 yaw frames at 5°, 16 multi-pitch frames, and 16 same-angle stability frames across light/dark checkerboards.
- Per model total: 288 yaw + 64 pitch + 64 stability = 416 rotation/stability frames.
- Same-angle maximum pixel MAE: 0.0. Maximum adjacent 5° object-luma delta: 4.82. Maximum adjacent silhouette-area delta: 0.00279.
- Forty cache-busted independent new-page loads: 2 engines × 2 levels × 10 views. All 40 used WebGL2, matched the frozen model hashes, and recorded zero overlay frames and zero console errors.
- `final/frame-analysis/summary.json`: 4/4 PASS. `final/static-40-loads/load-run.json`: 40/40 PASS.
- `final/matched-camera/`: 24 actual-GLB captures and 24 four-panel source/render/overlay/difference comparisons; front, rear, left, right, top and bottom are covered for both engines and both levels.

No final frame shows flicker, transparency jumps, interior leakage, face disappearance, mirroring, gray/white texture switching, or loading-mask mixing.

## Audits

- `final/audits/views-audit.json`: PASS, zero errors. Six alpha warnings were visually resolved as transparent canvas/anti-aliased silhouette or verified openings; every inset equipment core is 0% transparent.
- Standard/web baseline GLB audits: PASS, zero errors and zero warnings; six embedded face images are RGB/opaque.
- Standard/web enhanced audits: PASS, zero duplicate, coplanar, material-alpha, negative-transform, normal/winding and closed-core errors.
- Closed core is watertight, winding-consistent and positive-volume; all main face materials are `OPAQUE`, `[1,1,1,1]`, `doubleSided=false`; main chassis uses no `BLEND`.

## Official model search and residual risk

No public exact official Dell R240 3D/CAD/AR/GLB/glTF file was found in the 2026-08-27 recheck. Dell's dynamic manual route returned HTTP 403 in the Playwright CLI session and exposed no public model payload; artifacts are under `research/playwright-dell/`. Therefore no official binary exists to preserve, and both repaired self-built GLBs remain the deliverables.

The only residual evidence limitation is the documented exact-underside gap. `bottom.png` remains the conservative `GENERIC_BOTTOM_FALLBACK`, with no unsupported identifying detail. This is why the result is `PASS_WITH_BOTTOM_FALLBACK`, not ordinary `PASS`.

Pre-repair evidence is preserved under `qa/superseded/pre-rotation-review-20260827/`. A rejected intermediate post-freeze build and all of its evidence are preserved under `qa/superseded/post-freeze-rejected-fidelity-20260827T1502Z/`.
