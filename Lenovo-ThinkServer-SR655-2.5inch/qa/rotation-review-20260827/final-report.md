# Rotation and exact-appearance re-review — Lenovo ThinkSystem SR655 24x2.5

Final status: **PASS**  
Review date: 2026-08-27  
Delivery subject: original-generation Lenovo ThinkSystem SR655, types 7Y00/7Z01, B5VJ 24x2.5-inch front, PCIe-rich 8-slot rear, no rear drives, two 750W AC PSUs.

## Hash transition

| GLB | Pre-review SHA-256 | Final SHA-256 | Final bytes |
|---|---|---|---:|
| standard | `51e5d5a72fb4f4471d76cb24f16627d10e7ea12993ebeec220aa2da7f7f7bc25` | `b34a0af03dcd28de63131f9e18494ac17cd4f960c18e0726c51d81da0ab2c677` | 12,052,840 |
| web | `3a721b51d754151d01b5981391318b5d74b361ef8e9f980228167dc8846f1f09` | `b2fd3bfbd4457318066a52bad42563d61f30fb7bf08d79a5a3a80512b4952011` | 8,607,280 |

The complete pre-review checkpoint is under `qa/superseded/pre-rotation-review-20260827/`; the rejected white-top intermediate is under `qa/superseded/rotation-review-after-white-top-20260827/`.

## Reproduction and root cause

The pre-review standard and web GLBs each contained **230** photographic-surface/geometry pairs separated by at most 0.25 mm, plus overlapping frame corners and shared outward planes. The rear PNG was also 2600x467 at the front-ear width and failed the physical rear-body ratio by 8.32%, stretching a rear that has no rear ears.

Root cause: insufficient depth hierarchy/overlapping relief, compounded by an incorrectly normalized rear elevation. Lighting was not the causal repair layer.

## Repair

- Inset the closed core and establish stable photographic-skin/frame/handle/relief ordering without changing final bounds.
- Remove frame-corner overlap and duplicate full top/bottom plates; retain source-locked shallow seams in texture and real projecting parts as geometry.
- Reuse the already validated 2400x467 rear from the physically identical B5VK/B5VJ 8-slot, no-rear-drive, dual-750W configuration byte-for-byte, as required by the elevation pairing rule. No face was regenerated.
- Keep all six photo materials OPAQUE, neutral, single-sided and unlit.
- Standard/web geometry signature: `64a1cf1eb8025de20130b59e51f37f051bf1a6b7a544d4e46e9cf1eb8105f4db` in both files.

## Structural gates

- `audit_views.py`: PASS, 0 errors after rear correction; warnings are anti-aliased exterior edges only.
- `audit_glb.py`: standard/web PASS, 0 errors and 0 warnings.
- Final bounds: 482.0 x 86.5 x 764.7 mm.
- 256 nodes/meshes/primitives, 17 materials, six independent embedded RGB textures.
- Exact duplicate triangles: 0; near-coplanar photographic pairs <=0.25 mm: 230 -> 0; negative transforms: 0; material-alpha errors: 0.
- Closed core: watertight, winding-consistent, positive volume.

## Real-browser gates

| Viewer / GLB | 5-degree yaw frames | Continuous animation frames | Dark-checker pitch frames | Result |
|---|---:|---:|---:|---|
| Three / standard | 72 | 75 | 8 | PASS |
| Three / web | 72 | 75 | 8 | PASS |
| Babylon / standard | 72 | 31 | 8 | PASS |
| Babylon / web | 72 | 26 | 8 | PASS |

Both viewers are WebGL2 (Three.js r169, Babylon.js 9.22.0). Final-hash HTTP evidence proves 40/40 static loads plus four rotation loads. No final sequence shows flicker, transparency, checkerboard leakage, missing/mirrored faces, texture switching or a gray jump.

## Exact appearance

The current official tour and LP1161 still confirm B5VJ 24x2.5, carrier positions 0-23, the 8-slot rear and dual PSU configuration. The final rear now has the same validated structure and physical ratio as the identical 3.5-chassis rear configuration. All 32 feature-inventory rows pass against 24 matched-camera sheets in both engines and both GLBs.

Evidence entry points:

- `after/browser-gate-summary.json`
- `after/rotation-stress-report.json`
- `after/http-final-hash-audit.json`
- `after/structural-extra-standard.json` and `after/structural-extra-web.json`
- `after/matched-camera/comparison-manifest.json`
- `after/feature-inventory-verification.json`
- `after/rotation/<viewer>/<variant>/rotation-manifest.json`

Warnings/residual risk: none. Bottom is exact official-viewer evidence; no fallback is used.
