# HPE DL360 Gen10 2.5-inch final independent review

Final classification: **PASS_WITH_BOTTOM_FALLBACK**

The exact 1U/8SFF configuration, exterior structure, material and two-engine rotation gates pass. The only downgrade is the disclosed generic bottom; no non-bottom identity gap remains.

## Frozen deliverables

| Artifact | Previous SHA-256 | Final SHA-256 |
| --- | --- | --- |
| `model/HPE-DL360G10-2.5inch.glb` | `36fba895befbc28185d3aeeea77c84315812fb14863fe54ca3231cb1d0e12597` | `aaabe38a87552e0a51f3bd3392a324884134f5a10c255967ecc8fb58b766f313` |
| `model/HPE-DL360G10-2.5inch-web.glb` | `785c9a0824eccb823b5be0036ea970161df776dc40312556d87151e6d4275900` | `6785a8a4f21ed5bb9ce741a17b7d2dc465d3dd0c033bfd20c488f181456bc72e` |
| `qa/rotation-review/viewers/three.html` | — | `949b9bb2bb83b0a9668496cfb3ae986192b50e28151490011947447f4d181812` |
| `qa/rotation-review/viewers/babylon.html` | — | `957a34b4bed337545f0459eecba7f8e8b471f2b64aec8fa68b620c29673dac02` |

Final bounds are 482.6 x 42.925 x 707.02 mm, matching the 482.6 mm rack-ear span and the official 434.6 x 42.9 x 707.0 mm SFF body within audit tolerance. Right-handed orientation is +X device-right from the front, +Y up, +Z front.

## Authenticity result

- Verified ProLiant DL360 Gen10 standard 8SFF 2.5-inch 6+2 arrangement, not 4LFF/8+2SFF/10SFF and not Gen10 Plus/Gen11/Gen12.
- Front carriers, UMB/control area, rack ears, top/side sheet metal, rear port/blank order and factory HPE marks match the locked inventory.
- Two independent 500 W Flex Slot AC PSU modules and their fans/inlets are retained; no DC or mixed configuration exists.
- The 2026-08-27 official source/public-3D recheck is in `source-revalidation-20260827.md`. No public official exact 8SFF 3D binary was found, so there was no official file to preserve.

## Model root causes and causal repairs

1. Cylinder side triangles had inward winding; `model/build-glb.mjs` now emits outward side winding.
2. Rack-ear face holes were represented through a MASK face rather than stable geometry. The ear face is now an OPAQUE geometric ring with a real open center; no main chassis face depends on alpha masking.
3. PSU frame strips overlapped one another and sat too close to the rear source card. `work/geometry/repair_source_texture_relief.py` now produces non-overlapping strips and a deterministic 0.05 mm separation.
4. Colored relief used unnecessary unlit materials and generated audit noise. Only authoritative photo textures remain unlit; colored relief is ordinary OPAQUE PBR.
5. The deterministic relief repair pass is invoked by `model/build-glb.mjs`, so one build command reproduces the final deliverables.

No lighting change was used to conceal a defect.

## Viewer factors, kept separate from model causes

The prior QA viewer set did not provide independent Three.js and Babylon.js renderers. It was replaced by two frozen WebGL2, right-handed orbit viewers with loading-state checks, bounded near/far planes, neutral tone mapping and checker views. An early Babylon load-screenshot batch captured an expired explicit-render buffer; the actual rotation atlas was never blank. The invalid batch was moved to `qa/superseded/pre-load-capture-refresh-20260827/`, the capture runner now asks the viewer to render immediately before screenshot, and all 40 loads were rerun without changing the frozen viewers.

## Final QA evidence

- `views-audit.json`: PASS, 0 errors. Six warnings are limited to canonical PNG silhouette/anti-alias transparency and were visually checked; embedded GLB primary face images are opaque.
- `glb-standard-audit.json` and `glb-web-audit.json`: PASS, 0 errors and 0 warnings.
- Both tiers: duplicate/coplanar, material-alpha, negative-transform and closed-core PASS with 0 unresolved; reversed normals and degenerate triangles are 0.
- Every primary face is `OPAQUE`, `[1,1,1,1]`, `doubleSided=false`; no primary chassis BLEND/MASK material remains.
- Independent loads: 40/40 at 1200 x 800, unique cache bust and HTTP 200 model response for all 2 viewers x 2 GLBs x 10 views; no page/model/load error remains.
- Rotation: every engine/tier combination has 72 unique 5-degree yaw frames, 12 shallow/deep pitch/checker frames and 16 A/B frames at 600 x 400. All repeated A/B images are pixel-equal.
- Every capture asserts WebGL2, right-handed camera state and hidden loading overlay. The bounded near/far ratio is 485.686 in both engines; serialized queues and fixed 1200 x 800 / 600 x 400 resolutions prevent evidence mixing.
- Primary faces use separate clamp-sampled images, not a shared product atlas. Mipmapped rotation showed no edge/atlas bleed. Full yaw and shallow/deep checker contacts were visually reviewed with no z-fighting, flicker, transparent jump, checker leakage, face disappearance, mirroring, texture switch, gray/white jump or mask-frame mixing.
- Matched camera: 12 six-face/two-engine source/render/overlay/difference groups. All 31 feature-inventory rows were reviewed in `feature-match-review.csv`; `comparison-review-contact.png` is the review contact.
- The only console notice counted by the gate is Chromium's screenshot-time `ReadPixels` performance warning (12 occurrences), not a model/viewer correctness issue.

Machine-readable gate: `final-gate.json`. Frozen hashes: `frozen-hashes.json`. Load/rotation manifests: `manifests/`.

## Reproduction

From this model directory:

```bash
node model/build-glb.mjs
node qa/rotation-review/scripts/audit-rotation-glb.mjs model/HPE-DL360G10-2.5inch.glb qa/rotation-review/final/standard
node qa/rotation-review/scripts/audit-rotation-glb.mjs model/HPE-DL360G10-2.5inch-web.glb qa/rotation-review/final/web
work/venv/bin/python qa/rotation-review/scripts/finalize-evidence.py .
```

The Playwright runner requires a local HTTP server rooted here and an opened Playwright CLI session; exact arguments, cache-bust values and hashes are recorded by `qa/rotation-review/scripts/run-playwright-evidence.mjs` and the manifests.

## Residual risk

No identity-bearing exact DL360 Gen10 SFF underside was available. The bottom is intentionally a plain, closed galvanized fallback without borrowed holes, labels or stampings. This is the sole reason for `PASS_WITH_BOTTOM_FALLBACK`.
