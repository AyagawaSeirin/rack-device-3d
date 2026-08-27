# Dell C6300 + four PowerEdge C6320 2.5-inch rotation review — task 11

Final status: **PASS_WITH_BOTTOM_FALLBACK**

## Frozen deliverables

| Deliverable | SHA-256 |
|---|---|
| `models/Dell-PowerEdge-C6300-4xC6320-24SFF-standard.glb` | `7a109aa608a07c42cd8cb528416d82f3d23dc4bb1772d4181ae1a5be1eed5923` |
| `models/Dell-PowerEdge-C6300-4xC6320-24SFF-web.glb` | `42d92c055e3e086a7731669a509726d6a56d81d8191c04d19d07f3aaa0362858` |
| `qa/build_glb.py` | `467deebf4abdd75f7312039c8da09fdcd1c61ece615a20493c932b1b1b9c0a6c` |
| Three.js orbit viewer | `09397e305ac39f3a87af77d253a848eed6f0be8d163fa75d2b3580fc665a116a` |
| Babylon.js orbit viewer | `37ee630ebd49c0c28fb2a62c98f549b6112d099a41196d881f84e12a07347ca6` |
| Enhanced structure audit | `0db0161ba7674867a77ffc3029a52cfa142cf7088c5a19ee68f3f7c6641a9fb7` |

Frozen at `2026-08-27T16:09:00Z`. Freeze and post-evidence verification are in `final/frozen-hashes.json` and `final/freeze-verification.json`; all six records match after every final capture and report-generation step.

## Identity and authenticity

- Delivery subject: complete PowerEdge C6300 enclosure, B08S, 2U, with four standard two-socket C6320 sleds in all 2×2 rear positions; not C6320p and not a standalone sled.
- Front: 24 × 2.5-inch SFF, one vertical carrier row in four six-drive groups, no bezel, narrow non-usable cover and two control panels.
- Rear: four identical C6320 sleds; each exposes one PCIe blank/grille, USB 3.0, two embedded 10GbE SFP+, iDRAC8 RJ45, USB-to-serial, VGA and power/status. Two matching stacked 1400 W AC PSUs are at device physical right/rear viewer-left; HVDC, 1600 W and mixed pairs are excluded.
- Cooling: four shared internal fan-cage housings/rotors plus two source-photo PSU fan guards.
- Front-only ears and true open ring geometry are retained; no inferred rear ears.
- Genuine Dell and POWEREDGE C6320 factory markings come from the binding real photographs. The prior programmatically redrawn Dell/PowerEdge texture planes were removed.
- Exact world bounds are now 0.4823 × 0.0868 × 0.7959 m. The archived file was incorrectly authored 1000× larger.

Inventory verification: `final/inventory-verification/inventory-verification.json`, 40/40 rows plus 5/5 hard gates PASS for standard and web.

## Reproduction and causal root cause

The returned freeze was reproduced from the archived standard GLB with the enhanced audit. Its closed core bounds were X ±223.5, Y ±43.0 and Z ±397.5 mm. The front, left, right, top and bottom skins were inside that opaque core by 0.10–0.40 mm; the rear was outside by only 0.05 mm. The audit therefore reports all six skin-clearance checks as violations and finds 136 photo-related near-coplanar relationships. Both independent viewers showed the same gray top, while the embedded top image remained the correct silver photograph.

The root cause of this return was **the GLB model layer ordering, not the viewers**. The viewer files were not changed and no camera, culling, lighting or material override was added. Their frozen hashes remain `09397e…a116a` and `37ee63…47ca6`; both now expose the corrected photo skins under the same WebGL2, neutral-light, tone-mapping-off conditions.

The closed core is now 446.0 × 84.8 × 793.4 mm, with bounds X ±223.0, Y ±42.4 and Z ±396.7 mm. Actual skin clearances are front 0.40, rear 0.75, physical left 0.40, physical right 0.40, top 0.40 and bottom 0.40 mm, and all six normals point outward. Front coarse carrier/control bodies are behind the local source-photo planes with 0.25 mm clearance; fine latch/handle relief is 0.28 mm in front. Rear coarse node/PSU backing is behind the binding photograph, while verified fans, AC inlets, LEDs and orange releases remain in front. Side relief occupies X 223.8–224.0 mm outside the skins at ±223.4 mm. The top skin remains below its relief and the bottom fallback remains inside its perimeter lips without touching the core. The final 0.24 mm appearance-near-coplanar gate has zero records.

## Final WebGL2 evidence

- Four combinations; each has 72 × 5° yaw, 16 pitch and 16 stability frames with shallow/deep checkerboards.
- Total 416 rotation/pitch/stability frames. Same-angle maximum MAE is 0.0. Across all four combinations the maximum adjacent object-luma delta is 6.082 and the maximum adjacent silhouette-area delta is 0.00290; Three.js and Babylon.js agree.
- Forty cache-busted independent new-page loads all used WebGL2, matched frozen hashes, and had zero overlay/console errors.
- `final/frame-analysis/summary.json`: 4/4 PASS. `final/static-40-loads/load-run.json`: 40/40 PASS.
- `final/matched-camera/`: 24 captures and 24 source/render/overlay/difference sets. The rejected gray top is gone: Three/standard and Babylon/web top renders retain the silver source cover, folded edge, dimples and asymmetric pads. Front, rear, left and right source photographs are also externally visible. Difference panels mainly record intentional three-dimensional relief and the front-only mounting ears.
- `final/contact-sheets/`: 12 hash-bound sheets covering every combination's 72-yaw sequence, 16 pitch frames and 10 independent loads.

No final evidence shows flicker, transparency jumps, leakage, disappearance, mirroring, texture/gray switching or mask mixing.

## Audits

- Views audit: PASS, zero errors/warnings; six opaque cores are 0% transparent.
- Standard/web GLB audits: PASS, zero errors/warnings; bounds and units match exactly.
- Enhanced standard/web audits: zero duplicate, exact-coplanar, appearance-near-coplanar, material-alpha, negative-transform, normal/winding or closed-core errors; six of six skins pass the outward-core-clearance gate in both GLBs.
- Six main face materials are `OPAQUE`, `[1,1,1,1]`, `doubleSided=false`; no main chassis `BLEND`; closed core is watertight and positive-volume.

## Official model search and residual risk

No public official exact C6300 + four standard C6320 + 24 SFF model was found in the 2026-08-27 recheck. The Playwright CLI Dell dimensions route returned HTTP 403 and no model payload; evidence is under `research/playwright-dell/`. No C6320p or seller mesh was substituted.

The exact underside remains unavailable after documented official, browser-assisted and third-party searches. The conservative unbranded `GENERIC_BOTTOM_FALLBACK` is the only evidence exception, hence `PASS_WITH_BOTTOM_FALLBACK`.

Pre-repair material is preserved under `qa/superseded/pre-rotation-review-20260827/`. The rejected first post-freeze repair is under `qa/superseded/post-freeze-rejected-fidelity-20260827T1502Z/`. The returned occluded-skin freeze—including both GLBs, builder, viewers, tools, full `after/` and `final/` evidence and report—is preserved under `qa/superseded/post-freeze-rejected-occluded-skins-20260827T155907Z/`.
