# Rotation and exact-appearance re-review — Lenovo ThinkSystem SR655 12x3.5

Final status: **PASS**  
Review date: 2026-08-27  
Delivery subject: original-generation Lenovo ThinkSystem SR655, types 7Y00/7Z01, B5VK/AUR9 12x3.5-inch front, PCIe-rich 8-slot rear, no rear drives, two 750W AC PSUs.

## Hash transition

| GLB | Pre-review SHA-256 | Final SHA-256 | Final bytes |
|---|---|---|---:|
| standard | `bc4abc301d051b8396943855464c941993854cde23c4a6ad74f140a7545446f6` | `2a8925f1eb08f5fe67df99cac62bcfdcb823bc60ef152d710ab0dec0df59bb97` | 11,098,780 |
| web | `a7d9015d1a7a564acac7cab1ce497a1d1b11ca6f7053febeebc1a535916dbd3f` | `632af251f3d568340933e357eb425cf7d1e94b5727dc3400c8dc83b9031f3868` | 7,902,232 |

The complete pre-review GLBs, build/viewer code, six views, audits, loads, comparisons and reports are preserved under `qa/superseded/pre-rotation-review-20260827/`. A rejected intermediate that exposed solid white top stampings is preserved separately under `qa/superseded/rotation-review-after-white-top-20260827/` and is not a final result.

## Reproduction and root cause

The pre-review standard and web GLBs contained **162** photographic-surface/geometry pairs separated by at most 0.25 mm in each file. Several carrier and PCIe frame bars also overlapped at their corners, while handles/dividers shared the same outward depth plane. This was a deterministic z-buffer risk during orbit even though not every 5-degree sample produced a full missing face. The prior PASS did not include a continuous rotation stress gate.

Root cause: insufficient depth hierarchy between the six opaque photographic skins, the closed chassis/core and visible relief. Lighting was not the cause and was not used to mask the defect.

## Repair

- Inset the watertight chassis core behind the evidence-locked skins without changing the published final bounds.
- Establish stable ordered depth for photographic skins, frames, handles, dividers and relief; eliminate frame-corner overlap by shortening side bars between top/bottom bars.
- Remove duplicate full top/bottom cover plates. Shallow top stampings remain in the exact source-locked photograph because they do not alter the target-view silhouette; the genuinely projecting latch remains geometry.
- Keep all six main materials `OPAQUE`, neutral `[1,1,1,1]`, `doubleSided=false`; keep six photo materials `KHR_materials_unlit`.
- Apply the identical visible geometry to standard and web. Their geometry signature is `cea8cba1cbc8f50c0edfb722ee8613cdb444035ccdd0553091906dae4db7b90e`.

## Structural gates

- `audit_views.py`: PASS, 0 errors; six warnings are anti-aliased exterior edges, with zero transparent/partial-alpha core pixels.
- `audit_glb.py`: standard PASS 0/0 errors/warnings; web PASS 0/0.
- Final bounds: 482.0 x 86.5 x 764.7 mm.
- 184 nodes/meshes/primitives, 16 materials, six independent embedded RGB textures.
- Exact duplicate triangles: 0; near-coplanar photographic pairs <=0.25 mm: 162 -> 0; negative transforms: 0; material-alpha errors: 0.
- `ChassisBody`: watertight, winding-consistent, positive volume.

## Real-browser gates

Frozen viewer code: Three.js r169 and Babylon.js 9.22.0, both verified WebGL2.

| Viewer / GLB | 5-degree yaw frames | Continuous animation frames | Dark-checker pitch frames | Result |
|---|---:|---:|---:|---|
| Three / standard | 72 | 95 | 8 | PASS |
| Three / web | 72 | 89 | 8 | PASS |
| Babylon / standard | 72 | 38 | 8 | PASS |
| Babylon / web | 72 | 39 | 8 | PASS |

Final-hash HTTP audit proves 44 unique GLB responses: 40 required static loads plus four rotation loads. The 40 static captures cover 2 viewers x 2 GLBs x 10 views and all pass. Visual review found no surface flicker, transparency jump, checkerboard leakage, face disappearance, mirroring, texture switch or sudden gray state.

## Exact appearance

The 2026-08-27 refresh confirmed the current official Lenovo SR655 tour and LP1161 original-generation identity. The final model retains the exact 3x4 LFF carrier layout, left VGA/ThinkSystem latch, right I/O/SR655 latch, 3+3+2 rear PCIe banks, OCP/BMC/VGA/USB/serial order, dual 750W AC PSUs, asymmetric physical sides, service-label top and official-viewer underside. All 39 feature-inventory rows pass against 24 final-hash matched-camera source/render/overlay/difference sheets.

Evidence entry points:

- `after/browser-gate-summary.json`
- `after/rotation-stress-report.json`
- `after/http-final-hash-audit.json`
- `after/structural-extra-standard.json` and `after/structural-extra-web.json`
- `after/matched-camera/comparison-manifest.json`
- `after/feature-inventory-verification.json`
- `after/rotation/<viewer>/<variant>/rotation-manifest.json`

Warnings/residual risk: none. Bottom is exact official-viewer evidence; no fallback is used.
