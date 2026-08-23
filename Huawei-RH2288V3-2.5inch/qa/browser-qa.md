# Independent browser-viewer QA

Date: 2026-08-23

The repository-local HTTP viewer was exercised with a real Chromium browser through Playwright. A headed launch was attempted first, but the execution environment has no X server; the same browser and WebGL checks were therefore completed headlessly. This is an execution-environment fallback, not a rendering shortcut.

## Viewers

- Three.js: `qa/viewers/three.html`
- Babylon.js: `qa/viewers/babylon.html`
- Standard GLB and web GLB both reached `document.body.dataset.ready = 1` in both engines.
- Babylon's loader overlay was explicitly disabled after an early QA capture showed that the overlay could obscure an already-loaded scene.
- Final atomic Playwright capture waits for ready state before every screenshot.

Vendor JavaScript was copied byte-for-byte from the already vendored project-local Juniper-MX204 viewer assets; it is code-only reuse and contains no sibling model, texture or AI image:

- `GLTFLoader.js`: `6f1719dcc6a179d30273dfb0de07a8c898a7981f7b08e600b446387f5967371f`
- `three.module.js`: `0a3368c165eea773490aec7b77c22de70e3eac288503409256fdbf4d12578416`
- `babylon.js`: `873f60ec6665d0de1a030918a194eb70e12937e5f93ae23107e1cffb1bdf29d8`
- `babylonjs.loaders.min.js`: `9f7b1a7a52f1e9649614992c7e41c5cde287fc3f07ca6d6f6119a21daf2132d0`
- `BufferGeometryUtils.js`: `c25b7930e570e9ec56173cd3b866ec8d2e10016630db3937efb439daf1cedbf6`

## Final capture sets

- Three.js web: six orthographic plus four three-quarter views under `qa/output/playwright/three-web-*.png`.
- Babylon.js web: the same ten views under `qa/output/playwright/babylon-web-*.png`.
- Standard model cross-check: front, rear, front-left and rear-right in both engines under `qa/output/playwright/*-standard-*.png`.

Comparison sheets:

- `qa/comparisons/three-web-six-orthographic.png`
- `qa/comparisons/three-web-four-perspective.png`
- `qa/comparisons/babylon-web-six-orthographic.png`
- `qa/comparisons/babylon-web-four-perspective.png`
- `qa/comparisons/standard-two-engine-cross-check.png`
- `qa/comparisons/authoritative-three-quarter-vs-render.png`
- `qa/comparisons/six-orthographic-source-vs-render.png`

Final visual review found no missing texture, cross-origin failure, mirrored node, open chassis shell, duplicated side vent, top-face duplicate relief, or persistent loading overlay. Left/right remain byte-distinct and visually distinct.

## Post-ImageGen-front-repair rerun

After replacing the temporary rectified-photo front and rebuilding both GLBs, the complete matrix was rerun rather than spot-checked:

- Three.js standard: 10/10 views under `repair-imagegen-front/renders/three/standard/`.
- Three.js web: 10/10 views under `repair-imagegen-front/renders/three/web/`.
- Babylon.js standard: 10/10 views under `repair-imagegen-front/renders/babylon/standard/`.
- Babylon.js web: 10/10 views under `repair-imagegen-front/renders/babylon/web/`.

All 40 files are non-empty. Visual review of `repair-imagegen-front/comparisons/three-standard-contact.png`, `babylon-web-contact.png` and `front-two-engine-two-variant.png` confirms the repaired 24-carrier front, correct asymmetric ear controls, stacked-AC-PSU rear and matching standard/web output in both engines. No loading overlay survived into any final capture.
