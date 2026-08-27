# Dell PowerEdge R7525 3.5-inch final independent review

Final classification: **PASS_WITH_BOTTOM_FALLBACK**

The exact-model/configuration, exterior structure, materials and rotation-stability gates pass. The only downgrade is the explicitly disclosed generic bottom; no non-bottom identity gap remains.

## Frozen deliverables

| Artifact | Previous SHA-256 | Final SHA-256 |
| --- | --- | --- |
| `model/Dell-R7525-3.5inch.glb` | `90ec6e7a3601ae8166132f35ae3e9e8a62e646d349a548e419658b848a62ffc0` | `f8f56c1c2dc8277d68d3ca26f47b04dc34c9124c8c266610391a4fdca03c09d9` |
| `model/Dell-R7525-3.5inch-web.glb` | `e8655c521bfd599aa073756107ee5c1046c4efbe5631d8f16f3673832665aa05` | `dd729a31166daa9bc6afca1facae7b3849faefab8996d3187206b066f4c433c9` |
| `qa/rotation-review/viewers/three.html` | — | `949b9bb2bb83b0a9668496cfb3ae986192b50e28151490011947447f4d181812` |
| `qa/rotation-review/viewers/babylon.html` | — | `957a34b4bed337545f0459eecba7f8e8b471f2b64aec8fa68b620c29673dac02` |

The installed envelope is exactly 482.0 x 86.8 x 772.13 mm. Right-handed orientation is +X device-right from the front, +Y up, +Z front.

## Authenticity result

- Verified R7525 E68S/E68S001, 2U, 12 x 3.5-inch/LFF front, Dell EMC LCD/security bezel, no rear drives, four riser groups/eight PCIe positions, BOSS S2/OCP areas and locked rear I/O.
- Two independently modeled 2400 W AC PSUs, visible fan/inlet faces and six hidden internal fan modules are retained. No DC connector or mixed PSU configuration exists.
- Rack ears, carriers, handles, lattice, controls, ports, fillers, labels and factory Dell EMC logo match the locked source inventory. Optional serial DB9 and rear-drive module remain explicitly absent.
- The 2026-08-27 source/public-3D recheck is recorded in `source-revalidation-20260827.md`. Dell has an official interactive service 3D listing, but exposes no downloadable exact exterior binary; there was no official file to preserve.

## Model root causes and causal repairs

1. The bezel LCD carried an invented readable IP address. It was replaced with a source-neutral dark display using a tightly bounded generated LCD interior; the full generated canvas was rejected for drift and preserved. See `imagegen-front-lcd-repair.md` and `model/repair-front-lcd.py`.
2. Cylinder side triangles had inward winding. `model/build-model.js` now emits consistent outward side winding.
3. The closed chassis core shared the exact top/bottom depth with source-locked face cards, creating a near-coplanar risk. Only the hidden core was inset by 0.12 mm; authoritative exterior cards and the exact overall 86.8 mm height were retained.

No lighting change was used to conceal geometry or material defects.

## Viewer factors, kept separate from model causes

The final Three.js and Babylon.js pages are independent WebGL2, right-handed orbit viewers with explicit loading state, bounded near/far planes, neutral tone mapping and shallow/deep light/dark checker views. An early Babylon independent-load screenshot batch captured an expired explicit-render buffer and produced empty checkerboards even though the model was loaded; that was a capture-timing defect, not a GLB defect. The batch was moved to `qa/superseded/pre-load-capture-refresh-20260827/`, the capture runner now requests an immediate explicit orbit render before every screenshot, and all 40 loads were rerun without changing either frozen viewer.

## Final QA evidence

- `views-audit.json`: PASS, 0 errors. Five source-PNG warnings are limited to transparent/anti-aliased silhouette pixels; the inspected core regions are opaque. Embedded GLB primary face images are fully opaque.
- `glb-standard-audit.json` and `glb-web-audit.json`: PASS, 0 errors and 0 warnings.
- For both standard and web: duplicate/coplanar, material-alpha, negative-transform and closed-core reports are PASS with 0 unresolved; reversed normals and degenerate triangles are also 0.
- Materials: every primary face is `OPAQUE`, neutral `[1,1,1,1]`, `doubleSided=false`; no primary chassis material uses BLEND or MASK. Source-photo faces use stable embedded PNGs and unlit treatment where appropriate.
- Independent loads: 40/40 at 1200 x 800; 10 views for each of Three/standard, Three/web, Babylon/standard and Babylon/web, each with unique cache bust and HTTP 200 model response. No page/model/load error remains.
- Rotation: each of the four engine/tier combinations has 72 distinct 5-degree yaw frames, 12 shallow/deep pitch/checker frames and 16 A/B stability frames at 600 x 400. All eight A/B pairs per combination are pixel-equal; all 72 yaw images per combination are unique.
- Every capture asserts WebGL2, right-handed camera state and hidden loading overlay. The bounded near/far ratio is 485.686 in both engines; serialized evidence queues and fixed 1200 x 800 / 600 x 400 resolutions prevent mixed-frame evidence.
- Primary faces are separately embedded, clamp-sampled images rather than a shared product atlas. Mipmapped rotation showed no edge/atlas bleed. Full yaw and shallow/deep checker contacts were visually reviewed with no z-fighting, flicker, transparent jump, checker leakage, face disappearance, mirroring, texture switch, gray/white jump or mask-frame mixing.
- Matched camera: 12 source/render/overlay/difference groups cover six faces in both engines. All 33 feature-inventory rows were reviewed in `feature-match-review.csv`. Visual contacts are in `comparison-review-contact.png`.
- The only runtime console notice is Chromium's screenshot-time `ReadPixels` performance warning (16 occurrences); it is capture-only and not a model/viewer correctness failure.

Machine-readable gate: `final-gate.json`. Frozen hashes: `frozen-hashes.json`. Load/rotation manifests: `manifests/`.

## Reproduction

From this model directory:

```bash
node model/build-model.js
node qa/rotation-review/scripts/audit-rotation-glb.mjs model/Dell-R7525-3.5inch.glb qa/rotation-review/final/standard
node qa/rotation-review/scripts/audit-rotation-glb.mjs model/Dell-R7525-3.5inch-web.glb qa/rotation-review/final/web
qa/imagegen-venv/bin/python qa/rotation-review/scripts/finalize-evidence.py .
```

The Playwright evidence runner requires a local HTTP server rooted at this model directory and an already opened Playwright CLI session; its exact flags and frozen hashes are recorded by `qa/rotation-review/scripts/run-playwright-evidence.mjs` and the manifests.

## Residual risk

The exact R7525 12LFF underside was not publicly available. The bottom is deliberately plain, closed and non-identifying; it does not borrow holes, labels or stampings from another model. This is the sole reason for `PASS_WITH_BOTTOM_FALLBACK`.
