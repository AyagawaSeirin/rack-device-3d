# HPE ProLiant DL360 Gen10 2.5-inch 3D model final report

## Final status

**PASS_WITH_BOTTOM_FALLBACK**

The two delivered GLBs are source-built exact-exterior replicas of the verified HPE ProLiant DL360 Gen10 1U SFF configuration. All required structural, source-lock, GLB, dual-WebGL, orthographic, oblique, alpha, close-up, and comparison gates pass. The only controlled exception is the underside: no usable exact-model underside evidence was found after the documented exhaustive search, so the deliberately plain opaque bottom remains `GENERIC_BOTTOM_FALLBACK` as required by the skill contract.

## Locked identity and installed configuration

- Manufacturer/product: Hewlett Packard Enterprise (HPE) ProLiant DL360 Gen10.
- Exterior variant: 1U SFF, standard 8SFF 2.5-inch front cage.
- Drive layout: eight visible HPE SFF Smart Carrier-style fronts in the exact standard 6+2 arrangement; no +2SFF, NVMe Premium, uFF, LFF, or rear-drive conversion.
- Front: exposed carriers, Universal Media Bay blank/grille, factory control area, HPE/ProLiant brand appearance retained, no security bezel.
- Rear: blank PCIe and FlexibleLOM apertures, embedded 4x1GbE, dedicated iLO, serial, two USB 3.0, VGA, no rear drive.
- Power: two HPE 500W Flex Slot Platinum hot-plug **AC** PSUs, with the source-visible 500W/94% rear appearance. No DC PSU variant is mixed in.
- Verified body dimensions: 434.6 W × 42.9 H × 707 D mm; nominal front rack span including ears: 482.6 mm.
- Coordinate convention: right-handed glTF; +X is device-right viewed from the front, +Y is up, +Z is front.

Authoritative configuration record: [`source/identity-manifest.md`](../../source/identity-manifest.md), status `VERIFIED`.

## Delivered self-built GLBs

| Tier | File | Exact size | SHA-256 |
|---|---|---:|---|
| standard | [`model/HPE-DL360G10-2.5inch.glb`](../../model/HPE-DL360G10-2.5inch.glb) | 10,584,756 bytes (10.094 MiB) | `36fba895befbc28185d3aeeea77c84315812fb14863fe54ca3231cb1d0e12597` |
| web | [`model/HPE-DL360G10-2.5inch-web.glb`](../../model/HPE-DL360G10-2.5inch-web.glb) | 6,383,624 bytes (6.088 MiB) | `785c9a0824eccb823b5be0036ea970161df776dc40312556d87151e6d4275900` |

Both files are self-built deliverables. Neither is an official or third-party mesh. Both contain 356 named exterior nodes, 22 meshes/primitives, 17 materials, eight embedded base-color images, no external buffer, no mirrored node transform, and measured bounds of 482.6 × 42.925 × 707.02 mm. The non-uniform dimension-ratio error is 0.0379%.

The final repair keeps the six source-locked face textures visually authoritative while moving coarse helper faces behind them. Visible geometry remains for the closed chassis, separate rack ears and real through-holes, carrier frame relief, top cover seam/latch, side rail attachment details, rear PSU frames, and other independently shaped exterior assemblies. This removes the former flat/coarse occlusion without replacing the model with a six-plane box.

Current parts manifests:

- [`qa/manifests/HPE-DL360G10-2.5inch-parts.json`](../manifests/HPE-DL360G10-2.5inch-parts.json)
- [`qa/manifests/HPE-DL360G10-2.5inch-web-parts.json`](../manifests/HPE-DL360G10-2.5inch-web-parts.json)

## Six independent face locks

| Face | Locked production mode | Result |
|---|---|---|
| front | `SOURCE_LOCKED_GENERATION` | Exact 8SFF 6+2 layout, HPE/ProLiant ears, optical/display blank and control region retained. |
| rear | `SOURCE_LOCKED_GENERATION` | Correct port order, blank option apertures, no rear drive and two 500W/94% AC PSU faces retained. |
| left | `MULTI_REFERENCE_RECONSTRUCTION` | Independent left-specific fastener/seam pattern; not derived by mirroring right. |
| right | `MULTI_REFERENCE_RECONSTRUCTION` | Independent right-specific fastener/seam and PSU-edge pattern; not derived by mirroring left. |
| top | `MULTI_REFERENCE_RECONSTRUCTION` | Closed two-piece cover, seam, latch, vents and source-agreed service labels retained. |
| bottom | `GENERIC_BOTTOM_FALLBACK` | Conservative opaque galvanized sheet only; no unsupported label, logo, vent, hole, foot, rail, seam or protrusion invented. |

All six primary-source SHA-256 values match the declarations, all six final PNGs exist, and every face has its own prompt/source record. The authoritative ledger is [`source/face-source-lock.csv`](../../source/face-source-lock.csv). The bottom-search exhaustion record is [`source/underside-search-log.md`](../../source/underside-search-log.md).

Six same-canvas source/render comparison sheets were rebuilt from the final formal standard GLB and inspected feature by feature:

- [`qa/comparisons/front.png`](../comparisons/front.png)
- [`qa/comparisons/rear.png`](../comparisons/rear.png)
- [`qa/comparisons/left.png`](../comparisons/left.png)
- [`qa/comparisons/right.png`](../comparisons/right.png)
- [`qa/comparisons/top.png`](../comparisons/top.png)
- [`qa/comparisons/bottom.png`](../comparisons/bottom.png)

The small outboard silhouettes visible in the rear orthographic render are depth-collapsed projections of the genuine front ears; no rear-ear nodes exist.

## Independent WebGL load gate

Two independent browser implementations loaded both formal GLBs directly:

1. Viewer A: custom native WebGL2 GLB parser/renderer.
2. Viewer B: Three.js r128 `GLTFLoader`.

Each implementation loaded each GLB in six orthographic views (`front`, `rear`, `left`, `right`, `top`, `bottom`) and four three-quarter views (`front-left`, `front-right`, `rear-left`, `rear-right`). Total actual loads: **40/40**.

All 40 screenshots are 1200 × 800, newer than the exact GLB they load, and were captured only after the viewer DOM reported `PASS` for the requested model tier and angle. The four contact sheets were visually inspected:

- [`viewer-a-standard-10views.png`](contact-sheets/viewer-a-standard-10views.png)
- [`viewer-a-web-10views.png`](contact-sheets/viewer-a-web-10views.png)
- [`viewer-b-standard-10views.png`](contact-sheets/viewer-b-standard-10views.png)
- [`viewer-b-web-10views.png`](contact-sheets/viewer-b-web-10views.png)

The views show consistent geometry and appearance across both renderers and both tiers: exact front carrier count/layout, factory branding, independent left/right surfaces, closed top/body, correct rear ports and two AC PSUs, and no open seams or missing faces in oblique views.

## Alpha and fine-detail inspection

Viewer A and Viewer B each loaded the standard GLB front on both light and dark checkerboards. The product surfaces stay opaque; checkerboard visibility is confined to the external canvas and verified rack-ear openings. The two ear materials are the only `MASK` materials. There is no partial-alpha chassis haze and no vent/port color-key transparency.

Evidence:

- [`qa/final/alpha-inspection/`](alpha-inspection/): four actual GLB checkerboard loads.
- [`left-rack-ear.png`](closeups/left-rack-ear.png)
- [`right-rack-ear-hpe-logo.png`](closeups/right-rack-ear-hpe-logo.png)
- [`drive-bays-controls-text.png`](closeups/drive-bays-controls-text.png)

The close-ups confirm the real ear silhouettes/holes, retained HPE mark, eight carrier fronts, blank bay and front controls.

## Automated audits

| Audit | Status | Errors | Warnings | Disposition |
|---|---:|---:|---:|---|
| six canonical PNG views | PASS | 0 | 6 | Expected silhouette/true-hole alpha-edge warnings; chassis cores are opaque and visually checked. |
| standard GLB | PASS | 0 | 3 | Ear-only `MASK`, its intentionally large transparent hole/canvas area, and non-neutral unlit helper colors; all visually verified. |
| web GLB | PASS | 0 | 3 | Same verified warning classes as standard. |

The root and final copies of all three audits were regenerated from the current formal files, for six audit JSONs total. Final copies:

- [`qa/final/views-audit.json`](views-audit.json)
- [`qa/final/glb-standard-audit.json`](glb-standard-audit.json)
- [`qa/final/glb-web-audit.json`](glb-web-audit.json)

Machine-readable completion proof: [`qa/final/final-gate-summary.json`](final-gate-summary.json). Its final status is `PASS_WITH_BOTTOM_FALLBACK`, all gate booleans are true, and `total_actual_loads` is 40.

## Official exact 3D status

HPE Product Bulletin, Support Center, product catalog/media library, PartSurfer, HPE Community and exact identifiers were searched for public 3D/CAD/AR files. No exact public official HPE 3D/CAD/AR model for this configuration was found. A public 2D Visio reference exists but is not a 3D asset, so it was not stored as an optional model and was not substituted for the self-built GLBs.

The unmodified search record is [`source/optional-3d/README.md`](../../source/optional-3d/README.md). `source/optional-3d/` contains only this record because there is no exact official model file to preserve.

## Preservation and remaining risk

The pre-final formal GLBs were preserved unchanged under `work/repair-before-final-overlay/`:

- standard backup SHA-256: `47c9a39ae5c9d9e4ea8d8fcf19d1429163974a7209ef6b633e850717445a4b41`
- web backup SHA-256: `ce820e795178394878e55ec9c7e77bb197f625ebb6d4be0551277c5ea20c9e52`

No directory was cleared, no existing high-cost face asset was regenerated during finalization, and no Git commit or push was performed.

Remaining risk is limited to the documented absence of an exact underside photograph/drawing. The bottom therefore cannot claim model-specific underside fasteners or labels; it intentionally contains none. This is a controlled skill-defined fallback and is the sole reason the final result is `PASS_WITH_BOTTOM_FALLBACK` instead of `PASS`. There are no remaining non-bottom blockers.
