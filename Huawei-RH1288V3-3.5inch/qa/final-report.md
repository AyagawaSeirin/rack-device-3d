# Huawei RH1288 V3 3.5-inch exact-exterior GLB final report

Final status: **PASS_WITH_BOTTOM_FALLBACK**

Completed: 2026-08-23

Scope: `Huawei-RH1288V3-3.5inch/` only. No Git commit or push was made.

## Frozen delivery identity

- Manufacturer/product: Huawei FusionServer RH1288 V3, official nameplate model H12M-03.
- Delivery subject: complete 1U appliance, 4 x 3.5-inch LFF front, four closed factory carrier faces, no security bezel.
- Rear configuration: four-GE SM212-visible exterior, one management RJ45, two USB 3.0, VGA, serial, UID, full-height and half-height perforated PCIe blanks.
- Power: two matched 460 W 80 Plus Platinum hot-swap AC PSUs in 1+1 redundancy. No DC/HVDC or mixed PSU type.
- Rack hardware: verified front ears only; no rear-ear geometry.
- Branding: real Huawei wordmark, RH1288 V3 model mark and Intel Xeon badge are retained as product details.
- Published LFF body dimensions: 436 x 748 x 43 mm; nominal front-ear span 482.6 mm.

The frozen identity and configuration are recorded in `source/identity-manifest.md`, `source/dimension-ledger.csv`, `source/feature-inventory.csv`, and `source/evidence.md`.

## Final GLBs

| Deliverable | Bytes | SHA-256 |
|---|---:|---|
| `model/Huawei-RH1288V3-3.5inch.glb` | 8,101,412 | `c21ff62d34ee592364bd4fd8634a6bc2f8fb30e099985fa8b10540bc3ffb35bc` |
| `model/Huawei-RH1288V3-3.5inch-web.glb` | 5,372,668 | `af81151cbcb35e22161b351ba783b3b86cc426d4a3fa20b31c1510f855518cb6` |

The two pre-final-repair backups remain unchanged under `qa/repair-before-pass2/`:

| Backup | Bytes | SHA-256 |
|---|---:|---|
| `qa/repair-before-pass2/Huawei-RH1288V3-3.5inch.glb` | 8,103,408 | `30a2478cb82509f343bd876face4625996e47af5231a1a8186e787c519634ab3` |
| `qa/repair-before-pass2/Huawei-RH1288V3-3.5inch-web.glb` | 5,374,664 | `034e1d5e8d7fcf9f1b160c547315d5dacaa8c0f6e267d89a87cc4af2b7cea111` |

Both deliverables are self-contained glTF 2.0 GLBs with 267 nodes, 267 meshes/primitives, 14 materials, six embedded source-locked face textures, no external buffers, no negative/mirrored nodes, opaque single-sided materials, and `KHR_materials_unlit` source-photo rendering. Standard and web variants retain identical geometry, bounds, material structure, coordinate frame and visible feature inventory; only embedded texture resolution/packaging is reduced in the web file.

Computed world bounds for both GLBs are 482.6 x 43.25 x 749.85 mm. The 1.85 mm depth and 0.25 mm height over the published body dimensions are caused by the modeled visible face/handle/relief envelope. The audit's non-uniform ratio error is 0.3043%, with no dimension error or warning.

## Six face assets and source locks

| Face | Mode | Final size | Lineage result |
|---|---|---:|---|
| Front | `SOURCE_LOCKED_GENERATION` | 2244 x 200 | Exact real 4LFF primary; four carriers and real branding retained. |
| Rear | `SOURCE_LOCKED_GENERATION` | 2048 x 202 | Exact real four-GE primary; dual 460 W AC PSUs retained. |
| Left | `MULTI_REFERENCE_RECONSTRUCTION` | 2048 x 118 | Exact 4LFF real angles; physical-left landmarks retained. |
| Right | `MULTI_REFERENCE_RECONSTRUCTION` | 2048 x 118 | Exact 4LFF real angles; right-only rear vent retained. |
| Top | `MULTI_REFERENCE_RECONSTRUCTION` | 1194 x 2048 | Exact 4LFF real angles; two vent rows, latch, seams and labels retained. |
| Bottom | `GENERIC_BOTTOM_FALLBACK` | 1194 x 2048 | Conservative non-identifying galvanized sheet after documented search exhaustion. |

`source/face-source-lock.csv` primary-source hashes were recomputed and match the locked values. The six dedicated built-in image-generation prompt/input-role records are preserved in `qa/imagegen-prompts/`; no AI derivative or prior GLB render is used as a primary identity/style source. The canonical face files have distinct hashes; physical left/right are not mirrored, and bottom is neither the top nor a flipped top.

The standard GLB embeds the six full approved RGB face images. The web GLB embeds 1600 x 143 front, 1600 x 158 rear, 1536 x 89 left/right, and 896 x 1536 top/bottom RGB images. All embedded images are fully opaque; dark ports, vents and grilles are not transparency.

## Visible geometry gate

The final exterior is not a six-card box. It contains separate front ear bodies, four independent recessed LFF carriers with handles/status strips, operator and ESN relief, top seam/latch/vent relief, left/right-specific rail landmarks, a right-only rear vent, separate PCIe blanks/perforations, rear port-group recesses, two independent AC PSU blocks, fan relief/guards, IEC inlets, release levers and pull handles. Orthographic and oblique renders show the required parallax, seams, recesses, protrusions and closed exterior.

Feature review passed for:

- four LFF carrier faces in one row;
- Huawei on the physical-left front ear and RH1288 V3/Intel on the physical-right ear;
- four rear service RJ45 ports, management RJ45, two USB, VGA, serial and UID in the frozen order;
- two matched AC PSUs with fan, C14 inlet, green release detail and handle;
- no rear ears, no SFF/NVMe front, no 10GE/IB or two-GE rear substitution;
- different physical-left and physical-right side layouts;
- top cover latch, two slot-vent rows, cover seam and factory label groups;
- intentionally blank, non-identifying controlled bottom fallback.

## Structural audits

All five preserved audit files report `PASS`:

| Audit | Status | Errors | Warnings | Disposition |
|---|---|---:|---:|---|
| `qa/views-audit.json` | PASS | 0 | 3 | Reviewed: warnings are anti-aliased silhouette pixels; core transparent percentage is 0 on all six faces. |
| `qa/glb-audit-standard.json` | PASS | 0 | 1 | Reviewed: only untextured colored relief materials use non-neutral factors; all six photographic face materials remain neutral `[1,1,1,1]`. |
| `qa/glb-audit-web.json` | PASS | 0 | 1 | Same reviewed material warning as standard. |
| `qa/repair-before-pass2/glb-audit-standard.json` | PASS | 0 | 1 | Historical backup audit; not the final deliverable. |
| `qa/repair-before-pass2/glb-audit-web.json` | PASS | 0 | 1 | Historical backup audit; not the final deliverable. |

Latest actual-GLB normalized comparison panels are `qa/comparisons/front.png`, `rear.png`, `left.png`, `right.png`, `top.png`, and `bottom.png`. The stale pre-final normalized images were preserved under `qa/comparisons/normalized-before-final-reload/`; the current transparent WebGL canvas exports are under `qa/comparisons/raw-current/`. Feature-by-feature review found no face swap, mirror, large unmatched panel, missing component group or wrong port/PSU count. Numeric pixel differences remain diagnostic because real relief deliberately changes edge shading and occlusion.

## Independent WebGL loading gate

Two independent loaders were used: Three.js `GLTFLoader` and Babylon.js `SceneLoader`. Each loader actually loaded both final GLBs. The table counts the archived final viewer-capture batch.

| Viewer/model | Checker views | Light orthographic views | Archived final captures |
|---|---:|---:|---:|
| Three.js / standard | 10 | 6 | 16 |
| Three.js / web | 10 | 6 | 16 |
| Babylon.js / standard | 10 | 6 | 16 |
| Babylon.js / web | 10 | 6 | 16 |
| **Total** | **40** | **24** | **64** |

Each ten-view checker batch contains front, rear, left, right, top, bottom, front-left, front-right, rear-left and rear-right. The added light batch repeats all six orthographic views. Six further Three.js/standard transparent-canvas reloads produced the current `qa/comparisons/raw-current/` files after the stale-comparison check, so the complete final validation performed 70 confirmed GLB load events while retaining 64 named viewer-capture images. Every load reported the same bounds: 0.4826 x 0.04325 x 0.74985 m. Three.js reported 267 model children; Babylon.js reported 268 scene meshes including its root. No viewer loading error was recorded.

Final checker contact sheets:

- `qa/renders/final-three-standard-contact-sheet.png`
- `qa/renders/final-three-web-contact-sheet.png`
- `qa/renders/final-babylon-standard-contact-sheet.png`
- `qa/renders/final-babylon-web-contact-sheet.png`

Final light contact sheets:

- `qa/renders/final-three-standard-light-contact-sheet.png`
- `qa/renders/final-three-web-light-contact-sheet.png`
- `qa/renders/final-babylon-standard-light-contact-sheet.png`
- `qa/renders/final-babylon-web-light-contact-sheet.png`

Both viewers agree on front/rear orientation, physical left/right, opacity, branding, port order, PSU count and all six face assignments for both GLBs.

## Optional official 3D situation

No exact public official Huawei RH1288 V3 4LFF 3D payload was obtainable. Huawei's historic official viewer URL now redirects to a migration/maintenance page, and its public model resources are unavailable. The archived official viewer index is preserved unchanged at `source/optional-3d/Huawei-RH1288-V3-official-viewer-index-20221209.html`; its visible component naming points to an 8-SFF/DVD front and therefore does not prove the requested 4LFF exterior. Huawei's current download-all ZIP is also preserved unchanged and contains only SFF product images, not a 3D model. Nothing in `source/optional-3d/` replaced or contributed mesh data to the newly constructed GLBs.

## Remaining risks and final decision

1. Exact underside imagery was not found after official, interactive-viewer, PDF, video, reseller, marketplace, auction, used-equipment and multilingual searches. The controlled generic bottom is therefore the sole material limitation and forces `PASS_WITH_BOTTOM_FALLBACK` rather than `PASS`.
2. The historic official viewer payload remains unavailable; if Huawei later republishes an exact 4LFF official model, it should be preserved as an optional source and compared, not substituted automatically.
3. The exact internal SM210-versus-SM212 revision is not externally distinguishable. The delivered, visible four-GE exterior is frozen and verified, so this does not create an appearance ambiguity.
4. The visible modeled relief envelope exceeds the published body-only bounds by 1.85 mm in depth and 0.25 mm in height; this is within the documented audit tolerance and does not alter rack-span identity or face proportions.

All non-bottom exact-appearance, source-lineage, configuration, geometry, alpha, orientation, structural-audit, two-viewer, standard/web and reporting gates are satisfied. Final decision: **PASS_WITH_BOTTOM_FALLBACK**.
