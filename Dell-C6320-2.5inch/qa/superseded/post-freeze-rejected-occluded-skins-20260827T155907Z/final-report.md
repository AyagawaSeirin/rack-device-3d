# Dell C6300 + four PowerEdge C6320 2.5-inch rotation review — task 11

Final status: **PASS_WITH_BOTTOM_FALLBACK**

## Frozen deliverables

| Deliverable | SHA-256 |
|---|---|
| `models/Dell-PowerEdge-C6300-4xC6320-24SFF-standard.glb` | `29975a62fd6474f1c503de5f0c085fd7e089b8b95502e08a49487e3e96cb37af` |
| `models/Dell-PowerEdge-C6300-4xC6320-24SFF-web.glb` | `7cffab1497dfa4df16bc5c1312e6956e91f14038bb94c8ae0ddc413fcb99279b` |
| `qa/build_glb.py` | `3499b4853b405ba17c5ef68fa7bbec8929f0cac80f9ebab174dfd9b34e1005c3` |
| Three.js orbit viewer | `09397e305ac39f3a87af77d253a848eed6f0be8d163fa75d2b3580fc665a116a` |
| Babylon.js orbit viewer | `37ee630ebd49c0c28fb2a62c98f549b6112d099a41196d881f84e12a07347ca6` |

Freeze and post-evidence verification are in `final/frozen-hashes.json` and `final/freeze-verification.json`; all five records match.

## Identity and authenticity

- Delivery subject: complete PowerEdge C6300 enclosure, B08S, 2U, with four standard two-socket C6320 sleds in all 2×2 rear positions; not C6320p and not a standalone sled.
- Front: 24 × 2.5-inch SFF, one vertical carrier row in four six-drive groups, no bezel, narrow non-usable cover and two control panels.
- Rear: four identical C6320 sleds; each exposes one PCIe blank/grille, USB 3.0, two embedded 10GbE SFP+, iDRAC8 RJ45, USB-to-serial, VGA and power/status. Two matching stacked 1400 W AC PSUs are at device physical right/rear viewer-left; HVDC, 1600 W and mixed pairs are excluded.
- Cooling: four shared internal fan-cage housings/rotors plus two source-photo PSU fan guards.
- Front-only ears and true open ring geometry are retained; no inferred rear ears.
- Genuine Dell and POWEREDGE C6320 factory markings come from the binding real photographs. The prior programmatically redrawn Dell/PowerEdge texture planes were removed.
- Exact world bounds are now 0.4823 × 0.0868 × 0.7959 m. The archived file was incorrectly authored 1000× larger.

Inventory verification: `final/inventory-verification/inventory-verification.json`, 40/40 rows plus 5/5 hard gates PASS for standard and web.

## Reproduction and root cause

The archived GLBs contained 39 exterior same-facing coplanar overlaps, 0.01–0.05 mm photo/label layers, a 1000× world-unit error, and physical left/right nodes reversed relative to the declared +X convention. The old viewers compensated with reversed camera labels and used a 0.1–10000 range, worsening precision. The first repaired freeze was also rejected because coarse solid rear sled blocks obscured the binding photograph; that build and evidence were archived rather than accepted.

Root cause was **both model and viewer convention**, with the model dominant: incorrect units/layering/orientation and synthetic duplicate branding; viewer camera labels and clipping then masked the error. Repair converts authored millimetres to glTF metres, restores physical left=-X/right=+X, separates card/core/relief layers, places coarse rear structure behind the real source-photo skin, keeps only fine PSU/LED relief in front, removes synthetic logo/label planes, and establishes dynamic near/far ratio 120. Lighting is neutral and cannot hide the issue; face textures are unlit and tone mapping/post-processing are off.

## Final WebGL2 evidence

- Four combinations; each has 72 × 5° yaw, 16 pitch and 16 stability frames with shallow/deep checkerboards.
- Total 416 rotation/stability frames. Same-angle maximum MAE is 0.0. The gray body approaches the light checker and makes diagnostic object segmentation conservative in Three.js, but unsegmented adjacent full-frame MAE remains only 3.08 and Babylon agrees; no real gray jump exists.
- Forty cache-busted independent new-page loads all used WebGL2, matched frozen hashes, and had zero overlay/console errors.
- `final/frame-analysis/summary.json`: 4/4 PASS. `final/static-40-loads/load-run.json`: 40/40 PASS.
- `final/matched-camera/`: 24 captures and 24 source/render/overlay/difference sets. The final rear again preserves exact four-sled port/PSU photography instead of flat generic blocks.

No final evidence shows flicker, transparency jumps, leakage, disappearance, mirroring, texture/gray switching or mask mixing.

## Audits

- Views audit: PASS, zero errors/warnings; six opaque cores are 0% transparent.
- Standard/web GLB audits: PASS, zero errors/warnings; bounds and units match exactly.
- Enhanced standard/web audits: zero duplicate, coplanar, material-alpha, negative-transform, normal/winding or closed-core errors.
- Six main face materials are `OPAQUE`, `[1,1,1,1]`, `doubleSided=false`; no main chassis `BLEND`; closed core is watertight and positive-volume.

## Official model search and residual risk

No public official exact C6300 + four standard C6320 + 24 SFF model was found in the 2026-08-27 recheck. The Playwright CLI Dell dimensions route returned HTTP 403 and no model payload; evidence is under `research/playwright-dell/`. No C6320p or seller mesh was substituted.

The exact underside remains unavailable after documented official, browser-assisted and third-party searches. The conservative unbranded `GENERIC_BOTTOM_FALLBACK` is the only evidence exception, hence `PASS_WITH_BOTTOM_FALLBACK`.

Pre-repair material is preserved under `qa/superseded/pre-rotation-review-20260827/`. The rejected first post-freeze repair and its full evidence are preserved under `qa/superseded/post-freeze-rejected-fidelity-20260827T1502Z/`.
