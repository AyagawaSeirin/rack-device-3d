# HPE DL360 Gen9 3.5-inch final independent review

Final classification: **PASS_WITH_BOTTOM_FALLBACK**

The exact Gen9 4LFF installed configuration, exterior structure, materials and rotation-stability gates pass. The only downgrade is the disclosed generic bottom; no non-bottom identity gap remains.

## Frozen deliverables

| Artifact | Previous SHA-256 | Final SHA-256 |
| --- | --- | --- |
| `model/HPE-DL360G9-3.5inch.glb` | `cdc9a32363bf2cfcdfa3027533c9dbaca4fb897c62d325bdef7affa47bd39b04` | `08b5bb28fa61f21b73d56c7280fcd202c03db4346c49ba417a12af50babfaf6f` |
| `model/HPE-DL360G9-3.5inch-web.glb` | `b2dbde391730bd77a86813a803f3e68201c532f6ea5664ba2f558e348426531e` | `d80090ead95a1f3de27369633c1ad265dd44eae7409cf7d148442f33a9aa5f96` |
| `qa/rotation-review/viewers/three.html` | — | `949b9bb2bb83b0a9668496cfb3ae986192b50e28151490011947447f4d181812` |
| `qa/rotation-review/viewers/babylon.html` | — | `957a34b4bed337545f0459eecba7f8e8b471f2b64aec8fa68b620c29673dac02` |

Final bounds are 482.6 x 43.2 x 770.06 mm. The 434.6 x 43.2 x 750.0 mm official 4LFF body is preserved, with only source-measured front carrier/rear PSU-handle projections. Right-handed orientation is +X device-right from the front, +Y up, +Z front.

## Authenticity result

- Verified DL360 Gen9 4LFF/3.5-inch, one row of four installed carriers, exact 4LFF control strip, period factory marks and independent rack ears; no SFF or later-generation front was used.
- Rear PCIe blank/slot positions, 4x1GbE FlexibleLOM, USB/serial/iLO/NIC/VGA order and dual PSU layout match current HPE component identification plus the locked exact rear render.
- Two independently modeled 500 W Flex Slot AC PSUs and seven internal hot-plug fan modules are retained. No DC PSU or alternate rear adapter is mixed in.
- The 2026-08-27 source/public-3D recheck is recorded in `source-revalidation-20260827.md`. No public official exact 4LFF 3D binary was found, so there was no official file to preserve.

## Model root causes and causal repairs

1. PCIe slot-1 relief overlapped slot-2 by about 8 mm. Its width was reduced to the source-locked aperture span, eliminating duplicate/coplanar expression while retaining three distinct PCIe positions.
2. The top source card and hidden core/top relief shared or exceeded the official height envelope. The top source card is now 0.12 mm clear of the core, the bottom remains exactly at -21.6 mm, and top seam/vent relief is constrained inside the 43.2 mm height.
3. The installed bounds now retain the official body and measured carrier/PSU projections without nonuniform scale inflation.

No lighting change was used to hide a defect.

## Viewer factors, kept separate from model causes

The final evidence uses independent Three.js and Babylon.js WebGL2 right-handed viewers with orbit control, loading-state assertions, bounded near/far planes, neutral tone mapping and checker backgrounds. An early Babylon independent-load screenshot batch captured after the explicit-render buffer became unavailable; the model and rotation atlas were valid. That batch was preserved under `qa/superseded/pre-load-capture-refresh-20260827/`; the runner now requests an immediate render before screenshot and all 40 loads were rerun with unchanged frozen viewers.

## Final QA evidence

- `views-audit.json`: PASS, 0 errors. Six canonical source-PNG transparency warnings are limited to silhouette/anti-alias regions and were visually inspected; embedded main-face images are opaque.
- `glb-standard-audit.json` and `glb-web-audit.json`: PASS, 0 errors and 0 warnings.
- Both tiers: duplicate/coplanar, material-alpha, negative-transform and closed-core PASS with 0 unresolved; reversed normals and degenerate triangles are 0.
- Every primary face is `OPAQUE`, `[1,1,1,1]`, `doubleSided=false`; the main chassis has no BLEND/MASK material.
- Independent loads: 40/40 at 1200 x 800, unique cache bust and HTTP 200 for every 2-viewer x 2-GLB x 10-view combination; no page/model/load error remains.
- Rotation: each of four combinations has 72 unique 5-degree yaw frames, 12 shallow/deep pitch/checker frames and 16 A/B frames at 600 x 400. All repeated A/B images are pixel-equal.
- Every capture asserts WebGL2, right-handed camera state and hidden loading overlay. The bounded near/far ratio is 485.686 in both engines; serialized queues and fixed 1200 x 800 / 600 x 400 resolutions prevent evidence mixing.
- Primary faces use separate images rather than a shared product atlas. Rotation across minified views showed no edge/atlas bleed. Full yaw and shallow/deep checker contacts were visually reviewed with no z-fighting, flicker, transparent jump, checker leakage, face disappearance, mirroring, texture switch, gray/white jump or mask-frame mixing.
- Matched camera: 12 source/render/overlay/difference groups cover six faces in both engines. All 23 feature-inventory rows were reviewed in `feature-match-review.csv`; the review contact is `comparison-review-contact.png`.
- The only console notice counted by the gate is Chromium's screenshot-time `ReadPixels` performance warning (10 occurrences), not a model/viewer correctness error.

Machine-readable gate: `final-gate.json`. Frozen hashes: `frozen-hashes.json`. Load/rotation manifests: `manifests/`.

## Reproduction

From this model directory:

```bash
PYTHONPATH=qa/python-deps python3 model/build_model.py --profile both
node qa/rotation-review/scripts/audit-rotation-glb.mjs model/HPE-DL360G9-3.5inch.glb qa/rotation-review/final/standard
node qa/rotation-review/scripts/audit-rotation-glb.mjs model/HPE-DL360G9-3.5inch-web.glb qa/rotation-review/final/web
PYTHONPATH=qa/python-deps python3 qa/rotation-review/scripts/finalize-evidence.py .
```

`qa/python-deps` supplies NumPy, Pillow, pygltflib and trimesh for the recorded build environment. The Playwright runner requires a local HTTP server rooted here and an opened Playwright CLI session; exact arguments and cache-bust values are in `qa/rotation-review/scripts/run-playwright-evidence.mjs` and the manifests.

## Residual risk

No exact identity-bearing DL360 Gen9 4LFF underside was available. The bottom is deliberately plain and closed; no DL120 holes, feet, labels or stampings were copied. This is the sole reason for `PASS_WITH_BOTTOM_FALLBACK`.
