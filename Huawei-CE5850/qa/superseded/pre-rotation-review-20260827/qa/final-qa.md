# Final QA — Huawei CE5850-EI-B00

Final status: **PASS_WITH_BOTTOM_FALLBACK**

Review date: 2026-08-23  
Scope: only `Huawei-CE5850/`

## Delivery identity

| Field | Locked value | Result |
|---|---|---|
| Part number | `02359104` | PASS |
| Complete bundle | `CE5850-EI-B00` | PASS |
| Chassis PID | `CE5850-48T4S2Q-EI` | PASS |
| Port inventory | 48 x GE RJ45; 4 x 10GE SFP+; 2 x 40GE QSFP+ | PASS |
| Installed power/fans | 2 x PAC-150WA AC; 2 x FAN-40EA-F | PASS |
| Airflow | power-side intake; port-side exhaust | PASS |
| Branding | factory Huawei logo/model marking retained | PASS |
| Canonical orientation | port side = front / `+Z`; `+X` device right; `+Y` up | PASS |

The EI chassis is not substituted with the nearby HI model. No DC power module is present.

## Final files

| Deliverable | Bytes | SHA-256 |
|---|---:|---|
| `model/Huawei-CE5850-48T4S2Q-EI-B00.glb` | 13,271,532 | `95b8405d072e9cbdcce30b78be723fa2baef75c68464ea4e05d6f7fd9e75db1c` |
| `model/Huawei-CE5850-48T4S2Q-EI-B00-web.glb` | 7,251,648 | `d64f0ec516b486631e64bd143e2be6ec1a3f5ec0f784add7cae675fd87b704d4` |

The approved six face PNGs remain under `views/`. Their source modes and SHA-256 lineage are recorded in `source/face-source-lock.csv`; no approved face was regenerated during the final WebGL continuation.

## Structural audits

Both `qa/glb-standard-audit.json` and `qa/glb-web-audit.json` pass with:

- bounds: `482.6 x 43.6 x 420.0 mm` exactly after millimeter normalization;
- 1 scene, 185 nodes, 167 meshes, 167 primitives;
- 15 materials, 6 textures, 6 embedded images;
- no mirrored nodes or missing accessor bounds;
- six source-face materials are `OPAQUE`, unlit, neutral base color, and not double-sided;
- no external buffers/resources;
- error count `0`, warning count `0`.

The existing six-view audit `qa/views-audit.json` remains `PASS` with error count `0` and warning count `0`.

## Independent WebGL live loads

The dedicated CE5850 service used `127.0.0.1:9027`. Port `8765`, which belonged to another model viewer, was not reused or stopped.

Two independent named browser sessions and viewer implementations were used:

1. `ce5850-three-9027` — Three.js `GLTFLoader`
2. `ce5850-babylon-9027` — Babylon.js `SceneLoader`

Each session loaded both the standard and web GLB through HTTP and captured all ten cameras: front, rear, left, right, top, bottom, front-left, front-right, rear-left, and rear-right. This produced 40 final 1600 x 1000 live-load screenshots. Every row in `qa/checklists/webgl-live-load.csv` is `PASS`.

Final live checks confirmed:

- `document.body.dataset.ready = true` and no loader error;
- active WebGL canvas in both sessions;
- the web GLB transferred as the expected 7,251,648-byte resource in both viewers;
- Babylon right-handed mode enabled and all imported textures ready before capture;
- zero application/loader console errors in both final sessions.

Earlier screenshot operations could emit non-failing GPU readback performance warnings from headless Chromium; these were not loader, model, or material errors.

## Six orthographic and four oblique comparisons

Ten viewer/model matrices are in `qa/comparisons/` and contain:

- Three.js standard;
- Babylon.js standard;
- Three.js web;
- Babylon.js web.

Ten source/reference matrices are in `qa/comparisons/source-reference/`:

- six orthographic matrices compare the approved canonical PNG with all four actual-GLB render paths;
- canonical front-left/front-right compare against Huawei official `rear_left/rear_right` exact-EI photographs;
- canonical rear-left/rear-right compare against Huawei official `front_top` power-side evidence, with the approved asymmetric side views supplying the adjacent-face constraint.

Feature-by-feature review passed for Huawei/model placement, 48/4/2 port order, EI-without-HI-breakout indicators, dual PAC-150WA, dual FAN-40EA-F, management block, right-only grounding mark, top perforated band, separate rack ears, normal text orientation, and closed exterior.

Standard-versus-web screenshot RMSE was measured for all ten cameras in each viewer. The largest normalized value was `0.00630306`; no silhouette, orientation, component-count, branding, or readable identity feature was lost.

## Defects found and repaired during live QA

### Babylon first-frame / coordinate issue

The original Babylon validation page rendered once immediately after `AppendAsync`, before embedded textures were GPU-ready, and used Babylon's default left-handed scene. It could therefore show only underlying geometry and swap canonical left/right interpretation.

Repair in `qa/viewers/babylon.html`:

- enable `scene.useRightHandedSystem = true`;
- await `scene.whenReadyAsync()` before rendering and setting `ready`;
- expose a loader error through `data-error`.

This was a QA-viewer defect; the GLBs were not changed for it.

### Coplanar shell / face-card depth competition

The first four-oblique matrix revealed large jagged triangular regions on top/side surfaces in both viewers. The closed shell and source-locked top/bottom/side cards were coplanar.

Repair in `source/build-model.mjs`:

- inset the closed internal shell by 0.2 mm behind each top/bottom/side face card;
- keep the external face cards at the verified body envelope;
- move the 48 RJ45 dark-cavity relief 0.05 mm inward so overall depth remains exactly 420.0 mm.

Both GLBs were rebuilt, structurally re-audited, and all 40 screenshots were recaptured. No depth competition remains in any orthographic or oblique matrix. Pre-repair GLBs, audits, renders, and matrices are retained under `qa/repairs/pre-webgl-zfight/`.

## Source lineage, bottom exception, and optional official model

- Identity manifest: `source/identity-manifest.md`
- Dimension ledger: `source/dimension-ledger.md`
- Evidence/search log: `source/evidence.md`
- Face locks: `source/face-source-lock.csv`
- Visible-feature inventory: `source/feature-inventory.csv`
- Normalized selected-generation record: `qa/imagegen-prompts/selected-output-record.md`
- Feature acceptance checklist: `qa/checklists/feature-verification.csv`

No exact public downloadable Huawei 3D/CAD model was found. Huawei Info-Finder reported null public 3D URLs; the available Visio package is not 3D. See `source/optional-3d/README.md`.

Exact-model underside imagery was not found after the documented official and third-party search. The conservative blank underside remains `GENERIC_BOTTOM_FALLBACK`; it introduces no unsupported identifying feature and changes no verified silhouette. This is the sole reason the final status is `PASS_WITH_BOTTOM_FALLBACK` rather than ordinary `PASS`.

## Acceptance

All remaining continuation gates are closed:

- standard GLB: PASS;
- web GLB: PASS;
- two independent WebGL viewers: PASS;
- six orthographic views: PASS;
- four oblique views: PASS;
- exact dimensions: PASS;
- identity, Logo, all-AC installed configuration, and port-side exhaust: PASS;
- public official exact 3D search record: complete;
- final model status: **PASS_WITH_BOTTOM_FALLBACK**.
